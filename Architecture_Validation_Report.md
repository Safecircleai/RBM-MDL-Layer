# Architecture Validation Report — RBM MDL Layer

**Purpose:** answer one question — *can the MDL be built exactly as described, without violating its own
constitution?* This is a buildability validation of every **Core** capability
(`MDL_Capability_Framework.md` §1), the dependency graph among them, and the smallest implementation order
that yields a functioning MDL. **No code, no APIs, no schemas** — inputs and outputs are described as
*things*, not signatures. This report writes no new doctrine; where a capability cannot be built as written,
it is reported, not fixed.

**Relationship to the audit:** `Architecture_Audit_Report.md` found five CRITICAL defects. Two of them are
**hard build-blockers** surfaced again here at the capability level (the unratified jurisdiction stack; the
undefined authoring/ops roles). The other three affect *future* capabilities or *matrix labeling*, not the
buildable Core set — this validation says so precisely where each bears on a capability.

---

## 0. Headline verdict

**The Core architecture is buildable.** The eleven Core capabilities form a **clean directed acyclic graph**
— no cycles, no impossible ordering, and (at the capability layer) **no duplicated truth and no duplicated
authority**. Every Core capability can exist without violating an invariant, with two exceptions that are
**blocked pending ratification, not broken**:

1. **Jurisdiction Resolution cannot be built deterministically until the canonical jurisdiction stack is
   ratified** (audit A1/CR-5). Determinism (I1) is impossible over an undecided precedence order.
2. **Authoring & Governance Workflow and the Consumption Interface cannot have their access rules fully
   specified until the authoring/ops roles are defined** (audit CR-2 — "Operators"/"ops-admin" are used but
   undefined in the Consumer Model).

Everything else builds. Two further items (revocation-vs-immutability, discipline-determination determinism)
are **unresolved architectural questions that do not block the minimal Core build** because they live in a
*future* capability and a *remediation* path, not on the critical path to a first determination.

---

## 1. Per-capability validation (the eleven Core capabilities)

Each record answers the required fields. Inputs/outputs are conceptual. "Owning layer" refers to
`MDL_Internal_Architecture.md`; "lifecycle stage" to `MDL_Lifecycle.md` (Definition vs Application).
Verdict ∈ {**Buildable**, **Buildable-after-ratification**, **Buildable-with-caveat**}.

---

### C1 — Mandate Registry  · Verdict: **Buildable**
- **Purpose:** be the single authoritative store of encoded, versioned mandates and their rule sets.
- **Constitutional owner / authority:** MDL domain (owns the encoding; the *source* is authored elsewhere).
- **Owning layer:** Registry (layer 1). **Lifecycle stage:** Definition (Encode → store).
- **Consumed by:** Jurisdiction, Resolution, Distribution, Authoring, Auditors, Governance Supervisor (read).
- **Inputs:** an encoded mandate (jurisdiction layer, applicability, rule sets, effectivity, authoring-authority attribution) handed over by the Authoring workflow.
- **Produces / outputs:** the durable, retrievable set of mandate definitions by identity + version.
- **Requires (dependencies):** nothing else to exist first (foundational). Requires the Audit trail to record each write.
- **External dependencies:** none to *exist*; the *content* originates from external Mandate Authoring Authorities via Authoring.
- **Persistence:** durable, authoritative store; retains all versions (never deletes).
- **Deterministic requirement:** storage/retrieval is deterministic by identity+version; no compute on the deterministic path here.
- **Prohibited from:** holding a second competing mandate store; authoring any source obligation.
- **Implementation risks:** low. Standard versioned record store; the discipline is refusing in-place edits of a version.
- **Unresolved questions:** the CFRS 9-vs-13 table shape (audit L-2) is a migration-mapping question, not a Registry-existence question.

