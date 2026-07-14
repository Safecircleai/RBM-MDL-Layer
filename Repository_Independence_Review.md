# Repository Independence Review

**Status:** FOUNDATIONAL — the independence audit of this sprint and the standing test that keeps the
node independent. Ratification rests with the Human Ratifying Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Depends on:** `MDL_Consumer_Model.md` (the role
vocabulary this review enforces).

---

## 0. The misunderstanding this review prevents

The MDL capability was first built *inside CFRS* (`RBM_CAPABILITIES_V1.md:1624`) and a plan once proposed
hosting it *inside EchoForge* (`EchoForge/MDL_LAYER_README.md:80-95`). Either would repeat the
**historical-location fallacy** the Economic Domain had to correct: *because work happened in a
repository, the new domain inherits a dependency on it* (`RBM-Economic-Core/Repository_Independence_Review.md:12-24`).

**The correction, enforced here from the first line:** RBM-MDL-Layer is an **independent infrastructure
node**. It owns its own mandate doctrine. CFRS, EchoForge, LEAL, Economic Core, UPM, PERSE, RESA, Atlas,
and every business node are **consumers** — they reference the constitution; they never own it, never
parent it, and are never assumed by it to exist. *Every node owns its own constitution; consumers
reference constitutions; consumers never become constitutional owners.*

---

## 1. The mechanism: roles replace names

Independence is achieved by one move, defined in `MDL_Consumer_Model.md` and applied everywhere: **the
constitution binds *roles*; named systems appear only as non-binding examples of who occupies a role
today.** The before→after vocabulary:

| Was (a named system, load-bearing) | Now (a role, occupant illustrative) |
|---|---|
| CFRS (the embedded engine's home) | **Business-Node Consumer** |
| EchoForge (proposed host / supervisor) | **Governance Supervisor** |
| LEAL | **Doctrine-Governance Consumer** |
| RBM-Economic-Core | **Economic Consumer (peer)** |
| EchoForge Trust Runtime | **Discipline-Determination Provider (peer)** |
| Atlas-Sync | **Intelligence Consumer** |
| Regulators / prime clients / an organization | **Mandate Authoring Authority** / **External Authority** |
| UPM, B4Arts, PERSE, Housing, … | **Business-Node Consumers** |
| Phil / ecosystem human governance | **Human Ratifying Authority** |
| "hosted inside / a service of EchoForge" | *(removed)* — the node owns its doctrine; EchoForge supervises, does not host |

The test for each replacement: **remove the example occupant and the clause must still stand.** Every
replacement above passes it.

## 2. The audit — document by document

Every document authored this sprint was checked against four coupling classes. "Clean" means: describes
only mandate-domain behavior, names no runtime as load-bearing, and remains valid if every current
runtime were replaced.

| Document | Coupling checked | Result |
|---|---|---|
| `CLAUDE.md` | Not framed as an assistant; defines no assistant authority; names EchoForge/CFRS only as role occupants. | Clean |
| `Immutable_Core_Charter.md` | Authority section is the domain's own; relationships table is roles with example occupants. | Clean |
| `MDL_Infrastructure_Constitution.md` | Authority (§2) and evidentiary standard (§1.4) internalized; ownership table (§3) is roles. | Clean |
| `MDL_Consumer_Model.md` | Independent by construction — defines the roles. | Clean |
| `MDL_Truth_Ownership_Matrix.md`, `MDL_Responsibility_Matrix.md` | Every cell names the domain or a role; occupants illustrate. | Clean |
| `MDL_Capability_Framework.md`, `MDL_Lifecycle.md`, `MDL_Internal_Architecture.md`, `MDL_Event_Model.md`, `MDL_Consumption_Model.md`, `MDL_External_Interfaces.md` | Named systems (EchoForge, CFRS, Economic Core, Atlas) appear only as role occupants or as spec sources. | Clean |
| `Repository_Ownership_Report.md`, `Migration_Strategy_CFRS_to_RBM_MDL.md` | CFRS/EchoForge named as *historical/consumer facts* (where code lives, who migrates), never as owners of this doctrine. | Clean (historical/consumer mentions only) |
| `IEF_Classification.md`, `IAF_Innovation_Assessment.md`, `MDL_vs_Industry_Systems.md` | External systems named as comparables/facts; frameworks reconstructed, provenance flagged. | Clean |

## 3. The four coupling classes, and how each was eliminated

1. **Ownership coupling** — a consumer treated as owner/parent of mandate doctrine. *Eliminated* by the
   consumer model: no consumer is an owner; the domain owns its doctrine.
2. **Authority coupling** — the domain's authority derived from a consumer's constitution. *Eliminated* by
   internalizing the authority model (`MDL_Infrastructure_Constitution.md` §2) and evidentiary standard
   (§1.4).
3. **Naming coupling** — a clause depending on a named runtime existing. *Eliminated* by role
   substitution; occupants are removable examples.
4. **Assistant coupling** — repository guidance that becomes assistant-specific. *Eliminated* by making
   `CLAUDE.md` and every document describe **domain behavior, never assistant behavior**; the domain
   defines no assistant authority and hosts no persona.

## 4. The ten-year test

The binding acceptance test: **the constitution must remain valid if every current runtime were
replaced.** Applied:
- Replace CFRS → the **Business-Node Consumer** role is unchanged; the migration names a fact, not a
  dependency.
- Replace EchoForge → the **Governance Supervisor** and **Discipline-Determination Provider** roles are
  unchanged; the Service-Contract boundary binds the *relationship*, not the party.
- Replace LEAL → the **Doctrine-Governance Consumer** role is unchanged.
- Replace Economic Core → the **Economic Consumer** role is unchanged.
- Replace Atlas → the **Intelligence Consumer** role is unchanged.
- Change regulators/clients/orgs → **Mandate Authoring Authority** / **External Authority** are unchanged.

In every case only the *occupant* changes; not one constitutional clause requires rewriting. The node
passes the test.

## 5. The standing rule that prevents regression

> **No document in RBM-MDL-Layer may (a) name a consumer as an owner of mandate doctrine, (b) derive the
> domain's authority or truth standard from a consumer's constitution, (c) contain a clause that fails if
> a named runtime is removed, or (d) describe assistant behavior. A named system may appear only as a
> non-binding example of a role's occupant, a historical fact (where code lives, who migrates), or a
> generic external-industry term (regulator, PSP, policy engine). Anything else is a regression and is
> fixed on sight.**

Passing this check is what it means, in practice, for RBM-MDL-Layer to stand as an independent
infrastructure node with consumers adapting to it — never it adapting to any consumer.
