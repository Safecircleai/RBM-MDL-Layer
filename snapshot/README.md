# snapshot/ — Snapshot & Immutability (Architecture Layer 6)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** Immutable freezing of the resolved configuration + result; results reference snapshots, not live records.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§1 Mandate Truth) and
`../MDL_Internal_Architecture.md` (Layer 6).

**This directory may NEVER contain:** Snapshot mutation; a result that references a live mandate record instead of a snapshot.

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
