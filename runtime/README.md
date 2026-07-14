# RBM-MDL-Layer — Era 1 Runtime (Serviceability)

> **Implementation, not doctrine.** The constitutional phase is complete and the
> doctrine is **frozen at v1.0** (`../DOCTRINE_FREEZE.md`). Nothing in this
> directory creates, modifies, or extends doctrine. This is the minimum
> deterministic MDL runtime that makes the frozen constitution *serviceable* — a
> live runtime a real ecosystem consumer depends on for one production decision.

## What Era 1 proves

A live consumer (Viral Bot Machine) can: submit a deterministic request → have MDL
resolve applicable mandates → receive an **authoritative** determination → receive
an **immutable snapshot** → obey the determination → **never bypass MDL**. The
determination is binding; there is no fallback path.

## Layout — the eleven Core components, in build order

The runtime implements the eleven Core capabilities (C1–C11) as one cohesive,
importable package. Each module maps to one architecture layer and cites the
engineering spec it implements (`../engineering/`). The build order follows
`../Architecture_Validation_Report.md` §3:

```
Audit → Registry → Authoring(Governance) → Versioning → Jurisdiction
      → Resolution → Determination → Snapshot → Consumption(Interface/Client)
```

| Module | Layer · Capability | Governed by |
|---|---|---|
| `mdl/audit.py` | 9 · C9 | Component Contracts §Audit |
| `mdl/registry.py` | 1 · C1 | §Registry |
| `mdl/governance.py` | 10 · C10 | §Governance (authoring workflow, R3 roles) |
| `mdl/versioning.py` | 3 · C2 | §Versioning |
| `mdl/jurisdiction.py` | 2 · C3 | §Jurisdiction (R2 two-class stack) |
| `mdl/resolution.py` | 4 · C4 | §Resolution |
| `mdl/determination.py` | 5 · C5+C7 | §Determination (+ financial override) |
| `mdl/snapshot.py` | 6 · C6 | §Snapshot (immutable, idempotent per event) |
| `mdl/override.py` | 7 · C8 | §Override (dual-auth, read-time effectiveness) |
| `mdl/distribution.py` | 8 · C11-propagation | §Distribution |
| `mdl/interface.py` | 11 · C11-request | §Interfaces (least-privilege scoping) |
| `mdl/runtime.py` | — | Runtime Spec §2 (the wired pipeline) |
| `mdl/seeds.py` | — | Era-1 operational mandate set |

> **On directory placement.** The Repository Blueprint reserves top-level
> `registry/`, `resolution/`, … directories as future homes. Era 1 keeps the
> runtime in a single importable `runtime/mdl/` package so cross-layer imports
> form one clean module graph; the table above preserves the layer↔capability
> mapping the blueprint requires. Migrating modules into the blueprint's governed
> directories is tracked as remaining work (see `../ERA1_EVIDENCE.md`).

## The determination pipeline (Runtime Spec §2)

```
Interface (authenticate, scope to least-privilege projection)
  → Resolution  (Registry + Versioning + Jurisdiction)
  → Determination (+ Financial-Override)
  → Snapshot (freeze, idempotent per governing event)
  → Override (apply in-force overlay; snapshot unchanged)
  → Interface (return runtime outcome)
  ⟿ Audit (record)   ⟿ Distribution (emit event)
```

The deterministic path (resolve→determine→snapshot) reads **no wall-clock** —
effectivity uses the context `as_of`. The single sanctioned wall-clock read is
override expiry, which affects only the runtime overlay, never the frozen
snapshot (I1, §7).

## Run it

```bash
# core runtime invariants (no third-party deps)
python runtime/tests/test_runtime.py

# client ↔ service contract over a real HTTP socket (no fastapi needed)
python runtime/tests/test_client_http.py

# evidence demo: example determination + snapshot + audit + determinism
python runtime/demo/era1_demo.py

# the live service (needs fastapi + uvicorn)
uvicorn runtime.service.app:app --port 8080
```

## The consumer contract

`runtime/client/mdl_client.py` is the **single reusable client contract**, owned
here and vendored verbatim into every consuming node. It is standard-library
only, and it **fails closed**: an unreachable runtime, a non-2xx response, or a
non-admissible determination all result in *action refused* — never *allowed*.
Consumers call `MDLClient.require(...)` at their production decision point.

## Scope discipline (Era 1)

- Initial mandates are **ecosystem operational booleans** (Deployment Approved,
  Campaign Approved, Media Approved, Publishing Authorized, Account Active) — no
  government compliance, no trust scoring, no probabilistic evaluation.
- **EchoForge is not on the determination path.** No trust evaluation is consumed;
  the read-only supervision boundary is respected (I7).
- No dependency on Atlas, Economic Core, CFRS, PERSE, UPM, or Veronica.
