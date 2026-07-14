# IEF Classification — RBM MDL Layer

**Status:** FOUNDATIONAL — the first application of the Institutional Evaluation Framework (IEF) to this
node. Ratification rests with the Human Ratifying Authority. Architecture and doctrine only.

**Framework provenance [FACT]:** the *reusable* IEF is owned by the ecosystem home (referenced as
`SafeLaunchCenter/institutional-evaluation/`), which is **not present in this workspace**; the only
in-tree authority for the rubric is the reference self-application in
`RBM-Economic-Core/institutional-evaluation/Institutional_Evaluation_Reference_Implementation.md`. This
classification reconstructs the rubric from that reference and applies it here. Where the framework
definition is needed but absent, that is flagged.

**Run order [FACT]:** IEF runs **before** the IAF — "classification precedes the question of novelty"
(`RBM-Economic-Core/institutional-evaluation/README.md:28-29`). The honesty bar is deliberate: a first
evaluation that inflates its own node teaches every future node to do the same.

**Gate:** **E0→E1 (inception / architecture set)** — doctrine exists; no implementation, nothing depends
on it yet.

---

## The twelve determinations

Each determination carries a **confidence** label ∈ {Evidenced, Provisional, Insufficient Evidence}, per
the reference rubric.

**1. Domain & Institutional Identity.** Bounded domain: the *definition, versioning, jurisdiction-
resolution, satisfaction-determination, snapshotting, and override of mandates across business nodes*.
Institutional role today: performed as embedded business logic inside CFRS (#115), not by any
ecosystem institution. **[FACT** per `RBM_CAPABILITIES_V1.md:1624`**]** · Confidence: **Evidenced**.

**2. Comparable Systems.** Direct competitors (mechanism): OPA/Rego, AWS Verified Permissions/Cedar.
Adjacent: ServiceNow GRC, Drools, workflow engines, the in-ecosystem Trust Runtime. Partial replacement:
government/eligibility engines (single-jurisdiction). Full analysis: `MDL_vs_Industry_Systems.md`. A
"new category with no comparables" claim is **foreclosed** — mature comparables exist. · Confidence:
**Evidenced**.

**3. Primitive Provenance.** Each primitive tagged inherited / adapted / composed / novel:
- Deterministic rule evaluation — **inherited** (OPA/Cedar/Drools).
- Policy/service decoupling — **inherited** (OPA).
- Versioning + effectivity — **adapted** (GRC platforms).
- Jurisdiction precedence stack + inheritance behaviors — **composed** (jurisdictional rules-as-code +
  precedence).
- Determination-bound immutable snapshot — **composed** (event-sourcing + policy decision).
- AUTHOR/RESOLVE/ACT partition for mandates-as-infrastructure — **novel-here** (candidate).
- Provenance profile: **inherited 2 · adapted 1 · composed 2 · novel 1** · Confidence: **Evidenced** for
  the inherited/adapted; **Provisional** for the novel (pending prior-art search).

**4. Layer Classification.** The ladder is application / service / platform / **infrastructure** /
**institution**. Rule: *infrastructure is constituted by dependence; an institution persists across
operators.* Today **nothing depends on this node** (it is empty), so:
- Pre-implementation specification — **Evidenced**.
- Infrastructure — **Insufficient Evidence** (no dependents yet).
- Institution — **Insufficient Evidence** (no persistence across operators yet).
The *aspiration* is infrastructure (the uploaded specs and #115's cross-node design support it), but
aspiration is not evidence. · Confidence: **Evidenced (pre-implementation) / Insufficient (infra,
institution)**.

**5. Institutional Replacement Test.** Currently depended upon? **No** — no node consumes it yet; CFRS
still runs its embedded MDL. Sharpest rule: *a node nothing depends on cannot yet be the infrastructure
it aspires to be.* The test is **not yet passable**; it becomes passable when the first business node
retires its embedded logic and depends on this node (Migration Strategy Stage 2). · Confidence:
**Insufficient Evidence** for "depended upon".

**6. Economic Classification.** Candidate: **infrastructure / protocol-like** — a shared governance
backbone many verticals would consume, with cross-vertical value noted in the source
(`RBM_CAPABILITIES_V1.md:4163`). Not a cost centre by design; but until dependence exists this is
**Provisional**.

**7. Governance Analysis.** Requirement type: **constitutional** (this repository's constitution governs
its authority and independence) layered over **regulatory/operational** (the mandates it compiles are
regulatory; its enforcement is operational). · Confidence: **Evidenced**.

**8. Commercialization Analysis.** Natural model: shared internal infrastructure; the capability note
speculates external licensability ("standalone licensable product for any multi-jurisdiction compliance
use case," `RBM_CAPABILITIES_V1.md:1635`). Readiness band: **concept**. · Confidence: **Provisional**.

**9. IP / Value-Locus.** Primary locus among composition / governance / network-effects / operational-
expertise / patents: **composition + governance** (the ownership partition and the jurisdiction+snapshot
binding), with **network effects** latent (value grows as more nodes depend on one authority). Patent
questions deferred to the IAF. · Confidence: **Provisional**.

**10. Category Creation Test.** Determination: **better composition** — *not* a new institutional
category. MDL composes established primitives (deterministic evaluation, versioning, event-sourced audit,
jurisdictional rules) under a new ownership architecture. It does not invent a new category of software.
· Confidence: **Evidenced**.

**11. Readiness.** Roll-up verdict: **Partially Ready (as doctrine)** — the constitutional/architectural
layer is complete and internally consistent with the uploaded specs; infrastructure/institution status
is **Insufficient Evidence** pending real dependents. Re-evaluation trigger: **E2 (reduction to
practice)** — the first gate at which a real dependent can create the dependence and persistence evidence
the higher rungs require. · Confidence: **Evidenced**.

**12. What this classification demonstrates.** It demonstrates the honesty bar: a brand-new node with
genuine architectural ambition is classified as a **better-composition, pre-implementation
specification**, with infrastructure and institution status explicitly **unearned** until something
depends on it. Inflating it to "institution" now would be exactly the drift the framework refuses.

---

## Registry projection (governed output)

```
node                : rbm-mdl-layer
last_evaluated_gate : E0→E1 (doctrine) · re-evaluate at E2 (reduction to practice)
layer               : pre-implementation specification (Evidenced);
                      infrastructure (Insufficient Evidence); institution (Insufficient Evidence)
readiness           : partially-ready (as doctrine)
economic_function   : infrastructure/protocol-like (Provisional)
governance_requirement : constitutional over regulatory/operational (Evidenced)
category_determination : better composition (Evidenced) — not a new institutional category
escalations_pending : none (category test did not trigger escalation)
```

**Headline:** *RBM MDL Layer is, today, a better-composition pre-implementation specification with a
credible path to infrastructure — a path it has not yet walked, because nothing depends on it yet.*
