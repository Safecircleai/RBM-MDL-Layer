# The RBM MDL Infrastructure Constitution

**Status:** FOUNDATIONAL — established this sprint; constitutional ratification rests with the Human
Ratifying Authority (§2). Architecture and doctrine only — this document defines the standard every
future mandate implementation must meet; it implements nothing.

**Heads:** `Immutable_Core_Charter.md` (the immutable core this constitution expands).
**Reads with:** `MDL_Consumer_Model.md` (the independence key — roles vs. occupants),
`MDL_Truth_Ownership_Matrix.md`, `MDL_Responsibility_Matrix.md`, `MDL_Lifecycle.md`.
**Founded on:** `MDL_Ownership_Analysis.md` (the Phase-1 evidence) and the uploaded operational specs
(Mandate Definition Layer Specification v1.0; MDL ↔ EchoForge Service Contract v1; Jurisdiction Stack
Model v1.0).
**Independence:** this constitution is **owned by the mandate domain** and depends on no other
repository, runtime, or assistant. It defines its own authority model (§2) and evidentiary standard
(§1.4) internally; it names no consumer as load-bearing.

---

## 0. What this constitution governs, and what it does not

This is the governing doctrine for **every mandate capability** the RBM ecosystem will ever build. It
defines mandate truth, authority, ownership, the mandate object, events, determinations, governance,
and the constitutional principles that bind all of them. It governs the *mandate domain* — the
definition, versioning, jurisdiction-resolution, satisfaction-determination, snapshotting, override,
and audit of mandates.

It does **not** govern:
- *The source obligations themselves.* Statutes, client contracts, and organizational policies are
  authored by their own authorities (`MDL_Consumer_Model.md` §1, "Mandate Authoring Authority"). This
  domain compiles and versions them; it does not legislate them.
- *Economic execution.* Booking an invoice, forcing a tax to zero, moving money — that is the Economic
  Consumer's. This domain owns the financial-override *determination*; the Economic Consumer owns the
  *economic effect* (`MDL_Truth_Ownership_Matrix.md`).
- *The business decision and the execution act.* Whether and how to act on a determination is the
  Business-Node Consumer's.
- *Ecosystem/assistant governance doctrine.* That is the Doctrine-Governance Consumer's (e.g. LEAL)
  and the ecosystem doctrine home's (e.g. SafeLaunchCenter); this domain neither authors nor depends
  on it.
- *Discipline-specific legal reasoning.* HIPAA/Legal/Tax/PCI reasoning belongs to the peer
  Discipline-Determination Provider; this domain may consume its determination but does not perform
  it.

The single deliberate design decision that makes this constitution durable: **it defines boundaries
for the fully-evolved ecosystem — many jurisdictions, many nodes, cross-node propagation, federated
enforcement — from the start**, so later capabilities add consumers and jurisdiction layers rather
than re-cutting boundaries.

---

## 1. Mandate Truth

**Definition.** *Mandate truth* is the authoritative answer to a question of mandate fact: which
mandates apply to this entity, in this jurisdiction, at this effective moment; at what versions; and
whether the entity satisfies them. It is distinct from the *source obligation* (the law or contract
itself, owned by its authority) and from *operational* truth a node legitimately holds (a work order,
a lease, an invoice).

**The four constitutional properties of mandate truth:**

1. **Single-owned.** Mandate truth has exactly one authoritative owner (`MDL_Responsibility_Matrix.md`).
   The moment two systems each resolve mandates authoritatively, the ecosystem has policy
   fragmentation and irreproducible enforcement — the failure mode this domain exists to end. No node
   keeps a parallel mandate authority (uploaded *MDL Spec* §5).
2. **Deterministic.** Given identical context — node type, entity type, service type, jurisdiction,
   effective date, entity attributes — resolution returns an identical result. No randomness, no
   environment drift (uploaded *MDL Spec* §2.2). Determinism is what makes the truth reproducible and
   auditable, and it is why the resolution path contains no probabilistic or model-driven step.
3. **Snapshot-frozen.** Every determination produces an immutable snapshot capturing the mandate
   configuration at the moment of evaluation. Snapshots survive mandate version changes; validation
   results reference snapshots, never live mandate records (uploaded *MDL Spec* §2.3, §3.8).
