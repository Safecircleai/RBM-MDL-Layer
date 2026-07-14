# safecircleai/RBM-MDL-Layer — Repository Identity & Scope

**What this repository is:** the **constitutional Mandate Domain** of the RBM ecosystem — an
independent infrastructure node that owns the ecosystem's authoritative **Mandate Definition Layer
(MDL)**. It is the single, node-agnostic authority that *resolves* which mandates apply to an entity,
in a jurisdiction, at a version, and *determines* (deterministically, with immutable snapshots)
whether that entity satisfies them. It is doctrine now and (in a future implementation phase this
sprint does not begin) governance infrastructure.

**What this repository owns:** its own mandate doctrine, in full — the mandate model, the
jurisdiction stack, versioning and effectivity, resolution, snapshot immutability, the authoritative
compliance determination (including binding financial overrides), override evaluation, and the
mandate audit trail. These are **owned by this domain** — not by CFRS (where the capability was first
built), not by EchoForge (which supervises but does not own mandates), and not by any consuming node.

**What this repository is NOT, and does not do:**
- It is **not** the CFRS MDL implementation. CFRS retains its embedded MDL until migration; this node
  is a *new, independent* infrastructure node (`Migration_Strategy_CFRS_to_RBM_MDL.md`).
- It is **not part of** EchoForge, and EchoForge does not own or define mandates. EchoForge is the
  **governance supervisor** that monitors MDL, risk-scores, and can quarantine — over a read-only
  boundary (`MDL_External_Interfaces.md`, and the uploaded `MDL ↔ EchoForge Service Contract`).
- It **authors no source policy.** Regulators, organizations, and client contracts *author* the
  obligations; MDL *encodes, versions, resolves, and determines* them. It compiles policy; it does not
  invent it (`MDL_Truth_Ownership_Matrix.md`).
- It **executes nothing and holds no value.** It owns the authoritative *determination*; consuming
  nodes *act* on it (gate a payable, book a zero-tax invoice); EchoForge *supervises* the boundary.
- It **defines no assistant authority** and hosts no persona. An assistant operating here brings its
  authority from its own home constitution.

**How an assistant should work in this repository:** treat the mandate constitution as authoritative
domain doctrine; describe **domain behavior, never assistant behavior**; add no persona, chain of
command, or task-intake convention; introduce no coupling that assumes a specific consumer exists.
For cross-domain matters, an assistant defers to whatever authority its *own* home constitution
defines — this repository does not define that and is not that authority.

**Ecosystem convention (courtesy, not dependence):** the ecosystem maintains a `CLAUDE.md` identity
convention so no session mistakes a repository's guidance for ecosystem-wide authority. This file
honors that convention *and* the independence principle at once: it states an identity so no session
is confused, while making explicit that this domain is self-contained and subordinate to no consumer.

---

## Start here

`README.md` indexes the constitutional documents. Read `MDL_Consumer_Model.md` first for the
interpretive key: **roles bind; named occupants only illustrate; the domain stands alone.** This
repository currently contains **doctrine only** — no services, APIs, database models, migrations, or
integrations exist here yet, by design. The uploaded operational specs (Mandate Definition Layer
Specification v1.0, MDL ↔ EchoForge Service Contract v1, Jurisdiction Stack Model v1.0) are the
**operational contract** this doctrine governs and remains consistent with; where the doctrine and
those specs are reconciled, see `Open_Questions_and_Risks.md` §"Conflict & Source-Reconciliation
Report".
