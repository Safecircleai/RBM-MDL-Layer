"""Override — Layer 7 · C8 (Component Contracts §Override).

Dual-authorization enforcement and *runtime effectiveness evaluation*. An
override modifies the runtime outcome for a non-compliant determination without
ever mutating its bound Snapshot (I2).

- requestor ≠ approver (self-approval rejected);
- effectiveness is evaluated **at read time** against the current instant — never
  stored as an effective boolean; expired/revoked overrides are inert;
- expiry needs no write (derived), so it cannot be "missed" by a crash.

This is the single sanctioned wall-clock read (Runtime Spec §7): it affects only
the runtime overlay, never the frozen snapshot.
"""

from __future__ import annotations

import threading
import uuid
from typing import Callable, Optional

from .audit import AuditTrail
from .domain import Override, OverrideState
from .errors import AuthoringError


class OverrideRegistry:
    def __init__(self, audit: AuditTrail, clock: Callable[[], str], now: Callable[[], str]):
        self._audit = audit
        self._clock = clock          # audit timestamps
        self._now = now              # the sanctioned current-instant read
        self._lock = threading.Lock()
        self._by_id: dict[str, Override] = {}
        self._by_snapshot: dict[str, list[str]] = {}

    def request(self, snapshot_id: str, requestor: str, reason: str, expiry: str) -> Override:
        override = Override(
            override_id="ovr_" + uuid.uuid4().hex[:16],
            snapshot_id=snapshot_id,
            requestor=requestor,
            approver=None,
            reason=reason,
            expiry=expiry,
            created_at=self._clock(),
            state=OverrideState.REQUESTED,
        )
        with self._lock:
            self._by_id[override.override_id] = override
            self._by_snapshot.setdefault(snapshot_id, []).append(override.override_id)
        self._audit.append("override", requestor, "OVERRIDE_REQUESTED", override.override_id,
                           {"snapshot_id": snapshot_id, "expiry": expiry})
        return override

    def approve(self, override_id: str, approver: str) -> Override:
        with self._lock:
            override = self._by_id[override_id]
            if approver == override.requestor:
                raise AuthoringError("override self-approval is illegal (requestor ≠ approver)")
            if override.state is not OverrideState.REQUESTED:
                raise AuthoringError(f"override {override_id} is not awaiting approval")
            override = override.with_state(state=OverrideState.APPROVED, approver=approver)
            self._by_id[override_id] = override
        self._audit.append("override", approver, "OVERRIDE_APPROVED", override_id, {})
        return override

    def revoke(self, override_id: str, actor: str) -> Override:
        with self._lock:
            override = self._by_id[override_id]
            override = override.with_state(
                state=OverrideState.REVOKED, revoked_at=self._clock(), revoked_by=actor
            )
            self._by_id[override_id] = override
        self._audit.append("override", actor, "OVERRIDE_REVOKED", override_id, {})
        return override

    def effective_for(self, snapshot_id: str) -> Optional[Override]:
        """Return an in-force override for the snapshot, evaluated at read time.

        Effectiveness = Approved AND now < expiry AND not revoked. Computed each
        call; never cached as a stored flag.
        """
        now = self._now()
        with self._lock:
            ids = self._by_snapshot.get(snapshot_id, [])
            for oid in ids:
                o = self._by_id[oid]
                if o.state is OverrideState.APPROVED and o.revoked_at is None and now < o.expiry:
                    return o
        return None
