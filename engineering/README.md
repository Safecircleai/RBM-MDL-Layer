# MDL Engineering Specifications (Phase 5)

Engineering specifications derived directly from the constitutional layer
(`../MDL_Infrastructure_Constitution.md`) and the buildability validation
(`../Architecture_Validation_Report.md`). These are **not doctrine** — they translate the validated
architecture into specifications an engineer can implement **without making architectural decisions**. They
contain no code, APIs, schemas, database design, or endpoints, and they introduce no capability or boundary
beyond the eleven Core capabilities already validated.

Where a specification depends on an input that is not yet ratified, it is marked **[BLOCKED-INPUT]** and the
input is named — it is never decided in the specs (deciding is the HRA's).

**RATIFICATION UPDATE — 2026-07-14 (`../Ratification_Log.md`).** The three inputs these specs were blocked on
are now **RATIFIED**: the **canonical jurisdiction stack** (R2, `../MDL_Lifecycle.md` §4), the **authoring
roles** (R3, four constitutional roles — `../MDL_Consumer_Model.md` §1a), and **revocation/void-ab-initio**
(R4, `../MDL_Revocation_And_Invalidation.md`). Residual `[BLOCKED-INPUT]` markers in these documents refer now
only to the **detection** of invalid authority (delegation / authority-lineage), which remains open. The specs
are otherwise fully implementable in the build order of `../Architecture_Validation_Report.md` §3.

| # | Document | Defines |
|---|---|---|
| 1 | [`MDL_Runtime_Specification.md`](./MDL_Runtime_Specification.md) | Runtime responsibilities, execution flow, deterministic/authoring/read/propagation paths, failure/retry/idempotency/concurrency boundaries. |
| 2 | [`MDL_Domain_Model.md`](./MDL_Domain_Model.md) | Every permanent domain object: purpose, owner, lifecycle, immutable/mutable fields, relationships, invariants (conceptual). |
| 3 | [`MDL_State_Model.md`](./MDL_State_Model.md) | Every state machine (Mandate Version, Override, Determination, Conflict-Review): transitions, invariants, illegal transitions, recovery. |
| 4 | [`MDL_Persistence_Model.md`](./MDL_Persistence_Model.md) | Immutable / append-only / mutable / derived / projected / reconstructed classification; retention; historical preservation; snapshot guarantees. |
| 5 | [`MDL_Runtime_Sequence_Model.md`](./MDL_Runtime_Sequence_Model.md) | End-to-end runtime sequences: author→publish, resolve→determine→snapshot→return, override, propagation, version upgrade, jurisdiction conflict, retirement, re-evaluation. |
| 6 | [`MDL_Component_Contracts.md`](./MDL_Component_Contracts.md) | Per-component engineering contracts: consumes / produces / owns / cannot own / dependencies / guarantees / failure conditions. |

**Reading order:** Runtime Specification → Domain Model → State Model → Persistence Model → Sequence Model →
Component Contracts. The first frames behavior; the middle three define the things and their states and
storage; the last two show how the components interact and contract with each other.
