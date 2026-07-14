# MDL Runtime Specification

**Status:** ENGINEERING SPECIFICATION — derived directly from `MDL_Infrastructure_Constitution.md` and
`Architecture_Validation_Report.md`. Not doctrine. Describes **runtime behavior only** — no APIs, no code,
no schemas. Introduces no capability beyond the eleven Core capabilities and changes no constitutional
boundary. Where a behavior depends on an unratified input, it is marked **[BLOCKED-INPUT]** rather than
decided here.

**Traceability:** every section cites the capability (C1–C11 from the validation) and invariant (I1–I10
from `Architectural_Constraints.md`) it implements.

---

## 1. Runtime responsibilities

The MDL runtime has exactly these responsibilities and no others:

1. **Hold** the authoritative, versioned mandate definitions (C1 Registry).
2. **Resolve** — deterministically compute which mandates apply to an entity context (C2 Versioning, C3
   Jurisdiction, C4 Resolution).
3. **Determine** — evaluate entity state against the resolved set and produce the authoritative compliance
   result and the binding financial-override outcome (C5 Determination, C7 Financial-Override).
4. **Freeze** — capture each determination as an immutable, version-pinned snapshot (C6 Snapshot).
5. **Evaluate exceptions** — apply dual-authorized, expiring overrides to the runtime outcome without
   mutating the snapshot (C8 Override).
6. **Record** — append every mutation, determination, and override to the immutable audit trail (C9 Audit).
7. **Publish** — emit scoped mandate-domain events to subscribers (C11 Distribution).
8. **Admit** — run the role-based authoring workflow that compiles authored obligations into mandates (C10
   Governance/Authoring).
9. **Serve** — expose least-privilege read/request projections to consumers and a read-only boundary to the
   Governance Supervisor (C11 Interface).

The runtime **does not**: author source obligations, execute a business or economic action, book money,
score risk, perform discipline legal reasoning, or supervise bots. It *determines*; consumers *act*; the
Governance Supervisor *observes* (I8, I9).

---

## 2. Runtime execution flow (the request pipeline)

A consumer determination request traverses the pipeline exactly once, left to right, with no back-edges
(the acyclic pipeline confirmed in `Architecture_Validation_Report.md` §2.1):

```
Interface (authenticate, scope to least-privilege projection)
  → Resolution  (uses Registry + Versioning + Jurisdiction to compute the applicable, in-force,
                 precedence-ordered mandate set for the supplied entity context)
  → Determination (+ Financial-Override) (evaluates entity state against the resolved set)
  → Snapshot (freezes the resolved configuration + result, version-pinned, idempotent per governing event)
  → Override (applies any in-force override to the runtime outcome; snapshot unchanged)
  → Interface (returns the runtime outcome to the consumer)
  ⟿ Audit (records the determination)     ⟿ Distribution (emits the determination event)
```

Audit and Distribution are **side effects** taken after the outcome is produced; they never alter the
determination and never sit on the return path's critical section.

---

## 3. Deterministic execution path (I1)

**Scope of the deterministic path:** Resolution (C4) → Jurisdiction (C3) → Versioning selection (C2) →
Determination (C5) → Financial-Override (C7) → Snapshot freezing (C6). Every step in this scope MUST behave
as a **pure function of its persisted inputs and the supplied entity context**.

Rules the runtime MUST enforce on the deterministic path:
- **No wall-clock read** except the single sanctioned exception in §7 (override expiry, which is off the
  snapshot). Effective-date logic uses the `as_of` date carried in the resolution context, never "now".
- **No randomness, no environment-derived value, no external network call** in resolution or determination.
  (The *future* discipline-determination consumption — C5 note, audit CR-4 — would violate this; it is not
  part of the Core runtime and MUST NOT be added to this path without resolving that contradiction.)
- **Reproducibility:** identical (entity context, persisted mandate versions) MUST yield an identical
  resolved set, determination, and snapshot content. A consumer or auditor replaying the same inputs against
  the same versions gets the same snapshot.
- **RATIFIED (R2):** Jurisdiction precedence (C3) uses the ratified FEDERAL-anchored two-class stack
  (`MDL_Lifecycle.md` §4). Deterministic across the ratified order; the runtime refuses only an *unranked*
  layer (one not present in the stack), never picks an order.

