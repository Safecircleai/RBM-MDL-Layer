# MDL vs Existing Industry Systems — Honest Comparative Analysis

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Feeds:** `IEF_Classification.md` (§Comparable
Systems) and `IAF_Innovation_Assessment.md` (§Novelty). **Evidence discipline:** claims about external
systems are **[FACT]** where they restate well-documented public behavior of those systems as of the
2026 knowledge horizon, and **[INFERENCE]** where they are this sprint's comparison. This analysis is
deliberately deflationary: it foregrounds what already exists before claiming anything is novel.

---

## 0. The honest posture

The brief asks for intellectual honesty about "what already exists, what MDL improves, what is genuinely
novel, and where MDL is simply composing existing ideas." Most of MDL's *primitives* are prior art. The
comparison below establishes that plainly; the novelty claim (`IAF_Innovation_Assessment.md`) is
confined to what survives it.

---

## 1. The comparable systems

| System | What it is | Class vs MDL | Overlap with MDL | Where MDL differs |
|---|---|---|---|---|
| **Open Policy Agent (OPA) / Rego** | General-purpose policy engine; evaluates JSON input against declarative Rego policies; returns a decision. **[FACT]** | **Direct competitor (mechanism)** for *policy evaluation*. | Declarative rules, deterministic evaluation, decoupled policy-from-service. | OPA has **no first-class jurisdiction precedence stack, no versioned mandate object with effectivity windows, no immutable snapshot bound to a determination, and no dual-authorized override-with-expiry**. It is a policy *evaluator*, not a mandate *authority with an audit-grade memory*. |
| **AWS Verified Permissions / Cedar** | Managed authorization service over the Cedar policy language; fine-grained permit/forbid decisions. **[FACT]** | **Direct competitor (mechanism)** for *authorization decisions*. | Declarative, deterministic, principal/resource/context model resembling entity/applicability. | Cedar is an **authorization** model (can principal X do action Y on resource Z), not a **compliance-mandate** model (which regulatory/contractual obligations apply and are they satisfied). No jurisdiction inheritance, no snapshot/version audit artifact, no financial-override supremacy. |
| **Cedar (language)** | The open policy language under Verified Permissions; analyzable, deterministic. **[FACT]** | **Adjacent / partial primitive** — a candidate *encoding language*, not a competitor to the node. | Deterministic, analyzable rule evaluation. | Language-level only; owns no lifecycle, no jurisdiction stack, no snapshot memory. |
| **ServiceNow (policy/GRC)** | Enterprise workflow + governance/risk/compliance modules; policy, control, and attestation management. **[FACT]** | **Adjacent** for *GRC workflow*. | Policy lifecycle, attestation, audit. | Workflow-and-record oriented, not a *deterministic cross-node resolution engine*; jurisdiction precedence and snapshot-immutability-per-determination are not its model; it is a platform product, not shared node-agnostic infrastructure. |
| **Government policy / rules engines** (benefits eligibility, tax rules-as-code) | Jurisdiction-specific determination systems (e.g. benefit eligibility, tax computation). **[FACT]** | **Partial replacement** for *eligibility/threshold determination in one jurisdiction*. | Jurisdictional rules, eligibility/threshold logic, deterministic computation. | Each is **single-jurisdiction and single-domain**; none is a *cross-node, multi-jurisdiction precedence-resolving* authority reusable by unrelated business verticals. |
| **Business rule engines** (Drools, etc.) | Forward-chaining rule evaluation over a working memory. **[FACT]** | **Adjacent primitive** — a candidate evaluation mechanism. | Declarative rules, deterministic firing. | No mandate object, no jurisdiction stack, no versioned snapshot audit, no override model — an engine, not an authority. |
| **Eligibility engines** (insurance/benefits) | Determine qualification against program rules. **[FACT]** | **Partial replacement** for the *eligibility* capability. | Rule-based qualification. | Vertical-specific; not node-agnostic infrastructure; no cross-jurisdiction precedence. |
| **Workflow engines** (Camunda, Temporal, etc.) | Orchestrate multi-step processes/state. **[FACT]** | **Adjacent** — an orchestration substrate MDL's *authoring lifecycle* could run on. | State transitions, audit of steps. | Orchestration, not policy resolution; owns no mandate truth. |
| **EchoForge Trust Service Runtime** (in-ecosystem) | One contract/registry/API for *discipline* determinations (HIPAA/Legal/Tax/PCI). **[FACT]** `EchoForge/echoforge/trust/contract.py:5-14`. | **Adjacent peer** — the closest in-ecosystem system; must be disambiguated. | Node-agnostic, jurisdiction/regulation facets, deterministic-ish determinations, evidence provenance. | See §2 — the seam is definition/resolution-of-mandates (MDL) vs discipline-law-determination (Trust Runtime). |

