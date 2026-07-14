"""Interfaces — Layer 11 · C11-request + supervision boundary
(Component Contracts §Interfaces).

Authentication, scoping, and projection enforcement at the edge. Every request is
authenticated and scoped to the caller's least-privilege projection (I10): a
consumer reads only its own entities' snapshots and only mandates in its
jurisdiction scope. An over-scope request is refused, not silently narrowed.

The Governance Supervisor (EchoForge) gets read + subscribe only; it can never
drive a determination, write, or disable enforcement (I7). This runtime
implements *none* of the Supervisor's escalation state machine — Era 1 excludes
EchoForge from the determination path entirely.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .errors import ScopeError


@dataclass
class ConsumerRegistration:
    """A node's declaration of identity + scope (Domain Model §16)."""
    node_id: str
    node_type: str
    api_key: str
    jurisdiction_scope: tuple[str, ...]     # layers the node may resolve within
    can_determine: bool = True              # consumers determine; supervisor does not
    read_only: bool = False                 # the supervisor boundary (I7)


@dataclass
class ConsumerDirectory:
    _by_key: dict[str, ConsumerRegistration] = field(default_factory=dict)

    def register(self, reg: ConsumerRegistration) -> ConsumerRegistration:
        self._by_key[reg.api_key] = reg
        return reg

    def authenticate(self, api_key: str) -> ConsumerRegistration:
        reg = self._by_key.get(api_key)
        if reg is None:
            raise ScopeError("unrecognized consumer credential")
        return reg

    def authorize_determination(self, reg: ConsumerRegistration, node_type: str, jurisdiction: str) -> None:
        if reg.read_only or not reg.can_determine:
            raise ScopeError(f"consumer {reg.node_id} has no determination privilege (read-only boundary)")
        if node_type != reg.node_type:
            raise ScopeError(
                f"consumer {reg.node_id} ({reg.node_type}) may not request determinations for node_type '{node_type}'"
            )
        if reg.jurisdiction_scope and jurisdiction not in reg.jurisdiction_scope:
            raise ScopeError(
                f"consumer {reg.node_id} is not scoped to jurisdiction '{jurisdiction}'"
            )
