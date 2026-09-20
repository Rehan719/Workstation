# The cognitive engine fabric — what exists, what was proposed, what we will build

**Status:** review + plan. Written W480 (2026-09-20) from an outside proposal (a reconnaissance and a Phase 2/3
implementation sketch for a 12-engine cognitive architecture, a 5-gate clearance chain and a 6-stage recirculation
loop), interrogated against this repository commit by commit. Canonical plan items live in
`docs/FABLE_DELIVERY_PROMPT.md` and `docs/WORKSTATION_IDBO_LIVING_PLAN.md`; this file is the reasoning behind them.

The Owner's standing rule governs everything below: **never a claim the system cannot back.** An engine that returns a
constant is not an engine, and a gate that cannot fail is not a gate. That rule decides most of the corrections here.

---

## 1. The proposal, in one paragraph

Twelve engines in three tiers — six foundational (Inkashaf, Aqal, Samajh, Hoshiyari, Soch, Iman), three
meta-regulative (Tawazun, Niyyah, Tafakkur), three auxiliary (Tahqeeq, Mushāwara, Mudrik) — sitting behind a five-gate
constitutional clearance chain (Mushāwara → Niyyah → Tawazun → Tafakkur → Tahqeeq), driven by a six-stage
recirculation loop (Sense, Intend, Analyse, Act, Learn, Reflect) with latency budgets, each engine's result
cryptographically attested into the Unified Event Graph. New code would live under
`agentic_core/ai/cognitive_engines/` behind a `FEATURE_FLAG_COGNITIVE_ENGINES_V1` flag.

The **direction is right and is already this platform's direction.** The reconnaissance behind it is materially wrong
about the starting point, and the sample code would re-commit the exact defect class this delivery phase is closing.

## 2. What the reconnaissance got right

| Claim | Verdict |
| --- | --- |
| Backend `agentic_core/` (FastAPI), frontend `apps/workstation-superapp` (Vite/React/TS) | correct |
| Atomic JSON stores, strict reads, cross-process lock, `StoreUnavailable` on malformed data | correct (`agentic_core/config.py`) |
| Tenant-scoped memory, hardened against cross-tenant recall | correct (`agentic_core/ai/memory.py`) |
| The UEG is an append-only, hash-chained event graph and is the right home for attestations | correct (`agentic_core/gaas/v5/ueg.py`) |
| A constitutional interceptor already gates actions | correct (`agentic_core/gaas/v5/uci_v16_omega.py`) |
| `CrewManager` orchestrates the AI CEO and C-Suite | correct (`agentic_core/ai/orchestrator.py`) |
| The heartbeat is the right driver for a recirculation loop | correct (`agentic_core/organism/heartbeat.py`) |
| Real-money rails are gated; the economy is virtual WST | correct, and it stays that way (§6 below) |

## 3. What it got wrong — evidence

**3.1 The engines are not "planned or partial". Most of this architecture already exists in code.**

- `agentic_core/cognitive/` holds `inkashaf_engine.py`, `aqal_engine.py`, `samajh_engine.py`, `hoshiyari_engine.py`,
  `soch_engine.py`, `iman_engine.py`, `cascade_v16.py` and a `registry.py` whose `EngineType` already enumerates
  **nine** engines including Tawazun, Niyyah and Tafakkur.
- `agentic_core/consultation/interface.py` defines the consultation contract, and `agentic_core/consultation/mushawara/`
  holds the deliberation bridge.
- `agentic_core/avatars/core/clearance_chain.py` implements the five gates, in order, exactly as proposed.
- `agentic_core/avatars/core/recirculation_orchestrator.py` implements the six-stage loop with latency targets.
- `agentic_core/avatars/cognition/mushawara_bridge.py` fronts a nine-engine registry.

One honest caveat, already recorded in the repository: the avatar API is mounted and reached (the W477 sweep tested
`/api/v1/avatar/chat` from the VSB Cockpit, finding S1.6), but it **deliberately does not route through** the
recirculation orchestrator. Its module docstring says why: that orchestrator "fails on its very first execution
stage — its nine-engine cognitive registry was never actually populated with working engines — so building on it
would mean shipping another broken layer." The engine stack is therefore code-present and largely dormant, not a
live path.

So the task is **not** to write these engines. It is to populate the registry with engines that measure something,
make the dormant layers able to fail, and only then wire them to the surfaces that name them.

