# Native-AI Primitive Defect Ledger — 2026-09-01

**9 of 9 audited primitives carry a §4.5-class defect that survived adversarial refutation.**

The §4.5 class, named for the candidate-ranking defect that started this: *a value SELECTED or
REPORTED as a result when nothing actually discriminated* — plus its cousins, a constant
presented as a measurement, and a field whose NAME implies a determination the value cannot
support.

**None of these is currently reachable from any UI.** That is the only reason this is a latent
risk rather than a live one, and it is exactly why they were not wired: the backlog said
"10 unreached native-AI routes", and wiring them would have shipped nine misleading surfaces
in one change. Decomposing the backlog before working it is what caught this.

Each entry was produced by an agent that CALLED the endpoint and READ the implementation, then
attacked by an independent refuter instructed to default to "refuted". Three were additionally
re-verified by hand against the running backend — noted inline.

## Status — 2026-09-01

**FIXED and guarded (5):** `intent` (W430) · `entailment` · `consensus` · `decide` (W431) ·
`validate` (W432). Each guard was broken, watched fail with the original symptom, and restored.
**OPEN (4):** `rigor` · `quorum` · `topology` · `transduce`. None is wired, so none misleads a user
today — but "unreached" is not "ready", which is the whole point of this ledger.

| primitive | user value today | verdict |
|---|---|---|
| `consensus` | Real and usable at the default threshold: a user or a governance surface asking "did N o | fix_then_wire |
| `decide` | Nothing — and the honest accounting is that its value is negative, not zero. A user reac | fix_then_wire |
| `entailment` | As shipped: negative value. The only thing a user can do with a bare "ENTAILED" is belie | fix_then_wire |
| `entropy` | There is one real, defensible use: reproducible seeding. Feed a fixed list of source des | fix_then_wire |
| `quorum` | Nothing, as it currently stands. The output tells the user only what the user already ty | fix_then_wire |
| `rigor` | Nothing today, and worse than nothing on the first call. No caller exists — grep across  | fix_then_wire |
| `topology` | Real and concrete on clean input: beta0_components tells an operator their agent/depende | fix_then_wire |
| `transduce` | Close to nothing today, and what little exists is outweighed by what a user would wrongl | fix_then_wire |
| `validate` | As it stands, only the SEMANTIC path has real user value: a caller with a ground-truth r | fix_then_wire |

## `POST /api/v1/native-ai/consensus`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** Handler: agentic_core/api/native_ai.py:499-511 (native_consensus), request model ConsensusRequest at :492 (proposal_id, votes[{voter,choice}], total_nodes=0, threshold=0.66 — threshold is an UNVALIDATED free float, no Field bounds). Dispatches to agentic_core/swarm/conflict_resolution.py:34-45, ConsensusEngine.check_consensus. It tallies counts per choice into a plain dict, then: for choice, count
- **sample output:** `(a) honest case — 2xALPHA 1xBETA, thr 0.66: {"reached":true,"choice":"ALPHA","threshold":0.66,"total_nodes":3,"votes_cast":3,"method":"threshold consensus (owned swarm)"} (c) LOSER RETURNED — ALPHA 2 votes, BETA 3 votes, thr 0.4: {"reached":true,"choice":"ALPH`
- **only one possible value in this deployment:** False

**The defect.** PRIMARY (§4.5 class, exact): the "consensus choice" is selected by request-array order when nothing discriminated. Because check_consensus returns the first threshold-clearing entry of an insertion-ordered dict rather than the strongest, any threshold <= 0.5 lets several choices clear at once and the winner is whichever choice's first voter appeared earliest in the votes array.

Proven live, not speculated:
- Case (c): ALPHA 2 votes, BETA 3 votes, threshold 0.4. Both clear (0.4 and 0.6). Response is "reached":true,"choice":"ALPHA" — the LOSER — labelled "method":"threshold consensus (owned swarm)". Nothing in the payload hints BETA held a strictly larger share.
- Case (g): 1x REJECT vs 3x APPROVE, threshold 0.0 → "choice":"REJECT". The minority option reported as the consensus of the swarm.
- Cases (b)/(b2): identical vote multiset, only array order reversed, and "choice" flips ALPHA -> BETA at threshold 0.5. Same votes, different reported "consensus" — a genuine tie resolved by input ordering and presented as a determination.

SECONDARY (name cannot support the value): record_vote keys by voter_id and silently OVERWRITES, but total = req.total_nodes or len(req.votes) counts the raw list length. Case (e): three entries from voter "n1" report "total_nodes":3,"votes_cast":3 while the tally actually held ONE vote (1/3 = 0.33 < 0.66 -> reached false). The fields claim a 3-node, 3-vote ballot; the arithmetic used 1. The de-duplication is invisible in the output.

TERTIARY: threshold is unbounded — case (h) accepted threshold -1.0 and still returned "reached":true,"choice":"REJECT", a "consensus" that is meaningless by construction yet reported as reached.

NOT counted as defects: the empty case (d) returns reached:false with total_nodes:0/votes_cast:0, which makes the reason legible; case (f) (3/100 < 0.66) is correct and honest; the default 0.66 path is arithmetically sound.

**Why it is not wired.** The mechanism is genuinely real and input-driven — not the "zero nodes exist" shape. A fresh ConsensusEngine is built per call and every vote comes from the request body, so the output varies correctly with input: (a) 2/3 >= 0.66 -> ALPHA, (f) 3/100 < 0.66 -> no consensus. That is worth wiring. But at any threshold <= 0.5 it can name a MINORITY choice as the consensus (case g: REJECT wins over 3x APPROVE), which is worse than an unhelpful output — a caller would act on a decision the votes contradict. Contained fixes: (1) in check_consensus pick the max-count choice among those clearing the threshold and return None on a genuine tie for top count, instead of returning whichever the dict ordered first; (2) in the handler derive total from unique voters (len(ce.votes[proposal_id])) or report unique_voters alongside votes_cast so the silent overwrite is visible; (3) bound threshold on ConsensusRequest (Field(gt=0.5, le=1.0)) — above 0.5 the multi-pass case is mathematically impossible, which is exactly why the 0.66 default and the sole internal caller (orchestrator.py:644, pinned threshold=0.66) are safe today. Worth flagging: the existing test at integration_tests/test_mvp_spine.py:3947 only exercises the 0.66 default, so the suite is structurally blind to this whole class.

