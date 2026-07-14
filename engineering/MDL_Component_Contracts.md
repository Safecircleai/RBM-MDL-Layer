# MDL Component Contracts

**Status:** ENGINEERING SPECIFICATION — derived from `MDL_Internal_Architecture.md`,
`Architecture_Validation_Report.md`, and the runtime/domain/state/persistence/sequence specs. Defines the
**engineering contract** of every component: what it **Consumes**, **Produces**, **Owns**, **Cannot own**,
its **Dependencies**, **Guarantees**, and **Failure conditions**. These are behavioral contracts, **not APIs
or signatures** — no method names, no message shapes. Each component maps to one architecture layer and one
or more Core capabilities (C1–C11). Dependencies match the build DAG (`Architecture_Validation_Report.md`
§2.2) exactly — no component depends on anything downstream of it.

---

## Registry  (Layer 1 · C1)
- **Consumes:** Published Mandate Versions from Governance; read requests from Resolution/Distribution/auditors.
- **Produces:** the authoritative, retrievable set of mandate definitions by identity + version.
- **Owns:** the single authoritative store of mandate definitions.
- **Cannot own:** a second/competing mandate store; the source obligation; any determination or snapshot.
- **Dependencies:** Audit (records every write). No upstream data dependency (foundational).
- **Guarantees:** exactly one authoritative record per (mandate, version); published versions are immutable;
  no version is ever deleted; reads are consistent (monotonic — a version never disappears).
- **Failure conditions:** a write failure leaves the prior state intact (no partial version published); a read
  failure is surfaced, never substituted with a stale guess.

## Jurisdiction  (Layer 2 · C3)
- **Consumes:** a candidate set of in-force mandate versions with their layers + inheritance behaviors; the
  ratified Jurisdiction Stack.
- **Produces:** a precedence-ordered, conflict-reconciled ordering, or an `UNRESOLVED` marker + Conflict-Review
  Item.
- **Owns:** the application of the precedence stack and inheritance semantics.
- **Cannot own:** the *authoring* of the stack (ratified doctrine); ad-hoc conflict resolution.
- **Dependencies:** the ratified stack (**[BLOCKED-INPUT]** audit A1); Registry + Versioning outputs.
- **Guarantees:** deterministic ordering for identical inputs; same-level equal-date ties are flagged, never
  auto-resolved (I4).
- **Failure conditions:** if the stack is unratified it MUST refuse cross-layer resolution rather than pick an
  order; an ambiguous conflict yields `UNRESOLVED`, never a fabricated winner.

## Versioning  (Layer 3 · C2)
- **Consumes:** new-version requests from Governance; date queries from Resolution.
- **Produces:** version chains, supersession links, and "the in-force version at date D".
- **Owns:** version identity/number assignment, supersession linkage, effectivity evaluation.
- **Cannot own:** mutation or deletion of a prior version; mandate content authorship.
- **Dependencies:** Registry.
- **Guarantees:** a new version never mutates a prior version's behavior; version numbers are monotonic;
  "in-force at D" is a pure function of (chain, D).
- **Failure conditions:** concurrent version creation for one mandate resolves to one winner (optimistic
  concurrency); a failed version creation leaves the chain unchanged.

## Resolution  (Layer 4 · C4)
- **Consumes:** a Resolution Context (from Interface); definitions (Registry), in-force selection (Versioning),
  ordering (Jurisdiction).
- **Produces:** the Resolved Mandate Set (version-pinned) for the context.
- **Owns:** the deterministic computation of applicability + in-force selection + precedence into one set.
- **Cannot own:** any random/model/environment-dependent step; the entity state evaluation (that is
  Determination).
- **Dependencies:** Registry, Versioning, Jurisdiction.
- **Guarantees:** identical context + versions ⇒ identical set (I1); pins versions, never live records.
- **Failure conditions:** missing in-force version or unresolved conflict ⇒ `UNRESOLVED`/`INSUFFICIENT`, never
  a partial guess.

## Determination  (Layer 5 · C5 + C7)
- **Consumes:** the Resolved Mandate Set + the entity state (from the context).
- **Produces:** the authoritative compliance result (status + per-rule gaps) and the binding Financial-Override
  Outcome.
- **Owns:** the evaluation of entity state against mandate rules; the financial-override determination.
- **Cannot own:** discipline-specific legal reasoning; booking the economic effect or computing a tax amount;
  emitting an advisory result a consumer may ignore.
- **Dependencies:** Resolution. *(The future discipline-determination input is excluded from this path — audit
  CR-4.)*
- **Guarantees:** authoritative, not advisory (I6); deterministic and model-free (I1); financial-override
  supremacy expressed as an outcome, not an action (I3).
- **Failure conditions:** cannot evaluate on grounded versions ⇒ `INSUFFICIENT`; never fabricates compliance.

## Snapshot  (Layer 6 · C6)
- **Consumes:** the Resolved Mandate Set + Determination + governing-event identity.
- **Produces:** an immutable, version-pinned Snapshot; a stable reference.
- **Owns:** the freezing and immutable retention of determinations.
- **Cannot own:** mutation of any snapshot; the re-evaluation logic (that re-enters Determination).
- **Dependencies:** Determination, Resolution; Audit (records creation).
- **Guarantees:** write-once immutability; idempotency per governing event; reproducibility from snapshot +
  versions; isolation under propagation (I2).
