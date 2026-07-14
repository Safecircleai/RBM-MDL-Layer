# RBM MDL Layer — Era 1 Evidence (Serviceability)

**Status:** IMPLEMENTATION EVIDENCE — not doctrine. The v1.0 constitution remains
frozen (`DOCTRINE_FREEZE.md`); nothing in Era 1 created, modified, or extended it.
This report is the evidence the Era-1 sprint requires.

**Era 1 objective — met:** MDL is a **live deterministic runtime**, and **Viral Bot
Machine depends on it for one production decision** (bot deployment). Prometheus,
Content Factory, and Video Factory consume the **same client contract** without
modifying MDL. SafeLaunchCenter-Core routes and correlates; it does not own
mandates. EchoForge is **not** on the determination path.

---

## 1. Runtime architecture implemented

The runtime lives in `runtime/` and implements the eleven Core capabilities
(C1–C11) as one importable package, wired into the determination pipeline of
`engineering/MDL_Runtime_Specification.md` §2:

```
Interface (authenticate, scope to least-privilege projection)
  → Resolution  (Registry + Versioning + Jurisdiction)
  → Determination (+ Financial-Override)
  → Snapshot (freeze, idempotent per governing event)
  → Override (apply in-force overlay; snapshot unchanged)
  → Interface (return the runtime outcome)
  ⟿ Audit (record)     ⟿ Distribution (emit event)
```

Constitutional invariants enforced in code:

- **Determinism (I1):** the resolve→determine→snapshot path reads no wall-clock;
  effectivity uses the context `as_of`. The one sanctioned wall-clock read is
  override expiry, which overlays the runtime outcome only, never the snapshot.
- **Immutability (I2):** published mandate versions, snapshots, and audit events
  are frozen dataclasses; the snapshot id is the canonical content hash, so an
  identical replay reproduces the identical snapshot.
- **Idempotency per governing event (C6):** the same governing event converges on
  exactly one snapshot.
- **Jurisdiction (R2):** the FEDERAL-anchored two-class stack orders every resolve;
  same-level equal-date OVERRIDE conflicts return `UNRESOLVED`, never auto-resolve
  (I4).
- **Authoring separation of duties (R3):** Author ≠ Reviewer ≠ Publisher.
- **Least-privilege interface (I10):** a consumer may determine only for its own
  node type, within its jurisdiction scope.
- **Fail-closed (§7):** `UNRESOLVED`/`INSUFFICIENT`/unrecorded outcomes never
  permit an action; the client refuses on any error.

## 2. Components completed

| # | Component | Capability | Module | Status |
|---|---|---|---|---|
| 9 | Audit | C9 | `runtime/mdl/audit.py` | ✅ append-only, order-preserving |
| 1 | Registry | C1 | `runtime/mdl/registry.py` | ✅ immutable published versions |
| 10 | Governance (authoring) | C10 | `runtime/mdl/governance.py` | ✅ Intake→…→Publish, R3 roles |
| 3 | Versioning | C2 | `runtime/mdl/versioning.py` | ✅ in-force-at-`as_of` selection |
| 2 | Jurisdiction | C3 | `runtime/mdl/jurisdiction.py` | ✅ R2 two-class ordering, conflict flag |
| 4 | Resolution | C4 | `runtime/mdl/resolution.py` | ✅ deterministic applicable set |
| 5 | Determination | C5+C7 | `runtime/mdl/determination.py` | ✅ compliance + financial-override outcome |
| 6 | Snapshot | C6 | `runtime/mdl/snapshot.py` | ✅ immutable, idempotent per event |
| 7 | Override | C8 | `runtime/mdl/override.py` | ✅ dual-auth, read-time effectiveness |
| 8 | Distribution | C11-prop | `runtime/mdl/distribution.py` | ◑ in-process outbox (transport deferred) |
| 11 | Interfaces | C11-req | `runtime/mdl/interface.py`, `service/` | ✅ scoping + HTTP determination service |

Seed mandate set (`runtime/mdl/seeds.py`), all authored through the real workflow
and all **ecosystem operational booleans** — no government compliance, no trust
scoring, no probabilistic evaluation:

- `ecosystem-account-active` — PROGRAM · FLOOR · every node
- `vbm-deployment-approved` — INTERNAL · viral-bot-machine · `bot.publish`
- `prometheus-campaign-approved` — INTERNAL · prometheus · `campaign.activate`
- `content-media-approved` — INTERNAL · content-factory · `media.produce`
- `video-publishing-authorized` — INTERNAL · video-factory · `media.render`

