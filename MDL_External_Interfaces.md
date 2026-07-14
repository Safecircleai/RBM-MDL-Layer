# MDL External Interfaces & Least-Privilege Boundaries

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Companion:** `MDL_Responsibility_Matrix.md`
(who is responsible), `MDL_Consumption_Model.md` (how consumers integrate), `MDL_Event_Model.md` (the
events). **Reads with:** the uploaded *MDL ↔ EchoForge Service Contract v1* (the read-only supervision
boundary) and *MDL Specification* §5, §9 (cross-node integration & isolation).

---

## 0. The principle

**The MDL domain owns resolved-mandate truth; every other node gets the narrowest interface its
constitutional role requires — and nothing more.** Access is least-privilege by construction, not
convention. Boundaries are expressed as five interface modes, because saying only what a node *may do*
is half a boundary — what it must *never* do is as constitutional as what it may:

- **Consumes MDL** — sends entity context, receives a determination (resolve / validate / tax-policy /
  status).
- **Publishes to MDL** — authors/updates mandates through the governed authoring workflow.
- **Receives Events** — subscribes to the mandate-domain event stream, read-only.
- **Reads Only** — read access to mandate definitions, snapshots, validation outputs, audit — no writes.
- **Administrative Access** — schema/role/ops administration of the node itself.

**No node may hold a mode it does not need.** In particular, *publish* and *administrative* access are
the rare, guarded modes; the default for a business node is *consume + receive-events*, and for a
supervisor/auditor is *read-only*.

---

## 1. The interface matrix (roles, not names)

Occupants illustrate; the role binds (`MDL_Consumer_Model.md`). ✓ = granted; — = denied.

| Node / role | Consumes MDL | Publishes to MDL | Receives Events | Reads Only | Administrative | Never |
|---|---|---|---|---|---|---|
| **Business-Node Consumer** (e.g. CFRS, UPM, Housing, B4Arts, PERSE) | ✓ (resolve/validate/tax-policy/status) | — (except its *own* node-scoped mandates via authoring workflow, if granted the authoring role) | ✓ (its subscribed scope) | ✓ (its own snapshots/results) | — | Duplicate resolution logic; bypass a determination; read another node's mandate data |
| **Economic Consumer** (e.g. RBM-Economic-Core) | ✓ (tax-policy / validation *outcomes* it must book) | — | ✓ (financial-override changes) | ✓ (determinations it consumes) | — | Author mandates; alter a determination; define financial policy of its own |
| **Governance Supervisor** (e.g. EchoForge) | — (does not *drive* determinations) | — (may NOT write mandates) | ✓ (all mandate/snapshot/override events) | ✓ (mandates, validation outputs, override logs, version changes) | — | Write mandates; modify validation results; alter snapshots; force overrides; **disable enforcement** (uploaded *Service Contract* §2–5) |
| **Doctrine-Governance Consumer** (e.g. LEAL) | — | — | ✓ (as a bound system, for compliance-of-systems) | ✓ (aggregate/audit metadata) | — | Resolve mandates; introduce governance interpretations into mandate truth |
| **Discipline-Determination Provider** (peer, e.g. Trust Runtime) | ✓ (only if a mandate consumes its determination) | — | — | — | — | Own or resolve mandates; treat its determination as a mandate |
| **Intelligence Consumer** (e.g. Atlas-Sync) | — | — | ✓ (aggregate metrics/health) | ✓ (aggregate only) | — | Transaction/entity-level detail; PII; any write |
| **Mandate Authoring Authority** (regulator/client/org) | — | ✓ (authors the source obligation via governed intake) | — | ✓ (its own authored mandates) | — | Resolve/determine; touch another authority's mandates |
| **Auditor / Oversight Consumer** | — | — | — | ✓ (mandates, snapshots, audit trail, read-only) | — | Any write; mutate a snapshot |
| **Operators** (the node's own staff) | ✓ | ✓ (governed) | ✓ | ✓ | ✓ (schema/role/ops) | Raw edits that bypass audit; mutate snapshot history |
| **Human Ratifying Authority** | — | — | — | ✓ (everything, governed & logged) | Break-glass only, logged, with reason & expiry | — |

## 2. The supervision boundary (called out because it is easily over-granted)

The Governance Supervisor is the one role that watches *everything* and may change *nothing* in the
mandate truth. Its interface is fixed by the uploaded *Service Contract*:
- **May:** read mandate definitions, read validation outputs, read override logs, monitor version
  changes, subscribe to events (§3), and escalate — Soft Alert, Sentinel Alert, Quarantine Mode, Repair
  Mode (§5).
- **May NOT:** directly write mandates, modify validation results, alter snapshot history, force
  compliance overrides (§3), or **disable MDL enforcement** (§5).

This is the reason supervision is modeled as a *read-only edge of the Interface layer*
(`MDL_Internal_Architecture.md` §1, layer 11), not as a layer with reach into the deterministic core. It
lets the supervisor be absolute at the *oversight* interface (uploaded *AI Governance Guardrails* §1: no
AI execution may finalize/approve/override/modify without an MDL validation check, and EchoForge
intercepts a bypass) while being powerless over mandate truth.

## 3. Cross-node isolation (no unnecessary privilege)

Per the uploaded *MDL Spec* §9 and *Propagation Protocol* §4:
- Every node **declares** `node_id`, `node_type`, `jurisdiction_scope` at registration; its interface is
  scoped to that declaration.
- **Cross-node contamination is prevented**: a node reads only its own entity data, snapshots, and the
  mandates in its scope; a Federal-layer mandate is available to all, a State-layer mandate only to nodes
  in that state, a Prime-layer mandate only to associated entities (uploaded *Propagation Protocol* §2).
- **Mandate creation/modification is role-based** and logged; **schema modification requires ops-admin**
  (uploaded *Service Contract* §7).

## 4. Why these boundaries hold across a decade

Each interface is defined as a *projection of the single authoritative truth*, so adding a new consumer
means defining a new projection — never widening an existing node's access or duplicating the truth. The
supervisor's read-only boundary and the authoring workflow's RBAC are structural, not conventional, so
they do not erode as the node grows: a new business node arrives as *consume + receive-events* by
default, and any expansion beyond that is an explicit, ratified grant, never a silent one.
