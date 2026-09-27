# THE NATIVE AI FABRIC — the enhancement roadmap, interrogated

**Status:** design accepted for build as plan items **P3.20 – P3.24**, extending the cognitive items
**P3.12 – P3.19** that already exist. Nothing here describes running code. Every "what exists" claim was
measured against this working tree and this machine on **2026-09-27 (round W495)** by the command named
beside it.

**Source.** The Owner supplied an architect's *Native AI Fabric Strategic Enhancement Roadmap v2.0* and an
*Execution Directive* for four phases (wire the cognitive engines to local models · deploy LoRA specialists
and a knowledge graph · activate a litigation/career agent swarm with a verifier · prototype world models),
with the instruction to interrogate, review, adjust and build on it. This document is that interrogation.

**The brief's central diagnosis is correct, and this is the measurement that proves it:** of the six
cognitive engine modules in `agentic_core/cognitive/`, **zero contain any reference to the gateway, the
orchestrator or a model call** (`grep -c "gateway\|orchestrator\|complete(" agentic_core/cognitive/*_engine.py`
→ 0 for all six). The architecture routes; the cognition does not compute. That is exactly what the brief
says, and it is already the open work of plan item **P3.12** with five registered rows.

Everything else in the brief needs adjusting, and one part of it cannot be built on this machine at all.

---

## 1 · The measured audit

| The brief says | Measured on 2026-09-27 | Verdict |
| :-- | :-- | :-- |
| "Register the 9 engines (Soch, Samajh, etc.)" | **6 engine modules exist** (inkashaf, aqal, samajh, hoshiyari, soch, iman). The registry's `EngineType` enum declares **9** — adding tawazun, niyyah, tafakkur — and **none of those three exists in the live tree**. `cognitive/foundational/`, `cognitive/meta/` and `cognitive/v2/` are empty package shells (`__init__.py` only). | **WRONG as an action.** Registering nine would register three engines that do not exist. Already recorded: FU-221 (the registry is never populated and its call signature does not match the engines), FU-224 (the contract excludes the three meta engines). |
| "Un-archive `cognitive/bootstrap.py`" | It exists **only** at `_archive/jules-unwired/agentic_core/cognitive/bootstrap.py`, and it imports the nine engines from `foundational/` and `meta/` — paths that hold nothing in the live tree. | **PARTLY.** The file is a 26-line registration list, not the work. |
| (implied) the archived engines are a starting point | The three archived meta engines are **7-line stubs returning literals**. `niyyah_engine.py` returns `{"ratified": True, "signatures": ["council_node_1", "council_node_2", "council_node_owner"], "intent_status": "COMMITTED"}` — a fabricated governance record with three invented signatories. The archived `base_engine.py` hard-codes **`confidence=0.95`** on every successful output. | **REJECTED as a recovery target.** Un-archiving those would import a fabricated ratification and a confidence nothing computed — the class FU-233 and FU-224 already record. |
| "Set up `vector_store.py`" / GraphRAG / Neo4j | No `vector_store.py` and no embedding backend anywhere in the repo. | **MISSING.** Must be built, and on owned components (see §4). |
| "LoRA adapters: `uk-law-lora`, `gmp-science-lora`, …" hot-swapped to save VRAM | `agentic_core/ai/native/model_resource.py` exists; a repo-wide grep for `adapter`/`lora` in `agentic_core/ai/` returns **one comment and no implementation**. | **NOT SUPPORTED**, and see §2 — there is no VRAM to save. |
| "Pull `llama3:8b`, `deepseek-r1:8b`, `phi3:mini`" | Ollama **is** installed. `ollama list` holds `llama2:latest` (3.8 GB), `llama3.2:latest` (2.0 GB), `llama3.2:1b` (1.3 GB). None of the three named models is present. | **PARTLY** — a runtime exists; the models do not. |
| The 9 cognitive engines as the Phase-1 deliverable | This is **plan item P3.12** (+P3.13 for the meta three), already carrying FU-221, FU-223, FU-224, FU-229 and FU-257. | **ALREADY PLANNED.** The roadmap's Phase 1 is not new work; it is an existing item with five rows. |

---

## 2 · The ceiling this machine puts on the plan

Measured with `Get-CimInstance` on 2026-09-27:

| | Measured |
| :-- | :-- |
| RAM | **7.7 GB total** |
| CPU | Intel Core **i3-1315U**, 6 cores |
| GPU | **Intel UHD Graphics (integrated, ~1 GB shared)** — `nvidia-smi` is not installed and no discrete GPU is present |

The roadmap's model stack does not fit inside that, and no amount of configuration changes it:

- **DeepSeek-R1-Distill-Qwen-14B** and **StarCoder2-15B** (its T3 tier) need roughly 9–12 GB at 4-bit —
  **more than this machine's entire RAM**. They cannot load, let alone run.
- **Llama-3-8B-Instruct** (its T2 tier) is ~4.7 GB at Q4. That is nominally loadable but shares 7.7 GB with
  Windows, the browser, the dev server, the backend and the suite; on a CPU-only i3 a reply is minutes, not
  seconds.
