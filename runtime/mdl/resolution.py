"""Resolution — Layer 4 · C4 (Component Contracts §Resolution).

The deterministic computation of applicability + in-force selection + precedence
into one version-pinned Resolved Mandate Set. On the deterministic path (I1): no
wall-clock, no randomness, no network. Identical (context, versions) ⇒ identical
set.

Failure conditions: an unresolved same-level conflict ⇒ UNRESOLVED (never a
fabricated winner). A resolved set that is *empty* is a legitimate result (no
mandate governs this context), distinct from UNRESOLVED.
"""

from __future__ import annotations

from typing import Optional

from .jurisdiction import ConflictItem, Jurisdiction
from .domain import MandateVersion, ResolutionContext
from .registry import Registry
from .versioning import Versioning


class ResolvedMandateSet:
    def __init__(self, ordered: list[MandateVersion], conflict: Optional[ConflictItem]):
        self.ordered = ordered
        self.conflict = conflict

    @property
    def unresolved(self) -> bool:
        return self.conflict is not None

    @property
    def refs(self) -> list[str]:
        return [v.ref for v in self.ordered]


class Resolution:
    def __init__(self, registry: Registry, versioning: Versioning, jurisdiction: Jurisdiction):
        self._registry = registry
        self._versioning = versioning
        self._jurisdiction = jurisdiction

    def resolve(self, ctx: ResolutionContext) -> ResolvedMandateSet:
        applicable: list[MandateVersion] = []
        for mandate_id in self._registry.all_mandate_ids():
            version = self._versioning.in_force_version(mandate_id, ctx.as_of)
            if version is None:
                continue  # not in force at as_of — simply does not apply
            if version.applicability.matches(ctx):
                applicable.append(version)

        ordered, conflict = self._jurisdiction.order(applicable, ctx.governing_event_id)
        return ResolvedMandateSet(ordered, conflict)
