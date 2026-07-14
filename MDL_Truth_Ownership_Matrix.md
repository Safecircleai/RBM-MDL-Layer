# The MDL Truth Ownership Matrix

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Companion:** `MDL_Responsibility_Matrix.md`
(per-responsibility grid), `MDL_Consumer_Model.md` (the roles used below).

---

## 0. The five questions, per truth

For every truth that touches mandates, this matrix answers exactly five questions, so no truth is left
with an ambiguous owner:

- **Authors** — who creates the *source* of this truth (the obligation, the policy, the stack).
- **Owns (authoritative)** — the single accountable owner of the *authoritative form* of this truth.
  Exactly one, always.
- **Consumes** — who reads and acts on it.
- **May modify** — who may change it, and by what act.
- **May only observe** — who may read it but never change it.

The recurring shape is the **AUTHOR / RESOLVE / ACT** split (`MDL_Infrastructure_Constitution.md` §1):
the authority authors the source, the mandate domain resolves/determines the authoritative truth, and a
consumer acts. Keeping these separate is what stops the mandate domain from silently legislating policy
or from being reduced to advisory noise.

---

## 1. The matrix

Every cell names the **mandate domain** or a **consumer role** (`MDL_Consumer_Model.md`), never a
runtime. "MDL domain" = this node.

| Truth | Authors | Owns (authoritative) | Consumes | May modify | May only observe |
|---|---|---|---|---|---|
| **Mandates** (the encoded, versioned obligation) | Mandate Authoring Authority authors the *source*; **MDL domain** authors the *encoding* | **MDL domain** | Business-Node, Economic, Supervisor, Auditor consumers | **MDL domain** only, via governed authoring + versioning | All consumers |
| **Regulations** (statute/rule text) | External regulators / government | **External Authority** (the regulator) — *not* MDL | MDL domain (encodes into a mandate), Discipline Provider | The regulator (external) | MDL domain, all consumers |
| **Organizational policy** | The organization's governance | **The organization** (as Mandate Authoring Authority) | MDL domain (encodes), the org's nodes | The org (authors a new source version) | MDL domain, consumers |
| **Client contracts** (PRIME obligations) | The prime client / contracting party | **The contracting parties** (source); **MDL domain** owns the encoded prime-mandate | MDL domain, the bound Business-Nodes | The parties (contract change → new mandate version) | Consumers |
| **Jurisdiction hierarchy** (the precedence stack + inheritance) | Ecosystem doctrine (this repo, ratified) | **MDL domain** (owns and applies the stack) | Business-Node, Economic consumers (read resolution) | **MDL domain** via ratified constitutional change | All consumers |
| **Financial overrides** (e.g. `tax_exempt_override`) | Mandate Authoring Authority (the exempting policy) | **MDL domain** (the binding determination) | **Economic Consumer** (books zero tax), Business-Node | **MDL domain** only (as a mandate rule) | Supervisor, Auditor |
| **Eligibility** (rules-as-mandates + eligibility status) | Program/authority authors the eligibility *rule* | **MDL domain** owns the *rule encoding + eligibility determination*; the **Business-Node** owns the *grant/deny decision* | Business-Node (decides admission on the status) | MDL domain (rule/status); Business-Node (its decision) | Auditor, Supervisor |
| **Validation** (satisfaction of resolved mandates) | — | **MDL domain** (deterministic validation + snapshot) | Business-Node (gates on it), Economic, Auditor | **MDL domain** only (never a consumer) | Supervisor, all consumers |
| **Enforcement** | — | **MDL domain** owns the *authoritative determination* (compliant / override / block-condition) | Business-Node *performs the act*; Economic books the effect | MDL domain (the determination); Business-Node (the act, within its scope) | Supervisor (oversees, cannot disable) |
| **Audit** (mandate + determination trail) | — | **MDL domain** (append-only, immutable snapshots + logs) | Auditor, Supervisor, Intelligence (aggregate) | **MDL domain** append-only only; never edited | Auditors, Regulators, Human Ratifying Authority |
| **Risk** (risk scoring of behavior) | — | **Governance Supervisor** and/or **Intelligence Consumer** — *not* MDL | Executive/Operational and Intelligence consumers | Supervisor / Intelligence (their own models) | MDL domain (surfaces facts, not risk verdicts) |
| **Governance** (of *mandate* authoring workflow) | This repo's doctrine (ratified) | **MDL domain** (its own authoring/approval process) | Mandate Authoring Authorities, ops roles | **MDL domain** (governed workflow) | Supervisor, Auditor |
| **Governance** (of *ecosystem/assistant* doctrine) | Ecosystem doctrine home | **Doctrine-Governance Consumer** (e.g. LEAL) / ecosystem home — *not* MDL | The ecosystem's systems/bots | The doctrine home (external to MDL) | MDL domain (as a bound system) |
| **Execution** (the real-world/business/economic act) | — | **Business-Node Consumer** (business act) · **Economic Consumer** (economic act) — *never* MDL | The acting node's own downstream | The acting consumer, in its scope | MDL domain (never executes) |