- **Qwen-VL** vision (T4) — no.
- **"Adapter hot-swap onto the same base model instance to save VRAM"** — there is no VRAM. Integrated
  graphics with ~1 GB shared is not an inference device here; Ollama runs on the CPU.
- What *is* runnable today: **`llama3.2:1b` and `llama3.2` (3B)** — T1-class reflex and routing models —
  plus the deterministic floor the platform already owns.

**So the tiering is adopted as an ARCHITECTURE and refused as an inventory.** The registry will declare a
tier per resource and report, per tier, `runnable here: yes/no` **with the measured reason** — not a list of
models the platform cannot run. A surface that lists a 14B reasoning model on a 7.7 GB machine is the same
defect as a leaderboard nothing scored.

**This is an Owner decision** (registered): design for the 1–3B local tier plus the floor, provision real
hardware, or route specific high-value tasks to an Owner-gated external accelerant (which the platform
supports today and keeps switched off by default).

---

## 3 · Adopted as-is

| Idea | Why it is worth building here |
| :-- | :-- |
| **A tier declared per resource** (deterministic logic · reflex/routing · domain specialist · synthesis · perception) | The fabric already has a registry and a `prefer` control; what it lacks is a statement of *what class of work a resource can do*, which is what makes routing inspectable instead of a guess. |
| **The chain: classify → retrieve → draft → verify → synthesise** | Each step is separately assertable, and the verify step is where this platform's whole discipline lives. |
| **Agents as executors, not records** | Matches the measurement: the engines are records today. |
| **Staged simulation** — template/rules → retrieval over real precedent → causal graph → shadow-mode learned model | The staging is honest: each stage is a different kind of claim, and the early stages are checkable arithmetic rather than prediction. |
| **A verifier as an independent step** | Correct, with the adjustment in §4: it must check *checkable* things. |
| **Three circuit breakers** — withhold on an unverified claim · a **sacred-text firewall** · a data-egress alarm | The firewall is the canon rule made executable, and the egress alarm is the right shape for the Owner's sensitive material. |
| **Quadra-Veritas's four pillars** (evidential · logical · ethical · operational) | Maps onto the existing QMS gate, the compliance verdicts and the gaas.v5 interceptor rather than replacing them. |

---

## 4 · Adopted with adjustment

| Brief | Adjustment, and why |
| :-- | :-- |
| "If verifier confidence < 0.8, output is withheld" | **A model's confidence about itself is not a measurement.** This repo already carries three rows against exactly that shape (FU-233 a pipeline starting at 0.90 and adding 0.05 per iteration; FU-224 a contract forcing a float, which is why implementers return 0.96; the archived `base_engine.py` at 0.95). The verifier checks **checkable** things — does every citation resolve to a document in the index? does the quoted line exist at the cited page? does a statute reference exist in the retrieved text? — and returns **MET / UNMET / NOT ASSESSABLE** per check with the basis. A withhold is triggered by an UNMET check, never by a number a model wrote about itself. |
| LoRA specialists (`uk-law-lora`, …) as the Phase-2 deliverable | No such adapter exists to download, and training one needs a labelled corpus the Owner does not have. Specialisation comes from **retrieval + a domain prompt + the verifier**, which is buildable now. The registry keeps an **adapter slot** that reports `adapter: none installed` rather than implying one. |
| GraphRAG on Neo4j with `sentence-transformers` | No embedding backend is installed and external calls are Owner-gated. Build the **owned index** (lexical + a document/citation graph the platform writes itself), report `embeddings: none installed`, and never imply semantic recall. Shares P2.13's scan bounds, secret-exclusion rules and three-state per file. |
| "Register the 9 engines" | Six exist; three do not. P3.12 makes the six compute or declare themselves unassessable; P3.13 is where the other three get **written**, not registered. |
| "Replace constant returns with actual calls to local Ollama models" | Right, with the floor rule the platform already enforces: when no model serves, the engine returns **not assessable with the reason** — it does not fall back to a literal. On this hardware the 1–3B tier will often be the only model available, so the unassessable path is the common path and must be first-class. |
| **Tribunal outcome prediction** — "probability distribution of winning/settlement range", "judge tendencies (from public rulings)" | **Refused as specified.** There is no outcome dataset here, no judge data, and a settlement range presented to a party in a live matter is a number they may act on. What is adopted instead is **procedural**: deadlines and hearing windows computed from published rules and the case's own dates — checkable arithmetic, labelled as a schedule and not a forecast. The predictor stays out until the Owner asks for it with a data source, and even then it would be labelled a heuristic and never a legal opinion. |
| The litigation agent over the Owner's real case documents | Adopted with the same gate as P2.13: the Owner's legal material is **sensitive personal data**. Read-only, local-only, never sent to any external service (the egress alarm covers this), indexed with provenance per document, and every drafted output carries a **human-approval gate** and states that the platform does not give legal advice. Registered as an Owner decision. |
| "The Litigation Strategist drafts witness statements" | It may assemble, cite and cross-check; the Owner writes and signs. A drafted document carries its provenance and its unresolved checks on the page, not just in a log. |
| Career/CV agent ("STAR examples from completed projects") | Adopted, with one hard rule: it may only assemble from what the Owner recorded. It never invents an achievement, a metric or a date — the CV is a claim about a person, and the same rule as A.9.5 applies to a professional record. |
| "Phase 1–4 in 90 days, weeks 1–4, 5–8 …" | The plan measures pace in **rounds** from its own register and refuses to give dates (`followups.py forecast`). The phases are adopted as ordered items; the week numbers are dropped. |

