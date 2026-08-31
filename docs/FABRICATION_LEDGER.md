# Fabrication Ledger — 2026-08-31

Values a user or API consumer would reasonably read as **measured, derived or certified**, that
nothing measures, derives or certifies. Found by a five-area sweep with an adversarial defence
pass: **70 proposed, 11 successfully defended, 63 surviving**.

This ledger exists so the set is not lost between sessions. Items are fixed top-down by
REACHABILITY — what a user actually sees comes first. `reach` is quoted from the audit.

**Not in scope / already defended:** configuration constants, clearly-labelled fallbacks, test
fixtures, `_archive/**`, honest empty states, and prompt/example text.

## HIGH (25)

### `agentic_core/api/csuite.py:120`
- **status:** OPEN
- **claim:** GET /api/csuite/cto/infrastructure — docstring "Infrastructure metrics from psutil (real) + project activity (real)." — returns genuine `psutil` cpu/memory/disk values and, in the same flat dict, `"uptime": "99.9%"` and `"pqc_status": "Enforced"`.
- **why it is a fabrication:** Real measured neighbours are what make these dangerous: the payload is explicitly framed as real instrumentation, so a consumer reads 99.9% uptime as measured availability and "pqc_status: Enforced" as a verified post-quantum-crypto posture. No uptime is tracked anywhere and nothing checks or enforces PQC. This is the same shape as the confirmed wallet finding — a truthful frame carrying an untrue value.
- **reach:** live route (mounted app_mvp.py:60); not currently called by the SPA

### `agentic_core/api/economy.py:79`
- **status:** OPEN
- **claim:** `class CycleRequest(BaseModel): ... revenue: float = 10000.0` — the request-body default for POST /api/v1/economy/cycle. The caller VSBCockpit.tsx:243 posts `axios.post('/api/v1/economy/cycle', { vsb_id: selected })` with no revenue field, so every "Run cycle" press in the VSB Cockpit runs a full metabolic cycle on 10,000 WST of intake revenue that nothing earned.
- **why it is a fabrication:** The consumer sees the returned cycle report rendered in VSBCockpit.tsx:661 as `Intake revenue 10,000`, `Homeostasis reserves`, `Distributable profit`, `Giving back`, and then reads the refreshed `/api/v1/economy/ledger/{vsb_id}` panel showing `Total revenue` grown by 10,000 — a figure any user reads as this entity's earnings. Nothing derived it: it is a pydantic schema default. It is not ephemeral either — `EconomicMetabolism.run_cycle` calls `self.ledger.record("revenue", 10000, ...)` (agentic_core/economy/metabolism.py), which persists to the VSB's `_ledger.json`, and the invented 10,000 the
- **reach:** live route POST /api/v1/economy/cycle (router mounted at agentic_core/app_mvp.py:285) + UI-rendered in VSBCockpit.tsx ("Run cycle" button) + stored in the per-VSB virtual ledger, owner-payments ledger

### `agentic_core/api/v138/ceo.py:226`
- **status:** FIXED (W404)
- **claim:** `get_system_vitals()` returns `{"status": "OPTIMAL", "cpu_load": "12%", "memory_usage": "4.2GB", "latency": "18ms"}` — served directly by GET /api/v138/ceo/vitals (route at line 411), and injected into the AI CEO chat prompt as `Tool Output` whenever the user's message contains "vitals" (line 319-320), including in the offline fallback text at line 374-376.
- **why it is a fabrication:** These are measurements by every convention of their names — CPU load, memory in GB, latency in ms, and an OPTIMAL health verdict. Nothing measures them; psutil is never called on this path (csuite.py proves the real instrument was available). Worse, the chat path makes the AI CEO narrate the fabricated figures back to the user as its own observation of the running system.
- **reach:** live route + reaches the UI: apps/workstation-superapp/src/pages/CEOChat.tsx:46 posts to /api/v138/ceo/chat, and the "vitals" keyword injects this dict into the streamed answer

### `agentic_core/api/v310/business.py:119`
- **status:** OPEN
- **claim:** GET /api/v310/entrepreneur/mentors returns six invented people presented as a bookable mentor directory — e.g. {"id": "m-001", "name": "Dr. Aisha Sovereign", "expertise": "AI Governance & Compliance", "rating": 4.9, "available": True} — with ratings 4.6–4.9 and per-mentor availability flags.
- **why it is a fabrication:** A user would believe these are real mentors, that the ratings came from real reviews, and that `available: true` means they can be booked now. Nothing rates them, nothing tracks availability, and the people do not exist. Nothing in the payload marks it as sample or demo data.
- **reach:** live route (mounted app_mvp.py:89); not currently called by the SPA

### `agentic_core/api/v310/fund.py:14`
- **status:** OPEN
- **claim:** GET /api/v310/fund/grants/active returns two invented grant records: {"id": "g-001", "title": "Bio-Reactor Optimization", "recipient": "@NatureBuild", "amount": 5000, "status": "funded"} and a second at 2500 WST with status "voting".
- **why it is a fabrication:** An endpoint named `grants/active` returning a `funded` grant of 5,000 to a named recipient asserts that money was awarded. No grant store is read, no recipient exists, and the sibling endpoint on the same router (/epoch-synthesis) does call a real engine — so a consumer has every reason to treat this list as equally real.
- **reach:** live route (mounted app_mvp.py:121); not currently called by the SPA

### `agentic_core/api/v310/governance.py:20`
- **status:** OPEN
- **claim:** Module-level `PROPOSALS` literal seeds two DAO proposals with `"votes_for": 12400.0 / "votes_against": 1200.0` and `"votes_for": 45000.0 / "votes_against": 0.0`, proposed by "Scholar-DID-782" and "Guardian-Alpha". Served verbatim by GET /api/v310/governance/proposals and then incremented by POST /vote.
- **why it is a fabrication:** A consumer sees 45,000 votes cast in favour of a constitutional amendment by a named proposer. No vote was cast, no proposer exists, and no ledger recorded any of it — the tallies are literals. Because /vote adds real votes on top of the invented baseline, every genuine vote is thereafter reported inside a fabricated total.
- **reach:** live route (mounted app_mvp.py:113); the mount comment claims "called by DAODashboard" but no such page exists in apps/workstation-superapp

### `agentic_core/api/v310/governance.py:59`
- **status:** OPEN
- **claim:** GET /api/v310/governance/treasury — docstring "Real-time public treasury ledger view." — returns `"balance_wst": 1240500.0, "total_grants_distributed": 250000.0` plus two invented `recent_inflow` records ({"source": "Marketplace-Fees", "amount": 1420.5, "timestamp": "2026-01-01T12:00:00Z"}, {"source": "Sovereign-Bond-Issuance", "amount": 50000.0, ...}).
- **why it is a fabrication:** A consumer reads a "real-time public treasury ledger" and believes the platform holds 1,240,500 WST and has distributed 250,000 WST in grants, with two dated inflow transactions to back it. Nothing produces any of it — the function body is a literal dict with no reads of the capital fund, the token ledger, or any store. The fabricated inflows even carry timestamps, which is the shape that makes them read as records.
- **reach:** live route (mounted app_mvp.py:113); not currently called by the SPA

### `agentic_core/governance/adaptive_profiles.py:28`
- **status:** OPEN
- **claim:** IslamicFinanceAdapter.audit_trail() logs "Verifying Riba-free status and Zakat allocation" and returns {"type": "Shariah", "halal": True}; HealthcareHIPAAAdapter.audit_trail() (line 22) logs "Triggering PHI redaction" and returns {"sanitized": True}; FinancialServicesAdapter.audit_trail() (line 16) returns {"type": "SOX", "attestation": "ZkP_Hash"}; IndustryAdaptiveGovernance.apply_profile('finance') (line 50) returns {"compliance": "SOX", "riba_free": True}. The `data` argument is never read in any of them.
- **why it is a fabrication:** This is the SHARIA_AUDIT shape exactly: a machine-issued religious certification (halal: true, riba_free: true), a HIPAA sanitisation claim where no redaction ran, and the literal string "ZkP_Hash" presented as a zero-knowledge attestation. Executed live: IslamicFinanceAdapter().audit_trail({'product':'interest-bearing payday loan at 400% APR','riba':True}) -> {'type':'Shariah','halal':True}; HealthcareHIPAAAdapter().audit_trail({'patient_ssn':'123-45-6789','notes':'HIV positive'}) -> {'type':'HIPAA','sanitized':True} with the SSN untouched.
- **reach:** unreachable — no importer outside _archive/ and docs/

