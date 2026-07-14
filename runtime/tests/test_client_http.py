"""End-to-end client↔service contract test over a real HTTP socket.

Uses the stdlib http.server bound to the SAME shared handler the FastAPI app
uses (runtime/service/handler.py), so this exercises the true wire contract
without requiring fastapi/uvicorn to be installed. Proves:
  - the vendored mdl_client speaks the contract correctly over HTTP,
  - require() permits a compliant action and refuses a non-compliant one,
  - the client fails CLOSED when the runtime is unreachable (no fallback).
"""

import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "client"))

from mdl import build_seeded_runtime  # noqa: E402
from service.handler import handle_determination, snapshot_body  # noqa: E402
from mdl_client import MDLClient, MDLDenied, MDLUnavailable  # noqa: E402

KEYS = {"viral-bot-machine": "vbm-key"}
_runtime = build_seeded_runtime(KEYS)


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, status, body):
        blob = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length).decode())
        key = self.headers.get("X-MDL-Key", "")
        status, body = handle_determination(_runtime, payload, key)
        self._send(status, body)

    def do_GET(self):
        sid = self.path.rsplit("/", 1)[-1]
        status, body = snapshot_body(_runtime, sid)
        self._send(status, body)


def _start_server():
    server = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def run():
    server = _start_server()
    port = server.server_address[1]
    base_url = f"http://127.0.0.1:{port}"
    client = MDLClient(base_url, api_key="vbm-key", node_type="viral-bot-machine")
    common = dict(
        entity_type="bot_deployment",
        entity_id="intake-http",
        as_of="2026-07-14",
        purpose="bot.publish",
    )

    # 1) compliant → require() returns a permitted determination
    det = client.require(governing_event_id="deploy:http:1", attributes={
        "operator_authorized": True, "intake_approved": True, "account_active": True,
    }, **common)
    assert det.is_permitted and det.snapshot_id
    print("  ok  compliant deploy permitted over HTTP; snapshot", det.snapshot_id)

    # 2) non-compliant → require() raises MDLDenied with the gaps attached
    try:
        client.require(governing_event_id="deploy:http:2", attributes={
            "operator_authorized": True, "intake_approved": False, "account_active": True,
        }, **common)
        assert False, "expected MDLDenied"
    except MDLDenied as exc:
        assert exc.determination is not None and exc.determination.status == "NON_COMPLIANT"
        print("  ok  non-compliant deploy refused over HTTP:", exc.determination.gap_summary())

    # 3) wrong node scope → HTTP 403 surfaces as MDLUnavailable (fail closed)
    rogue = MDLClient(base_url, api_key="vbm-key", node_type="prometheus")
    try:
        rogue.determine(governing_event_id="x", entity_type="campaign_execution",
                        entity_id="c1", as_of="2026-07-14", purpose="campaign.activate")
        assert False, "expected refusal"
    except MDLUnavailable:
        print("  ok  out-of-scope request refused (403 → fail closed)")

    # 4) runtime unreachable → fail CLOSED, never allow
    server.shutdown()
    dead = MDLClient(base_url, api_key="vbm-key", node_type="viral-bot-machine")
    try:
        dead.require(governing_event_id="deploy:http:3", attributes={
            "operator_authorized": True, "intake_approved": True, "account_active": True,
        }, **common)
        assert False, "expected MDLUnavailable"
    except MDLUnavailable:
        print("  ok  unreachable runtime → action refused (no fallback)")

    print("\n4/4 client↔service HTTP contract checks passed")


if __name__ == "__main__":
    run()
