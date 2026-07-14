# MDL Repository Blueprint

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. **Architecture only. No implementation.** This document recommends the repository layout; it
does not build it.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `MDL_Internal_Architecture.md`
(the layers each directory hosts), `Repository_Ownership_Report.md`.

---

## 0. The principle behind the layout

The repository is laid out so that **the constitutional layer sits at the root, immutable and
implementation-free, and every future implementation home is a directory whose README points back up to
the doctrine that governs it.** A directory may never contain a capability whose governing constitution
it cannot cite. This keeps implementation from drifting away from doctrine over a decade: the governing
document is always one directory-level away.

The layout mirrors the *internal architecture* (`MDL_Internal_Architecture.md`), so the shape of the code
will match the shape of the constitution — registry, jurisdiction, versioning, resolution, determination,
snapshot, override, distribution, audit, governance, interfaces — not the shape of whatever policy-engine
SDK is fashionable when it is built.

---

## 1. The recommended layout

```
RBM-MDL-Layer/
│
├── README.md                              # Entry point and document index
├── CLAUDE.md                              # Repository identity & scope (independence-first, domain-centric)
├── .atlas-config.yaml                     # Ecosystem-intelligence registration (metadata, not code)
├── ATLAS_STATUS.md                        # Human-readable status projection of the above
│
│   ── THE CONSTITUTIONAL LAYER (root — immutable, implementation-free) ──
├── MDL_Consumer_Model.md                  # The independence key — roles vs. occupants
├── Immutable_Core_Charter.md              # The immutable core
├── MDL_Infrastructure_Constitution.md     # The governing doctrine
├── MDL_Ownership_Analysis.md              # Phase-1 evidence-backed ownership analysis
├── MDL_Truth_Ownership_Matrix.md          # Per-truth ownership (authors/owns/consumes/modifies/observes)
├── MDL_Responsibility_Matrix.md           # Owner/Author/Reader/Writer/Actor/Supervisor/Audit grid
├── MDL_Capability_Framework.md            # Capabilities: Core/Optional/Future/External
├── MDL_Lifecycle.md                       # Definition + Application lifecycles; the jurisdiction stack
├── MDL_Internal_Architecture.md           # The eleven permanent layers
├── MDL_External_Interfaces.md             # Least-privilege interface matrix per node
├── MDL_Consumption_Model.md               # How consumers integrate
├── MDL_Event_Model.md                     # The mandate-domain event doctrine
├── MDL_Repository_Blueprint.md            # This document
├── Repository_Ownership_Report.md         # Does MDL deserve its own repo? (yes) + ownership map
├── Migration_Strategy_CFRS_to_RBM_MDL.md  # CFRS MDL → RBM MDL Layer migration
├── MDL_Infrastructure_Roadmap.md          # The 10–20 year roadmap
├── Architectural_Constraints.md           # The binding constraints
├── Open_Questions_and_Risks.md            # Risks + the source-conflict / reconciliation report
├── Repository_Independence_Review.md      # The independence audit + standing rule
├── MDL_vs_Industry_Systems.md             # Honest comparative analysis
│
├── institutional-evaluation/              # IEF applied to this node (reference self-application)
│   └── IEF_Classification.md
├── innovation/                            # IAF applied to this node (reference self-application)
│   └── IAF_Innovation_Assessment.md
├── research/                              # Founding research — this node's single authoritative owner
│   └── README.md
│
│   ── FUTURE IMPLEMENTATION HOMES (architecture placeholders only; no code yet) ──
├── registry/        # Layer 1 — encoded, versioned mandate store
├── jurisdiction/    # Layer 2 — precedence stack + inheritance behaviors
├── versioning/      # Layer 3 — version chains, supersession, effectivity
├── resolution/      # Layer 4 — deterministic applicability resolution
├── evaluation/      # Layer 5 — satisfaction determination + financial override
├── snapshot/        # Layer 6 — immutable determination snapshots
├── overrides/       # Layer 7 — dual-authorized, expiring override evaluation
├── distribution/    # Layer 8 — event publication + scoped propagation
├── audit/           # Layer 9 — append-only mandate/determination audit trail
├── governance/      # Layer 10 — role-based authoring workflow
└── interfaces/      # Layer 11 — consumption entry points + read-only supervision boundary
```

Each future-implementation directory is a **placeholder containing only a `README.md`** that (a) states
it is not yet implemented, (b) names the layer and capability tier(s) it will host, and (c) cites the
governing section of `MDL_Infrastructure_Constitution.md` / `MDL_Internal_Architecture.md`. No code,
schema, or migration exists in any of them during the constitutional phase — by design.

---

## 2. Why each directory exists, and what it may never contain

| Directory | Hosts (future) | Governed by | May **never** contain |
|---|---|---|---|
| `registry/` | The encoded, versioned mandate store | Constitution §4; Arch layer 1 | A second competing mandate store; source-policy authorship |
| `jurisdiction/` | Precedence stack + inheritance | Lifecycle §4; Arch layer 2 | Ad-hoc conflict resolution; auto-resolution of same-level ambiguity |
| `versioning/` | Version chains, effectivity | Constitution §4; Arch layer 3 | Mutation of a prior version; deletion of a version |
| `resolution/` | Deterministic applicability | Constitution §1.2; Arch layer 4 | Any random or model-driven step |
| `evaluation/` | Satisfaction determination + financial override | Constitution §6; Arch layer 5 | Advisory-only results; discipline legal reasoning |
| `snapshot/` | Immutable snapshots | Constitution §1; Arch layer 6 | Snapshot mutation; live-record references |
| `overrides/` | Dual-auth expiring overrides | Constitution §7; Arch layer 7 | Snapshot mutation; unapproved overrides |
| `distribution/` | Event publication + propagation | Constitution §5; Arch layer 8 | Consumer-emitted events; snapshot mutation on propagation |
| `audit/` | Append-only trail | Constitution §6; Arch layer 9 | Edited/deleted audit entries; out-of-scope PII |
| `governance/` | Authoring workflow | Constitution §7; Arch layer 10 | Source-obligation authorship; non-RBAC writes |
| `interfaces/` | Consumption + supervision boundary | Constitution §9; Arch layer 11 | Over-privileged projections; supervisor write access |

The right-hand column is load-bearing: it encodes the non-goals of `Immutable_Core_Charter.md` §4 and the
constitution's principles into the directory structure, so a future contributor is told, at the directory
level, what does not belong there before writing a line.

---

## 3. What is deliberately absent

There is no `models/`, `migrations/`, `services/`, or `api/` at the constitutional foundation, because
none exists yet and their premature presence would imply an implementation the constitution has not
authorized. When implementation begins, it lands inside the governed directories above — not at the root,
which stays the immutable constitutional layer. The `.atlas-config.yaml` and `ATLAS_STATUS.md` are the
only non-document files at the foundation, and they are ecosystem metadata, not implementation.

## 4. How the structure protects the constitution over time

1. **Doctrine at the root, code in subdirectories** — the constitution is never buried inside an
   implementation package and can be amended without touching code.
2. **Every implementation home cites its governing clause** — drift is visible: a directory whose code no
   longer matches its cited constitution is a detectable violation, not a silent one.
3. **The "may never contain" column is structural** — non-goals are enforced at the layout level, not
   left to a reviewer's memory.
4. **The layout matches the internal architecture, not a vendor** — changing policy-engine, protocol, or
   deployment never reshapes the repository; only the contents of the layer directories change.
