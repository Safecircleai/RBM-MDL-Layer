# Ratification Log

**Status:** APPEND-ONLY LEDGER of constitutional ratifications issued by the Human Ratifying Authority (HRA).
Entries are immutable once recorded; a later change is a new entry, never an edit (mirrors the mandate-audit
discipline). The HRA occupant and succession are recorded in `Ratification_Authority.md`.

**Interim HRA occupant at time of these entries:** the **Founder** (exclusive ratification authority per
`Ratification_Authority.md` §1).

---

## R1 — Constitutional Foundation · Ratified · 2026-07-14
**Decision:** **Ratified.** The MDL Constitution and its foundational doctrine are established as the
governing document of RBM-MDL-Layer.
**Effect:** the internal doctrine ceases to be "proposed foundation pending ratification" and becomes the
governing constitution. Status surfaces (`README.md`, `ATLAS_STATUS.md`, `.atlas-config.yaml`) updated to
reflect ratified standing.
**Authored amendment:** status-line updates only; no doctrinal clause changed by R1 itself.

## R2 — Canonical Jurisdiction Stack · Ratified: Option B · 2026-07-14
**Decision:** **Option B — the FEDERAL-anchored two-class model** (`Jurisdiction_Stack_Ratification_Analysis.md`
§7–§8). Rationale recorded by the HRA: it is the only option consistent with the Economic Core, the Trust
Runtime, LEAL, future international expansion, and legal reality; the separation of **precedence** from
**minimum required compliance (floor)** is the correct architectural distinction. The MDL Specification's
**PRIME-apex ordering is explicitly rejected** (Option D) as legally invalid.
**Effect:** unblocks Jurisdiction Resolution (capability C3; audit A1/Q1 resolved).
**Authored amendment:** `MDL_Lifecycle.md` §4 replaced with the ratified two-class stack + governing rules;
`Open_Questions_and_Risks.md` A1/Q1 marked resolved; downstream `[BLOCKED-INPUT]` jurisdiction markers flipped
to ratified.

## R3 — Authoring / Operations Roles · Ratified: four constitutional roles · 2026-07-14
**Decision:** do **not** define a generic "Operators" role. Formalize **four constitutional roles** with
**separation of duties**; **operational staff are never constitutional actors** (they may only act *under* a
constitutional role, never *as* one):
1. **Human Ratification Authority (HRA)** — ratifies constitutional changes, jurisdiction changes, and
   immutable doctrine; **never performs operational authoring.**
2. **Governance Author** — drafts mandates; creates versions; **cannot publish.**
3. **Governance Reviewer** — reviews; rejects; requests revisions.
4. **Governance Publisher** — publishes approved mandates; makes versions effective; **cannot modify content.**
**Effect:** resolves audit CR-2 (the undefined "Operators"/"ops-admin" and phantom "Executive/Operational"
actors); defines the RBAC of the authoring workflow (C10) and the admin/publish projections (C11).
**Authored amendment:** `MDL_Consumer_Model.md` gains an "internal governance roles" section; the "Operators"
row and phantom "Executive/Operational" references are replaced by the four ratified roles across
`MDL_External_Interfaces.md`, the matrices, and the engineering authoring/state/contract specs.

## R4 — Revocation / Void-ab-initio · Ratified: own doctrine · 2026-07-14
**Decision:** this deserves its **own doctrine** because it affects evidence preservation. The ratified model:
**nothing is ever deleted.** If authority was invalid:
- the **determination becomes invalid**,
- the **mandate becomes void** (ab initio — as if it never held authority),
- **snapshots remain immutable**,
- **audit history remains immutable**,
- **later determinations reference the invalidation.**
**Effect:** resolves audit CR-3 (revocation vs snapshot immutability) by making invalidation an *additive,
append-only overlay* that never mutates a snapshot or the audit trail — evidence is preserved in full.
**Authored amendment:** new doctrine `MDL_Revocation_And_Invalidation.md`; `engineering/MDL_State_Model.md`
adds the now-ratified **Void** transition (distinct from Retire); `MDL_Event_Model.md` adds `MANDATE_VOIDED`
and `DETERMINATION_INVALIDATED` (and promotes the retirement events to ratified); `engineering/MDL_Persistence_Model.md`
adds the **Invalidation Record** (append-only, immutable). *Note:* the **detection** of invalid authority
(delegation / authority-lineage — the other half of the audit CR-3 cluster) remains a future refinement; R4
ratifies the **remediation** semantics.

---

## Standing items not yet ratified (for the record)
- **Delegation / authority-lineage** (audit CR-3 cluster, detection half) — how a mandate's authoring
  authority is proven authorized at its scope. R4 supplies the remedy; the detection model is future work.
- **Storage retention / data-erasure vs snapshot immutability** (audit H-8) — an open constitutional pressure
  (`engineering/MDL_Persistence_Model.md` §7); not raised for ratification here.
- **Ownership of the uploaded operational specs** (audit Q2) — an ecosystem-scoped question, not MDL's to
  settle.
