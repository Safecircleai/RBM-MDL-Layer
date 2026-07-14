# Architecture Audit Report — RBM MDL Layer

**Prepared by:** External Architecture Review Board (adversarial constitutional audit).
**Scope:** every document in `RBM-MDL-Layer/` (23 root docs + IEF/IAF + placeholder READMEs), cross-checked
against each other and against the boundary claims in `RBM-Economic-Core/` and `EchoForge/echoforge/trust/`.
**Mandate:** attempt to *break* the architecture. Analysis only — this report rewrites no doctrine and
proposes no new architecture. Every finding carries file:line evidence; suspected defects that did **not**
hold are stated explicitly for honesty.

---

## 0. Verdict

**The architecture does NOT fully survive the audit.** The *method* is sound — constitutional
independence genuinely holds (the ten-year runtime-replacement test passes; no repository-to-runtime
coupling; no ownership cycle), and the AUTHOR/RESOLVE/ACT framing is a defensible seam. But there are
**five CRITICAL defects** that would, as written, produce duplicate truth, phantom authority, a
constitutional contradiction, or an inability to scale — each of which must be resolved before
implementation. Below CRITICAL sit a substantial band of HIGH implementation-purity and boundary
findings. The doctrine's own honesty apparatus (`Open_Questions_and_Risks.md`) already catches roughly a
third of these; the audit's value is the two-thirds it does not.

**One-line summary:** *the constitution is independent and coherent in the abstract, but its authoritative
grids reference actors it never defines, its immutability guarantees collide with revocation and
data-law, its single-global-owner claim does not survive jurisdictional sovereignty, and its purity is
breached by implementation detail throughout.*

| Severity | Count | Gist |
|---|---|---|
| CRITICAL | 5 | duplicate truth; phantom authority + self-audit failure; revocation-vs-immutability; determinism-vs-discipline-consumption; single-owner-vs-sovereignty |
| HIGH | 11 | implementation leaks (×4), CFRS-specificity, EchoForge escalation-ladder leak, jurisdiction-stack ceiling, storage/erasure, industry-analog omission, "consumer" overload, independence over-claim |
| MEDIUM | 9 | override/enforcement overloads, retire-vs-stale, supervisor-enforcement dependency, IEF/IAF external ownership, tie-break bottleneck, eligibility two-owner cell, etc. |
| LOW | 6 | undefined minor terms, table-count drift, term interchange, activation event, knowledge-horizon date |

---

## 1. CRITICAL findings

> Trigger set (per the audit brief): duplicate truth · duplicate authority · circular ownership ·
> repository coupling · inability to scale · constitutional contradiction.

### CR-1 — Duplicate truth: "Validation" and "Enforcement" are the same MDL-owned truth, listed twice
**Trigger: duplicate truth.**
`MDL_Truth_Ownership_Matrix.md:44` — "**Validation** (satisfaction of resolved mandates) | … | **MDL
domain** (deterministic validation + snapshot)"; `:45` — "**Enforcement** | … | **MDL domain** owns the
*authoritative determination* (compliant / override / block-condition)". Both rows are owned by the MDL
domain and both *are* the compliance determination (the verdict "compliant" appears in each). The matrix's
own premise is that "no truth is left with an ambiguous owner" (`:14`). Additionally there is no
"Enforcement" capability in `MDL_Capability_Framework.md` §1 to back the row — the truth exists twice in
the matrix and zero times in the capability set. **Effect:** one authoritative truth carries two labels;
downstream consumers cannot tell whether "Validation" and "Enforcement" are one obligation or two.

### CR-2 — Phantom authority in the authoritative grids, and the independence self-audit certifies it "Clean"
**Trigger: duplicate/undefined authority + constitutional contradiction.** `MDL_Consumer_Model.md:9` declares
itself "the interpretive key to every other document," and its rule (`:26-29`) is that every cell names the
domain or a *defined* role. The grids violate this:
- **"Executive / Operational" consumer** — undefined in the role table (`MDL_Consumer_Model.md:39-49`) yet
  granted **read *and act*** authority: `MDL_Truth_Ownership_Matrix.md:47` "Executive/Operational and
  Intelligence consumers"; `MDL_Responsibility_Matrix.md:49` "…| Executive acts on it |". An undefined actor
  is exercising authority in the authoritative grid.
- **"Operators (the node's own staff)"** — undefined role holding the *sole* Administrative grant besides
  break-glass: `MDL_External_Interfaces.md:47` "✓ (schema/role/ops)". The broadest privilege in the interface
  matrix rests on an actor doctrine never defines.
- **"External Authority"** — used as an *Owner* of truth (`MDL_Truth_Ownership_Matrix.md:38`, the Regulations
  row) though it is neither the domain nor one of the nine roles; it is silently equated with "Mandate
  Authoring Authority" (`Repository_Independence_Review.md:40`). A tenth, undefined owner-role.
