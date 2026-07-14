# The MDL Event Model

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only — this defines the event doctrine, not a schema or broker.

**Governed by:** `MDL_Infrastructure_Constitution.md` §5. **Reads with:** `MDL_Lifecycle.md`,
`MDL_Consumption_Model.md`, and the uploaded *MDL ↔ EchoForge Service Contract* §4 (the event hooks) and
*Cross-Node Mandate Propagation Protocol* (propagation).

---

## 0. The event doctrine

Mandate state advances only by events, and consumers learn of change only by events. Three rules bind
every mandate-domain event:

1. **The mandate domain is the sole publisher.** No consumer emits a mandate-domain event; consumers
   subscribe read-only (uploaded *Service Contract* §4).
2. **Events are immutable and append-only.** A correction is a new event with a lineage pointer, never a
   mutation.
3. **Propagation never mutates history.** When an event propagates a mandate change, existing snapshots
   remain bound to their original version; cross-node changes never alter historical compliance
   (uploaded *Propagation Protocol* §3).

---

## 1. The canonical events

The core event set is fixed by the uploaded *Service Contract* §4; this doctrine adopts those names as
canonical and groups them by the lifecycle stage that emits them (`MDL_Lifecycle.md`).

### Definition-lifecycle events (the mandate clock)

| Event | Emitted when | Primary subscribers |
|---|---|---|
| `MANDATE_CREATED` | A new mandate is authored and approved. | Supervisor, subscribed nodes |
| `MANDATE_VERSIONED` | A new version is created (supersession link set). | Supervisor, subscribed nodes |
| `MANDATE_UPDATED` | An active mandate's non-behavioral metadata changes. | Supervisor, subscribed nodes |

### Application-lifecycle events (the determination clock)

| Event | Emitted when | Primary subscribers |
|---|---|---|
| `SNAPSHOT_CREATED` | A determination freezes a snapshot. | Auditor, Supervisor |
| `VALIDATION_RESULT_RECORDED` | A determination's result is persisted (references a snapshot). | Business-Node, Economic, Auditor |
| `OVERRIDE_CREATED` | A dual-auth override is requested. | Supervisor (override-frequency), Auditor |
| `OVERRIDE_APPROVED` | An override's second authorization is recorded. | Supervisor, Auditor |
| `OVERRIDE_REVOKED` | An override is revoked (or expires). | Supervisor, Business-Node, Auditor |

*(A future `MANDATE_RETIRED`/`MANDATE_SUPERSEDED` pair is anticipated for the retirement stage; it is
named here so it is added to this canonical set, not invented ad hoc, when the retirement lifecycle is
implemented — `Open_Questions_and_Risks.md`.)*

## 2. Propagation semantics (scoped, not broadcast)

A mandate change propagates only as far as its jurisdiction scope reaches (uploaded *Propagation
Protocol* §2):

| Authored at layer | Propagates to |
|---|---|
| **Federal** | All nodes |
| **State** | Nodes registered in that state |
| **Prime (contract)** | Entities associated with the prime |
| **Program** | Entities in that program |

Each node registers `node_id`, `node_type`, `jurisdiction_scope` and subscribes to the update events
relevant to its scope (uploaded *Propagation Protocol* §4). Scoped propagation is a least-privilege
property: a node never receives events for mandates outside its jurisdiction, so it cannot even learn of
another scope's policy.

## 3. Snapshot isolation under propagation

The most important invariant this model protects: **a propagated change never rewrites the past.** When
`MANDATE_VERSIONED` fires and a node updates to the new version for *future* resolutions, every snapshot
already frozen against the old version stays valid and unchanged (uploaded *MDL Spec* §7; *Propagation
Protocol* §3). This is what lets a mandate evolve continuously across a federation while every historical
determination remains reproducible.

## 4. What events are used for by whom

- **Business-Nodes** react to `MANDATE_VERSIONED`/`_UPDATED` to know a re-evaluation may be due, and to
  `VALIDATION_RESULT_RECORDED`/`OVERRIDE_*` for their own entities.
- **The Governance Supervisor** subscribes to *all* events to detect anomalies — override-frequency
  spikes, repeated `NON_COMPLIANT` submissions, mandate-mutation attempts, tax-override anomalies
  (uploaded *AI Governance Guardrails* §3) — and to escalate (Soft/Sentinel Alert, Quarantine, Repair
  Mode).
- **The Economic Consumer** reacts to financial-override changes to re-book affected economic effects.
- **Intelligence Consumers** consume *aggregate* event metrics only (no entity-level detail).
- **Auditors** consume snapshot/override events for the immutable trail.

## 5. Why the event model holds for a decade

Because the publisher is single, the events are append-only, and propagation is scope-bounded and
snapshot-isolated, the event model scales from one embedded node to a federation of independently
deployed nodes without changing its contract: adding a node is a *registration + subscription*, not a new
event type or a new writer. The event set is a projection of the lifecycle, so it changes only when the
lifecycle does — and every such change is a ratified addition to this canonical list, never an ad-hoc
emission.