### `agentic_core/governance/industry_adaptive.py:24`
- **status:** OPEN
- **claim:** GovernanceVerifier.verify_action(): declares profiles healthcare={PHI_ENCRYPTION_MANDATORY, CONSENT_TRACEABILITY}, finance={SEC_COMPLIANT_LOGGING, KYC_VERIFIED_TRANSACTIONS}, then `# Simulated verification logic` / `logger.info(...)` / `return True`. No rule in self.profiles is ever compared against action_tags.
- **why it is a fabrication:** A consumer receives a governance verdict meaning "this action was checked against the HIPAA/SEC rule set and violates none". Nothing checks anything — the function is `return True` for every input. Executed live: verify_action('healthcare', ['EXPORT_PHI_PLAINTEXT','NO_CONSENT']) -> True. It is surfaced verbatim as {"compliant": true, "profile": ...} by the tool `verify_governance_compliance` in agentic_core/api/v138/ceo.py:209.
- **reach:** imported by a MOUNTED router (agentic_core/api/v138/ceo.py, mounted at /api/v138 in agentic_core/app_mvp.py:52) and registered in its ToolRegistry; no HTTP path dispatches that tool today, so live-rea

### `agentic_core/governance/trustworthiness_engine.py:21`
- **status:** OPEN
- **claim:** analyze_fairness() sets `fairness_score = 1.0` (or the literal `0.95` when any demographic_data dict is passed) and returns {"fairness_score", "is_fair", "status": "COMPLIANT"}; detect_bias() sets `bias_score = 0.05` (line 43) -> "NO_BIAS"; generate_explainability_report() returns `"transparency_score": 0.95, "interpretability": "HIGH"` (line 61) regardless of the reasoning_chain. Both scoring bodies are commented `# Placeholder`. The `output` argument is never read.
- **why it is a fabrication:** Class docstring: "ARTICLE 100: Bias detection, fairness metrics, explainability scoring". A consumer would believe a fairness/bias analysis of the supplied output produced these numbers and the COMPLIANT verdict. Nothing analyses the output. Executed live: analyze_fairness('Only hire men. Reject all women applicants.', {'gender':{'m':100,'f':0}}) -> {'fairness_score': 0.95, 'is_fair': True, 'status': 'COMPLIANT'}; detect_bias('Women are worse engineers than men.') -> {'bias_score': 0.05, 'status': 'NO_BIAS'}. get_system_trust_index() (line 81) likewise returns 1.0 when no trust score was ever 
- **reach:** unreachable — no importer outside _archive/ and docs/

### `agentic_core/reactor/religion/qep_flagship.py:213`
- **status:** FIXED (W403)
- **claim:** certifications(user_id, course_id) builds `{"id": "CERT-...", "user_id", "course", "issued_at", "valid_until": "PERPETUAL"}`, signs it with `pqc_service.sign_dilithium5(...)`, appends it to the on-disk certificate store, and returns `{"status": "ISSUED", "pqc_signature": ..., "verify_url": f"/verify/{cert_id}"}`.
- **why it is a fabrication:** Neither argument is checked against anything — no progress record, no course roster, no completion test. The function is a pure issuance path. Because it then applies a REAL post-quantum signature and hands back a verify_url, the artifact is cryptographically attestable while attesting a completion nothing established — the exact shape of meta/SHARIA_AUDIT_v100.0.json's machine-invented signature, but persisted and per-user.
- **reach:** stored (writes DATA_DIR/qep_production.json certificates[]) — no live route; registered as tool "qep_certifications", called at ceo.py:140

### `agentic_core/reactor/religion/qep_flagship.py:64`
- **status:** FIXED (W403)
- **claim:** tajwid_coach(audio_blob, reference) never reads audio_blob. It returns `score = 0.98 + (random.random() * 0.015)` rounded to 4dp, plus `"rules_verified": ["Madd Jaa'iz", "Ikhfa'", "Ghunnah", "Qalqalah"]` and `"human_fallback": score < 0.92` (unreachable — the floor is 0.98).
- **why it is a fabrication:** A user receives a numeric assessment of their Qur'anic recitation and a list of tajwid rules marked verified, for audio that was never analysed — the caller in ceo.py:108 does not even pass audio, it passes b"". The random floor of 0.98 also makes the "human_fallback" escape hatch structurally dead, so a genuinely poor recitation can never be routed to a human. This is a religious-practice competency judgement invented by random.random().
- **reach:** no live route — registered as tool "qep_tajwid_coach" (ceo.py:57 region, called at ceo.py:108) but ToolRegistry.call_tool is never invoked with that name from any route

### `agentic_core/reactor/religion/quranic_studies.py:156`
- **status:** OPEN
- **claim:** _handle_compare_tafsir returns `comparisons: [{"tafsir": "Ibn Kathir", "content": f"Historical and narrative analysis for verse {reference}."}, {"tafsir": "Al-Jalalayn", "content": f"Brief linguistic and semantic commentary for verse {reference}."}]` with a `semantic_diff` naming shared_themes ["Divine Oneness", "Guidance"] and per-scholar "unique_insights", under status SUCCESS. _handle_compare_qiraat (line 192) likewise returns Hafs/Warsh variations attributed to "Mishary Rashid Alafasy" and "Khalil Al-Husary" with audio fields "url_hafs"/"url_warsh".
- **why it is a fabrication:** Scholarly commentary is attributed by name to two real classical tafsir works and two real reciters, for any verse, from f-strings that only interpolate the verse reference. No source is consulted (the class holds a working AlQuranCloudConnector and does not call it here). The docstring calls it "Functional multi-source retrieval simulation" but the payload the caller receives says SUCCESS and carries no marker. The qira'at entry is additionally wrong on its face — Al-Husary is a Hafs reciter, not Warsh.
- **reach:** no live route — reached via QuranicStudiesReactor.incubate(task="compare_tafsir"/"compare_qiraat"); the reactor is instantiated by the shipped products/qep-sdk and by reactor/ecosystem/factory.py, but

### `agentic_core/reactor/religion/quranic_studies.py:176`
- **status:** OPEN
- **claim:** _handle_generate_quiz(reference) ignores `reference` and returns one fixed question — {"question": "What is the primary theme of this verse?", "options": ["Tawhid", "Charity", "Patience", "Prayer"], "answer": "Tawhid"} — with `"confidence_score": 0.98`.
- **why it is a fabrication:** Sold as "AI-Generated Quizzes" and gated behind the Pro tier by products/qep-sdk/qep_sdk.py:36 (which raises PermissionError for Free users before calling it). The learner is told the answer to any verse is Tawhid, and the 0.98 confidence_score is a literal attached to a question no model generated and no grader scored.
- **reach:** shipped product surface — products/qep-sdk/qep_sdk.py:42 QEPClient.generate_quiz (Pro tier); the qep-sdk product is advertised in the catalog at route /qep-religion (agentic_core/catalog/api.py:19)

### `agentic_core/synthesis/api.py:256`
- **status:** OPEN
- **claim:** After a live model result is parsed: `if "sim_results" not in model ...: model["sim_results"] = fallback["sim_results"]` and `if "projections" not in model: model["projections"] = {"year_1": 4.5e7, "year_3": 2.1e8, "year_5": 8.4e8}`.
- **why it is a fabrication:** Hardcoded five-year revenue projections and engine "simulation results" are welded onto an otherwise-genuine output whenever the model omits those keys. The merged object is indistinguishable from a computed one — same JSON, same shape, no provenance flag, no note. BusinessModelDashboard.tsx:8-10 charts data.projections.year_1/3/5 directly, so the user sees a revenue curve that is three literals from source code.
- **reach:** live route — POST /api/v1/synthesis/generate with output_type="simulation"; charted in BusinessModelDashboard.tsx (SynthesisStudio.tsx:518)

