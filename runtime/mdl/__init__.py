"""MDL Era-1 deterministic runtime.

The minimum serviceable Mandate Definition Layer runtime: the eleven Core
components (C1–C11) wired into the determination pipeline, implemented faithfully
to the frozen v1.0 constitution and the Phase-5 engineering specifications
(``engineering/``). No doctrine is created or extended here — this is
implementation only.

Public surface:
    MDLRuntime            the wired runtime facade (the pipeline)
    build_seeded_runtime  a runtime pre-loaded with the Era-1 operational mandates
    ResolutionContext     the consumer-supplied determination input
    DeterminationResult   the runtime outcome a consumer obeys
"""

from .domain import (
    DeterminationStatus,
    InheritanceBehavior,
    JurisdictionLayer,
    ResolutionContext,
)
from .interface import ConsumerRegistration
from .runtime import DeterminationResult, MDLRuntime
from .seeds import build_seeded_runtime

__all__ = [
    "MDLRuntime",
    "build_seeded_runtime",
    "ResolutionContext",
    "DeterminationResult",
    "DeterminationStatus",
    "JurisdictionLayer",
    "InheritanceBehavior",
    "ConsumerRegistration",
]
