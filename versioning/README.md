# versioning/ — Versioning & Effectivity (Architecture Layer 3)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** Version chains, supersession links, effective/sunset windows.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§4 The Mandate Object) and
`../MDL_Internal_Architecture.md` (Layer 3).

**This directory may NEVER contain:** Mutation of a prior version's behavior; deletion of any version (breaks snapshot references).

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
