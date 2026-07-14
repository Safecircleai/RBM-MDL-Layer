# IAF Innovation Assessment — RBM MDL Layer

**Status:** FOUNDATIONAL — the first application of the Innovation Assessment Framework (IAF) to this
node. Ratification rests with the Human Ratifying Authority. Architecture and doctrine only.

**Framework provenance [FACT]:** the *reusable* IAF is owned by the ecosystem home (referenced as
`SafeLaunchCenter/innovation-assessment/`), which is **not present in this workspace**; the only in-tree
authority for the rubric is the reference self-application in
`RBM-Economic-Core/innovation/Innovation_Assessment_Reference_Implementation.md`. This assessment
reconstructs the rubric from that reference and applies it here.

**Run order [FACT]:** the IAF runs **after** the IEF (`IEF_Classification.md`), which classified this
node as a *better-composition pre-implementation specification*. The IAF therefore assesses novelty of a
node that is doctrine-only, with **no reduction to practice**.

**Gate:** **G0→G1 (inception / architecture set)**. Re-confirm at implementation.

**Honesty rule adopted [FACT]:** novelty is **capped at Notable/Strong pending a professional prior-art
search**; at Concept maturity there is no reduction to practice, so **no patent is ripe to file**
(reference `Innovation_Assessment_Reference_Implementation.md:91,100`). This assessment refuses
inflation on its own node.

---

## 1. Classification (the five axes)

| Axis | Value | Note |
|---|---|---|
| **A · Ecosystem function** | **Domain / Infrastructure** | A cross-node mandate authority. |
| **B · Innovation type (Henderson–Clark)** | **Architectural** | Reuses known components (deterministic evaluation, versioning, event-sourced audit) under a *new authority/ownership architecture*; it does not invent the components. |
| **C · Market posture** | **New-market / sustaining hybrid** | New as ecosystem infrastructure; sustaining relative to existing GRC/policy tooling. |
| **D · Novelty origin** | **Architectural primitive (primary) + governance/business-logic (secondary)** | The partition and the jurisdiction+snapshot binding, not the engine. |
| **E · Maturity** | **Concept (TRL 1–3)** | Doctrine only; nothing depends on it. |

Five-tuple: **Domain · Architectural · new-market/sustaining · Primitive+Governance-logic · Concept.**

## 2. Architectural primitives (with provenance)

Each primitive: boundary → five-tests pass/fail → provenance tag → counterfactual.

| Primitive | Provenance | Counterfactual (what its absence would cost) |
|---|---|---|
| Deterministic rule evaluation | **inherited** (OPA/Cedar/Drools) | Nothing — freely available elsewhere. |
| Policy/service decoupling | **inherited** (OPA) | Nothing — established pattern. |
| Versioning + effectivity windows | **adapted** (GRC) | Modest — re-derivable from GRC practice. |
| **Jurisdiction precedence stack + declared inheritance (FLOOR/ADDITIVE/OVERRIDE)** | **composed / novel-here** | Without it, cross-jurisdiction conflict resolution is hand-coded per node — the fragmentation MDL exists to end. |
| **Determination-bound immutable snapshot (version-pinned)** | **composed** | Without it, "the engine decided" is not reproducible; audit degrades to logs. |
| **AUTHOR / RESOLVE / ACT partition for mandates-as-infrastructure** (single resolver, external author, external actor, read-only supervisor) | **novel-here** (candidate) | Without it, a mandate engine either legislates policy it shouldn't, or is advisory noise a node ignores — the two failure modes the partition prevents. |

**Primitive count (novel-here only, per anti-double-counting): 2** — the AUTHOR/RESOLVE/ACT partition and
the jurisdiction-precedence-as-resolution-primitive. The snapshot binding is **composed** (event-sourcing
+ decision), counted as adaptation, not invention. The evaluation engine and versioning are **not**
counted as this node's invention.

## 3. Novelty scoring (D1–D6 vector; 1–5 scale; band capped at Strong pending search)

| Primitive | D1 Novelty | D2 Non-obv | D3 Arch depth | D4 Defensibility | D5 Reuse | D6 Value | Band |
|---|---|---|---|---|---|---|---|
| **AUTHOR/RESOLVE/ACT partition (mandates)** | 3 | 3 | 4 | 2 | 4 | 4 | **Notable→Strong** |
| **Jurisdiction-precedence-as-primitive** | 2 | 2 | 3 | 2 | 4 | 4 | **Notable** |
| Determination-bound snapshot | 2 | 2 | 3 | 2 | 3 | 4 | **Notable** |

Bands scale routine → notable → strong → exceptional. **Nothing is scored Exceptional**, and Strong is
provisional pending a professional prior-art search — because the individual mechanisms are prior art and
only their *composition and ownership framing* is candidate-novel. **[INFERENCE]**

## 4. IP candidates (routes; none ripe to file at Concept)

| Candidate | Route | Rationale |
|---|---|---|
| Cross-node mandate resolution with jurisdiction-precedence + version-pinned snapshot | **Patent — monitor** | Possible method claim, but reduction-to-practice absent; monitor until implementation; prior-art search required first (OPA/Cedar/GRC are dense art). |
| AUTHOR/RESOLVE/ACT partition + read-only governance-supervisor boundary | **Trade secret / defensive publication — candidate** | The *ownership architecture* is doctrine already partly public; best protected by being the reference implementation and defensively published, not patented. |
| The deterministic resolution algorithm specifics | **Trade secret — candidate** (if any non-obvious optimization emerges at implementation) | Nothing to protect yet; flag for re-assessment at implementation. |

**Commodity implementations (explicitly not IP):** the rule engine, the rule categories, the event log,
the versioning — all prior art; protecting them would be inflation.

## 5. Commercialization

Vectors: **platform** (be the shared authority every node builds on), **standard** (the mandate contract
others conform to), **moat** (network effects — value compounds as more nodes depend on one authority),
**license** (the speculated external multi-jurisdiction-compliance product). Top **CRL: Hypothesis** —
none realizable until dependents exist.

## 6. Registry summary (governed projection)

```
node                : rbm-mdl-layer
last_assessed_gate  : G0→G1 (doctrine) · freshness: re-assess at implementation
classification      : Domain · Architectural · new-market/sustaining · Primitive+Governance-logic · Concept
primitive_count     : 2 (novel-here); 3 adapted/inherited (not counted)
candidates_by_band  : { routine: n/a, notable: 3, strong: 0–1 (pending prior-art search), exceptional: 0 }
ip_candidates       : { patent: 1 (monitor), trade_secret: 2 (candidate), defensive: 1 (candidate) }
commercialization   : { vectors: [platform, standard, moat, license], top CRL: hypothesis }
protection_ceiling  : open/internal (doctrine partly public); patent not ripe (no reduction to practice)
```

**Headline:** *MDL's mechanisms are largely prior art; its candidate novelty is the AUTHOR/RESOLVE/ACT
ownership architecture applied to mandates-as-ecosystem-infrastructure, scored Notable (provisionally
Strong pending prior-art search), with no patent ripe to file until reduction to practice.*
