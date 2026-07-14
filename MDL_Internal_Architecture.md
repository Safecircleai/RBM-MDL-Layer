# MDL Internal Architecture — The Permanent Layers

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only — this names the permanent layers; it implements none of them.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `MDL_Lifecycle.md`,
`MDL_Capability_Framework.md`, `MDL_Repository_Blueprint.md` (the directory that hosts each layer).

---

## 0. What a "permanent layer" is, and how these were chosen

A **permanent layer** is a separation of concern that must exist for a decade regardless of
implementation — because removing it would collapse a boundary the constitution requires. The brief's
example list (Registry, Jurisdiction, Resolution, Version, Snapshot, Distribution, Override, Audit) is a
good start; this document does not copy it blindly. Each layer below is justified from a constitutional
invariant or a spec requirement, and three layers are *added* to the example (**Determination**,
**Governance/Authoring**, **Interface**) because the example omits where compliance is *judged*, where
mandates are *authored under control*, and how consumers *reach* the node — each a boundary the specs
require. One example layer is *merged* (Version folded into **Versioning & Effectivity**).

The layers divide into three zones by the constitution's determinism rule (§1.2):
- **The deterministic core** (no randomness, no model): Registry, Jurisdiction, Versioning, Resolution,
  Determination, Snapshot, Override.
- **The distribution & memory zone**: Distribution, Audit.
- **The control & access zone**: Governance/Authoring, Interface.

---

## 1. The eleven permanent layers

| # | Layer | Responsibility | Owns (capability) | May **never** do | Justified by |
|---|---|---|---|---|---|
| 1 | **Registry** | Store encoded, versioned mandates and rule sets as the single source of mandate definitions. | Mandate Registry | Hold a second competing mandate store; author source policy. | Single-owner truth (uploaded *MDL Spec* §3, §5). |
| 2 | **Jurisdiction** | Hold the precedence stack + inheritance behaviors; order and reconcile mandates across layers. | Jurisdiction Resolution | Resolve conflicts ad hoc; auto-resolve a same-level ambiguity (must flag). | Deterministic precedence (uploaded *Jurisdiction Stack* §1–3). |
| 3 | **Versioning & Effectivity** | Version chains, supersession, effective/sunset windows. | Versioning & Effectivity | Mutate a prior version's behavior; delete a version. | Immutable-per-version (uploaded *MDL Spec* §7). |
| 4 | **Resolution** | Deterministically compute the applicable mandate set for an entity context. | Applicability Resolution | Return non-deterministic or environment-dependent results; contain any model/random step. | Determinism (uploaded *MDL Spec* §2.2, §4.1). |
| 5 | **Determination (Validation)** | Evaluate entity state against the resolved set → authoritative compliance result + financial override. | Satisfaction Determination, Financial-Override Determination | Emit an *advisory* result a consumer may ignore; perform discipline legal reasoning. | Authoritative determination (`MDL_Infrastructure_Constitution.md` §6; uploaded *MDL Spec* §2.5, §4.3). |
| 6 | **Snapshot** | Freeze the resolved configuration + result as an immutable artifact; bind results to snapshots. | Snapshot & Immutability | Mutate a snapshot; let a result reference a live record instead of a snapshot. | Snapshot immutability (uploaded *MDL Spec* §2.3, §3.8). |
| 7 | **Override** | Evaluate dual-authorized, expiring overrides that modify runtime outcome. | Override / Exception Evaluation | Mutate a snapshot; apply an override without approval/expiry/reason. | Non-mutating overrides (uploaded *MDL Spec* §8; *Service Contract* §7). |
| 8 | **Distribution** | Publish mandate-domain events; propagate updates scoped by jurisdiction; manage subscriptions. | Consumption Interface & Propagation (event side) | Let a consumer emit mandate-domain events; mutate snapshots on propagation. | Sole publisher; snapshot isolation (uploaded *Service Contract* §4; *Propagation Protocol* §2–3). |
| 9 | **Audit** | Append-only, immutable record of mutations, determinations, and override approvals. | Mandate Audit Trail | Edit or delete an audit entry; expose PII beyond scope. | Audit-trail integrity (uploaded *MDL Spec* §9). |
| 10 | **Governance / Authoring** | Role-based intake→encode→review→approve→version workflow for mandates. | Authoring & Governance Workflow | Author a source obligation; let a non-authoring role write a mandate. | Compile-not-legislate; RBAC (uploaded *Service Contract* §7). |
| 11 | **Interface** | The consumption entry points and the read-only supervision boundary. | Consumption Interface (request side) | Grant a consumer more than its least-privilege projection; give the Supervisor write access. | Least privilege; read-only supervision (uploaded *Service Contract* §3; `MDL_External_Interfaces.md`). |

## 2. How a request flows through the layers (the deterministic path)

A consumer's `resolve`/`validate`/`tax-policy` call traverses, in order:

```
Interface (authenticate, scope)
   → Resolution (applicability) ─uses→ Registry + Versioning + Jurisdiction
   → Determination (validate state) ─produces→ compliance result + financial override
   → Snapshot (freeze) ─consults→ Override (runtime outcome)
   → Interface (return determination)   ⟶ Audit (record)   ⟶ Distribution (emit event)
```

Every step from Resolution through Snapshot is on the **deterministic path**: identical context yields an
identical snapshot. Audit and Distribution are off-path side effects that never alter the determination.
The Governance/Authoring layer is a *separate* write path used only by authoring roles, never by a
consuming request.

## 3. Why this layering holds for a decade

1. **Determinism is structural, not conventional.** Randomness and models are excluded from layers 1–7 by
   design, so the reproducibility invariant cannot erode as features are added.
2. **The write path and the read path are separate layers.** Authoring (layer 10) and consumption (layer
   11) never share a code path, so a consumer can never become an author by accident.
3. **Supervision is a read-only edge of the Interface layer**, not a layer with reach into the core — so
   the Governance Supervisor can watch everything and change nothing (uploaded *Service Contract* §2).
4. **Each layer maps to exactly one directory** (`MDL_Repository_Blueprint.md`), so drift is visible: a
   directory whose future code crosses a layer's "may never do" is a detectable violation, not a silent
   one.
