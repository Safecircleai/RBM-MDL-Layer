# MDL State Model

**Status:** ENGINEERING SPECIFICATION — derived from `MDL_Lifecycle.md`, `MDL_Domain_Model.md`, and
`Architecture_Validation_Report.md`. Defines every state machine, its legal transitions, invariants, illegal
transitions, and recovery behavior. No new state is invented beyond the lifecycle stages already in doctrine.

Four objects have runtime state machines: **Mandate Version**, **Override**, **Determination**, and
**Conflict-Review Item**. All other objects are either immutable-on-creation (Snapshot, Audit Event,
Propagation Event) or simple mutable records (Consumer Registration) with no meaningful lifecycle.

---

## 1. Mandate Version state machine

Maps the Definition lifecycle (`MDL_Lifecycle.md` §1) onto states. The example chain in the brief is adopted
verbatim; "Draft" and "Effective" name the Encode-output and effectivity-active conditions the lifecycle
already describes.

```
Draft → Reviewed → Approved → Published → Effective → ┬→ Superseded → Archived
                                                       └→ Retired    → Archived
```

**States:**
- **Draft** — encoded, not yet reviewed. Not resolvable.
- **Reviewed** — passed conformance review (schema-shape, precedence coherence, ceiling guards). Not
  resolvable.
- **Approved** — admitted by the required authoring role. **[BLOCKED-INPUT]** roles undefined (audit CR-2).
  Not yet resolvable.
- **Published** — version assigned; content frozen; resolvable **within its effective window**.
- **Effective** — the current date is inside the effective window; actively applies to new resolutions.
- **Superseded** — a later version has replaced it for future resolutions; historical snapshots keep pinning
  it.
- **Retired** — its effective window has closed (sunset); it stops applying to new resolutions.
- **Archived** — retained immutably for oversight; terminal.

**Legal transitions:**
| From | To | Trigger |
|---|---|---|
| Draft | Reviewed | conformance review passes |
| Reviewed | Approved | required-role approval |
| Approved | Published | version assigned + made available |
| Published | Effective | current date enters the effective window |
| Published | Retired | sunset before ever becoming effective (window closed early) |
| Effective | Superseded | a newer version is published that replaces it |
| Effective | Retired | effective window closes (sunset) |
| Superseded | Archived | retention step |
| Retired | Archived | retention step |

**State invariants:**
- Content is **immutable from Published onward** (I2); any change is a *new* Mandate Version.
- Only one version of a Mandate is **Effective** for a given (jurisdiction layer, applicability, date) at a
  time; the resolver selects it deterministically.
- A version in Published/Effective/Superseded/Retired/Archived is **never deleted** (snapshots reference it).
- Superseded and Retired both stop *future* application but **never invalidate frozen snapshots** (snapshot
  isolation, I2).

**Illegal transitions (MUST be rejected):**
- Any backward transition past Published (e.g. Published → Draft, Approved → Reviewed → edit-content).
- Effective → Draft/Reviewed/Approved (no un-publishing).
- Any → Deleted (mandates are never deleted; `MDL_Lifecycle.md` §5).
- Editing Rule Set / Applicability / Effectivity / Jurisdiction Layer of a Published+ version (must be a new
  version).
- **[BLOCKED-INPUT / illegal-until-ratified]** Any transition to a "Revoked/Void" state — no such state exists
  in doctrine; a mandate authored under invalid authority has **no legal transition** today (audit CR-3). The
  runtime MUST NOT invent one; it surfaces the case for ratification.

**Recovery behavior:**
- A failure between Draft→Approved leaves an **Authoring Work Item** in its last durable state; the workflow
  resumes from there — no partial publish occurs.
- A failure during Approved→Published means the version is **not** Published (invisible to resolution); retry
  re-attempts the same publish under the same version intent (no spurious second version).
- Published→Effective is a **derived, time-driven** transition (no write needed): "Effective" is computed from
  the effective window at read time. There is nothing to recover — a missed transition simply means the next
  resolution observes the correct in-force state.

---

## 2. Override state machine

Maps the Application-lifecycle Override stage (`MDL_Lifecycle.md` §2).

```
Requested → Approved → Active → ┬→ Expired
                                └→ Revoked
```

**States:**
- **Requested** — a requestor has submitted an override bound to a Snapshot, with reason + expiry.
- **Approved** — a *distinct* approver has authorized it (dual-authorization).
- **Active** — approved and within its expiry window; overlays the runtime outcome.
- **Expired** — the expiry instant has passed; inert. (Derived, time-driven.)
- **Revoked** — explicitly revoked before expiry; inert; terminal.