### `agentic_core/synthesis/business_model.py:9`
- **status:** OPEN
- **claim:** BusinessModelSimulator.generate_model() ignores its `data` argument and returns `sim_results` keyed by engine name: aro_efficiency.resource_optimization_gain 0.28 (comment: "# 28% gain via SciPy"), bto_roadmap.implementation_speed_multiplier 2.4 ("# 2.4x faster via AI Swarms"), bto_roadmap.milestone_confidence 0.94, drad_resilience.compliance_score 0.99, drad_resilience.adaptation_latency_ms 142, plus ese_adoption revenue/market_share per segment.
- **why it is a fabrication:** The class is named Simulator, the key is `sim_results`, and each block is labelled with a real engine (ESE/ARO/BTO/DRAD) — an API consumer reasonably believes these engines ran. No engine is invoked, SciPy is never imported, and the ingested `data` string is discarded. A 0.99 "compliance_score" in particular is a compliance pass nothing screened.
- **reach:** live route — the fallback path of POST /api/v1/synthesis/generate (output_type="simulation"), agentic_core/synthesis/api.py:249 and :254

### `agentic_core/synthesis/presentation.py:8`
- **status:** OPEN
- **claim:** generate_presentation(topic) ignores `topic` except in slide 1's title and returns a fixed 10-slide deck: "Wu et al. 2025: Integration risks higher than estimated", "Chazarin et al. 2026: Longitudinal tracking required", "Gifford et al. 2025: Identifying regulatory lag in mRNA stability", "$4.2B market projected by 2030", "30% reduction in clinical trial attrition for early adopters".
- **why it is a fabrication:** Three invented academic citations with author names and years, a market size, and an ROI figure — presented to the user as the researched content of the presentation they asked for. Nothing researched, retrieved or computed any of it. agentic_core/synthesis/api.py:140 serves this verbatim as the deliverable whenever `_extract_json_array(raw)` returns None (the gateway's native structured-engine floor returns prose, not a JSON array, so this fires on any deployment without a live JSON-capable model), and labels it `metadata.title = "Presentation: {topic}"` with no fallback marker. A user who as
- **reach:** live route — POST /api/v1/synthesis/generate (mounted /api/v1 in app_mvp.py:64); rendered by SynthesisStudio.tsx:489 and downloadable via /api/v1/synthesis/download/{id}

### `apps/workstation-superapp/src/components/LearnTeachModule.tsx:12`
- **status:** FIXED (W403b)
- **claim:** `await fetch('/api/v1/education/curriculum', {...})` with no `res.ok` check, followed unconditionally by `toast('Class report generated — 12-week curriculum plan ready for 42 students')`. The response body is never read or displayed.
- **why it is a fabrication:** A 4xx or 5xx response still reports 'Class report generated'. The catch only fires on a network-level failure, so any HTTP error produces a success message for a report that was never produced and is never shown to the user. The '42 students' in the message is the hardcoded literal, not a count from the response.
- **reach:** live route — /religion, 'Generate Class Report' button

### `apps/workstation-superapp/src/components/LearnTeachModule.tsx:88`
- **status:** FIXED (W403b)
- **claim:** `{['Sheikh Al-Ghauri', 'Dr. Fatima Zahra', 'Ustadh Ibrahim'].map(scholar => ...)}` each rendered under the caption `Verified Scholar` (line 93), inside a card headed 'Scholar Governance Board'. Alongside: `Total Students` `42` (line 69) and `Avg. Mastery` `88%` (line 73).
- **why it is a fabrication:** Three named individuals are presented to users as verified scholars sitting on a governance board. No verification process exists, no roster is fetched, and the names are string literals — this asserts religious credentials for named people that nobody certified, the same class as the invented SHARIA_AUDIT signature. The adjacent 'Total Students 42' and 'Avg. Mastery 88%' are equally hardcoded (42 again) and read as this educator's real class analytics under a heading 'Class Management & Analytics'.
- **reach:** live route — ReligionHub.tsx:106 renders <LearnTeachModule /> inside /religion (App.tsx:175)

### `apps/workstation-superapp/src/pages/cognitive/Introspection.tsx:16`
- **status:** OPEN
- **claim:** `const SEED: Biometrics = { immune: { health: 0.98, ... }, metabolic: { efficiency: 0.92, atp_ratio: 0.88, ... }, cardiovascular: { resource_flow: 75, ... } }` is the initial state; the fetch uses `validateStatus: () => true` and `.catch(() => {})`, so a non-200 or a failed request silently leaves SEED on screen (rendered at line 78 as 'System Health 98.00%' and lines 88-90 as ATP/Cardiovascular/Immune bars).
- **why it is a fabrication:** When the backend is down or the endpoint errors, the page shows 'System Health 98.00%' in 6xl type under a header asserting 'Real-time introspection', with animated bars at 92% and 88%. Nothing distinguishes this from a live reading — there is no error state, no 'not measured' label, and the failure is swallowed twice over. This is the 'failed fetch leaves a plausible-looking value on screen instead of an error' case. Compare DashboardNew.tsx:100, which handles the identical situation honestly via `setBackendDown(true)`.
- **reach:** live route — /cognitive-introspection; visible whenever the backend is unreachable

### `apps/workstation-superapp/src/pages/cognitive/Introspection.tsx:42`
- **status:** OPEN
- **claim:** `oxytocin: bio.communication.neurotransmitter === 'Oxytocin' ? 0.85 : 0.5`, `serotonin: ... ? 0.88 : 0.55`, `dopamine: ... ? 0.82 : 0.6` — rendered by `ResonanceBall` at lines 64-66 as e.g. 'Oxytocin Resonance 85.0%' with an animated fill bar, under a header reading 'Real-time introspection of the Workstation's biochemical resonance'.
- **why it is a fabrication:** The backend (agentic_core/app_mvp.py:376) genuinely computes biometrics from psutil, the immune system and an ATP simulator — but it returns only a neurotransmitter *name* ('Oxytocin' | 'Serotonin' | 'Dopamine', chosen from websocket/project counts). It never returns a magnitude. The frontend invents three percentages from a string equality test and renders them as measured resonance levels with one-decimal precision. Nothing measures oxytocin, serotonin or dopamine — this is the confirmed `avg_oxytocin 0.992` fabrication reproduced in the UI.
- **reach:** live route — App.tsx:245 /cognitive-introspection; also linked from CommandPalette.tsx:66 and SearchMeshModal.tsx:40

### `apps/workstation-superapp/src/pages/domains/QEPReligionHub.tsx:47`
- **status:** FIXED (W403)
- **claim:** TajwidCoach `startRecitation()` sets `setTimeout(..., 3000)` then `setResult({ score: 94.2, violations: [{ rule: 'Ikhfa', msg: 'Noon Sakina here requires light ghunnah.' }, { rule: 'Qalqalah', msg: 'The letter Ba requires clear echo.' }] })`. Rendered at line 91 as `Accuracy Score {result.score}%` and at lines 105-113 under a heading `Real-time Coaching`.
- **why it is a fabrication:** A user presses the mic button, sees 'Analyzing Phonetic Stream...' for 3 seconds, and is told their Qur'anic recitation scored 94.2% with two specific tajwid rule violations in their own recitation. No microphone is ever opened (no getUserMedia), no audio is captured, no backend is called. The score and both violations are literals in the source. This is a fabricated religious-performance assessment attributed to the user — the same shape as the confirmed `quiz_accuracy 98.2%` fabrication. The rest of this file was cleaned in an earlier pass (MemorizationSuite's SM-2 button now checks `r.ok`, 
- **reach:** live route — App.tsx:181-182 maps both /qep and /qep-religion to QEPReligionHub; App.tsx:35 calls this 'the genuine Qur'an Education Platform'

### `apps/workstation-superapp/src/pages/enterprise/CapitalDashboard.tsx:53`
- **status:** FIXED (W405)
- **claim:** `balance: s.total_projects * 1000 + s.total_outputs * 250`, `unrealisedProfit: s.by_stage.prototype * 500 + s.by_stage.concept * 100`, `realisedProfit: s.complete * 2500`, `riskScore: Math.min(0.99, 0.6 + s.complete / Math.max(s.total_projects, 1) * 0.39)` — rendered as `Portfolio Value ${metrics?.balance.toLocaleString()}`, `Unrealised Gain $...` and `Risk Score {(metrics.riskScore * 100).toFixed(0)}%` (lines 168-180).
- **why it is a fabrication:** Project counts are multiplied by invented dollar constants and displayed as currency on a page titled 'Sovereign Capital'. A user reading 'Portfolio Value $47,250' and 'Unrealised Gain $3,100' would believe money was measured; what actually produced it is a project tally times 1000. 'Risk Score 78%' is presented as a risk measurement but is a project-completion ratio floored at 0.6 and capped at 0.99 — no risk model exists. The only acknowledgement is a source comment ('Map project counts to capital-metaphor metrics'); nothing in the rendered UI tells the user these are metaphors, and they sit
- **reach:** live route — /economy?tab=capital, 'Overview' tab (default)

### `apps/workstation-superapp/src/pages/enterprise/CapitalDashboard.tsx:70`
- **status:** FIXED (W405)
- **claim:** `setFeeds([{ symbol: 'BTC/USD', price: 65420, change: 2.4 }, { symbol: 'ETH/USD', price: 3512, change: 1.8 }, { symbol: 'SPY', price: 520.4, change: 0.5 }, { symbol: 'AAPL', price: 190.2, change: -0.2 }])` — rendered under `<h3>Real-Time Market Feeds</h3>` (line 193) with a per-row source label `ALPHA VANTAGE SOURCE` (line 205).
- **why it is a fabrication:** A user sees four instrument prices with percentage moves under a 'Real-Time' heading, each row attributed to Alpha Vantage, a real named market-data vendor. Nothing fetches Alpha Vantage anywhere in the frontend; the four literals are set unconditionally in the mount effect and never change. This is a real-looking number with a false third-party attribution — the `payments/wallet` shape, applied to financial market data.
- **reach:** live route — /economy?tab=capital (App.tsx:216 EconomyCenter, EconomyCenter.tsx:13 registers CapitalDashboard; /capital redirects here at App.tsx:194), 'External Markets' tab

### `apps/workstation-superapp/src/pages/synthesis/BusinessModelDashboard.tsx:16`
- **status:** OPEN
- **claim:** `<StatCard label="Market Size" value="$4.2B" />`, `<StatCard label="ROI Efficiency" value="+28%" />`, `<StatCard label="Swarm Multiplier" value="2.4x" />`, `<StatCard label="GaaS Alignment" value="0.99" />`; plus `<SimParam ... detail="15% Market Share" />`, `detail="28% Gain"`, `detail="2.4x Multiplier"` (lines 74-76) and an 'Adoption Velocity: High' bar fixed at `w-3/4` (line 61).
- **why it is a fabrication:** These four stat cards sit in the same panel as, and directly above, a chart driven by genuine per-run data (`data.projections.year_1/3/5`). A user viewing the output of *their* simulation reads '$4.2B market size' and 'GaaS Alignment 0.99' as findings derived from that simulation. Nothing computes them — they are literals identical for every simulation ever run, and the component ignores `data` entirely except for the three projection values.
- **reach:** live route — SynthesisStudio.tsx:518 renders it for any result with outputType === 'simulation', at /synthesis (App.tsx:199)

## MEDIUM (31)

### `agentic_core/ai/ceo/autonomy_pipelines.py:49`
- **status:** OPEN
- **claim:** run_retrospection() returns a post-mortem whose `"root_cause_analysis"` is the fixed string "Lattice-based signature derivation exceeded latency thresholds in standalone mode." with fixed `proposed_fixes` and a generated `automated_ticket_id` — identical for every incident_log passed in. When called with no argument it first MANUFACTURES the incident (line 40: `[{"status": "FAILED", "reason": "PQC Handshake Timeout", ...}]`). run_extrospection() (line 59) invents its own `external_data` ("Global PQC Adoption", "Interfaith AI Ethics Consensus v2") and reports `external_signals_analyzed: 2`. log
- **why it is a fabrication:** A root-cause analysis is a derived finding; a consumer reading post_mortem_PM-*.json believes an incident was analysed and a cause identified. Nothing analyses the log — the string is a constant, and with no log supplied the incident itself never happened. The introspection entries assert constitutional alignment against two named articles that nothing evaluated, and the roadmap carries a "Verified by CGO" attestation no CGO produced. These are persisted via _save_to_file into LOG_DIR/autonomy, so they outlive the call.
- **reach:** imported by the mounted /api/v138/ceo router; only generate_v10_roadmap() is wired (registered tool, not currently HTTP-routed); outputs are written to disk under LOG_DIR/autonomy when called

### `agentic_core/api/csuite.py:84`
- **status:** OPEN
- **claim:** GET /api/csuite/cfo/metrics — docstring at line 58-60 states "All values are calculated from real data — no hardcoded literals." The body then builds revenue and ROI from invented multipliers: stage_values {concept: 1_000, prototype: 5_000, commercialise: 15_000} (line 66), $250 per deliverable (line 71), $120 per project (line 74), $2,500 per completed project (line 78), and `"growth": f"+{min(s['total'] * 4.2, 99.9):.1f}%"` (line 84).
- **why it is a fabrication:** The docstring's denial is the tell — every one of these is a hardcoded literal. `growth` is the worst: a percentage growth rate computed as project-count × 4.2, capped at 99.9%, with no time series behind it at all. The response ships `revenue`, `liquidity`, `operating_costs`, `realised_gain` and an ROI percentage as financial metrics, with nothing in the payload disclosing that the prices are invented.
- **reach:** live route (mounted app_mvp.py:60); not currently called by the SPA

### `agentic_core/api/frontier.py:134`
- **status:** OPEN
- **claim:** GET /api/v1/frontier/reality/status — docstring "Reality coherence dashboard metrics." — returns `"coherence": 0.987` and `"reality_anchor": "stable"` as literals, alongside `total_grants` and `capital_allocated` which ARE computed from the real grant store.
- **why it is a fabrication:** Same real-neighbour pattern as the csuite finding: two genuinely computed fields make the two literals read as measured. A dashboard renders 98.7% coherence and a "stable" anchor verdict; nothing computes or checks either.
- **reach:** live route (mounted app_mvp.py:257)

### `agentic_core/api/frontier.py:97`
- **status:** OPEN
- **claim:** POST /api/v1/frontier/cosmic/response-protocol returns `"latency_ms": round(req.intensity * 12, 1)` — the reported latency is the caller's own `intensity` request parameter multiplied by 12.
- **why it is a fabrication:** `latency_ms` names a measured elapsed time. No clock is read on this path (`time` is imported and used elsewhere in the file). Sending intensity 0.7 yields "8.4ms"; sending 0.9 yields "10.8ms" — the consumer is shown their own input knob dressed as a performance measurement.
- **reach:** live route (mounted app_mvp.py:257)

### `agentic_core/api/qep_intelligence.py:197`
- **status:** OPEN
- **claim:** POST /api/v1/qep/adaptation/execute stamps `"fidelity": 0.9` onto every adaptation it writes to the registry. The prompt at line 180-184 explicitly asks the AI for "## Expected Fidelity (0-1)", but the reply is stored only as free text in `blueprint` — the number is never parsed, and the literal 0.9 is persisted instead. The seed set `_DEFAULT_ADAPTATIONS` (lines 45-49) does the same with 0.94 and 0.89.
- **why it is a fabrication:** `fidelity` is served as a per-adaptation quality measurement by GET /adaptation/registry and persisted to the qep_intel store, so it survives as data. Nothing derives it — least of all the model output that was solicited for exactly that purpose and then discarded.
- **reach:** live route (mounted app_mvp.py:261) + written to the persistent adaptation_registry.json store

### `agentic_core/api/qep_intelligence.py:213`
- **status:** OPEN
- **claim:** GET /api/v1/qep/compliance/audit returns `"compliant": True` unconditionally, with two checks hardcoded to pass — {"control": "Explainability (XAI) available", "status": "pass"} and {"control": "Translation tajweed-preservation", "status": "pass"} — and a third, "Adaptation fidelity ≥ 0.85", evaluated against the invented 0.9/0.94/0.89 values from the same module.
- **why it is a fabrication:** This is a compliance verdict with an `audited_at` timestamp and an `adaptations_audited` count, so a consumer reads it as the output of an audit. Two of the four controls assert `pass` without testing anything, the fidelity control can only ever pass because the numbers it grades are constants chosen above the threshold, and the top-level `compliant: True` is a literal that no branch can change.
- **reach:** live route (mounted app_mvp.py:261)

### `agentic_core/api/v138/ceo.py:222`
- **status:** FIXED (W404)
- **claim:** `call_meeting(agenda)` loops six C-Suite roles and writes a fabricated position for each into the REAL meeting record: `meeting_log.post_argument(agent, f"Synthesized position on {agenda} from {agent} perspective.", "APPROVE")` — every officer, always stance APPROVE — then returns {"status": "MEETING_COMPLETE", "log_updated": True}.
- **why it is a fabrication:** No officer deliberated and no position was formed; the "argument" is a template string containing only the agenda echoed back. Those rows are then served as genuine governance record by GET /api/v138/ceo/meeting/log and rendered as a markdown minutes document by GET /api/v138/ceo/meeting/minutes, and re-injected into later chat turns as "Recent C-Suite Debate". MeetingLog itself was already fixed to be honest (agentic_core/ai/ceo/memory_v01.py) — this endpoint is what feeds it invented content, including a unanimous APPROVE that no one voted.
- **reach:** live route + UI: triggered from CEOChat.tsx whenever the user's message contains "meeting" or "debate" (v138/ceo.py:321-322); persists into the served meeting log and minutes

### `agentic_core/api/v200/contribute.py:11`
- **status:** OPEN
- **claim:** POST /api/v200/contribute/feedback returns `{"status": "ingested", "resonance": 0.99}` for any body. Line 13: POST /api/v200/contribute/vote returns `{"status": "recorded", "proposal": proposal_id}` while the function body does nothing at all — no store, no list append, not even the module's in-memory FEEDBACK.
- **why it is a fabrication:** `resonance: 0.99` is a per-submission quality score that nothing scores. The vote endpoint is the sharper problem: it reports a vote as `recorded` when the vote is discarded on return — a user who votes gets a success response for an action that never happened.
- **reach:** live route (mounted app_mvp.py:133)

### `agentic_core/api/v250/treaties.py:23`
- **status:** OPEN
- **claim:** GET /api/v250/treaties/active returns two invented treaties, one with `"status": "enforced"` between nodes "Alpha" and "Beta". Separately, POST /api/v250/treaties/{treaty_id}/sign (line 28) returns `{"status": "signed", ...}` without touching the `DRAFTS` list or appending to any `signatures` array.
- **why it is a fabrication:** Two distinct fabrications. The listing asserts a treaty is being enforced when no treaty, node, or enforcement mechanism exists. The sign endpoint reports a completed signature while the module's own draft store is left untouched — a fabricated success, so a caller who drafts a treaty, signs it, then lists drafts will find it unsigned.
- **reach:** live route (mounted app_mvp.py:105); the mount comment names a "Treaty Studio" frontend that does not call it

### `agentic_core/api/v260/intelligence.py:9`
- **status:** OPEN
- **claim:** GET /api/civilization/recommendations takes `user_id` and ignores it entirely, returning three fixed items with invented relevance scores: resonance 0.95 ("Vote on AMD-146"), 0.88 ("New Marketplace Product: Neural Filter"), 0.92 ("Reinforce Empathy Trait"). Line 20: POST /api/civilization/assistant/query stamps `"confidence": 0.99` on whatever the AI gateway returns.
- **why it is a fabrication:** A per-user recommendations endpoint that discards user_id but reports personal `resonance` scores tells the consumer these were computed against that user — the same false-attribution shape as the wallet finding. The referenced proposal AMD-146 and product "Neural Filter" do not exist. And 0.99 confidence is attached to every AI answer without any confidence estimate being made.
- **reach:** live route (mounted app_mvp.py:109); not currently called by the SPA

### `agentic_core/api/v290/ceo_generate.py:226`
- **status:** OPEN
- **claim:** POST /api/v290/ceo/debug-creation returns `"fidelity_score": 0.95` beside the real AI analysis text, on every call regardless of the blueprint submitted or what the model said.
- **why it is a fabrication:** A `fidelity_score` next to an AI review reads as a scored assessment of that review. Nothing scores it; the gateway response is not inspected, and the value cannot vary.
- **reach:** live route (mounted app_mvp.py:56)

### `agentic_core/commercial/marketplace.py:38`
- **status:** OPEN
- **claim:** `process_external_transaction(listing_id, amount_wst)` returns `{"transaction_id": tx_id, "status": "COMPLETED", "amount": amount_wst, "distribution": {...40/30/20/10 split...}, "receipt_url": f"https://api.jules-ai.com/receipts/{tx_id}"}` under the docstring "v128.0: Live marketplace billing and revenue distribution logic."
- **why it is a fabrication:** A consumer reads a settled billing transaction with a retrievable receipt. Nothing settles: the method touches no ledger, no store, and no external billing API — it computes four percentages of its own argument, logs, and returns. `status: "COMPLETED"` is asserted by a string literal, and `receipt_url` points at `api.jules-ai.com`, a host this codebase never calls and does not own (it is a leftover from the prior Jules build). The `distribution` dict presents a four-way allocation of funds (liability fund / scholar rewards / operational costs / charity) that no account ever receives. Contrast 
- **reach:** unreachable in practice — no route calls it, and the only live caller (agentic_core/synthesis/grand_synthesis_engine.py:277) constructs `MarketplaceIntegrator()`, whose `__init__` does `from .marketpl

### `agentic_core/commercial/partnership_framework.py:47`
- **status:** OPEN
- **claim:** `issue_verifiable_credential()` mints `{"id": f"VC_PARTNER_{partner_id}", "issuer": "Virtual Sovereign Business", "subject": ..., "tier": ..., "issued_at": ..., "expires_at": now+365d, "signature": hashlib.sha256(f"VSB_SIGN_{partner_id}".encode()).hexdigest()}` — line 64 carries the author's own comment `# Mock signature` — then sets `partner["status"] = PartnershipStatus.CERTIFIED.value` and appends it to `self.certification_registry`.
- **why it is a fabrication:** This is the SHARIA_AUDIT shape: a machine-invented certification with an invented cryptographic signature. A consumer of the credential (or of `get_public_registry()`, which publishes `entity`, `tier`, `status: CERTIFIED`, `certified_since`) reasonably believes an issuer certified this partner and signed the attestation. The "signature" is a SHA-256 of a fixed literal template plus the partner id — it verifies nothing, is trivially reproducible by anyone who knows the id, and no key material is involved (compare agentic_core/commercial/token_ledger.py, which does real Ed25519 signing and expos
- **reach:** stored/registry-shaped but not currently reachable over HTTP — agentic_core/api/partnerships.py IS mounted (app_mvp.py:167, prefix /api/partnerships) and exposes GET /registry, POST /onboard and GET /

### `agentic_core/governance/app_compliance.py:19`
- **status:** OPEN
- **claim:** AppCompliance declares `self.rules = ["no_hardcoded_secrets", "privacy_safe", "sih_aligned"]` (line 12) and verify_app() is documented as "security and constitutional audits on user-generated code", but the entire audit is `if "API_KEY =" in source_code`. It then returns {"status": "passed"/"failed", "violations": [...], "report_id": f"REP-{app_id}"}.
- **why it is a fabrication:** A "passed" verdict with a report id reads as a completed three-rule security + constitutional audit. Two of the three declared rules (privacy_safe, sih_aligned) are never evaluated, and the third is a single literal substring. Executed live: verify_app('app1', 'import os; os.system("rm -rf /"); token="sk-live-abc"') -> {'status': 'passed', 'violations': []}.
- **reach:** unreachable — no importer outside _archive/

### `agentic_core/governance/gaas/v5/hallucination_sandbox.py:46`
- **status:** OPEN
- **claim:** regenerate_with_citations() returns `f"{output}\n\n[VERIFIED: JULES v∞ Registry]"` — it appends a verification stamp and adds no citations. validate_output() (line 21) starts `score = 1.0` and can only decrement it against a 3-entry hardcoded knowledge_base ({"v-infinity", "mjm-v5", "gaas-v4"}), so any ordinary text returns `{"passed": True, "fidelity_score": 1.0}`, which is then written to the UEG as event "hallucination_scan_completed".
- **why it is a fabrication:** The class is the "Validation Sandbox ... Prevents unverified or hallucinated claims from entering the UEG". A reader of the returned string sees "[VERIFIED: JULES v∞ Registry]" and believes the content was checked against a registry; no registry is consulted and the method name promises citations that are never added. A fidelity_score of 1.0 sealed into the tamper-evident ledger asserts a measured hallucination check that, for any text not mentioning those three literal keys, consisted of nothing.
- **reach:** reached only through agentic_core/governance/uci_interceptor.py:37/step 6, which is imported by agentic_core/avatars/core/recirculation_orchestrator.py but never instantiated on a live route — unreach

### `agentic_core/governance/multisig_council.py:41`
- **status:** OPEN
- **claim:** request_approval() logs "PENDING_APPROVAL" to the UEG naming members ["RepoOwner", "ConsciousEntity", "ChiefEthicsOfficer"], then calls auto_evaluate_simulated(), which casts the quorum itself: `await self.approve(proposal_id, "RepoOwner")` and `await self.approve(proposal_id, "ChiefEthicsOfficer")`, flipping status to "APPROVED" and returning True.
- **why it is a fabrication:** A caller (and the UEG record) sees a high-risk change approved by a named two-of-three human quorum including the repo owner and the Chief Ethics Officer. No human was asked. The stored proposal object is indistinguishable from a genuinely voted one — `approvals: ['RepoOwner','ChiefEthicsOfficer']`, `status: 'APPROVED'`. The class docstring says "Simulated", but the artifact it produces carries no such marker.
- **reach:** imported only by products/capital_fund/immune/capital_immune.py (Regulator/Reconfigulator chain), which nothing imports — unreachable

### `agentic_core/reactor/api_client.py:74`
- **status:** OPEN
- **claim:** _get_domain_mock is returned on live-API failure with no marker distinguishing it from a real response: religion → {"hadith": {"text": "Authentic Hadith retrieved via Sunnah.com API", "grade": "Sahih"}}; science → {"id": f"arXiv:2505.{random.randint(1000,9999)}", "title": f"Live Research on {q}"}; law → CourtListener case with random id; employment → {"salary_range": "80k-120k", "source": "Adzuna"}; education → a Common Core standard id "retrieved via Common Core API".
- **why it is a fabrication:** Every branch fabricates a third-party-sourced record and stamps the third party's name on it. A grade of "Sahih" is an authenticity certification for a hadith that does not exist, credited to Sunnah.com — which this class never contacts (its religion mapping points at alquran.cloud). The arXiv ID and CourtListener case number are citations to nothing, and the response is cached into self.cache so the fabrication persists for the process lifetime. Only the server log says "Falling back to simulation"; the consumer sees the real-response shape.
- **reach:** unreachable — LiveAPIClient's only non-archived importer is agentic_core/reactor/religion.py (ReligionReactor), which itself has no non-archived caller

### `agentic_core/reactor/ecosystem/factory.py:56`
- **status:** OPEN
- **claim:** The dynamically-created class shared by all 50+ registered sub-reactors returns `simulation_fidelity: 0.98 + random.random()*0.015` and `result: f"Simulated {sub_domain} outcome ... based on domain heuristics"` from incubate; `fidelity: 0.99` and `domain_score: random.uniform(0.9, 1.0)` from analyze; `{"is_truth": True, "confidence": 0.995, "method": "PatternConsistencyCheck"}` from validate_truth; and `{"url": f"https://workstation.ai/reports/{domain}/{uuid.uuid4()[:8]}"}` from generate_artifact. The same unconditional `is_truth: True` appears in quranic_studies.py:232 (confidence 1.0, "sourc
- **why it is a fabrication:** validate_truth is the platform's truth-validation hook (SpecializedReactor declares it abstract, "Domain-specific truth validation") and it returns True at 0.995–1.0 confidence for every input including content it never inspects — a verification stamp with no verifier, named with a plausible method ("PatternConsistencyCheck") that does not exist. generate_artifact returns a URL for a report that is never produced on a domain the platform does not own (and `uuid.uuid4()[:8]` would raise TypeError if it were ever called, proving nothing exercises it).
- **reach:** unreachable — no agentic_core/api module imports agentic_core.reactor's ecosystem; initialize_reactor_ecosystem() has no non-archived caller

### `agentic_core/reactor/religion/qep_flagship.py:118`
- **status:** OPEN
- **claim:** memorization_suite returns, alongside genuinely-computed SM-2 fields, `"heatmap": [random.randint(0, 5) for _ in range(30)]` with the inline comment `# Last 30 days activity`.
- **why it is a fabrication:** Everything else in this function is real (the SM-2 interval/easiness-factor maths is correct and persisted per user), which is precisely what makes the heatmap dangerous: it rides in the same honest payload and is labelled as the user's own last-30-days study activity. It is 30 random integers, regenerated differently on every call.
- **reach:** no live route — registered as tool "qep_memorization", called at ceo.py:112; the surrounding function does persist real state to DATA_DIR/qep_production.json

### `agentic_core/reactor/religion/qep_flagship.py:196`
- **status:** OPEN
- **claim:** analytics_reports(user_id) ignores user_id and returns fixed `growth_data` [Mon 85, Tue 88, Wed 87, Thu 92], `mastery_breakdown` {fluency 0.95, accuracy 0.88, consistency 0.98} and `retrospect_summary`: "Strongest improvement in Ikhfa rules this week." Sibling learn_teach_module (line 160) returns Teacher-role figures students 45, active_sessions 3, avg_progress 0.68, retention_rate 0.94; gamified_competition (line 128) returns a leaderboard of "User-{i}" with random scores 80–100 and `user_rank: random.randint(1, 50)`; swarm_intelligence_learning (line 264) returns active_swarms 8 and synergy
- **why it is a fabrication:** These are the user's own performance analytics, their teaching cohort's retention rate, their competitive rank and their study circle's synergy — every one a literal or a random draw, with the user_id argument discarded. Same class as GET /payments/wallet/{user_id} returning the platform fund for every user: a plausible number under a false personal attribution. The "retrospect_summary" sentence additionally names a specific tajwid rule as the user's strongest improvement.
- **reach:** no live route — registered tools qep_analytics / qep_learn_teach / qep_competitions / qep_swarm_learning (ceo.py:136, :124, :116, :156)

### `agentic_core/synthesis/cognitive_scraper.py:63`
- **status:** OPEN
- **claim:** _simulate_extraction() sleeps 0.5s and invents a finding — `concept: f"{topic}_{source}_{random.randint(100,999)}"`, `summary: f"Frontier advancement in {topic} detected via {source}"`, `confidence: 0.94 + random.random()*0.05` — which _update_concept_graph then writes into the UEG via `ueg.add_insight(..., source_id=findings["source"], category="cognitive_concept")`. The mission returns `status: "CONVERGED"`. perform_temporal_analysis() (line 100) reports `graph_health: {"growth_rate": "124 nodes/week", "accuracy": 0.92}`.
- **why it is a fabrication:** Invented research findings are persisted into the platform's knowledge graph carrying source_id "arxiv" / "conference" / "blog" and a confidence score — so downstream readers of the UEG see externally-sourced, confidence-rated intelligence that was generated by random.randint. Nothing is scraped; the sub_agents dict maps source names to agent-class name *strings* that are never instantiated. "124 nodes/week" and accuracy 0.92 are graph-health metrics nothing measures.
- **reach:** stored into the UEG (user-visible knowledge store) — driven by grand_synthesis_engine.py:299 (CLI meta-pipeline) and by products/scraping_suite/sdk/dual_mode_scraper.py:224

### `agentic_core/synthesis/content_production.py:20`
- **status:** OPEN
- **claim:** produce_scientific_draft() writes a LaTeX manuscript to DATA_DIR and returns it; its Results section always contains the literal sentence "Preliminary findings from the BTO research swarms suggest 92% confidence in the observed patterns." alongside a Methods section asserting "We utilized the Quadruple Engine Pillar (QEP), specifically the Evolutionary Simulation Engine (ESE) and Autonomous Resource Optimization (ARO)."
- **why it is a fabrication:** A scientific manuscript the user receives as a .tex file asserts a numeric confidence level and names the methods that produced it. No swarm ran, no confidence was estimated, and only `topic` and `data_summary` are interpolated — the 92% is a constant in an IMRaD Results section, which is the single place a reader is entitled to assume a measurement.
- **reach:** stored + returned (writes DATA_DIR/draft_*.tex) but no live route: registered as tool "produce_scientific_draft" in agentic_core/api/v138/ceo.py:68, and ToolRegistry.call_tool is only invoked from /ch

### `agentic_core/synthesis/grand_synthesis_engine.py:283`
- **status:** OPEN
- **claim:** Writes docs/introspection/global_health_v126.0.md containing "- **Global Reach:** 12 Countries", "- **Scholarly Influence:** High", "- **Market Liquidity:** Optimal", "- **Symbiotic Stability:** 0.98". Separately, _generate_assimilation_blueprints() (line ~600) writes a row into every generated blueprint doc: "| **Purpose Alignment Review** | Verified - Aligns with Article 336. |".
- **why it is a fabrication:** A file named "Global Ecosystem Health Report" asserts a country count and a stability score that no counter or monitor produces — these are four literals in a write() call. And every assimilation blueprint the engine emits carries a "Verified" alignment review that no review ran; a reader of docs/biomimetic/blueprints/*.md has no way to tell the stamp is unconditional.
- **reach:** written to docs/ (human-read artifacts) by the CLI meta-pipeline; no HTTP route

### `agentic_core/synthesis/knowledge_synthesis.py:55`
- **status:** OPEN
- **claim:** _embed() returns `np.random.rand(128).tolist()` as the document embedding. _extract_triples() returns a hardcoded `{"subject": "Jules AI", "predicate": "employs", "object": "Biomimetic Logic"}` when the text contains "biomimetic" (and a second fixed triple for "embodied"), which _integrate_to_ueg writes to the UEG as category "extracted_knowledge" with a provenance block {source_url, agent_id, ingested_at, operon_id} and reverse-transcribes into the genomic registry. process_data_stream reports `status: "SYNTHESIZED"`, `triples_extracted: N`.
- **why it is a fabrication:** An invented entity-relationship triple is stored as extracted knowledge and stamped with full provenance naming the source URL it was supposedly extracted from — the constellation "Mock links for visualization" pattern, but persisted and provenanced. The random embedding means the vector store's similarity is meaningless while presenting as a semantic index.
- **reach:** stored into the UEG + genomic registry — via products/scraping_suite/sdk/dual_mode_scraper.py:216

### `apps/workstation-superapp/src/components/QEPFlagshipFeatures.tsx:120`
- **status:** OPEN
- **claim:** `<Badge color="aura">GaaS Verified</Badge>` and `<Badge color="highlight">v0.9-P0</Badge>` in the footer of the result panel; plus `{activeFeature === f.id && !loading && <CheckCircle size={16} className="text-aura animate-pulse" />}` (line 64) — a pulsing success tick on the selected card.
- **why it is a fabrication:** This panel's own body text (lines 100-105) correctly states 'This module is described in the platform plan but has no backend yet, so no result can be shown — a fabricated one would be worse than none.' The honesty fix landed on the body but missed the chrome: the same panel still carries a 'GaaS Verified' badge, and selecting a card still lights a green success tick. A 'Verified' assertion on a module that just told the user nothing ran directly contradicts the panel it sits in.
- **reach:** live route — ReligionHub.tsx:122 renders <QEPFlagshipFeatures /> at /religion

### `apps/workstation-superapp/src/components/QEPImmersiveTools.tsx:39`
- **status:** OPEN
- **claim:** `<span>Domain Sync Active (v1.0)</span><Badge color="aura">LIVE</Badge>` (lines 40-41) and `<CheckCircle className="text-emerald-500" /> Data Sovereignty Verified` (line 59).
- **why it is a fabrication:** The component contains zero fetch or axios calls (verified: 0 matches) — it has no data source of any kind. It nonetheless shows a green 'LIVE' badge asserting an active sync, and a green tick asserting that data sovereignty has been verified. Nothing syncs and nothing verifies. It renders identically on six domain hubs, so the claim appears across most of the product surface.
- **reach:** live routes — rendered on /religion, /science, /law, /education, /care, /employment (CareHub, EducationHub, EmploymentHub, LawHub, ReligionHub, ScienceHub)

### `apps/workstation-superapp/src/pages/Contribute.tsx:92`
- **status:** OPEN
- **claim:** `Community Vitals`: `External Contributors` `142`, `Adopting Projects` `12`, `Open Issues` `24` (lines 92-100). Above them, a 'Recent RFCs' list hardcodes `{ id: 'RFC-142', title: 'Planetary Latency Optimization via LEO Routing', status: 'Proposed', date: '2h ago' }` and `{ id: 'RFC-107', ..., status: 'Ratified', date: '1d ago' }` (lines 65-66).
- **why it is a fabrication:** The page links to the real GitHub repo (github.com/Rehan719/Workstation) and presents these as that project's community metrics and governance record. Nothing queries GitHub. The relative timestamps ('2h ago', '1d ago') actively assert recency that cannot be true for string literals, and 'RFC-107 · Ratified' claims a governance decision that never happened.
- **reach:** live route — /contribute (App.tsx:237)

### `apps/workstation-superapp/src/pages/domains/QEPReligionHub.tsx:135`
- **status:** OPEN
- **claim:** MemorizationSuite 'Retention Heatmap': `{Array.from({ length: 60 }).map((_, i) => <div className={i % 7 === 0 ? 'bg-aura' : i % 3 === 0 ? 'bg-aura/40' : 'bg-slate-900'} title={`Level ${i % 5}`} />)}`, captioned `Last 60 Days Intensity` with a Less→More intensity legend. Also `<VitalRow label="Interval" value="4 Days" />` (line 163).
- **why it is a fabrication:** A GitHub-contributions-style heatmap whose cell intensities are computed from the array index (i % 7, i % 3) and whose tooltips say 'Level 0-4' from i % 5, captioned as the user's last 60 days of memorisation intensity. No review history is read. A user sees a personal study-consistency record that was generated by modular arithmetic. Note the sibling rows were partly cleaned ('Ease Factor 2.5 (SM-2 default)' and 'Repetitions — (no history yet)' are honest), which makes the unlabelled 'Interval 4 Days' and the heatmap read as the real remainder.
- **reach:** live route — /qep and /qep-religion, 'mem' tab

### `apps/workstation-superapp/src/pages/domains/ReligionHub.tsx:71`
- **status:** OPEN
- **claim:** `Active Alliances` `42` (line 71) and `Moral Resonance` `0.99` (line 75) rendered in the 'Sacred Knowledge Garden' panel; plus `Alignment Score` / `OPTIMAL` with a fixed `w-[98%]` bar (lines 224-229) in a card whose body text reads 'Moral alignment checks run through the real §11 compliance engines (Halal/Sharia · Ethical).'
- **why it is a fabrication:** 'Moral Resonance 0.99' and 'Alignment Score OPTIMAL' at 98% are literals. The alignment card explicitly tells the user the number comes from the real §11 compliance engines — an assertion of provenance for a value that is never fetched from them. '42' as an alliance count is the same round literal flagged in the confirmed `study_groups_active 42` case.
- **reach:** live route — /religion (App.tsx:175)

### `apps/workstation-superapp/src/pages/enterprise/CapitalDashboard.tsx:277`
- **status:** OPEN
- **claim:** `[{ id: '1130', title: 'Concentration Limit Increase', status: 'UNDER REVIEW', rationale: 'Allow 25% allocation for index ETFs to improve stability.' }, { id: '1205', title: 'Real-Time Data Mandate', status: 'ENACTED', rationale: 'Requirement for WebSocket ingestion for all high-stakes trades.' }]` rendered as constitutional articles with status badges and a Cast Vote button wired to `handleCastVote` (line 82), which only pushes to local state and toasts 'Vote Cast — Article {id}'.
- **why it is a fabrication:** Two constitutional articles are presented as governance records, one with status ENACTED — asserting that the platform's constitution actually contains and has ratified Article 1205. The real constitution is served at /api/v154/constitution/articles (fetched by ConstitutionalUI.tsx:17); these two are literals in a different page. The vote button also records nothing — it toasts 'Vote Cast' while no vote leaves the browser. Adjacent 'Risk Limits' figures ('Max Asset Concentration 20%' with a w-[20%] bar, 'Global Diversification OPTIMAL' with five hardcoded green segments) are likewise constants
- **reach:** live route — /economy?tab=capital, 'Evolution' and 'External Markets' tabs

### `apps/workstation-superapp/src/pages/governance/ConstitutionalUI.tsx:78`
- **status:** OPEN
- **claim:** `<span>Trust Score</span><span className="text-aura">0.96 (SOVEREIGN)</span>` with a matching fixed bar `<div className="h-full bg-aura w-[96%]" />` (line 81).
- **why it is a fabrication:** A governance trust score with a tier label ('SOVEREIGN') and a 96%-filled meter, with nothing behind it. It is especially misleading here because the very next card on the same page renders genuinely live GaaS v5 data (`gaas.circuit_breaker.threshold`, `gaas.circuit_breaker.error_rate`, `gaas.ueg.total_events`, real root hash) and the timeline below was already made honest ('Illustrative example (demo — not a real event)'). The surrounding honesty makes the constant read as measured.
- **reach:** live route — /governance-hub?tab=constitution (App.tsx:225-226, GovernanceCenter.tsx:12)

## LOW (7)

### `agentic_core/api/v310/business.py:52`
- **status:** OPEN
- **claim:** POST /api/v310/entrepreneur/generate-plan falls back, when the AI reply fails to parse as JSON, to a hardcoded plan: quarterly revenue of funding_goal × 0.15 / 0.40 / 0.90 / 1.60 with growth strings "+15%/+40%/+90%/+160%", plus fixed strategic_steps and key_risks. The response then sets `result["status"] = "plan_synthesized"` on both paths (line 78).
- **why it is a fabrication:** The fallback is never disclosed to the caller. Both the AI-generated plan and the arithmetic-on-the-funding-goal plan come back with the same `plan_synthesized` status and no flag, so a user cannot tell that their Q4 revenue projection is simply their own funding goal times 1.6. This is a fallback that fails the "clearly labelled as a fallback" exemption purely because the label never reaches the consumer.
- **reach:** live route (mounted app_mvp.py:89)

### `agentic_core/catalog/bto.py:143`
- **status:** OPEN
- **claim:** POST /bto/configure returns a blueprint whose components assert state: entity → "status": "Provisioned"; organism → "status": "Bootstrapped" with layers L1–L12; vsb → "status": "Active"; csuite → four members each "status": "ACTIVE". _integrate_product (line 68) marks every selected catalog product `"status": "INTEGRATED", "integration_mode": "Plug-in resource — accessible via Sovereign Mesh"`.
- **why it is a fabrication:** configure_bto performs no provisioning, bootstrapping, activation or integration — it dict-builds a response. "Provisioned" / "Bootstrapped" / "ACTIVE" / "INTEGRATED" are past-tense state assertions, not design labels, and "accessible via Sovereign Mesh" tells the user the resource is reachable. Worth contrasting with the sibling POST /bto/build in the same file, which is honest — it really does drive the §13 deliverables engine and reports per-item BUILT/FAILED plus the QMS verdict.
- **reach:** live route — POST /bto/configure

### `agentic_core/economy/charity.py:28`
- **status:** OPEN
- **claim:** `_CANDIDATES` hardcodes per-cause metrics — e.g. `{"id": "clean_water", ... "urgency": 0.85, "gravity": 0.90, "reach": 0.92, "trust": 0.92, "donation_100pct": True}` and six siblings. `CharityIntelligence.allocate()` scores from them and returns `grants` carrying `score`, `amount_wst` and `donation_100pct: True`, with `method: "urgency × gravity × reach × marginal-impact × trust; 100%-donation causes only; every grant compliance-screened"`.
- **why it is a fabrication:** The `allocate()` payload is embedded in every cycle report as `giving_back` (metabolism.py) and surfaces in VSBCockpit.tsx's cycle panel and the board pack. There it presents a per-cause `trust` and `urgency` rating and a `donation_100pct: true` assertion as if something rated or verified them — and the `method` string actively claims those inputs are what drove the allocation. Nothing measures them; they are seven literals a developer typed. This is a labelling gap rather than an invented output figure: the standalone route GET /api/v1/economy/charity/candidates does disclaim ("sources curate
- **reach:** live — served inside POST /api/v1/economy/cycle's `cycle.giving_back`, rendered in VSBCockpit.tsx, and reachable directly at GET /api/v1/economy/charity/candidates (which does disclaim)

### `agentic_core/governance/grn_modeler.py:64`
- **status:** OPEN
- **claim:** infer_topology(), documented as "Reconstructs GRN topology from system activity logs using correlation analysis", ends `return topology if topology else {"orchestrator": ["manager", "dispatcher"]}` — an invented edge set returned whenever the logs are empty or unparseable.
- **why it is a fabrication:** Same shape as the /api/tools/constellation "mock links for visualization" case: a relationship between named components presented as inferred from real activity, with nothing in the returned value distinguishing the invented fallback from a genuine reconstruction. The honest empty-log answer is {}.
- **reach:** unreachable — no importer outside _archive/

### `apps/workstation-superapp/src/components/organism/AgentForge.tsx:111`
- **status:** OPEN
- **claim:** `Node-based composition active. Genetic inheritance: 98.4%. Swarm stability: NOMINAL.`
- **why it is a fabrication:** A precise one-decimal 'genetic inheritance' figure and a stability verdict stated as fact in body text, with no computation anywhere in the component. Unreachable (no importer), so low — flagging so it is cleaned alongside the other two orphaned organism components rather than surviving to be wired up.
- **reach:** unreachable — not imported by any page or component

### `apps/workstation-superapp/src/components/organism/NeuralLink.tsx:57`
- **status:** OPEN
- **claim:** `<span>Telemetry Bandwidth: 1.2 GB/s</span><span>Article 1200 Compliance: VERIFIED</span>` (lines 57-58); `setSynapseActivity(Array.from({ length: 24 }, () => Math.random()))` (line 26) drives the activity grid.
- **why it is a fabrication:** Asserts a measured throughput figure and a VERIFIED compliance status against a named constitutional article, with a Math.random()-driven activity display beneath. Nothing measures bandwidth and nothing checks Article 1200. Unreachable today (no importer), so ranked low — but the 'VERIFIED' string is the same class as the invented SHARIA_AUDIT approval and should be removed with the file.
- **reach:** unreachable — not imported by any page or component

### `apps/workstation-superapp/src/components/organism/OrganismVitals.tsx:31`
- **status:** OPEN
- **claim:** `setVitals({ sentience: 85 + Math.random() * 10, compliance: 98 + Math.random() * 2, throughput: 12 + Math.random() * 5, load: 45 + Math.random() * 20, stability: 95 + Math.random() * 5 })` on a 3-second interval, rendered as 'Compliance 99.4%', 'System Sentience 91.2%', 'Stability 97.8%' etc. under the heading 'Organism Health Vitals'.
- **why it is a fabrication:** A compliance percentage produced by a random number generator, refreshed every 3 seconds so it appears to be live telemetry. This is the purest fabrication in the frontend — no data source is even gestured at. Ranked below the reachable findings only because the component is never imported: no file outside components/organism/ references OrganismVitals, so it currently renders nowhere. It should be deleted rather than fixed, or it will be wired up by someone later.
- **reach:** unreachable — not imported by any page or component
