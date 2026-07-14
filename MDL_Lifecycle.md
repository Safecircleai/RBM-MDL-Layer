# The MDL Lifecycle

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `MDL_Internal_Architecture.md`
(the layers each stage runs in), `MDL_Event_Model.md` (the events each stage emits), the uploaded
*Jurisdiction Stack Model v1.0*.

---

## 0. Why two lifecycles, not one

The example lifecycle in the brief — Author → Review → Approval → Version → Publication → Propagation →
Consumption → Snapshot → Override → Retirement → Historical Archive — is **incomplete in one structural
way**: it conflates the lifecycle of a *mandate definition* (which is authored once and lives for years)
with the lifecycle of a *determination* (which happens per entity, per event, thousands of times against
that mandate). **[INFERENCE]** These are different clocks. Merging them hides the fact that a single
mandate version is *snapshotted* many times, and that *override* and *reconciliation* belong to the
determination clock, not the authoring clock.

This document therefore separates them into two complete lifecycles — the **Definition Lifecycle** (the
mandate) and the **Application Lifecycle** (the determination) — joined at Publication → Resolution. This
is the improvement over the example; each stage below also states its owner and the invariant it must
preserve.

---

## 1. The Definition Lifecycle (the mandate)

The life of a mandate *definition*, from the authored obligation to the historical archive.

```
Intake → Encode → Review → Approve → Version → Publish → Propagate
                                                             │
                                          ┌──────────────────┼───────────────────┐
                                     Supersede            Sunset / Retire     (stays active)
                                          │                  │
                                          └──────────────────┴──► Historical Archive (immutable)
```

| # | Stage | Owner | What happens | Invariant preserved |
|---|---|---|---|---|
| 1 | **Intake** | Mandate Authoring Authority → MDL domain | An authored obligation (statute, prime contract, org/program policy) is received with its provenance. | The source is attributed to its authoring authority; the domain compiles, it does not legislate. |
| 2 | **Encode** | MDL domain | The obligation is compiled into a structured mandate: jurisdiction layer, applicability, rule sets (documents, evidence, thresholds, participation, financial policy). | Encoding is data-driven and declarative; hardcoded per-node exclusions are avoided (uploaded *MDL Spec* §3.3–3.4). |
| 3 | **Review** | MDL domain (governed role) | The encoded mandate is checked for conformance (schema, ceiling guards, precedence coherence). | Review never edits the *source*; it validates the *encoding*. |
| 4 | **Approve** | MDL domain (authoring/ops role) | Role-based approval admits the mandate; constitutional mandate-governance changes require Human Ratifying Authority. | Role-based access on creation/modification (uploaded *Service Contract* §7). |
| 5 | **Version** | MDL domain | A version number is assigned; a new version links to the one it supersedes; prior versions remain immutable. | New versions never mutate historical behavior (uploaded *MDL Spec* §7). |
| 6 | **Publish** | MDL domain | The version becomes active within its effective window and available to resolution. | Effectivity-bounded; publication ≠ effectivity (a mandate may publish before its effective date). |
| 7 | **Propagate** | MDL domain (sole publisher) | A `MANDATE_VERSIONED`/`MANDATE_UPDATED` event is emitted; subscribed nodes learn of the change, scoped by jurisdiction layer. | Snapshot isolation: propagation never mutates existing snapshots (uploaded *Propagation Protocol* §2–3). |
| 8a | **Supersede** | MDL domain | A newer version replaces an active one for future resolutions; historical snapshots keep the old version. | Supersession is a version link, not a mutation. |
| 8b | **Sunset / Retire** | MDL domain | The mandate's effective window closes; it stops applying to *new* resolutions. | Retirement never invalidates snapshots already frozen against it. |
| 9 | **Historical Archive** | MDL domain (append-only) | Retired/superseded versions and their audit trail are retained immutably for oversight. | Append-only; never edited or deleted. |

## 2. The Application Lifecycle (the determination)

The life of a *determination*, per entity, per governing event — the clock that runs against a published
mandate.

```
Resolve → Determine (Validate) → Snapshot → (Override?) → Act → Re-evaluate/Reconcile → Audit
```

| # | Stage | Owner | What happens | Invariant preserved |
|---|---|---|---|---|
| 1 | **Resolve** | MDL domain | Given an entity context, deterministically resolve the applicable mandate set (applicability + jurisdiction precedence + effectivity). | Determinism: identical context → identical set (uploaded *MDL Spec* §2.2, §4.1). |
| 2 | **Determine (Validate)** | MDL domain | Evaluate entity state against the resolved set → compliance status, gaps, and the binding financial-override outcome. | Authoritative, not advisory (`MDL_Infrastructure_Constitution.md` §6). |
| 3 | **Snapshot** | MDL domain | Freeze the resolved configuration + result as an immutable snapshot; results reference the snapshot, not live records. Idempotent per governing event. | Snapshot immutability (uploaded *MDL Spec* §2.3, §3.8, §4.2). |
| 4 | **Override** (conditional) | MDL domain (dual-auth) | If non-compliant, a dual-authorized, expiring override may modify the *runtime outcome* without mutating the snapshot. | Overrides do not mutate snapshots (uploaded *MDL Spec* §8). |
| 5 | **Act** | Business-Node / Economic Consumer | The consumer acts on the determination: gates a payable, requires a document, or books a zero-tax invoice. It may not contradict or bypass. | Resolve/act separation; the domain never acts. |
| 6 | **Re-evaluate / Reconcile** | MDL domain | On a new governing event or a version change, a *new* determination + snapshot is produced; prior snapshots stay bound to their versions. | Historical compliance is never retroactively altered (uploaded *MDL Spec* §7; *Propagation Protocol* §3). |
| 7 | **Audit** | MDL domain (append-only) → Auditor/Supervisor | The determination, its snapshot, and any override are recorded and made available for oversight. | Audit-trail integrity (uploaded *MDL Spec* §9). |