**3.2 Creating `agentic_core/ai/cognitive_engines/` would add a third parallel engine tree.**
There would then be `agentic_core/cognitive/`, `agentic_core/avatars/cognition/` and the new tree, with three
registries and no single answer to "which engine ran". We will not do that. The existing `cognitive/registry.py` is the
one registry; the empty `cognitive/foundational/` and `cognitive/meta/` packages are where the real implementations go.

**3.3 The sample code would re-commit the defect class this phase exists to kill.**
Every proposed engine returns a constant: a pattern id `p_001` with `confidence 0.85`; `optimization_score 0.92`;
`intent confidence 0.88`; `alignment_score 0.95`. None reads its input. The existing engines have the same defect and
it is already on the register: the W477 sweep (S2.0, register row FU-146) found `AqalEngine.reason` returning
`{"status": "SUCCESS", "plan": "computed"}` for any challenge, `ImanEngine` returning alignment `0.99`, and the VSB
Spawn Studio showing those constants as "Cascade Complete" with a green tick. Adding six more such stubs would widen
the class, not close it.

**3.4 The clearance chain, when it is wired, will not be able to refuse anything.**
(It is dormant today — see the caveat in 3.1 — so this is a defect to fix *before* wiring, not a live certification.)
In `clearance_chain.py` (called only from the dormant `recirculation_orchestrator.py`) every gate defaults to pass:
`tawazun_res.get("balanced", True)`,
`tahqeeq_res.get("verified", True)`, `tafakkur_res.get("risk_score", 0) > 0.15`. An engine that returns `{}` clears all
five gates. The attestations are literal strings (`"SIG_MUSHAWARA_v1"`, `"SIG_NIYYAH_v1"`, …) written into the UEG as
if they were signatures. A chain that cannot fail, recording signatures that are not signatures, is worse than no
chain: it certifies. This is the same class as the §10 quality bar (register rows FU-094, FU-095, FU-105).

**3.4b The wiring between the existing pieces does not line up.** Three gaps, each checked:
- **Nothing ever registers an engine.** `CognitiveEngineRegistry._engines` starts empty and no module calls
  `register()`, so `registry.get(...)` raises `ValueError` on the first call. That is precisely why the avatar API
  bypasses the orchestrator.
- **The call contract differs.** `EngineRegistry9.get_engine_response` calls
  `engine.process(input_data, context, enforcement)` and reads `result.payload`; the engines expose
  `unveil_patterns` / `comprehend` / `reason` / `detect_anomalies` / `reflect` / `validate_values` plus a `consult`,
  and return plain dicts. No engine would satisfy the registry's call even if it were registered.
- **The consultation schema excludes the meta engines and forces a number.** `ConsultationRequest.engine` is a
  `Literal` of seven names (the six lenses plus `mjm`), so `niyyah`, `tawazun` and `tafakkur` cannot be requested
  through it, and `ConsultationResponse.confidence` is a required float in 0..1 — which is why the existing engines
  return literals like `0.96`. A contract that *requires* a confidence pushes every implementer toward inventing one.
  The contract must gain an explicit "not assessable" state before the engines are written against it.

**3.5 Some numbers in the reconnaissance are not this repository's numbers.**
It claims "461+ API endpoints" and "140+ routes, 64 verified"; the app mounts 79 routers and `App.tsx` declares 73
routes. The claim of "10,000-dim deterministic HD perspective aggregation" appears in commit prose, not in measured
behaviour. Numbers in our docs must come from a measurement, with the command that produced them.

**3.6 Post-quantum signatures are named in the code, not exercised.**
`Dilithium`/`Kyber` appear in five modules as strings and descriptions. Nothing in the attestation path performs a
post-quantum signature today. An attestation chain must therefore start with something real (an HMAC or Ed25519
signature over a canonical payload, with the key handling stated) and must never be labelled post-quantum until it is.

## 4. The invariants any engine work must satisfy

1. **An engine computes from its input or says it cannot.** No constant verdicts, scores or confidences. Where an
   engine has no real method yet, it returns `assessable: false` with the reason, and every surface renders that as
   "not assessed" — never a number, never a green tick.
2. **Every engine result carries provenance**: what served it (the owned model, the deterministic structured floor,
   an opt-in external accelerant), or that it failed. This matches the rule W479 applied to the intelligence
   pipelines: a failed call is never output, is never fed into another prompt, and is never counted as having run.
