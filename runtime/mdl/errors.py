"""MDL runtime errors.

Every error here expresses a *refusal*, never a silent narrowing. The runtime
fails closed and honest (Runtime Specification §7): it never fabricates a
"compliant" outcome to recover from a failure.
"""


class MDLError(Exception):
    """Base class for every MDL runtime error."""


class ImmutabilityError(MDLError):
    """Raised on any attempt to mutate a frozen artifact (I2).

    Published mandate versions, snapshots, and audit events are write-once.
    """


class AuthoringError(MDLError):
    """Raised when the authoring workflow's role separation is violated (R3)."""


class ScopeError(MDLError):
    """Raised when a caller requests outside its least-privilege projection (I10)."""


class UnresolvedConflict(MDLError):
    """Raised (internally) when a same-level, equal-date conflict cannot resolve (I4).

    Surfaced to the consumer as an ``UNRESOLVED`` determination, never a guess.
    """