4. **Evidenced.** The mandate domain holds its **own** evidentiary standard (§1.4): every mandate
   determination carries a stable identifier, a named authoritative source (a specific mandate version
   and snapshot — never "the engine says so"), the resolved rule set it rested on, and a provenance to
   the authoring authority. A determination that cannot name its snapshot and versions is inadmissible.

**The AUTHOR / RESOLVE / ACT distinction (the sharpest idea in this constitution).** Authoring the
*source obligation* is different from *resolving and determining* it authoritatively, which is
different again from *acting* on the determination. A regulator or client **authors** a rule; the
mandate domain **resolves** which rules apply and **determines** satisfaction (the binding result +
snapshot); a business node **acts** on it (gates a payable) and the Economic Consumer **books** its
effect. Conflating these is exactly how a compliance engine either drifts into legislating policy it
has no authority to write, or is reduced to advisory noise a node may ignore. Every ownership question
in this constitution is answered along these three axes, never as a single "who controls it."

## 1.4 The evidentiary standard (owned here)

Every mandate claim carries: a stable claim identifier; a named **authoritative source** (the specific
mandate id + version + snapshot id); an accepted **evidence class** (a resolution event, a frozen
snapshot, a recorded override, a human ratification of a mandate version); and a **freshness anchor**
(the effective window and the snapshot timestamp). A mandate assertion with no snapshot or expired
effectivity is **inadmissible** — rendered as `UNRESOLVED`/`STALE`, never smoothed into a confident
"compliant." **Owning a truth does not exempt its owner from evidencing it.** A consumer also bound by
an ecosystem-wide truth convention reconciles the two on its own side; this standard stands on its own.

---

## 2. Mandate Authority

Mandate authority is the right to *resolve and determine* mandate truth. This domain defines its own
authority model — it is not derived from, and does not depend on, any consumer's authority. Authority
is assigned to **roles** (`MDL_Consumer_Model.md`), never to named systems:

- **The mandate domain holds resolving-and-determining authority:** it *resolves* which mandates apply
  and *determines* satisfaction, including the binding financial-override outcome. It never *authors*
  the source obligation and never *acts* on the determination.
- **Mandate Authoring Authorities hold authorship of the source obligation:** regulators, prime
  clients, an organization's governance, a program office. They author; the domain compiles and
  versions.
- **Business-Node and Economic Consumers hold action authority within their own scope:** the decision
  to gate, to book, to enforce a document requirement. They *act on* determinations; they do not
  produce them.
- **The Governance Supervisor holds oversight authority, read-only:** it monitors, risk-scores, and may
  quarantine a consumer that bypasses; it may never define mandates, rewrite snapshots, alter results,
  or disable enforcement (uploaded *Service Contract* §2, §5).
- **The Human Ratifying Authority holds ratification and exception authority** — the only role that may
  ratify a constitutional mandate-governance change or declare a bounded, logged exception.

**Authority is granted, never assumed.** Any expansion of this domain's authority requires an explicit,
bounded, logged grant ratified by the Human Ratifying Authority. A capability, clause, or config that
grants itself new authority is void. **The mandate domain may never author its own authority.**

---

## 3. Mandate Ownership

Ownership is resolved *per truth category*, along the AUTHOR / RESOLVE / ACT axes. This is the summary;
the authoritative grids are `MDL_Truth_Ownership_Matrix.md` (per truth) and `MDL_Responsibility_Matrix.md`
(per responsibility). Named systems are avoided; ownership is assigned to the **mandate domain** or a
**consumer role**.

