"""Era-1 evidence demo — produces the artifacts the sprint requires as evidence:

  1. an example determination (COMPLIANT, permitted)
  2. an example refusal (NON_COMPLIANT, action denied, with gaps)
  3. the immutable snapshot backing a determination
  4. the audit record for the governing event
  5. proof of snapshot idempotency and cross-run reproducibility

It exercises the runtime in-process (no server needed) so the evidence is
reproducible by anyone running `python runtime/demo/era1_demo.py`.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mdl import JurisdictionLayer, ResolutionContext, build_seeded_runtime  # noqa: E402

KEYS = {
    "viral-bot-machine": "vbm-key",
    "prometheus": "prom-key",
    "safelaunch-content-factory": "content-key",
    "safelaunch-video-factory": "video-key",
}


def _ctx(event_id, **attrs):
    base = {"operator_authorized": True, "intake_approved": True, "account_active": True}
    base.update(attrs)
    return ResolutionContext(
        node_type="viral-bot-machine",
        entity_type="bot_deployment",
        entity_id="intake-EVIDENCE",
        jurisdiction=JurisdictionLayer.INTERNAL,
        as_of="2026-07-14",
        governing_event_id=event_id,
        purpose="bot.publish",
        attributes=base,
        correlation_id="trace-abc-123",
    )


def main():
    rt = build_seeded_runtime(KEYS)

    print("=" * 72)
    print("1) EXAMPLE DETERMINATION — compliant Viral-Bot-Machine deployment")
    print("=" * 72)
    ok = rt.determine(_ctx("deploy:intake-EVIDENCE:1"), api_key="vbm-key")
    print(json.dumps(ok.to_wire(), indent=2))

    print("\n" + "=" * 72)
    print("2) EXAMPLE REFUSAL — intake not approved → action denied, snapshotted")
    print("=" * 72)
    bad = rt.determine(_ctx("deploy:intake-EVIDENCE:2", intake_approved=False), api_key="vbm-key")
    print(json.dumps(bad.to_wire(), indent=2))

    print("\n" + "=" * 72)
    print("3) IMMUTABLE SNAPSHOT backing determination (1)")
    print("=" * 72)
    snap = rt.snapshots.get(ok.snapshot_id)
    print(json.dumps({
        "snapshot_id": snap.snapshot_id,
        "governing_event_id": snap.governing_event_id,
        "frozen_context": snap.frozen_context,
        "pinned_versions": list(snap.pinned_versions),
        "determination": snap.determination,
        "financial_override": snap.financial_override,
        "created_at": snap.created_at,
    }, indent=2))

    print("\n" + "=" * 72)
    print("4) AUDIT RECORD for governing event deploy:intake-EVIDENCE:1")
    print("=" * 72)
    events = [e for e in rt.audit.all()
              if e.object_ref == ok.snapshot_id
              or e.detail.get("governing_event_id") == "deploy:intake-EVIDENCE:1"]
    for e in events:
        print(f"  #{e.seq} [{e.stream}] {e.act} by {e.actor} → {e.object_ref}")

    print("\n" + "=" * 72)
    print("5) DETERMINISM — idempotency + cross-runtime reproducibility")
    print("=" * 72)
    again = rt.determine(_ctx("deploy:intake-EVIDENCE:1"), api_key="vbm-key")
    rt2 = build_seeded_runtime(KEYS)
    fresh = rt2.determine(_ctx("deploy:intake-EVIDENCE:1"), api_key="vbm-key")
    print(f"  same governing event, same runtime:   {ok.snapshot_id == again.snapshot_id}")
    print(f"  same inputs, independent runtime:      {ok.snapshot_id == fresh.snapshot_id}")
    print(f"  snapshot id: {ok.snapshot_id}")


if __name__ == "__main__":
    main()
