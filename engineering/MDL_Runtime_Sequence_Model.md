# MDL Runtime Sequence Model

**Status:** ENGINEERING SPECIFICATION — derived from `MDL_Runtime_Specification.md`, `MDL_State_Model.md`, and
`Architecture_Validation_Report.md`. Describes the end-to-end runtime sequences as ordered interactions
between the eleven components. **No code, no APIs, no message formats** — only the order of interactions, the
component at each step, and the guarantee each step upholds. Components are named as in
`MDL_Component_Contracts.md`: Interface, Registry, Versioning, Jurisdiction, Resolution, Determination,
Snapshot, Override, Distribution, Audit, Governance.

Notation: `Actor/Component ▷ action ⇒ guarantee`. Steps are strictly ordered; `∥` marks a side effect taken
after the outcome, off the critical path.

---

## Sequence 1 — Author → Publish (Definition lifecycle)

```
1. Authoring Authority ▷ submits an authored source obligation + provenance
     → Governance ▷ Intake            ⇒ source attributed; MDL compiles, does not author
2. Governance ▷ Encode into a structured mandate (layer, applicability, rule sets, effectivity)
                                        ⇒ declarative, data-driven; no per-node hardcoding
   ∥ Audit ▷ record intake+encode
3. Governance ▷ Review (conformance: shape, precedence coherence, ceiling guards)
                                        ⇒ validates the encoding, never the source
   ∥ Audit ▷ record review outcome
4. Governance ▷ Approve (required authoring role)   [BLOCKED-INPUT: roles undefined, audit CR-2]
                                        ⇒ role-based; no non-authoring writer
   ∥ Audit ▷ record approval + approver
5. Versioning ▷ assign version, link supersession   ⇒ prior versions untouched (I2)
6. Registry ▷ store the Published version           ⇒ single authoritative store
   ∥ Audit ▷ record publish
7. Distribution ▷ emit MANDATE_CREATED / MANDATE_VERSIONED, scoped by jurisdiction
                                        ⇒ publish-after-commit; sole publisher (I5)
```
**End state:** a Published Mandate Version, resolvable within its effective window. **Recovery:** a failure
before step 6 leaves no Published version (Authoring Work Item resumes); a failure at step 7 re-emits (events
are at-least-once).

---

## Sequence 2 — Resolve → Determine → Snapshot → Return (Application lifecycle, the core path)

```
1. Consumer ▷ requests a determination with a Resolution Context (node/entity/service type, jurisdiction,
   as_of, entity attributes, governing-event id)
     → Interface ▷ authenticate + scope to least-privilege projection   ⇒ I10
2. Resolution ▷ gather candidate mandates
     → Registry ▷ read definitions
     → Versioning ▷ select in-force version at as_of      ⇒ pure function of (chain, as_of)
     → Jurisdiction ▷ order by precedence + apply inheritance (FLOOR/ADDITIVE/OVERRIDE)
                                        ⇒ deterministic; same-level tie → Sequence 5
        [BLOCKED-INPUT: canonical stack unratified, audit A1 — refuse multi-layer until ratified]
   ⇒ produces the Resolved Mandate Set (version-pinned), deterministically
3. Determination ▷ evaluate entity state against the Resolved Mandate Set
     ⇒ compliance status + per-rule gaps; authoritative, not advisory (I6)
   Determination ▷ compute Financial-Override Outcome from financial-policy rules
     ⇒ binding; MDL never books the amount (I3, I9)
4. Snapshot ▷ freeze {context, pinned versions, rule sets applied, result, financial-override}
     ⇒ immutable; idempotent per governing-event id (I2); same event → same snapshot
   ∥ Audit ▷ record VALIDATION_RESULT_RECORDED + SNAPSHOT_CREATED
5. Override ▷ overlay any in-force override on the runtime outcome (snapshot unchanged)  [see Sequence 3]
6. Interface ▷ return the runtime outcome to the Consumer
   ∥ Distribution ▷ emit the determination event, scoped
7. Consumer ▷ ACTS on the outcome (gates a payable, requires a document, books zero tax)
     ⇒ the consumer acts; MDL determined; the boundary holds (I9)
```
**Guarantee across the sequence:** identical inputs + versions ⇒ identical snapshot (I1). **Failure:** if
resolution/determination cannot complete on grounded in-force versions, Interface returns `UNRESOLVED`/
`INSUFFICIENT` (never a fabricated compliant); if the Snapshot write fails, the outcome is returned **marked
unrecorded** and a retry converges idempotently on one snapshot.

---

## Sequence 3 — Override flow

```
1. Requestor ▷ requests an override bound to a Snapshot (reason, expiry)
     → Override ▷ create in Requested        ⇒ bound to exactly one Snapshot; snapshot untouched
   ∥ Audit ▷ record OVERRIDE_CREATED
2. Approver (≠ requestor) ▷ approves
     → Override ▷ Requested → Approved → Active   ⇒ dual-authorization; self-approval rejected
   ∥ Audit ▷ record OVERRIDE_APPROVED
   ∥ Distribution ▷ emit OVERRIDE_APPROVED
3. On any later determination read for that Snapshot's entity/event:
     → Override ▷ evaluate effectiveness against current instant (< expiry, not revoked)
     ⇒ overlays the RUNTIME OUTCOME only; the Snapshot is never mutated (I2)
4. (Optional) Revoker ▷ revokes
     → Override ▷ Active → Revoked            ⇒ inert immediately; evaluated at read, never cached
   ∥ Audit ▷ record OVERRIDE_REVOKED ; Distribution ▷ emit
```
**Guarantee:** the Snapshot and the recorded Determination are unchanged throughout; only the *runtime
outcome* reflects the override, and only while it is Active and unexpired. **Failure/recovery:** an approval
failure leaves it Requested; expiry needs no write (derived at read).

