# Doctrine Freeze — v1.0

**Frozen:** 2026-07-14, on `Constitutional_Traceability_Review.md` reaching **architectural closure** and on
the ratifications in `Ratification_Log.md` (R1–R4).
**Frozen by authority of:** the Human Ratifying Authority (interim occupant: the Founder,
`Ratification_Authority.md`).
**Version:** **v1.0** (git tag `v1.0`).

---

## What "frozen" means

The constitutional and engineering doctrine of RBM-MDL-Layer is **closed and stable at v1.0**. Every runtime
behavior is owned by exactly one doctrine and one capability; every clause and specification trace to each
other in both directions (`Constitutional_Traceability_Review.md`). From this point:

> **No new doctrine unless implementation proves a constitutional defect.**

This is the discipline that keeps the MDL from growing indefinitely and preserves the integrity of the
architecture. A "constitutional defect" is a contradiction, an unowned behavior, a boundary breach, or an
impossibility that **implementation actually demonstrates** — not a topic that merely could be elaborated.

## The freeze rule, operationally

- **Allowed without unfreezing:** implementation code and tests; the implementation-era cleanups noted as
  non-blocking in `Constitutional_Traceability_Review.md` §7; recording ratifications the HRA issues.
- **Requires the HRA to unfreeze (a new ratified version, e.g. v1.1):** any change to a constitutional clause,
  an ownership/boundary, the jurisdiction stack, the role model, an immutable guarantee, or a capability's
  owned truth.
- **The three recorded deferrals** (discipline-determination consumption; authority-lineage/delegation
  detection; retention-vs-erasure) are the *expected* sites of a future ratified amendment; addressing any of
  them is a new ratified version, not an edit under the freeze.

## What is frozen (the v1.0 corpus)

The root constitutional layer (Consumer Model, Immutable Core Charter, Infrastructure Constitution, Ownership
Analysis, Truth Ownership Matrix, Responsibility Matrix, Capability Framework, Lifecycle incl. the ratified
jurisdiction stack, Internal Architecture, External Interfaces, Consumption Model, Event Model, Revocation &
Invalidation, Repository Blueprint, Ownership Report, Migration Strategy, Roadmap, Industry Comparison, IEF,
IAF, Architectural Constraints, Open Questions & Risks, Independence Review, Ratification Authority,
Ratification Log, Jurisdiction Stack Ratification Analysis, Constitutional Traceability Review), the
`engineering/` specifications, and the reports (Audit, Validation) as the point-in-time record.

## Next: implementation

Begin implementation exactly as the build order specifies
(`Architecture_Validation_Report.md` §3):

```
Audit → Registry → Authoring → Versioning → Jurisdiction → Resolution → Determination → Snapshot → Consumption
```

Override and Distribution are additive after a functioning single node. Each component is implemented against
its contract in `engineering/MDL_Component_Contracts.md`; each traces to a frozen clause.
