# Repository Ownership Report — Does RBM MDL Layer Deserve Its Own Repository?

**Status:** FOUNDATIONAL — established this sprint; ratification rests with the Human Ratifying
Authority. Architecture and doctrine only.

**Governed by:** `MDL_Infrastructure_Constitution.md`. **Founded on:** `MDL_Ownership_Analysis.md`
(Phase-1 evidence). **Enforces the rule:** every capability and constitutional document has exactly one
authoritative owner — no duplicates, no forks, no competing versions.

---

## 0. The question

Should "mandate definition" be a standalone repository/node, or should it remain a capability inside CFRS
or become a service inside EchoForge? This report answers with evidence and states the ownership map that
follows.

---

## 1. The determination: yes — its own repository

**RBM MDL Layer deserves its own repository and node.** The evidence:

1. **It is consumed by many nodes and must be referenced, not copied.** "A node-agnostic governance
   spine" whose "Same mandate infrastructure serves FLEET, HOUSING, CONSTRUCTION, and all other nodes"
   (`EchoForge/MDL_LAYER_README.md:54,64`), and the uploaded *MDL Spec* §5 forbids nodes from duplicating
   it. A truth many nodes consume and may not duplicate is, by the ecosystem's own pattern, an
   **infrastructure node** (`MDL_Ownership_Analysis.md` §1). **[FACT]**
2. **Its current home is a business node, which is the wrong owner for shared infrastructure.** It is
   embedded in CFRS as business logic (#115, `RBM_CAPABILITIES_V1.md:1624`) and is flagged as *hardcoded
   to one node/one jurisdiction* (`TRUST_CLAIM_AUDIT.md:39`). A business node owning shared governance
   infrastructure is the fragmentation the ecosystem's no-duplication rule exists to end. **[FACT]**
3. **It is not EchoForge's to own.** The uploaded *MDL ↔ EchoForge Service Contract* §2 treats MDL and
   EchoForge as **separate systems** — "EchoForge does not define mandates." Hosting MDL *inside*
   EchoForge would collapse the supervisor/owner separation the Service Contract exists to protect
   (`MDL_Responsibility_Matrix.md` §3). **[FACT]**
4. **The precedent exists.** The Economic Domain took exactly this path — a shared truth extracted from
   product history into an independent constitutional node with its own doctrine
   (`RBM-Economic-Core/Repository_Independence_Review.md:20-24`). MDL is the same move for mandate truth.
   **[PRINCIPLE]**
5. **An empty `RBM-MDL-Layer` repo already exists** — the ecosystem has already begun chartering it as
   its own node (`MDL_Ownership_Analysis.md` §2). This report ratifies that choice with reasons. **[FACT]**

**Rejected alternatives, with reasons:**
- *Keep it in CFRS* — fails the no-duplication and consumer-agnostic tests; a business node cannot be the
  ecosystem's mandate authority.
- *Host it inside EchoForge (as "EchoForge MDL Service," `MDL_LAYER_README.md:80-95`)* — collapses the
  supervisor/owner separation; the Service Contract already separates them. EchoForge supervises; it does
  not own.
- *Shared internal package* (uploaded *MDL Spec* §10 Option A) — acceptable as an *implementation
  distribution* mechanism later, but a package is not an owner; ownership still needs a home node. This
  report chooses the independent node as the owner; the package is an implementation detail of Stage 2+.

---

## 2. The ownership map (single owner per document)

Every constitutional document in this repository is owned **by the mandate domain** and by no other
repository. The rule: *a constitutional document lives in exactly one repository, and every other
repository references it rather than copying it.*

| Document class | Owner | Note |
|---|---|---|
| All `MDL_*.md`, `Immutable_Core_Charter.md`, matrices, lifecycle, architecture, blueprint | **RBM-MDL-Layer** | Authored here; owned here; referenced (never copied) elsewhere. |
| IEF/IAF applications (`institutional-evaluation/`, `innovation/`) | **RBM-MDL-Layer** | The *reusable frameworks* are owned by the ecosystem home; only this node's *application* is owned here. |
| The uploaded operational specs (MDL Spec, Service Contract, Jurisdiction Stack) | **Ecosystem operational-contract owner** (to be confirmed — see below) | This doctrine *governs and remains consistent with* them; it does not claim to own them. See `Open_Questions_and_Risks.md`. |
| The CFRS embedded MDL (`mdl_engine.py`, `mandate.py`) | **CFRS-Enterprise** until migration | Retained by CFRS until the Migration Strategy retires it; ownership of the *capability* transfers to this node, the *legacy code* is retired in place. |

## 3. Cross-repository references (no duplication)

Other repositories must **reference** this node, never copy its doctrine:
- CFRS/UPM/business nodes reference `MDL_Consumption_Model.md` and consume the node; they do not restate
  its constitution.
- EchoForge references `MDL_External_Interfaces.md` §2 (the supervision boundary) and the Service
  Contract; it does not author mandate doctrine.
- Economic Core references `MDL_Truth_Ownership_Matrix.md` for the financial-override seam; it does not
  own it.
- The ecosystem capability index (`RBM_CAPABILITY_INDEX.md`) should re-point capability **#115** Primary
  Node from **CFRS-Enterprise** to **RBM-MDL-Layer** — an additive edit to the *index owner's* document,
  not a move this node makes. Recorded here so it is done in the right place.

## 4. Verification: one owner, no duplicates

After this sprint the invariant holds and can be checked mechanically:
1. Every `MDL_*` constitutional document exists as full content in **exactly one** repository
   (RBM-MDL-Layer); other repos hold references, not copies.
2. No mandate doctrine authored here restates or depends on another repository's constitution; the node
   defines its own authority and evidentiary standard (`Repository_Independence_Review.md`).
3. The capability-index re-pointing of #115 (a consumer-side edit) removes the second owner rather than
   creating one.

If any check fails, either the single-owner rule (a duplicate appeared) or the independence rule (an
upward dependency appeared) has been violated, and the offending content is reduced to a self-contained
statement or a non-binding reference.
