# registry/ — Mandate Registry (Architecture Layer 1)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** The authoritative store of encoded, versioned mandates and their rule sets.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§4 The Mandate Object) and
`../MDL_Internal_Architecture.md` (Layer 1).

**This directory may NEVER contain:** A second competing mandate store; authorship of any source obligation (law, contract, org policy).

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
