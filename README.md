# RBM-MDL-Layer

**The constitutional Mandate Domain of the RiteByMe (RBM) ecosystem — an independent infrastructure
node.**

RBM-MDL-Layer is the single authoritative owner of the ecosystem's **resolved-mandate truth**: the one
node that compiles authored obligations (regulatory, contractual, organizational, operational) into
structured, versioned mandates and *deterministically resolves and determines* which of them apply to
any entity, in any jurisdiction, at any time — with immutable snapshots as the audit artifact.

> **It owns the determination. It does not own the law, the money, or the act.**
>
> RBM-MDL-Layer does not author the source obligation (regulators, clients, and organizations do), does
> not execute a business or economic action (consuming nodes and the Economic Domain do), and is not the
> governance supervisor (EchoForge supervises it over a read-only boundary). It owns *which mandates
> apply and whether they are satisfied* — authoritatively, deterministically, reproducibly.

## An independent node — the first thing to understand

RBM-MDL-Layer **owns its own doctrine, in full.** Every other system — CFRS, EchoForge, LEAL, the
Economic Domain, UPM, PERSE, RESA, Atlas, and every business node — is a **consumer** of this
constitution, never an owner of it and never a dependency it assumes into existence. The MDL capability
was first built inside CFRS; that history never made CFRS the owner of what the doctrine governs. Read
**[`MDL_Consumer_Model.md`](./MDL_Consumer_Model.md)** first: it is the interpretive key — *roles bind;
named occupants only illustrate; the node stands alone.*

## This is a constitutional sprint, not an implementation sprint

This repository contains **doctrine only** — no services, APIs, database models, migrations, or
integrations, by deliberate design. The constitutional, architectural, and governance layer is settled
*before* any capability is built, so a decade of implementation can evolve without rewriting the
authority boundaries. The doctrine is authored to be **consistent with** the three uploaded operational
specs (Mandate Definition Layer Specification v1.0, MDL ↔ EchoForge Service Contract v1, Jurisdiction
Stack Model v1.0); the one place the sources conflict with each other is reported in
[`Open_Questions_and_Risks.md`](./Open_Questions_and_Risks.md) Part A.

## The documents

**Read in this order:**

