"""MDL determination service — the HTTP projection of the Interface layer (C11).

This is the *live runtime* a consuming node calls. It exposes exactly the
least-privilege read/determination surface the constitution permits — no write
path, no supervisor escalation, no discipline reasoning.

    POST /v1/determinations     run the pipeline, return the runtime outcome
    GET  /v1/snapshots/{id}      read an immutable snapshot (reproducibility anchor)
    GET  /v1/audit/{event_id}    read the audit record for a governing event
    GET  /health                 liveness

Consumer credentials are supplied via ``X-MDL-Key`` and mapped to node identity by
the runtime's consumer directory. Keys come from the environment
(MDL_KEY_<NODE>), never hardcoded.

Run:  uvicorn runtime.service.app:app  (requires fastapi + uvicorn)
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Header, HTTPException  # type: ignore
from pydantic import BaseModel, Field  # type: ignore

from mdl import build_seeded_runtime
from mdl.seeds import NODE_CONTENT, NODE_PROMETHEUS, NODE_VBM, NODE_VIDEO
from service.handler import handle_determination, snapshot_body


def _keys_from_env() -> dict[str, str]:
    return {
        NODE_VBM: os.getenv("MDL_KEY_VBM", "vbm-dev-key"),
        NODE_PROMETHEUS: os.getenv("MDL_KEY_PROMETHEUS", "prometheus-dev-key"),
        NODE_CONTENT: os.getenv("MDL_KEY_CONTENT", "content-dev-key"),
        NODE_VIDEO: os.getenv("MDL_KEY_VIDEO", "video-dev-key"),
    }


runtime = build_seeded_runtime(_keys_from_env())
app = FastAPI(title="RBM MDL Layer — Determination Service (Era 1)", version="1.0.0-era1")


class DeterminationRequest(BaseModel):
    node_type: str
    entity_type: str
    entity_id: str
    jurisdiction: str = Field(default="INTERNAL")
    as_of: str
    governing_event_id: str
    purpose: str | None = None
    service_type: str | None = None
    attributes: dict = Field(default_factory=dict)
    correlation_id: str | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "runtime": "mdl-era1", "mandates": len(runtime.registry.all_mandate_ids())}


@app.post("/v1/determinations")
def determine(req: DeterminationRequest, x_mdl_key: str = Header(default="")) -> dict:
    status, body = handle_determination(runtime, req.model_dump(), x_mdl_key)
    if status != 200:
        raise HTTPException(status_code=status, detail=body.get("detail"))
    return body


@app.get("/v1/snapshots/{snapshot_id}")
def get_snapshot(snapshot_id: str) -> dict:
    status, body = snapshot_body(runtime, snapshot_id)
    if status != 200:
        raise HTTPException(status_code=status, detail=body.get("detail"))
    return body


@app.get("/v1/audit/{governing_event_id}")
def get_audit(governing_event_id: str) -> dict:
    events = [
        {
            "seq": e.seq,
            "stream": e.stream,
            "actor": e.actor,
            "act": e.act,
            "object_ref": e.object_ref,
            "timestamp": e.timestamp,
            "detail": e.detail,
        }
        for e in runtime.audit.all()
        if e.object_ref == governing_event_id
        or e.detail.get("governing_event_id") == governing_event_id
    ]
    return {"governing_event_id": governing_event_id, "events": events}