- **Failure conditions:** a create failure means the determination is **unrecorded** (returned marked so);
  retry converges idempotently on one snapshot — never two.

## Override  (Layer 7 · C8)
- **Consumes:** override grants (requestor, approver, reason, expiry) bound to a Snapshot; current instant at
  read.
- **Produces:** the runtime-effective outcome (determination as overlaid by any in-force override).
- **Owns:** dual-authorization enforcement and runtime effectiveness evaluation.
- **Cannot own:** any mutation of the bound Snapshot; a stored "effective" flag; self-approval.
- **Dependencies:** Snapshot, Determination, Audit.
- **Guarantees:** requestor ≠ approver; snapshot never mutated (I2); effectiveness evaluated at read against
  the instant; expired/revoked overrides are inert.
- **Failure conditions:** approval failure leaves it Requested; expiry needs no write (derived), so cannot be
  "missed".

## Distribution  (Layer 8 · C11-propagation)
- **Consumes:** committed changes from Registry/Versioning/Snapshot/Override; Consumer Registrations.
- **Produces:** scoped Propagation Events delivered at-least-once.
- **Owns:** event publication and jurisdiction-scoped delivery; subscription matching.
- **Cannot own:** consumer-emitted events; snapshot mutation on propagation; the escalation state machine of
  any consumer (that is the Governance Supervisor's / EchoForge's — audit H-6).
- **Dependencies:** the producers whose events it forwards; Consumer Registrations.
- **Guarantees:** sole publisher (I5); publish-after-commit; per-mandate ordering; scope-bounded delivery;
  snapshot isolation.
- **Failure conditions:** undelivered events retried (outbox); duplicates expected and tolerated by consumers.

## Audit  (Layer 9 · C9)
- **Consumes:** audit events from every mutating component.
- **Produces:** the immutable, ordered, queryable trail.
- **Owns:** the append-only record of all mutations, determinations, and override acts.
- **Cannot own:** editing/deleting entries; out-of-scope PII; any determination truth (it records, it does not
  decide).
- **Dependencies:** none to exist (foundational sink); every mutating component depends on it.
- **Guarantees:** append-only, order-preserving per stream, durable-before-acknowledge.
- **Failure conditions:** if an act's audit write is not durable, the act is **not acknowledged** — there is no
  acknowledged-but-unaudited mutation.

## Governance  (Layer 10 · C10 Authoring Workflow)
- **Consumes:** an authored source obligation + provenance; role-based approvals.
- **Produces:** an approved, versioned mandate handed to Registry/Versioning.
- **Owns:** the Intake→Encode→Review→Approve workflow and its RBAC.
- **Cannot own:** the authoring of the source obligation; a non-authoring role writing a mandate; the
  supervision of bots (that is the external Governance Supervisor).
- **Dependencies:** Registry, Versioning, Audit; **the defined authoring/ops roles** (**[BLOCKED-INPUT]** audit
  CR-2).
- **Guarantees:** compile-not-legislate (I8); role-gated writes; every step audited; no partial publish.
- **Failure conditions:** a failure before publish leaves an Authoring Work Item to resume; no half-published
  mandate; cannot verify *authority to author* until delegation/lineage exist (audit CR-3 cluster).

## Interfaces  (Layer 11 · C11-request + supervision boundary)
- **Consumes:** consumer determination/read requests; the Governance Supervisor's read/subscribe.
- **Produces:** determinations and reads scoped to the caller's least-privilege projection; the read-only
  supervision boundary.
- **Owns:** authentication, scoping, and projection enforcement at the edge.
- **Cannot own:** granting more than least-privilege; giving the Supervisor write/disable; implementing the
  Supervisor's escalation logic.
- **Dependencies:** the capabilities it fronts (Resolution, Determination, Snapshot, Override, Registry read).
- **Guarantees:** least-privilege projections (I10); read-only supervision (I7); a consumer reads only its own
  entities and in-scope mandates.
- **Failure conditions:** an unauthorized/over-scope request is refused, not narrowed silently; the admin
  projection is unavailable until the ops role is defined (audit CR-2).

---

## Contract-level consistency checks (the guarantees that must hold across components)

1. **No component depends on a downstream component** — the dependency lists above form the acyclic build DAG
   (`Architecture_Validation_Report.md` §2.2). Verified: Registry/Audit foundational; each other component
   depends only on those to its left.
2. **Every mutating component depends on Audit** — there is exactly one path to an acknowledged mutation, and
   it passes through a durable audit write.
3. **Exactly one component owns each truth** — Registry owns definitions, Versioning owns version facts,
   Jurisdiction owns precedence application, Resolution owns the applicable set, Determination owns the
   result + financial-override, Snapshot owns the frozen record, Override owns the runtime overlay, Distribution
   owns events, Audit owns the trail, Governance owns the authoring workflow, Interfaces own edge access. **No
   two components own the same truth** (the CR-1 "Validation/Enforcement" duplicate is a matrix label, not a
   second component — validation §2.3).
4. **No component crosses a constitutional boundary** — none authors a source obligation, executes a business
   or economic act, books money, scores risk, performs discipline reasoning, or supervises bots. Each
   "Cannot own" line above is the boundary made contractual.
5. **Three contracts carry a ratified-input dependency, not a design choice** — Jurisdiction (stack),
   Governance + Interfaces (ops roles). These are supplied to the component as ratified doctrine; the component
   is otherwise fully specified by its contract above.