- **The self-audit fails:** `Repository_Independence_Review.md:60` certifies the two matrices "**Clean** —
  Every cell names the domain or a role," which is the direct opposite of the evidence above.

**Effect:** the repository's central claim — *"roles bind; occupants illustrate; the domain stands alone"* —
is not actually enforced by its own matrices, and the audit designed to catch exactly this passes a failing
artifact. This is the highest-leverage structural defect in the repository.

### CR-3 — Constitutional contradiction: a mandate authored under invalid authority cannot be remedied (Revocation × Immutability)
**Trigger: constitutional contradiction + missing concept cluster.** The only lifecycle exits are
Supersede / Sunset / Retire, all forward-only and snapshot-preserving (`MDL_Lifecycle.md:51-53`,
"Retirement never invalidates snapshots already frozen against it"), and "mandates are never deleted"
(`:124-125`). Principle 4 forbids altering history (`MDL_Infrastructure_Constitution.md:253`). Yet the
evidentiary standard binds every determination to "a provenance to the authoring authority" (`:73-74`),
and §2 already declares self-granted authority "**void**" (`:120`). **There is no mechanism to propagate
the void-ness of an authority to the frozen determinations that rested on it.** A mandate later found to
have been authored *ultra vires* (by an authority that never held the right) leaves every prior
determination frozen as "valid," with no doctrinal remedy. Compounded by two absent, constitutionally
necessary concepts (see §3): **Delegation** (no way to represent that an author was authorized at a scope)
and **Authority Lineage** (attribution exists — `:174` — but not a chain proving the right to author).
Revocation-for-invalidity and snapshot-immutability collide with no reconciliation.

### CR-4 — Constitutional contradiction: the determinism invariant forbids what an anticipated capability requires
**Trigger: constitutional contradiction.** The invariant: "the resolution path contains no probabilistic or
model-driven step" (`MDL_Infrastructure_Constitution.md:67`); "No probabilistic or model-driven step exists
in the resolution or determination path … Determinism is a hard invariant" (`:213`); Constraint I1 "no model
in the resolution path" (`Architectural_Constraints.md:32`); Principle 7 "Authoritative, not advisory"
forbids advisory inputs (I6). Yet a Future capability, **Discipline-Determination Consumption**
(`MDL_Capability_Framework.md:60`; `MDL_Infrastructure_Constitution.md:142`), has a mandate's satisfaction
"require a peer discipline determination." That peer output is, per `EchoForge/echoforge/trust/contract.py`,
a "**machine assessment**, **not** … authority" (`:357-364`), carries a **heuristic** confidence (`:66-73`),
stamps a non-reproducible `datetime.utcnow()` (`:321`), and can return `requires_review` /
`insufficient_information` (`:90-95`). Consuming it injects a non-deterministic, advisory, self-labelled
non-authoritative input into a path the constitution declares deterministic and authoritative. The doctrine
flags the tension (Q5, `Open_Questions_and_Risks.md:121`) but does not resolve it while asserting the
capability as anticipated — an unresolved contradiction, not merely an open question.

### CR-5 — Inability to scale: "the one node / owned once, here" does not survive jurisdictional sovereignty
**Trigger: inability to scale + constitutional contradiction.** The strongest single-authority claims:
"the … **single authoritative Mandate Definition Layer**: **the one node**" (`Immutable_Core_Charter.md:14`);
"**One authoritative owner** — mandate resolution is owned once, here" (`:85`); Principle 1 "Every mandate
truth traces to **exactly one owner — this domain**" (`MDL_Infrastructure_Constitution.md:246-248`). The
federation escape-hatch — "federation multiplies **deployments**, never **authorities**"
(`MDL_Infrastructure_Roadmap.md:66`) — assumes all deployments defer to one logical authority. **Data-residency
and jurisdictional-sovereignty law** (data-localization regimes, tribal/foreign sovereignty) can legally
compel a *separate, in-jurisdiction, co-equal authoritative operator* that stores and resolves that
jurisdiction's mandates itself — multiple co-equal authorities, which Principle 1 and Charter §7.5 forbid.
The Charter asserts these guarantees "hold across a decade because each is defined by a relationship or
invariant, not by any named runtime" (`Immutable_Core_Charter.md:87-88`) — but sovereignty is exactly a
force that breaks a single-authority invariant, and **no clause contemplates jurisdiction-forced authority
partitioning.** At "hundreds of jurisdictions" this forces a constitutional amendment.

---

## 2. HIGH findings