Because the account-active floor sits at PROGRAM (rank 700) and the node mandates
at INTERNAL (rank 800), every determination resolves **two** mandates — proving the
jurisdiction stack orders a real multi-mandate set, not a single rule.

Tests (all green, no third-party deps required):
`python runtime/tests/test_runtime.py` → 11/11;
`python runtime/tests/test_client_http.py` → 4/4 (client↔service over a real socket).

## 3. Components intentionally deferred

- **Distribution transport (C11):** the outbox and scoping are implemented; the
  durable at-least-once delivery transport (queue/webhook) is deferred — Era 1
  needs no cross-node event delivery for its single vertical slice.
- **Persistent storage:** stores are in-memory/deterministic. The Persistence
  Model classifications are honored semantically (immutable / append-only /
  derived); binding to a durable engine is post-Era-1.
- **Void / Invalidation overlay (R4):** the `Void` state and append-only
  Invalidation-Record semantics are modeled in the domain/state layer; the
  invalidation-overlay runtime is not exercised in Era 1 (no void event occurs on
  the slice).
- **Financial-override content:** the mechanism is present (a `financial_policy`
  rule yields a binding outcome); Era-1 operational mandates carry none, so the
  outcome is `NONE`. Tax content is future work, not Era 1.
- **Conflict-Review workflow:** `UNRESOLVED` is produced and a Conflict Item is
  raised; the human review workflow UI/queue is deferred.
- **Discipline-determination consumption:** excluded from the deterministic path by
  design (audit CR-4); not implemented.
- **EchoForge / Governance-Supervisor path:** deliberately absent — Era 1 excludes
  EchoForge from determination; the read-only boundary (I7) is preserved by not
  building it.

## 4. First consumer integration (the binding decision)

**Viral Bot Machine — bot deployment.** The production path
`POST /api/worker/deploy/{intake_id}` (`botforge/api/worker.py`) cannot execute
without MDL. Before any deployment record is created, `deploy_chatbot` calls
`require_deployment_approved(profile)` (`botforge/mdl/deployment_gate.py`), which
submits a deterministic context to the MDL runtime and obeys the result:

- COMPLIANT + admissible → deployment proceeds, logging the snapshot id as
  authorization evidence.
- NON_COMPLIANT / UNRESOLVED / unreachable / unconfigured → **403, deployment
  refused**, no fallback.

The client (`botforge/mdl/mdl_client.py`) is the canonical contract vendored
verbatim; it is **byte-identical** across all four consumers (verified by md5).
Prometheus, Content Factory, and Video Factory each add exactly one gate at their
production dispatch using the same contract:

| Consumer | Production path gated | Mandate | Insertion |
|---|---|---|---|
| Viral Bot Machine | bot deployment | `vbm-deployment-approved` | `worker.py` `deploy_chatbot` |
| Prometheus | real campaign dispatch | `prometheus-campaign-approved` | `execution/service.py` `_real_dispatch` |
| Content Factory | media job acceptance | `content-media-approved` | `contract/router.py` `dispatch_job` |
| Video Factory | render/voiceover acceptance | `video-publishing-authorized` | `contract/router.py` `dispatch_job` |
| SafeLaunchCenter-Core | routing + correlation only | — (Core owns no mandate) | `gateway/dispatcher.py` `_route_to_mdl` |

## 5. Example determination (COMPLIANT, permitted)

```json
{
  "status": "COMPLIANT",
  "admissible": true,
  "recorded": true,
  "permits_action": true,
  "snapshot_id": "snap_5790fc0ac56bc19fc33644a334d13348",
  "override_applied": false,
  "governing_event_id": "deploy:intake-EVIDENCE:1",
  "as_of": "2026-07-14",
  "mandate_versions": ["ecosystem-account-active@1", "vbm-deployment-approved@1"],
  "gaps": [],
  "financial_override": {"outcome": "NONE", "deciding_version": null, "reason": null},
  "conflict_ref": null
}
```

Example **refusal** (same path, `intake_approved=false`) — action denied, still
snapshotted and admissible:

```json
{
  "status": "NON_COMPLIANT",
  "permits_action": false,
  "snapshot_id": "snap_7fb56cc5a5d97b35e8e8d8393a841841",
  "mandate_versions": ["ecosystem-account-active@1", "vbm-deployment-approved@1"],
  "gaps": [{
    "mandate": "vbm-deployment-approved@1",
    "rule_id": "deploy.intake_approved",
    "category": "evidence",
    "attribute": "intake_approved",
    "reason": "attribute 'intake_approved' does not satisfy is_true"
  }]
}
```