## `POST /api/v1/native-ai/decide`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** agentic_core/api/native_ai.py:566-576 (handler `native_decide`, model `DecideRequest` at :561 — fields are only `state` and `actions`). It dispatches to agentic_core/cognition/minimax_optimizer.py:16 `MinimaxOptimizer.evaluate_strategy(state, actions, default_utility_func)`, with the utility hardcoded at the call site — the caller CANNOT supply one. What it really computes: agentic_core/cognition/
- **sample output:** `Two calls, IDENTICAL action set, only the ORDER differs: A) payload {"state":{"base_stability":0.9},"actions":["detonate_reactor","evacuate_safely","do_nothing"]} {"posture":"in-house","method":"minimax adversarial (owned cognition)","actions":["detonate_react`
- **only one possible value in this deployment:** True

**The defect.** Textbook §4.5: a value SELECTED and reported as a result when nothing discriminated.

1. `selected_action` is a positional echo laundered as a game-theoretic determination. The utility function ignores the action argument entirely, so all candidates tie at exactly the same maximin value, and the strict-`>` tie-break silently returns whichever action the caller listed first. Calls A and B above are the proof: the same three actions, reordered, produce a different "decision" — and with the ordering in A the endpoint reports `detonate_reactor` as the maximin-optimal action under adversarial stress. The field name asserts a determination the value cannot support.

2. The surrounding labels amplify the claim rather than qualify it. The response asserts `"method":"minimax adversarial (owned cognition)"`; the handler docstring says "Real game-theory, not LLM text"; the capability catalog at agentic_core/api/native_ai.py:247 advertises it as "Real maximin game-theory decision over actions under worst-case stressors." Every one of those is true of the *engine* and false of *this endpoint's configuration of it*. Nothing in the payload tells the user the utility never looked at the action.

3. `consistency_score` and `worst_case_utility` are a fixed ramp presented as a measurement. They are a closed-form arithmetic function of exactly one caller-supplied number, `state["base_stability"]` (default 0.9). They vary, which makes them look computed, but they measure nothing about the actions, nothing about the rest of `state` (case C passes cash/runway/legal_risk/staff — all discarded), and nothing about the environment.

4. `stressors` are advertised as four; two are inert. `oxidative_burst` and `thermal_stress` subtract nothing, so the "worst case" is hypoxia by construction, not by adversarial search.

Notably, the engine itself is NOT the bug. agentic_core/ai/native/orchestrator.py:609-620 calls the same MinimaxOptimizer with its own `_util`, which genuinely varies per action (per-action base 0.92/0.84/0.78, per-action stressor sensitivity 0.30/0.18/0.10) and reads real run signals. That is a working, honest use of the same class — and a ready-made template. The defect is isolated to `default_utility_func`, whose only live caller is this endpoint.

**Why it is not wired.** Answering the question directly: no, `selected_action` can never be anything other than what I saw. It is `actions[0]`, always, in this deployment and in every deployment — not because of a config flag, a missing model, or an empty data store that might later fill, but because the utility function is mathematically incapable of distinguishing actions. No value of `state`, no set of actions, no environment change can move it. The numeric fields do vary, but only as a fixed formula over one input number, so they too carry no decision information. There is exactly one possible decision per call and the call never influences it. Do not wire this as-is: it would present the caller's own list ordering back to them as an adversarially-stress-tested recommendation, over a UI labelled "Real maximin game-theory". That is worse than an empty result — a user cannot detect it, because the output is well-formed, plausibly-valued, and confidently labelled. But the fix is small and well-scoped, which is why this is fix_then_wire, not do_not_wire. Three options, in order of preference: (a) make `default_utility_func` actually read `action` — the orchestrator's `_util` at agentic_core/ai/native/orchestrator.py:609 is a working in-repo model of how (per-action base utility plus per-action stressor sensitivity); (b) extend `DecideRequest` so the caller supplies per-action utilities or state-to-action couplings, and 422 when they are absent, rather than silently falling back to a degenerate default; (c) at minimum, detect the all-way tie in `evaluate_strategy` and report it honestly — return `selected_action: null` with `tie: true`, `tied_actions: [...]`, and a note that the supplied utility did not discriminate, instead of letting the strict-`>` tie-break manufacture a winner. Option (c) alone would have caught this class here and is worth adding to the engine regardless, since it protects every future caller. Also either implement `oxidative_burst`/`thermal_stress` or stop advertising them.

## `POST /api/v1/native-ai/entailment`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** C:\Users\rehan\Workstation\agentic_core\api\native_ai.py:477-484 (EntailmentRequest at :472, fields premise/hypothesis) dispatches to NLIEngine().verify_premise_entailment at C:\Users\rehan\Workstation\agentic_core\nlp\nli_engine.py:62-82. What it really computes, in full — there is nothing else in the method: premise_words = set(premise.lower().split()); hypothesis_words = set(hypothesis.lower().
- **sample output:** `Valid call (premise/hypothesis, 422 correctly on a missing field): $ curl -X POST /api/v1/native-ai/entailment -d '{"premise":"The quarterly revenue grew by 12 percent in Q3","hypothesis":"revenue grew in Q3"}' {"premise":"...","hypothesis":"revenue grew in Q3`
- **only one possible value in this deployment:** False

**The defect.** §4.5 class, "field whose NAME implies a determination the value cannot support" — the strongest instance of it, because the label is a logical claim (premise entails hypothesis) and the measurement is lexical containment, which is not evidence for it in either direction.

