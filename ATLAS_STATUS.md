# ATLAS_STATUS — RBM MDL Layer

**Human-readable projection of `.atlas-config.yaml` for the ecosystem intelligence layer. Metadata, not
implementation.**

| Field | Value |
|---|---|
| **Node** | RBM MDL Layer (`rbm-mdl-layer`) |
| **Repository** | safecircleai/RBM-MDL-Layer |
| **Layer** | Infrastructure |
| **Classification** | Governance Infrastructure — Constitutional Node (Mandate Definition Layer) |
| **node_type** | `governance-infrastructure` |
| **Operational status** | Foundational (doctrine only) |
| **Readiness** | 5 / 100 — constitutional foundation set; no implementation |
| **Constitutional dependencies** | None (independent node) |
| **Operational dependencies** | None yet |

## What this node is

The single authoritative owner of the ecosystem's **resolved-mandate truth** — which mandates apply, at
what version, in which jurisdiction, and whether an entity satisfies them, frozen as immutable snapshots.
It compiles authored obligations; it does not author the source law, execute the act, or supervise the
ecosystem. It is an **independent infrastructure node** — not the CFRS implementation, and not hosted
inside EchoForge.

## Current milestone

Constitutional foundation established this sprint (21 doctrine documents + IEF/IAF applications). No
services, APIs, schemas, or migrations exist — by design.

## Ratifications (2026-07-14 — `Ratification_Log.md`, interim HRA: the Founder)

- **R1 Constitutional foundation — RATIFIED** (governing document).
- **R2 Canonical jurisdiction stack — RATIFIED** (FEDERAL-anchored two-class model; PRIME-apex rejected).
- **R3 Four constitutional governance roles — RATIFIED** (HRA + Author/Reviewer/Publisher; separation of duties).
- **R4 Revocation / void-ab-initio — RATIFIED** (own doctrine; remediation half).

## Known risks

- Doctrine only; no runtime capability yet (readiness intentionally low).
- **Authority-lineage / delegation** (the *detection* of invalid authority) still to be ratified — R4 ratified
  the *remediation*, not the detection.
- Retention vs data-erasure under never-delete immutability remains an open constitutional pressure
  (`engineering/MDL_Persistence_Model.md` §7).

## Recommended next action

The constitution and its four gating decisions are ratified. Implementation may proceed in the build order of
`Architecture_Validation_Report.md` §3, by strangler-fig extraction
from CFRS per `Migration_Strategy_CFRS_to_RBM_MDL.md` — not before.