| # | Document | What it settles |
|---|---|---|
| 0 | **[`MDL_Consumer_Model.md`](./MDL_Consumer_Model.md)** | The independence key: consumers as *roles*, and the rule that consumers reference but never own. |
| 1 | **[`Immutable_Core_Charter.md`](./Immutable_Core_Charter.md)** | The charter: mission, purpose, scope, non-goals, authority, the five immutable guarantees. |
| 2 | **[`MDL_Infrastructure_Constitution.md`](./MDL_Infrastructure_Constitution.md)** | The governing doctrine: mandate truth, authority, ownership, the mandate object, events, determinations, governance, principles. |
| 3 | **[`MDL_Ownership_Analysis.md`](./MDL_Ownership_Analysis.md)** | Phase-1 evidence-backed ownership analysis: what MDL is, why it is infrastructure, what it owns and does not. |
| 4 | **[`MDL_Truth_Ownership_Matrix.md`](./MDL_Truth_Ownership_Matrix.md)** | Per truth (mandates, regulations, policy, contracts, jurisdiction, financial overrides, eligibility, validation, enforcement, audit, risk, governance, execution): authors / owns / consumes / modifies / observes. |
| 5 | **[`MDL_Responsibility_Matrix.md`](./MDL_Responsibility_Matrix.md)** | Owner / Author / Reader / Writer / Actor / Supervisor / Audit Authority per mandate concern. |
| 6 | **[`MDL_Capability_Framework.md`](./MDL_Capability_Framework.md)** | Capabilities classified Core / Optional / Future / External. |
| 7 | **[`MDL_Lifecycle.md`](./MDL_Lifecycle.md)** | The Definition lifecycle + the Application lifecycle, and the jurisdiction stack. |
| 8 | **[`MDL_Internal_Architecture.md`](./MDL_Internal_Architecture.md)** | The eleven permanent layers. |
| 9 | **[`MDL_External_Interfaces.md`](./MDL_External_Interfaces.md)** | Least-privilege interface matrix per node (consumes / publishes / receives events / reads only / admin). |
| 10 | **[`MDL_Consumption_Model.md`](./MDL_Consumption_Model.md)** | How consumers integrate, and the "compliance zone" obligations. |
| 11 | **[`MDL_Event_Model.md`](./MDL_Event_Model.md)** | The mandate-domain event doctrine and scoped propagation. |
| 12 | **[`MDL_Repository_Blueprint.md`](./MDL_Repository_Blueprint.md)** | The recommended repository layout — architecture only. |
| 13 | **[`Repository_Ownership_Report.md`](./Repository_Ownership_Report.md)** | Does MDL deserve its own repo? (Yes) + the single-owner map. |
| 14 | **[`Migration_Strategy_CFRS_to_RBM_MDL.md`](./Migration_Strategy_CFRS_to_RBM_MDL.md)** | The strangler-fig migration from CFRS's embedded MDL. |
| 15 | **[`MDL_Infrastructure_Roadmap.md`](./MDL_Infrastructure_Roadmap.md)** | The 10–20 year roadmap. |
| 16 | **[`MDL_vs_Industry_Systems.md`](./MDL_vs_Industry_Systems.md)** | Honest comparison vs OPA, Cedar, Verified Permissions, ServiceNow, rule/eligibility/workflow engines, and the Trust Runtime. |
| 17 | **[`institutional-evaluation/IEF_Classification.md`](./institutional-evaluation/IEF_Classification.md)** | The Institutional Evaluation Framework applied to this node. |
| 18 | **[`innovation/IAF_Innovation_Assessment.md`](./innovation/IAF_Innovation_Assessment.md)** | The Innovation Assessment Framework applied to this node. |
| 19 | **[`Architectural_Constraints.md`](./Architectural_Constraints.md)** | The binding constraints (ecosystem-position + invariant). |
| 20 | **[`Open_Questions_and_Risks.md`](./Open_Questions_and_Risks.md)** | Open questions, risks, and the **Conflict & Source-Reconciliation Report**. |
| 21 | **[`Repository_Independence_Review.md`](./Repository_Independence_Review.md)** | The independence audit and the standing anti-regression rule. |

## The rules that govern this repository

1. **One authoritative owner per mandate truth.** No duplicates, no forks, no competing resolution
   engines.
2. **Consumers reference; they never own.** Every consumer adapts to this node; the node adapts to no
   consumer.
3. **Roles bind; occupants illustrate.** No clause depends on a named runtime existing.
4. **Compile, don't legislate; determine, don't act.** The node owns the resolved determination, never
   the source law, the money, or the act.

## Where this node sits

RBM-MDL-Layer is an independent infrastructure node (registered as `node_type:
governance-infrastructure`). It relates to every other system by **consumer role**
(`MDL_Consumer_Model.md`): a Human Ratifying Authority ratifies it; Mandate Authoring Authorities author
the obligations it compiles; a Governance Supervisor monitors it read-only; Business-Node and Economic
consumers act on its determinations; a peer Discipline-Determination Provider answers discipline law;
Intelligence and Auditor consumers read. Change the occupants and the constitution is unchanged.

## Status

**Foundational — constitutional foundation established this sprint. Ratification of the internal doctrine
rests with the Human Ratifying Authority**, evidenced by human sign-off, not self-ratified.

**RATIFIED — 2026-07-14 (`Ratification_Log.md`).** The constitutional foundation is **ratified** (R1) and is
the governing document. The Human Ratifying Authority has also ratified: the **canonical jurisdiction stack**
(R2, FEDERAL-anchored two-class model — `MDL_Lifecycle.md` §4), the **four constitutional governance roles**
(R3 — `MDL_Consumer_Model.md` §1a), and the **revocation / void-ab-initio doctrine** (R4 —
`MDL_Revocation_And_Invalidation.md`). The interim ratification authority is the **Founder**
(`Ratification_Authority.md`). No implementation exists yet; the build may proceed per
`Architecture_Validation_Report.md` §3.