1. NEGATION AND ROLE INVERSION ARE REPORTED AS ENTAILMENT. "The sky is not blue" -> "The sky is blue" returns label ENTAILED: hypothesis tokens {the,sky,is,blue} are all present in the premise, ratio 4/4 = 1.0, and the token "not" — the entire semantic content of the premise — is simply not in the hypothesis set so it never enters the ratio. Same for "Alice paid Bob 500 dollars" -> "Bob paid Alice 500 dollars", ENTAILED. A user who reads ENTAILED concludes the premise supports the hypothesis; here the premise refutes it. The word-order-scrambled "blue is sky the" also returns ENTAILED, confirming order is not read at all. In the other direction, a genuine entailment with disjoint vocabulary (Socrates/mortal -> "Socrates will die") is downgraded to PARTIAL_ENTAILMENT. So the label is uncorrelated with entailment in both directions, and it is presented as the answer.

2. THE DISCRIMINATING NUMBER IS COMPUTED AND WITHHELD. overlap_ratio and the 0.9/0.2 cut-points exist at nli_engine.py:75-82 and never reach the response. The user gets a bare verdict with no way to see that a 4/4 token match produced it — a determination shipped without its evidence.

3. THE ADVERTISING OVERCLAIMS. native_ai.py:479-480 docstring says "REAL word-overlap natural-language inference"; the primitive catalog at native_ai.py:268-270 says "Real word-overlap natural-language inference (ENTAILED / PARTIAL / NEUTRAL)". The response `method` field, "word-overlap NLI (owned nlp)", is a partial mitigation — it does name the mechanism — but it still asserts "NLI", and naming a method does not license a label the method cannot earn.

4. EMPTY OUTPUT WITH NO REASON. hypothesis "" hits the `if hypothesis_words else 0.0` guard at :75 and returns NEUTRAL — indistinguishable from a genuinely unrelated hypothesis. Nothing was inferred; something was reported.

5. AN UNREACHABLE LABEL IN THE CONTRACT. The method docstring at nli_engine.py:64 says it returns "(ENTAILED, CONTRADICTION, NEUTRAL)". CONTRADICTION is never returned anywhere in the file. The one label that would have caught finding #1 does not exist in the implementation.

Aggravating: infer_intent, thirty lines above in the SAME class, was already repaired for exactly this defect class (the W430 comment at nli_engine.py:29-36, which added no_signal/tied/basis disclosure). verify_premise_entailment was left as-is. The remedy pattern is already sitting in the file.

**Why it is not wired.** Not do_not_wire: unlike the always-fails-consensus shape, this genuinely discriminates. All three labels are reachable on real input — I observed ENTAILED, PARTIAL_ENTAILMENT and NEUTRAL from different payloads — the function is deterministic and total, the request model is right, and a missing field honestly 422s. The underlying quantity (lexical containment of the hypothesis in the premise) is a real, cheap, useful measurement. Not wire_as_is: the measurement is real but the NAME on it is false. Shipping a surface that prints ENTAILED for "The sky is not blue" -> "The sky is blue" is worse than shipping nothing, because it manufactures confidence in a logical claim the code never evaluated. The fix is small and already patterned in this file (mirror the W430 treatment of infer_intent, nli_engine.py:29-60): a. Return the evidence: add overlap_ratio, matched/unmatched hypothesis tokens, and the 0.9/0.2 thresholds to the payload. b. Rename the labels to what is measured — FULL_LEXICAL_OVERLAP / PARTIAL_LEXICAL_OVERLAP / LOW_LEXICAL_OVERLAP — or keep the entailment names only behind an explicit `negation_checked: false` / `argument_order_checked: false` disclosure plus a `basis` string ("all 4 hypothesis tokens appear in the premise; word order and negation not examined"). c. Handle the empty hypothesis as its own outcome (label null, basis "hypothesis is empty — nothing to check") instead of NEUTRAL. d. Fix or drop the CONTRADICTION claim in the nli_engine.py:64 docstring, and drop "natural-language inference" from the endpoint docstring and the catalog entry at native_ai.py:268-270 in favour of "lexical overlap check". Nothing here is currently rendered in the frontend — grep for "entail" across apps/workstation-superapp returns nothing, including the developers/NativeAI.tsx catalog page — so the fix can land before any user ever sees a label.

## `POST /api/v1/native-ai/entropy`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** Route: C:\Users\rehan\Workstation\agentic_core\api\native_ai.py:425-437 (`native_entropy`, request model `EntropyRequest` at :421 — one field, `sources: List[Dict[str, Any]] = []`). Dispatches to: C:\Users\rehan\Workstation\agentic_core\crypto\entropy_pool.py:6-34 (`EntropyPool`). What it really computes: - `__init__` seeds the pool with the literal `b"v-infinity-genesis-seed"` (:8). - `add_entrop
- **sample output:** `Live calls against 127.0.0.1:8010 (HTTP 200, real payload every time): A. `{"sources":[]}` — repeated 3x, and `{}` with no field at all: {"seed":9392136076795838001,"bits_harvested":0,"pool_integrity":"31fe8b0b00925782","sources_mixed":0,"algo":"sha3_512 + XOR`
- **only one possible value in this deployment:** False

**The defect.** Three defects, the first two squarely §4.5-class ("a constant or fixed ramp presented as a measurement" / "a field whose name implies a determination the value cannot support").

(1) `bits_harvested` is a fixed +128 ramp, not a measurement. It is exactly `128 x sources_mixed` — a value already fully determined by another field in the same response. Nothing about the source content is examined. The live calls prove it: five empty `{}` dicts carrying zero information report **640 bits harvested** (case C), while one source declaring a 10 MB size and a 384-bit content hash reports **128** (case D) — less than the five empty dicts. Worse, case E reports **5120 bits harvested** into a pool whose entire state is a 512-bit SHA3-512 digest; a 512-bit register cannot hold 5120 bits of entropy. The name "harvested" asserts a quantity was measured off the inputs. Nothing discriminated.

