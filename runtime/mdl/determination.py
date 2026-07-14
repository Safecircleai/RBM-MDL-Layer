"""Determination — Layer 5 · C5 + C7 (Component Contracts §Determination).

Evaluates entity state against the Resolved Mandate Set → the authoritative
compliance result (status + per-rule gaps) and the binding Financial-Override
Outcome. Authoritative, not advisory (I6); deterministic and model-free (I1).

Cannot own: discipline-specific reasoning, booking the economic effect, or
computing a tax amount. It expresses the financial-override *supremacy* as an
outcome, never an action (I3). Era-1 operational mandates carry no financial
rule, so the outcome is NONE — the mechanism is present, not the tax content.
"""

from __future__ import annotations

from .domain import (
    Determination,
    DeterminationStatus,
    FinancialOutcome,
    FinancialOverrideOutcome,
    Op,
    ResolutionContext,
    RuleCategory,
    RuleGap,
)
from .resolution import ResolvedMandateSet


class DeterminationEngine:
    def determine(self, resolved: ResolvedMandateSet, ctx: ResolutionContext) -> Determination:
        # Same-level unresolved conflict is a first-class outcome, not an error (I4).
        if resolved.unresolved:
            return Determination(
                status=DeterminationStatus.UNRESOLVED,
                resolved_refs=tuple(resolved.refs),
                gaps=(),
                financial=FinancialOverrideOutcome(),
                conflict_ref=resolved.conflict.ref,
            )

        gaps: list[RuleGap] = []
        financial = FinancialOverrideOutcome()  # default NONE

        for version in resolved.ordered:
            for rule in version.rules:
                satisfied = rule.evaluate(ctx.attributes)
                if rule.category is RuleCategory.FINANCIAL_POLICY:
                    financial = self._financial_outcome(version.ref, rule, satisfied, financial)
                    # A financial-policy rule also participates in compliance.
                if not satisfied:
                    reason = (
                        f"attribute '{rule.attribute}' absent"
                        if rule.attribute not in ctx.attributes
                        else f"attribute '{rule.attribute}' does not satisfy {rule.op.value}"
                    )
                    gaps.append(
                        RuleGap(
                            mandate_ref=version.ref,
                            rule_id=rule.rule_id,
                            category=rule.category.value,
                            attribute=rule.attribute,
                            reason=reason,
                        )
                    )

        status = DeterminationStatus.COMPLIANT if not gaps else DeterminationStatus.NON_COMPLIANT
        return Determination(
            status=status,
            resolved_refs=tuple(resolved.refs),
            gaps=tuple(gaps),
            financial=financial,
            conflict_ref=None,
        )

    @staticmethod
    def _financial_outcome(ref: str, rule, satisfied: bool, current: FinancialOverrideOutcome) -> FinancialOverrideOutcome:
        # A financial-policy rule expresses exemption. The highest-precedence
        # (earliest in the ordered set) deciding rule wins; we keep the first set.
        if current.outcome is not FinancialOutcome.NONE:
            return current
        outcome = FinancialOutcome.EXEMPT if satisfied else FinancialOutcome.NOT_EXEMPT
        return FinancialOverrideOutcome(
            outcome=outcome,
            deciding_version=ref,
            reason=rule.description or rule.rule_id,
        )
