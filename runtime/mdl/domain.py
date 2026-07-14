"""MDL domain objects (engineering/MDL_Domain_Model.md).

Conceptual objects made concrete as immutable dataclasses. Everything that the
Domain Model marks "immutable once Published / once Snapshotted" is a frozen
dataclass here; the frozen-ness *is* the constitutional guarantee made physical
(Persistence Model §3).

No object exists here that a Core capability (C1–C11) does not already require.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Mapping, Optional


# ---------------------------------------------------------------------------
# Jurisdiction stack — RATIFIED (R2), the FEDERAL-anchored two-class model
# (MDL_Lifecycle.md §4). Ranks carry gaps so a future tier inserts without
# renumbering. Era 1 seeds use only the Class-2 operational layers, but the
# whole ratified stack is present so resolution is correct end-to-end.
# ---------------------------------------------------------------------------
class JurisClass(str, Enum):
    GOVERNMENTAL = "governmental"   # Class 1 — legal spine, OVERRIDE-precedence
    CONTRACTUAL = "contractual"     # Class 2 — FLOOR/ADDITIVE only, never over Class 1


class JurisdictionLayer(str, Enum):
    FEDERAL = "FEDERAL"
    STATE = "STATE"
    COUNTY = "COUNTY"
    MUNICIPAL = "MUNICIPAL"
    PRIME_CONTRACT = "PRIME_CONTRACT"
    PROGRAM = "PROGRAM"
    INTERNAL = "INTERNAL"


# rank (lower wins precedence) and class per R2 §4 rule 4.
_LAYER_META = {
    JurisdictionLayer.FEDERAL: (100, JurisClass.GOVERNMENTAL),
    JurisdictionLayer.STATE: (200, JurisClass.GOVERNMENTAL),
    JurisdictionLayer.COUNTY: (300, JurisClass.GOVERNMENTAL),
    JurisdictionLayer.MUNICIPAL: (400, JurisClass.GOVERNMENTAL),
    JurisdictionLayer.PRIME_CONTRACT: (600, JurisClass.CONTRACTUAL),
    JurisdictionLayer.PROGRAM: (700, JurisClass.CONTRACTUAL),
    JurisdictionLayer.INTERNAL: (800, JurisClass.CONTRACTUAL),
}


def layer_rank(layer: JurisdictionLayer) -> int:
    return _LAYER_META[layer][0]


def layer_class(layer: JurisdictionLayer) -> JurisClass:
    return _LAYER_META[layer][1]


class InheritanceBehavior(str, Enum):
    FLOOR = "FLOOR"          # lower layers may only raise requirements
    ADDITIVE = "ADDITIVE"    # constraints accumulate
    OVERRIDE = "OVERRIDE"    # higher layer replaces lower — same class only


class RuleCategory(str, Enum):
    # The only categories the Constitution §4 names; no new category invented.
    DOCUMENT = "document"
    EVIDENCE = "evidence"
    THRESHOLD = "threshold"
    PARTICIPATION = "participation"
    FINANCIAL_POLICY = "financial_policy"


class Op(str, Enum):
    IS_TRUE = "is_true"
    EQ = "eq"
    IN = "in"
    GTE = "gte"
    LTE = "lte"


class MandateVersionState(str, Enum):
    DRAFT = "Draft"
    REVIEWED = "Reviewed"
    APPROVED = "Approved"
    PUBLISHED = "Published"
    # Effective / Retired are DERIVED from the effectivity window at read time
    # (State Model §5.2), never written; they are computed by versioning.
    SUPERSEDED = "Superseded"
    VOID = "Void"            # RATIFIED R4 — overlay only, never a mutation
    ARCHIVED = "Archived"


class DeterminationStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    UNRESOLVED = "UNRESOLVED"       # same-level conflict / missing in-force version (I4)
    INSUFFICIENT = "INSUFFICIENT"   # cannot evaluate on grounded versions


class FinancialOutcome(str, Enum):
    NONE = "NONE"                   # no financial-policy rule applied
    EXEMPT = "EXEMPT"
    NOT_EXEMPT = "NOT_EXEMPT"


class OverrideState(str, Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    ACTIVE = "Active"      # derived: Approved + now < expiry
    EXPIRED = "Expired"    # derived: now >= expiry
    REVOKED = "Revoked"


def canonical_hash(payload: Any) -> str:
    """Stable content hash — the reproducibility anchor.

    Identical logical content yields an identical hash regardless of dict key
    order, so a replay of the same inputs reproduces the same snapshot id.
    """
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Rule / Rule Set (Domain Model §3)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: RuleCategory
    attribute: str
    op: Op
    expected: Any = True
    description: str = ""

    def evaluate(self, attributes: Mapping[str, Any]) -> bool:
        """Pure boolean evaluation against supplied entity attributes.

        A missing attribute is a *gap* (returns False), never an exception — the
        determination stays deterministic and total.
        """
        if self.attribute not in attributes:
            return False
        value = attributes[self.attribute]
        if self.op is Op.IS_TRUE:
            return value is True
        if self.op is Op.EQ:
            return value == self.expected
        if self.op is Op.IN:
            return value in self.expected
        if self.op is Op.GTE:
            return value >= self.expected
        if self.op is Op.LTE:
            return value <= self.expected
        return False


@dataclass(frozen=True)
class Applicability:
    """Declarative conditions under which a version applies (Domain Model §7)."""
    node_types: tuple[str, ...] = ()      # empty tuple = applies to all nodes
    entity_types: tuple[str, ...] = ()
    service_types: tuple[str, ...] = ()
    purposes: tuple[str, ...] = ()        # the consumer's declared production purpose

    @staticmethod
    def _match(declared: tuple[str, ...], supplied: Optional[str]) -> bool:
        if not declared:
            return True                    # unconstrained dimension
        return supplied is not None and supplied in declared

    def matches(self, ctx: "ResolutionContext") -> bool:
        return (
            self._match(self.node_types, ctx.node_type)
            and self._match(self.entity_types, ctx.entity_type)
            and self._match(self.service_types, ctx.service_type)
            and self._match(self.purposes, ctx.purpose)
        )


@dataclass(frozen=True)
class EffectivityWindow:
    """In-force interval (Domain Model §6). 'in force at D' is pure in (window, D)."""
    effective_from: str                    # ISO date, inclusive
    effective_to: Optional[str] = None     # ISO date, exclusive; None = open-ended

    def in_force(self, as_of: str) -> bool:
        if as_of < self.effective_from:
            return False
        if self.effective_to is not None and as_of >= self.effective_to:
            return False
        return True


@dataclass(frozen=True)
class MandateVersion:
    """The versioned, immutable-from-Published content (Domain Model §2)."""
    mandate_id: str
    version: int
    jurisdiction_layer: JurisdictionLayer
    inheritance: InheritanceBehavior
    rules: tuple[Rule, ...]
    applicability: Applicability
    effectivity: EffectivityWindow
    authoring_authority: str
    state: MandateVersionState = MandateVersionState.PUBLISHED
    supersedes: Optional[int] = None
    superseded_by: Optional[int] = None

    @property
    def ref(self) -> str:
        return f"{self.mandate_id}@{self.version}"

    def content_fingerprint(self) -> dict:
        """The frozen, version-pinned content captured into a snapshot."""
        return {
            "ref": self.ref,
            "jurisdiction_layer": self.jurisdiction_layer.value,
            "inheritance": self.inheritance.value,
            "authoring_authority": self.authoring_authority,
            "effectivity": {
                "from": self.effectivity.effective_from,
                "to": self.effectivity.effective_to,
            },
            "rules": [
                {
                    "rule_id": r.rule_id,
                    "category": r.category.value,
                    "attribute": r.attribute,
                    "op": r.op.value,
                    "expected": r.expected,
                }
                for r in self.rules
            ],
        }


@dataclass(frozen=True)
class ResolutionContext:
    """The consumer-supplied input for one determination (Domain Model §8)."""
    node_type: str
    entity_type: str
    entity_id: str
    jurisdiction: JurisdictionLayer
    as_of: str                              # ISO date; the runtime never substitutes "now" (I1)
    governing_event_id: str                 # stable identity → snapshot idempotency
    purpose: Optional[str] = None
    service_type: Optional[str] = None
    attributes: Mapping[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None    # opaque; supplied by Core for audit correlation

    def frozen_input(self) -> dict:
        return {
            "node_type": self.node_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "jurisdiction": self.jurisdiction.value,
            "as_of": self.as_of,
            "governing_event_id": self.governing_event_id,
            "purpose": self.purpose,
            "service_type": self.service_type,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True)
class RuleGap:
    mandate_ref: str
    rule_id: str
    category: str
    attribute: str
    reason: str


@dataclass(frozen=True)
class FinancialOverrideOutcome:
    outcome: FinancialOutcome = FinancialOutcome.NONE
    deciding_version: Optional[str] = None
    reason: Optional[str] = None


@dataclass(frozen=True)
class Determination:
    """Authoritative result (Domain Model §10). Immutable once produced."""
    status: DeterminationStatus
    resolved_refs: tuple[str, ...]
    gaps: tuple[RuleGap, ...]
    financial: FinancialOverrideOutcome
    conflict_ref: Optional[str] = None      # set when status == UNRESOLVED


@dataclass(frozen=True)
class Snapshot:
    """Immutable, version-pinned freeze (Domain Model §12). Never mutated (I2)."""
    snapshot_id: str                        # deterministic content id (canonical_hash)
    governing_event_id: str
    frozen_context: dict
    pinned_versions: tuple[dict, ...]       # content fingerprints
    determination: dict                     # frozen determination payload
    financial_override: dict
    created_at: str                         # metadata; not on the deterministic path


@dataclass(frozen=True)
class AuditEvent:
    seq: int
    stream: str
    actor: str
    act: str
    object_ref: str
    timestamp: str
    detail: dict = field(default_factory=dict)


@dataclass(frozen=True)
class PropagationEvent:
    event_id: str
    kind: str
    object_ref: str
    jurisdiction_scope: str
    timestamp: str


@dataclass(frozen=True)
class Override:
    """Dual-authorized, expiring exception (Domain Model §13)."""
    override_id: str
    snapshot_id: str
    requestor: str
    approver: Optional[str]
    reason: str
    expiry: str                             # ISO datetime
    created_at: str
    state: OverrideState = OverrideState.REQUESTED
    revoked_at: Optional[str] = None
    revoked_by: Optional[str] = None

    def with_state(self, **changes) -> "Override":
        return replace(self, **changes)
