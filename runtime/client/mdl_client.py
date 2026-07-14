"""MDL determination client — the single reusable consumer contract.

CANONICAL COPY. This module is *owned by RBM-MDL-Layer* and vendored verbatim
into every consuming node (Viral-Bot-Machine, Prometheus, Content Factory, Video
Factory). Consumers do not fork or re-implement it — "consumers reference; they
never own" (README rule 2). To keep the contract identical everywhere it depends
only on the Python standard library.

The contract in one sentence: a consumer submits a deterministic
ResolutionContext to MDL, receives an authoritative determination bound to an
immutable snapshot, and **obeys it** — it never fabricates a fallback outcome.

Fail-closed guarantee (Runtime Spec §7): every error path — unreachable runtime,
non-2xx, malformed body, non-admissible determination — results in *action
refused*, never *action allowed*. There is no code path in which a consumer
proceeds without an admissible COMPLIANT determination.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional

CONTRACT_VERSION = "1.0.0-era1"


def _safe_detail(exc: "urllib.error.HTTPError") -> str:
    try:
        body = json.loads(exc.read().decode("utf-8"))
        return str(body.get("detail", body))
    except Exception:
        return exc.reason if getattr(exc, "reason", None) else "unknown error"


class MDLDenied(Exception):
    """The action is NOT permitted. Consumers must treat this as a hard stop.

    Carries the determination payload when one was produced (gaps, snapshot id),
    and ``None`` when the runtime could not be reached at all.
    """

    def __init__(self, message: str, determination: Optional["MDLDetermination"] = None):
        super().__init__(message)
        self.determination = determination


class MDLUnavailable(MDLDenied):
    """The MDL runtime could not be reached or answered unusably.

    A subclass of MDLDenied *by design*: an unreachable authority means the action
    is refused (no fallback), not allowed. Catching MDLDenied catches this too.
    """


@dataclass
class MDLDetermination:
    status: str
    admissible: bool
    recorded: bool
    permits_action: bool
    snapshot_id: Optional[str]
    mandate_versions: list = field(default_factory=list)
    gaps: list = field(default_factory=list)
    financial_override: dict = field(default_factory=dict)
    override_applied: bool = False
    governing_event_id: Optional[str] = None
    raw: dict = field(default_factory=dict)

    @property
    def is_permitted(self) -> bool:
        # The single binding bit — COMPLIANT, admissible (snapshotted), recorded.
        return bool(self.permits_action and self.admissible and self.recorded and self.snapshot_id)

    def gap_summary(self) -> str:
        return "; ".join(f"{g.get('mandate')}:{g.get('rule_id')} ({g.get('reason')})" for g in self.gaps) or "none"

    @classmethod
    def from_wire(cls, body: dict) -> "MDLDetermination":
        return cls(
            status=body.get("status", "INSUFFICIENT"),
            admissible=bool(body.get("admissible", False)),
            recorded=bool(body.get("recorded", False)),
            permits_action=bool(body.get("permits_action", False)),
            snapshot_id=body.get("snapshot_id"),
            mandate_versions=body.get("mandate_versions", []),
            gaps=body.get("gaps", []),
            financial_override=body.get("financial_override", {}),
            override_applied=bool(body.get("override_applied", False)),
            governing_event_id=body.get("governing_event_id"),
            raw=body,
        )


class MDLClient:
    def __init__(self, base_url: str, api_key: str, node_type: str, timeout: float = 5.0):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._node_type = node_type
        self._timeout = timeout

    @classmethod
    def from_env(cls, node_type: str, timeout: float = 5.0) -> "MDLClient":
        base = os.getenv("MDL_BASE_URL", "").strip()
        key = os.getenv("MDL_API_KEY", "").strip()
        if not base or not key:
            # Fail closed on misconfiguration: a consumer without an MDL endpoint
            # must refuse the gated action, not silently skip the gate.
            raise MDLUnavailable("MDL_BASE_URL / MDL_API_KEY not configured; gated action refused")
        return cls(base, key, node_type, timeout)

    def determine(
        self,
        *,
        entity_type: str,
        entity_id: str,
        as_of: str,
        governing_event_id: str,
        purpose: Optional[str] = None,
        jurisdiction: str = "INTERNAL",
        service_type: Optional[str] = None,
        attributes: Optional[Mapping[str, Any]] = None,
        correlation_id: Optional[str] = None,
    ) -> MDLDetermination:
        """Submit one determination request. Raises MDLUnavailable on transport
        failure (fail closed). Returns the determination (which may be
        NON_COMPLIANT — the caller checks ``is_permitted`` or uses ``require``)."""
        payload = {
            "node_type": self._node_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "jurisdiction": jurisdiction,
            "as_of": as_of,
            "governing_event_id": governing_event_id,
            "purpose": purpose,
            "service_type": service_type,
            "attributes": dict(attributes or {}),
            "correlation_id": correlation_id,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self._base_url}/v1/determinations",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json", "X-MDL-Key": self._api_key},
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = _safe_detail(exc)
            raise MDLUnavailable(f"MDL refused determination (HTTP {exc.code}): {detail}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise MDLUnavailable(f"MDL runtime unreachable: {exc}")
        except (ValueError, json.JSONDecodeError) as exc:
            raise MDLUnavailable(f"MDL returned an unreadable body: {exc}")
        return MDLDetermination.from_wire(body)

    def require(self, **kwargs) -> MDLDetermination:
        """Determine and enforce: raise MDLDenied unless the action is permitted.

        This is the one call a production path uses to make itself impossible to
        execute without an admissible COMPLIANT MDL determination."""
        det = self.determine(**kwargs)
        if not det.is_permitted:
            raise MDLDenied(
                f"MDL determination '{det.status}' does not permit the action "
                f"(gaps: {det.gap_summary()})",
                determination=det,
            )
        return det
