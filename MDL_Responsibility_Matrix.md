# The MDL Responsibility Matrix

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Companion:** `MDL_Truth_Ownership_Matrix.md`
(per-truth ownership), `MDL_External_Interfaces.md` (who may see what). This document says *who is
responsible*; the truth matrix says *what is owned*; the interfaces doc says *who may see*.

---

## 0. The seven responsibilities, defined

For every mandate concern, this matrix assigns exactly seven responsibilities. Defining them precisely
is what keeps the matrix from collapsing into a vague "who's in charge":

- **Owner** — the single accountable party for the *authoritative truth* of this concern. Exactly one,
  always.
- **Author** — who creates the *source* the owner compiles (the obligation, the policy, the stack).
- **Reader** — who may read this concern's truth (bounded by `MDL_External_Interfaces.md`).
- **Writer (the act)** — who may change it, and by what act. For mandates the only legitimate write is a
  governed authoring/versioning event; determinations are written only by the domain's engine.
- **Actor** — who performs the real-world business/economic action the determination governs (distinct
  from who determines it).
- **Supervisor** — who monitors the concern read-only and may escalate (never defines/alters/disables).
- **Audit Authority** — who may verify the concern after the fact, read-only.

The recurring shape is the **AUTHOR / RESOLVE / ACT** split with a **SUPERVISE** overlay: authoring is
external, resolution/determination is the domain's, action is the consumer's, and supervision is the
Governance Supervisor's read-only oversight.

---

## 1. The matrix

Every cell names the **MDL domain** or a **consumer role** (`MDL_Consumer_Model.md`), never a runtime.

| Mandate concern | Owner (truth) | Author (source) | Reader | Writer (the act) | Actor (executes) | Supervisor | Audit Authority |
|---|---|---|---|---|---|---|---|
| **Mandate definition & versioning** | **MDL domain** | Mandate Authoring Authority | All consumers (own scope) | MDL domain, via governed authoring + version events | — | Governance Supervisor (read-only) | Auditors, Human Ratifying Authority |
| **Jurisdiction resolution & precedence** | **MDL domain** | Ratified doctrine (this repo) | Business-Node, Economic | MDL domain (deterministic resolver) | — | Supervisor | Auditors |
| **Applicability resolution** | **MDL domain** | — | Business-Node (own context) | MDL domain (resolver) | Business-Node passes context | Supervisor | Auditors |
| **Satisfaction determination (validation)** | **MDL domain** | — | Business-Node, Economic, Auditor | MDL domain (engine, deterministic) | Business-Node gates on result | Supervisor | Auditors |
| **Snapshot (immutable audit artifact)** | **MDL domain** | — | Auditors, Supervisor, consumers | MDL domain (append-only; never mutated) | — | Supervisor | Auditors, Regulators |
| **Financial override determination** | **MDL domain** | Mandate Authoring Authority (exempting policy) | Economic Consumer, Business-Node | MDL domain (as a mandate rule) | **Economic Consumer** books zero tax | Supervisor (anomaly-detects) | Auditors, Tax Authorities |
| **Override / exception grant** | **MDL domain** (evaluates at runtime) | Requestor + Approver (dual auth) | Business-Node, Supervisor | MDL domain records; requestor/approver author the grant | Business-Node honors runtime outcome | Supervisor (override-frequency) | Auditors |
| **Enforcement (act on determination)** | MDL domain owns the *determination* | — | Business-Node | MDL domain (determination) | **Business-Node Consumer** (the gating act) | Supervisor intercepts bypass | Auditors |
| **Cross-node propagation** | **MDL domain** (sole publisher) | — | Subscribed nodes | MDL domain (emits events) | Nodes react (subscribe) | Supervisor (monitors versions) | Auditors |
| **Risk scoring of behavior** | **Governance Supervisor** / Intelligence | — | Intelligence, Governance Supervisor | Supervisor / Intelligence (own models) | the Supervisor/Intelligence's own upstream acts on it (outside MDL) | — | Auditors |
| **Mandate-authoring governance workflow** | **MDL domain** | Ratified doctrine | ops/authoring roles, Supervisor | MDL domain (governed workflow) | — | Supervisor (read-only) | Auditors, Human Ratifying Authority |
| **Ecosystem/assistant governance doctrine** | **Doctrine-Governance Consumer** (e.g. LEAL) — never MDL | Ecosystem doctrine home | ecosystem systems/bots | Doctrine home | — | — | Auditors |
| **The business/economic execution act** | **Business-Node** / **Economic Consumer** — never MDL | — | own downstream | the acting consumer | **the acting consumer** | Supervisor (bypass only) | Auditors |

---

## 2. What the MDL domain is responsible for that nothing else is today

Reading down the Owner column, the MDL domain is the single accountable owner of: mandate definition &
versioning, jurisdiction resolution, applicability resolution, satisfaction determination, the immutable
snapshot, the financial-override determination, override runtime evaluation, and cross-node propagation.
It is the owner of **none** of: source authorship, the business act, the economic act, ecosystem/
assistant governance doctrine, or risk verdicts. That negative space is deliberate and load-bearing.

## 3. The columns that must never collapse

- **Owner (resolution) + Author (source)** must never collapse — else the domain legislates the policy
  it resolves (`MDL_Infrastructure_Constitution.md` §2).
- **Owner (determination) + Actor (execution)** must never collapse — else the domain executes the act it
  determines, becoming the node or the economic domain it serves.
- **Owner + Supervisor** must never collapse — the Governance Supervisor is a *separate* read-only role;
  it "does not define mandates … does not alter compliance results" and "cannot disable MDL enforcement"
  (uploaded *Service Contract* §2, §5). A design that folds supervision into the owner loses the
  independent check the Service Contract exists to guarantee.

A future capability proposal is tested against this matrix by checking that it collapses none of these
columns.

## 4. Reading the matrix against the interfaces

This matrix says *who is responsible*; `MDL_External_Interfaces.md` says *who may see*. They are
consistent by construction: a party is a Reader here only if the interfaces grant it that projection,
and no party is a Writer of a concern it may not, per the interfaces, even see. Where the two documents
ever appear to disagree, `MDL_Infrastructure_Constitution.md` governs and the disagreement is itself a
claim to be resolved, never left ambiguous.
