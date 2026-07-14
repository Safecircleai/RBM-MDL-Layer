"""Snapshot — Layer 6 · C6 (Component Contracts §Snapshot).

The freezing and immutable retention of determinations. Guarantees:
- **write-once immutability** — no field ever altered (I2);
- **idempotency per governing event** — the same governing event yields exactly
  one snapshot; concurrent/retried creation converges on it (the load-bearing
  guarantee, Runtime Spec §9);
- **reproducibility** — the determination is recomputable from snapshot + pinned
  versions, yielding an identical result;
- **isolation under propagation** — a later version never alters an existing
  snapshot.

The snapshot id is the canonical content hash, so a replay of identical inputs
reproduces the identical id.
"""

from __future__ import annotations

import threading
from typing import Callable, Optional

from .audit import AuditTrail
from .domain import (
    Determination,
    ResolutionContext,
    Snapshot,
    canonical_hash,
)
from .resolution import ResolvedMandateSet


class SnapshotStore:
    def __init__(self, audit: AuditTrail, clock: Callable[[], str]):
        self._audit = audit
        self._clock = clock
        self._lock = threading.Lock()
        self._by_id: dict[str, Snapshot] = {}
        self._by_event: dict[str, str] = {}   # governing_event_id -> snapshot_id

    def freeze(self, ctx: ResolutionContext, resolved: ResolvedMandateSet, det: Determination) -> Snapshot:
        pinned = tuple(v.content_fingerprint() for v in resolved.ordered)
        det_payload = {
            "status": det.status.value,
            "resolved_refs": list(det.resolved_refs),
            "gaps": [
                {
                    "mandate_ref": g.mandate_ref,
                    "rule_id": g.rule_id,
                    "category": g.category,
                    "attribute": g.attribute,
                    "reason": g.reason,
                }
                for g in det.gaps
            ],
            "conflict_ref": det.conflict_ref,
        }
        financial_payload = {
            "outcome": det.financial.outcome.value,
            "deciding_version": det.financial.deciding_version,
            "reason": det.financial.reason,
        }
        # Deterministic content id — excludes the wall-clock creation timestamp so
        # a replay of identical inputs reproduces the identical snapshot id.
        content = {
            "governing_event_id": ctx.governing_event_id,
            "frozen_context": ctx.frozen_input(),
            "pinned_versions": list(pinned),
            "determination": det_payload,
            "financial_override": financial_payload,
        }
        snapshot_id = "snap_" + canonical_hash(content)[:32]

        with self._lock:
            # Idempotency per governing event: converge on one snapshot.
            existing_id = self._by_event.get(ctx.governing_event_id)
            if existing_id is not None:
                return self._by_id[existing_id]

            snapshot = Snapshot(
                snapshot_id=snapshot_id,
                governing_event_id=ctx.governing_event_id,
                frozen_context=content["frozen_context"],
                pinned_versions=pinned,
                determination=det_payload,
                financial_override=financial_payload,
                created_at=self._clock(),
            )
            self._by_id[snapshot_id] = snapshot
            self._by_event[ctx.governing_event_id] = snapshot_id

        self._audit.append(
            stream="snapshot",
            actor="mdl-runtime",
            act="SNAPSHOT_CREATED",
            object_ref=snapshot_id,
            detail={"governing_event_id": ctx.governing_event_id, "status": det.status.value},
        )
        return snapshot

    def get(self, snapshot_id: str) -> Optional[Snapshot]:
        with self._lock:
            return self._by_id.get(snapshot_id)

    def for_event(self, governing_event_id: str) -> Optional[Snapshot]:
        with self._lock:
            sid = self._by_event.get(governing_event_id)
            return self._by_id.get(sid) if sid else None
