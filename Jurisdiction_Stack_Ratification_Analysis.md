# Jurisdiction Stack — Ratification Analysis

**Status:** DECISION SUPPORT for the **Human Ratifying Authority (HRA)**. This document analyzes every
proposed jurisdiction ordering and recommends one, **but ratifies nothing and implements nothing** — the
canonical stack is a constitutional choice reserved to the HRA (`MDL_Infrastructure_Constitution.md` §2;
audit A1/Q1). No doctrine file is edited by this analysis; the MDL Constitution still carries the open item
until the HRA rules.

**Why this is blocking:** `Architecture_Validation_Report.md` and `engineering/MDL_Runtime_Specification.md`
mark Jurisdiction Resolution **[BLOCKED-INPUT]** — deterministic resolution (invariant I1/I4) is *impossible*
over an undecided precedence order, because a different order silently changes every conflict determination
(`MDL_Lifecycle.md:115`).

**Evidence discipline:** every ordering is quoted with file:line; each argument is tagged **[FACT]**
(sourced), **[LAW]** (a well-established legal principle), or **[INFERENCE]** (this analysis's synthesis).

---

## 1. The proposed orderings (verbatim, cited)

| # | Source | Ordering (highest precedence → lowest) | Levels | Apex | Evidence |
|---|---|---|---|---|---|
| **S1** | **CFRS MDL** | FEDERAL → STATE → PRIME → LOCAL | 4 | FEDERAL | `EchoForge/MDL_LAYER_README.md:178-184,922`; "Higher jurisdiction levels take precedence" (`:184`) |
| **S2** | **Uploaded MDL Specification §2.4** | PRIME (Client Contract) → STATE → LOCAL → PROGRAM → INTERNAL | 5 | **PRIME** | uploaded *MDL Spec* `:86-98`; "Higher precedence overrides lower precedence" (`:98`); **no FEDERAL** |
| **S3** | **Uploaded Jurisdiction Stack Model v1.0 §1** | FEDERAL → PRIME_CONTRACT → STATE → COUNTY → MUNICIPAL → PROGRAM → INTERNAL | 7 | FEDERAL | uploaded *Jurisdiction Stack Model* `:172-186`; "highest wins in conflict" (`:172`) |
| **S4** | **MDL Constitution (current)** | = S3 (adopted verbatim, flagged for ratification) | 7 | FEDERAL | `MDL_Lifecycle.md:90,108-114` |
| **R** | **Trust Runtime (peer node, for reference)** | GLOBAL → INTERNATIONAL → FEDERAL → STATE → LOCAL → ORGANIZATIONAL → UNKNOWN | 7 | GLOBAL | `EchoForge/echoforge/trust/contract.py:54-63` — an *altitude* model, not a conflict-precedence stack |

All four MDL sources agree on the **secondary rules**: inheritance behaviors **FLOOR / ADDITIVE / OVERRIDE**
(S1 `:169-173`; S2 has none explicit; S3 `:188-206`), and the conflict tiebreak **higher precedence → newer
`effective_date` → flag for review** (S3 `:210-222`; adopted in `MDL_Lifecycle.md:98-103`). The disagreement
is entirely in the **precedence order and level set**.

---

## 2. The differences — two independent axes

The four orderings differ on **two separate questions**, which must not be conflated:

### Axis A — the apex authority: FEDERAL or PRIME?
- **FEDERAL at the top:** S1, S3, S4 (and the Trust Runtime places FEDERAL below only GLOBAL/INTERNATIONAL).
- **PRIME (client contract) at the top, FEDERAL absent:** S2 alone.

This is the **substantive constitutional conflict**. It asks: *can a private client contract outrank — and
therefore override — federal (and state) law?*

### Axis B — granularity and the level set
- **LOCAL** as one level (S1, S2) vs **COUNTY + MUNICIPAL** split (S3, S4).
- **PROGRAM + INTERNAL** present (S2, S3, S4) vs absent (S1).
- **PRIME** named `PRIME` (S1, S2) vs `PRIME_CONTRACT` (S3, S4) — same concept.
- **No source** has GLOBAL / INTERNATIONAL / SUPRANATIONAL / TREATY / TRIBAL — but the **Trust Runtime does**
  (GLOBAL, INTERNATIONAL above FEDERAL) `contract.py:57-58`.

Axis B is a *completeness/granularity* choice with no legal error attached. Axis A is where a wrong choice
produces determinations a court, a regulator, or the Economic Core would reject.

### Comparison matrix (position of each authority, top=1)

| Authority | S1 (CFRS) | S2 (MDL Spec) | S3/S4 (Stack Model) | R (Trust Runtime) |
|---|---|---|---|---|
| GLOBAL / INTERNATIONAL | — | — | — | 1–2 |
| FEDERAL | **1** | **absent** | **1** | 3 |
| PRIME (contract) | 3 | **1** | **2** | (ORGANIZATIONAL, bottom) |
| STATE | 2 | 2 | 3 | 4 |
| COUNTY | (LOCAL) | — | 4 | (LOCAL) |
| MUNICIPAL | (LOCAL) | 3 (LOCAL) | 5 | 5 (LOCAL) |
| PROGRAM | — | 4 | 6 | (ORGANIZATIONAL) |
| INTERNAL / ORGANIZATIONAL | — | 5 | 7 | 6 |

The matrix exposes the anomaly: **every source except S2 keeps government above contract; the Trust Runtime
puts contractual/organizational authority at the *bottom* — the opposite of S2/S3's placement of PRIME near
the top.**

---

## 3. Root cause — precedence (OVERRIDE) conflated with stringency (FLOOR)

The FEDERAL-vs-PRIME conflict dissolves once two mechanisms the specs *already contain* are kept distinct:

- **Precedence rank** decides who wins an **OVERRIDE** conflict — the authority to *replace* another layer's
  rule (S3 `:204-206`: "OVERRIDE — Higher layer fully replaces lower behavior").
- **Stringency** is expressed by **FLOOR** inheritance — "lower layers may increase requirements but not
  reduce them" (S3 `:196-198`). A layer can be *stricter* without outranking anyone.

The intuition behind S2's "PRIME at top" is real: **in contracting, the client contract drives the strictest
requirements.** **[LAW]** But a private contract *raises the floor above the legal minimum*; it **cannot
remove a legal requirement** — a contract clause purporting to waive a federal statutory obligation is void.
So the contract's business primacy is correctly modeled as **FLOOR/ADDITIVE inheritance over the legal
baseline**, *not* as **OVERRIDE precedence above federal law**. **[INFERENCE]** S2 mis-modeled a
*stringency* fact as a *precedence* fact — and by doing so granted contracts the power to override statute,
which is legally invalid.

**Corollary category insight [INFERENCE].** The stack interleaves two *kinds* of authority that behave
differently:
- **Governmental / legal altitude** (INTERNATIONAL, FEDERAL, STATE, COUNTY, MUNICIPAL) — sourced from public
  law; higher government **preempts** lower; OVERRIDE flows top-down within this spine.
- **Contractual / organizational** (PRIME_CONTRACT, PROGRAM, INTERNAL) — sourced from private agreement or
  internal policy; these may **FLOOR/ADD** over the legal result but may **never OVERRIDE public law**.

Placing `PRIME_CONTRACT` *between* FEDERAL and STATE (S3/S4) is the residual category error: it still lets a
contract OVERRIDE state statute. The Trust Runtime's model already corrects this — contractual/carrier rules
are `ORGANIZATIONAL`, the **bottom** tier (`contract.py:62`, "e.g. accreditation body, carrier rule").

---

## 4. Architectural consequences of each ordering

| Ordering | Consequence |
|---|---|
| **S2 (PRIME apex, no FEDERAL)** | **Unusable as a legal precedence stack.** [LAW] A contract OVERRIDES statute → determinations no court/regulator would honor. **No FEDERAL slot** → federal mandates cannot be placed deterministically → a determinism-of-coverage hole (fails I1). **Rejected.** |
| **S1 (FED→STATE→PRIME→LOCAL)** | FEDERAL-apex is correct. But **LOCAL below PRIME** [INFERENCE] means a municipal ordinance is OVERRIDDEN by a private contract — legally wrong for OVERRIDE. Too coarse: no PROGRAM/INTERNAL, no COUNTY/MUNICIPAL split → cannot express common mandate sources. Would need extension almost immediately (fails Principle 10, "cut for the end state"). |
| **S3/S4 (FED→PRIME_CONTRACT→STATE→…→INTERNAL)** | FEDERAL-apex correct; good granularity (COUNTY/MUNICIPAL/PROGRAM/INTERNAL). **Residual error:** `PRIME_CONTRACT` above STATE lets a contract OVERRIDE state law (fine for FLOOR, wrong for OVERRIDE). **No international headroom.** Contradicts the Trust Runtime (contract should be organizational-bottom). Closest to correct, but not correct on Axis A for OVERRIDE. |
| **Recommended (§7)** | FEDERAL-anchored governmental spine + contractual/organizational as a FLOOR-only class at the bottom + reserved supranational/tribal tiers + gap-numbered ranks. Legally sound, ecosystem-compatible, future-proof. |

---

## 5. Compatibility analysis

### 5.1 Economic Core
Economic Core's doctrine makes external legal authorities **sovereign**: regulators are sovereign over
legality and "it complies, it does not self-exempt" (`RBM-Economic-Core/Economic_Truth_And_External_Authority.md:56`);
the domain "does not **Exempt** the ecosystem from any legal or financial obligation" (`:87`) and "does not
**Define** tax law" (`:82-88`). **[FACT]**

- A stack where **PRIME overrides FEDERAL/STATE (S2)** would let a *mandate* exempt the ecosystem from a legal
  tax/compliance obligation via a contract — **directly incompatible** with Economic Core's sovereignty model.
- A **FEDERAL-apex** stack where contracts only **FLOOR** is **compatible**: MDL owns the *mandate override
  determination*, the Economic Consumer *books* it (`MDL_Truth_Ownership_Matrix.md` §4), and public law is
  never contract-overridden.
- **Corroboration from the specs' own financial rules [FACT]:** the Jurisdiction Stack Model's **tax
  precedence** (§5, `:232-244`) is **Federal → Prime → State → Vendor Profile → Auto Tax Engine** — it places
  **FEDERAL above PRIME above STATE**. The specs' *financial* ordering already contradicts S2's PRIME-apex and
  even S3's PRIME-above-STATE, and points to FEDERAL-apex with contract below the legal tiers.

**Verdict:** FEDERAL-apex compatible; PRIME-apex incompatible with Economic Core.

### 5.2 Trust Runtime
The Trust Runtime is the peer MDL must compose with (Era 4). Its `JurisdictionLevel` **altitude** model is
`GLOBAL → INTERNATIONAL → FEDERAL → STATE → LOCAL → ORGANIZATIONAL` (`contract.py:54-63`). **[FACT]** Two
direct implications:
- **Contractual/organizational authority is the *bottom* tier** (`ORGANIZATIONAL`, "carrier rule") — so PRIME
  belongs near the bottom, **not** above STATE. This is in-ecosystem evidence *against* S2 and S3's PRIME
  placement.
- **International/global sits *above* FEDERAL** — the headroom S1–S4 all lack.
- A **FEDERAL-apex, organizational-bottom** MDL stack **maps cleanly** onto the Trust Runtime: MDL FEDERAL→TR
  FEDERAL, STATE→STATE, COUNTY/MUNICIPAL→LOCAL, PRIME/PROGRAM/INTERNAL→ORGANIZATIONAL. **S2 cannot be mapped**
  (no FEDERAL; contract-apex has no TR analog). **[INFERENCE]**

**Verdict:** a FEDERAL-apex/organizational-bottom stack is Trust-Runtime-compatible and composes without
duplication; S2/S3's PRIME placement diverges from the peer model.

### 5.3 Future international expansion
Principle 10 requires boundaries "cut for the end state," so growth "adds … jurisdiction layers rather than
re-cutting boundaries" (`MDL_Infrastructure_Constitution.md:264-267`). **[FACT]** The audit (H-7) showed that
**adding a tier *above* FEDERAL re-orders precedence** — a constitutional change — precisely because the
current stacks are a fixed ordinal list with no headroom. Two design moves neutralize this:
1. **Reserve the supranational tiers now** (INTERNATIONAL / SUPRANATIONAL / TREATY above FEDERAL) and a
   **TRIBAL / sovereign** slot, even if unused at launch — so the international end-state needs no re-cut.
2. **Rank by tier *numbers with gaps* (or an abstract altitude), not by ordinal position** — so inserting a
   tier is assigning an unused number, never renumbering the rest. **[INFERENCE]** This is what turns "adding
   a top layer" from a constitutional re-cut into an additive registration, satisfying Principle 10.

**Verdict:** none of S1–S4 is internationally future-proof as written; the recommendation adds reserved tiers
+ a gap-numbered rank model to make it so.

---

## 6. Constitutional-principle test

| Principle | S1 | S2 | S3/S4 | Recommended |
|---|---|---|---|---|
| **Determinism of coverage (I1/I4)** — every mandate has a deterministic slot | Pass | **Fail** (no FEDERAL slot) | Pass | Pass |
| **Compile-don't-legislate / external-authority sovereignty (I8)** — no contract OVERRIDES public law | Partial (LOCAL<PRIME) | **Fail** | Partial (PRIME>STATE) | **Pass** |
| **Financial-override supremacy consistent with tax law (I3)** — Federal tax not contract-overridable | Pass | **Fail** | Partial | **Pass** |
| **Economic Core compatibility** (§5.1) | Pass | **Fail** | Pass | **Pass** |
| **Trust Runtime compatibility** (§5.2) | Partial | **Fail** | Partial | **Pass** |
| **Boundaries cut for the end state (Principle 10)** — international headroom, no re-cut | **Fail** | **Fail** | **Fail** | **Pass** |
| **Explicit & total order (I4)** | Pass | Pass | Pass | Pass |

No source ordering passes all principles. **S2 fails the most and is legally invalid; S3/S4 is the best of the
sourced options but carries the PRIME-above-STATE OVERRIDE error and no international headroom.**

---

## 7. Recommendation (for HRA ratification — not a decision)

**Recommended: a FEDERAL-anchored, two-class stack with reserved supranational headroom and gap-numbered
ranks.** It resolves the FEDERAL-vs-PRIME conflict at its root (precedence vs stringency), preserves the
business truth behind S2, and is compatible with the Economic Core, the Trust Runtime, and international
expansion.

**Class 1 — Governmental / legal spine (OVERRIDE-precedence, top-down):**
```
[reserved: GLOBAL / SUPRANATIONAL / TREATY]  →  FEDERAL  →  STATE  →  COUNTY  →  MUNICIPAL
                                        (+ reserved: TRIBAL / sovereign, ranked per legal status)
```
**Class 2 — Contractual / organizational (FLOOR/ADDITIVE only; may NEVER OVERRIDE Class 1):**
```
PRIME_CONTRACT  →  PROGRAM  →  INTERNAL      (the "ORGANIZATIONAL" tier, mapping to Trust Runtime)
```

**The governing rules the HRA would ratify with it:**
1. **OVERRIDE flows only *downward within a class*.** A Class-1 layer may OVERRIDE a lower Class-1 layer; a
   Class-2 layer may OVERRIDE a lower Class-2 layer. **No Class-2 layer may OVERRIDE any Class-1 layer.**
2. **Class-2 layers may FLOOR/ADD over the Class-1 result** — this is how a client contract lawfully imposes
   requirements stricter than statute (the S2 business truth, correctly located).
3. **Tiebreak within a tier:** newer `effective_date` wins; equal-and-ambiguous → flag for review (I4) — as
   all sources already agree.
4. **Ranks are assigned as numbers with gaps** (e.g. Class-1: 100/200/300/400/500 with reserved 10/20/50
   above FEDERAL; Class-2: 600/700/800), so a future tier inserts without renumbering (Principle 10).
5. **Tax/financial precedence** (Federal → Prime → State → Vendor → Auto-Tax, S3 §5) is preserved and is a
   *special case* of rule 1 + rule 2: federal tax law is Class-1 apex; a contract exemption is a Class-2 FLOOR
   that can only *add* obligations, and a mandate `tax_exempt_override` is honored only where a *higher legal
   authority* permits the exemption — never as a contract overriding tax law.

This recommendation **differs from all four sourced orderings** and is therefore a genuine design decision,
not a copy — which is exactly why it must be **ratified by the HRA**, not adopted silently.

---

## 8. The ratification options, laid out for the HRA

The HRA may ratify any one of the following. Each is complete enough to unblock Jurisdiction Resolution.

| Option | Ordering | Pros | Cons |
|---|---|---|---|
| **A — Ratify S3/S4 as-is** | FEDERAL → PRIME_CONTRACT → STATE → COUNTY → MUNICIPAL → PROGRAM → INTERNAL | Most complete sourced option; already in the current Constitution; minimal change; FEDERAL-apex is correct. | PRIME_CONTRACT above STATE lets a contract OVERRIDE state law (legal error for OVERRIDE, fine for FLOOR); no international headroom; diverges from the Trust Runtime (contract-at-bottom). |
| **B — Ratify the §7 two-class stack (RECOMMENDED)** | Governmental spine + organizational FLOOR-only class + reserved supranational/tribal + gap ranks | Legally sound; Economic-Core-compatible; Trust-Runtime-aligned; internationally future-proof; resolves the conflict at its root; preserves S2's business truth via FLOOR. | Differs from all sources (a real decision); requires stating the OVERRIDE-only-within-class rule; marginally more complex to explain. |
| **C — Ratify S1 (CFRS)** | FEDERAL → STATE → PRIME → LOCAL | FEDERAL-apex; simplest; matches the original engine. | Too coarse (no PROGRAM/INTERNAL, no COUNTY/MUNICIPAL); LOCAL-below-PRIME is legally odd; no international headroom; would need re-cutting almost immediately (fails Principle 10). |
| **D — Reject S2 explicitly** | (n/a) | Records that PRIME-apex is legally invalid so it is never revived. | — |

**This analysis recommends B, with A as the pragmatic fallback if the HRA prefers to ratify a sourced
ordering now and defer the two-class refinement.** In either case, **S2 should be explicitly rejected**
(Option D) because it is legally invalid and its revival would corrupt every conflict determination.

---

## 9. What this analysis does NOT do

- It **does not edit** `MDL_Lifecycle.md` or any doctrine — the open item stands until the HRA rules
  (implementing the choice here would usurp the HRA's authority, `MDL_Infrastructure_Constitution.md` §2).
- It **does not invent** a new jurisdiction concept beyond reserving named-but-unused tiers for the end state
  (which Principle 10 already anticipates).
- It **does not decide** the COUNTY/MUNICIPAL granularity or the exact reserved-tier names — those are
  ratification details the HRA settles when it rules.

**Once the HRA ratifies one option, the single required action is a one-line doctrine amendment** replacing
the open jurisdiction-stack item in `MDL_Lifecycle.md` §4 with the ratified stack + rules — after which
Jurisdiction Resolution (C3) is unblocked and the build order in `Architecture_Validation_Report.md` §3 can
proceed.
