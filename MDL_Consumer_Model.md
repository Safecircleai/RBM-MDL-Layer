# The MDL Consumer Model

**Status:** FOUNDATIONAL — the independence key for this repository. Ratification rests with the
Human Ratifying Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Purpose:** to make RBM-MDL-Layer a
self-contained infrastructure node by defining *consumers as roles*, so that no named runtime, node,
or assistant is ever hardwired into the mandate constitution. Read this first — it is the interpretive
key to every other document here.

---

## 0. The independence principle

**RBM-MDL-Layer is an independent infrastructure node. It owns its own mandate doctrine. Every other
system in the ecosystem is a consumer of that doctrine — never an owner of it, never a parent of it,
and never a dependency the doctrine assumes into existence.**

A capability authored *inside* another repository's history (the MDL engine was first built inside
CFRS) does not make that repository the owner of what the doctrine governs. Mandate doctrine is owned
by the mandate domain regardless of where it was first written. This document exists so the whole
constitution can be read, and remains valid, **without any particular consumer existing** — if every
current runtime were replaced in ten years, not one clause below would need rewriting, because not one
clause names a runtime as load-bearing.

**The rule, stated so it can be enforced:** *Every constitutional statement in this repository
describes mandate-domain behavior in terms of roles. A named product, node, assistant, or service may
appear only as a non-binding example of who occupies a role today. Remove the example and the clause
must still stand.*

---

## 1. Consumers are roles, not names

A **consumer role** is a relationship a system may have to the mandate domain. Roles are permanent and
doctrinal; the systems that occupy them are contingent and replaceable. The constitution binds the
role; it never binds the occupant.

| Consumer role | What the role does with the mandate domain | Example occupant today (non-binding) |
|---|---|---|
| **Human Ratifying Authority** | Ratifies constitutional change; authorizes constitutional exceptions; the only role that may amend this constitution. A human role by definition. | The ecosystem's human founder/governance |
| **Mandate Authoring Authority** | *Authors the source obligation* MDL compiles — a statute, a client-contract clause, an organizational policy, a program rule. MDL encodes and versions what this role authors; it never invents policy of its own. | Regulators, prime-contract clients, an organization's governance, a program office |
| **Governance Supervisor** | *Monitors* MDL over a read-only boundary — risk-scores behavior, detects override/anomaly patterns, can quarantine consumers that try to bypass. Supervises; never defines, rewrites, or disables mandates. | EchoForge (per the MDL ↔ EchoForge Service Contract) |
| **Doctrine-Governance Consumer** | Governs *ecosystem/assistant doctrine and system-compliance* — interprets governance doctrine into enforceable checks on *bots/systems*. Never resolves mandates. | The ecosystem's compliance-of-systems engine (e.g. LEAL) |
| **Business-Node Consumer** | Passes entity context to MDL before finalization, *acts* on the determination (gates a payable, enforces a document requirement), and never duplicates mandate logic. Decides its own business action; consumes the mandate outcome. | Fleet, Housing, Property-Management, Arts, Emergency-Response and other product nodes (e.g. CFRS, UPM, B4Arts, PERSE) |
| **Economic Consumer (peer domain)** | Consumes MDL's *financial-override and compliance determinations* and books the economic effect (e.g. forces tax to zero); owns economic truth, not mandate truth. | The ecosystem's Economic Domain (e.g. RBM-Economic-Core) |
| **Discipline-Determination Provider (peer)** | A *peer* trust/compliance runtime that answers discipline-specific legal determinations (HIPAA, Legal, Tax, PCI). MDL may *consume* its determination as one satisfaction condition of a mandate; neither owns the other. | EchoForge's Trust Service Runtime |
| **Intelligence Consumer** | Reads *aggregate* mandate metrics and runtime health to produce insight/readiness scoring. Read-only; advisory; never writes mandate truth. | An ecosystem intelligence/observability service (e.g. Atlas-Sync) |
| **Auditor / Oversight Consumer** | Reads mandate truth and snapshots after the fact, read-only, through governed interfaces, to verify it. | Internal/external auditors, regulators exercising oversight |

**No role in this table is an owner of mandate truth.** Ownership of the resolved-mandate truth belongs
to the mandate domain alone (`MDL_Infrastructure_Constitution.md` §1). Every role above is a *consumer*
of it — that is the entire point of the model.

---

## 2. What a consumer may do, and what it may never do

Uniform rules that bind every consumer role, so the domain's independence does not depend on the good
behavior of any particular occupant:

**A consumer MAY:**
- Reference this constitution and build against the capabilities and determinations it defines.
- Occupy exactly the role(s) the model grants it, and read exactly the projection least-privilege
  allows for those roles (`MDL_External_Interfaces.md`).
- Pass entity context and *receive* an authoritative determination; act on that determination within
  its own scope.
- Adapt itself to the mandate domain's interfaces and doctrine.

**A consumer MAY NEVER:**
- Become an owner of any resolved-mandate truth, or author mandate doctrine on the domain's behalf.
- Duplicate, fork, or re-implement mandate resolution/enforcement logic (uploaded *MDL Spec* §5).
- Contradict, suppress, or bypass an authoritative determination or financial override (uploaded *MDL
  Spec* §5; *Service Contract* §8).
- Require the mandate domain to adapt its constitution to the consumer's internal design.
- Assume, in the domain's own documents, that the consumer exists — the constitution must read
  correctly with the consumer absent.

**The direction of adaptation is fixed:** *consumers adapt to the mandate domain; the mandate domain
never adapts to a consumer.* A request that would require the constitution to bend around one consumer
is, by that fact, out of order — it is resolved by the consumer changing, or by a constitutional
amendment made through the Human Ratifying Authority, never by silent coupling.

---

## 3. Supervision and authorship are consumer roles, not ownership

Two roles deserve explicit clarification because they are easily mistaken for ownership:

- **The Governance Supervisor** (e.g. EchoForge) *supervises* MDL — it reads, monitors, risk-scores,
  and can escalate to quarantine — but it "does not define mandates … does not rewrite snapshots …
  does not alter compliance results" (uploaded *Service Contract* §2). Supervision is oversight of a
  boundary, not ownership of what lies inside it. EchoForge "cannot disable MDL enforcement" (§5).
- **The Mandate Authoring Authority** (regulators, clients, an organization) *authors the source
  obligation*. MDL compiles that obligation into a structured, versioned mandate and owns the
  authoritative *encoded and resolved* form — but it never authors the underlying law or contract. A
  regulator changing a statute is the authority changing; MDL re-encodes and re-versions. The domain
  compiles policy; it does not legislate it.

Assistants, orchestration runtimes, and automations are simply systems that occupy one or more
consumer roles. They have no special standing in the mandate domain; an assistant brings its authority
from its *own* home constitution, which is not this one. This repository defines, grants, and
constrains no assistant authority and hosts no persona.

---

## 4. How to read every other document in this repository

Wherever any document here shows a named system (CFRS, EchoForge, LEAL, Economic Core, UPM, PERSE,
RESA, Atlas, an Insurance node), read it as **"the occupant of role R, today"** — not as a dependency.
The binding content is always the role. `Repository_Independence_Review.md` verifies that every such
name is removable without loss, and that no clause makes the domain subordinate to, or dependent on,
any consumer.

This model is therefore the interpretive key to the whole constitution: **roles bind; occupants
illustrate; the domain stands alone.**