3. **A gate must be able to fail, and a gate's default is refusal**, not approval. Any gate whose inputs are missing
   returns "not assessable" and blocks the terminal action rather than clearing it.
4. **An attestation names its algorithm and its key**, or it is not called an attestation. No placeholder signature
   strings in the UEG.
5. **One registry.** Engines are registered in `agentic_core/cognitive/registry.py` and reached through it.
6. **Feature-flagged and default-off**, with the flag read at call time (not at import), so a flag change needs no
   restart and tests can flip it.
7. **Latency budgets are measured and recorded**, not asserted. A breach is a recorded fact, not a log line only.
8. **Nothing in this work enables real money.** See §6.

## 5. The adjusted build order

Each stage lands as its own round: audit, patch, guard test, blind-test every guard leg, refute in isolated
worktrees, probe on a fresh backend, full suite, docs and register.

- **C1 — Truth first (already carried by P1.18):** FU-146 — the VSB spawn cascade and the six existing engines stop
  presenting constants as analysis. Either the engine measures something, or the surface says nothing was assessed.
- **C2 — The engine contract, then the six foundational engines:** extend the consultation contract with an explicit
  `assessable` state and a provenance block (so "no confidence" is expressible and a fabricated number is not the path
  of least resistance), widen its engine names to the nine the registry already declares, give the registry one
  populated binding and one call signature that the engines actually implement, and add a base class carrying the
  feature flag (read at call time), measured latency and the result type. Then implement the six foundational engines
  in the empty `agentic_core/cognitive/foundational/` package against real inputs, replacing the constant-returning
  modules in place. Also remove the two unused cascade/MJM singletons left in `agentic_core/api/intelligence.py`
  after W479 stopped calling them.
- **C3 — The three meta-regulative engines** (Tawazun, Niyyah, Tafakkur) implemented as refusals-by-default:
  Tawazun a real Pareto frontier over named objectives; Niyyah an intent ratification whose quorum is counted from
  real signatures; Tafakkur a drift check against a recorded baseline.
- **C4 — The clearance chain made able to refuse:** every gate's default flipped to block, each gate's verdict
  recorded with its basis, and the chain's result surfaced wherever an emission it cleared is shown.
- **C5 — Real attestations:** a canonical payload, a named algorithm, a stated key source, appended to the UEG and
  verifiable by a route that re-computes them. Post-quantum only when it is actually post-quantum.
- **C6 — The three auxiliary engines** (Tahqeeq output verification, Mushāwara deliberation, Mudrik as the bridge to
  the transformation surface) and the recirculation loop driven by the heartbeat, with measured stage latencies.

Sequencing rule: **C1 before C2.** Building new engines while the old ones still certify constants would mean two
generations of the same untruth on the same screens.

## 6. Owner gates (unchanged by this work)

- **Real money stays off.** The proposal puts a Stripe entitlement check inside the Niyyah engine. Live Stripe,
  real-money rails and the exposed key are the Owner's decision (the key must be rolled by the Owner first). Niyyah
  may carry an *entitlement input*, supplied by the existing virtual economy, and nothing in this build calls a
  payment provider.
- **Faith content** is unaffected: Quran Arabic is never generated, only sourced; AI-authored notes stay labelled.
- **External AI** stays opt-in and off by default; the in-house fabric is first.

## 7. What was taken from the proposal as-is

The tier structure, the engine names and their domains, the five-gate order, the six-stage loop with latency budgets,
the attestation-into-UEG idea, the feature-flag rollout, and the SLA wrapper. The corrections above are about
truthfulness and about not duplicating what exists — not about the architecture's shape.

---

# Part II — the Biomimetic Minimisation Engine (BME)