## 2. MDL vs the Trust Runtime (the in-ecosystem look-alike)

This is the comparison the ecosystem most needs, because both call themselves "node-agnostic" and both
carry jurisdiction/regulation concepts, risking the very duplication the Trust Runtime doctrine warns
against (`EchoForge/TRUST_RUNTIME_ARCHITECTURE.md:196-199`). The seam **[INFERENCE, evidence-anchored]**:

| Axis | RBM MDL Layer | Trust Service Runtime |
|---|---|---|
| **Question answered** | "Which *mandates* (regulatory/contractual/org/operational obligations) apply to this entity, at what version, in which jurisdiction, and are they satisfied?" | "Given this subject, what does a *discipline's body of professional law* (HIPAA/Legal/Tax/PCI) say — permitted / blocked / requires-review?" (`contract.py:81-95`) |
| **Primary object** | A versioned **mandate** with rule sets + an immutable **snapshot**. | A **TrustDetermination** — a machine assessment carrying a non-authority disclaimer (`contract.py:357-364`). |
| **Authority stance** | *Authoritative and binding* over its mandate truth (financial-override supremacy). | *Explicitly non-authoritative* — "not a legal, tax, medical … authority" (`contract.py:357-364`). |
| **Memory** | Snapshot-per-determination is the core artifact. | Determinations are produced on demand; grounding/provenance carried, not a versioned mandate registry. |
| **Relationship** | MDL **may consume** a Trust determination as *one satisfaction condition* of a mandate. | The Trust Runtime does not define or resolve mandates. |

**Conclusion:** they are complementary layers, not duplicates. MDL is the *mandate authority and
resolution engine*; the Trust Runtime is the *discipline determination engine*. A clean composition:
MDL resolves the applicable mandates; where a mandate's satisfaction requires a discipline judgment, MDL
calls the Trust Runtime and treats its `outcome` as an input. This must be stated in both nodes' doctrine
to prevent drift (`Open_Questions_and_Risks.md`).

## 3. What already exists, what MDL improves, what is genuinely novel

**Already exists (prior art MDL reuses, not invents):**
- Declarative, deterministic policy/rule evaluation (OPA, Cedar, Drools). **[FACT]**
- Decoupling policy from services (OPA's core value proposition). **[FACT]**
- Jurisdiction-specific rules-as-code (government tax/benefit engines). **[FACT]**
- Immutable audit logs / event sourcing (a standard architectural pattern). **[PRINCIPLE]**
- Policy versioning and effectivity windows (common in GRC and rules platforms). **[FACT]**

**What MDL improves (better composition of known parts):**
- It **binds** deterministic evaluation to a **first-class jurisdiction precedence stack with declared
  inheritance behaviors** (FLOOR/ADDITIVE/OVERRIDE) — most engines leave precedence to hand-written
  rules; MDL makes it a resolution primitive. **[INFERENCE]**
- It **binds every determination to an immutable, version-pinned snapshot** as the audit artifact —
  turning "the engine decided" into "the engine decided *this exact rule set*, reproducibly, forever."
  **[INFERENCE]**
- It makes a **financial override authoritative across an entire ecosystem of unrelated business
  verticals** through one node — a cross-vertical supremacy most vertical rules engines cannot express.
  **[INFERENCE]**

**What is (candidate) genuinely novel — subject to the IAF cap:**
- The **AUTHOR / RESOLVE / ACT ownership partition** applied to *mandates as ecosystem infrastructure*:
  a single node that resolves-and-determines but neither authors the source nor acts, with a supervisor
  that watches but cannot alter. This *institutional* separation — not the evaluation mechanism — is the
  candidate novelty (`IAF_Innovation_Assessment.md`). **[INFERENCE]**

**Where MDL is simply composing existing ideas (stated plainly):** the evaluation engine, the rule
categories (documents/evidence/thresholds/participation), versioning, and the event/audit log are all
established patterns. The composition's *value* is real; its *mechanisms* are largely prior art. Honesty
here is the point (`IEF_Classification.md` §honesty).
