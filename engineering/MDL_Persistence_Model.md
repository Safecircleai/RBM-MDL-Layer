# MDL Persistence Model

**Status:** ENGINEERING SPECIFICATION — derived from `MDL_Infrastructure_Constitution.md` §5–§6,
`MDL_Domain_Model.md`, and `Architecture_Validation_Report.md`. Describes the **persistence semantics** of
every domain object — what is immutable, append-only, mutable, derived, projected, or reconstructed — plus
retention, historical preservation, and snapshot guarantees. **No database design, no schema, no storage
engine.** These are semantic classifications an engineer maps onto whatever store is chosen.

---

## 1. The six persistence classes

| Class | Meaning | Write rule |
|---|---|---|
| **Immutable** | Once created, content never changes. | Write-once; edits forbidden. |
| **Append-only** | A stream to which entries are only added, never edited/removed. | Append; order-preserving. |
| **Mutable** | May change in place, under governed transitions. | Update under state rules + audit. |
| **Derived** | Computed from other durable data; not itself a source of truth. | Recompute; never authored. |
| **Projected** | A read-model shaped for a consumer; a view over source truth. | Rebuildable from source. |
| **Reconstructed** | Recoverable in full by replaying immutable/append-only sources. | No independent authority. |

---

## 2. Classification of every domain object

| Object | Class | Notes |
|---|---|---|
| **Mandate** (identity) | Mutable (head pointer only) | Identity immutable; only its current-head pointer and derived active posture move. Never deleted. |
| **Mandate Version** | **Immutable from Published**; Mutable only in Draft→Approved (pre-publish) | Content frozen at Publish (I2). Pre-publish drafts are mutable work-in-progress. |
| **Rule Set / Applicability / Effectivity Window** | **Immutable from Published** | Bound to a version; frozen with it. |
| **Jurisdiction Layer / Stack** | Immutable (config-as-doctrine) | Changes only by constitutional amendment; runtime treats as read-only. |
| **Resolution Context** | Transient (not persisted as truth) | Held only for the request; its content is *captured into the Snapshot*. |
| **Resolved Mandate Set** | **Derived / transient** | Recomputed from Registry+Versioning+Jurisdiction; frozen into the Snapshot, never stored separately as truth. |
| **Determination (Validation Result)** | **Immutable** (once Snapshotted) | Frozen inside/alongside its Snapshot; a re-evaluation is a new record. |
| **Financial-Override Outcome** | **Immutable** (part of the Determination/Snapshot) | Never recomputed against a live record. |
| **Snapshot** | **Immutable + retained forever** | The anchor of record; the heaviest persistence. |
| **Override (grant)** | **Mutable status over immutable core** | Bound Snapshot ref, requestor, approver, reason, expiry are immutable; only status (Active→Revoked) and revocation stamp move. |
| **Audit Event** | **Append-only + immutable** | Never edited or deleted. |
| **Propagation Event** | **Append-only** (delivery log/outbox) | Emitted after commit; retained per delivery policy. |
| **Consumer Registration** | Mutable | Scope/subscription/projection may change; changes audited. |
| **Conflict-Review Item** | Mutable status over immutable conflict facts | The conflicting versions + context are immutable; review status moves. |
| **Authoring Work Item** | Mutable (pre-publish) | Discarded/settled once it produces a Published version. |
| **Latest Validation Status (per entity)** | **Derived / Projected** | The most recent Determination for an entity; a read-model over Snapshots, not a new truth. |

---

## 3. What is immutable (the frozen core)

The following are **write-once and never altered** — they are the constitutional guarantees made physical:
- **Published Mandate Versions** and their Rule Set / Applicability / Effectivity (I2).
- **Snapshots** — every field, forever (I2).
- **Determinations and Financial-Override Outcomes** once Snapshotted.
- **Audit Events**.

A store that permits in-place edit of any of these violates the constitution regardless of its convenience.
The immutability is enforced at write time (write-once), not by policy or review.

## 4. What is append-only