**Status:** review + plan, W482 (2026-09-20), from a second outside proposal ("BME verified integration
specification"). It is a marked improvement on the first: it reads this repository's own defect register and
sequences itself behind those fixes. Its direction is accepted. Its facts still need correcting, and its sample
code repeats the defect class it sets out to remove.

## 8. What the proposal asks for

Eight new engines under `agentic_core/cognitive/foundational/` — variational free energy, a Schrödinger bridge,
entropic optimal transport, a diffusion process, least action, Murray's law, a Landauer meter, and a unified
Ω-functional that scores a policy as a weighted sum with hard constraints acting as infinities — all logged to the
UEG with real signatures, gated by the constitutional engine and the VRPR pipeline, behind a feature flag.

## 9. What it got right

It names the same five defects this repository already has on its register (constant-returning engines, gates that
default to pass, placeholder attestations, an unpopulated registry, a contract that forces a confidence), and it
puts them BEFORE its own build. That ordering is correct and matches P3.12–P3.15. It also respects the one-registry
rule and proposes no parallel tree.

## 10. What it got wrong — evidence

**10.1 Eight of the paths it says exist do not.** Checked: `agentic_core/validation/vrpr/`,
`agentic_core/constitutional/constraint_engine.py`, `agentic_core/ledger/ueg/`,
`core/constitutional/constraint_engine.py`, `agentic_core/compliance/nemoclaw/`, `tests/`, and the three engine
files it ticks as existing — `cognitive/tawazun_engine.py`, `niyyah_engine.py`, `tafakkur_engine.py` — are all
absent. The real homes are `agentic_core/quality/vrpr_pipeline.py`,
`agentic_core/validation/omni_enforcement_pattern_supreme.py`, `agentic_core/gaas/v5/ueg.py` with
`agentic_core/ueg/logger.py`, and `integration_tests/`. The registry declares nine engine TYPES; only six engine
files exist.

**10.2 Its sample code calls methods this repository does not have.** `ueg.append_event(...)` and
`ueg.get_master_key()` do not exist (the loggers expose `log`, `log_event`, `log_minimisation_event`, and no key
accessor); `vrpr.validate_and_redraft(...)` does not exist (`VRPRPipeline.process(draft, context)` does); and the
registry is class-level with `register`/`get`, not an instance with `get_engine`. Several of its verification
commands would therefore fail against correct code.

**10.3 The "20 absolute constraints engine" cannot currently fail.** `OmniEnforcementPatternSupreme` holds a phase
map of twenty-one validator NAMES, and its `validators` dict starts empty with `register_validator` never called
anywhere in the repository. All three of its constructors — the clearance chain, the recirculation orchestrator and
the Mushāwara bridge — pass `fail_on_missing_validator: False`, so every phase is skipped and `validate()` returns
passed. Building BME's compliance on it would be a fourth gate that cannot refuse.

**10.4 Much of the BME already existed here, and was deleted.** `agentic_core/biomimicry/minimisation/` is a real
package: `core/optimal_transport.py` holds a Sinkhorn `OptimalTransportRouter`, and the compiled artefacts beside it
name `omega_functional`, `schrodinger_bridge` and `diffusion_engine`, whose sources were removed in W382. The
deleted Ω-functional is recoverable from git and is the same object the proposal describes: `MinimisationObjective`
with `J(π) = α·F + β·W_ε + γ·KL + δ·S_export + ζ·M` and a hard legal-compliance constraint that sends J to infinity.
The work is a **recovery and completion**, not a greenfield build.

**10.5 The one real piece cannot run today.** `OptimalTransportRouter` needs POT (`import ot`), which is not
installed and is not in `requirements.txt`; the import is guarded, so the router silently becomes unavailable.
`torch` and `numpy` ARE declared dependencies, so the proposal's use of them is not a new dependency — but the
solver it depends on is missing, and the adapter that would use it (`EntropyRegularisedGaaS`) is mounted on no route.

**10.6 Its sample code repeats the defect class it exists to remove.** Computing a number from the input is not the
same as measuring the named quantity. In the proposal: "Murray's law efficiency" is `1 − diameter/node_count`;
"quantum security score" is the fraction of crypto operations whose string contains "kyber", "dilithium", "falcon"
or "sphincs"; "bits erased" for the Landauer meter is `(len(str(policy)) + len(str(context))) * 8 // 1000`; the
Wasserstein distance is a mean absolute difference. Each is then reported under the name of a physical or
mathematical law. A reader is told the system measured entropy export; it multiplied a made-up bit count by
Boltzmann's constant.

**10.8 The VRPR pipeline it wants to gate on invents its own confidence.** `agentic_core/quality/vrpr_pipeline.py`
is twenty-six lines. `process()` starts at a hard-coded `conf = 0.90` and adds `0.05` per refinement iteration; the
number never depends on the content. Its loop exits successfully when `enforcement.validate(curr)` passes and
`conf >= 0.95` — and the enforcement always passes (10.3). Its `_polish` step is two string replacements that turn
"Action result" into "Certified Sovereign Action Outcome", and a pass returns `constitutional_articles=[18, 19, 20]`
as a literal. Gating the Ω-functional on "VRPR confidence ≥ 0.95" would therefore import a manufactured number and
call it validation. VRPR itself needs the P3.12 treatment before anything depends on it.

**10.9 The Landauer meter already exists — and is fed invented bit counts.**
`core/transcendent_subsystems/tfel.py` is the `ThermodynamicFreeEnergyLedger`: `E_min = k_B · T · ln 2`,
`meter_operation(name, bits)`, a budget, and `export_cycle_ledger`. Writing a second `landauer_meter.py` would be a
duplicate. The defect is not its absence, it is its inputs: every caller passes a constant —
`tool_registry.py` meters `bits=2e5` per effector call with a comment "standard bit cost",
`recirculation_orchestrator.py` meters `bits=1e4` for its sense stage, and `causal_simulator.py` uses
`len(task_batch) * 1.5e6`. The physics is right and the measurement is imaginary, so the joules it reports are
imaginary too. `export_cycle_ledger` also returns `"compliance": True` as a literal. The proposal's
`_estimate_bits_erased` (payload length ÷ 1000) would add a fourth invented count.

**10.10 The engines were ARCHIVED, not lost — and the archive holds the missing wiring.** `scripts/recovery_audit.py`
(written this round) reads git history WITH RENAMES and finds 519 sources that left their place under
`agentic_core/` and `core/`: 516 were MOVED into `_archive/`, 3 were deleted outright. Among the moved:

| what | lines | now at |
| --- | --- | --- |
| `cognitive/bootstrap.py` | 25 | `_archive/jules-unwired/agentic_core/cognitive/bootstrap.py` |
| `cognitive/base_engine.py` | 23 | `_archive/jules-unwired/agentic_core/cognitive/base_engine.py` |
| the six foundational + three meta engines | 7–31 each | `_archive/jules-unwired/agentic_core/cognitive/{foundational,meta}/` |
| `minimisation/core/diffusion_engine.py` | 100 | `_archive/jules-unwired/agentic_core/biomimicry/minimisation/core/` |
| `minimisation/core/schrodinger_bridge.py` | 87 | same directory |
| `minimisation/core/omega_functional.py` | 61 | same directory |

This resolves W480's §3.4b. `bootstrap.py` is the function that populates the registry — it calls
`registry.register(EngineType.AQAL, AqalEngine(ueg))` for all nine — and `base_engine.py` defines the
`CognitiveEngine` ABC whose `process(input_data, context, enforcement) -> EngineOutput` is EXACTLY the contract
`EngineRegistry9.get_engine_response` calls and `.payload` it reads. The registry is not unpopulated by design; its
populator and the engines that satisfy its contract were moved to the archive, leaving the live callers pointing at
nothing. Recovery restores the wiring in one step.

**What recovery does NOT give is computation.** The archived engines are stubs too: `InkashafEngine._process_logic`
returns `{"discovery": "Pattern revealed", "vector": [1]*10000}` and `TafakkurEngine` hard-codes `drift = 0.003`.
`base_engine.py` stamps `confidence=0.95` on every successful output. So the "10,000-dimensional deterministic HD
perspective aggregation" that the first proposal quoted from a commit message is a list of ten thousand ones. The
Schrödinger bridge and diffusion engine are the exception — those are real mathematics (IPF/Sinkhorn with citations;
a `torchsde` SDE) and are worth restoring as they are.

**10.11 `core/` exists, but not the file the proposal cites.** The repository root does hold `core/identity.py` and
`core/transcendent_subsystems/`; `core/constitutional/constraint_engine.py` does not exist.

**10.7 Deployment and cost claims are outside a build item.** "$0 owner expenditure", "zero-cost deployment via the
existing Google Cloud free tier", "eternal operational integrity" — this repository deploys nothing without the
Owner (P4.5), and no such mapping exists here to verify.

## 11. The naming invariant (added to §4, for all engine work)

**A quantity may carry the name of a law, a metric or a method only when it is computed by that law, metric or
method.** Otherwise it is a proxy, and the field, the API and the page all say so — `api_surface_coverage`, not
`vision_realisation`; `estimated_bits_from_payload_size`, not `bits_erased`; `pqc_named_in_config_ratio`, not
`quantum_security_score`. W481 applied exactly this to a "digital-twin simulation" that was one line of arithmetic.
A heuristic honestly named is an asset; the same heuristic wearing a law's name is the defect this phase removes.

## 12. The adjusted BME build order (P3.17, after P3.12–P3.16)

- **B0 — The two engines BME would lean on must be able to fail first.** VRPR's confidence is computed from the
  content or it is `assessable: false` (no 0.90-plus-0.05 ladder), its enforcement runs registered validators or
  reports which it could not run, and the TFEL's bit counts come from an instrumented operation or the reading is
  named a proxy. This is P3.12's and P3.14's rule applied to `agentic_core/quality/vrpr_pipeline.py` and
  `core/transcendent_subsystems/tfel.py`.
- **B1 — Recover from the archive and read.** Restore `omega_functional.py`, `schrodinger_bridge.py` and
  `diffusion_engine.py` from `_archive/jules-unwired/agentic_core/biomimicry/minimisation/core/` (the audit prints
  the paths), read them against the vision, and remove the orphan compiled artefacts left beside their old homes.
  Decide POT: add it to requirements, or implement Sinkhorn over numpy. Until a solver is present, the transport
  router reports itself unavailable rather than silently degrading.
- **B2 — One contract, recovered not reinvented.** `_archive/jules-unwired/agentic_core/cognitive/base_engine.py`
  already defines the `CognitiveEngine` ABC that the live registry and `EngineRegistry9` call, and `bootstrap.py`
  already registers all nine engines. Restore both (P3.12's work), then make the engines compute and drop the
  hard-coded `confidence=0.95`. The BME engines register through the same one registry and answer the same contract:
  no second registry, no second result type.
- **B3 — Honest names and honest gaps.** Every term of the Ω-functional either computes its named quantity or
  returns `assessable: false` with the reason. A term that is a proxy is named as one. No term contributes a number
  the run cannot justify.
- **B4 — One meter, and it meters.** The Landauer term uses the EXISTING `ThermodynamicFreeEnergyLedger`; no
  second meter is written. Its bit count comes from an actual measurement, or the figure is named a proxy and is
  not reported as energy. Arithmetic over payload size is a payload-size proxy.
- **B5 — Gates that can refuse.** The validators the enforcement phases name are registered, or the engine reports
  which phases it could not run; `fail_on_missing_validator: False` stops being the default at its three call sites.
  This is P3.14's rule applied to the second enforcement surface.
- **B6 — Wire it where it is used.** The Ω-functional is reachable from a surface that states what it scored, with
  every term's basis shown, or it stays unmounted and the documentation says so.

Owner gates unchanged: no real money, no deployment, no external AI by default, faith content sourced only.

## 13. Finding work this repository already has — `scripts/recovery_audit.py`

Three rounds running, an outside proposal offered to build something that already existed here. The pattern is now a
tool, not a habit: `python scripts/recovery_audit.py` reads the repository and reports, with the command that
recovers each item and never a claim that something is dead:

| finding | what it means | W482 count |
| --- | --- | --- |
| `orphans` | a `.pyc` with no source beside it — something left, the compiled form stayed | 524 |
| `deleted` | each of those classified from history WITH RENAMES: `moved_to_archive` · `recoverable` · `name_elsewhere` · `unknown`, biggest first | 516 · 3 · 0 · 0 |
| `archived` | modules under `_archive/` that nothing live mentions | run it |
| `optional` | `try: import X` guards whose module is NOT installed, so the guarded path is silently off | e.g. POT |
| `unwired` | `APIRouter` modules the app never includes | run it |
| `unfilled` | a registry with a `register()` API that nothing ever calls | e.g. the cognitive registry |

**The lesson, in one line: before building, ask the archive.** `--diff-filter=D` alone is not enough — this
repository's cleanup rounds MOVED files (a git rename), so the work that is most worth recovering is invisible to a
deletion-only search. Run the audit at the start of any round that would create a new module, and read what it
names. Three specific habits follow:
1. An empty package (`cognitive/foundational/`) usually means its contents were archived, not that nobody wrote them.
2. A caller with no implementation (the registry, the clearance chain, `EngineRegistry9`) usually means the
   implementation moved; find it before designing a replacement contract.
3. Recovering structure is not recovering substance. The archived engines restore the wiring and keep the constant
   returns; they must still be made to compute, under §4 and §11.
