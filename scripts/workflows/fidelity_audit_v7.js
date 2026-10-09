// Workstation IDBO — the six-region vision-fidelity assessment, TIERED EDITION (v7).
// A Claude Code *Workflow* script (see the Workflow tool / workflow-authoring reference), not a Node program.
//
// WHY THIS FILE EXISTS (FU-418, W590). MILESTONE M1 is mandated before any P2–P4 item and its bar is a
// standing TIER-1 count of 0 — and until now the milestone could not be re-run from this repository. The only
// committed workflow was fidelity_audit_v3.js, whose schemas carry NO TIER, while render_fidelity_ledger.py
// computes the M1 measure from exactly that field (standing_tier reads a verdict's `corrected_tier`, else the
// finding's `tier`). A run of v3 therefore produced a ledger in which every standing tier was None and the
// milestone could not be scored at all. The tiered instrument that produced v4 (W474), v5 (W476) and v6
// (W572) was never committed: W572's commit 93f51c95 shipped ten files — the ledger, the v5 archive, the
// prompt, the register, the test file, the renderer, blinds — and no workflow script. So the instrument that
// produced the standing count of 20 existed only in that session's transcript.
//
// NOT HARDCODED, DELIBERATELY. v3 pinned the HEAD, the date and the port into its prompt text, so re-running
// it meant editing it first, and an un-edited re-run would have told six assessors they were auditing a commit
// from weeks earlier. Everything that changes per run comes in through `args`:
//   Workflow({ scriptPath: 'scripts/workflows/fidelity_audit_v7.js',
//              args: { base: 'http://127.0.0.1:8031', head: '<short sha>', date: '2026-10-05' } })
//
// HOW TO RUN. Boot a FRESH backend from HEAD on a scratch DATA_DIR with AI_DISABLE_LOCAL=1 (that mirrors CI
// and is NOT the shipped default: with the flag unset and Ollama discoverable the gateway serves from the
// local model — the flag is what makes floor-disclosure assessable). Point `base` at it. Then, after the run:
//   python scripts/refutation_gate.py after --result <result.json>      # the agents all finished
//   python scripts/render_fidelity_ledger.py <result.json> docs/VISION_FIDELITY_LEDGER.md <HEAD> <date> <port> 7 W<round>
// and regenerate the prompt's <ledger> block from it. A fidelity verdict is dated the day it ran.
//
// WHAT THIS EDITION IS NOT. W572 ran SIXTY-SIX agents over these six regions; this is TWELVE (one assessor and
// one refuter per region). It is the faithful shape — region briefs, the ten-finding cap, an independent
// refuter defaulting to refuted — at a smaller agent count, and that difference must be stated wherever its
// number is compared with v6's. A lower Tier-1 count from a smaller instrument is NOT evidence of progress.
// The ledger already warns that each edition is "a fourth measurement rather than a score on the third"
// because the surfaces sampled differ; from v7 the INSTRUMENT differs too, and the agent count belongs beside
// the count in anything that compares them.

export const meta = {
  name: 'fidelity-audit-v7-tiered',
  description: 'MILESTONE M1: audit the current state against the vision — six regions against a booted HEAD, every finding tiered and adversarially refuted',
  phases: [{ title: 'Assess' }, { title: 'Refute' }],
}

const A = (typeof args === 'object' && args) || {}
const BASE = A.base || 'http://127.0.0.1:8024'
const HEAD = A.head || 'UNSTATED'
const DATE = A.date || 'UNSTATED'
if (HEAD === 'UNSTATED' || DATE === 'UNSTATED') {
  // A fidelity verdict is dated the day it ran and names the commit it ran against. An audit that cannot say
  // which commit it assessed is not a measurement, so this refuses rather than producing an unattributable one.
  throw new Error('fidelity_audit_v7 needs args {base, head, date}: an audit that cannot name the commit it ran against is not a measurement')
}

