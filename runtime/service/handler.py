"""Transport-agnostic request handling for the determination service.

Both the FastAPI app (production) and the stdlib test harness call these two
functions, so the wire contract is defined and tested in exactly one place. No
framework is imported here — it is pure mapping between a request dict and a
(status_code, body) pair.
"""

from __future__ import annotations

from typing import Tuple

from mdl import JurisdictionLayer, ResolutionContext
from mdl.errors import ScopeError
from mdl.runtime import MDLRuntime


def handle_determination(runtime: MDLRuntime, payload: dict, api_key: str) -> Tuple[int, dict]:
    try:
        jurisdiction = JurisdictionLayer(payload.get("jurisdiction", "INTERNAL"))
    except ValueError:
        return 400, {"detail": f"unranked jurisdiction layer: {payload.get('jurisdiction')}"}

    required = ("node_type", "entity_type", "entity_id", "as_of", "governing_event_id")
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return 400, {"detail": f"missing required fields: {', '.join(missing)}"}

    ctx = ResolutionContext(
        node_type=payload["node_type"],
        entity_type=payload["entity_type"],
        entity_id=payload["entity_id"],
        jurisdiction=jurisdiction,
        as_of=payload["as_of"],
        governing_event_id=payload["governing_event_id"],
        purpose=payload.get("purpose"),
        service_type=payload.get("service_type"),
        attributes=payload.get("attributes") or {},
        correlation_id=payload.get("correlation_id"),
    )
    try:
        result = runtime.determine(ctx, api_key=api_key)
    except ScopeError as exc:
        return 403, {"detail": str(exc)}
    return 200, result.to_wire()


def snapshot_body(runtime: MDLRuntime, snapshot_id: str) -> Tuple[int, dict]:
    snap = runtime.snapshots.get(snapshot_id)
    if snap is None:
        return 404, {"detail": "snapshot not found"}
    return 200, {
        "snapshot_id": snap.snapshot_id,
        "governing_event_id": snap.governing_event_id,
        "frozen_context": snap.frozen_context,
        "pinned_versions": list(snap.pinned_versions),
        "determination": snap.determination,
        "financial_override": snap.financial_override,
        "created_at": snap.created_at,
    }
