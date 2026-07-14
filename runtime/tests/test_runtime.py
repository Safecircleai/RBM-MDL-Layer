"""Era-1 runtime tests — the load-bearing invariants, exercised end-to-end.

Run: python -m pytest runtime/tests/  (pytest optional; also runnable directly).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mdl import (  # noqa: E402
    DeterminationStatus,
    JurisdictionLayer,
    ResolutionContext,
    build_seeded_runtime,
)
from mdl.errors import AuthoringError, ScopeError  # noqa: E402

KEYS = {
    "viral-bot-machine": "vbm-key",
    "prometheus": "prom-key",
    "safelaunch-content-factory": "content-key",
    "safelaunch-video-factory": "video-key",
}


def _vbm_ctx(event_id, **attrs):
    base = {"operator_authorized": True, "intake_approved": True, "account_active": True}
    base.update(attrs)
    return ResolutionContext(
        node_type="viral-bot-machine",
        entity_type="bot_deployment",
        entity_id="intake-123",
        jurisdiction=JurisdictionLayer.INTERNAL,
        as_of="2026-07-14",
        governing_event_id=event_id,
        purpose="bot.publish",
        attributes=base,
    )


def test_compliant_deployment_is_permitted_and_snapshotted():
    rt = build_seeded_runtime(KEYS)
    res = rt.determine(_vbm_ctx("deploy:intake-123:1"), api_key="vbm-key")
    assert res.status is DeterminationStatus.COMPLIANT
    assert res.permits_action is True
    assert res.admissible and res.recorded
    assert res.snapshot_id is not None
    # Resolved BOTH the PROGRAM floor and the INTERNAL node mandate.
    refs = set(res.determination.resolved_refs)
    assert "ecosystem-account-active@1" in refs
    assert "vbm-deployment-approved@1" in refs


def test_noncompliant_deployment_is_refused_with_gaps():
    rt = build_seeded_runtime(KEYS)
    res = rt.determine(_vbm_ctx("deploy:intake-124:1", intake_approved=False), api_key="vbm-key")
    assert res.status is DeterminationStatus.NON_COMPLIANT
    assert res.permits_action is False
    assert any(g.attribute == "intake_approved" for g in res.determination.gaps)
    # Still admissible: a NON_COMPLIANT result is a real determination, snapshotted.
    assert res.admissible and res.snapshot_id is not None


def test_missing_account_active_floor_blocks():
    rt = build_seeded_runtime(KEYS)
    res = rt.determine(_vbm_ctx("deploy:intake-125:1", account_active=False), api_key="vbm-key")
    assert res.status is DeterminationStatus.NON_COMPLIANT
    assert any(g.mandate_ref == "ecosystem-account-active@1" for g in res.determination.gaps)


def test_snapshot_idempotent_per_governing_event():
    rt = build_seeded_runtime(KEYS)
    a = rt.determine(_vbm_ctx("deploy:intake-126:1"), api_key="vbm-key")
    b = rt.determine(_vbm_ctx("deploy:intake-126:1"), api_key="vbm-key")
    assert a.snapshot_id == b.snapshot_id  # same governing event → one snapshot


def test_determinism_same_inputs_same_snapshot_id_across_runtimes():
    rt1 = build_seeded_runtime(KEYS)
    rt2 = build_seeded_runtime(KEYS)
    a = rt1.determine(_vbm_ctx("deploy:intake-127:1"), api_key="vbm-key")
    b = rt2.determine(_vbm_ctx("deploy:intake-127:1"), api_key="vbm-key")
    # Reproducibility: identical inputs → identical snapshot content id.
    assert a.snapshot_id == b.snapshot_id


def test_scope_enforcement_wrong_node_type_refused():
    rt = build_seeded_runtime(KEYS)
    ctx = _vbm_ctx("deploy:intake-128:1")
    try:
        rt.determine(ctx, api_key="prom-key")  # prometheus key, vbm request
        assert False, "expected ScopeError"
    except ScopeError:
        pass


def test_unknown_credential_refused():
    rt = build_seeded_runtime(KEYS)
    try:
        rt.determine(_vbm_ctx("deploy:intake-129:1"), api_key="bogus")
        assert False, "expected ScopeError"
    except ScopeError:
        pass


def test_override_overlays_runtime_outcome_not_snapshot():
    rt = build_seeded_runtime(KEYS)
    res = rt.determine(_vbm_ctx("deploy:intake-130:1", intake_approved=False), api_key="vbm-key")
    assert res.permits_action is False
    snap_id = res.snapshot_id
    # Dual-authorized override (requestor ≠ approver), far-future expiry.
    ovr = rt.overrides.request(snap_id, requestor="ops.alice", reason="approved exception", expiry="2099-01-01T00:00:00+00:00")
    rt.overrides.approve(ovr.override_id, approver="ops.bob")
    res2 = rt.determine(_vbm_ctx("deploy:intake-130:1", intake_approved=False), api_key="vbm-key")
    assert res2.override_applied is True
    assert res2.permits_action is True
    # The snapshot itself is unchanged (same id, frozen NON_COMPLIANT determination).
    assert res2.snapshot_id == snap_id
    assert rt.snapshots.get(snap_id).determination["status"] == "NON_COMPLIANT"


def test_override_self_approval_rejected():
    rt = build_seeded_runtime(KEYS)
    res = rt.determine(_vbm_ctx("deploy:intake-131:1", intake_approved=False), api_key="vbm-key")
    ovr = rt.overrides.request(res.snapshot_id, requestor="ops.alice", reason="x", expiry="2099-01-01T00:00:00+00:00")
    try:
        rt.overrides.approve(ovr.override_id, approver="ops.alice")
        assert False, "expected AuthoringError"
    except AuthoringError:
        pass


def test_authoring_separation_of_duties():
    rt = build_seeded_runtime(KEYS)
    from mdl.domain import Applicability, EffectivityWindow, InheritanceBehavior, Op, Rule, RuleCategory
    item = rt.governance.draft(
        intake_id="x", source_authority="ops", mandate_id="test-m",
        jurisdiction_layer=JurisdictionLayer.INTERNAL, inheritance=InheritanceBehavior.OVERRIDE,
        rules=(Rule("r", RuleCategory.PARTICIPATION, "a", Op.IS_TRUE),),
        applicability=Applicability(node_types=("viral-bot-machine",)),
        effectivity=EffectivityWindow("2026-01-01"), author="same.person",
    )
    try:
        rt.governance.review(item, reviewer="same.person")
        assert False, "author must not review own draft"
    except AuthoringError:
        pass


def test_audit_records_every_determination():
    rt = build_seeded_runtime(KEYS)
    rt.determine(_vbm_ctx("deploy:intake-140:1"), api_key="vbm-key")
    det_events = rt.audit.stream("determination")
    assert any(e.act == "DETERMINATION_RECORDED" for e in det_events)
    snap_events = rt.audit.stream("snapshot")
    assert any(e.act == "SNAPSHOT_CREATED" for e in snap_events)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn()
        passed += 1
        print(f"  ok  {fn.__name__}")
    print(f"\n{passed}/{len(fns)} runtime tests passed")