const TIERS = `
TIER — AND THIS IS THE AXIS MILESTONE M1 IS SCORED ON, so it carries as much weight as the verdict:
  1  A TRUTH DEFECT ON A REACHED SURFACE. The system tells a user something untrue, fabricates a figure, or
     certifies what it could not assess. "Reached" means a person actually gets there — an API-only surface's
     reached form is its response body and the stored record.
  2  AN INVISIBLE SHORTFALL. It is partial, and the surface does NOT say so.
  3  A CAPABILITY GAP THAT IS DISCLOSED, or a surface nobody reaches.
  0  DELIVERED — no tier. Use 0 only with verdict DELIVERED.
THREE THINGS THAT ARE NOT TIER 1, because each has been wrongly tiered before:
  · "no model ran" is the ENVIRONMENT (AI_DISABLE_LOCAL=1), not a defect. What IS assessable is whether the
    surface SAYS the floor served it. A surface that discloses the floor honestly is not misleading anyone.
  · an OMISSION is not an assertion. A blank field discloses nothing untrue; a field asserting an outcome the
    platform did not produce does.
  · a shortfall the surface itself states is tier 3, however large. The tier is about what a reader is told,
    not about how much is missing.
Give why_this_tier for EVERY finding: the specific sentence or figure a reader is shown, and why that lands on
the tier you chose rather than the one above or below it.`

const COMMON = `
Repo: C:/Users/rehan/Workstation (HEAD ${HEAD}, ${DATE}). A backend booted from HEAD is LIVE at
${BASE} (single-user mode, AUTH off, AI_DISABLE_LOCAL=1 -> only the deterministic native floor serves
model calls — that is the environment, not a defect; what IS assessable is whether every floor-served
surface DISCLOSES it honestly). The built frontend is served by the same backend at ${BASE}/ (use
curl for routes; read apps/workstation-superapp/src for what the UI renders — you cannot drive a
browser, so reason from the source about what a user sees, and say so).
THE VISION is docs/WORKSTATION_IDBO_WHOLE_VISION.md — read YOUR region's sections in full, plus §1
and §15 for the principles. APPENDIX A (the Quran Education Platform, the Religion domain's flagship)
is in scope for R1 and R5. Its A.9 lists SIX things the inherited QEP vision assumes that §11
FORBIDS — recitation scoring, generated Qur'an Arabic, translation of sacred text, emotion
inference, Fitrah-as-measurement, and an AI Ask-a-Scholar. Those are RATIFIED BOUNDARIES, not
gaps: never report them MISSING or STUB. A surface that refuses one of them, and says so, is
DELIVERED. A.12's five Owner rulings are likewise open by decision, not by neglect. A.10 lists
what the appendix deliberately EXCLUDES (the source repos' 2025 technology, service architecture,
19-phase roadmap, methodology and every status claim they made) — never report an excluded item
as a shortfall, and never treat the long-form QEP document's technology or roadmap parts as a
vision claim. YOU ARE BARRED from four sources: the vision's own §16, docs/VISION_FIDELITY_LEDGER.md
(the PREVIOUS edition — reading it would make this a review of it rather than a fresh measurement),
docs/AUTONOMOUS_PROGRESS.md (a record of intent, not proof), and the delivery plan's own DONE
markers in docs/FABLE_DELIVERY_PROMPT.md (an item marked done is a claim to be tested, not evidence).
Assess the SYSTEM: execute routes, read handlers and components, count stores.
Verdict vocabulary — DELIVERED (works as the vision says, verified by execution); PARTIAL (works
with a shortfall — say whether the shortfall is DISCLOSED to the user at the surface); API_ONLY
(backend exists, no UI reaches it); STUB (a surface that pretends); MISSING (nothing implements it);
DOC_OVERCLAIM (the vision or a canon doc claims more than the system does).
${TIERS}
Your job is the GAP that remains, but report DELIVERED where you verified it — the honest picture needs both.
Up to 10 findings, most consequential first (rank by how much a real person is misled or blocked). The CAP IS
TEN AND THAT IS NOT THE SIZE OF THE GAP: if you hit it, say so in region_summary, because a reader must not
read ten as "all there was". Set unlisted_findings to the NUMBER of further gaps you found and could not
list (0 if you listed everything you found).
STATE YOUR COVERAGE. In surfaces_exercised list every API route you actually CALLED (as "METHOD /path", the
route template, not the filled-in id) and every page or component file you actually READ (repo-relative
path). Only what you executed or opened — not what you know exists. A surface you did not reach is not a
clean surface, and this list is how a reader tells the two apart.
EVERY finding's \`section\` is its ONE-LINE TITLE — a sentence naming what is wrong, not a section number.
It becomes the finding's heading and is the only handle a register row or a reader has on it.`