### H-1 — Constitutional purity: function signatures in doctrine
`MDL_Consumption_Model.md:36-42` names exact signatures — `resolve_applicable_mandates(context)`,
`create_mandate_snapshots(entity)`, `validate_entity_against_mandates(entity)`, `resolve_tax_policy(entity)`,
`get_latest_validation_status(entity)` — repeated at `Migration_Strategy_CFRS_to_RBM_MDL.md:38,44`. This is
the exact thing the Capability Framework says to avoid: "A capability is a durable function … an API is a
perishable implementation detail" (`MDL_Capability_Framework.md:16`), and the Constitution claims to define
"no storage, API, schema" (`MDL_Infrastructure_Constitution.md:273`).

### H-2 — Constitutional purity: return-field / flag names in doctrine
`MDL_Consumption_Model.md:38-40` — `compliance_status`, `missing_documents`, `missing_evidence`,
`threshold_blocks`, `participation_blocks`, `is_tax_exempt`, `reason`, `mandate_id`, `mandate_version`. The
flag `tax_exempt_override` recurs in doctrine (`MDL_Truth_Ownership_Matrix.md:42`, `MDL_Capability_Framework.md:39`,
`MDL_Lifecycle.md:106` `tax_exempt_override=True`). JSON/field shapes are schema in a schema-free layer.

### H-3 — Constitutional purity: HTTP verbs + endpoint paths in doctrine
`MDL_Consumption_Model.md:44-45` — "`GET /mdl/mandates`, `GET /mdl/snapshots/{id}`,
`GET /mdl/validation-results/{entity}`"; `MDL_Ownership_Analysis.md:72` cites "`POST /echoforge/mdl/validate`".
Concrete REST surface in the "no API" constitutional layer.

### H-4 — Constitutional purity: database table names enumerated in doctrine
`Migration_Strategy_CFRS_to_RBM_MDL.md:39` enumerates "the 9 core tables: `mandates`, `mandate_applicability`,
…, `mandate_overrides`"; more at `Open_Questions_and_Risks.md:86-87`. This lives in a repo that states "There
is no `models/`, `migrations/`" (`MDL_Repository_Blueprint.md:111`). *(Migration is the least-bad home for
this — it is about lifting real tables — but the count/names still constitute schema in doctrine.)*

### H-5 — CFRS-specificity leaking into infrastructure doctrine
A node-agnostic constitution imports one vertical's concepts as primitives:
- The mandate object's rule sets include "**participation**" (MWBE) baked into the Constitution itself
  (`MDL_Infrastructure_Constitution.md:156`), and "**Participation Aggregation** … (e.g. **MWBE**/workforce)"
  as a named capability (`MDL_Capability_Framework.md:49`) — MWBE is a US-procurement-vertical concept.
- The CFRS vertical `NodeType` enum (FLEET, HOUSING, HUMAN_SERVICES, …) is treated as an infrastructure
  parameter (`Migration_Strategy_CFRS_to_RBM_MDL.md:43`, `MDL_Infrastructure_Roadmap.md:29`,
  `Open_Questions_and_Risks.md:69-70`) — contradicting "no named product … is ever hardwired"
  (`MDL_Consumer_Model.md:8`). Partly mitigated by A5's "NodeType is a resolution parameter" note, but the
  enum *values* remain CFRS's verticals.
- The roadmap adopts "**FLEET/NY**" as its Phase-1 identity (`MDL_Infrastructure_Roadmap.md:24`), coupling
  forward doctrine to one vertical + one US state.