(2) `pool_integrity` is a re-encoding of `seed`, presented as an independent digest. The handler docstring promises "a deterministic 64-bit seed + a pool-integrity digest" — two artefacts. They are one value. Verified against every live response: `struct.pack('<Q', seed).hex() == pool_integrity` returned True for all five (31fe8b0b00925782, c84bff7b4bd152e4, ff0510089573569e, 1252356f361dfbfa, 4c882cdb8defd5b1). A digest that is a byte-identical copy of the thing it claims to attest can never disagree with it, so it can never detect anything. It is decoration shaped like verification.

(3) Nothing is ever harvested. The response calls itself an "entropy pool" and reports "bits_harvested", but no system, hardware, or physical entropy is read anywhere — the pool is a hash chain over caller-supplied metadata strings. The single source of genuine unpredictability is the `metadata.get('timestamp', time.time())` fallback at :16, which fires only when the caller omits `timestamp` — a low-entropy, adversary-guessable wall-clock value, and one that is near-identical across all sources mixed in a single request (case C's five dicts land within the same instant). That path still reports the full 128 bits per source. A user reading "640 bits harvested" off case C is being handed roughly a handful of real bits.

What is NOT a defect, to be fair: the `algo` field ("sha3_512 + XOR mixing") is accurate — the mixing is genuinely SHA3-512 + XOR; and the docstring's determinism claim ("same sources with fixed timestamps => same seed") is true and I confirmed it (seed 12814411707299170380 twice). The dishonesty is confined to the two quantitative fields and the "harvested" framing.

**Why it is not wired.** Answering the question asked directly: yes, the response as a whole can vary — `seed` genuinely changes with the sources supplied (16452442510870924232 vs 11409433789912319487 vs 18085080848267563538 across cases B/D/E), so this is not the all-nodes-zero, one-outcome shape. But the variation is narrower than it looks, in three specific ways: - On the DEFAULT payload — `{"sources":[]}` or an empty body, which is what any "generate a seed" button with nothing to feed it will send — the answer is a hardcoded constant, forever, in this and every deployment: seed 9392136076795838001, pool_integrity "31fe8b0b00925782", both derived from the string literal `b"v-infinity-genesis-seed"` at entropy_pool.py:8. Three identical calls confirmed it. - `bits_harvested` can never take a value other than `128 x sources_mixed`. It carries no information the caller did not already send. - `pool_integrity` can never take a value other than the hex of `seed`. It carries no information the response did not already state. So two of the four substantive fields are non-discriminating by construction, and the third collapses to a constant on the default call. The underlying mechanism is real and worth keeping, which is why this is fix_then_wire and not do_not_wire. Minimum fixes before it reaches a user: (a) rename `bits_harvested` to something the value can support — `sources_mixed` already says it, so drop the field or relabel it `mixing_rounds` / `nominal_bits_per_source: 128 (fixed, not measured)`; (b) delete `pool_integrity` or make it an actual independent digest over the full 64-byte pool (e.g. hexdigest()[16:32], or a digest of pool||counter) rather than a copy of the seed bytes; (c) rename the primitive away from "entropy" or state plainly in the response that this is a deterministic seed derivation over caller-supplied metadata with no system entropy source, and that the seed must not be used as a key, nonce, or token. Fix (c) matters most — the catalogue entry at native_ai.py:271-273 is half-honest ("a deterministic seed for reproducible in-house seeding") and that sentence should be in the response body, not only in a catalogue a user never reads.

## `POST /api/v1/native-ai/quorum`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** C:\Users\rehan\Workstation\agentic_core\api\native_ai.py:445-457 (handler native_quorum, request model QuorumRequest at :439) dispatches to C:\Users\rehan\Workstation\agentic_core\quorum\sensing.py:6 (class QuorumSensing). What it really computes: concentration = agents x secretion (a loop calling secrete_ai2 which does `self.ai2_concentration += amount`), then get_behavior_mode() returns "COOPERA
- **sample output:** `Default body {} -> {"agents":1,"concentration":10.0,"threshold":50.0,"behavior_mode":"INDEPENDENT","cooperative":false,"method":"quorum sensing (owned biomimetic swarm)"} {"agents":6,"secretion":10.0,"threshold":50.0} -> {"agents":6,"concentration":60.0,"thres`
- **only one possible value in this deployment:** False

**The defect.** Five overlapping problems; the core one is "a computation over caller-supplied parameters presented as a measurement of the live system", plus "field names implying a determination the values cannot support".

1. NOTHING IS SENSED. The word "sensing" and the catalog line (native_ai.py:262-264) "Real bacterial-style AI-2 density model — the swarm flips COOPERATIVE/INDEPENDENT at a population threshold" both assert the endpoint detected a population. It did not. The population is a request field the caller types in. A real roster exists in this same deployment and is ignored: GET /api/v1/swarm/agents returns a live agent list (CEO, CFO, CTO, CMO, ...). The endpoint never consults it, or /api/v1/hub/agents, or anything else.

2. "SHARED FIELD" DOES NOT EXIST. Docstring (:448) and the QuorumRequest comment (:440, "number of agents currently signalling into the shared field") describe agents signalling into shared state. A fresh QuorumSensing object is constructed per request (:451) and discarded. Three consecutive identical calls each returned concentration 30.0 — proof there is no field and nothing signals into it.

3. "REAL THRESHOLD KINETICS" IS FALSE. Docstring (:449) claims kinetics; the class advertises t1/2 ~ 2 hours decay. Zero kinetics execute: update_concentration (the only decay code) is unreachable from this handler and from all live code. The runtime path is integer-count multiplication and one `>`.

4. behavior_mode / cooperative ARE MISNAMED. They read as a determination about how the swarm is actually operating. They can only restate whether the caller's own product exceeded the caller's own threshold. A user reading `"behavior_mode":"COOPERATIVE"` would reasonably conclude the swarm has entered cooperative mode; nothing in the system changed and nothing was observed.

5. THE REPORTED NUMBERS CANNOT REPRODUCE THE REPORTED VERDICT. concentration is round(...,2) at :455 but the comparison at sensing.py:34 uses the unrounded value. Two different requests both render {"concentration":50.0,"threshold":50.0} while returning cooperative false and cooperative true respectively. One of those responses shows 50.0 > 50.0 evaluating to true. Related: no validation on secretion, so {"secretion":-100} yields "concentration":-300.0 emitted as a concentration with a straight-faced INDEPENDENT verdict.

**Why it is not wired.** Not the classic §4.5 shape — the output genuinely varies (INDEPENDENT/COOPERATIVE, concentration 0.0 / 10.0 / 60.0 / 10000.0 / -300.0), so it is not "only one value possible". But the variation is information-free with respect to this deployment: the response is a pure function of the request body, identical forever for a given payload no matter what the Workstation's actual agent population is. It is the adjacent honesty class — arithmetic on user input dressed as a biological measurement, with names (sensing, shared field, kinetics, behavior_mode) asserting determinations the values cannot support, plus a rounding bug that lets the payload display 50.0 > 50.0 = true. The math is correct and the primitive is cheap to make honest, so do not delete it. Fix before wiring: (a) Wire agents to the real roster — read GET /api/v1/swarm/agents (live, non-empty) and return the sensed count as the default, with the request field only as an explicit override, echoing which was used (e.g. "population_source":"live_roster"|"caller_supplied"). (b) If (a) is out of scope, keep the parameters but stop claiming sensing: rename to a threshold calculator, rename behavior_mode -> mode_if_population_were, and say plainly "computed from supplied parameters; no live swarm was observed". (c) Drop "Real threshold kinetics" from :449 and the "shared field" language at :440/:448, or actually call update_concentration — as written both claims are false. (d) Fix the rounding: compare and report the same value (or report full precision), so a user can re-derive the verdict from the payload. (e) Validate secretion >= 0 rather than emitting a negative concentration.

## `POST /api/v1/native-ai/rigor`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** agentic_core/api/native_ai.py:533-543 (`native_rigor`) → process-global `_RIGOR` built at native_ai.py:522-530 → `LiveRigorMonitor.validate_metric` at agentic_core/statistics/live_rigor_monitor.py:20-52. What it really computes: - It keeps `self.metric_history[metric_name]` in memory and appends whatever number the caller POSTs. There is no "live metric series" — the series IS the caller's own sub
- **sample output:** `First call for any new metric name (payload {"metric_name":"zzz_new2","value":999999.0,"baseline":0.0}): {"metric":"zzz_new2","value":999999.0,"baseline":0.0,"ci_95":[999999.0,999999.0],"p_value":1.0,"power":0.51,"significant":false,"method":"scipy CI + one-sa`
- **only one possible value in this deployment:** False

**The defect.** Four defects, the first two squarely §4.5-class.

1. `power` is a fixed ramp presented as a measurement. It is `n/100 + 0.5` over the call count and nothing else. The field is named `power`, the handler docstring says "power-gated significance", and the capability registry (native_ai.py:253-255) advertises "power-gated significance over a live metric series". The class docstring says "Monitors production metrics with 95% CI and power analysis." No power analysis exists. `power: 0.51` on the first call is not a property of the data; it is `1/100 + 0.5`.

2. `significant` is a determination the value cannot support — it is decided by call count, not evidence. Real output: `"p_value": 1.5000180001300012e-24, "significant": false`. The t-test screamed, and the endpoint reports "not significant" because a fabricated number was below 0.8. Conversely at n=34 `significant: true` arrives because the counter crossed 30, not because anything about the evidence changed. A user reading `significant` is reading a call counter wearing a statistics label.

3. Unmeasured values reported as measurements, with no reason given. For every first call on any metric name — the only call a one-shot UI or an agent would ever make — the output is invariably `ci_95: [value, value]`, `p_value: 1.0`, `power: 0.51`, `significant: false`, whatever the numbers are. `p_value: 1.0` was never computed (n<=2 short-circuit at line 32) but is returned in the same shape as a real one; `ci_95: [999999.0, 999999.0]` is n=1 masquerading as an infinitely precise 95% interval. Nothing in the payload says "not enough samples". The `method` string — "scipy CI + one-sample t-test (owned statistics)" — asserts a t-test that did not run.

4. Crash on the commonest real case, plus a phantom ledger entry. A metric that has not moved (value == baseline, constant series) makes `stats.ttest_1samp` return NaN at n>=3; `float(nan)` then fails FastAPI's JSON serialization and the caller gets HTTP 500. But `await self.ueg.log_event(...)` on line 51 already fired, so a NaN "STATISTICAL_VALIDATION" is sealed into the UEG provenance chain for a response no user ever received. The existing regression test (integration_tests/test_mvp_spine.py:3977) posts the flat metric exactly once, so n stays at 1, `p_value` takes the hardcoded 1.0 path, and the crash is never reached. That test also asserts only `isinstance(last["significant"], bool)` — it never asserts `significant` is ever True, so the power gate is untested.

Secondary: code comment at line 27 and the `_compute_ci` docstring both say "Bootstrap"; no bootstrap is performed (it is a t/SEM interval). The response `method` string is accurate here, the internal docs are not.

**Why it is not wired.** Direct answer to "could this ever return anything other than what you just saw": yes, but not for any reason a user would expect. `ci_95` and `p_value` do vary with the data once n >= 3 — those are genuine scipy. `power` can NEVER vary with the data; it is `n/100 + 0.5` and nothing else. `significant` is therefore frozen at false for the first 29 submissions of every metric name regardless of evidence, and every first call on a fresh metric name returns the identical fixed triple `p_value 1.0 / power 0.51 / significant false`. I flipped it to true only by POSTing 34 times, which changed the counter, not the evidence. So it is not literally single-valued, but the one field that claims to be the determination is driven by a call counter. Not do_not_wire: the CI and the t-test are real, and the fixes are small and local — (a) delete `power` and the power gate, or rename it `sample_count_ramp` and label it simulated as the source comment already does internally; (b) return `p_value: null` with `"reason": "n<3, t-test not run"` instead of a fabricated 1.0; (c) return `ci_95: null` (or flag `n=1`) instead of a zero-width interval; (d) guard the zero-variance NaN before both the UEG write and the response, returning an honest "no variance in series" rather than a 500 plus a poisoned ledger entry. Until (a) and (b) land, the endpoint tells users the opposite of what its own statistics found.

## `POST /api/v1/native-ai/topology`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** agentic_core/api/native_ai.py:409-419 (TopologyRequest at :404) dispatches to agentic_core/topology/defense.py:21 TopologyDefense.compute_persistent_homology, constructed fresh per request. What it really computes: - defense.py:55 beta0 = len({_find(n) for n in node_ids}) — real union-find, and it only unions edges that pass validation (`if a in parent and b in parent`); malformed/dangling edges a
- **sample output:** `Well-formed input — correct, and it discriminates: tree {"nodes":["a","b","c"],"edges":[["a","b"],["b","c"]]} -> {"beta0_components":1,"beta1_cycles":0,"status":"STABLE","nodes":3,"edges":2,"method":"graph Betti numbers via Euler characteristic (owned topology`
- **only one possible value in this deployment:** False

**The defect.** Two §4.5-class defects, both user-visible.

1. beta1_cycles is manufactured from an unvalidated count — a field whose NAME implies a determination the value cannot support. beta1 comes from `len(edges)` (defense.py:57), the raw request list length, while the union-find that produces beta0 discards every edge that is malformed or names a node outside the node list. Nothing discriminated: with edges=["junk",42,null,{"nope":1}] the engine accepted zero edges yet reported "beta1_cycles": 4 — presented as "independent cycles / structural holes" per the handler docstring and the capability catalog (native_ai.py:276 "β₁ cycles ('structural holes'); detects fractures"). Dangling edges do the same (beta1_cycles: 3 on a graph with no usable edges). This is the realistic failure mode, not a contrived one: any caller building the graph from logs or a registry where edges can reference pruned nodes gets fabricated structural holes. The reported `edges` count is the same inflated raw number, so the response is internally inconsistent with its own stated method and gives the user no way to notice.

2. status is a hardcoded, undisclosed threshold wearing the name of a temporal detection. "SPIKE_DETECTED" asserts a rise against a baseline; no baseline exists and nothing temporal is measured. `self.history = []` (defense.py:18) is initialized and never appended to, and native_ai.py:415 constructs `TopologyDefense()` fresh on every request, so history could not accumulate across calls even if it were written. The 3.0 cutoff (defense.py:17) never appears in the response, so "STABLE" alongside beta1_cycles=3 reads as a health verdict when it only means "≤ an arbitrary constant you were not shown". And status ignores beta0 entirely: 8 isolated nodes return "status":"STABLE" from the primitive whose catalog entry advertises "detects fractures".

**Why it is not wired.** The core math is real and genuinely discriminates — this is not the consensus/zero-node shape. The graph comes entirely from the request body, so nothing in the deployment pins the answer: across calls I observed beta0 ∈ {0,1,2,3,8}, beta1 ∈ {0,1,2,3,4,6}, and both status values. On well-formed input every result was exactly correct (tree 1/0, triangle 1/1, two components 2/0, K5 1/6). That part is worth wiring. But it must not ship as-is, because the two shapes above are exactly the class this codebase keeps finding. Fixes, all local to defense.py: (a) count the edges union-find actually accepted and compute beta1 from that; return both `edges_submitted` and `edges_applied` so the user sees the discard, or 422 on edges that are not [u,v] / {source,target} pairs and on edges naming unknown nodes. (b) surface `beta1_threshold: 3.0` in the response and rename status to something a single-shot measurement can support (e.g. `beta1_over_threshold: true`) — drop "SPIKE" unless history is actually retained across calls, which the per-request construction at native_ai.py:415 currently prevents. (c) either make status read beta0 or stop advertising "detects fractures" at native_ai.py:276. Decide separately whether duplicate edges and self-loops (beta1=4 for 4 parallel edges, 4 self-loops) are intended multigraph semantics — those are defensible, but should be stated.

## `POST /api/v1/native-ai/transduce`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** Handler: C:\Users\rehan\Workstation\agentic_core\api\native_ai.py:388-401. Line 394 dispatches to EmpiricalSignalTransduction(frequency, hill).simulate_cascade(input_signal); lines 395-398 build the response. Impl: C:\Users\rehan\Workstation\agentic_core\signaling\empirical_transduction.py:17-33. The whole "ODE-inspired phosphorylation kinetics" is four lines: line 15: self.base_latency = 45.0 # S
- **sample output:** `POST {"input_signal": 0.55, "frequency": 0.5} -> {"input_signal":0.55,"peak_intensity":0.6055337375087939,"latency_s":29.032258064516128,"hill":4.5,"frequency":0.5,"propagated":true,"trajectory_points":100,"method":"Hill-equation pulsatile cascade (owned signa`
- **only one possible value in this deployment:** False

**The defect.** Three separate §4.5-class defects in one 8-field response.

(1) FIXED RAMP PRESENTED AS A MEASUREMENT -- `latency_s`. base_latency is the literal `45.0 # Seconds` (empirical_transduction.py:15) and latency = 45.0/(1+input_signal). Nothing is timed. It is provably independent of `hill` (identical 30.2013 / 29.8013 at hill = 1.0, 3.2, 4.5, 5.7, 20.0) and of `frequency` (identical 29.032258 at f = 0.001 through 1.5). The field name `latency_s` plus the capability blurb "(with latency kinetics)" (native_ai.py:261) and the handler docstring "Real biochemical-kinetics math, not a constant" assert a measured duration in seconds. It is a constant divided by (1+x). The endpoint itself answers in milliseconds while reporting "latency_s: 29.03".

(2) A DETERMINATION THE CASCADE CANNOT SUPPORT -- `propagated`. Because peak = 0.99987 * s^h/(0.5^h + s^h), and s^h/(0.5^h+s^h) >= 0.5 <=> s >= 0.5 for ANY h > 0, the boolean is algebraically identical to `input_signal >= 0.5`. Verified: at hill=1.0 and hill=20.0 alike it flips between s=0.49 and s=0.51. The Hill coefficient, the frequency, and the 100-point trajectory are decorative with respect to the headline determination. The user is told a signal "propagated supra-threshold through a biomimetic cascade"; the actual content is "the number you sent is >= 0.5".

(3) A PARAMETER ECHOED AS GOVERNING WHEN IT DISCRIMINATES NOTHING -- `frequency`. peak_intensity is byte-identical (0.6055337375087939) across the entire advertised "pulsatile decoding (0.02-0.8 Hz)" band. Its only residual effect is a sample-grid artifact. Yet `frequency` is reflected in the response payload beside the result, and docs\AGENTIC_CORE_INTEGRATION_AUDIT.md:105 certifies the module "REAL biomimetic math (Hill-equation sigmoidal cascade + pulsatile decoding...)". The pulsatile decoding does not exist; the sine contributes one constant scale factor of 0.9998741277 and is otherwise thrown away by max().

Supporting: the trajectory is exactly symmetric about zero (min = -max, 49/100 points negative) -- an "activation cascade" that is negative half the time, which no phosphorylation model produces. And `input_signal: -0.5` returns HTTP 200 with peak_intensity 0.49993706383693753, numerically identical to +0.5, because (-0.5)**4.5 is complex (K = 0.5+0.5i) and float() silently discards the imaginary part; `input_signal: -1.0` returns HTTP 500. A fabricated real number from complex arithmetic, unflagged.

**Why it is not wired.** Not single-valued: peak_intensity and latency_s do track input_signal, so this is not the "consensus that always fails" shape. But the answer to "could this ever return anything other than what you just saw?" is: only along ONE axis, input_signal, and only through a plain saturating sigmoid of the caller's own number. Every other knob is inert. Freeze input_signal and the entire response is frozen -- no state, no measurement, no deployment fact can move it, at any frequency in the documented band, at any Hill coefficient. The salvageable core is real: K = s^h/(0.5^h + s^h) is a genuine monotone Hill transform, and `hill` genuinely changes its steepness (0.400 vs 0.477 at s=0.49). That is why this is fix_then_wire rather than do_not_wire. But the fix is substantial, not cosmetic: - DELETE `latency_s` (do not rename it). There is no latency here to report; 45/(1+x) has no referent in this system. - DELETE `frequency` from the request model and the response, or make the sine actually enter the result (e.g. report frequency-dependent transmitted power rather than max()). Today it is a lie by echo. - RELABEL `propagated` for what it is -- `input_signal >= 0.5` against a hardcoded K50 -- and expose K50 as a field rather than burying `0.5**self.hill` in the expression. - CHANGE `method` from "Hill-equation pulsatile cascade" to "Hill saturation transform, K50=0.5" and drop "pulsatile". - 422 on input_signal < 0 instead of returning a complex artifact at 200 / crashing at 500. - Correct docs\AGENTIC_CORE_INTEGRATION_AUDIT.md:105, which certifies "pulsatile decoding" and "latency inversely scales with signal" as REAL. Also worth flagging: agentic_core\ai\native\orchestrator.py:661-668 feeds consensus.proceed_fraction into this same module and surfaces the same `latency_s` and `propagated` fields inside the /tree response, so the same three defects are already on a second, more visible surface.

## `POST /api/v1/native-ai/validate`

- **status:** OPEN · fix_then_wire · not reachable from any UI
- **implementation:** Route: agentic_core/api/native_ai.py:551-558 (`native_validate`, model `ValidateRequest` at :545). It dispatches to `AccuracyValidator().validate_output(...)` at agentic_core/validation/accuracy_validator.py:17-54, constructed fresh per request (so `validation_history` / `get_aggregate_accuracy` / `check_compliance` are dead here). What each branch really computes: - accuracy_validator.py:22 — `co
- **sample output:** `All returned HTTP 200 with a real payload. Real calls against 127.0.0.1:8010: SEMANTIC (genuinely discriminates — this branch is fine): {"prediction":"totally unrelated gibberish","actual":"the cat sat on the mat","task_type":"SEMANTIC"} -> {"is_accurate":fals`
- **only one possible value in this deployment:** False

**The defect.** Four distinct §4.5-class defects. The SEMANTIC branch is honest; the other three-quarters of the surface are not.

1. CONFIDENCE THAT NOTHING COMPUTED (accuracy_validator.py:22 + :44-45). In the `else`/GENERIC branch `confidence` is never assigned — the caller receives the bare initializer `1.0`. A field named `confidence` reports maximum confidence for a flatly wrong answer (`alpha` vs `omega` -> `is_accurate:false, confidence:1.0`). It is structurally incapable of taking any other value on this branch. This is exactly the nli_engine shape: an untouched default reported as a determination.

2. SILENT FALLTHROUGH MISLABELLED AS DIFFLIB. `task_type` is a bare `str` with no enum validation (native_ai.py:548), so anything outside the four documented values — including the lowercase typo `"semantic"` — lands in the `else` equality branch. The response then echoes the caller's own string back as `task_type` and attaches the hardcoded `"method":"...(difflib, real)"` (native_ai.py:558). The user is told difflib semantic similarity ran when a Python `==` ran. The `method` field, the one thing meant to make this endpoint auditable, is a constant that does not track the branch taken.

3. APP_CODE IGNORES THE REFERENCE AND FABRICATES ITS CONFIDENCE (:39-42). The endpoint docstring promises "code-presence checks against a REFERENCE". `actual` is never read on this branch. `confidence` is the literal `0.85`/`0.2` — a constant presented as a measurement, with no quantity behind it. Worst concrete consequence: `"I could not define anything, import failed"` validates as `is_accurate:true, confidence:0.85` purely because it contains the substring `"import "`. A validator that stamps a model's own failure message as accurate is worse than no validator, because a caller gating on `is_accurate` will pass the failure through.

4. NUMERICAL: two wrong answers, both presented as verdicts. (a) `error <= 0.01 * actual` compares a non-negative error against a negative tolerance whenever `actual < 0`, so an exact match returns `is_accurate:false` — and pairs it with `confidence:1.0` from the untouched initializer path being partly overwritten (`1/(1+0)`), so the response reads "definitely wrong, with total confidence". (b) The bare `except:` at :30 converts a type error into `is_accurate:false, confidence:0.0` — an empty/zero output with no statement of why it is empty. `"hello"` vs `"hello"` is reported as a failed numeric validation rather than as a malformed request; an honest 422 or an error field is what this case warrants. Separately `confidence = 1/(1+error)` is scale-blind: an absolute error of 0.5 yields 0.6667 whether the reference is 100 or 1000, so the number is not on any confidence scale — it is a decay curve wearing a probability's name.

**Why it is not wired.** Answering the question as asked — could this return anything other than what I saw in THIS deployment? Per branch: SEMANTIC yes, it genuinely varies with the input (difflib is real and discriminating, 0.2449 vs 1.0 on my two calls). But the `confidence` field on GENERIC and on every unrecognised task_type can only ever be 1.0, no input can move it; on APP_CODE it can only ever be 0.85 or 0.2, and no value of `actual` can move it at all because `actual` is never read. So three of the four documented task types report a `confidence` that nothing discriminated, and the `method` string is a constant on all four. Not do_not_wire: the SEMANTIC path is a real reference comparison and is the one genuinely useful capability here, so the endpoint is worth keeping. Not wire_as_is: the surface is labelled "validation" with a `confidence` score and an explicit "(difflib, real)" provenance claim, and a caller gating on `is_accurate`/`confidence` would be actively misled — most sharply by APP_CODE stamping a failure message as accurate at 0.85. Minimum fixes before wiring: (1) make `task_type` a validated enum so an unknown value 422s instead of silently becoming `==`; (2) compute `method` from the branch actually taken rather than hardcoding it at native_ai.py:558; (3) on GENERIC either compute a real confidence or drop the field / return `null` and say it is unmeasured; (4) on APP_CODE either compare against `actual` or rename the branch to what it is (a syntax-token presence heuristic) and drop the fabricated 0.85 — presence/absence is a boolean, not a confidence; (5) NUMERICAL: use `abs(0.01 * actual)` for the tolerance, and let the `except` return an explicit error rather than a `false`/`0.0` verdict.


---

# §4.5-class defects OUTSIDE the native-AI primitives

**W433 — swept, 7 live defects found and ALL FIXED.** Grepping the shapes rule 13 names across
`agentic_core` gave 25 candidate sites; 9 were reachable; 7 carried a live defect. Every one was the
same sentence — *"the top X"* resolved by insertion order — over data where ties are the NORMAL
condition (small integer counts, or dict keys inserted in fixed order).

| site | claim | status |
|---|---|---|
| `products.py` Studio max/min | top performer, fed to "Recommended Action" | FIXED — `tied_with` + the prompt stat |
| `swarm.py` served_by | model credited for a cascade verdict — **moves routing** | FIXED — every tied leader credited |
| `organism_status.py` dominant_trait | population's dominant trait | FIXED — null + `dominant_trait_tied` |
| `resource_fabric.py` dominant_trait | same field | FIXED — null + `dominant_trait_tied` |
| `immune.py` hot_endpoint | most affected endpoint | FIXED — + `hot_endpoint_errors` |
| `governance.py` verdict | **rejected vs held** | FIXED — most restrictive + `governance_ambiguous` |
| `products.py` top realm | portfolio leader | FIXED — count + tie phrase |

Guards: `test_w433_studio_discloses_a_tied_max_instead_of_naming_one` ·
`test_w433_cascade_quality_is_credited_to_every_model_that_led` ·
`test_w433_superlatives_disclose_ties_and_carry_their_magnitude` ·
`test_w433_governance_tie_resolves_to_the_most_restrictive_and_says_so`.

The remaining entry below is LATENT — unreached code.

The class was named after nine instances in one subsystem. These are the sites found by grepping
the shapes rule 13 names — `max(` over a mapping, a `sort` then `[0]`, a loop returning the first
item clearing a threshold — across the rest of `agentic_core`.

**Reachability is checked FIRST here, and that ordering is the lesson.** The entry below was
audited in depth — including measuring how badly noise outweighed the real signal — before anyone
asked whether it runs. It does not. A defect in unreached code is a ledger entry, not an incident,
and inflating one into the other wastes exactly the attention the real ones need.

## `GenomeEvolutionEngine.run_evolution_cycle` — fitness is mostly a random number

- **file:** `agentic_core/evolution/evolution_engine.py:98` — `max(fitness_scores, key=fitness_scores.get)`
- **status:** OPEN · **LATENT — no live caller**
- **reachability:** ZERO imports in live code. The three references to the name are STRINGS: a
  reconfiguration flag (`reconfiguration.py:60`), a gateway agent label
  (`v191/evolution.py:138`), and a resource-registry `rtype` whose real endpoint is
  `/api/v1/sovereign-evolution/cycle` (`resource_fabric.py:180`). Every genuine import is under
  `_archive/`. The heartbeat's `auto_evolve` calls `sovereign_evolution.run_cycle`, NOT this.

**The defect.** `fitness_scores[id] = 0.5 + (0.2 if any gene is COMMERCIAL else 0) + 0.3 * random()`.
The only criterion carrying meaning — mission alignment — is worth 0.20, while the random term spans
0.30. Measured over 200,000 head-to-head pairs, a NON-commercial mutant out-scores a commercial one
**5.6%** of the time purely on the roll. Worse, among mutants sharing gene types — the common case —
fitness is **100% noise**, so "Identify Optimal Offspring" selects the luckiest, not the fittest,
and the log reports `Best fitness: X` as though something was measured.

**Minimal fix, if it is ever revived:** derive fitness from something the mutant actually differs
on, or drop the random term and DISCLOSE that selection within a cohort is arbitrary. Do not keep a
field named `fitness` whose dominant component is `random()`.