### C2 — Versioning & Effectivity  · Verdict: **Buildable**
- **Purpose:** manage version chains, supersession links, and effective/sunset windows; guarantee a new version never mutates a prior version's behavior.
- **Owner / authority:** MDL domain. **Owning layer:** Versioning (layer 3). **Lifecycle:** Definition (Version → Publish; Supersede/Sunset).
- **Consumed by:** Jurisdiction, Resolution (to select the in-force version), Snapshot (to pin a version).
- **Inputs:** a mandate and a new-version request; an effectivity window.
- **Produces:** version chains with supersession pointers; the in-force version for a given date.
- **Requires:** Registry.
- **External dependencies:** none.
- **Persistence:** durable (version chains, effectivity), append-preferring (old versions retained immutably).
- **Deterministic requirement:** "which version is in force at date D" must be a pure function of (chain, D).
- **Prohibited from:** mutating a prior version's behavior; deleting a version (would break snapshot references).
- **Implementation risks:** low–medium — the immutability-per-version discipline must be enforced at write time, not by convention.
- **Unresolved questions:** none material.

### C3 — Jurisdiction Resolution  · Verdict: **Buildable-after-ratification (BLOCKER)**
- **Purpose:** apply the precedence stack + declared inheritance behaviors (FLOOR/ADDITIVE/OVERRIDE) to order and reconcile mandates across layers.
- **Owner / authority:** MDL domain. **Owning layer:** Jurisdiction (layer 2). **Lifecycle:** Application (part of Resolve).
- **Consumed by:** Applicability Resolution (uses precedence to reconcile the candidate set).
- **Inputs:** a candidate set of in-force mandates, each tagged with a jurisdiction layer + inheritance behavior; the ratified precedence stack.
- **Produces:** a precedence-ordered, conflict-reconciled ordering; or a flagged unresolved conflict.
- **Requires:** Registry + Versioning; **and the ratified canonical precedence stack**.
- **External dependencies:** none (the stack is internal ratified doctrine).
- **Persistence:** the precedence stack itself (near-immutable config-as-doctrine); the capability is otherwise stateless compute.
- **Deterministic requirement:** hard — identical candidate set + stack → identical ordering; same-level ambiguity yields a deterministic *`UNRESOLVED`*, never an ad-hoc pick.
- **Prohibited from:** ad-hoc conflict resolution; auto-resolving a same-level, equal-date ambiguity.
- **Implementation risks:** **Cannot be built deterministically until the stack is ratified** — the three source specs disagree on ordering (audit A1), and a wrong order silently changes every conflict determination. Also: the fixed 7-level US-centric stack has no international/tribal tier (audit H-7) — buildable today, but the value set will need constitutional extension at scale.
- **Unresolved questions:** (1) the canonical ordering (audit A1/Q1) — **must be resolved before build**; (2) the deterministic tie-break for same-level, same-date conflicts is *by design* human review (audit M-7) — buildable, but the Conflict-Review Queue is a human-throughput dependency, not a deterministic resolver.

### C4 — Applicability Resolution  · Verdict: **Buildable** (composite of C1–C3)
- **Purpose:** deterministically return the mandate set applicable to an entity context.
- **Owner / authority:** MDL domain. **Owning layer:** Resolution (layer 4). **Lifecycle:** Application (Resolve).
- **Consumed by:** Satisfaction Determination, Financial-Override Determination, Business-Node consumers (read).
- **Inputs:** an entity context — node type, entity type, optional service type, jurisdiction, effective date, entity attributes — supplied by the calling consumer.
- **Produces:** the applicable, in-force, precedence-ordered mandate set for that context.
- **Requires:** Registry + Versioning + Jurisdiction.
- **External dependencies:** the entity context is supplied by the consuming node (an input, not a build dependency).
- **Persistence:** none — stateless compute over the persisted registry.
- **Deterministic requirement:** hard — identical context → identical set (the load-bearing determinism guarantee).
- **Prohibited from:** any random or environment-dependent step; any model in the path.
- **Implementation risks:** low, *given* C3 is ratified. The determinism guarantee is only as sound as its inputs — a consumer supplying stale entity attributes gets a deterministic-but-wrong result (input integrity is the consumer's, not MDL's; worth stating in the consumption contract).
- **Unresolved questions:** inherits C3's stack-ratification blocker.

