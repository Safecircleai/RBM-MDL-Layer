# MDL Domain Model

**Status:** ENGINEERING SPECIFICATION — derived from `MDL_Infrastructure_Constitution.md` §4–§6 and
`Architecture_Validation_Report.md`. Defines every permanent domain object **conceptually** — no schemas, no
types, no storage. "Fields" are named concepts, not columns. Introduces no object beyond those the
constitution and validation already require.

For each object: **purpose · owner · lifecycle · immutable fields · mutable fields · relationships ·
invariants.** All objects are owned by the **MDL domain** unless stated; "owner" here names the responsible
domain, not a runtime.

---

## 1. Mandate
- **Purpose:** the durable identity of an obligation the MDL compiles and governs across its versions.
- **Owner:** MDL domain (the *encoded* mandate); the *source obligation* is the Mandate Authoring Authority's.
- **Lifecycle:** created at first authoring; lives as long as any version exists; never deleted.
- **Immutable fields:** mandate identity; the authoring-authority attribution of origin.
- **Mutable fields:** the pointer to its current head version (advances on new version); active/inactive
  posture (derived from its versions' states).
- **Relationships:** one Mandate has many **Mandate Versions**; belongs to one **Jurisdiction Layer** family;
  may link to a superseded/parent Mandate.
- **Invariants:** exactly one authoritative Mandate per identity; a Mandate always has at least one Version
  once it exists; a Mandate is never deleted (only its versions retire/supersede).

## 2. Mandate Version
- **Purpose:** the concrete, versioned content of a mandate at a point in its evolution — the unit that is
  resolved and pinned into snapshots.
- **Owner:** MDL domain.
- **Lifecycle:** Draft → Reviewed → Approved → Published → Effective → (Superseded | Retired) → Archived
  (`MDL_State_Model.md`).
- **Immutable fields (once Published):** version identity; version number; jurisdiction layer; inheritance
  behavior (FLOOR/ADDITIVE/OVERRIDE); the Rule Set content; the Applicability; the Effectivity Window; the
  supersession link to the version it replaces; authoring-authority attribution.
- **Mutable fields:** lifecycle state only (advances forward; never backward past Published); the
  superseded-by pointer (set once when a later version supersedes it).
- **Relationships:** belongs to one **Mandate**; carries one **Rule Set**, one **Applicability**, one
  **Effectivity Window**, one **Jurisdiction Layer**; is referenced (pinned) by many **Snapshots**.
- **Invariants:** **content is immutable after Publish** (I2) — a change is a *new* version, never an edit; a
  published version is never deleted (snapshots reference it); version numbers are monotonic within a Mandate.

## 3. Rule Set
- **Purpose:** the structured obligations a mandate version imposes — the evaluable content.
- **Owner:** MDL domain (encoding); source authored externally.
- **Lifecycle:** bound to its Mandate Version; immutable once the version is Published.
- **Immutable fields (once Published):** the rule categories the version carries — document requirements,
  evidence requirements, threshold rules, participation rules, and financial policy. *(These categories are
  those already named in the Constitution §4; no new category is introduced.)*
- **Mutable fields:** none once Published (a change is a new version).
- **Relationships:** one Rule Set per Mandate Version; each rule is evaluated by the Determination component.
- **Invariants:** rules are declarative and data-driven, never hardcoded per node; a financial-policy rule is
  the *only* rule that yields a binding financial-override outcome; ceiling/coherence guards hold at Review.

## 4. Jurisdiction Layer
- **Purpose:** the altitude at which a mandate version applies (its position in the precedence stack).
- **Owner:** MDL domain (the stack is ratified doctrine).
- **Lifecycle:** a fixed, ratified enumeration; changes only by constitutional amendment.
- **Immutable fields:** the layer identity and its precedence rank within the ratified stack.
- **Mutable fields:** none at runtime.
- **Relationships:** a Mandate Version has exactly one Jurisdiction Layer; the **Jurisdiction Stack** orders
  all layers.
- **Invariants:** precedence is total and explicit; **RATIFIED (R2)** — the canonical ordering is the
  FEDERAL-anchored two-class stack (`../MDL_Lifecycle.md` §4); jurisdiction resolution is deterministic over it.

## 5. Jurisdiction Stack
- **Purpose:** the total precedence order + conflict-resolution rules across all Jurisdiction Layers.
- **Owner:** MDL domain (ratified doctrine).
- **Lifecycle:** near-immutable config; amended only constitutionally.
- **Immutable fields:** the ordered layer list; the conflict rules (higher precedence wins → newer effective
  date → flag for review).
- **Mutable fields:** none at runtime.
- **Relationships:** governs every Resolution.
- **Invariants:** deterministic; same-level equal-date conflicts are flagged, never auto-resolved (I4).

## 6. Effectivity Window
- **Purpose:** the time interval in which a mandate version is in force.
- **Owner:** MDL domain.
- **Lifecycle:** set at authoring; immutable once Published.
- **Immutable fields:** effective-from; sunset/effective-to (may be open-ended).
- **Mutable fields:** none (a change is a new version).
- **Relationships:** one per Mandate Version; consulted by Resolution and by the Published→Effective and
  →Retired state transitions.
- **Invariants:** "in force at date D" is a pure function of (window, D); publication may precede effectivity.

## 7. Applicability
- **Purpose:** the declarative conditions under which a mandate version applies to an entity.
- **Owner:** MDL domain.
- **Lifecycle:** bound to its version; immutable once Published.
- **Immutable fields:** the entity type(s), optional service type(s), and node type(s) the version targets.
- **Mutable fields:** none.
- **Relationships:** one per Mandate Version; matched against the Resolution Context.
- **Invariants:** declarative and evaluated against supplied context; never a hardcoded per-node exclusion.

## 8. Resolution Context
- **Purpose:** the input describing the entity and moment for which mandates are resolved.
- **Owner:** supplied by the **consuming node** (an input, not MDL-owned truth).
- **Lifecycle:** transient — exists for one determination request.
- **Immutable fields (for that request):** node type; entity type; optional service type; jurisdiction;
  `as_of` date; entity attributes; the governing-event identity (for snapshot idempotency).
- **Mutable fields:** none (a new request is a new context).
- **Relationships:** consumed by Resolution; carried into the Snapshot as the frozen input.
- **Invariants:** determinations are pure functions of this context + in-force versions; the runtime never
  substitutes "now" for the supplied `as_of` (I1).

## 9. Resolved Mandate Set
- **Purpose:** the applicable, in-force, precedence-ordered set of mandate versions for a Resolution Context.
- **Owner:** MDL domain (transient derivation).
- **Lifecycle:** transient — produced by Resolution, consumed by Determination, frozen into the Snapshot.
- **Immutable fields:** the ordered list of pinned Mandate Versions; any unresolved-conflict marker.
- **Mutable fields:** none.
- **Relationships:** derived from Registry + Versioning + Jurisdiction; input to Determination; captured in
  the Snapshot.
- **Invariants:** deterministic for identical context + versions; contains version-pinned references, never
  live mandate pointers.

## 10. Determination (Validation Result)
- **Purpose:** the authoritative result of evaluating entity state against the Resolved Mandate Set —
  compliance status, per-rule gaps, and the binding financial-override outcome.
- **Owner:** MDL domain.
- **Lifecycle:** produced once per governing event; frozen immediately into a Snapshot; never edited.
- **Immutable fields:** overall compliance status; per-rule gaps (missing documents/evidence, threshold
  blocks, participation gaps, missing certifications); the Financial-Override Outcome; the Snapshot reference;
  the Mandate Version identities relied upon.
- **Mutable fields:** none (a re-evaluation produces a *new* Determination + Snapshot).
- **Relationships:** references one **Snapshot** and many **Mandate Versions**; may be overlaid at runtime by
  an **Override** (which changes the *runtime outcome*, not this record).
- **Invariants:** authoritative, not advisory (I6); reproducible from its Snapshot + versions; a Determination
  without a Snapshot is inadmissible (Constitution §1.4).

## 11. Financial-Override Outcome
- **Purpose:** the binding financial policy determination (e.g. tax-exemption) that a consuming Economic actor
  must honor.
- **Owner:** MDL domain (the determination); the Economic Consumer books the effect.
- **Lifecycle:** computed within a Determination; frozen in its Snapshot.
- **Immutable fields:** the outcome (e.g. exempt / not-exempt); the deciding Mandate Version; the reason.
- **Mutable fields:** none.
- **Relationships:** part of a Determination; consumed by the Economic Consumer.
- **Invariants:** supreme over a node's tax engine (I3); MDL never computes the tax *amount* or books it
  (I9).

## 12. Snapshot
- **Purpose:** the immutable, version-pinned freeze of a Determination and the configuration that produced it
  — the audit artifact and the anchor for reproducibility and overrides.
- **Owner:** MDL domain.
- **Lifecycle:** created once per governing event; immutable forever; retained indefinitely.
- **Immutable fields (all):** the governing-event identity; the frozen Resolution Context; the pinned Mandate
  Version identities; the frozen Rule Set content applied; the Determination result; the Financial-Override
  Outcome; the creation timestamp.
- **Mutable fields:** **none, ever** (I2).
- **Relationships:** references the Mandate Versions and the Determination it froze; referenced by any
  **Override**; read by Auditors, consumers, the Supervisor.
- **Invariants:** never mutated; version-pinned (a later version never alters it); idempotent per governing
  event; a validation result references *it*, never a live record.

## 13. Override (Exception Grant)
- **Purpose:** a dual-authorized, expiring exception that modifies the *runtime outcome* for a non-compliant
  determination without mutating its Snapshot.
- **Owner:** MDL domain (evaluates it); requestor + approver author the grant.
- **Lifecycle:** Requested → Approved → Active → (Expired | Revoked) (`MDL_State_Model.md`).
- **Immutable fields:** the bound Snapshot reference; the requestor identity; the approver identity; the
  reason; the expiry; the creation timestamp.
- **Mutable fields:** status (Active → Revoked); the revocation timestamp/actor (set once, on revoke).
- **Relationships:** references exactly one **Snapshot**; overlays one Determination's runtime outcome.
- **Invariants:** requestor ≠ approver; never mutates the Snapshot; effectiveness is evaluated at read time
  against the current instant (never stored as an effective flag); expired/revoked overrides are inert.

## 14. Audit Event
- **Purpose:** the immutable record of a single mutation, determination, or override act.
- **Owner:** MDL domain.
- **Lifecycle:** appended once; never edited or deleted.
- **Immutable fields (all):** the acting identity; the act; the affected object reference; the timestamp; the
  ordering position within its stream.
- **Mutable fields:** none.
- **Relationships:** references the object it records; read by Auditors, Supervisor, Intelligence (aggregate).
- **Invariants:** append-only; order-preserving per stream; no out-of-scope PII.

## 15. Propagation Event
- **Purpose:** the scoped, published notice of a mandate-domain change consumers subscribe to.
- **Owner:** MDL domain (sole publisher).
- **Lifecycle:** emitted after the change commits; delivered at-least-once.
- **Immutable fields:** the event identity; the event kind (mandate created/versioned/updated, snapshot
  created, validation recorded, override created/approved/revoked); the affected reference; the jurisdiction
  scope; the timestamp.
- **Mutable fields:** none.
- **Relationships:** derived from a committed change; delivered to matching Consumer Registrations.
- **Invariants:** published only by MDL; scoped by jurisdiction; carries a stable identity for consumer
  deduplication; never mutates a snapshot on receipt.

## 16. Consumer Registration
- **Purpose:** a node's declaration of who it is and what scope it subscribes to.
- **Owner:** the consuming node declares it; MDL holds it.
- **Lifecycle:** created on registration; updated on scope change; removed on deregistration.
- **Immutable fields:** the node identity.
- **Mutable fields:** node type; jurisdiction scope; subscription set; least-privilege projection grant.
- **Relationships:** governs which Propagation Events reach the node and which projection it may read.
- **Invariants:** a node reads/receives only within its declared scope (I10); publish/admin are guarded, not
  default.

## 17. Conflict-Review Item
- **Purpose:** a first-class record of a same-level, equal-date jurisdiction conflict that MUST NOT
  auto-resolve.
- **Owner:** MDL domain.
- **Lifecycle:** Flagged → Under Review → (Resolved | Escalated).
- **Immutable fields:** the conflicting Mandate Versions; the Resolution Context that surfaced it; the
  timestamp.
- **Mutable fields:** review status; the resolution decision (a ratified ordering or an escalation).
- **Relationships:** references the conflicting versions; blocks a deterministic resolution for that context
  until resolved.
- **Invariants:** never auto-resolved (I4); its resolution is a human/ratified act, recorded in Audit.

## 18. Authoring Work Item
- **Purpose:** the in-flight state of a mandate moving through the authoring workflow before Publish.
- **Owner:** MDL domain (workflow); the source is the Authoring Authority's.
- **Lifecycle:** Intake → Encode → Review → Approve → (produces a Published Mandate Version).
- **Immutable fields:** the intake identity; the source-authority attribution.
- **Mutable fields:** the encoded draft content; the workflow state; review/approval records.
- **Relationships:** produces one **Mandate Version** on approval; appends to Audit at each step.
- **Invariants:** never publishes without the required role approval (**RATIFIED R3** — Governance
  Reviewer approves, Governance Publisher publishes, Author cannot self-approve; `../MDL_Consumer_Model.md`
  §1a); never authors the source obligation itself.

---

## Relationship summary (object graph, conceptual)

```
Mandate ──1:N── Mandate Version ──1:1── {Rule Set, Applicability, Effectivity Window, Jurisdiction Layer}
Jurisdiction Layer ──ordered by── Jurisdiction Stack
Resolution Context ──drives── Resolved Mandate Set ──pins── Mandate Version(s)
Resolved Mandate Set ──input to── Determination ──contains── Financial-Override Outcome
Determination ──frozen into── Snapshot ──referenced by── Override
every mutation/determination/override ──appends── Audit Event
every committed change ──emits── Propagation Event ──matched to── Consumer Registration
same-level conflict ──raises── Conflict-Review Item
Authoring Work Item ──produces── Mandate Version
```

No object here exists that a Core capability (C1–C11) does not already require; no relationship crosses a
constitutional boundary (source authorship, economic execution, and business action remain outside).
