# Frontend Defect Ledger — seeded by the Round-11 reconnaissance (2026-08-30)

Source: a 5-agent static scan (one agent per defect class) over `apps/workstation-superapp/src`,
cross-referenced against `agentic_core` handlers, plus a method-aware UI→backend endpoint diff.
Status legend: **CONFIRMED** = independently re-verified against the tree by the orchestrator;
**high/medium** = the scanning agent's confidence — re-verify in the browser before fixing, and
re-verify line numbers (they drift). Every fix needs: fix at source → re-test the exact control in
a real browser → regression guard → honest progress-log entry.

## Round-11 fix log (append-only)

**Batch A — cluster 1 (the governance surface), fixed + browser-verified 2026-08-30:**
- ChangeControlAgency.tsx REWRITTEN to the real contract: reads `changes` (not `entries`), rows keyed
  `cca_id`/`impact_tier`/lowercase status, AUTO badge from `decision === 'auto_approved'`, detail
  (description/review_result/twin verdict) fetched from GET /{cca_id} on expand, review POSTs the
  required ReviewDecision body, review/implement failures surface the backend's `detail` (the 409
  twin-pre-validation messages included), honest load-error state. BROWSER-VERIFIED: 50 real records
  render (was permanently empty); Implement click transitioned approved->implemented live.
- NEW DISCOVERY fixed with it: the UI called GET `/api/v1/cca/` (trailing slash) which the SPA
  catch-all intercepts into a 404 BEFORE FastAPI's slash-redirect — trailing slashes are NOT
  forgiven in this app. `/api/v1/projects/` + `/api/v1/ingest/` were probed and are correct as-is
  (those routers register WITH the slash).
- VSBEconomy.tsx: the 200 `{cycle:null, governance:held}` materiality branch now renders an amber
  Owner-approval hold card (cca_id + link to /change-control). BROWSER-VERIFIED with a 2,000,000 WST
  material cycle.
- genesis.py: the SSE `complete` event now carries the real `governance` object (parity with the
  blocking path); GenesisJourney badge fallback is 'not reported', never a fabricated 'allowed'.
- GenesisJourney.tsx: the blocking-establish fallback no longer renders an error body as a born VSB
  (res.ok + visible error), and gate approve/reject no longer silently no-ops on 4xx/5xx.
- Regression guard: `test_cca_ui_contract_shapes` (integration_tests/test_mvp_spine.py) locks the
  list/review/submit/detail shapes + the trailing-slash 404 behavior in CI.