| Mandate category | AUTHORS the source | RESOLVES / DETERMINES (owns truth) | ACTS on it |
|---|---|---|---|
| Mandate definition (encoded, versioned) | Mandate Authoring Authority (law/contract/policy) | **Mandate domain** (encodes, versions, stores) | — |
| Jurisdiction resolution (which layer wins) | — (stack is doctrine, §Jurisdiction) | **Mandate domain** | — |
| Applicability (which mandates apply to an entity) | — | **Mandate domain** (deterministic resolution) | Business-Node passes context |
| Satisfaction determination (compliant / not) | — | **Mandate domain** (validation + snapshot) | Business-Node gates on it |
| Financial override (e.g. tax exemption) | Mandate Authoring Authority (the exempting policy) | **Mandate domain** (the binding determination) | **Economic Consumer** books zero tax |
| Override / exception grant | Requestor + approver (dual auth) | **Mandate domain** (evaluates at runtime) | Business-Node honors outcome |
| Snapshot / mandate audit trail | — | **Mandate domain** (append-only, immutable) | Auditor reads |
| The business action (gate, block, proceed) | — | Mandate domain *determines*; it does not act | **Business-Node Consumer** |
| Economic execution (book, move money) | — | Mandate domain *determines* the override only | **Economic Consumer** |
| Discipline legal reasoning (HIPAA/Tax/Legal) | External law | **Discipline-Determination Provider** (peer) | Mandate domain *consumes* as a condition |
| Ecosystem/assistant governance doctrine | Ecosystem doctrine home | **Doctrine-Governance Consumer** (e.g. LEAL) | — (never resolves mandates) |

**The one-sentence rule of mandate ownership:** *the resolved, versioned, jurisdiction-aware,
snapshot-frozen mandate determination lives in the MDL domain — authoritatively and deterministically
— with the source obligation authored by its own authority, the economic effect booked by the Economic
Consumer, and the business action taken by the node. The domain owns the determination; it never owns
the law, the money, or the act.*

---

## 4. The Mandate Object

**Definition.** A *mandate* is a versioned, jurisdiction-scoped, node-and-entity-applicable structured
obligation with rule sets (documents, evidence, thresholds, participation, and financial policy). It is
the canonical unit of mandate truth (uploaded *MDL Spec* §3).

**Constitutional rules for the mandate object:**

1. **Versioned and immutable-per-version.** A new version never mutates a prior version's behavior;
   snapshots referencing older versions remain valid (uploaded *MDL Spec* §2.2, §7). Supersession links
   a new version to the one it replaces.
2. **Jurisdiction-scoped and precedence-ordered.** Every mandate names its jurisdiction layer; conflicts
   resolve by the deterministic precedence stack and inheritance behaviors (`MDL_Lifecycle.md` §Jurisdiction;
   uploaded *Jurisdiction Stack Model*).
3. **Declaratively applicable.** Applicability (entity type, optional service type, node type) is
   declarative data, evaluated against context a node supplies — not hardcoded per node (uploaded *MDL
   Spec* §3.3).
4. **Effectivity-bounded.** Each mandate carries an effective window; resolution honors effective and
   sunset dates.
5. **Attributed to an authoring authority.** Every mandate names the authority whose obligation it
   compiles, so provenance is traceable and re-encoding on a source change is a versioning event, not a
   silent edit.

---

## 5. Mandate Events

**Definition.** A *mandate event* is an atomic, recorded fact in a mandate's or determination's
lifecycle — created, versioned, published, resolved, snapshotted, overridden, retired. Events are the
only way mandate state advances and the only way consumers learn of change (`MDL_Event_Model.md`;
uploaded *Service Contract* §4).

**Constitutional rules for mandate events:**
1. **Immutable and append-only.** Events are never mutated or deleted; a correction is a new event with
   a lineage pointer.
2. **The mandate domain is the sole publisher.** No consumer emits mandate-domain events; consumers
   subscribe read-only (uploaded *Service Contract* §4; *Cross-Node Propagation Protocol* §4).
3. **Snapshot isolation on propagation.** Even when a mandate update propagates across nodes, existing
   snapshots remain bound to their original version; cross-node changes never mutate historical
   compliance (uploaded *Propagation Protocol* §3).
4. **Every mutation is audited.** Mandate creation/modification and override approval are logged with
   the acting identity (uploaded *MDL Spec* §9; *Service Contract* §7).

---

## 6. Mandate Determinations & State

**Definition.** A *determination* is the deterministic result of resolving mandates for an entity and
evaluating its state against them, frozen as a snapshot. *Mandate state* is the current derived
position — the latest validation status per entity — computed from determinations, never authored
directly.