## 3. Where the two lifecycles join

The Definition Lifecycle produces *published, versioned mandates*; the Application Lifecycle *consumes*
them at **Resolve**. The join is one-way and clean: publishing a mandate never triggers a determination
(the node does, when it passes context); and a determination never edits a mandate (it only reads and
snapshots it). This one-way join is what lets one mandate version be snapshotted thousands of times
without any feedback loop into the definition.

## 4. The Jurisdiction Stack (resolution's backbone) — RATIFIED (Option B)

Resolution's precedence backbone, **ratified by the Human Ratifying Authority on 2026-07-14** as the
FEDERAL-anchored **two-class model** (`Jurisdiction_Stack_Ratification_Analysis.md` Option B;
`Ratification_Log.md` R2). The two classes separate *precedence* (who wins an OVERRIDE) from *minimum
required compliance* (a FLOOR a lower authority may raise but never lower).

**Class 1 — Governmental / legal spine** (OVERRIDE-precedence, highest wins in conflict, top-down):

```
[reserved: GLOBAL / SUPRANATIONAL / TREATY]  ▸  FEDERAL  ▸  STATE  ▸  COUNTY  ▸  MUNICIPAL
                                         (+ reserved: TRIBAL / sovereign, ranked per legal status)
```

**Class 2 — Contractual / organizational** (FLOOR/ADDITIVE only; may NEVER OVERRIDE Class 1):

```
PRIME_CONTRACT  ▸  PROGRAM  ▸  INTERNAL
```

**Inheritance behaviors** (each mandate declares one):
- **FLOOR** — lower layers, and any Class-2 layer over the Class-1 result, may *increase* requirements but
  never reduce them.
- **ADDITIVE** — lower layers *accumulate* constraints.
- **OVERRIDE** — a higher layer fully replaces lower behavior — **only within the same class** (rule 1).

**Ratified governing rules:**
1. **OVERRIDE flows only downward within a class.** A Class-1 layer may OVERRIDE a lower Class-1 layer; a
   Class-2 layer may OVERRIDE a lower Class-2 layer. **No Class-2 layer may OVERRIDE any Class-1 layer** — a
   private contract can never remove a legal (governmental) requirement.
2. **Class-2 may FLOOR/ADD over the Class-1 result** — this is how a client contract lawfully imposes
   requirements stricter than statute (stringency), without gaining precedence over law.
3. **Tiebreak within a tier:** the newer `effective_date` wins; equal-and-ambiguous → **flag for review**,
   never auto-resolve (Conflict-Review Queue capability; invariant I4).
4. **Ranks are assigned as tier numbers with gaps** (Class-1: reserved 10/20/50 above FEDERAL=100, then
   STATE=200, COUNTY=300, MUNICIPAL=400, plus a reserved TRIBAL slot; Class-2: PRIME_CONTRACT=600,
   PROGRAM=700, INTERNAL=800), so a future tier inserts by taking an unused number, never renumbering —
   satisfying Principle 10 ("boundaries cut for the end state").

**Financial (tax) override precedence** is the special case of rules 1–2 for the financial-policy rule:
federal tax law (Class-1 apex) is honored first, then state; a Class-2 contract may only *raise* obligations,
or apply a mandate-level tax exemption where a *higher legal authority* permits it — never as a contract
overriding tax law (consistent with the Economic Consumer's external-authority sovereignty). MDL owns the
override *determination*; the Economic Consumer books the effect.

> **Supersedes the prior source-conflict note.** The three source orderings (CFRS FEDERAL→STATE→PRIME→LOCAL;
> MDL Spec PRIME→STATE→LOCAL→PROGRAM→INTERNAL; Jurisdiction Stack Model FEDERAL→PRIME_CONTRACT→STATE→COUNTY→
> MUNICIPAL→PROGRAM→INTERNAL) are resolved by this ratification. The MDL Specification's **PRIME-apex
> ordering is explicitly rejected** as legally invalid — a contract cannot override public law. See
> `Jurisdiction_Stack_Ratification_Analysis.md` and `Ratification_Log.md` R2.

## 5. Is the lifecycle complete?

With the two-lifecycle separation, the jurisdiction stack, and the added stages (**Intake**, **Encode**,
**Reconcile/Re-evaluate**, and the explicit **Supersede vs Retire** split), the lifecycle is complete for
the anticipated end state (many jurisdictions, many nodes, cross-node propagation). The example's stages
all map onto it (Author→Intake+Encode; Review; Approval; Version; Publication; Propagation; Consumption→
Resolve; Snapshot; Override; Retirement→Sunset; Historical Archive), with four genuine additions. The one
element deliberately *not* added is a "delete" stage — mandates are never deleted, only superseded or
retired and archived, because deletion would break snapshot references (uploaded *MDL Spec* §7).