### C5 — Satisfaction Determination (Validation)  · Verdict: **Buildable**
- **Purpose:** evaluate an entity's state against the resolved mandate set → the authoritative compliance result (status + per-rule gaps).
- **Owner / authority:** MDL domain. **Owning layer:** Determination/Evaluation (layer 5). **Lifecycle:** Application (Determine).
- **Consumed by:** Business-Node (gates on it), Economic Consumer, Snapshot (freezes it), Auditors.
- **Inputs:** the resolved mandate set (from C4) + the entity's current state.
- **Produces:** an authoritative, binding compliance determination — compliant / not / block-conditions, with the gaps that drove it.
- **Requires:** Applicability Resolution (C4); pairs with Financial-Override Determination (C7).
- **External dependencies:** entity state from the consuming node. **Core Determination requires no external discipline determination** — that is a *Future* capability (see note).
- **Persistence:** none — stateless compute; its *result* is persisted by Snapshot (C6), not by this capability.
- **Deterministic requirement:** hard — model-free; identical (resolved set, entity state) → identical result.
- **Prohibited from:** emitting an advisory-only result a consumer may ignore; performing discipline-specific legal reasoning.
- **Implementation risks:** low for the Core determination. **Note (audit CR-4):** the *Future* "Discipline-Determination Consumption" capability would inject a non-deterministic peer output into this path — that contradiction is confined to the future capability and does **not** affect the Core Determination's buildability. Core is clean.
- **Unresolved questions:** the "Enforcement" truth-row (audit CR-1) is a *matrix-labeling* redundancy of *this* capability; at the capability layer there is no separate "Enforcement" capability to build, so the buildable set is non-redundant (see §2).

### C6 — Snapshot & Immutability  · Verdict: **Buildable-with-caveat**
- **Purpose:** freeze the resolved configuration + result as an immutable audit artifact; bind results to snapshots, not to live records.
- **Owner / authority:** MDL domain. **Owning layer:** Snapshot (layer 6). **Lifecycle:** Application (Snapshot).
- **Consumed by:** Override (snapshot-bound), Auditors, Business-Node (status retrieval), Distribution.
- **Inputs:** the resolved configuration (C4) + the determination result (C5) + the versions relied upon; a governing-event identity (for idempotency).
- **Produces:** an immutable, version-pinned snapshot; a stable reference other capabilities point to.
- **Requires:** Determination (C5) and Resolution (C4).
- **External dependencies:** none.
- **Persistence:** durable, append-only, immutable, retained indefinitely — the **heaviest persistence** in the system.
- **Deterministic requirement:** freezing is deterministic given its inputs; idempotent per governing event.
- **Prohibited from:** mutating a snapshot; letting a result reference a live mandate record.
- **Implementation risks:** **medium–high at scale** — unbounded, never-delete growth with entity attributes frozen inside (audit H-8), and no data-minimization/erasure path, which collides with right-to-erasure law. Buildable now; a retention/erasure reconciliation is a known future constitutional pressure.
- **Unresolved questions:** **revocation-vs-immutability (audit CR-3)** — if a mandate is later found authored under invalid authority, there is no defined path to mark snapshots frozen against it as inadmissible. This does **not** block building the snapshot store; it means the *remediation* semantics are undefined. Flagged, not resolved.