- The **Audit trail** — the ordered record of all mutations/determinations/overrides.
- The **Snapshot store** — snapshots are only added, never modified or removed.
- **Version chains** — a new version is appended and linked; prior versions stay.
- The **Propagation/outbox log** — events appended after commit for reliable delivery.

Append-only stores grow monotonically; §7 covers the retention pressure this creates.

## 5. What is mutable (under governed transitions + audit)

- **Pre-publish Authoring Work Items / Draft versions** (Draft→Reviewed→Approved).
- **Override status** (Active→Revoked) — the *only* mutable field on an otherwise immutable override.
- **Consumer Registrations** (scope/subscription/projection).
- **Conflict-Review status**.
- A **Mandate's head pointer** (advances as versions publish).

Every mutation appends an Audit Event; there is no un-audited write anywhere in the system.

## 6. What is derived, projected, and reconstructed

- **Derived:** the Resolved Mandate Set; "the in-force version at date D"; a Mandate's active posture; the
  latest validation status per entity. None is a source of truth; each is recomputed from immutable sources.
- **Projected:** per-consumer least-privilege read-models (a consumer's own snapshots/results, scoped
  mandates) and aggregate metrics for Intelligence consumers. Projections are rebuildable and hold no
  authority; deleting a projection loses nothing but a cache.
- **Reconstructed:** **any Determination is fully reproducible from its Snapshot + the pinned Mandate
  Versions** — this is the reproducibility guarantee. The entire "current compliance state" of the ecosystem
  is reconstructable by replaying determinations; no derived state is authoritative on its own.

**Consequence:** the *only* things that must survive to preserve truth are the immutable + append-only stores
(§3, §4). Everything else can be dropped and rebuilt. A recovery/rebuild plan therefore needs only those.

## 7. Retention & historical preservation

- **Mandates, versions, snapshots, and audit events are retained indefinitely** — never deleted
  (`MDL_Lifecycle.md` §5). Retirement/supersession are lifecycle states, not deletions.
- **Historical preservation** is achieved by the combination of: immutable version chains (the definition
  history), immutable snapshots (the determination history), and the append-only audit trail (the act
  history). Together they answer "what did the mandate say, and what did we determine, at any past moment"
  without any mutable record.
- **[OPEN — audit H-8, not decided here]** Unbounded never-delete retention with entity attributes frozen in
  snapshots creates (a) monotonic storage growth and (b) tension with data-erasure law. This spec **records**
  the constraint and does **not** resolve it (resolving it would be new doctrine). An implementer MUST treat
  retention tiering / cryptographic erasure of *entity attributes within snapshots* as a **ratified-input
  decision**, because the constitution currently forbids trading immutability for storage relief
  (`Architectural_Constraints.md` §3). Until ratified, the runtime retains everything.

## 8. Snapshot guarantees (restated as persistence requirements)

An implementation MUST provide, for every Snapshot:
1. **Write-once immutability** — no field is ever altered after creation.
2. **Version-pinning** — it references specific Mandate Version identities; a later version never changes what
   it pinned.
3. **Idempotency per governing event** — the same governing event yields exactly one Snapshot; concurrent or
   retried creation converges on it.
4. **Reproducibility** — the Determination it froze is recomputable from it + the pinned versions, yielding
   an identical result.
5. **Isolation under propagation** — a mandate update propagating to consumers never touches any existing
   Snapshot.
6. **Indefinite retention** — it is never deleted or expired (subject to the §7 open item).

## 9. Consistency & durability expectations

- **Publish-after-commit:** a Propagation Event or a returned "recorded" determination is emitted/returned
  only after the underlying immutable write is durable — consumers never observe truth that did not persist.
- **Read-your-writes for the authoring authority** on its own drafts; **monotonic reads** for consumers over
  published versions (a consumer never sees a version disappear).
- **Audit durability precedes acknowledgement:** an act is acknowledged only once its Audit Event is durable;
  there is no acknowledged-but-unaudited mutation.
