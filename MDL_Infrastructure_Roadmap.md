# MDL Infrastructure Roadmap (10–20 Year Horizon)

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only — this sequences capability, not code.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Reads with:** `Migration_Strategy_CFRS_to_RBM_MDL.md`
(the extraction path), `MDL_Capability_Framework.md` (the tiers being sequenced).

**Design horizon:** the brief mandates building "for the next 10–20 years, not the next sprint." Every
era below adds *consumers and jurisdiction layers*, never re-cuts a boundary — the property the
constitution's Principle 10 exists to guarantee.

---

## Era 0 — Constitutional foundation (this sprint)
- Doctrine complete: constitution, matrices, lifecycle, architecture, interfaces, event model, IEF/IAF,
  migration, blueprint. **No implementation.**
- Exit: ratification by the Human Ratifying Authority.

## Era 1 — Faithful extraction (Migration S1–S5)
- Stand up the eleven layers against the uploaded engine contract; lift CFRS's mandate data preserving
  snapshot immutability; prove determinism parity in shadow mode; cut over behind a flag; retire CFRS's
  embedded engine.
- **Capabilities:** all Core (`MDL_Capability_Framework.md` §1), scoped to FLEET/NY (faithful to today).
- Exit: RBM-MDL-Layer is the single authoritative mandate engine for its first consumer; the IEF
  "depended upon" test is *one consumer* from passable.

## Era 2 — Generalization (Migration S6)
- Activate the modeled node types (HOUSING, HUMAN_SERVICES, CONSTRUCTION, PROCUREMENT, WORKFORCE,
  PROPERTY_MGMT, ENTERTAINMENT) and jurisdictions beyond NY; onboard a second business node (e.g. a
  Housing/UPM consumer).
- **Capabilities:** Optional tier — Participation Aggregation, Eligibility Determination, Conflict-Review
  Queue, Consumer Registration.
- Exit: two+ independent business nodes depend on the node → the IEF layer classification can move from
  *pre-implementation specification* toward *infrastructure* on evidence, not aspiration.

## Era 3 — Federation (Migration S7; Deployment Phase 3)
- Event-driven distributed enforcement; scoped cross-node propagation live; the node operates as the
  "internal governance microservice with unified enforcement" (uploaded *Propagation Protocol* §5).
- **Capabilities:** Future tier — Event-Driven Distributed Enforcement, Multi-Tenant Isolation at Scale.
- Exit: a federation of independently deployed nodes consumes one mandate authority without duplication.

## Era 4 — Composition with the discipline plane
- Formalize the seam with the Trust Runtime: mandates whose satisfaction requires a discipline
  determination (HIPAA/Legal/Tax/PCI) consume the peer's `outcome` as an input.
- **Capabilities:** Future tier — Discipline-Determination Consumption.
- Exit: mandate ↔ discipline composition is live and non-duplicative; both nodes' doctrine cross-reference
  the seam (`Open_Questions_and_Risks.md`).

## Era 5 — Mandate intelligence & external standard
- The authoritative data substrate for mandate-coverage/drift analytics (read-only, aggregate) feeds
  Intelligence consumers; explore the speculated external multi-jurisdiction-compliance offering
  (`RBM_CAPABILITIES_V1.md:1635`) only if the node has earned infrastructure/institution status by then.
- **Capabilities:** Future tier — Mandate Intelligence (data).
- Exit: the node is depended-upon infrastructure with an evidenced institution claim (the IEF
  re-evaluation at reduction-to-practice, then at operator-persistence, can finally be met).

---

## The three properties every era must preserve (the 20-year invariants)

1. **Determinism** — never introduce a random or model-driven step into resolution/determination, at any
   scale (`MDL_Infrastructure_Constitution.md` §1.2).
2. **Snapshot immutability** — a determination frozen in Era 1 must reproduce identically in Era 5.
3. **One authoritative owner** — federation multiplies *deployments*, never *authorities*; there is always
   exactly one owner of a given mandate truth.

Any roadmap item that would violate one of these is not a future era; it is an unconstitutional proposal,
escalated to the Human Ratifying Authority rather than scheduled.
