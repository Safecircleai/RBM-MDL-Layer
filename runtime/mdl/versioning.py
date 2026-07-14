"""Versioning — Layer 3 · C2 (Component Contracts §Versioning).

Owns version identity assignment, supersession linkage, and effectivity
evaluation: "the in-force version at date D". "in force at D" is a pure function
of (chain, D) — no wall-clock (I1); effectivity uses the supplied ``as_of`` only.

Cannot own: mutation/deletion of a prior version; mandate content authorship.
"""

from __future__ import annotations

from typing import Optional

from .domain import MandateVersion, MandateVersionState
from .registry import Registry


class Versioning:
    def __init__(self, registry: Registry):
        self._registry = registry

    def next_version_number(self, mandate_id: str) -> int:
        head = self._registry.head(mandate_id)
        return 1 if head is None else head + 1

    def in_force_version(self, mandate_id: str, as_of: str) -> Optional[MandateVersion]:
        """The single in-force version of a mandate at ``as_of``.

        Deterministic selection: among published, non-void, non-superseded
        versions whose effectivity window contains ``as_of``, pick the one with
        the newest ``effective_from`` (State Model §1 tiebreak), then highest
        version number. Returns None if none is in force (a gap Resolution
        reports honestly, never guesses around).
        """
        candidates = [
            v
            for v in self._registry.chain(mandate_id)
            if v.state in (MandateVersionState.PUBLISHED, MandateVersionState.SUPERSEDED)
            and v.state is not MandateVersionState.VOID
            and v.effectivity.in_force(as_of)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda v: (v.effectivity.effective_from, v.version))
        return candidates[-1]