### H-6 — Boundary leak into EchoForge: MDL doctrine defines the Governance Supervisor's escalation ladder
`MDL_External_Interfaces.md:55` and `MDL_Event_Model.md:85-86` enumerate "Soft Alert, Sentinel Alert,
Quarantine Mode, Repair Mode" as the Supervisor's escalation states. The Consumer Model grants the Supervisor
only "can quarantine" (`MDL_Consumer_Model.md:43`). The four-mode state machine is a *specific consumer's*
internal capability (EchoForge's); writing it into MDL's own interface/event doctrine makes a consumer's
internals load-bearing — the coupling the standing rule forbids (`MDL_Consumer_Model.md:26-29`). Remove
EchoForge and these clauses lose their referent.

### H-7 — Ten-year scaling: the fixed 7-level, US-centric jurisdiction stack cannot express the world
`MDL_Lifecycle.md:90` — "FEDERAL ▸ PRIME_CONTRACT ▸ STATE ▸ COUNTY ▸ MUNICIPAL ▸ PROGRAM ▸ INTERNAL." No
GLOBAL, INTERNATIONAL, SUPRANATIONAL (EU), TREATY, or TRIBAL layer; the terms are US-specific. The **peer
Trust Runtime already models what MDL lacks**: `EchoForge/echoforge/trust/contract.py:54-63` `JurisdictionLevel`
= `GLOBAL, INTERNATIONAL, FEDERAL, STATE, LOCAL, ORGANIZATIONAL, UNKNOWN`. Inserting an INTERNATIONAL tier
*above* FEDERAL re-orders precedence and, by the doctrine's own words, "silently changes every conflict
determination" (`MDL_Lifecycle.md:115`) — a constitutional change, contradicting Principle 10's promise that
growth "adds … jurisdiction layers rather than re-cutting boundaries" (`MDL_Infrastructure_Constitution.md:264`).
Aggravated by A1: the ordering is *already* unratified and inconsistent across the three source specs.

### H-8 — Ten-year scaling: never-delete immutability collides with storage economics and right-to-erasure
`Immutable_Core_Charter.md:78` "never mutated"; snapshots capture "entity attributes"
(`MDL_Infrastructure_Constitution.md:64`); "mandates are never deleted" (`MDL_Lifecycle.md:124`); "a
determination frozen in Era 1 must reproduce identically in Era 5" (`MDL_Infrastructure_Roadmap.md:64`). No
retention limit, tiering, tombstone, crypto-shred, or data-minimization concept exists — and the constitution
*pre-forbids* the relief: "**never trade snapshot immutability for storage elegance**"
(`Architectural_Constraints.md:45`). At millions of entities × per-event snapshots × forever, storage is
unbounded; and a GDPR/CCPA erasure request over frozen entity attributes **cannot be honored** without
breaking an immutable guarantee. Forces either an HRA exception or legal non-compliance.

### H-9 — Independence over-claim: the operational invariants are sourced from specs the node does not own
The constitution claims to depend "on no other repository, runtime, or assistant"
(`MDL_Infrastructure_Constitution.md:13`) and `.atlas-config.yaml:29` asserts `constitutional_dependencies:
[]`. Yet nearly every hard invariant in `Architectural_Constraints.md` §2 (I1–I10) cites the *uploaded MDL
Spec / Service Contract / Jurisdiction Stack* as its **source**, and `Open_Questions_and_Risks.md:118` (Q2)
admits their ownership is unresolved. The abstract authority/evidentiary model *is* internalized (§2, §1.4) —
so this is not full repo coupling — but the concrete invariants the node lives by change if those
externally-owned specs change. The independence claim is over-stated for the operational invariant set; the
Independence Review's four coupling classes (`Repository_Independence_Review.md:66-76`) have no
"named-document/spec-source coupling" class and are structurally blind to this.

### H-10 — Industry comparison omits the three closest ownership-model analogs, and two improvement-claims are false against them
`MDL_vs_Industry_Systems.md:25-35` and `IEF_Classification.md:32-36` compare OPA, Cedar, ServiceNow, Drools,
government/eligibility/workflow engines, and the Trust Runtime — but **omit Azure Policy, AWS IAM/Organizations,
and Stripe Connect**, which are the nearest *ownership-model* analogs (single authoritative evaluator +
scope-hierarchy inheritance + exemptions/deny-precedence + binding must-honor verdict + recorded compliance).
Consequently two claims are false as written: "most engines leave precedence to hand-written rules; MDL makes
it a **resolution primitive**" (`:68`) is untrue of Azure Policy (management-group inheritance) and AWS
Organizations (SCP inheritance, explicit-deny precedence); and "a financial override authoritative … a
cross-vertical supremacy most vertical rules engines cannot express" (`:73`) under-weights Stripe Connect,
whose compliance verdict binds platforms cross-merchant. The IEF's boast that comparables were surveyed and
a "new category … foreclosed" (`IEF_Classification.md:34`) surveyed the *farther* comparables; the residual
IAF novelty (AUTHOR/RESOLVE/ACT scored D1=3/D2=3, `IAF_Innovation_Assessment.md:59`) is over-scored once
IAM (admin authors / IAM resolves / service acts / CloudTrail observes) and Stripe (regulator authors /
Stripe resolves / platform acts) are admitted as structural analogs.

### H-11 — Terminology: "Consumes / Consumer" carries two incompatible meanings
Meaning A — "reads and acts on it" (`MDL_Truth_Ownership_Matrix.md:19`), under which the Supervisor *is* a
consumer (`:37`). Meaning B — an interface mode "**Consumes MDL** — sends entity context, receives a
determination" (`MDL_External_Interfaces.md:22`), under which the Supervisor is explicitly *denied* Consume
(`:41`). This is the single most load-bearing term in the repository (the entire model is "consumers as
roles"), and the overload produces the direct contradiction M-2 below.

---

## 3. MEDIUM findings

- **M-1 — "Override" overloaded** across (a) a *financial-override mandate rule* (`MDL_Capability_Framework.md:39`)
  and (b) a *dual-authorized runtime exception grant* (`MDL_Infrastructure_Constitution.md:138`). Two different
  truths, different authors, one word — invites owner-ambiguity in the very matrices meant to prevent it.
- **M-2 — Supervisor: "does not drive determinations / denied Consume" vs listed as a Consumer of truth.**
  `MDL_External_Interfaces.md:41` denies the Supervisor Consume; `MDL_Truth_Ownership_Matrix.md:37` lists
  "Supervisor" among consumers. Reconcilable only by noticing "Consume" means two things (H-11).
- **M-3 — "Retirement never invalidates snapshots" vs "expired effectivity → inadmissible/STALE."**
  `MDL_Lifecycle.md:52` says a snapshot frozen against a retired mandate stays valid; `MDL_Infrastructure_Constitution.md:91`
  says "no snapshot or **expired effectivity** is **inadmissible** — rendered as `UNRESOLVED`/`STALE`." The two
  point opposite directions for the same artifact and are never reconciled.
- **M-4 — MDL cannot self-enforce "authoritative, not advisory."** MDL "holds no value and performs no business
  action" (`Immutable_Core_Charter.md:41`), so it cannot block a bypass itself; the only named
  bypass-prevention is the Governance Supervisor intercepting (`MDL_External_Interfaces.md:63`). Principle 7's
  flagship "determinations bind consumers" (`MDL_Infrastructure_Constitution.md:258`) is therefore operationally
  dependent on a consumer/supervisor — in tension with "never a dependency the doctrine assumes into existence"
  (`MDL_Consumer_Model.md:16`).
- **M-5 — IEF/IAF frameworks are externally owned and were reconstructed from a *peer* repo.**
  `IEF_Classification.md:8-11` / `IAF_Innovation_Assessment.md:6-10` — the reusable frameworks are "owned by the
  ecosystem home … not present in this workspace," and the classification "reconstructs the rubric" from
  `RBM-Economic-Core`'s reference. Applying an externally-owned, cross-repo-reconstructed framework is a real
  methodological dependency (disclosed, but it qualifies the independence claim).
- **M-6 — "Enforcement" sequences the node's tax-engine stack and declares the arithmetic outcome.**
  `MDL_Lifecycle.md:105-106` sequences "Vendor Profile ▸ Auto Tax Engine" and states "tax is zero," while the
  Charter says MDL "does not book invoices" (`Immutable_Core_Charter.md:42`). Defensible under the
  determination/booking split (hence MEDIUM, not a proven Economic-Core leak — see §4-B) but it edges into the
  Economic Consumer's execution truth.
- **M-7 — Tie-break bottleneck at scale.** Same-level, same-`effective_date` conflicts have *no* deterministic
  final resolution; the rule is "flag the conflict for review — it must not auto-resolve"
  (`MDL_Lifecycle.md:100-103`; invariant I4). At millions of mandates this makes human review a scaling
  bottleneck, and Principle 3 "Deterministic by construction" is incomplete — the system deterministically
  produces `UNRESOLVED` but does not deterministically *resolve*.
- **M-8 — Eligibility cell has two owners and is self-disclosed as unresolved.** `MDL_Truth_Ownership_Matrix.md:43`
  splits a single cell — MDL owns "eligibility determination," Business-Node owns "grant/deny decision" — while
  `Open_Questions_and_Risks.md:120` (Q4) admits the line is unresolved. The matrix asserts as settled what the
  risk ledger flags as open.
- **M-9 — Registration fields + event enum names in doctrine.** `node_id`/`node_type`/`jurisdiction_scope`
  (`MDL_External_Interfaces.md:69`) and the `MANDATE_*`/`SNAPSHOT_*`/`OVERRIDE_*`/`NON_COMPLIANT` wire enums
  (`MDL_Event_Model.md:36-52,84`) are named implementation detail (softened only by being "adopted from the
  Service Contract").

---

## 4. LOW findings

- **L-1 — Undefined minor terms in binding tables:** "decision-role consumer" (`MDL_Capability_Framework.md:92`),
  "Tax Authorities" (`MDL_Responsibility_Matrix.md:45`), "Regulated providers" (`MDL_Capability_Framework.md:69`)
  — named actors with no role definition.
- **L-2 — CFRS 9-vs-13 table-count drift** lives in doctrine (`Open_Questions_and_Risks.md:85-90`) — a migration
  detail, not constitutional matter.
- **L-3 — "Validation" / "Satisfaction Determination" / "Determination" used interchangeably**
  (`MDL_Capability_Framework.md:37`, `MDL_Internal_Architecture.md:38`, `MDL_Truth_Ownership_Matrix.md:44`) —
  the drift that seeds the CR-1 duplicate.
- **L-4 — No `MANDATE_ACTIVATED` event** fires when an effective date is crossed (`MDL_Event_Model.md:36-52`);
  consumers must poll effectivity. Nice-to-have.
- **L-5 — Knowledge-horizon inconsistency:** `MDL_vs_Industry_Systems.md:9` cites "2026" while
  `IEF_Classification.md` reasons at "2024–2025."
- **L-6 — "financial policy" vs "financial override" vs the mandate "financial policy" rule set** drift toward
  each other (`MDL_Capability_Framework.md:39`, `MDL_Infrastructure_Constitution.md:157`).

---

## 5. Mandated investigations

### 5.1 Boundary Integrity — can MDL be proven to own something belonging to another node?

| Against | Verdict | Evidence |
|---|---|---|
| **Economic Core** | **No ownership leak proven** (one MEDIUM edge). MDL owns the *override determination*; Economic Core *books* it — consistent across all three MDL docs and with Economic Core's own "does not Define tax law … Exempt the ecosystem" (`RBM-Economic-Core/Economic_Truth_And_External_Authority.md:82-88`). The only edge is M-6 (MDL sequencing the tax-engine stack + "tax is zero"). MDL does **not** claim tax *amounts*. | `MDL_Truth_Ownership_Matrix.md:89-94`; `MDL_Lifecycle.md:105-106` |
| **EchoForge** | **Leak proven (H-6):** MDL doctrine defines EchoForge's Soft/Sentinel/Quarantine/Repair escalation ladder — reaching into the Supervisor's own authority. | `MDL_External_Interfaces.md:55`; `MDL_Event_Model.md:85-86` |
| **LEAL** | **No leak.** LEAL appears only as the Doctrine-Governance Consumer role; MDL claims no doctrine-governance authority. If anything the role is *thin* (LEAL barely interacts with MDL) — over-modeled, not leaked. | `MDL_Consumer_Model.md:44` |
| **Business Nodes** | **No ownership leak**, one fuzzy boundary (M-8, the eligibility grant/deny cell). MDL determines; the node acts. | `MDL_Truth_Ownership_Matrix.md:43` |
| **Trust Runtime** | **No ownership leak; no cycle** (§4-B). But the *determinism-vs-consumption* contradiction (CR-4) lives at this seam. | `EchoForge/echoforge/trust/contract.py:11-13,357-364` |
| **Asset Domain (RESA)** | **No leak found.** No MDL document claims asset/token/custody truth; the Asset Domain is absent from every matrix, correctly. | (absence across `MDL_*` matrices) |
| **PERSE** | **No leak.** PERSE appears only as an example Business-Node Consumer occupant. | `MDL_Consumer_Model.md:44` |
| **Executive Runtime** | **No *ownership* leak, but a phantom-actor defect (CR-2):** the grids invoke an "Executive/Operational" consumer that the role model never defines. | `MDL_Truth_Ownership_Matrix.md:47`; `MDL_Responsibility_Matrix.md:49` |

**Where leakage could not be proven, it is stated so:** Economic Core (tax amounts), Asset Domain, PERSE,
LEAL, and the MDL→Trust direction are clean on ownership.

### 5.2 Missing Concepts — present? necessary?

| Concept | Present? | Verdict |
|---|---|---|
| **Publication** | Yes — `MDL_Lifecycle.md:49` stage 6. | Adequate. |
| **Activation** | As effectivity — `MDL_Lifecycle.md:49` ("publication ≠ effectivity"). | Adequate; only missing an activation *event* (L-4). Not necessary. |
| **Revocation** (distinct from retire/sunset) | **No** — only `OVERRIDE_REVOKED` (an override, not a mandate). | **Constitutionally necessary (CR-3).** No void-ab-initio for an invalidly-authored mandate; collides with immutability. |
| **Delegation** (of authoring authority) | **No** — zero occurrences; Q7 leaves PROGRAM/INTERNAL authorship unresolved. | **Constitutionally necessary.** Precondition for detecting ultra-vires authoring. |
| **Composition** (mandate→mandate) | No (only Era-4 discipline sense). | Not necessary at foundation; inheritance covers layered accumulation. |
| **Inheritance** | Yes — FLOOR/ADDITIVE/OVERRIDE (`MDL_Lifecycle.md:93-96`). | Adequate. |
| **Entitlement** | No (subsumed by Eligibility + node grant/deny). | Not necessary as distinct. |
| **Temporal validity** | Yes — effectivity windows + freshness anchor (`MDL_Infrastructure_Constitution.md:171,90`). | Strong. |
| **Scope** | Yes — jurisdiction/node/entity/service applicability + `jurisdiction_scope`. | Strong. |
| **Authority lineage** | **Partial** — attribution present (`MDL_Infrastructure_Constitution.md:174`), chain-of-authority absent. | **The missing half is necessary.** Attribution records *which* authority, not *whether it held the right*. |

**Headline gap:** REVOCATION + DELEGATION + AUTHORITY-LINEAGE form one interlocking, constitutionally
necessary cluster (delegation+lineage make invalid authoring *detectable*; revocation makes it *remediable*;
remediation collides with immutability). This is the most serious substantive doctrinal gap.

### 5.3 Repository Independence — can it survive if every other RBM repository disappeared?

**Constitutional independence: TRUE.** Remove CFRS, EchoForge, LEAL, Economic Core, Atlas, RESA — every
clause still stands, because each is a removable role-occupant; the ten-year replacement test passes
(`Repository_Independence_Review.md:79-92`; `MDL_Consumer_Model.md:22-24`). No repo-to-runtime coupling
survives adversarial removal.

**Operational independence: FALSE, and more strongly than disclosed.** The node's core capability (Mandate
Registry) is not merely useless without consumers — it is **un-populatable without external Mandate Authoring
Authorities**: with zero authors there are zero source obligations to compile, so nothing to resolve
(`MDL_Capability_Framework.md:33`; `IEF_Classification.md:51`). The node's *invariants* also lean on the three
externally-owned uploaded specs (H-9). So: the **constitution** stands alone; the **functioning node** and its
**operational invariant set** do not. This is acceptable for an infrastructure node (a road needs traffic),
but the doctrine's blanket "depends on no other repository" and `constitutional_dependencies: []` over-state
it and should be qualified.

### 5.4 Ten-Year Test — where scaling forces a constitutional change

| Pressure | Clause that breaks | Severity |
|---|---|---|
| Data-residency / sovereignty | Single-owner "the one node" (Principle 1) — forces authority partitioning | CRITICAL (CR-5) |
| International/tribal/supranational law | Fixed US-centric 7-level stack; adding a top tier re-cuts precedence (vs Principle 10) | HIGH (H-7) |
| Millions of snapshots, forever; erasure law | Never-delete immutability; relief pre-forbidden | HIGH (H-8) |
| Millions of same-level conflicts | "Never auto-resolve" → human-review bottleneck | MEDIUM (M-7) |
| A wrong mandate discovered years later | No revocation/void-ab-initio | CRITICAL (CR-3) |

Every row above requires amending an *immutable guarantee* or a *principle* — i.e. a constitutional change,
which the constitution promises should not be needed as it scales. That promise does not hold in five places.

### 5.5 Industry Comparison — ownership models

| System | Owns the truth | Authority | Scope/inheritance | Immutable record | Must-honor verdict |
|---|---|---|---|---|---|
| OPA/Rego | per-bundle deployers | decentralized | packages, no inheritance | optional decision logs | only if the PEP enforces |
| **AWS IAM/Organizations** | AWS owns semantics; admins author | **single evaluator** | **Org→OU→account; SCP inheritance; explicit-deny precedence** | CloudTrail (not pinned) | **yes — denied at API** |
| **Azure Policy** | Azure evaluates; admins author | **single evaluator** | **mgmt-group→subscription→RG inheritance + exemptions** | compliance state | **yes — `deny` blocks** |
| K8s Admission Controllers | per-cluster; admins author | single per cluster | match/scope selectors | audit logs | **yes — request rejected** |
| **Stripe Connect** | **Stripe owns the verdict** | **single authority** | per-account/country scope | requirement/capability state | **yes — payouts disabled until met** |
| Epic policy engines | health system | single per org | care-setting scope | in-chart | workflow-binding |
| ServiceNow GRC | org | single platform | policy→control→attestation | attestation records | workflow-binding |

**Closest ownership-model analogs:** **Azure Policy** (scope hierarchy + inheritance + exemptions + deny +
recorded compliance) maps almost one-to-one onto MDL's *jurisdiction stack + inheritance + override + snapshot
+ determination*; **AWS IAM/Organizations** (hierarchical inheritance, deny-precedence, single evaluator);
**Stripe Connect** (single-authority binding compliance verdict consumers must honor — the truest analog to
MDL's "authoritative, not advisory"). **These three are absent from MDL's own comparison (H-10),** which
weakens both the IEF "comparables surveyed" claim and the IAF novelty score. MDL's genuine differentiators
that survive the fuller comparison: (a) *jurisdiction* as the scope axis (vs org/cloud/account) with declared
FLOOR/ADDITIVE/OVERRIDE inheritance semantics, and (b) the *version-pinned determination snapshot* as the
first-class audit artifact (Azure/IAM/Stripe record compliance *state*, not an immutable version-pinned
determination). The AUTHOR/RESOLVE/ACT partition itself is **not** novel against IAM/Stripe and is over-scored.

### 5.6 Constitutional Purity — implementation leaks

The root layer is declared "immutable and implementation-free" (`MDL_Repository_Blueprint.md:14`) and the
Constitution "defines no storage, API, schema" (`MDL_Infrastructure_Constitution.md:273`). Leaks found:
function signatures (H-1), field/flag names incl. `tax_exempt_override` (H-2), HTTP verbs + endpoint paths
(H-3), DB table names (H-4), registration fields + event enums (M-9). **Assessment:** these were introduced
deliberately to stay consistent with the uploaded operational specs — a reasonable *intent*, wrong *layer*.
The doctrine should speak of "resolve the applicable mandate set" (a capability), not
`resolve_applicable_mandates(context)` (a signature); of "a binding tax-exemption determination" (a truth),
not `tax_exempt_override=True` (a flag). The operational specs are the correct home for those names.

### 5.7 Terminology Consistency

| Term | Status |
|---|---|
| **Consumer / Consumes** | **Drift (H-11):** "any reader" vs "a request mode" — produces M-2. |
| **Override** | **Drift (M-1):** financial-override rule vs runtime exception grant. |
| **Enforcement / enforces** | **Drift:** three acts (determine / gate / oversee), yet used as one owned-truth label though MDL is "not an executor" — the doctrine even documents the overload (A4) but keeps it. |
| **Validation / Determination / Satisfaction Determination** | **Drift (L-3):** three terms, one concept — seeds CR-1. |
| **Mandate / Rule / Policy / Obligation / Requirement** | **Largely disciplined** — "source obligation" (authored) vs "mandate" (encoded) vs "rule set" (contents) held apart; minor "financial policy" drift (L-6). No synonym collapse proven. |
| **Snapshot / Version / Jurisdiction / Authority / Ownership / Resolution / Compliance** | Consistent. No drift proven. |

---

## 6. Suspected defects that did NOT hold (stated for honesty)

An adversarial audit that only reports hits is not credible. The following were tested and **cleared**:
- **No circular ownership / dependency.** MDL→Trust→MDL does not exist — the Trust Runtime's consumer list
  excludes MDL and a full-tree grep of `EchoForge/echoforge/trust/` finds zero mandate references
  (`contract.py:11-13`). The "supervised-by + exposes-endpoints-to" relationship is one-way Supervisor→MDL, not
  a cycle (the residual is the *enforcement* dependency M-4, not a cycle).
- **No Economic Core reverse dependency; the financial-override boundary is consistent** across all three MDL
  docs and with Economic Core's own doctrine (A6 holds). MDL does not claim tax *amounts*.
- **No named-runtime clause coupling** — every named system is a removable role-occupant; the ten-year test
  passes.
- **Financial-override owner is consistent** across Constitution §3, Truth Matrix, and Responsibility Matrix —
  not a duplicate-truth (unlike CR-1's Validation/Enforcement).
- **"M110" document code** and other CFRS artifacts suspected of leaking are **not present**.
- **Mandate/Rule/Policy/Obligation** are largely kept distinct; no synonym collapse proven.
- **The Governance Supervisor is never actually granted determination-driving Consume** — the only residue is
  the terminology overload (H-11), not a real authority grant.

---

## 7. Closing assessment

The RBM MDL Layer's constitutional *strategy* is sound and its independence-as-doctrine is real — it passes
the tests it was built to pass (runtime replacement, no ownership cycle, no repo coupling in the abstract).
It fails a different, harder set of tests it did not anticipate: its own authoritative grids reference actors
its role model never defines (and its self-audit certifies them clean anyway); its immutable guarantees have
no answer for invalid-authority revocation, for jurisdictional sovereignty, or for data-erasure law; its
determinism invariant contradicts a capability it plans to add; and it lets implementation detail and one
vertical's vocabulary leak into a layer it declares implementation-free and node-agnostic.

None of the five CRITICALs is fatal to the *approach* — each is a specific, locatable defect with a bounded
resolution (define the missing roles or delete the phantom ones; add revocation/delegation/lineage and
reconcile them with immutability; scope the determinism invariant or forbid consuming non-deterministic
inputs; state the single-authority rule as "one owner per jurisdiction-scope" and add sovereignty
partitioning; move signatures/tables/flags to the operational specs). But until they are resolved, the
constitution does not yet hold together under adversarial reading, and **implementation should not begin.**
The doctrine's own `Open_Questions_and_Risks.md` already anticipated A1 (jurisdiction ordering), Q4
(eligibility), Q5 (discipline determinism), and Q7 (authorship scope) — this audit's contribution is the
defects it did not: CR-1, CR-2, CR-3, CR-5, H-6, H-9, H-10, and the revocation/delegation/lineage cluster.
