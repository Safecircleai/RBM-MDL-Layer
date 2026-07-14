# jurisdiction/ — Jurisdiction Resolution (Architecture Layer 2)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** The precedence stack and inheritance behaviors (FLOOR/ADDITIVE/OVERRIDE); cross-layer ordering and reconciliation.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§1.2 Determinism; Lifecycle §4) and
`../MDL_Internal_Architecture.md` (Layer 2).

**This directory may NEVER contain:** Ad-hoc conflict resolution; auto-resolution of a same-level, ambiguous conflict (it must be flagged for review).

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
