# MDL Ownership Analysis (Phase 1 — Evidence-Backed)

**Status:** FOUNDATIONAL — the Phase-1 research deliverable that grounds every other document in this
repository. Ratification rests with the Human Ratifying Authority. Architecture and doctrine only.

**Evidence discipline:** per the ecosystem's evidence-of-truth convention
(`RBM-Economic-Core/research/FINANCIAL_NODE_CONSTITUTIONAL_RESEARCH.md:22-24`), every assertion below
is tagged **[FACT]** (documented, sourced), **[PRINCIPLE]** (a widely accepted architectural
pattern), or **[INFERENCE]** (this sprint's synthesis). Opinion is never presented as evidence.

---

## 0. What this analysis settles

Before any doctrine is written, this document answers the Phase-1 question — *does responsibility for
"mandate definition" already have an owner, and where are the boundaries?* — from the evidence in the
session's repositories and the three uploaded MDL specifications. The finding is then reduced to a
single ownership determination the rest of the repository builds on.

---

## 1. The primary question: what is the RBM MDL Layer?

**Institutional role.** The RBM MDL Layer is the ecosystem's **authoritative Mandate Definition
Layer**: the one node that compiles authored obligations (regulatory, contractual, organizational,
operational) into structured, versioned mandates, and *deterministically resolves and determines*
which of them apply to any entity, in any jurisdiction, at any point in time — with immutable
snapshots as the audit artifact. **[FACT]** the uploaded *Mandate Definition Layer Specification*
§1 defines it as "the universal governance and policy resolution engine across all Business Nodes …
[that] defines, resolves, enforces, and audits contractual, regulatory, financial, and operational
mandates in a deterministic, cross-node manner." **[FACT]** the same spec §12: "MDL is not a
feature. It is: A policy compiler / A compliance resolution engine / A financial override authority /
A governance backbone. All future nodes must treat MDL as infrastructure."

**Why it is infrastructure (not a product or a feature).** **[PRINCIPLE]** across the ecosystem, an
*infrastructure node* is one that (a) owns a truth many nodes consume and reference rather than copy,
(b) is consumer-agnostic — no consumer name is load-bearing in it, and (c) is not externally sold as
a product (Economic Core: `RBM-Economic-Core/README.md:6,19,84`; Trust Runtime:
`EchoForge/echoforge/trust/README.md:4`, `EchoForge/TRUST_RUNTIME_ARCHITECTURE.md:199`). **[FACT]**
MDL meets (a): it is "a node-agnostic governance spine" whose "Same mandate infrastructure serves
FLEET, HOUSING, CONSTRUCTION, and all other nodes" (`EchoForge/MDL_LAYER_README.md:54,64`), and the
uploaded spec §5 forbids nodes from duplicating it. **[FACT]** it meets (b): the uploaded spec is
written against `NodeType`/`entity_type`/`service_type` context, not against any one caller. **[FACT]**
it meets (c): the closest capability (#115) is catalogued as internal governance, not a sold product,
and is flagged as *hardcoded to one node/one jurisdiction today*
(`SafeLaunchCenter-Core/governance/platform/TRUST_CLAIM_AUDIT.md:39`).

**What truth it authoritatively owns.** **[INFERENCE, from the specs]** the *authoritative resolved
mandate set and the determination of satisfaction* — i.e. *which mandates apply, at what version, and
whether an entity meets them, frozen as an immutable snapshot*, including the binding financial-override
outcome. This is the truth no other node owns today (§3).

**What truths it explicitly does NOT own** (established in detail in `MDL_Truth_Ownership_Matrix.md`):
the *source obligations themselves* (authored by regulators / organizations / client contracts); the
*economic execution* of a determination (Economic Core books it); the *business decision and
execution action* (the consuming node acts); *ecosystem governance doctrine* (LEAL/SafeLaunchCenter);
and *discipline-specific legal reasoning* (EchoForge's Trust Runtime). It owns the *resolution and
determination*, never the law, the money, the decision, or the act.

---

## 2. Does "mandate definition" already have an owner? (the ownership tension)

**[FACT]** Today the capability is owned as **embedded business logic by CFRS-Enterprise**: it is
capability **#115 "Mandate Definition Layer (MDL) — Cross-Node Governance Rule Engine," Primary Node:
CFRS-Enterprise** (`SafeLaunchCenter-Core/governance/platform/RBM_CAPABILITIES_V1.md:1624-1635`),
implemented in `cfrs-backend/models/mandate.py` and `cfrs-backend/services/mdl_engine.py`
(`EchoForge/MDL_LAYER_README.md:322-327`).

**[FACT]** There is a written plan to extract it from CFRS into a standalone shared authority — but
the *home* of that standalone authority was **left ambiguous** across the source material:
- `EchoForge/MDL_LAYER_README.md:25,80-95` proposes an **"EchoForge MDL Service"** (`POST
  /echoforge/mdl/validate`).
- The uploaded *MDL Specification* §10 offers host-neutral options: "Shared Internal Package" or an
  "Internal Governance Service."
- A **new empty `RBM-MDL-Layer` repository** now exists, implying the standalone authority is instead
  being chartered as **its own independent node**.

**[FACT]** the capability's own catalog note says its value exceeds its current owner: "a
jurisdiction-aware compliance engine has value far beyond fleet management"
(`RBM_CAPABILITIES_V1.md:4163`); "this alone could be a standalone licensable product for any
multi-jurisdiction compliance use case" (`:1635`).

**Determination [INFERENCE, ratified by the task charter].** *Mandate definition is real and
currently owned by CFRS as embedded business logic, but no standalone infrastructure node owns it
ecosystem-wide.* That gap is what this repository fills. The ambiguity of home is resolved here: the
RBM MDL Layer is an **independent infrastructure node with its own repository** — not the CFRS
implementation, and not hosted inside EchoForge. This is consistent with the uploaded *MDL ↔ EchoForge
Service Contract*, which already treats MDL and EchoForge as **two separate systems** (§2), the strongest
evidence in the source material that MDL is meant to stand on its own.

---

## 3. Where responsibility boundaries already exist (the seams to respect)

Each boundary below is drawn from existing text, not invented. The full grids are in
`MDL_Responsibility_Matrix.md` and `MDL_Truth_Ownership_Matrix.md`; this is the evidence.

| Boundary | Established by (evidence) | The seam |
|---|---|---|
| **LEAL ↔ MDL** | LEAL "governs systems," is barred from "introduc[ing] new governance interpretations" (`EchoForge/governance/LEAL_SPEC.md:29-31,196-197`); mandate resolution is an MDL-engine function (`EchoForge/MDL_LAYER_README.md:327,332-333`). | LEAL enforces *doctrine-compliance of bots/systems*; it never resolves mandates. **[FACT]** |
| **EchoForge ↔ MDL** | "EchoForge does not define mandates. EchoForge does not rewrite snapshots. EchoForge does not alter compliance results." (uploaded *Service Contract* §2); EchoForge reads MDL over read-only endpoints, may not "Directly write mandates … Force compliance overrides" (§3). | EchoForge *supervises* (monitors, risk-scores, quarantines) over a read-only boundary; MDL *owns* the mandate and the determination. **[FACT]** |
| **Economic Core ↔ MDL** | Economic Core "enforces economic policy it does not author" and treats a *mandate* as an *authority basis it consumes*, not one it writes (`RBM-Economic-Core/RBM_Economic_Constitution.md:102-103`; `Economic_Intent_Constitution.md:38`; `Economic_Lifecycle_Constitution.md:74`); it "does not Define tax law … or Exempt the ecosystem" (`Economic_Truth_And_External_Authority.md:82-88`). Meanwhile the uploaded *MDL Spec* §2.5 makes mandate-level financial policy (e.g. `tax_exempt_override`) *authoritative* over tax engines. | MDL **owns** the financial-override *mandate determination*; Economic Core **consumes** it and books the economic effect (e.g. forces tax to zero). Neither defines the other's truth. **[FACT]** |
| **Trust Runtime (EchoForge) ↔ MDL** | The Trust Runtime answers *discipline determinations* (HIPAA/Legal/Tax/PCI) via one contract and carries a non-authority disclaimer (`EchoForge/echoforge/trust/contract.py:5-14,357-364`); MDL *authors/versions/resolves mandates* (`EchoForge/MDL_LAYER_README.md:54,327`). Both call themselves "node-agnostic," so the seam must be explicit. | Trust Runtime = *evaluate a subject against a discipline's body of professional law*. MDL = *resolve the authoritative, versioned mandate set for an entity and determine satisfaction*. A mandate MAY require a trust determination as one satisfaction condition; MDL consumes it, it does not perform the legal reasoning. **[INFERENCE]** (see `MDL_vs_Industry_Systems.md` §"MDL vs the Trust Runtime"). |
| **Business Nodes ↔ MDL** | "Every Business Node must … Pass context into MDL before financial finalization. Respect validation response. Respect financial overrides." and must NOT "Duplicate mandate enforcement logic … Bypass tax_exempt_override logic." (uploaded *MDL Spec* §5). | Nodes *consume* MDL and *act* on its determination; they never duplicate or fork it. **[FACT]** |
| **PERSE, UPM, B4Arts, Insurance, RESA, CAI ↔ MDL** | These are consumers/peers: UPM/B4Arts/CFRS are business/product nodes (`RBM-Economic-Core/Repository_Independence_Review.md:46`); PERSE is a research-stage emergency-response node (`RBM_CAPABILITY_INDEX.md:91`); RESA is the future Asset-Domain peer (`Constitutional_Migration_Plan.md:104`); Insurance and Customer Acquisition Infrastructure (CAI) are planned consumers (`TRUST_RUNTIME_ARCHITECTURE.md:181,187`). | All consume MDL by role; none owns or duplicates it. Occupants illustrate; the role binds. **[FACT]/[INFERENCE]** |

---

## 4. The ownership determination (one sentence, then the corollaries)

> **The RBM MDL Layer is the single authoritative owner of the ecosystem's resolved-mandate truth —
> which mandates apply, at what version, in which jurisdiction, and whether an entity satisfies them,
> frozen as immutable snapshots — and it owns nothing else: not the source law it compiles, not the
> money its determinations touch, not the business decision or the execution act, and not the
> ecosystem's governance doctrine.**

Corollaries, each load-bearing for a later document:
1. **One owner, no duplication.** No node re-implements mandate resolution; consumers reference MDL
   (uploaded *MDL Spec* §5; `TRUTH_REGISTRY_REPORT.md:3`). **[FACT]**
2. **Determinations are authoritative, not advisory.** Financial overrides and compliance
   determinations bind the consumer; the consumer *acts* but may not *contradict* (uploaded *MDL
   Spec* §2.5; *Service Contract* §8 "Immutable Guarantees"). **[FACT]** This revises the earlier
   CFRS "soft validator" framing — see `Open_Questions_and_Risks.md`.
3. **MDL compiles, it does not legislate.** Source obligations are authored by external authorities;
   MDL owns the encoded, resolved, versioned truth. **[INFERENCE]**
4. **Independence is constitutional.** The node owns its doctrine in full and names no consumer as
   load-bearing; it passes the ten-year test (`Repository_Independence_Review.md`). **[PRINCIPLE]**

Everything downstream — the constitution, the matrices, the lifecycle, the architecture, the
interfaces, the migration, and the IEF/IAF assessments — is this determination, applied.
