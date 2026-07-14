# Migration Strategy — CFRS MDL → RBM MDL Layer

**Status:** FOUNDATIONAL — established this sprint; ratification and any cross-repository move rest with
the Human Ratifying Authority. Architecture and doctrine only — this sequences the migration; it executes
none of it.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `Repository_Ownership_Report.md`,
`MDL_Infrastructure_Roadmap.md`, and the uploaded *MDL Spec* §10 (Portability Strategy) and *Propagation
Protocol* §5 (Deployment Model).

---

## 0. The constraint that shapes the whole migration

**CFRS retains its own MDL implementation until migration.** (Architectural constraint; uploaded *MDL
Spec* §10 "Current Phase: MDL resides inside CFRS backend.") The migration is therefore a **strangler-fig
extraction**, not a big-bang cutover: the new node stands up beside CFRS's embedded engine, proves
parity, and CFRS retires its copy only after the new node is authoritative. At no point are two authoritative
mandate engines making divergent live determinations for the same entity.

---

## 1. The three-phase deployment path (from the specs)

The uploaded specs already name the deployment phases; this strategy adopts and sequences them:

| Phase | Uploaded-spec name | This node's role |
|---|---|---|
| **Phase 1** | "MDL embedded in CFRS" (*Propagation Protocol* §5; *MDL Spec* §10) | Status quo. CFRS is authoritative. This node is doctrine only. |
| **Phase 2** | "Extract to shared service" | Stand up RBM-MDL-Layer as the standalone authority; CFRS calls it behind a flag; parity proven; CFRS retires its embedded engine. |
| **Phase 3** | "Internal governance microservice with unified enforcement" (*Propagation Protocol* §5) | Federated, event-driven cross-node enforcement; other nodes onboard. |

## 2. The migration stages (evidence-anchored, strangler-fig)

| Stage | Action | Owner | Exit criterion |
|---|---|---|---|
| **S0 — Doctrine (this sprint)** | Author this repository's constitution and architecture. | RBM-MDL-Layer | Doctrine ratified by the Human Ratifying Authority. |
| **S1 — Scaffold the node** | Build the eleven layers per `MDL_Internal_Architecture.md` against the uploaded engine contract (`resolve_applicable_mandates`, `create_mandate_snapshots`, `validate_entity_against_mandates`, `resolve_tax_policy`, `get_latest_validation_status`). | RBM-MDL-Layer | The node answers the five engine calls deterministically over a test corpus. |
| **S2 — Data lift** | Migrate CFRS's mandate data (the 9 core tables: `mandates`, `mandate_applicability`, `mandate_required_documents`, `mandate_evidence_rules`, `mandate_threshold_rules`, `mandate_participation_rules`, `mandate_execution_snapshots`, `mandate_validation_results`, `mandate_overrides`) into the node, preserving **all active mandates, all snapshots (immutable), all active overrides with expiries intact, all versions**. | RBM-MDL-Layer + CFRS | Every CFRS snapshot re-loads unchanged; determinism check: node reproduces CFRS's historical determinations from the migrated snapshots. |
| **S3 — Parity shadow** | CFRS calls the node in parallel with its embedded engine (shadow mode); results are compared. | CFRS (as consumer) | Zero divergence on a representative corpus (or every divergence explained and ratified). |
| **S4 — Cutover behind a flag** | CFRS routes MDL calls to the node behind a feature flag; the embedded engine becomes fallback only. | CFRS | CFRS runs on the node in production for the FLEET/NY scope with no regressions. |
| **S5 — Retire the embedded engine** | CFRS removes `mdl_engine.py`/`mandate.py` after the node is authoritative; capability index #115 re-points to RBM-MDL-Layer. | CFRS + index owner | CFRS holds no parallel mandate authority; `Repository_Ownership_Report.md` §4 checks pass. |
| **S6 — Generalize beyond FLEET/NY** | Activate the modeled-but-pending node types (HOUSING, HUMAN_SERVICES, CONSTRUCTION, PROCUREMENT, WORKFORCE, PROPERTY_MGMT, ENTERTAINMENT) and jurisdictions beyond NY. | RBM-MDL-Layer | Second business node (e.g. UPM/Housing) depends on the node — the IEF "depended upon" test becomes passable. |
| **S7 — Federated enforcement** | Phase-3 event-driven distributed enforcement; scoped propagation live. | RBM-MDL-Layer | Multiple independently deployed nodes consume one authority. |

## 3. What must be preserved through the migration (invariants)

1. **Snapshot immutability across the lift** — a migrated snapshot is byte-for-byte the determination it
   was; the node reproduces historical results from it (uploaded *MDL Spec* §7). This is the single
   hardest correctness requirement and S2's exit criterion.
2. **Determinism parity** — the node must return, for identical context, what CFRS returned; S3 shadow
   mode exists to prove it before cutover.
3. **No dual authority window** — at every stage exactly one engine is authoritative for a given entity;
   shadow mode is compare-only, cutover is flagged, retirement is last.
4. **Override continuity** — active overrides migrate with expiries and dual-auth records intact.

## 4. The scope-honesty note

CFRS's MDL is *hardcoded to FLEET and NY today* (`TRUST_CLAIM_AUDIT.md:39`). The migration therefore has
two distinct jobs that must not be conflated: **(a) extract** the existing FLEET/NY capability faithfully
(S1–S5), and **(b) generalize** it to the multi-vertical, multi-jurisdiction design the schema already
anticipates (S6). Job (a) is a correctness-preserving lift; job (b) is genuinely new capability. Claiming
the node is "multi-vertical" the moment it is extracted would repeat the very scope-inflation the audit
flagged. Extraction ≠ generalization.

## 5. Rollback

At every stage before S5, rollback is trivial: CFRS's embedded engine remains and can be re-flagged
authoritative. Only S5 (retirement) is one-way, and it is gated on S4 having run cleanly in production.
This is the safety property the strangler-fig sequence buys.