Off-path (may vary in timing, never in truth): Audit append order timing, Distribution delivery timing,
Authoring human steps, Interface routing.

---

## 4. Authoring path (the write path — C10)

The authoring path is **physically and logically separate** from the read/determination path (a consumer
request can never enter it — validation §2.1, I8/I10). Its runtime behavior:

1. **Intake** — an authored source obligation is received with its authoring-authority attribution.
2. **Encode** — it is compiled into a structured mandate (jurisdiction layer, applicability, rule sets,
   effectivity). Encoding is data-driven, never hardcoded per node.
3. **Review** — a conformance check (schema-shape validity, precedence coherence, ceiling guards) runs; it
   validates the *encoding*, never the *source*.
4. **Approve** — a role-based approval admits the mandate. **RATIFIED (R3):** the actors are the Governance
   Reviewer (reviews/approves) and Governance Publisher (publishes); the Author cannot approve or publish its
   own draft (separation of duties, `MDL_Consumer_Model.md` §1a).
5. **Version** — a version is assigned; supersession is linked; prior versions are untouched.
6. **Publish** — the version becomes resolvable within its effective window.

Every step appends to Audit (C9). The path is human-in-the-loop and need not be deterministic. It MUST never
author a source obligation itself, and never permit a non-authoring role to write a mandate.

---

## 5. Read path (C11 Interface)

The read path serves determinations and reads. Its runtime behavior:
- Every request is **authenticated and scoped** to the caller's least-privilege projection (I10). A consumer
  reads only its own entities' snapshots/results and only the mandates in its jurisdiction scope.
- **Determination requests** (resolve / validate / financial-policy) run the pipeline (§2) and return the
  runtime outcome.
- **Status/snapshot reads** return persisted, immutable snapshots and the latest validation status —
  lock-free (the artifacts are immutable).
