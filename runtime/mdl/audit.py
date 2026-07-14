"""Audit — Layer 9 · C9 (Component Contracts §Audit).

Append-only, order-preserving per stream, durable-before-acknowledge. The audit
log owns *no determination truth*: it records, it does not decide. Every mutating
component appends here; there is exactly one path to an acknowledged mutation and
it passes through a durable audit write (contract consistency check §2).
"""

from __future__ import annotations

import threading
from typing import Callable

from .domain import AuditEvent


class AuditTrail:
    def __init__(self, clock: Callable[[], str]):
        self._events: list[AuditEvent] = []
        self._lock = threading.Lock()
        self._clock = clock

    def append(self, stream: str, actor: str, act: str, object_ref: str, detail: dict | None = None) -> AuditEvent:
        with self._lock:
            seq = len(self._events)
            event = AuditEvent(
                seq=seq,
                stream=stream,
                actor=actor,
                act=act,
                object_ref=object_ref,
                timestamp=self._clock(),
                detail=detail or {},
            )
            self._events.append(event)
            return event

    def stream(self, name: str) -> list[AuditEvent]:
        with self._lock:
            return [e for e in self._events if e.stream == name]

    def all(self) -> list[AuditEvent]:
        with self._lock:
            return list(self._events)