---

## 2. What the MDL domain owns that nothing else authoritatively owns today

Reading down the "Owns" column, the MDL domain owns exactly the truths that are currently *unowned as
ecosystem infrastructure* or *fragmented inside one business node* (`MDL_Ownership_Analysis.md` §2):

1. **The authoritative resolved-mandate set** — today embedded in CFRS, hardcoded to one node/one
   jurisdiction (`TRUST_CLAIM_AUDIT.md:39`); no ecosystem node owns it.
2. **The deterministic satisfaction determination + immutable snapshot** — the reproducible audit
   artifact.
3. **The binding financial-override determination** — the truth the Economic Consumer must honor but
   does not itself define.
4. **The jurisdiction precedence resolution** — the one place conflict between layers is resolved
   deterministically.

It owns these four; it explicitly owns **none** of: the source law/contract/policy, economic execution,
the business decision/act, ecosystem/assistant governance doctrine, risk verdicts, or discipline legal
reasoning. That negative space is as much the deliverable as the positive space.

## 3. The three roles that must never collapse

The most important thing this matrix encodes is that **Author (source), Owner (resolution/determination),
and Actor (execution) are different roles and must stay different**:

- If **Author + Owner** collapse, the mandate domain is *legislating* the policy it also resolves — an
  unaccountable actor writing the law it enforces. Forbidden (`MDL_Infrastructure_Constitution.md` §2).
- If **Owner + Actor** collapse, the mandate domain is *executing* the business/economic act it also
  determines — it has become the node or the bank it serves. Forbidden.
- If **all three** collapse, the mandate domain is an unaccountable policy-and-execution monolith — the
  exact fragmentation-plus-overreach the ecosystem's no-duplication rule exists to prevent.

Every row above keeps them apart on purpose. A future capability proposal is tested against this matrix
by checking that it does not collapse these roles.

## 4. Reconciliation notes (evidence-anchored)

- **Financial overrides — owned here, booked by Economic Core.** The uploaded *MDL Spec* §2.5 makes the
  override *authoritative*; the Economic Domain's own doctrine says it "enforces economic policy it does
  not author" and "does not Exempt the ecosystem" of its own accord
  (`RBM-Economic-Core/RBM_Economic_Constitution.md:102-103`; `Economic_Truth_And_External_Authority.md:87`).
  The two are consistent: MDL owns the *override mandate/determination*; Economic Core *consumes and
  books* it. **[FACT-reconciled]**
- **Enforcement — determination here, act at the node.** The specs both say MDL "enforces" (*MDL Spec*
  §1, §12) and that nodes "enforce payable gating" (*MDL Spec* §11). Reconciled: MDL owns the
  *authoritative determination*; the node performs the *act*; the Supervisor ensures no bypass
  (*Service Contract* §5). **[INFERENCE]**
- **Risk — not MDL's.** MDL surfaces compliance *facts* (missing documents, threshold blocks); *risk
  scoring* of behavior/anomaly is the Governance Supervisor's (*Service Contract* §2, "Risk scoring") or
  an Intelligence Consumer's. MDL never issues a risk verdict. **[FACT]**
