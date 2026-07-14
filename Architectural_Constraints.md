# Architectural Constraints

**Status:** FOUNDATIONAL — the binding constraints on every current and future decision in this
repository. Ratification rests with the Human Ratifying Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. These constraints are the brief's stated
constraints plus the invariants the uploaded specs and the constitution make non-negotiable. A proposal
that violates any is out of order until amended by the Human Ratifying Authority.

---

## 1. The ecosystem-position constraints (from the brief)

| # | Constraint | Where it is enforced in this doctrine |
|---|---|---|
| C1 | **RBM MDL Layer is an independent infrastructure node.** | `Repository_Ownership_Report.md`; `Repository_Independence_Review.md`; `CLAUDE.md`. |
| C2 | **CFRS retains its own MDL implementation until migration.** | `Migration_Strategy_CFRS_to_RBM_MDL.md` §0 (strangler-fig; no dual authority window). |
| C3 | **EchoForge supervises; it does not own mandates.** | `MDL_External_Interfaces.md` §2; `MDL_Responsibility_Matrix.md` §3; consistent with the uploaded *Service Contract* §2. |
| C4 | **LEAL governs doctrine; it does not resolve mandates.** | `MDL_Consumer_Model.md` (Doctrine-Governance Consumer); `MDL_Truth_Ownership_Matrix.md` (Governance rows). |
| C5 | **Economic Core consumes mandate outcomes; it does not define them.** | `MDL_Truth_Ownership_Matrix.md` (Financial overrides row); §Reconciliation. |
| C6 | **Business Nodes consume MDL; they do not duplicate it.** | `MDL_Consumption_Model.md` §4; consistent with uploaded *MDL Spec* §5. |
| C7 | **Veronica is not part of the architecture.** | No document in this repository grants Veronica any role; not present in any matrix or interface. |
| C8 | **Build for the next 10–20 years, not the next sprint.** | `MDL_Infrastructure_Roadmap.md`; Constitution Principle 10. |
| C9 | **Follow the Evidence of Truth Constitution.** | `[FACT]/[PRINCIPLE]/[INFERENCE]` tagging throughout; `MDL_Ownership_Analysis.md` §0. |
| C10 | **Every assertion supported by evidence or clearly marked as inference.** | Same tagging discipline; unsourced claims are inadmissible (Constitution §1.4). |
| C11 | **Prefer correctness over elegance.** | Adopted as a standing rule (§3 below). *(The literal clause is not present in the in-tree corpus; it is honored as an explicit constraint here — `Open_Questions_and_Risks.md`.)* |

## 2. The invariant constraints (from the constitution + uploaded specs)

| # | Constraint | Source |
|---|---|---|
| I1 | **Deterministic resolution** — identical context → identical result; no randomness, no environment drift; no model in the resolution path. | Uploaded *MDL Spec* §2.2; Constitution §1.2. |
| I2 | **Snapshot immutability** — a frozen determination is never mutated; version changes never alter history; results reference snapshots, not live records. | Uploaded *MDL Spec* §2.3, §3.8, §7. |
| I3 | **Financial-override supremacy** — a mandate financial override binds over any node tax engine or manual override. | Uploaded *MDL Spec* §2.5; *Service Contract* §8. |
| I4 | **Jurisdictional precedence is explicit and deterministic** — conflicts resolve by the ratified stack + declared inheritance; same-level ambiguity is flagged, never auto-resolved. | Uploaded *Jurisdiction Stack* §1–3. |
| I5 | **One authoritative owner** — no node duplicates or forks mandate resolution. | Uploaded *MDL Spec* §5; `RBM_CAPABILITIES_V1.md` single-owner model. |
| I6 | **Authoritative, not advisory** — determinations bind consumers; a consumer acts but may not contradict. | Uploaded *MDL Spec* §2.5, §5; revises the CFRS "soft validator" framing (§3). |
| I7 | **Read-only supervision** — the Governance Supervisor may read/monitor/escalate but may never define, alter, force, or disable. | Uploaded *Service Contract* §2, §5. |
| I8 | **Compile, don't legislate** — the domain encodes/versions authored obligations; it never authors source policy. | Constitution §2; `MDL_Truth_Ownership_Matrix.md`. |
| I9 | **Resolve/act separation** — the domain determines; consumers act; the domain executes nothing and holds no value. | Constitution §3, Principle 8. |
| I10 | **Least privilege** — every consumer gets the narrowest interface its role requires; publish/admin are guarded modes. | `MDL_External_Interfaces.md`. |

## 3. The standing correctness rule (C11, made concrete)

**Prefer correctness over elegance.** Where a cleaner design would weaken any invariant in §2, the
invariant wins. Concretely: never trade snapshot immutability for storage elegance; never trade
determinism for a "smarter" (model-driven) resolver; never collapse the supervisor into the owner for
architectural tidiness; never merge the definition and application lifecycles because one clock is
simpler. Elegance that costs an invariant is a defect, not an improvement.

## 4. How a proposal is tested against these constraints

A future capability, clause, or configuration is admitted only if it violates **none** of C1–C11 and
**none** of I1–I10. A proposal that appears to require violating one is resolved by (a) changing the
proposal, or (b) a bounded, logged, ratified exception from the Human Ratifying Authority — never by
silent relaxation. A clause or config that grants itself relief from a constraint is void
(`MDL_Infrastructure_Constitution.md` §2).