**Constitutional rules:**
1. **Determinations are authoritative, not advisory.** A compliance determination and its financial
   override bind the consumer: the consumer *acts* on it and may not contradict, suppress, or bypass it
   (uploaded *MDL Spec* §2.5, §5; *Service Contract* §8). *(This is a deliberate revision of the earlier
   CFRS "soft validator" framing; see `Open_Questions_and_Risks.md`.)*
2. **Derived from snapshots, never asserted.** A validation result references a frozen snapshot and the
   mandate versions it rested on; a result that cannot name its snapshot is inadmissible.
3. **Determinism is a hard invariant.** No probabilistic or model-driven step exists in the resolution
   or determination path; identical context is identical result.
4. **Enforcement is a determination the domain owns and an action the consumer takes.** The domain owns
   *whether* an entity is compliant and *whether* an override applies; the consuming node performs the
   *act* (blocks the payable, requires the document); the Governance Supervisor ensures no actor
   bypasses. Owning the determination is not performing the act.

---

## 7. Mandate Governance (authoring workflow)

**Definition.** *Mandate governance* is the controlled process by which an authored obligation becomes
an active, versioned mandate — intake, encoding, review, approval, versioning, publication — and by
which overrides are granted.

**Constitutional rules:**
1. **The domain compiles; it does not legislate.** The source obligation is authored by its authority;
   the domain governs only the *encoding, review, approval, and versioning* of the mandate that compiles
   it.
2. **Role-based authorship.** Mandate creation/modification requires the appropriate authoring/ops role;
   schema modification requires an ops-admin role (uploaded *Service Contract* §7; *MDL Spec* §9).
3. **Overrides are dual-authorized, snapshot-bound, and non-mutating.** An override references a
   snapshot id, records requestor, approver, expiry, and reason, and modifies the *runtime outcome*
   without mutating the snapshot (uploaded *MDL Spec* §8; *Service Contract* §7).
4. **Supervised, not governed-from-outside.** The Governance Supervisor monitors this workflow
   read-only and may escalate; it never enters it as an author or approver of mandates.

---

## 8. Constitutional Principles

The principles that bind every mandate capability, present and future. A capability that violates any
of these is unconstitutional regardless of how useful it seems.

1. **One authoritative owner per mandate truth.** No duplicates, no forks, no competing resolution
   engines. Every mandate truth traces to exactly one owner — this domain.
2. **Compile, don't legislate.** The domain encodes and versions authored obligations; it never invents
   source policy.
3. **Deterministic by construction.** Identical context is identical result; no randomness, no model in
   the resolution path.
4. **Snapshot immutability.** A frozen determination is never mutated; version changes never alter
   history.
5. **Financial-override supremacy.** A mandate-level financial override binds over any node's tax engine
   or manual override.
6. **Jurisdictional precedence is explicit.** Conflicts resolve by a deterministic stack and declared
   inheritance behaviors, never ad hoc.
7. **Authoritative, not advisory.** Determinations bind consumers; a consumer acts but may not
   contradict.
8. **Resolve/act separation.** The domain determines; consumers act; the supervisor oversees. The domain
   never executes a business or economic action of its own.
9. **Least privilege everywhere.** Every consumer gets the narrowest projection its role requires
   (`MDL_External_Interfaces.md`); the Governance Supervisor's boundary is read-only.
10. **Boundaries cut for the end state.** Many jurisdictions, many nodes, cross-node propagation, and
    federated enforcement are anticipated from the first line, so growth adds consumers and jurisdiction
    layers rather than re-cutting boundaries. This is the principle that lets implementation evolve for a
    decade without rewriting the constitution.

---

## 9. What this constitution does not do

It defines no storage, API, schema, or enforcement mechanism — that is implementation, deliberately out
of scope for this foundation, though it remains consistent with the uploaded operational specs it
governs. It creates no source law and forbids legislating one. It is self-contained: it defines its own
authority and evidentiary standard and depends on no other repository, runtime, or assistant. A consumer
also bound by ecosystem-wide conventions reconciles them on its own side. It sets the bar every future
mandate capability must clear the moment it is built; it is the constitutional layer that must not need
rewriting as that implementation — or any current consumer — evolves.
