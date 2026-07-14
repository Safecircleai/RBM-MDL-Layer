# The MDL Consumption Model

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only — this describes *how* consumers integrate, at the doctrinal
level; it defines no API code or schema.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `MDL_External_Interfaces.md`,
`MDL_Event_Model.md`, and the uploaded *MDL Specification* §4–5 (the engine contract & integration
rules) and *Service Contract* §3.

---

## 0. The consumption contract, in one sentence

**A consumer passes entity context to MDL before financial finalization, receives an authoritative
determination, and acts on it — it never duplicates, forks, contradicts, or bypasses mandate logic.**
(uploaded *MDL Spec* §5.)

---

## 1. The four ways to consume MDL

| Mode | What it is | Who uses it | Doctrine |
|---|---|---|---|
| **Pull — resolve/determine** | Synchronous request: pass context, get the resolved mandate set and/or the compliance determination. | Business-Node, Economic Consumer | The core integration path; must run *before* financial finalization (uploaded *MDL Spec* §2.1, §5). |
| **Pull — snapshot/status retrieval** | Read a prior determination's snapshot or the latest validation status (e.g. for payable gating). | Business-Node, Auditor | `get_latest_validation_status` gates payables (uploaded *MDL Spec* §4.5). |
| **Push — event subscription** | Subscribe to the mandate-domain event stream; react to mandate/version/override changes. | Business-Node, Economic, Supervisor, Intelligence | Sole publisher is MDL; consumers subscribe read-only (`MDL_Event_Model.md`; uploaded *Service Contract* §4). |
| **Authoring (guarded)** | Submit an authored obligation into the governed intake→approve→version workflow. | Mandate Authoring Authority, granted ops/authoring roles only | Role-based; the domain compiles, it does not legislate (uploaded *Service Contract* §7). |

## 2. The engine contract consumers build against (doctrinal reference)

The operational entry points are fixed by the uploaded *MDL Specification* §4 and *Service Contract* §3.
This doctrine references them so the constitution and the operational contract stay aligned; it does not
re-specify them:

- `resolve_applicable_mandates(context)` — the applicable mandate set for an entity context.
- `create_mandate_snapshots(entity)` — immutable snapshot per mandate version; **idempotent**.
- `validate_entity_against_mandates(entity)` — `compliance_status`, `missing_documents`,
  `missing_evidence`, `threshold_blocks`, `participation_blocks`.
- `resolve_tax_policy(entity)` — `is_tax_exempt`, `reason`, `mandate_id`, `mandate_version`; resolved
  **before** invoice totals are finalized.
- `get_latest_validation_status(entity)` — used for payable gating.

Read-only supervision endpoints (`GET /mdl/mandates`, `GET /mdl/snapshots/{id}`,
`GET /mdl/validation-results/{entity}`) are exposed to the Governance Supervisor only (uploaded *Service
Contract* §3).

## 3. The consumer's obligations (the "compliance zone")

A node is **governance-ready** — eligible to participate — only when it meets the uploaded *MDL Spec*
§11 minimum compliance zone. Restated as consumer obligations:

1. **Integrate MDL for enforcement** — resolve/validate before financial finalization.
2. **Use snapshot-based validation** — reference snapshots, never re-derive compliance locally.
3. **Respect mandate financial overrides** — honor `tax_exempt_override` (bind, do not contradict).
4. **Log override activity** — surface override use into the audit trail.
5. **Enforce payable gating** — act on `get_latest_validation_status` before paying.

A consumer that does not meet these is not merely non-compliant; it is **not governance-ready** and, per
the uploaded *MDL Spec* §11, cannot reach maturity ("No node reaches maturity without MDL integration,"
§1).

## 4. What a consumer must never do

Restated from `MDL_Consumer_Model.md` §2 and the uploaded *MDL Spec* §5:
- **Never duplicate** mandate enforcement logic or keep a parallel mandate authority.
- **Never hardcode** compliance rules outside MDL.
- **Never bypass** `tax_exempt_override` or any authoritative determination.
- **Never modify** snapshot history or a determination it received.
- **Never assume** it is MDL's only consumer, or require MDL to adapt to its internal design.

## 5. The determinism guarantee the consumer can rely on

Because resolution and determination are deterministic (`MDL_Infrastructure_Constitution.md` §1.2), a
consumer that passes identical context receives an identical result and an identical snapshot. This is
what makes MDL safe to depend on: a consumer never has to reconcile two different answers to the same
question, and an auditor can reproduce any determination from its snapshot and versions. Determinism is
the property that turns "call the shared service" from a risk into a guarantee.
