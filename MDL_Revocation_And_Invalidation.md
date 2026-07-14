# MDL Revocation & Invalidation Doctrine

**Status:** FOUNDATIONAL — **ratified by the Human Ratifying Authority on 2026-07-14** (`Ratification_Log.md`
R4). Its own doctrine because it governs **evidence preservation**. Governed by
`MDL_Infrastructure_Constitution.md`; resolves audit finding CR-3 (revocation vs snapshot immutability).

---

## 0. The distinction this doctrine draws

The Definition lifecycle already has forward-only exits — **Supersede** and **Sunset/Retire** — which stop a
mandate applying to *future* resolutions while **preserving the validity of every past determination**. This
doctrine adds a *different* exit for a *different* cause:

> **Retirement** answers "this mandate no longer applies going forward." **Invalidation (void ab initio)**
> answers "this mandate never validly applied at all, because the authority behind it was invalid." The first
> preserves past determinations; the second must *mark them invalid* — **without ever deleting or mutating
> them.**

---

## 1. The ratified rule

**Nothing is ever deleted.** When a mandate's authoring authority is found invalid (it never held the right to
author at that scope — *ultra vires*), the following occur, all **additively**:

1. The **mandate becomes void** — ab initio: treated as if it never held authority. It enters a terminal
   **Void** state (distinct from Retired).
2. Every **determination** that rested on the void mandate **becomes invalid**.
3. **Snapshots remain immutable** — no snapshot is edited, deleted, or rewritten.
4. **Audit history remains immutable** — nothing prior is altered; the invalidation is a *new* immutable
   record.
5. **Later determinations reference the invalidation** — new resolutions exclude the void mandate and, where
   relevant, cite the invalidation.

The mechanism that makes this possible without violating snapshot immutability (I2): invalidation is an
**append-only overlay**, exactly analogous to how an Override modifies a *runtime outcome* without mutating
its snapshot. The snapshot's *content* is untouched; its *validity* is now overlaid by an immutable
Invalidation Record read alongside it.

---

## 2. The Invalidation Record (the new immutable artifact)

- **Purpose:** the immutable, appended fact that a mandate is void and the determinations resting on it are
  invalid.
- **Owner:** MDL domain (recorded); the *finding of invalid authority* is a **ratified act** (HRA, or a
  future authority-lineage check — §5).
- **Immutable fields (all):** the void mandate + version identity; the ground (invalid authority, with the
  provenance that failed); the ratifying decision reference; the timestamp; the set of determinations/snapshots
  thereby invalidated (by reference, not by copy or edit).
- **Persistence class:** **append-only + immutable** (`engineering/MDL_Persistence_Model.md`).
- **Invariant:** an Invalidation Record never mutates a snapshot, a determination, or an audit event; it is a
  new fact read *alongside* them.

---

## 3. Effect on reads and later determinations

- **Reading an invalidated determination** returns the original snapshot **unchanged**, plus the overlay: the
  determination is surfaced as **INVALID**, with a pointer to the Invalidation Record. The evidence trail
  therefore shows, in full and forever: (a) the determination as it was originally made, (b) the invalidation
  and its ground, and (c) that the result is no longer valid.
- **New determinations** resolve as if the void mandate does not exist (it is excluded from the resolved set),
  and where a prior determination for the same entity is superseded by re-evaluation, the new snapshot cites
  the invalidation as the reason the prior result changed.
- **Determinism is preserved:** exclusion of a void mandate is deterministic given the Invalidation Record;
  identical context + versions + invalidation records ⇒ identical result.

---

## 4. State & event effects (cross-references)

- **State (`engineering/MDL_State_Model.md`):** the Mandate Version gains a ratified terminal transition to
  **Void** (from any post-Draft state), distinct from Retired: Retired is forward-only and preserves past
  validity; Void invalidates past determinations via the overlay. A Determination gains an **Invalidated**
  overlay condition (analogous to Runtime-Overlaid), never a mutation.
- **Events (`MDL_Event_Model.md`):** two ratified events — `MANDATE_VOIDED` (a mandate is voided ab initio)
  and `DETERMINATION_INVALIDATED` (a determination is marked invalid by an overlay) — are added to the
  canonical set, emitted publish-after-commit and scoped like all propagation events.
- **Audit:** voiding and invalidation each append an Audit Event; the audit trail is never edited.

---

## 5. What R4 does and does not settle

- **Settles (ratified):** the **remediation** semantics — what happens to mandates, determinations, snapshots,
  and audit when authority is found invalid. Nothing is deleted; evidence is preserved in full.
- **Does not settle (future refinement):** the **detection** of invalid authority — i.e. **delegation** and
  **authority-lineage**: how MDL proves an authoring authority was authorized at its scope in the first place
  (the other half of the audit CR-3 cluster). Until that model exists, the *trigger* for invalidation is a
  **ratified finding** (an HRA act, `Ratification_Authority.md`), not an automatic check. This doctrine is
  designed to accept an authority-lineage trigger additively when it is ratified, without changing the
  remediation semantics above.

---

## 6. Why this preserves evidence (the point of the doctrine)

Because invalidation is additive and append-only, the system can always reconstruct the complete history: the
original determination (immutable), the invalidation and its cause (immutable), and every later determination
that honored it (immutable). No record is ever destroyed to correct an error — the correction is a new fact
layered over an unaltered past. This is the exact opposite of deletion, and it is what lets MDL remain a
truthful evidentiary authority even when it must undo a mandate that should never have existed.
