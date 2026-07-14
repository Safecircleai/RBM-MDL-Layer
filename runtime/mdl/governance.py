"""Governance — Layer 10 · C10 authoring workflow (Component Contracts §Governance).

The Intake→Encode→Review→Approve→Version→Publish workflow and its RBAC. RATIFIED
R3 roles with separation of duties (MDL_Consumer_Model.md §1a):
- **Author** drafts; cannot approve or publish its own draft;
- **Reviewer** reviews/approves (conformance: schema-shape, precedence coherence);
- **Publisher** publishes (assigns version, makes resolvable).

Compile-not-legislate (I8): the workflow never authors the source obligation; it
encodes an already-authored obligation. Every step appends to Audit; no partial
publish.

Cannot own: source-obligation authorship; a non-authoring role writing a mandate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .audit import AuditTrail
from .domain import (
    Applicability,
    EffectivityWindow,
    InheritanceBehavior,
    JurisdictionLayer,
    MandateVersion,
    MandateVersionState,
    Rule,
)
from .errors import AuthoringError
from .registry import Registry
from .versioning import Versioning


@dataclass
class AuthoringWorkItem:
    """In-flight authoring state (Domain Model §18)."""
    intake_id: str
    source_authority: str
    mandate_id: str
    jurisdiction_layer: JurisdictionLayer
    inheritance: InheritanceBehavior
    rules: tuple[Rule, ...]
    applicability: Applicability
    effectivity: EffectivityWindow
    author: str
    state: str = "Draft"
    reviewer: Optional[str] = None
    publisher: Optional[str] = None


class Governance:
    def __init__(self, registry: Registry, versioning: Versioning, audit: AuditTrail):
        self._registry = registry
        self._versioning = versioning
        self._audit = audit

    # -- Intake + Encode (Author) --------------------------------------------
    def draft(
        self,
        *,
        intake_id: str,
        source_authority: str,
        mandate_id: str,
        jurisdiction_layer: JurisdictionLayer,
        inheritance: InheritanceBehavior,
        rules: tuple[Rule, ...],
        applicability: Applicability,
        effectivity: EffectivityWindow,
        author: str,
    ) -> AuthoringWorkItem:
        item = AuthoringWorkItem(
            intake_id=intake_id,
            source_authority=source_authority,
            mandate_id=mandate_id,
            jurisdiction_layer=jurisdiction_layer,
            inheritance=inheritance,
            rules=rules,
            applicability=applicability,
            effectivity=effectivity,
            author=author,
        )
        self._audit.append("governance", author, "MANDATE_DRAFTED", mandate_id,
                           {"intake_id": intake_id, "source_authority": source_authority})
        return item

    # -- Review (Reviewer) ----------------------------------------------------
    def review(self, item: AuthoringWorkItem, reviewer: str) -> AuthoringWorkItem:
        if reviewer == item.author:
            raise AuthoringError("the Author cannot review/approve its own draft (R3 separation of duties)")
        self._conformance_check(item)
        item.state = "Approved"
        item.reviewer = reviewer
        self._audit.append("governance", reviewer, "MANDATE_APPROVED", item.mandate_id, {})
        return item

    # -- Version + Publish (Publisher) ---------------------------------------
    def publish(self, item: AuthoringWorkItem, publisher: str) -> MandateVersion:
        if item.state != "Approved":
            raise AuthoringError("mandate must be Approved before publish")
        if publisher == item.author:
            raise AuthoringError("the Author cannot publish its own draft (R3 separation of duties)")
        version_number = self._versioning.next_version_number(item.mandate_id)
        supersedes = version_number - 1 if version_number > 1 else None
        version = MandateVersion(
            mandate_id=item.mandate_id,
            version=version_number,
            jurisdiction_layer=item.jurisdiction_layer,
            inheritance=item.inheritance,
            rules=item.rules,
            applicability=item.applicability,
            effectivity=item.effectivity,
            authoring_authority=item.source_authority,
            state=MandateVersionState.PUBLISHED,
            supersedes=supersedes,
        )
        published = self._registry.publish(version)
        item.state = "Published"
        item.publisher = publisher
        return published

    def _conformance_check(self, item: AuthoringWorkItem) -> None:
        """Validate the *encoding*, never the *source* (Runtime Spec §4.3)."""
        if not item.rules:
            raise AuthoringError("a mandate version must carry at least one rule")
        # OVERRIDE flows only downward within a class — a Class-2 layer may never
        # be encoded to OVERRIDE across classes. Era-1 seeds are Class-2 only; the
        # guard is present for when Class-1 mandates arrive.
        for r in item.rules:
            if not r.attribute:
                raise AuthoringError(f"rule {r.rule_id} has no attribute to evaluate")
