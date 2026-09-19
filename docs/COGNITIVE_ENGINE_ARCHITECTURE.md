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
