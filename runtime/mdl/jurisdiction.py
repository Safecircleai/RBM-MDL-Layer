"""Jurisdiction — Layer 2 · C3 (Component Contracts §Jurisdiction).

Applies the ratified precedence stack (R2, FEDERAL-anchored two-class model,
MDL_Lifecycle.md §4) and inheritance semantics. Produces a precedence-ordered
ordering, or an UNRESOLVED marker + Conflict-Review Item.

Owns: the *application* of the stack. Cannot own: authoring the stack, or ad-hoc
conflict resolution. Same-level equal-date ties are flagged, never auto-resolved
(I4).
"""

from __future__ import annotations

from typing import Optional

from .domain import (
    JurisClass,
    MandateVersion,
    layer_class,
    layer_rank,
)


class ConflictItem:
    """A first-class same-level, equal-date conflict (Domain Model §17).

    Its resolution is a human/ratified act; while flagged, resolutions for the
    conflicting context return UNRESOLVED (State Model §4).
    """

    def __init__(self, refs: list[str], context_id: str):
        self.refs = refs
        self.context_id = context_id

    @property
    def ref(self) -> str:
        return f"conflict:{self.context_id}:{'+'.join(sorted(self.refs))}"


class Jurisdiction:
    def order(self, versions: list[MandateVersion], context_id: str) -> tuple[list[MandateVersion], Optional[ConflictItem]]:
        """Precedence-order versions; flag an ambiguous same-tier tie.

        Precedence: lower rank wins (FEDERAL=100 outranks INTERNAL=800). Class-1
        always outranks Class-2 (rule 1: no Class-2 layer may OVERRIDE Class-1).
        Ties at the same rank are broken by the newer ``effective_from``; an
        equal-and-ambiguous tie is flagged (rule 3, I4).
        """
        # Detect same-rank, equal-effective-date ambiguity among OVERRIDE versions
        # (only OVERRIDE fights for precedence; FLOOR/ADDITIVE accumulate).
        by_rank: dict[int, list[MandateVersion]] = {}
        for v in versions:
            by_rank.setdefault(layer_rank(v.jurisdiction_layer), []).append(v)

        for rank, group in by_rank.items():
            overrides = [v for v in group if v.inheritance.value == "OVERRIDE"]
            if len(overrides) > 1:
                dates = {v.effectivity.effective_from for v in overrides}
                if len(dates) == 1:
                    # same rank, same effective date, both OVERRIDE → cannot pick (I4)
                    return [], ConflictItem([v.ref for v in overrides], context_id)

        ordered = sorted(
            versions,
            key=lambda v: (
                0 if layer_class(v.jurisdiction_layer) is JurisClass.GOVERNMENTAL else 1,
                layer_rank(v.jurisdiction_layer),
                # within a rank, newer effective date first for deterministic order
                _neg_date_key(v.effectivity.effective_from),
                v.mandate_id,
            ),
        )
        return ordered, None


def _neg_date_key(iso_date: str) -> tuple:
    """Sort newer dates first deterministically without arithmetic on strings."""
    # Invert each character's ordinal so a later date sorts earlier.
    return tuple(-ord(c) for c in iso_date)