const FINDINGS = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  section: { type: 'string' }, verdict: { type: 'string' },
  tier: { type: 'number' }, why_this_tier: { type: 'string' },
  vision_claim: { type: 'string' }, observed: { type: 'string' }, evidence: { type: 'string' },
  disclosed_to_user: { type: 'string' }, severity: { type: 'string' }, smallest_honest_fix: { type: 'string' } },
  required: ['section', 'verdict', 'tier', 'why_this_tier', 'vision_claim', 'observed', 'evidence'] } },
  region_summary: { type: 'string' }, hit_the_cap: { type: 'boolean' },
  unlisted_findings: { type: 'number' },
  surfaces_exercised: { type: 'object', properties: {
    routes: { type: 'array', items: { type: 'string' } },
    files: { type: 'array', items: { type: 'string' } } }, required: ['routes', 'files'] } },
  required: ['findings', 'region_summary', 'hit_the_cap', 'unlisted_findings', 'surfaces_exercised'] }

const VERDICTS = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
  index: { type: 'number' }, refuted: { type: 'boolean' }, reproduced: { type: 'boolean' },
  corrected_verdict: { type: 'string' }, corrected_tier: { type: 'number' },
  reason: { type: 'string' }, evidence: { type: 'string' } },
  required: ['index', 'refuted', 'reproduced', 'corrected_verdict', 'corrected_tier', 'reason'] } } },
  required: ['verdicts'] }

const REGIONS = [
  { key: 'R1', title: '§10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution',
    brief: 'Assess §10 (every solution specifically designed·modelled·simulated·optimised·ranked; best-in-class; verified·tested·validated) and §11 (live compliance engines integrated into every workflow; the faith-content constitution: Quran text never AI-generated, sourced-only, recitation never scored, floor never presented as scholarship). Execute: a deliverable via /api/v1/deliverables/produce, the QMS routes under /api/v1/vbs/qms/*, the compliance screen, and the QEP routes under /api/v1/qep/* and the religion domain (tafsir, translation refusal, hifz, written recall). Read GenesisJourney.tsx, Deliverables.tsx, QEPStudio.tsx, ReligionHub.tsx, QEPReligionHub.tsx for what a user sees. Assess QEP against vision APPENDIX A (A.6 features, A.9 constitutional deltas, A.10 exclusions, A.11 measured status).' },
  { key: 'R2', title: '§4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS',
    brief: 'Assess each of §4.1-§4.10 and §13 (the canonical output = a living VSB IDBO repository integrating Website + Web app + Phone app). Execute a Genesis journey (/api/v1/genesis/*), /establish, the VSB routes (/api/v1/vsb/*), ship/export/repo routes including /api/v1/vsb/{id}/repo and its file and zip endpoints; read GenesisJourney.tsx, VSBCockpit.tsx, the ship/repo generators. Count stages that contain the USER\'S OWN problem vs the engine\'s scaffold (the W434 lesson). Is there ONE gated lifecycle? What does an "established" VSB actually contain and do?' },
  { key: 'R3', title: '§5 + §17.3 + §17.4 — the living organisation (Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order), the living business system layers, the three integration modes',
    brief: 'Assess the org chain, arms-length Change Control, the Chief-owned Business Plan opening with Executive Summary·Concept·Vision, Strategy + living Roadmap, the Board pack, review gates (Mode 3), the digital-twin Chief. Execute /api/v1/board/* (including /chief/model), /api/v1/business-plan/*, /api/v1/swarm/cascade, /api/v1/cca/*, /api/v1/vsb/{id}/board-pack and review-gates, and the §17.3 cadence at /api/v1/organism/cadence; read BoardOfDirectors.tsx, CEOChat.tsx, SwarmIntelligence.tsx, LivingOrganisationHub.tsx, AgentHubPanel.tsx.' },
  { key: 'R4', title: '§6 + §7 + §17.2 — the native AI mandate (own swarm·models·orchestration), the reconfigurable resource fabric, the seven biomimetic layers',
    brief: 'Assess: is the AI genuinely native/in-house-first with external providers optional (read agentic_core/ai/gateway.py, native/, the /api/v1/native-ai/* routes incl. models/complete/primitives and the Primitive Console page NativeAI.tsx)? Are cascades bespoke per solution/founder and USER-reconfigurable (Synthesis Lab, Build-to-Order, Forge, the NativeAI.tsx cascade designer at /native-ai?focus=cascade-designer, ResourceFabric.tsx)? Which of the seven layers (§17.2) have real implementations vs names (organism/*, nervous, immune, self-healing, genome, biobus, heartbeat, evolution)? Is provenance (served_by/is_external) honest everywhere output reaches a user — including SSE stage events and the durable record, not only the final response?' },
  { key: 'R5', title: '§1-§3, §3A, §9, §14, §15, §17.1 — the offerings (Domains working + the end-to-end lifecycle), the multimodal enterprise-aware avatar/UX, democratisation, the founding principles, the 4×6×4 grid',
    brief: 'Assess: do the six Domains each offer real in-house-AI-mediated tools (execute each domain\'s /services + a tool per domain under /api/v1/{religion,science,education,law,employment,care}/*; read the *Hub.tsx pages)? The avatar (multimodal, enterprise-aware, voice) — /api/v1/avatar/*, components/avatar/*. Accessibility/all-language/personalisation (i18n, the explicit user profile W428). The 4 Realms × 6 Domains × 4 Products grid: agentic_core/taxonomy.py + apps/workstation-superapp/src/lib/taxonomy.ts + the products catalogue — does the product expose the grid? (W505: configs/realms.yaml was DELETED as part of P2.5 — it held a third, drifted vocabulary matching neither the four realms nor the six domains, and no code read it. Do not look for it.) Principle 6 (never fabricate; label simulation) — spot-check surfaces for fabricated figures. For the Religion domain assess offering-1 depth against vision APPENDIX A.1/A.6.' },
  { key: 'R6', title: '§8 + §12 + §17.5 — the biomimetic living organism (self-running, defending, healing, learning, improving), the economic organism (VSB as hybrid Waqf/Trust/Multinational), the ten architecture invariants',
    brief: 'Assess the organism: heartbeat (/api/v1/heartbeat/*), homeostasis, self-healing, immune, sovereign evolution, survival instinct — does it RUN itself (read heartbeat/, organism/, the OrganismHub + Anatomy pages)? Does a beat REPORT what it could not do, or only what it did? The economy: /api/v1/economy/* (cycle, waterfall, ledger, board-pack, transfer, close-period, ventures, charity, owner-payments), the 6-stage waterfall, virtual-WST honesty, double-entry integrity (post a cycle, a transfer, a close — check the books balance), charity intelligence with the Owner\'s directives. The ten invariants §17.5: check each against code (user isolation, GaaS gate on every output, append-only DCS, arms-length, twin pre-validation, torch optionality, single router mount, signal-bus atomicity, plan ≤5-min staleness, KPI gate).' },
]