---

## Sequence 4 — Propagation flow

```
1. Any committed change (create/version/update/snapshot/override) 
     → Distribution ▷ derive a Propagation Event, scoped to the change's jurisdiction
     ⇒ emitted AFTER durable commit (publish-after-commit)
2. Distribution ▷ match the event to Consumer Registrations whose jurisdiction_scope covers it
     ⇒ Federal→all; State→in-state; Prime→associated entities; Program→program entities
3. Distribution ▷ deliver at-least-once, ordered per mandate
     ⇒ a version event never precedes its create event for the same mandate
4. Consumer ▷ receive; dedupe by event identity; react (e.g. schedule re-evaluation)
     ⇒ exactly-once EFFECT via consumer-side dedupe
5. Snapshot isolation holds: a consumer adopting a new version applies it to FUTURE resolutions only
     ⇒ existing snapshots unchanged (I2)
```
**Guarantee:** consumers never receive out-of-scope events and never observe an event for an uncommitted
change. **Failure/recovery:** undelivered events are retried (outbox); duplicates are expected and tolerated.

---

## Sequence 5 — Version Upgrade flow

```
1. Authoring Authority ▷ authors a change to an existing mandate
     → run Sequence 1 (Author → Publish) producing a NEW Mandate Version
2. Versioning ▷ link new version --supersedes--> prior version
     ⇒ prior version content untouched (I2); version numbers monotonic
3. Prior version ▷ Effective → Superseded (for FUTURE resolutions)
     ⇒ still pinned by existing snapshots; historical determinations unchanged
4. Distribution ▷ emit MANDATE_VERSIONED, scoped
5. Next determination for an affected entity ▷ Re-evaluate (Sequence 2) against the NEW in-force version
     ⇒ produces a NEW Determination + NEW Snapshot; the old snapshot remains valid and reproducible
```
**Guarantee:** a version upgrade never rewrites history; it changes only which version *future* resolutions
select. **Failure/recovery:** if publish of the new version fails, the prior version stays Effective (no
supersession recorded); nothing is half-upgraded.

---

## Sequence 6 — Jurisdiction Conflict flow

```
1. During Sequence 2 step 2, Jurisdiction ▷ finds two applicable mandates
2. Jurisdiction ▷ apply rules in order:
     (a) higher precedence layer wins            ⇒ deterministic
     (b) if same layer, newer effective_date wins ⇒ deterministic
     (c) if equal & ambiguous → do NOT auto-resolve (I4)
3. On (c): Resolution ▷ return UNRESOLVED for that context (a first-class outcome, not an error)
     → raise a Conflict-Review Item (Flagged)
   ∥ Audit ▷ record the flagged conflict
4. Conflict-Review Item ▷ Flagged → Under Review → (Resolved by ratified decision | Escalated to HRA)
     ⇒ resolution is a human/ratified act, recorded in Audit; runtime never picks
5. While unresolved, determinations for that exact conflicting context return UNRESOLVED
```
**Guarantee:** the runtime is deterministic in producing `UNRESOLVED`; it never fabricates a winner.
**[BLOCKED-INPUT]** step 2 requires the ratified canonical stack (audit A1) for (a) to be correct.

---

## Sequence 7 — Retirement flow

```
1. Sunset condition: a version's effective window closes (or an explicit retire is authored)
2. Versioning/Effectivity ▷ Effective → Retired  (derived from the window; no content change)
     ⇒ stops applying to NEW resolutions
   ∥ Audit ▷ record retirement
   ∥ Distribution ▷ emit (retirement notice; canonical MANDATE_RETIRED pending event-set ratification)
3. Existing snapshots pinning the retired version ▷ remain valid and reproducible
     ⇒ retirement NEVER invalidates frozen snapshots (I2)
4. Retired → Archived (retention step)  ⇒ retained immutably; never deleted
```
**Guarantee:** retirement is forward-only and non-invalidating. **Not covered by doctrine (audit CR-3):**
retiring a mandate that was authored under *invalid authority* — there is no "void ab initio" flow; the
runtime MUST surface this for ratification and MUST NOT invent an invalidation of past snapshots.

---

## Sequence 8 — Re-evaluation / Reconciliation flow (on a governing event or version change)

```
1. Trigger: a new governing event for an entity, OR a MANDATE_VERSIONED event the consumer reacts to
2. Consumer ▷ request a fresh determination (Sequence 2)
     ⇒ produces a NEW Determination + NEW Snapshot against the now-in-force versions
3. Prior snapshots ▷ stay bound to their versions
     ⇒ history is never altered; only the latest-status projection advances
```
**Guarantee:** re-evaluation accretes new immutable records; it never edits prior ones. The "latest validation
status" is a derived projection over the newest snapshot (Persistence Model §6), not a mutated record.

---

## Cross-sequence guarantees (the invariants every sequence upholds)

1. **Determinism on the resolve→determine→snapshot path** (I1): identical inputs + versions ⇒ identical
   snapshot, in every sequence that produces one.
2. **Snapshot immutability** (I2): no sequence — upgrade, override, retirement, re-evaluation, propagation —
   ever mutates an existing snapshot.
3. **Publish-after-commit**: no sequence emits an event or returns a "recorded" result before its immutable
   write is durable.
4. **Resolve/act separation** (I9): every sequence ends with MDL returning a determination; the *act* is
   always the consumer's, never MDL's.
5. **Audit everywhere**: every mutating step in every sequence appends an Audit Event before acknowledgement.