- The **Governance Supervisor** reads mandates, validation outputs, override logs, and version changes over a
  **read-only** boundary and MUST NOT be able to drive a determination, write, or disable enforcement (I7).
  The runtime exposes read + subscribe to it; it implements **none** of the Supervisor's escalation state
  machine (that is EchoForge's — audit H-6).

---

## 6. Propagation path (C11 Distribution)

- The runtime is the **sole publisher** of mandate-domain events (I5 corollary). No consumer emits them.
- Events are emitted **after** the truth they describe is durably recorded (publish-after-commit), so a
  consumer never sees an event for a change that did not persist.
- Propagation is **scoped by jurisdiction**: a Federal-layer change reaches all subscribers; a State-layer
  change reaches subscribers registered in that state; a Prime/Program change reaches associated entities
  only. A subscriber never receives events outside its declared scope.
- Delivery is **at-least-once**; ordering is guaranteed **per mandate** (a version event never overtakes the
  create event for the same mandate), not globally.
- Propagation **never mutates a snapshot**: a subscriber updating to a new version applies it to *future*
  resolutions only (snapshot isolation, I2).

---

## 7. Failure boundaries

The runtime fails **closed and honest**, never open and guessing:
- **Determination integrity first.** If resolution or determination cannot be completed with grounded,
  in-force versions, the runtime returns an explicit non-result (`UNRESOLVED` / `INSUFFICIENT`), never a
  fabricated "compliant". A determination that cannot name its snapshot and versions is inadmissible
  (Constitution §1.4).
- **The runtime never acts on a failure.** Because MDL executes nothing (I9), a failure is expressed *as a
  determination outcome* returned to the consumer; the consumer decides what to do. MDL never blocks, books,
  or moves anything itself.
- **Write-path failures are isolated from truth.** An authoring failure leaves the Registry unchanged (no
  partial mandate is published); a Snapshot write failure means the determination is *not* recorded and the
  consumer is told the determination is unrecorded — it is never returned as recorded.
- **Sanctioned time-dependence (the one wall-clock exception):** an override's effectiveness is evaluated
  against the current instant (its expiry). This affects only the **runtime outcome**, never the immutable
  snapshot. "Identical context → identical result" therefore holds for a fixed evaluation instant; across
  time only the override overlay may change (audit M-... / validation C8).
- **Same-level unresolved conflict** is a first-class outcome, not a failure: resolution returns
  `UNRESOLVED` and raises a Conflict-Review item; it MUST NOT auto-pick (I4).

---

## 8. Retry boundaries

- **Safe to retry (idempotent):** any read; resolution; determination; snapshot creation for a governing
  event (§9); event *consumption* (consumers dedupe by event identity).
- **Not safe to blind-retry (require idempotency key or state check):** authoring approval (a second approval
  is a distinct act, not a retry); override grant/approval (dual-authorization, each a distinct actor act);
  version creation (retry only under the same idempotency intent, else it creates a spurious version).
- **Propagation retries** are expected (at-least-once); consumers MUST tolerate duplicate delivery.
- A retried determination MUST return the *same* snapshot as the first attempt for the same governing event —
  never a second snapshot (§9).

---

## 9. Idempotency expectations

- **Snapshot creation is idempotent per governing event.** A governing event (e.g. a specific submission /
  approval / award for a specific entity) has a stable identity; creating a snapshot for it twice yields the
  *same* snapshot, not two. This is the load-bearing idempotency guarantee (C6; Constitution §6.2).
- **Resolution and determination are naturally idempotent** (pure functions of persisted inputs + context).
- **Authoring is not idempotent** by nature (each approval/version is a deliberate, audited act); idempotency
  there is intent-scoped, not automatic.
- **Events carry a stable identity**; consumers achieve exactly-once *effect* by deduplicating on it.

---

## 10. Concurrency expectations

- **Registry / Versioning writes are serialized per mandate.** Two concurrent new-version requests for the
  same mandate MUST NOT both succeed silently; one wins and the other observes the new head (optimistic
  concurrency on the version chain). Different mandates proceed concurrently.
- **Snapshot creation is safe under concurrency** via the governing-event idempotency key: concurrent
  attempts for the same governing event converge on one snapshot.
- **Determinations are read-mostly and lock-free** over immutable versions and snapshots; a version change
  concurrent with a determination does not affect the in-flight determination (it resolved against the
  versions in force at its `as_of`).
- **Overrides require two distinct actors** (requestor ≠ approver); the runtime MUST reject a
  self-approval and MUST evaluate override effectiveness at read time, never cache it as a stored effective
  flag.
- **Audit append is concurrency-safe and total-order-preserving per stream**; it never blocks the
  determination path (append is a side effect, §2).
- **Reads never block writes and writes never block reads of prior immutable artifacts** — because the truths
  consumers read (published versions, snapshots) are immutable once visible.

---

## 11. What this specification does not decide (required inputs)

**RATIFICATION UPDATE — 2026-07-14 (`Ratification_Log.md`).** Three of the four inputs below are now
**RATIFIED** and are supplied to the runtime; the `[BLOCKED-INPUT]` markers earlier in this document are
lifted accordingly:
- The **canonical jurisdiction precedence stack** — **RATIFIED (R2):** the FEDERAL-anchored two-class model
  (`MDL_Lifecycle.md` §4). Deterministic resolution (§3) is now unblocked; the runtime resolves across the
  ratified stack and refuses only an *unranked* layer.
- The **authoring roles** — **RATIFIED (R3):** HRA + Governance Author / Reviewer / Publisher, separation of
  duties, no generic "Operators" (`MDL_Consumer_Model.md` §1a). The authoring path (§4) and admin projection
  (§5) use these roles.
- The **revocation / void-ab-initio semantics** — **RATIFIED (R4):** `MDL_Revocation_And_Invalidation.md`
  (append-only invalidation overlay; nothing deleted). The runtime now supports Void in addition to
  Supersede/Sunset/Retire.

Still an open input, not decided here:
- Whether and how the runtime may ever consume a discipline determination (audit CR-4) — excluded from the
  deterministic path here.
- The **detection** of invalid authority (delegation / authority-lineage) — R4 ratified the *remediation*; the
  detection trigger remains a ratified HRA finding until the lineage model is ratified.

An engineer implements everything else directly from §§1–10.
