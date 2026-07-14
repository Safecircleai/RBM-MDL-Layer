# Open Questions, Risks & Source-Reconciliation Report

**Status:** FOUNDATIONAL — the honest ledger of what is unresolved, and the record of how this doctrine
was reconciled with the uploaded operational specs. Ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Evidence discipline:** conflicts are **[FACT]**
(both sources quoted/located) or **[INFERENCE]** (this sprint's reading).

> **RATIFICATION UPDATE — 2026-07-14 (`Ratification_Log.md`).** Several items below are now **RESOLVED by HRA
> ratification** and are retained for history:
> - **A1 / Q1 (jurisdiction ordering) — RESOLVED (R2):** ratified as the FEDERAL-anchored two-class model
>   (Option B); the MDL Spec PRIME-apex ordering is explicitly rejected. See `MDL_Lifecycle.md` §4.
> - **CR-2 authoring/ops roles (Q7 authorship) — RESOLVED (R3):** four constitutional roles (HRA, Governance
>   Author/Reviewer/Publisher) with separation of duties; no generic "Operators". See `MDL_Consumer_Model.md`
>   §1a. *(The PROGRAM/INTERNAL authorship question Q7 is answered: a Governance Author under the workflow,
>   never operational staff as constitutional actors.)*
> - **CR-3 revocation — RESOLVED (R4, remediation half):** ratified as its own doctrine
>   `MDL_Revocation_And_Invalidation.md` (nothing deleted; void ab initio via append-only overlay). The
>   **detection** half (delegation / authority-lineage) remains open (below).
> Items still open: Q2 (spec ownership), Q3/Q4/Q5 (Trust-Runtime seam, eligibility line, discipline
> determinism), the **authority-lineage/delegation** detection model, and H-8 (retention vs erasure).

---

## PART A — Conflict & Source-Reconciliation Report

This part exists to answer one question directly: *does the authored doctrine conflict with the three
uploaded MDL spec documents, and where do the sources conflict with each other?* Each entry states the
conflict, the sources, and how this doctrine resolved it. **Where a conflict is between the sources
themselves, this doctrine picks a resolution and flags it for ratification — it does not silently
choose.**

### A1. Jurisdiction ordering — the sources disagree with each other **[FACT] — UNRESOLVED, needs ratification**
Three source documents give three different precedence orderings:
- CFRS `EchoForge/MDL_LAYER_README.md:129,176-182`: **FEDERAL → STATE → PRIME → LOCAL**.
- Uploaded *MDL Specification* §2.4: **PRIME (Client Contract) → STATE → LOCAL → PROGRAM → INTERNAL**
  (PRIME at the **top**, FEDERAL absent).
- Uploaded *Jurisdiction Stack Model v1.0* §1: **FEDERAL → PRIME_CONTRACT → STATE → COUNTY → MUNICIPAL →
  PROGRAM → INTERNAL**.

**This is a real conflict *inside the uploaded specs*** (MDL Spec §2.4 puts PRIME above STATE with no
FEDERAL; the Jurisdiction Stack Model puts FEDERAL at the top). **Resolution taken:** `MDL_Lifecycle.md`
§4 adopts the *Jurisdiction Stack Model v1.0* (most complete, most granular, self-described as the
jurisdiction model) and records the divergence here. **Action required:** the Human Ratifying Authority
must ratify the canonical stack before implementation, because a wrong ordering silently changes every
conflict determination. *This is the single most important conflict to resolve.*

### A2. "Soft validator" vs "authoritative enforcement" **[FACT] — RESOLVED toward the uploaded specs**
- CFRS `EchoForge/MDL_LAYER_README.md:60,364-371` frames MDL as a **"Soft Validator"** that "does NOT
  hard-block … Calling code decides whether to gate."
- Uploaded *MDL Spec* §2.5, §12 and *Service Contract* §8 make determinations and financial overrides
  **authoritative** ("Financial enforcement is not advisory. It is authoritative.").

**Resolution taken:** this doctrine sides with the **uploaded specs** — determinations are authoritative;
a consumer *acts* but may not *contradict* (`MDL_Infrastructure_Constitution.md` §6; Constraint I6). The
reconciliation is the *determination vs act* split: MDL owns the binding determination; the node performs
the gating act; the Supervisor prevents bypass. **No conflict remains with the uploaded specs**; the
divergence is with the older CFRS README, which the migration supersedes. Flagged because it changes
integration semantics (a consumer may not treat a determination as advisory).

### A3. Standalone home — EchoForge-hosted vs independent node **[FACT] — RESOLVED toward independence**
- CFRS `EchoForge/MDL_LAYER_README.md:25,80-95` proposes an **"EchoForge MDL Service"** hosting MDL.
- Uploaded *MDL Spec* §10 is **host-neutral** ("Shared Internal Package" or "Internal Governance
  Service"); the uploaded *Service Contract* §2 treats MDL and EchoForge as **separate systems**.
- The task charter and this doctrine: an **independent node with its own repository**.

**Resolution taken:** independent node (`Repository_Ownership_Report.md`). **No conflict with the
uploaded specs** — they are host-neutral and the Service Contract's separation *supports* independence.
The only conflicting source is the older CFRS README's "EchoForge MDL Service" phrasing, which this
doctrine and Constraint C3 supersede (EchoForge supervises; it does not host or own).

### A4. "MDL enforces" vs "EchoForge supervises" vs "nodes enforce payable gating" **[FACT] — RESOLVED by role split**
The uploaded *MDL Spec* says MDL "enforces" (§1, §12); it also says nodes "enforce payable gating" (§11);
the *Service Contract* says EchoForge supervises and "cannot disable MDL enforcement" (§5). Read
literally, three parties "enforce."
**Resolution taken:** the three verbs are three different acts — MDL *owns the authoritative
determination*, the node *performs the gating act*, the Supervisor *ensures no bypass*
(`MDL_Responsibility_Matrix.md` §1, "Enforcement"). No source is contradicted; the doctrine names the
seam the specs leave implicit.

### A5. Node-type taxonomy vs ecosystem business-node taxonomy **[FACT] — CLARIFIED**
The uploaded *MDL Spec* §6 enumerates **NodeTypes**: FLEET, HOUSING, HUMAN_SERVICES, CONSTRUCTION,
PROCUREMENT, WORKFORCE, PROPERTY_MGMT, ENTERTAINMENT. The task's "Business Nodes" are **repositories**:
CFRS, UPM, RESA, Economic Core, Insurance, B4Arts, Customer Acquisition, PERSE. These are **two different
axes** — the spec's `NodeType` is a *domain/vertical scope filter within resolution*, while the
ecosystem's "business node" is a *consuming repository*. **No conflict**, but the terms collide;
`MDL_Consumer_Model.md` uses "Business-Node Consumer" for the repository and treats `NodeType` as a
resolution parameter. Flagged so no future reader conflates them.

### A6. Financial-override supremacy vs Economic Core's "does not self-exempt" **[FACT] — RESOLVED, complementary**
Uploaded *MDL Spec* §2.5 makes mandate financial policy override tax engines; Economic Core's doctrine
says it "enforces economic policy it does not author" and "does not Exempt the ecosystem" of its own
accord (`RBM-Economic-Core/RBM_Economic_Constitution.md:102-103`; `Economic_Truth_And_External_Authority.md:87`).
**No conflict:** MDL owns the *override determination*; the Economic Consumer *consumes and books* it
(`MDL_Truth_Ownership_Matrix.md` §4). The two doctrines are consistent by construction.

### A7. Data-model naming/count drift **[FACT] — noted for migration**
Uploaded *MDL Spec* §3.1 lists **9 core tables** and names `mandate_evidence_rules`; CFRS
`MDL_LAYER_README.md:104-121` lists **13 tables** and names `mandate_evidence_requirements` (plus
`mandate_node_types`, `mandate_asset_requirements`, `mandate_certification_requirements`,
`mandate_state_toggles`). **Not a doctrinal conflict** (this repo authors no schema), but a
**migration-time reconciliation item**: the extraction (`Migration_Strategy` S2) must map the CFRS 13
onto the spec's 9-table contract (or ratify the superset). Flagged.

### A8. "Correctness over elegance" clause **[FACT] — honored but unsourced**
The brief's constraint "Prefer correctness over elegance" **does not appear verbatim anywhere in the
in-tree corpus or the uploaded specs** (nearest analog: the IEF/IAF "authored to be exemplary, not
flattering"). It is honored as an explicit standing rule (`Architectural_Constraints.md` §3) rather than
cited. Flagged for transparency.

### A9. Absent referenced authorities **[FACT] — dependency gap**
Documents this doctrine and the ecosystem reference but that are **absent from the workspace**:
`SafeLaunchCenter/TRUST_INFRASTRUCTURE_NODE.md`, `DISCIPLINE_RUNTIME_CONTRACT.md`,
`TRUST_DOCTRINE_OWNERSHIP.md`, `EVIDENCE_OF_TRUTH_CONSTITUTION.md`, and the *reusable* IEF/IAF framework
definitions (only reference implementations exist). This doctrine reconstructs rubrics from the
reference implementations and flags the definitional sources as unauthored. No conflict, but a standing
gap the ecosystem should close.

**Bottom line:** *nothing in this authored doctrine conflicts with the three uploaded spec documents.*
The only hard conflict is **A1 — the jurisdiction ordering disagreement between the uploaded MDL Spec and
the uploaded Jurisdiction Stack Model**, which must be ratified. A2 and A3 are conflicts with the older
CFRS README that this doctrine deliberately supersedes and that the migration resolves.

---

## PART B — Open Questions

| # | Question | Why it matters | Owner of the answer |
|---|---|---|---|
| Q1 | What is the ratified canonical jurisdiction stack (A1)? | Changes every conflict determination. | Human Ratifying Authority |
| Q2 | Who owns the three uploaded operational specs as documents? | Single-owner rule requires one home; this node governs-consistency but should not silently claim ownership. | Ecosystem doctrine home / HRA |
| Q3 | Exactly where is the MDL ↔ Trust Runtime seam drawn, and is it ratified in *both* repos? | Prevents the duplication both nodes' doctrine warns against. | RBM-MDL-Layer + EchoForge, ratified |
| Q4 | For eligibility, what is the precise line between MDL's *status* and the node's *grant/deny decision*? | Avoids MDL drifting into business decisions. | RBM-MDL-Layer + consuming node |
| Q5 | Does MDL *consume* discipline determinations, or merely reference them, in Era 4? | Determinism: a consumed external determination must itself be deterministic/snapshot-able. | RBM-MDL-Layer |
| Q6 | Migration table mapping (A7): adopt the spec's 9 or the CFRS 13 as the contract? | Correctness of the data lift. | Migration owners |
| Q7 | Are `PROGRAM`/`INTERNAL` layers authored by orgs (Mandate Authoring Authority) or configured by nodes? | Determines who may write those mandate layers. | RBM-MDL-Layer governance |

## PART C — Risks

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | **Wrong jurisdiction ordering shipped** (A1 unresolved). | High | Block implementation on Q1 ratification; encode the stack as ratified doctrine, not config. |
| R2 | **Dual authoritative engines during migration** (CFRS + node diverge). | High | Strangler-fig: shadow-compare (S3), flagged cutover (S4), retire last (S5); never two live authorities. |
| R3 | **Determinism erosion** — a future "smart"/model-driven resolver. | High | Constraint I1; no model in layers 1–7 (`MDL_Internal_Architecture.md`). |
| R4 | **Snapshot corruption in the data lift.** | High | S2 exit criterion: node reproduces every historical determination from migrated snapshots byte-for-byte. |
| R5 | **Duplication with the Trust Runtime** (both "node-agnostic"). | Medium | Q3 seam ratified in both repos; `MDL_vs_Industry_Systems.md` §2. |
| R6 | **Scope inflation** — claiming multi-vertical at extraction. | Medium | Extraction ≠ generalization (`Migration_Strategy` §4); IEF honesty bar. |
| R7 | **Supervisor over-reach** — EchoForge granted write/disable. | Medium | Constraint I7; interface matrix denies write/disable to the Supervisor. |
| R8 | **Consumer treats a determination as advisory** (A2 legacy). | Medium | Constraint I6; consumption model §3–4 make binding-ness explicit. |
| R9 | **Absent ecosystem authorities** (A9) leave rubrics/doctrine unratified. | Low–Medium | Flag definitional gaps; reconstruct from references; escalate closure to the ecosystem. |
| R10 | **Institution/infrastructure claim outruns evidence.** | Low | IEF caps the claim at pre-implementation until a real dependent exists. |