## 6. Example immutable snapshot

Version-pinned freeze backing the COMPLIANT determination above. The snapshot id is
the canonical content hash; an identical replay reproduces it exactly (verified
across two independent runtimes).

```json
{
  "snapshot_id": "snap_5790fc0ac56bc19fc33644a334d13348",
  "governing_event_id": "deploy:intake-EVIDENCE:1",
  "frozen_context": {
    "node_type": "viral-bot-machine", "entity_type": "bot_deployment",
    "entity_id": "intake-EVIDENCE", "jurisdiction": "INTERNAL",
    "as_of": "2026-07-14", "purpose": "bot.publish",
    "attributes": {"operator_authorized": true, "intake_approved": true, "account_active": true}
  },
  "pinned_versions": [
    {"ref": "ecosystem-account-active@1", "jurisdiction_layer": "PROGRAM", "inheritance": "FLOOR", "rules": [
      {"rule_id": "account.active", "category": "participation", "attribute": "account_active", "op": "is_true"}]},
    {"ref": "vbm-deployment-approved@1", "jurisdiction_layer": "INTERNAL", "inheritance": "OVERRIDE", "rules": [
      {"rule_id": "deploy.operator_authorized", "category": "participation", "attribute": "operator_authorized", "op": "is_true"},
      {"rule_id": "deploy.intake_approved", "category": "evidence", "attribute": "intake_approved", "op": "is_true"}]}
  ],
  "determination": {"status": "COMPLIANT", "gaps": [], "conflict_ref": null},
  "financial_override": {"outcome": "NONE"},
  "created_at": "2026-07-14T..."
}
```

Reproduce it: `python runtime/demo/era1_demo.py`.

## 7. Example audit record

Append-only trail for governing event `deploy:intake-EVIDENCE:1`:

```
#15 [snapshot]      SNAPSHOT_CREATED       by mdl-runtime       → snap_5790fc0ac56bc19fc33644a334d13348
#16 [determination] DETERMINATION_RECORDED by viral-bot-machine → snap_5790fc0ac56bc19fc33644a334d13348
```

Authoring the seed set also appended `MANDATE_DRAFTED` / `MANDATE_APPROVED`
(distinct reviewer) / `MANDATE_VERSION_PUBLISHED` (distinct publisher) events —
every mutation is audited; there is no un-audited write.

## 8. Remaining work before CFRS parity

Era 1 is a serviceability slice, **not** CFRS parity. To reach parity:

1. **Durable persistence** — bind the immutable/append-only stores to a real engine
   (the Persistence Model already classifies every object); add reconstruction/replay.
2. **Distribution transport** — durable at-least-once delivery with per-mandate
   ordering and jurisdiction-scoped subscriptions; consumer registration API.
3. **Government-compliance mandates** — the Class-1 legal spine (FEDERAL→…→MUNICIPAL)
   with FLOOR/ADDITIVE stringency and the binding **financial (tax) override**
   content the Economic Consumer honors.
4. **Void / Invalidation overlay (R4)** — exercise append-only invalidation and
   `MANDATE_VOIDED` propagation end-to-end.
5. **Conflict-Review workflow** — the human/ratified resolution queue for
   `UNRESOLVED` items.
6. **Full authoring UX + authority-lineage detection** — the still-open input
   (delegation / authority lineage) the specs mark unresolved.
7. **Migrate modules into the blueprint's governed directories** (`registry/`,
   `resolution/`, …) as the CFRS strangler-fig migration proceeds
   (`Migration_Strategy_CFRS_to_RBM_MDL.md`).
8. **Supervisor read-only boundary** for EchoForge — read + subscribe only, with the
   escalation state machine remaining EchoForge's, never MDL's.

## 9. Faithfulness check against the sprint constraints

- ✅ No doctrine created/modified; v1.0 treated as frozen.
- ✅ Only the eleven Core capabilities; no new stages/roles/boundaries.
- ✅ Build order honored (Audit→Registry→Authoring→Versioning→Jurisdiction→
  Resolution→Determination→Snapshot→Consumption).
- ✅ Started with ecosystem operational booleans, not government compliance.
- ✅ One binding production path (VBM bot deployment); no fallback, no duplicated
  rules.
- ✅ Same client contract reused across Prometheus/Content/Video (byte-identical).
- ✅ Core orchestrates only; mandate ownership stays in MDL.
- ✅ EchoForge excluded from the determination path; boundary preserved.
- ✅ No dependency on Atlas, Economic Core, CFRS, PERSE, UPM, or Veronica.