---

## 5 · Rejected

| Rejected | Reason |
| :-- | :-- |
| The "Final Summary of Execution Status" table — Phase 1 **WIRED**, Phase 2 **DEPLOYED**, Phase 3 **ACTIVE**, Phase 4 **PROTOTYPED** | A status table asserting four phases are done, in the same document that proposes doing them. Nothing was wired, deployed, activated or prototyped. |
| "The Workstation is now alive. It thinks, it remembers, it verifies, and it predicts." | A claim about code that does not exist. Identical to the Horizon brief's "The Organism is Now Alive" (see `docs/HORIZON_INTEGRATION.md`). |
| The Execution Directive's code blocks | Every `python`/`yaml` block in the delivered text is **empty** — line numbers only (`12345678910…`). There is no implementation to review; what arrived is a roadmap. Said plainly here so no later round mistakes it for delivered code. |
| "Judge tendencies (from public rulings)" as a model input | Not available, not verifiable, and improper as a basis for advice to a party. |
| Confidence thresholds as the safety gate | See §4. A threshold over an invented number is a gate that cannot refuse. |
| "Register the 9 engines" as a Phase-1 success criterion | It would pass while nothing computes — the criterion is *does an engine read its input*, which is what P3.12's rows already say. |

---

## 6 · The two postures this touches

**The law domains.** Nothing the platform produces is legal advice, and no output about a live matter
leaves this machine. Every assembled claim carries the document and line it came from; every unresolved
check is visible on the page; every filing-shaped artefact is gated on the Owner's approval. The platform
may be a meticulous clerk. It may not be counsel.

**Faith content (canon, unchanged).** Quran Arabic is never generated; Quranic text comes only from
`quran.com`, `alquran.cloud` or `tanzil.net` with recorded provenance; recitation is never scored; AI
content is labelled; ruling **A.9.5** stands — the Fitrah Spectrum is never a measurement and no AI verdict
is passed on a person's spiritual state. The brief's **sacred-text firewall** is adopted as the executable
form of the first two: a generation request that would emit Quranic Arabic is **intercepted and replaced by
a retrieval call**, the interception is recorded, and the surface says the text was retrieved, from where.
The brief's "tokenizer-level" framing is adjusted to what is implementable and provable here: an
interceptor in front of the serving path, with its coverage stated (it screens the platform's own
generation paths; it is not a claim about every possible route to text).

---

## 7 · The plan items

These extend the existing cognitive items rather than duplicating them. **P3.12** (the engine contract and
the six) and **P3.13** (the three meta engines) already carry the brief's Phase 1; **P3.14**–**P3.19**
carry the clearance chain, attestations, the auxiliary engines, the BME and the cycles.

| Item | What it delivers | Blocked by |
| :-- | :-- | :-- |
| **P3.20** | **The tier registry and the router.** Every AI resource declares its tier and what it can serve; the router chooses by domain and risk from the declared tiers and records why; each tier reports `runnable here` with the measured reason (RAM, no CUDA device, model absent). A tier nothing can serve says so instead of listing models. | §2 Owner decision on hardware |
| **P3.21** | **The verifier, and the withhold it can trigger.** Checkable checks only — citation resolves, quote exists at the cited location, figure appears in the cited source — each MET / UNMET / NOT ASSESSABLE with a basis; an UNMET check withholds the output and says which check failed. No confidence float anywhere in the path. | — |
| **P3.22** | **The owned knowledge index and its provenance.** Lexical + citation-graph index over the repo and (gated) the Owner's archives, sharing P2.13's bounds, secret-exclusion and three-state per file; every retrieved passage carries its document id and location; `embeddings: none installed` stated rather than implied. | P2.13, §7 gates |
| **P3.23** | **The domain specialists as executors, with their gates.** The first four the Owner named — law, GMP/science, career, QEP — each as a composition of retrieval + prompt + verifier, each with its human gate (legal filing: Owner approval; GMP: QA sign-off; QEP doctrinal content: scholar review; career: no invented achievement). | P3.21, P3.22 |
| **P3.24** | **Staged simulation, procedural first.** Stage 1 rules/arithmetic (a procedural timeline computed from published rules and the case's own dates — a schedule, not a forecast); stage 2 retrieval over real precedent; stage 3 a causal graph; stage 4 shadow-mode only, never on a surface. Each stage states which stage produced a figure, and no stage outputs a probability of a legal outcome. | §4 Owner decision on the predictor |

**The risk these items must not realise:** a fabric that reports a capability its hardware cannot serve, a
verifier that passes on a number it wrote itself, an index that claims to have read what it never read, or
a prediction about the Owner's own case presented as anything but arithmetic over published rules. Every
one of those is the class rounds W477–W495 removed from 132 surfaces of this platform.
