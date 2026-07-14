# interfaces/ — Consumption & Supervision (Architecture Layer 11)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** The consumption entry points and the read-only supervision boundary.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§9; External Interfaces) and
`../MDL_Internal_Architecture.md` (Layer 11).

**This directory may NEVER contain:** An over-privileged consumer projection; write access for the Governance Supervisor.

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
