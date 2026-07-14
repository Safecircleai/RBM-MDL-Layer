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

## Known risks

- Doctrine only; no runtime capability yet (readiness intentionally low).
- **Canonical jurisdiction stack unresolved** — the uploaded MDL Specification and Jurisdiction Stack
  Model disagree on precedence ordering (see `Open_Questions_and_Risks.md` A1). Needs ratification before
  implementation.
- Internal doctrine is a proposed foundation pending constitutional ratification by the Human Ratifying
  Authority.

## Recommended next action

Ratify (a) the internal mandate doctrine and (b) the canonical jurisdiction stack, by the Human Ratifying
Authority, evidenced by recorded human sign-off. Implementation then proceeds by strangler-fig extraction
from CFRS per `Migration_Strategy_CFRS_to_RBM_MDL.md` — not before.