const results = await pipeline(REGIONS,
  r => agent(COMMON + `\nYOUR REGION (${r.key}): ${r.title}\n${r.brief}`,
    { label: `assess:${r.key}`, phase: 'Assess', schema: FINDINGS }),
  (assessed, r) => {
    if (!assessed || !assessed.findings?.length) return { region: r.key, findings: [], verdicts: [], summary: assessed?.region_summary || '' }
    const listing = assessed.findings.map((f, i) => `[${i}] ${f.section} — ${f.verdict} · tier ${f.tier}: claim="${f.vision_claim}" observed="${f.observed}" evidence="${f.evidence}" disclosed=${f.disclosed_to_user || '?'} why_this_tier="${f.why_this_tier}"`).join('\n')
    return agent(COMMON + `\nYOU ARE THE REFUTER for region ${r.key} (${r.title}). An assessor produced these findings:\n${listing}\n\nAttack EVERY finding. Default to refuted=true unless you personally reproduce the gap (execute the route, read the code, count the store). SAY WHICH IT WAS ON EVERY INDEX: set reproduced=true ONLY if you personally reproduced the gap the finding describes - whatever you then decide about its verdict or its tier - and reproduced=false if you could not, or found the capability delivered. A finding you reproduced and merely re-labelled or re-tiered STANDS at your tier; one you could not reproduce does not. The ledger counts by this field, so do not leave it to be guessed from the tier. A finding is refuted when the capability IS delivered/disclosed as the vision says, when the evidence does not support the verdict, or when the verdict is the wrong one (say the corrected verdict — findings often need correcting UPWARD to DELIVERED or DOWNWARD when the assessor was too kind).\n\nAND GIVE corrected_tier ON EVERY INDEX, even when you leave it unchanged — it is the axis MILESTONE M1 is scored on, and a refuter who reports only a verdict hides a tier they moved. In v6 FOUR findings were escalated into tier 1 and the record said none had been made harsher, because direction was computed from the verdict alone; two of those had their verdict index RISE while the tier tightened. Tier the finding as YOU stand behind it after checking, against the tier definitions above, and say in \`reason\` why that tier rather than the one above or below.`,
      { label: `refute:${r.key}`, phase: 'Refute', schema: VERDICTS })
      .then(v => ({ region: r.key, findings: assessed.findings, verdicts: v?.verdicts || [], summary: assessed.region_summary, hit_the_cap: assessed.hit_the_cap, unlisted_findings: assessed.unlisted_findings, surfaces_exercised: assessed.surfaces_exercised }))
  })

return results
