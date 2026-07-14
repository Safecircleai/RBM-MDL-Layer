# The MDL Capability Framework

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only — this classifies capabilities; it builds none of them.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Companion:** `MDL_Responsibility_Matrix.md`
(who owns each), `MDL_External_Interfaces.md` (who may see each), `MDL_Internal_Architecture.md` (where
each lives).

---

## 0. Think in capabilities, not APIs

This framework enumerates the *capabilities* the mandate domain needs — the things it must be able to
do — independent of any service, endpoint, or vendor. A capability is a durable function ("resolve
applicable mandates", "freeze a snapshot"); an API is a perishable implementation detail. Cutting the
constitution along capabilities is what lets the implementation change deployments and vendors for a
decade without the constitution changing.

Each capability is classified on two axes:
- **Tier** — **Core** (constitutive; the node is not itself without it), **Optional** (real, but not
  required for the node to exist), **Future** (anticipated, not built at the foundation), or **External**
  (belongs to another node/authority, consumed not owned).
- **Determinism** — whether it sits on the **deterministic path** (resolution/determination, where no
  randomness or model is permitted) or is **off-path** (distribution, audit read, admin).

---

## 1. Core capabilities — the node is not itself without these

| Capability | Tier | What it is | Constitutional note |
|---|---|---|---|
| **Mandate Registry** | Core | The authoritative store of encoded, versioned mandates and their rule sets. | The reason the node exists; the single owner of mandate definitions (uploaded *MDL Spec* §3). |
| **Jurisdiction Resolution** | Core | Applies the precedence stack + inheritance behaviors to order and reconcile mandates across layers. | Deterministic; conflicts resolve by explicit rules, never ad hoc (`MDL_Lifecycle.md` §Jurisdiction). |
| **Versioning & Effectivity** | Core | Version chains, supersession, effective/sunset windows; new versions never mutate old behavior. | Immutable-per-version (uploaded *MDL Spec* §7). |
| **Applicability Resolution** | Core | Deterministically returns the mandates applicable to an entity context (node/entity/service type, jurisdiction, date, attributes). | On the deterministic path; identical context → identical result (uploaded *MDL Spec* §2.2, §4.1). |
| **Satisfaction Determination (Validation)** | Core | Evaluates entity state against the resolved mandate set → compliance status + per-rule gaps. | Authoritative, not advisory (`MDL_Infrastructure_Constitution.md` §6; uploaded *MDL Spec* §4.3). |
| **Snapshot & Immutability** | Core | Freezes the mandate configuration at determination time as an immutable audit artifact; results reference snapshots, not live records. | Snapshot immutability is an immutable guarantee (uploaded *MDL Spec* §2.3, §3.8). |
| **Financial-Override Determination** | Core | Resolves binding financial policy (e.g. `tax_exempt_override`) that overrides node tax engines. | Financial supremacy (uploaded *MDL Spec* §2.5); booked by the Economic Consumer. |
| **Override / Exception Evaluation** | Core | Dual-authorized, snapshot-bound, expiring overrides that modify runtime outcome without mutating the snapshot. | Non-mutating (uploaded *MDL Spec* §8). |
| **Mandate Audit Trail** | Core | Append-only, immutable log of mandate mutations, determinations, and override approvals. | Audit-trail integrity (uploaded *MDL Spec* §9). |
| **Authoring & Governance Workflow** | Core | Role-based intake→encode→review→approve→version→publish of mandates. | The domain compiles; it does not legislate (§Constitution §7). |
| **Consumption Interface & Propagation** | Core | The resolve/validate/tax-policy/status entry points and the event stream consumers subscribe to. | Sole publisher of mandate-domain events (uploaded *Service Contract* §3–4). |

## 2. Optional capabilities — real, but the node exists without them

| Capability | Tier | What it is | Constitutional note |
|---|---|---|---|
| **Participation Aggregation** | Optional | Aggregates participation (e.g. MWBE/workforce) against mandate targets across an entity portfolio. | Snapshot-bound (uploaded *MDL Spec* §3.7); the node exists without cross-portfolio math. |
| **Eligibility Determination** | Optional | Computes eligibility *status* from eligibility-rules-as-mandates. | The status is the domain's; the *grant/deny decision* is the Business-Node's (`MDL_Truth_Ownership_Matrix.md`). |
| **Conflict-Review Queue** | Optional | Surfaces same-level, ambiguous mandate conflicts that cannot auto-resolve, for human review. | Required by the stack's "flag for review" rule (uploaded *Jurisdiction Stack* §3). |
| **Mandate-Simulation / Dry-Run** | Optional | Resolves/determines against hypothetical context without recording a snapshot. | Read-only; never writes truth. |
| **Consumer Registration** | Optional | Nodes declare `node_id`, `node_type`, `jurisdiction_scope` and subscribe to updates. | Enables scoped propagation (uploaded *Propagation Protocol* §4). |

## 3. Future capabilities — anticipated, not built at the foundation

| Capability | Tier | What it is | Constitutional note |
|---|---|---|---|
| **Event-Driven Distributed Enforcement** | Future | Federated propagation and enforcement across many independently deployed nodes. | Anticipated deployment Phase 3 (uploaded *Propagation Protocol* §5, §1). |
| **Discipline-Determination Consumption** | Future | A mandate satisfaction condition that requires a peer discipline determination (HIPAA/Legal/Tax). | MDL *consumes* the peer's determination; it never performs the legal reasoning. |
| **Multi-Tenant Isolation at Scale** | Future | Hard cross-node/cross-tenant contamination prevention as node count grows. | Required by security & isolation (uploaded *MDL Spec* §9). |
| **Mandate Intelligence (data)** | Future | The authoritative data substrate for mandate-coverage / drift analytics. | The domain produces the data; Intelligence consumers present the insight (read-only). |

## 4. External capabilities — owned by other nodes/authorities, consumed not owned

| Capability | Owner | MDL domain's relationship |
|---|---|---|
| **Source obligation** (law, contract, org policy) | Mandate Authoring Authority / External Authority | MDL *encodes and versions* it; never authors it. |
| **Economic execution** (booking, tax remittance, money movement) | Economic Consumer / Regulated providers | MDL *determines* the override; the Economic Consumer *books* it. |
| **Discipline legal reasoning** (HIPAA/Legal/Tax/PCI) | Discipline-Determination Provider (peer) | MDL *consumes* the determination as a satisfaction condition. |
| **Governance supervision / risk scoring** | Governance Supervisor | MDL *exposes* read-only endpoints and events; the Supervisor watches. |
| **Ecosystem/assistant governance doctrine** | Doctrine-Governance Consumer / doctrine home | MDL is a *bound system*; it does not author this. |
| **The business action** (gate, block, proceed) | Business-Node Consumer | MDL *determines*; the node *acts*. |

## 5. The classification rule, and the line

**The line is the deliverable.** Everything in §1 is the *mandate resolution/determination* the domain
owns. §2 are real extensions that do not constitute the node. §3 are anticipated. §4 is everything the
domain *touches but must never become*.

**How to classify a new capability** (the test every future proposal must pass):
1. **Does it author a source obligation (a law, contract, or policy)?** If yes, it is a Mandate Authoring
   Authority's, never the domain's — the domain may only *encode* it.
2. **Does it execute a business or economic action, or hold value?** If yes, it is a Business-Node's or
   the Economic Consumer's; the domain may only *determine*.
3. **Does it perform discipline legal reasoning, risk scoring, or ecosystem-governance?** If yes, it
   belongs to the peer/consumer that owns that; the domain may only *consume* or *expose*.
4. **Is it resolution, determination, versioning, snapshotting, override evaluation, or propagation of
   mandates?** If yes, it is a mandate-domain capability — classify its tier and place it in §1–§3.

A capability that cannot be placed by this test is a signal the boundary is being tested — the correct
response is to escalate to a decision-role consumer and, if constitutional, to the Human Ratifying
Authority, never to invent a new mixed capability inside the mandate domain.