### C7 — Financial-Override Determination  · Verdict: **Buildable**
- **Purpose:** resolve the binding financial policy (e.g. a tax-exemption override) that overrides a consuming node's tax computation.
- **Owner / authority:** MDL domain (owns the *determination*; the Economic Consumer books the effect).
- **Owning layer:** Determination/Evaluation (layer 5). **Lifecycle:** Application (Determine).
- **Consumed by:** Economic Consumer (books zero tax), Business-Node.
- **Inputs:** the resolved mandate set (C4) and its financial-policy rules; the financial-precedence order.
- **Produces:** a binding financial-override outcome (e.g. "exempt / not-exempt", with the mandate + version that decided it).
- **Requires:** Applicability Resolution (C4); computed within the Determination pass (alongside C5).
- **External dependencies:** none (computed from mandates).
- **Persistence:** none — its outcome is carried in the snapshot (C6).
- **Deterministic requirement:** hard — a pure function of the resolved financial rules + precedence.
- **Prohibited from:** booking the economic effect, computing tax *amounts*, or moving money (that is the Economic Consumer's execution truth).
- **Implementation risks:** low. Boundary caveat (audit M-6): the doctrine sequences a node's tax-engine stack and states "tax is zero" — the *build* must stop at the override outcome and not compute the amount.
- **Unresolved questions:** none material; the Economic-Core boundary is consistent (audit A6 holds).

### C8 — Override / Exception Evaluation  · Verdict: **Buildable-with-caveat**
- **Purpose:** evaluate dual-authorized, expiring overrides that modify a runtime outcome without mutating the snapshot.
- **Owner / authority:** MDL domain (evaluates at runtime); the grant is authored by a requestor + approver.
- **Owning layer:** Override (layer 7). **Lifecycle:** Application (Override).
- **Consumed by:** Business-Node (honors the runtime outcome), Governance Supervisor (override-frequency monitoring), Auditors.
- **Inputs:** an override grant (bound to a snapshot reference, with requestor, approver, expiry, reason) + the current time.
- **Produces:** a runtime-effective outcome (the determination as modified by any in-force override).
- **Requires:** Snapshot (C6), Determination (C5), Audit (C9).
- **External dependencies:** none.
- **Persistence:** durable (override grants, approvals, expiries, revocations).
- **Deterministic requirement:** deterministic *given (grant, evaluation-instant)* — **time-dependent**: an override's effectiveness is evaluated against the current clock (expiry), so "identical context → identical result" holds only for a fixed instant. The **snapshot stays immutable**; only the *runtime outcome* varies with time. This is acceptable and consistent, but it must be stated: overrides introduce controlled time-dependence into the *outcome*, never into the *snapshot*.
- **Prohibited from:** mutating the snapshot; applying an override without approval, expiry, and reason.
- **Implementation risks:** low–medium — dual-authorization and expiry-at-evaluation are straightforward; the discipline is never persisting override effectiveness as a stored flag (it is always re-evaluated).
- **Unresolved questions:** the override runtime clock is the only sanctioned time-dependence in the determination stack — confirm no other capability reads wall-clock into truth.

### C9 — Mandate Audit Trail  · Verdict: **Buildable** (foundational)
- **Purpose:** append-only, immutable record of mandate mutations, determinations, and override approvals.
- **Owner / authority:** MDL domain. **Owning layer:** Audit (layer 9). **Lifecycle:** both (records every stage).
- **Consumed by:** Auditors, Governance Supervisor, Intelligence (aggregate).
- **Inputs:** audit events from every mutating capability (Registry writes, versioning, determinations, snapshots, overrides).
- **Produces:** the immutable, queryable trail.
- **Requires:** nothing to *exist* (it is a foundational sink); every mutating capability requires *it*.
- **External dependencies:** none.
- **Persistence:** durable, append-only, immutable.
- **Deterministic requirement:** append is order-preserving; not on the determination path.
- **Prohibited from:** editing or deleting an entry; exposing out-of-scope PII.
- **Implementation risks:** low; shares the never-delete storage-growth pressure with Snapshot (audit H-8).
- **Unresolved questions:** retention at decade scale (shared with C6).

### C10 — Authoring & Governance Workflow  · Verdict: **Buildable-after-ratification (BLOCKER)**
- **Purpose:** the role-based Intake → Encode → Review → Approve → Version workflow that turns an authored obligation into a stored mandate.
- **Owner / authority:** MDL domain governs the *workflow*; the Mandate Authoring Authority authors the *source*.
- **Owning layer:** Governance/Authoring (layer 10). **Lifecycle:** Definition (Intake → Version).
- **Consumed by:** Mandate Authoring Authorities, ops/authoring roles; writes to Registry (C1) and Audit (C9).
- **Inputs:** an authored source obligation with provenance; approvals from the appropriate roles.
- **Produces:** an approved, versioned mandate handed to the Registry.
- **Requires:** Registry (C1) + Audit (C9); **and defined authoring/ops roles**.
- **External dependencies:** the Mandate Authoring Authority supplies the source obligation — the one Core capability that is **un-populatable without an external author** (the registry stays empty otherwise; audit independence point).
- **Persistence:** durable (in-flight drafts, approval state).
- **Deterministic requirement:** off the determination path (human-in-the-loop); need not be deterministic.
- **Prohibited from:** authoring a source obligation itself; permitting a non-authoring role to write a mandate.
- **Implementation risks:** **its RBAC cannot be specified until the roles it references ("ops role", "ops-admin", "Operators") are defined** (audit CR-2) — those actors appear in doctrine but not in the Consumer Model.
- **Unresolved questions:** who may author at PROGRAM/INTERNAL layers (audit Q7); and delegation/authority-lineage (audit CR-3 cluster) — needed to check an author was *authorized*, currently absent. The workflow builds without them, but cannot *verify authoring authority* until they exist.

### C11 — Consumption Interface & Propagation  · Verdict: **Buildable-with-caveat**
- **Purpose:** the request entry points consumers call, and the event stream / scoped propagation they subscribe to.
- **Owner / authority:** MDL domain (sole publisher of mandate-domain events). **Owning layer:** Interface (layer 11) + Distribution (layer 8). **Lifecycle:** Application (Resolve request; Propagate).
- **Consumed by:** all consumer roles, each at its least-privilege projection; the Governance Supervisor over the read-only boundary.
- **Inputs (request face):** an entity context or a read request. **Inputs (propagation face):** internal mandate/determination events.
- **Produces:** determinations/reads back to consumers; scoped propagation events to subscribers.
- **Requires:** the capabilities it fronts — Resolution (C4), Determination (C5), Snapshot (C6), Override (C8), Registry read (C1); the propagation face requires the producers whose events it forwards.
- **External dependencies:** the consumers/subscribers themselves (they receive, they are not build prerequisites).
- **Persistence:** durable subscriptions/registrations; a reliable-delivery event log/outbox; the request face is stateless.
- **Deterministic requirement:** the *request* face returns the deterministic determination; the *propagation* face is asynchronous (delivery timing is not truth).
- **Prohibited from:** granting any consumer more than its least-privilege projection; letting a consumer emit mandate-domain events; giving the Governance Supervisor write access.
- **Implementation risks:** medium — least-privilege projections and the read-only supervision boundary must be enforced structurally. The Supervisor's escalation ladder (Soft/Sentinel/Quarantine/Repair) is EchoForge's, not MDL's (audit H-6) — MDL builds the read-only endpoints + events; it must **not** implement the escalation state machine.
- **Unresolved questions:** the "Operators" admin projection is undefined (audit CR-2); the same role gap as C10.

---

## 2. The dependency graph

### 2.1 Request / data-flow order (as posed)

The linear chain in the brief is the **runtime request pipeline** (matches `MDL_Internal_Architecture.md` §2):

```
Registry → Jurisdiction → Resolution → Determination → Snapshot → Override → Distribution → Audit
  (C1)        (C3)          (C4)          (C5,C7)        (C6)       (C8)        (C11-prop)   (C9)
```

Notes on the mapping: **Versioning (C2)** feeds Jurisdiction and Resolution (an in-line dependency, not a
pipeline stage); **Authoring (C10)** is the *write path* that populates the Registry *before* any request
runs; **Consumption Interface (C11-request)** is the front door the pipeline enters through; **Audit (C9)**
is a side-effect sink written at every stage (shown last because it records the completed determination).
The pipeline is **linear and therefore acyclic by construction** — each stage reads only from stages to its
left and never calls back.

### 2.2 Build-dependency DAG (what must exist before what)

Request-order ≠ build-order. In build terms, **Registry and Audit are foundational** (Audit is last in the
pipeline but must exist *first*, because every write must be audited). The build DAG:

```
                 ┌─────────────┐        ┌─────────────┐
   (foundation)  │ C1 Registry │        │  C9 Audit   │
                 └──────┬──────┘        └──────┬──────┘
                        │                      │
              ┌─────────┴─────────┐            │ (every mutating capability writes here)
              ▼                   ▼            │
        ┌───────────┐      ┌──────────────┐    │
        │C2 Version-│      │ C10 Authoring│◄───┘   (C10 requires C1 + C9)
        │ing & Eff. │      │  Workflow    │
        └─────┬─────┘      └──────────────┘
              ▼
        ┌─────────────┐
        │C3 Jurisdict.│  (also requires the RATIFIED stack)
        └─────┬───────┘
              ▼
        ┌─────────────┐
        │C4 Resolution│
        └─────┬───────┘
              ▼
        ┌───────────────────────────┐
        │ C5 Satisfaction Determ.    │  ── pairs with ──  ┌───────────────────────────┐
        │                            │                    │ C7 Financial-Override Det. │
        └─────┬─────────────────────┘                    └─────────────┬─────────────┘
              ▼                                                          │
        ┌─────────────┐   ◄─────────────────────────────────────────────┘
        │ C6 Snapshot │
        └─────┬───────┘
              ▼
        ┌─────────────┐
        │ C8 Override │  (requires C6 + C5 + C9)
        └─────┬───────┘
              ▼
        ┌──────────────────────────────┐
        │ C11 Consumption & Propagation │  (fronts C1/C4/C5/C6/C8; emits events)
        └──────────────────────────────┘
```

### 2.3 The four confirmations

- **No circular dependencies — CONFIRMED.** Topological sort exists (§3). Every edge points "later"; no
  capability requires a capability that (transitively) requires it. The one relationship that *looked*
  circular in the audit — MDL exposes endpoints to the Supervisor which supervises MDL — is one-way
  (Supervisor reads MDL; MDL does not depend on the Supervisor to compute), so it is not a build edge at all.
  The MDL→Trust discipline consumption is a *future* edge and is one-way (audit cleared the cycle).
- **No duplicated truth — CONFIRMED at the capability layer.** Each capability produces a distinct truth:
  definitions (C1), version/effectivity facts (C2), precedence ordering (C3), applicable set (C4), compliance
  result (C5), financial-override outcome (C7), frozen artifact (C6), runtime override outcome (C8), the trail
  (C9), events (C11). The audit's CR-1 duplicate ("Validation" vs "Enforcement") is a **Truth-Matrix labeling
  redundancy of C5**, not a second buildable capability — there is no "Enforcement" capability in the Core
  set, so the *buildable* set is non-redundant. (This is a useful disposition of CR-1: fix the label, not the
  build.)
- **No duplicated authority — CONFIRMED.** Every Core capability is owned by the **one** MDL domain; no two
  capabilities claim authority over the same decision. The financial override (C7) is MDL-owned and
  Economic-*consumed*, not co-owned. The only authority ambiguities the audit found (undefined
  Executive/Operators roles) are **consumer/actor** definitions, not *capability-owner* duplications — no Core
  capability's ownership is contested.
- **No impossible implementation order — CONFIRMED, with two gating ratifications.** The DAG sorts cleanly, so
  no capability is required before something it depends on. The only "impossible-until" edges are external to
  the graph: C3 cannot be *correct* until the jurisdiction stack is ratified, and C10/C11 access rules cannot
  be *specified* until the ops roles are defined. Neither is a cyclic or ordering impossibility; both are
  **inputs that must be supplied before those nodes are built.**

---

## 3. Implementation sequence — the smallest build order to a functioning MDL

"Functioning" = **the node can accept a mandate and return an authoritative, snapshotted determination for
an entity** — the irreducible purpose. Below is the actual dependency order (not phases/milestones).
Anything not on this list is *additive* to a functioning node.

**The critical path (minimal functioning MDL):**

1. **C9 Audit trail** — must exist before any write, because every mutation must be recorded (invariant).
2. **C1 Mandate Registry** — somewhere to hold a mandate.
3. **C10 Authoring Workflow (minimal)** — the only way to *get a mandate in*; without an author the registry
   is empty and nothing is resolvable. *(Blocked on defining the authoring role — audit CR-2.)*
4. **C2 Versioning & Effectivity** — a mandate must be versioned and effectivity-bounded to be resolved
   deterministically (immutability-per-version is an invariant).
5. **C3 Jurisdiction Resolution** — required for deterministic selection/precedence. *(Blocked on ratifying
   the canonical stack — audit A1/CR-5. With a single jurisdiction layer it is a near-no-op, but the ratified
   ordering must exist before it is correct for two.)*
6. **C4 Applicability Resolution** — the core "which mandates apply" — the first half of a determination.
7. **C5 Satisfaction Determination + C7 Financial-Override** — the determination itself (the two are one pass).
8. **C6 Snapshot** — freeze the determination; an unsnapshotted determination violates the immutability
   invariant, so this is **required**, not optional, for a *constitutional* functioning node.
9. **C11 Consumption Interface (minimal read/request face)** — a way for a consumer to ask and receive the
   determination. *(Least-privilege projections needed; admin projection blocked on the ops role — CR-2.)*

At step 9 the node **functions**: author a mandate → resolve → determine → snapshot → return.

**Additive capabilities (not required for a functioning single node; build when their need arrives):**

10. **C8 Override / Exception Evaluation** — needed only when non-compliant entities require sanctioned
    exceptions; a functioning node can deny-by-default without it.
11. **C11 Distribution / Propagation (event face)** — needed only for multi-node/cross-node propagation; a
    single embedded node functions without emitting events.

**Two ratifications gate the *start*, not the *shape*, of the build:**
- **Ratify the canonical jurisdiction stack** before C3 (audit A1/Q1). Non-negotiable — determinism is
  impossible over an undecided order.
- **Define the authoring/ops roles** before C10/C11 access rules (audit CR-2).

**Two questions can be deferred past the minimal build but must be answered before the corresponding
capability is trusted in production:**
- **Revocation / void-ab-initio vs snapshot immutability** (audit CR-3) — before C6/C8 are relied on for
  legally-consequential determinations.
- **Discipline-determination determinism** (audit CR-4) — only when the *future* discipline-consumption
  capability is scheduled; it does not touch the minimal Core build.

---

## 4. Buildability conclusion

**Can this be built exactly as described? Yes — the Core architecture is a clean, acyclic, non-redundant,
single-authority DAG that a team can implement in the order above — with two ratifications required before
the first blocked node (jurisdiction stack; ops roles), and two architectural questions to answer before the
snapshot/override and future-discipline capabilities are trusted.** No capability, on the minimal critical
path, requires violating an invariant to exist:
- Determinism (I1) is preserved on C3–C7 (no model in the path); the only sanctioned time-dependence is C8's
  override-expiry, which never touches the snapshot.
- Snapshot immutability (I2) is preserved by C6/C9 being append-only; the open storage/erasure pressure
  (H-8) is a *scaling* concern, not an *existence* blocker.
- Single-owner (I5) holds: every Core capability is MDL-owned; the DAG contains no second authority.
- Compile-not-legislate (I8) and resolve/act separation (I9) hold: C10 compiles authored obligations, C5/C7
  determine, and no Core capability executes a business or economic act.

The architecture's description and its buildability agree. The gaps that remain are the audit's — and none of
them makes the Core un-buildable; they make specific nodes *un-startable until an input (a ratified stack, a
defined role) is supplied*, or specific *future/edge* behaviors undefined. The right next action is therefore
to resolve the two gating ratifications, then build in the order of §3 — not to write more doctrine.