**Legal transitions:**
| From | To | Trigger |
|---|---|---|
| Requested | Approved | second, distinct actor approves |
| Approved | Active | approval recorded and current time < expiry |
| Active | Expired | current time ≥ expiry (derived) |
| Active | Revoked | explicit revocation |
| Approved | Revoked | revoked before ever active |

**State invariants:**
- Requestor ≠ approver (dual-authorization); self-approval is illegal.
- An override **never mutates its bound Snapshot** (I2).
- Effectiveness is **evaluated at read time** against the current instant — never persisted as a stored
  "effective" boolean. Expired/Revoked overrides contribute nothing to the runtime outcome.
- An override binds exactly one Snapshot; it cannot be re-pointed.

**Illegal transitions (MUST be rejected):**
- Requested → Active (skipping approval).
- Any → back to Requested/Approved from Active/Expired/Revoked.
- Approval by the requestor.
- Mutating the bound Snapshot as part of any transition.

**Recovery behavior:**
- Expiry is derived from the clock; no transition write is required — a crash cannot "miss" an expiry, because
  effectiveness is recomputed each read.
- A failure during approval leaves the override **Requested** (not Active); retrying approval is safe if and
  only if the approver is distinct and the act is not double-counted.

---

## 3. Determination state machine

The Determination is produced once and frozen; its "states" describe the request's progression, not a mutable
record (the Determination/Snapshot are immutable once created).

```
Pending → Resolved → Determined → Snapshotted → [Runtime-Overlaid?]
                          │
                          └→ Unresolved (terminal for this request)
```

**States:**
- **Pending** — request accepted; nothing computed yet.
- **Resolved** — the Resolved Mandate Set is computed (applicability + precedence + effectivity).
- **Determined** — entity state evaluated → compliance result + financial-override outcome.
- **Snapshotted** — the Determination is frozen into an immutable Snapshot (the point of record).
- **Unresolved** — resolution hit a same-level unresolved conflict or missing in-force version; a first-class,
  honest non-result (not an error) — raises a Conflict-Review item where applicable.
- **Runtime-Overlaid** — at read time, an in-force Override overlays the runtime outcome (the Snapshot is
  unchanged).

**State invariants:**
- A Determination is **admissible only once Snapshotted** (Constitution §1.4); a Determined-but-unsnapshotted
  result is never returned as recorded (see recovery).
- Snapshotting is **idempotent per governing event** — re-running the same governing event returns the same
  Snapshot, never a second.
- Unresolved is terminal for that request and MUST NOT auto-resolve to a compliant/non-compliant guess.

**Illegal transitions (MUST be rejected):**
- Determined → return-as-recorded without Snapshotted.
- Snapshotted → re-Determined-in-place (a re-evaluation is a *new* Determination + Snapshot, not a mutation).
- Unresolved → compliant/non-compliant by default.

**Recovery behavior:**
- If Snapshot write fails after Determined, the runtime returns the outcome **marked unrecorded**; a retry for
  the same governing event either finds the existing Snapshot (idempotent) or creates it once — never twice.
- If resolution fails mid-flight, the request is **Pending**/**Unresolved**; nothing is persisted as a
  determination; the consumer is told to retry (safe, idempotent).

---

## 4. Conflict-Review Item state machine

```
Flagged → Under Review → ┬→ Resolved (ratified ordering / decision applied going forward)
                         └→ Escalated (to the Human Ratifying Authority)
```

**State invariants:**
- Created only by resolution encountering a same-level, equal-date, ambiguous conflict (I4).
- Its resolution is a **human/ratified act**, recorded in Audit; the runtime never resolves it automatically.
- While Flagged/Under Review, resolutions for the exact conflicting context return **Unresolved**.

**Illegal transitions:** Flagged → Resolved by the runtime without a recorded human/ratified decision.

**Recovery behavior:** the item is durable; a crash mid-review resumes from the last recorded review state; no
determination is silently completed in the interim.

---

## 5. Cross-machine invariants (the ones that bind all four)

1. **Immutability dominates state.** No state transition may mutate a Published version's content, a Snapshot,
   or an Audit Event. Transitions change *lifecycle position and overlays*, never frozen truth.
2. **Time-driven transitions are derived, not written.** Published→Effective, Effective→Retired (on sunset),
   and Active→Expired are computed from windows/expiries at read time; they need no write and cannot be
   "missed" by a crash.
3. **Forward-only past the point of record.** Once a version is Published or a Determination is Snapshotted,
   there is no legal backward transition; correction is always a *new* object (new version, new determination,
   revocation of an override).
4. **No invented terminal states.** The set above is exhaustive for the current doctrine; the absent
   Revoke/Void-mandate transition (audit CR-3) is a **known gap the runtime must not fill by invention** — it
   is surfaced for ratification, not implemented.
