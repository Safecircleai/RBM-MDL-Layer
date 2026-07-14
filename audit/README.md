# audit/ — Mandate Audit Trail (Architecture Layer 9)

**Status:** PLACEHOLDER — not yet implemented. Architecture and doctrine only; no code, schema, or
migration exists here during the constitutional phase, by design.

**Hosts (future):** Append-only, immutable record of mandate mutations, determinations, and override approvals.

**Governed by:** `../MDL_Infrastructure_Constitution.md` (§6 Determinations & State) and
`../MDL_Internal_Architecture.md` (Layer 9).

**This directory may NEVER contain:** Edited or deleted audit entries; out-of-scope PII.

When implementation begins, it lands here — not at the repository root, which stays the immutable
constitutional layer (`../MDL_Repository_Blueprint.md`). Any code added here must cite the governing
clause above; code that crosses the "may never contain" line is a detectable violation, not a silent one.
