"""MDLRuntime — the facade that wires the eleven components into the request
pipeline (Runtime Specification §2).

    Interface (authenticate, scope)
      → Resolution (Registry + Versioning + Jurisdiction)
      → Determination (+ Financial-Override)
      → Snapshot (freeze, idempotent per governing event)
      → Override (apply in-force overlay; snapshot unchanged)
      → Interface (return runtime outcome)
      ⟿ Audit (record)   ⟿ Distribution (emit event)

The pipeline traverses once, left to right, no back-edges. Audit and Distribution
are side effects taken *after* the outcome is produced; they never alter the
determination.

Determinism (I1): the deterministic path (resolve→determine→snapshot) reads no
wall-clock — effectivity uses the context ``as_of``. The single sanctioned
wall-clock read is override expiry (§7), which affects only the runtime overlay.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from .audit import AuditTrail
from .determination import DeterminationEngine
from .distribution import Distribution
from .domain import (
    Determination,
    DeterminationStatus,
    ResolutionContext,
    Snapshot,
)
from .governance import Governance
from .interface import ConsumerDirectory, ConsumerRegistration
from .jurisdiction import Jurisdiction
from .override import OverrideRegistry
from .registry import Registry
from .resolution import Resolution
from .snapshot import SnapshotStore
from .versioning import Versioning


@dataclass
class DeterminationResult:
    """The runtime outcome returned to a consumer (the read-path response)."""
    status: DeterminationStatus
    admissible: bool                 # true iff frozen into a snapshot (Constitution §1.4)
    recorded: bool                   # true iff the snapshot write succeeded
    permits_action: bool             # the single binding bit the consumer obeys
    snapshot_id: Optional[str]
    determination: Determination
    override_applied: bool
    governing_event_id: str
    as_of: str

    def to_wire(self) -> dict:
        det = self.determination
        return {
            "status": self.status.value,
            "admissible": self.admissible,
            "recorded": self.recorded,
            "permits_action": self.permits_action,
            "snapshot_id": self.snapshot_id,
            "override_applied": self.override_applied,
            "governing_event_id": self.governing_event_id,
            "as_of": self.as_of,
            "mandate_versions": list(det.resolved_refs),
            "gaps": [
                {
                    "mandate": g.mandate_ref,
                    "rule_id": g.rule_id,
                    "category": g.category,
                    "attribute": g.attribute,
                    "reason": g.reason,
                }
                for g in det.gaps
            ],
            "financial_override": {
                "outcome": det.financial.outcome.value,
                "deciding_version": det.financial.deciding_version,
                "reason": det.financial.reason,
            },
            "conflict_ref": det.conflict_ref,
        }


class MDLRuntime:
    def __init__(self, clock: Callable[[], str], now: Callable[[], str]):
        """``clock`` stamps audit/snapshot metadata (off the deterministic path).
        ``now`` is the sanctioned current-instant read for override expiry."""
        self.audit = AuditTrail(clock)
        self.registry = Registry(self.audit)
        self.versioning = Versioning(self.registry)
        self.jurisdiction = Jurisdiction()
        self.resolution = Resolution(self.registry, self.versioning, self.jurisdiction)
        self.determination = DeterminationEngine()
        self.snapshots = SnapshotStore(self.audit, clock)
        self.overrides = OverrideRegistry(self.audit, clock, now)
        self.distribution = Distribution(clock)
        self.governance = Governance(self.registry, self.versioning, self.audit)
        self.consumers = ConsumerDirectory()

    # -- registration ---------------------------------------------------------
    def register_consumer(self, reg: ConsumerRegistration) -> ConsumerRegistration:
        return self.consumers.register(reg)

    # -- the determination pipeline (§2) -------------------------------------
    def determine(self, ctx: ResolutionContext, api_key: str) -> DeterminationResult:
        # Interface: authenticate + scope to least-privilege projection (I10).
        reg = self.consumers.authenticate(api_key)
        self.consumers.authorize_determination(reg, ctx.node_type, ctx.jurisdiction.value)

        # Resolution → Determination (deterministic path).
        resolved = self.resolution.resolve(ctx)
        det = self.determination.determine(resolved, ctx)

        # UNRESOLVED / INSUFFICIENT are honest non-results: no snapshot, not
        # admissible, action refused (fail closed — Runtime Spec §7).
        if det.status in (DeterminationStatus.UNRESOLVED, DeterminationStatus.INSUFFICIENT):
            self.audit.append("determination", reg.node_id, "DETERMINATION_UNRESOLVED",
                              ctx.governing_event_id, {"status": det.status.value})
            return DeterminationResult(
                status=det.status,
                admissible=False,
                recorded=False,
                permits_action=False,
                snapshot_id=None,
                determination=det,
                override_applied=False,
                governing_event_id=ctx.governing_event_id,
                as_of=ctx.as_of,
            )

        # Snapshot: freeze (idempotent per governing event). A snapshot failure
        # means the determination is unrecorded and MUST NOT be returned as
        # recorded — the consumer is told and fails closed.
        try:
            snapshot: Snapshot = self.snapshots.freeze(ctx, resolved, det)
            recorded = True
        except Exception:
            self.audit.append("determination", reg.node_id, "DETERMINATION_UNRECORDED",
                              ctx.governing_event_id, {})
            return DeterminationResult(
                status=det.status,
                admissible=False,
                recorded=False,
                permits_action=False,
                snapshot_id=None,
                determination=det,
                override_applied=False,
                governing_event_id=ctx.governing_event_id,
                as_of=ctx.as_of,
            )

        # Override: apply any in-force overlay to the runtime outcome; the
        # snapshot is unchanged. Effectiveness evaluated at read time (§7).
        effective_status = det.status
        override_applied = False
        if det.status is DeterminationStatus.NON_COMPLIANT:
            active = self.overrides.effective_for(snapshot.snapshot_id)
            if active is not None:
                effective_status = DeterminationStatus.COMPLIANT
                override_applied = True

        permits = effective_status is DeterminationStatus.COMPLIANT

        # Side effects: Audit the determination, Distribution emits the event —
        # publish-after-commit, off the return path's critical section.
        self.audit.append(
            "determination",
            reg.node_id,
            "DETERMINATION_RECORDED",
            snapshot.snapshot_id,
            {
                "status": det.status.value,
                "effective_status": effective_status.value,
                "override_applied": override_applied,
                "governing_event_id": ctx.governing_event_id,
                "correlation_id": ctx.correlation_id,
            },
        )
        self.distribution.publish("VALIDATION_RECORDED", snapshot.snapshot_id, ctx.jurisdiction.value)

        return DeterminationResult(
            status=effective_status,
            admissible=True,
            recorded=recorded,
            permits_action=permits,
            snapshot_id=snapshot.snapshot_id,
            determination=det,
            override_applied=override_applied,
            governing_event_id=ctx.governing_event_id,
            as_of=ctx.as_of,
        )