**Batch B — cluster 2 (HTTP-status blindness), class-killed 2026-08-30:**
- NEW `lib/api.ts`: `apiJson()` throws ApiError (with the backend's own `detail`) on any non-2xx +
  `errorMessage()` for honest user-facing text — the structural end of `setState(await r.json())`
  swallowing error bodies.
- Adopted at: Deliverables (produce/open/regenerate — error bodies can no longer crash the detail
  pane), NativeAI (complete/ensemble/swarm/saved-run/lifecycle — page-crash paths closed, lifecycle
  failures visible), TransformationDashboard (tick/assess/orchestrate — crash path closed),
  CognitionIntegration (solve/align — blank-success pane closed), ManagementSystemsHub (all six
  Generate buttons now surface failure), VSBCockpit (produce + orchestrate route into actErr),
  SynthesisStudio (delete failure → errorMsg), Login (create-user network catch), Generator (copy
  failure visible), GovernanceHub (meta-proposal: res.ok gate — no more false success toast — plus
  the REAL request field `submitted_by` and the real `cca_id` in the list entry).
- Browser-verified representative: Deliverables produce ran through apiJson and rendered the detail
  pane; no new console errors. tsc 0 + vite build clean.

**Batch C — cluster 3 (fabricated/theatrical governance handlers), fixed + browser-verified 2026-08-30:**
- GovernanceHub AuditTab: "Run Manual Audit" now recomputes the real tamper-evident UEG hash chain
  (GET /api/v1/gaas/ueg/verify) instead of fabricating a PASSED row with a Math.random() hash; stats
  and the event log are live UEG data (326 events, chain VALID verified in-browser); hardcoded
  mockInventory/mockCommits deleted.
- GovernanceHub SanctumTab: proposals are the REAL pending constitutional CCA changes; the fake
  1.5s "reputation" access timer is now the constitutional ledger answering; "Cast Sovereign Vote"
  (approve/reject) POSTs the Owner's audit-trailed override. VERIFIED END TO END in the browser: a
  real CRITICAL change submitted -> appeared in the Sanctum -> Sovereign Approve clicked -> server
  record approved with review_result "Manual override: Sovereign vote..." and audit trail
  submitted,review_started,approved,twin_prevalidation_pass.
- Fabricated "1,420 reputation / 2.42x voting weight / 142 cross-realm contributions" panel deleted;
  replaced with Owner-sovereign truth + the real pending-change count.
- STILL OPEN in cluster 3 (next): SolutionsPlatform Build/Launch fake provisioning + scripted
  "Mission is LIVE" log and its catch that fabricates a spec; QEPDashboard engine cards and the 13
  QEPFlagshipFeatures cards (mock results on 7 hub pages); CEOChat "Retry" flipping the status pill
  without reconnecting; the unbound Composer temperature slider.

**Batch D — cluster 3 COMPLETE (all remaining fabricated handlers), 2026-08-30:**
- SolutionsPlatform: design-catch fabrication removed (failure now visible); Build no longer invents
  a provisioned infrastructure (honest PLAN instead); Launch replaced the scripted always-success
  "Mission is LIVE" log with a REAL readiness check + an honest "this page provisions nothing" +
  a pointer to Genesis.
- QEPDashboard engine cards (7 hub pages) and the 13 QEPFlagshipFeatures cards: mock results deleted,
  honest "not yet built" states with links to the live capabilities.
- CEOChat "Retry": real health check instead of flipping the pill to online.
- VisualAgentComposer temperature slider: bound to the agent's real params.temp (was inert).
- Proof: the shipped bundle contains ZERO occurrences of the fabricated strings ("Mission … is LIVE",
  "All systems nominal", "infra-", "Engine running at 100", "CERT-87a1b2c3", "1,420", "2.42x",
  "Provisioning infrastructure"). CLUSTER 3 IS CLOSED.

**Batch E — cluster 5 CLOSED (raw-anchor bearer bypass), 2026-08-30:**
- GenesisJourney's three preview links (site/webapp/PWA), ProjectsHub Download, and SynthesisStudio's
  per-format + history downloads now use openExport/downloadExport (bearer-carrying fetch -> blob)
  instead of raw navigations that 401 under auth; failures surface instead of dying in a new tab.
- Whole-tree sweep confirms ZERO remaining raw /api anchors, window.open('/api'), or response-field
  hrefs. ALL FIVE LEDGER CLUSTERS ARE NOW CLOSED.

**New discovery-sweep item (open):** ws://localhost:8010/api/v154/ws/streams fails repeatedly in the
browser console (pre-existing; the frontend opens a WebSocket the backend refuses) — triage in the
discovery sweep.

## Endpoint layer (method-aware diff: 170 UI calls vs 459 backend method+route pairs)
- Exactly ONE missing endpoint: `POST /api/v1/claude/chat` (components/ClaudeAgentPanel.tsx) — backend has only `/api/v1/claude/status`. **CONFIRMED**
- ZERO method mismatches. The user-visible breakage therefore lives almost entirely in the classes below, not in missing routes.

## Response-shape mismatches (UI reads keys the backend never returns)
1. **[CONFIRMED]** `pages/enterprise/ChangeControlAgency.tsx:292` — Change Control Agency page — the entire change-request list and the four stats tiles (Pending/Approved/Rejected/Implemented)
   - The page is permanently empty ('No change requests yet. Submit one above.') and every stat shows 0, no matter how many change requests exist — including the economy materiality holds the /cycle endpoint tells users to review here.
   - Evidence: `UI reads a key the backend never returns: ChangeControlAgency.tsx:292 `const all: CCAEntry[] = allRes.data.entries ?? [];` vs agentic_core/api/change_control.py:574 `return {"changes": all_changes[:50], "total": len(all_`
2. **[high]** `pages/enterprise/ChangeControlAgency.tsx:80` — CCA entry cards — status icon, tier chip, status filter tabs, AI Review / Implement buttons
   - Even once the list key is fixed, every card is broken: `STATUS_ICONS[entry.status]` is undefined for the real lowercase statuses (rendering `<Icon/>` with undefined crashes React), the tier chip reads `entry.tier` (backend sends `impact_tier`), the filters `e.status === 'PENDING'` never match, and the Review/Implement buttons would POST to /api/v1/cca/undefined/review because `entry.id` doesn't exist (backend sends `cca_id`). `description`, `ai_review`, `auto_approved`, `health_at_submission` are also never present in list rows.
   - Evidence: `UI: ChangeControlAgency.tsx:16-27 `interface CCAEntry { id: string; ... tier: Tier; status: Status; ... ai_review?: string; auto_approved?: boolean; }` with `type Status = 'PENDING' | 'APPROVED' | ...`; backend list rows`
3. **[CONFIRMED]** `pages/enterprise/VSBEconomy.tsx:132` — 'Run Metabolic Cycle' button on the Economic Metabolism page
   - When a cycle is material (estimated distributable ≥ 250,000 WST, default ECONOMY_MATERIALITY_WST) the backend returns HTTP 200 with `cycle: null` and a governance hold that names the CCA id to approve — but the UI renders governance only inside `{cycle && ...}`, so the click ends with no result card, no error, and no hold notice: a silent no-op on exactly the flows the Owner must approve.
   - Evidence: `UI: VSBEconomy.tsx:132 `setCycle(d.cycle); setGov(d.governance?.status ?? '');` with the only governance rendering at line 328 inside the `{cycle && (` block (line 314). Backend: agentic_core/economy/governance.py:145-14`
4. **[high]** `pages/enterprise/ChangeControlAgency.tsx:180` — 'Submit Change Request' form confirmation message
   - The success message always shows '✓ Change submitted — awaiting AI review', even when the backend auto-approved the LOW-tier change, because the UI branches on a key the submit endpoint never returns.
   - Evidence: `UI: ChangeControlAgency.tsx:180 `setMsg(res.data.auto_approved ? '✓ Change auto-approved (LOW tier + healthy organism)' : '✓ Change submitted — awaiting AI review');` vs backend change_control.py:218-223 `return {"cca_id`
5. **[high]** `pages/synthesis/GenesisJourney.tsx:273` — 'Establish VSB IDBO Entity' button — fallback (blocking) establish path
   - If the SSE stream fails and the blocking /establish also returns an error (e.g. 401 under auth, 422, 500), the UI stores the FastAPI error body `{detail: ...}` as the established VSB and renders a fabricated success card: an undefined name, 'vsb_id · operational', and 'Living Enterprise IDBO generated — dashboard undefined'.
   - Evidence: `UI: GenesisJourney.tsx:270-273 `const res = await fetch('/api/v1/genesis/establish', ...); setVsb(await res.json());` — no `res.ok` check before treating the JSON as `{vsb_id, name, dashboard}`; a FastAPI HTTPException b`
6. **[high]** `pages/synthesis/GenesisJourney.tsx:720` — Governance badge on the established-VSB card after the streamed 'Establish VSB IDBO Entity' flow
   - After a streamed establishment the card always shows 'governance allowed' regardless of the actual gaas.v5 gate outcome, because the SSE 'complete' event's data omits the governance object the UI reads (the blocking /establish path does include it).
   - Evidence: `UI: GenesisJourney.tsx:720 `{vsb.vsb_id} · operational · governance {vsb.governance?.status ?? 'allowed'}` where vsb is set from the complete event (line 261/266). Backend: agentic_core/api/genesis.py:727-733 `yield _eve`
7. **[medium]** `pages/enterprise/ChangeControlAgency.tsx:309` — 'AI Review' button on a pending change entry
   - The review action posts no body, but the backend declares a required `ReviewDecision` body model with no default — FastAPI rejects the bodiless POST with 422, so the review would never run even after the list-shape fixes make the button reachable.
   - Evidence: `UI: ChangeControlAgency.tsx:309 `await axios.post(`/api/v1/cca/${id}/review`);` (no data argument) vs backend change_control.py:416 `async def review_change(cca_id: str, req: ReviewDecision):` — a Pydantic model paramete`
   
   _Scanner summary:_ Scanned the ~15 most user-critical UI fetch paths (all 21 DomainTool run buttons across the 6 domain hubs + LawHub analyse, Deliverables produce/list/types/output-formats/regenerate/refine/export, Genesis journey/establish/establish-stream/repo/website/webapp/mobile/board-pack/review-gates, Economy entity-types/cycle/waterfall/owner-payments/payout/board-pack/living-vsbs, Marketplace catalog/products, CCA list/queue/submit/review/implement) against their agentic_core handlers. Most surfaces match key-for-key. The verified response-shape defects cluster in the Change Control Agency page (reads `entries` where the backend returns `changes`; expects `id`/`tier`/UPPERCASE statuses where the backend sends `cca_id`/`impact_tier`/lowercase; reads a never-returned `auto_approved`; posts a bodiless review to a required-body endpoint) — making the governance surface permanently empty; plus the Economy 'Run Metabolic Cycle' button silently swallowing the {cycle:null, governance:held} materiality-hold branch, and two Genesis establish edge branches (SSE complete data lacks `governance`, and the blocking fallback renders an error body as a successful VSB).

## Silent failures (HTTP-status blindness: no res.ok / empty catch on user actions)
8. **[high]** `pages/governance/GovernanceHub.tsx:396` — Sovereign Sanctum 'Submit to CCA' button (submitMetaProposal, wired at line 477)
   - Constitutional meta-proposal POST to /api/v1/cca/submit never checks res.ok. On any 4xx/5xx the code still appends the proposal to the list, clears the form, and shows the success toast 'Constitutional meta-proposal submitted to Change Control Agency for review' — a false success for a governance-critical action. Only network-level failures reach the catch.
   - Evidence: `const data = await res.json(); setProposals(prev => [...prev, { id: data.id ?? `meta-${Date.now()}`, ... }]); ... toast('Constitutional meta-proposal submitted to Change Control Agency for review');`
9. **[high]** `pages/enterprise/ChangeControlAgency.tsx:317` — 'Review' and 'Implement' buttons on change requests (triggerReview line 306 / triggerImplement line 314, wired via onReview/onImplement at 415-416)
   - Both handlers are try/finally with NO catch. If the axios POST fails (403, 409, 422, 500), the rejection is unhandled: the spinner clears (finally), the list is not reloaded, no message appears. The user clicks Implement on a change request and nothing visibly happens.
   - Evidence: `try { await axios.post(`/api/v1/cca/${id}/implement`); await load(); } finally { setActionId(null); }`
10. **[high]** `pages/synthesis/GenesisJourney.tsx:353` — Review-gate Approve (✓) / Reject (✗) buttons (decideGate, wired at lines 920-921)
   - The gate-decision POST has no res.ok check. On HTTP 4xx/5xx nothing throws; the code refetches the gates (unchanged) and shows no error — the Owner's approve/reject click on a stage gate silently does nothing. The W344 catch covers only network failure.
   - Evidence: `await fetch(`/api/v1/vsb/${vsb.vsb_id}/review-gates/${stage}/decision`, { method: 'POST', ... }); setGates(await fetch(...).then(r => r.json()));`
11. **[high]** `pages/SolutionsPlatform.tsx:139` — 'Generate Specification' button (handleDesign, wired at line 367)
   - When the /api/v1/ai/query call fails, the catch fabricates a canned specification client-side and sets status design:'done' — the user sees a completed AI-generated spec that was never generated, with no indication of failure.
   - Evidence: `} catch { setSpec(s => ({ ...s, generated_spec: `## Solution Specification...` })); setStatus(s => ({ ...s, design: 'done' })); }`
12. **[high]** `pages/Deliverables.tsx:68` — 'Produce' button (produce, wired at line 154; same defect in regenerate at line 89)
   - No r.ok check on POST /api/v1/deliverables/produce. On 422/500 the FastAPI error body ({detail:...}) is passed to setSelected(), opening a broken detail pane as if a deliverable was produced. regenerate() (line 89) likewise replaces the currently open deliverable with the error body and clears the brief, implying success. Catch handles network errors only.
   - Evidence: `const d = await r.json();       setSelected(d);       await loadList();`
13. **[high]** `pages/synthesis/GenesisJourney.tsx:273` — 'Establish this VSB' button (establish fallback path, wired at line 694)
   - The blocking fallback sets the established entity from res.json() without checking res.ok — a 4xx/5xx body renders the post-establishment panel with an undefined vsb_id (subsequent repo/website/gates calls hit /api/v1/vsb/undefined/...), implying the entity was born. If the fallback also network-fails, the inner catch is empty: the spinner stops and nothing at all is shown.
   - Evidence: `setVsb(await res.json());       } catch { /* surfaced by absence of vsb */ }`
14. **[high]** `pages/enterprise/VSBCockpit.tsx:182` — Deliverables 'Produce' button in the VSB cockpit (produceDeliverable, wired at line 504)
   - Catch is an empty comment. If the produce POST fails (validation, 500, network), the busy state clears and nothing visible happens — the comment's claim ('surfaced by the list not growing') is not a user-visible signal, especially when deliverables already exist.
   - Evidence: `} catch { /* surfaced by the list not growing */ }`
15. **[high]** `pages/enterprise/VSBCockpit.tsx:165` — Per-objective 'orchestrate' button in the Living Plan tab (orchestrateObjective, wired at line 470)
   - Catch is an empty comment; axios throws on every HTTP error, so a failed orchestration ends the spinner with no output and no error. Additionally, a 200 response without r.data.tree also renders nothing. The user cannot distinguish success, failure, or no-op.
   - Evidence: `if (r.data?.tree) setObjOrchResult(m => ({ ...m, [oid]: r.data.tree }));     } catch { /* best-effort — the run is recorded server-side */ }`
16. **[high]** `pages/CognitionIntegration.tsx:41` — 'Run cascade' button (runSolve, wired at line 87)
   - Empty catch with no error state for the solve action: on network failure the spinner stops and nothing appears. There is also no r.ok check, so on 4xx/5xx the error body is set as the result and the result panel renders 'Engines run:' with empty content — implying the cascade ran.
   - Evidence: `setSolveRes(await r.json());     } catch { /* surfaced by absent result */ }`
17. **[high]** `pages/developers/NativeAI.tsx:210` — Model lifecycle buttons: evaluate / promote / retire / reinstate (lifecycleAction, wired at lines 532 and 538)
   - The lifecycle POST has no res.ok check and the catch is empty ('surfaced via reload'). On HTTP 4xx/5xx nothing throws, loadLifecycle() reloads the unchanged estate, and on network failure the empty catch shows nothing either — a retire/promote click that fails is indistinguishable from one that succeeded with no change.
   - Evidence: `await fetch(`/api/v1/native-ai/lifecycle/${action}`, { method: 'POST', ... });       loadLifecycle();     } catch { /* surfaced via reload */ }`
18. **[high]** `pages/synthesis/SynthesisStudio.tsx:176` — Ingested-file delete (trash) button in the knowledge base list (deleteFile, wired at lines 690-691)
   - Catch only console.errors. If the DELETE fails, the file stays in the list with no message — the user's delete click silently does nothing (errorMsg state exists in this component but is not used here).
   - Evidence: `} catch (e) { console.error('Delete failed:', e); }`
19. **[high]** `pages/TransformationDashboard.tsx:54` — 'Tick' and 'AI Assess' buttons (tick line 52 / assess line 57, wired at lines 103 and 106)
   - Neither handler checks r.ok, so HTTP 4xx/5xx pass silently: Tick 'succeeds' and reloads the picture as if the heartbeat ran; AI Assess sets assessment to '' (d.assessment ?? '' on an error body) so the spinner stops and nothing appears. The W329 catches cover only network-unreachable.
   - Evidence: `try { await fetch('/api/v1/transformation/tick', { method: 'POST' }); await load(); } catch { setError('Tick failed — backend unreachable'); }`
   
   _Scanner summary:_ Scanned all onClick/onSubmit handler paths under apps/workstation-superapp/src (pages/ + components/) for swallowed fetch/axios failures. The dominant residual pattern after the W329/W344 rounds is HTTP-status blindness: raw fetch() calls whose catch handles only network failure while 4xx/5xx responses flow through the success path (false success toast in GovernanceHub's constitutional CCA submit; silent no-op on GenesisJourney gate approve/reject, TransformationDashboard Tick/Assess, NativeAI model lifecycle; error bodies rendered as results in Deliverables produce/regenerate and GenesisJourney's establish fallback). A second tier is comment-only/empty catches on real user actions (VSBCockpit produceDeliverable and orchestrateObjective, CognitionIntegration runSolve, SynthesisStudio deleteFile), one handler with no catch at all (ChangeControlAgency Review/Implement — unhandled rejection), and one fabricated-success catch (SolutionsPlatform Generate Specification synthesizes a canned spec and marks the phase done). Not flagged as they exceed the 12-cap but same pattern, lower materiality: Deliverables open(), VSBSpawnStudio Refresh (catch {}) and its Produce, BusinessPlan.orchestrate, NativeAI runComplete/runEnsemble/runSwarm and ResourceFabric simulate/run/compose (result set without r.ok), Login signup/addUser (no try/catch on network failure). Well-handled pages verified and excluded: VSBEconomy, ComplianceChecker, BoardOfDirectors, SovereignEvolution, ProjectsHub, ApplicationStudio, BTOCatalog, ChangeControlAgency submit form, DomainTool, Login sign-in.

## Dead / theatrical handlers (fabricated success, no backend call — HONESTY violations)
20. **[CONFIRMED]** `pages/governance/GovernanceHub.tsx:135` — "Run Manual Audit" button (AuditTab, wired at line 153)
   - Clicking runs no audit: after a 1.2s setTimeout it prepends a fabricated PASSED commit row with a random hash to the audit list. No backend call is made; the same tab also seeds mockInventory/mockCommits even when the status fetch succeeds (lines 114-128).
   - Evidence: `setTimeout(() => { setCommits(prev => [ { hash: Math.random().toString(16).slice(2, 10), status: 'PASSED', date: new Date().toISOString().slice(0, 10), issues: 0 },`
21. **[high]** `pages/governance/GovernanceHub.tsx:421` — "Cast Sovereign Vote" button (Sanctum tab, wired at line 495)
   - The vote handler only increments a local support percentage on hardcoded proposals — nothing is sent or persisted anywhere; a page reload discards the 'vote'. The proposals themselves are hardcoded at lines 415-418 and the access gate is a fake 1.5s timer (line 414).
   - Evidence: `const castSovereignVote = (id: string) => { setProposals(prev => prev.map(p => { ... const next = Math.min(100, parseFloat(p.support) + 1); return { ...p, support: `${next}%` };`
22. **[high]** `pages/SolutionsPlatform.tsx:155` — Build-phase "Build" action (handleBuild) on /solutions
   - Handler provisions nothing: it sleeps 1.8s then renders a fabricated infrastructure config (random infrastructure_id, hardcoded estimated_tps, provisioned_at timestamp) as if real provisioning happened, and marks the Build phase 'done'.
   - Evidence: `await new Promise(r => setTimeout(r, 1800)); const config = { infrastructure_id: `infra-${Math.random().toString(36).slice(2, 9)}`,`
23. **[high]** `pages/SolutionsPlatform.tsx:178` — Launch-phase "Launch" action (handleLaunch) on /solutions
   - Handler contacts no backend: it plays a scripted 11-step mission log via setTimeout delays, always ending in success ('All systems nominal.', 'Mission ... is LIVE.') regardless of any real system state, then marks launch 'done'.
   - Evidence: `['All systems nominal.', 'success', 400], [`Mission ${id} is LIVE.`, 'success', 200], ]; for (const [msg, level, delay] of steps) { await new Promise(r => setTimeout(r, delay)); appendLog(msg, level);`
24. **[high]** `components/QEPDashboard.tsx:36` — Engine cards (Card onClick at line 76) on 6 domain hubs (Religion/Science/Law/Education/Employment/Care)
   - Clicking an engine card runs nothing: runEngine sleeps 1.5s then renders a hardcoded mock result (status 'OPTIMAL', 'Engine running at 100% fidelity') with an 'Active' badge. No API is called. The inner 'Launch Engine' Button separately routes to the honest notImplemented toast (line 86), so the card and its button contradict each other.
   - Evidence: `await new Promise(resolve => setTimeout(resolve, 1500)); const mockResult: QEPResult = { engine, timestamp: new Date().toISOString(), status: 'OPTIMAL',`
25. **[high]** `components/QEPFlagshipFeatures.tsx:43` — 13 flagship feature cards (Card onClick at line 77) on the Religion hub
   - launchFeature performs no request: after a 1.2s sleep it renders hardcoded mockData (fake tajwid scores, competition rank, 'ISSUED' certificate id, zakat status, etc.) as feature results, with a CheckCircle success indicator.
   - Evidence: `// Simulated API call to the new CEO tools\n    await new Promise(resolve => setTimeout(resolve, 1200)); ... const mockData: Record<string, any> = {`
26. **[high]** `pages/enterprise/ChangeControlAgency.tsx:306` — "AI Review" and "Implement" buttons on change-control entries (wired at lines 135/145; triggerImplement at line 314 has the identical defect)
   - try/finally with no catch: if the POST fails (4xx/5xx/network), the promise rejection is unhandled — the spinner stops and the entry silently stays PENDING/APPROVED with zero feedback (the component has no error state at all; failure surfaces only in console).
   - Evidence: `const triggerReview = async (id: string) => { setActionId(id); try { await axios.post(`/api/v1/cca/${id}/review`); await load(); } finally { setActionId(null); } };`
27. **[high]** `pages/enterprise/ManagementSystemsHub.tsx:118` — All six "Generate ... Framework" buttons on /management (QMS line 118, BMS 150, and the panels at 181/211/241/272 share the identical pattern)
   - Each generate handler is try/finally with no catch: a failed POST leaves an unhandled promise rejection, the spinner stops, and no framework or error message ever appears — the button looks like it did nothing.
   - Evidence: `try { const res = await axios.post('/api/v1/mgmt/qms/generate', { organisation_name: org, domain, size }); onResult(res.data.framework); } finally { setLoading(false); }`
28. **[high]** `pages/CEOChat.tsx:190` — "Retry" (Retry connection) button in the CEO chat header, shown whenever aiStatus is not 'online'
   - The handler performs no reconnection attempt or health check — it just flips the status pill back to 'Planetary Strategy Active' by setting local state, misrepresenting a still-dead backend as online until the next send fails.
   - Evidence: `onClick={() => setAiStatus('online')}\n  title="Retry connection"`
29. **[high]** `components/organism/VisualAgentComposer.tsx:112` — "Inference Temperature" range slider in the Composer tab of LivingOrganisationHub (/ceo)
   - The slider is completely unbound — no value, no onChange, not connected to the selected agent's params — so dragging it changes nothing anywhere (it is the only unbound form input in the whole src tree). The adjacent 'GaaS COMPLIANT' badge is likewise unconditional.
   - Evidence: `<input id="agent-inference-temp" type="range" aria-label="Inference Temperature" title="Inference Temperature" className="w-full" />`
30. **[high]** `pages/Login.tsx:63` — "Create user" button (addUser, wired at line 142)
   - The fetch has no try/catch: HTTP errors are reported via nuMsg, but a network-level failure (server down) rejects the fetch itself, leaving an unhandled rejection and no message — the button silently does nothing. Contrast with login() above it, which wraps the same pattern in try/catch.
   - Evidence: `const r = await fetch('/api/v1/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(nu), });`
31. **[high]** `pages/developers/Generator.tsx:77` — "Copy" button for generated output (handleCopy)
   - clipboard.writeText is awaited with no catch: when the Clipboard API rejects (permission denied, non-secure context, window unfocused), the rejection is unhandled and the 'Copied' confirmation never appears — the user gets no signal the copy failed. Other copy handlers in the app (MyWork.tsx:24, DomainTool.tsx:151) wrap this in try/catch.
   - Evidence: `await navigator.clipboard.writeText(result.output); setCopied(true);`
   
   _Scanner summary:_ Scanned all pages/ and components/ of apps/workstation-superapp/src for dead/no-op handlers. No literally-empty handlers, handler-less buttons, or always-disabled-but-styled-enabled controls exist (verified by exhaustive AST-ish scans), and the notImplemented() calls are honest 'Coming Soon' toasts, so they were excluded. The real defects fall into two families: (1) theatrical handlers that fabricate success with setTimeout + hardcoded/mock data instead of calling any backend — worst on the Governance hub (fabricated PASSED audit records and a local-only 'Sovereign Vote'), the /solutions Build/Launch phases (fake infrastructure provisioning and a scripted 'Mission is LIVE' log), and the QEP engine/feature cards rendered on 7 hub pages; plus CEOChat's Retry button that flips the status pill to 'online' without reconnecting, and an unbound Inference Temperature slider in the agent Composer. (2) async handlers whose rejection is unhandled so failures are silent: ChangeControlAgency's AI Review/Implement buttons and all six ManagementSystemsHub Generate buttons use try/finally with no catch and have no error UI; Login's Create-user and Generator's Copy lack catches for network/clipboard rejection. Streaming pages (IntelligenceLab, DesignDevEngine, AuthorshipEngine, SynthesisNexus, VSBSpawnStudio) were checked and are fine — their local streamPost helpers catch internally and route to onError.

## Incoherent renders (error bodies as results, raw JSON dumps, crash-on-error panes)
32. **[high]** `pages/Deliverables.tsx:188` — Produce / Regenerate buttons and the deliverable detail pane (Living Deliverables page)
   - produce() (line 68) and regenerate() (line 89) do setSelected(await r.json()) with no r.ok check, so any 4xx/5xx error payload {detail:...} becomes `selected`; the detail pane then dereferences selected.versions.length and selected.ai_provenance.is_external and throws, killing the whole page render
   - Evidence: `{selected.type} · v{selected.versions.length}  …  ${selected.ai_provenance.is_external ?`
33. **[high]** `pages/TransformationDashboard.tsx:134` — Orchestrate button on the Vision·Realisation·Transformation dashboard
   - orchestrate() does setOrch(await r.json()) with no r.ok check (line 72); an error payload has no .validation, so the result block throws on orch.validation.validated and the page crashes instead of showing the run result
   - Evidence: `${orch.validation.validated ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`
34. **[high]** `pages/CognitionIntegration.tsx:170` — Route Gaps button (Autonomous Alignment card)
   - runAlign() does setAlign(await r.json()) with no r.ok check (line 47); on a 401/422/500 the payload has no gaps_routed, so align.gaps_routed.length throws and the page crashes (only network exceptions set alignErr)
   - Evidence: `align.gaps_routed.length === 0`
35. **[high]** `pages/developers/NativeAI.tsx:484` — Ensemble (all owned models) button in the native completion console
   - runEnsemble() does setEnsRes(await r.json()) with no r.ok check (line 256); an error payload has no .members, so ensRes.members.length throws while rendering and the whole Native AI page crashes
   - Evidence: `Ensemble · {ensRes.members.length} owned models in parallel`
36. **[high]** `pages/developers/NativeAI.tsx:51` — Run Swarm / Run saved-cascade buttons (Trace panel)
   - runSwarm (line 268) and runSaved (line 331) set state from await r.json() with no r.ok check; an error payload reaches <Trace> where run.trace is undefined and .map throws, crashing the page
   - Evidence: `{run.trace.map(s => (`
37. **[high]** `pages/developers/NativeAI.tsx:508` — Complete button (single native completion result card)
   - runComplete() does setCRes(await r.json()) with no r.ok check (line 240); an error payload renders as a result card with a false provenance badge reading 'in-house · undefined' (cRes.is_external undefined is falsy) and an empty output paragraph — the error is presented as a successful blank completion
   - Evidence: `<p className="text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">{cRes.output}</p>`
38. **[high]** `pages/CognitionIntegration.tsx:94` — Run cascade button (Cognitive Cascade §7 card)
   - runSolve() does setSolveRes(await r.json()) with no r.ok check (line 40) and the catch comment claims errors are 'surfaced by absent result'; a non-ok response still sets solveRes, so the result section renders with an empty 'Engines run:' line and no cascade/MJM/synthesis blocks — a blank success pane with no error shown
   - Evidence: `Engines run: <span className="text-aura">{(solveRes.engines_used || []).join(' · ')}</span>`
39. **[high]** `components/organism/SwarmIntelligence.tsx:149` — Delegate Mission to Swarm output pane
   - when the cascade endpoint is non-ok, the fallback delegate response object is dumped raw via JSON.stringify into streamOutput and rendered verbatim in the mission output pane (line 242 {streamOutput}) — the user sees an unformatted JSON blob as the swarm's delivery
   - Evidence: `setStreamOutput(JSON.stringify(res.data, null, 2));`
40. **[medium]** `components/DomainTool.tsx:118` — Every domain tool's result panel (shared component) and its Copy/Download/Refine controls
   - when a 2xx response lacks the expected resultKey/deliverable field, the entire response object is JSON.stringify'd and shown as the tool's deliverable text (and saved to My Work via line 106), so provenance/metadata JSON renders as if it were the generated output
   - Evidence: `String(result[resultKey] ?? result.deliverable ?? JSON.stringify(result, null, 2))`
41. **[medium]** `pages/synthesis/GenesisJourney.tsx:181` — Genesis journey run — the My Work history record it saves (rendered in MyWork.tsx rec.output pane)
   - when no stage text can be extracted, the raw response JSON truncated mid-token at 4000 chars becomes the record's user-visible output, so My Work shows a mangled JSON dump as the journey's deliverable
   - Evidence: `output: (stages || JSON.stringify(data).slice(0, 4000)),`
42. **[medium]** `hooks/useAvatarSession.ts:233` — Avatar chat reply bubble (avatar components consume this hook)
   - the reply is taken directly from resp.data.response with no empty/undefined guard; a 2xx response with a missing or empty response field pushes a blank assistant bubble (content undefined/'' ) and still sets aiStatus 'online', so the user gets a silent empty answer
   - Evidence: `const replyText: string = resp.data.response;`
   
   _Scanner summary:_ Scanned all pages/ and components/ of apps/workstation-superapp/src for incoherent output renders. The dominant defect pattern is setState(await r.json()) with no r.ok check feeding result panes: five paths hard-crash the page when the backend returns an error payload (Deliverables produce/regenerate, TransformationDashboard orchestrate, CognitionIntegration align, NativeAI ensemble and swarm/saved-run Trace), and two more render error payloads as blank 'successful' results (NativeAI complete shows an 'in-house · undefined' badge with empty output; CognitionIntegration solve shows an empty 'Engines run:' pane). Three raw-JSON-as-content renders: SwarmIntelligence dumps JSON.stringify(res.data) into the mission output pane on its fallback path, DomainTool falls back to stringifying the whole response as the deliverable text, and GenesisJourney saves a 4000-char JSON slice as the My Work output. One unguarded data.response (avatar chat) can render an empty assistant bubble while reporting the AI online. Well-guarded pages (ForgePipeline, ComplianceChecker, Generator, IntelligenceLab, BusinessPlan, VSBEconomy, ReactorStudio, BoardOfDirectors, HeartbeatMonitor, SSE studios) and intentional raw-JSON inspectors (BTOCatalog expanded view, VSBCockpit governance mono line) were not flagged.

## Raw-anchor exports/previews (bypass the bearer layer → 401 under auth)
43. **[CONFIRMED]** `pages/synthesis/GenesisJourney.tsx:803` — "Open the live site" link on the generated Website card (Genesis journey, §13 increment 2)
   - Raw anchor navigates to site.preview = /api/v1/vsb/{id}/website/page/index (agentic_core/api/vsb.py:586). A plain new-tab navigation carries no Authorization header — the route depends on get_current_user (vsb.py:616) which raises 401 without a bearer (auth/core.py:189-194) — so under AUTH_ENABLED=true the new tab shows a 401 JSON error instead of the generated site.
   - Evidence: `<a href={site.preview} target="_blank" rel="noreferrer"`
44. **[high]** `pages/synthesis/GenesisJourney.tsx:833` — "Open the web app" link on the generated Web app card (Genesis journey, §13 increment 3)
   - Raw anchor to webapp.preview = /api/v1/vsb/{id}/webapp/page/index (vsb.py:745); the webapp file route (vsb.py:775) requires get_current_user, so the bearer-less browser navigation 401s under auth — the control dead-ends in an error tab.
   - Evidence: `<a href={webapp.preview} target="_blank" rel="noreferrer"`
45. **[high]** `pages/synthesis/GenesisJourney.tsx:865` — "Open the phone app" link on the generated PWA card (Genesis journey, §13 increment 4)
   - Raw anchor to pwa.preview = /api/v1/vsb/{id}/mobile/page/index (vsb.py:880); the mobile file route (vsb.py:910) requires get_current_user, so the navigation 401s under auth and the installable-PWA preview never opens.
   - Evidence: `<a href={pwa.preview} target="_blank" rel="noreferrer"`
46. **[high]** `pages/projects/ProjectsHub.tsx:423` — "Download" button on each saved project output card
   - Download link built from the response field out.download_url = /api/v1/synthesis/download/{output_id} (agentic_core/projects/api.py:157) as a raw <a download> anchor — it skips the patched window.fetch bearer injection (lib/auth.ts:60-71). It only works today because GET /api/v1/synthesis/download/{output_id} (synthesis/api.py:374) carries NO auth dependency, i.e. outputs are anonymously fetchable under AUTH_ENABLED=true; the moment that route gets the get_current_user guard its siblings have, this control dead-ends 401. Every other export in the app was migrated to the downloadExport helper for exactly this (W338, Deliverables.tsx:257).
   - Evidence: `href={out.download_url}                   download`
47. **[high]** `pages/synthesis/SynthesisStudio.tsx:274` — Per-result format download buttons (line 467) and the history-item download button (line 356) in Synthesis Studio
   - handleDownload programmatically clicks an anchor whose href is the response field result.output_url = /api/v1/synthesis/download/{output_id} (from the SSE done event, synthesis/api.py:363) — same raw-anchor bearer bypass as ProjectsHub: no Authorization header is attached, and the download only succeeds because that backend route is currently unauthenticated; under a consistently-guarded backend the button becomes a silent 401 dead click (no error handling on the anchor path).
   - Evidence: `a.href = result.output_url;     a.download = `${title}.${fmt}`;`
   
   _Scanner summary:_ Scanned apps/workstation-superapp/src for raw /api export/download paths that bypass the patched window.fetch bearer layer (lib/auth.ts installAuth). Found 5 defects: three GenesisJourney preview anchors (Open the live site / web app / phone app) navigate directly to /api/v1/vsb/{id}/*/page/index routes that require get_current_user and therefore 401 in the new tab under AUTH_ENABLED=true; and two synthesis-output download controls (ProjectsHub saved-output Download anchor, SynthesisStudio handleDownload used by the result and history download buttons) build raw <a download> anchors from the response field download_url/output_url (/api/v1/synthesis/download/{id}), skipping bearer injection — these currently function only because that one backend route uniquely lacks an auth dependency, which also means synthesis outputs are anonymously downloadable under auth. All other download/export code paths verified clean: they either build blobs from local content or use the lib/download fetch->blob helpers (downloadExport/openExport), which are the intended W338 pattern.


Total: 47 findings + 1 endpoint break. Fix in ledger order within each class; the Change Control
Agency cluster and the fabricated-success handlers are the most material (governance surface dead +
honesty violations).
