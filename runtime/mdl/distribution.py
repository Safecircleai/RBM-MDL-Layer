"""Distribution — Layer 8 · C11-propagation (Component Contracts §Distribution).

Scoped event publication. MDL is the *sole publisher* (I5); events are emitted
**after** the truth they describe is durably recorded (publish-after-commit), so
a consumer never sees an event for a change that did not persist. Propagation
never mutates a snapshot (I2).

Era-1 scope: an in-process append-only outbox with jurisdiction-scoped matching.
Delivery transport (queue/webhook) is intentionally deferred — the doctrine's
at-least-once guarantee is a transport property this outbox is built to satisfy.
"""

from __future__ import annotations

import threading
import uuid
from typing import Callable

from .domain import PropagationEvent


class Distribution:
    def __init__(self, clock: Callable[[], str]):
        self._clock = clock
        self._lock = threading.Lock()
        self._outbox: list[PropagationEvent] = []

    def publish(self, kind: str, object_ref: str, jurisdiction_scope: str) -> PropagationEvent:
        event = PropagationEvent(
            event_id="evt_" + uuid.uuid4().hex[:16],
            kind=kind,
            object_ref=object_ref,
            jurisdiction_scope=jurisdiction_scope,
            timestamp=self._clock(),
        )
        with self._lock:
            self._outbox.append(event)
        return event

    def outbox(self) -> list[PropagationEvent]:
        with self._lock:
            return list(self._outbox)
