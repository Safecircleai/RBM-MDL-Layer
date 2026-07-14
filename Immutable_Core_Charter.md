# Immutable Core Charter — RBM MDL Layer

**Status:** FOUNDATIONAL — the immutable core this node's constitution expands. Ratification rests
with the Human Ratifying Authority. Architecture and doctrine only.

**Reads with:** `MDL_Consumer_Model.md` (the independence key), `MDL_Infrastructure_Constitution.md`
(the governing doctrine). **Independence:** this charter is **owned by the mandate domain** and depends
on no other repository, runtime, or assistant; it names no consumer as load-bearing.

---

## 1. Mission

To be the RBM ecosystem's **single authoritative Mandate Definition Layer**: the one node that
compiles authored obligations into structured, versioned mandates and *deterministically resolves and
determines* which mandates apply to any entity, in any jurisdiction, at any time — with immutable
snapshots as the audit artifact — so that governance precedes execution and no business node
re-implements policy independently.

## 2. Purpose

The ecosystem cannot let each node invent its own compliance logic; that fragments policy, drifts
across jurisdictions, and makes enforcement irreproducible (uploaded *MDL Spec* §1;
`EchoForge/MDL_LAYER_README.md:18-25`). The MDL exists to centralize the *definition and resolution*
of mandates once, authoritatively, so every node consumes one truth.

## 3. Scope — what this node is

- A **policy compiler**: it encodes authored obligations into structured mandates.
- A **compliance resolution engine**: it resolves which mandates apply to an entity's context.
- A **determination authority**: it produces the authoritative, deterministic compliance result and
  the binding financial-override outcome, frozen as an immutable snapshot.
- A **governance backbone / infrastructure node**: all future nodes treat it as infrastructure
  (uploaded *MDL Spec* §12).

## 4. Non-goals — what this node is NOT, and must never become

1. **Not the source authority.** It does not author the statute, contract, or organizational policy it
   compiles. It compiles; it does not legislate.
2. **Not an executor.** It holds no value and performs no business action. It owns the determination;
   consumers act on it.
3. **Not the economic domain.** It owns the financial-override *mandate*; it does not book invoices,
   move money, or own economic truth (that is the Economic Consumer's).
4. **Not the governance supervisor.** It does not monitor bots, risk-score AI, or quarantine — that is
   the Governance Supervisor's role over a read-only boundary.
5. **Not a discipline legal-reasoner.** It does not perform HIPAA/Legal/Tax/PCI legal reasoning — that
   is the peer Discipline-Determination Provider's; MDL may consume its determination as an input.
6. **Not an assistant, and defines no assistant authority.** It hosts no persona and no task-intake
   convention.
7. **Not the CFRS implementation.** CFRS retains its embedded MDL until migration; this is a new,
   independent node.

## 5. Authority

This node holds exactly one kind of authority: **authority over resolved-mandate truth** — the right
to be the single, authoritative, deterministic answer to "which mandates apply and are they
satisfied." It holds no authority beyond that. It never authors the source policy, never executes,
never decides a business action, and may never author its own authority. Any expansion of this node's
authority requires an explicit, bounded, logged grant ratified by the Human Ratifying Authority. A
clause, capability, or configuration that grants itself new authority is void.

## 6. Ecosystem relationships (roles, not names)

This node relates to every other system by **consumer role** (`MDL_Consumer_Model.md`): a Human
Ratifying Authority ratifies it; Mandate Authoring Authorities author the obligations it compiles; a
Governance Supervisor monitors it read-only; a Doctrine-Governance Consumer governs system-compliance
without resolving mandates; Business-Node Consumers pass context and act on determinations; an
Economic Consumer books the financial effect; a peer Discipline-Determination Provider answers
discipline law; Intelligence and Auditor consumers read. Change the occupants and this charter is
unchanged.

## 7. The immutable guarantees

These five guarantees are the immutable core; violating any is a constitutional defect (uploaded
*Service Contract* §8; *MDL Spec* §§2.2–2.5, §7):

1. **Snapshot immutability** — a determination, once frozen, is never mutated; version changes never
   alter historical results.
2. **Deterministic resolution** — identical context yields an identical result; no randomness, no
   environment drift.
3. **Financial-override supremacy** — a mandate-level financial override (e.g. tax exemption) binds
   over any node's tax engine or manual override.
4. **Jurisdictional precedence** — mandate conflicts resolve by an explicit, deterministic precedence
   stack, never ad hoc.
5. **One authoritative owner** — mandate resolution is owned once, here; no node duplicates it.

These guarantees hold across a decade because each is defined by a *relationship or invariant*, not by
any named runtime, jurisdiction, or vendor.
