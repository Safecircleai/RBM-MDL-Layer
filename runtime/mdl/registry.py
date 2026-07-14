"""Registry — Layer 1 · C1 (Component Contracts §Registry).

The single authoritative store of published mandate definitions by identity +
version. Published versions are immutable; no version is ever deleted; reads are
monotonic (a version never disappears). Every write records to Audit.

Cannot own: a second/competing store, the source obligation, any determination or
snapshot.
"""

from __future__ import annotations

import threading
from typing import Optional

from .audit import AuditTrail
from .domain import MandateVersion
from .errors import ImmutabilityError


class Registry:
    def __init__(self, audit: AuditTrail):
        self._audit = audit
        self._lock = threading.Lock()
        # mandate_id -> {version:int -> MandateVersion}
        self._versions: dict[str, dict[int, MandateVersion]] = {}
        # mandate_id -> current head version number
        self._head: dict[str, int] = {}

    def publish(self, version: MandateVersion) -> MandateVersion:
        """Append a published version. Never mutates or deletes a prior version."""
        with self._lock:
            chain = self._versions.setdefault(version.mandate_id, {})
            if version.version in chain:
                raise ImmutabilityError(
                    f"version {version.ref} already published; a change is a new version, never an edit"
                )
            chain[version.version] = version
            self._head[version.mandate_id] = max(self._head.get(version.mandate_id, 0), version.version)
        self._audit.append(
            stream="registry",
            actor=version.authoring_authority,
            act="MANDATE_VERSION_PUBLISHED",
            object_ref=version.ref,
        )
        return version

    def get(self, mandate_id: str, version: int) -> Optional[MandateVersion]:
        with self._lock:
            return self._versions.get(mandate_id, {}).get(version)

    def chain(self, mandate_id: str) -> list[MandateVersion]:
        with self._lock:
            return [self._versions[mandate_id][v] for v in sorted(self._versions.get(mandate_id, {}))]

    def all_mandate_ids(self) -> list[str]:
        with self._lock:
            return list(self._versions.keys())

    def head(self, mandate_id: str) -> Optional[int]:
        with self._lock:
            return self._head.get(mandate_id)
