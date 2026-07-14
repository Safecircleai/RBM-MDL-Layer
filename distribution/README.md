# distribution/ — Distribution & Propagation (Architecture Layer 8)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** Event publication and jurisdiction-scoped propagation; subscription management.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§5 Mandate Events) and
`../MDL_Internal_Architecture.md` (Layer 8).

**This directory may NEVER contain:** Consumer-emitted mandate-domain events; snapshot mutation on propagation.

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
