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

## 4. The Jurisdiction Stack (resolution's backbone)

Resolution's precedence backbone, per the uploaded *Jurisdiction Stack Model v1.0* (the more complete of
the source orderings — see the source-conflict note below).

**Precedence (highest wins in conflict):**

```
FEDERAL  ▸  PRIME_CONTRACT  ▸  STATE  ▸  COUNTY  ▸  MUNICIPAL  ▸  PROGRAM  ▸  INTERNAL
```

**Inheritance behaviors** (each mandate declares one):
- **FLOOR** — lower layers may *increase* requirements but not reduce them.
- **ADDITIVE** — lower layers *accumulate* constraints.
- **OVERRIDE** — a higher layer fully replaces lower behavior.

**Conflict resolution rules** (deterministic):
1. Compare precedence level; apply the higher.
2. If the same level, the newer `effective_date` wins.
3. If equal and ambiguous, **flag the conflict for review** — it must not auto-resolve (uploaded
   *Jurisdiction Stack* §3). This is why `Conflict-Review Queue` is a capability
   (`MDL_Capability_Framework.md` §2).

**Financial (tax) override precedence** resolves in order Federal ▸ Prime ▸ State ▸ Vendor Profile ▸ Auto
Tax Engine; if any layer sets `tax_exempt_override=True`, tax is zero (uploaded *Jurisdiction Stack* §5).

> **Source-conflict note [FACT].** The three source documents give *three different* jurisdiction
> orderings: the CFRS `MDL_LAYER_README.md:129,176-182` uses FEDERAL→STATE→PRIME→LOCAL; the uploaded
> *MDL Specification* §2.4 uses PRIME→STATE→LOCAL→PROGRAM→INTERNAL (PRIME at the top, no FEDERAL); the
> uploaded *Jurisdiction Stack Model v1.0* §1 uses FEDERAL→PRIME_CONTRACT→STATE→COUNTY→MUNICIPAL→PROGRAM
> →INTERNAL. This doctrine adopts the *Jurisdiction Stack Model v1.0* as the most complete and most
> recent, and records the divergence as an open item for ratification in
> `Open_Questions_and_Risks.md`. The precedence stack is doctrine and must be ratified before
> implementation, because a wrong ordering silently changes every conflict determination.

## 5. Is the lifecycle complete?

With the two-lifecycle separation, the jurisdiction stack, and the added stages (**Intake**, **Encode**,
**Reconcile/Re-evaluate**, and the explicit **Supersede vs Retire** split), the lifecycle is complete for
the anticipated end state (many jurisdictions, many nodes, cross-node propagation). The example's stages
all map onto it (Author→Intake+Encode; Review; Approval; Version; Publication; Propagation; Consumption→
Resolve; Snapshot; Override; Retirement→Sunset; Historical Archive), with four genuine additions. The one
element deliberately *not* added is a "delete" stage — mandates are never deleted, only superseded or
retired and archived, because deletion would break snapshot references (uploaded *MDL Spec* §7).
