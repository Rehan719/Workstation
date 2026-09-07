// Workstation IDBO — the six-region vision-fidelity assessment (W446, ledger v3).
// A Claude Code *Workflow* script (see the Workflow tool / workflow-authoring reference), not a Node program.
// HOW TO RUN: boot a FRESH backend from HEAD on a scratch DATA_DIR (AI_DISABLE_LOCAL=1 mirrors CI and the
// shipped default), set BASE below to it, then Workflow({script: <this file's contents>}). Every finding is
// adversarially refuted (default refuted=true; a refuter must REPRODUCE a gap to let it stand).
// RENDER: python scripts/render_fidelity_ledger.py <result.json> docs/VISION_FIDELITY_LEDGER.md <HEAD> <date>
// Re-run at every milestone (delivery-prompt rule 27) — a fidelity verdict is dated the day it ran.

export const meta = {
  name: 'w446-fidelity-audit-v3',
  description: 'Phase 2: audit the current state against the vision — six regions assessed against a booted HEAD, every finding adversarially refuted',
  phases: [{ title: 'Assess' }, { title: 'Refute' }],
}
const BASE = 'http://127.0.0.1:8024'
const COMMON = `
Repo: C:/Users/rehan/Workstation (HEAD 06c51109, 2026-09-04). A backend booted from HEAD is LIVE at
${BASE} (single-user mode, AUTH off, AI_DISABLE_LOCAL=1 → only the deterministic native floor serves
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
vision claim. YOU ARE BARRED from three sources: the vision's own §16, docs/
VISION_FIDELITY_LEDGER.md (stale v2), and docs/AUTONOMOUS_PROGRESS.md (a record of intent, not
proof). Assess the SYSTEM: execute routes, read handlers and components, count stores.
Verdict vocabulary — DELIVERED (works as the vision says, verified by execution); PARTIAL (works
with a shortfall — say whether the shortfall is DISCLOSED to the user at the surface); API_ONLY
(backend exists, no UI reaches it); STUB (a surface that pretends); MISSING (nothing implements it);
DOC_OVERCLAIM (the vision or a canon doc claims more than the system does). Your job is the GAP
that remains, but report DELIVERED where you verified it — the honest picture needs both. Up to 10
findings, most consequential first (rank by how much a real person is misled or blocked).`
const FINDINGS = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  section: { type: 'string' }, verdict: { type: 'string' }, vision_claim: { type: 'string' },
  observed: { type: 'string' }, evidence: { type: 'string' }, disclosed_to_user: { type: 'string' },
  severity: { type: 'string' }, smallest_honest_fix: { type: 'string' } },
  required: ['section', 'verdict', 'vision_claim', 'observed', 'evidence'] } },
  region_summary: { type: 'string' } }, required: ['findings', 'region_summary'] }
const VERDICTS = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
  index: { type: 'number' }, refuted: { type: 'boolean' }, corrected_verdict: { type: 'string' },
  reason: { type: 'string' }, evidence: { type: 'string' } },
  required: ['index', 'refuted', 'reason'] } } }, required: ['verdicts'] }
const REGIONS = [
  { key: 'R1', title: '§10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution',
    brief: 'Assess §10 (every solution specifically designed·modelled·simulated·optimised·ranked; best-in-class; verified·tested·validated) and §11 (live compliance engines integrated into every workflow; the faith-content constitution: Quran text never AI-generated, sourced-only, recitation never scored, floor never presented as scholarship). Execute: a deliverable via /api/v1/deliverables/produce, the QMS routes under /api/v1/vbs/qms/*, the compliance screen, and the QEP routes under /api/v1/qep/* and the religion domain (tafsir, translation refusal, hifz, written recall). Read GenesisJourney.tsx, Deliverables.tsx, QEPStudio.tsx, ReligionHub.tsx for what a user sees. Assess QEP against vision APPENDIX A (A.6 features, A.9 constitutional deltas, A.10 exclusions, A.11 measured status).' },
  { key: 'R2', title: '§4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS',
    brief: 'Assess each of §4.1-§4.10 and §13 (the canonical output = a living VSB IDBO repository integrating Website + Web app + Phone app). Execute a Genesis journey (/api/v1/genesis/*), /establish, the VSB routes (/api/v1/vsb/*), ship/export routes; read GenesisJourney.tsx, VSBCockpit.tsx, the ship/repo generators. Count stages that contain the USER\'S OWN problem vs the engine\'s scaffold (the W434 lesson). Is there ONE gated lifecycle? What does an "established" VSB actually contain and do?' },
  { key: 'R3', title: '§5 + §17.3 + §17.4 — the living organisation (Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order), the living business system layers, the three integration modes',
    brief: 'Assess the org chain, arms-length Change Control, the Chief-owned Business Plan opening with Executive Summary·Concept·Vision, Strategy + living Roadmap, the Board pack, review gates (Mode 3), the digital-twin Chief. Execute /api/v1/board/*, /api/v1/business-plan/*, /api/v1/swarm/cascade, /api/v1/cca/*, /api/v1/vsb/{id}/board-pack and review-gates; read BoardOfDirectors.tsx, CEOChat.tsx, SwarmIntelligence.tsx, LivingOrganisationHub.tsx, AgentHubPanel.tsx.' },
  { key: 'R4', title: '§6 + §7 + §17.2 — the native AI mandate (own swarm·models·orchestration), the reconfigurable resource fabric, the seven biomimetic layers',
    brief: 'Assess: is the AI genuinely native/in-house-first with external providers optional (read agentic_core/ai/gateway.py, native/, the /api/v1/native-ai/* routes incl. models/complete/primitives and the Primitive Console page NativeAI.tsx)? Are cascades bespoke per solution/founder and USER-reconfigurable (Synthesis Lab, Build-to-Order, Forge, VisualAgentComposer.tsx, ResourceFabric.tsx)? Which of the seven layers (§17.2) have real implementations vs names (organism/*, nervous, immune, self-healing, genome, biobus, heartbeat, evolution)? Is provenance (served_by/is_external) honest everywhere output reaches a user?' },
  { key: 'R5', title: '§1-§3, §3A, §9, §14, §15, §17.1 — the offerings (Domains working + the end-to-end lifecycle), the multimodal enterprise-aware avatar/UX, democratisation, the founding principles, the 4×6×4 grid',
    brief: 'Assess: do the six Domains each offer real in-house-AI-mediated tools (execute each domain\'s /services + a tool per domain under /api/v1/{religion,science,education,law,employment,care}/*; read the *Hub.tsx pages)? The avatar (multimodal, enterprise-aware, voice) — /api/v1/avatar/*, components/avatar/*. Accessibility/all-language/personalisation (i18n, the explicit user profile W428). The 4 Realms × 6 Domains × 4 Products grid: taxonomy.py + configs/realms.yaml + the products catalogue — does the product expose the grid? Principle 6 (never fabricate; label simulation) — spot-check surfaces for fabricated figures. For the Religion domain assess offering-1 depth against vision APPENDIX A.1/A.6.' },
  { key: 'R6', title: '§8 + §12 + §17.5 — the biomimetic living organism (self-running, defending, healing, learning, improving), the economic organism (VSB as hybrid Waqf/Trust/Multinational), the ten architecture invariants',
    brief: 'Assess the organism: heartbeat (/api/v1/heartbeat/*), homeostasis, self-healing, immune, sovereign evolution, survival instinct — does it RUN itself (read heartbeat/, organism/, the OrganismHub + Anatomy pages)? The economy: /api/v1/economy/* (cycle, waterfall, ledger, board-pack, transfer, close-period, ventures, charity, owner-payments), the 6-stage waterfall, virtual-WST honesty, double-entry integrity (post a cycle, a transfer, a close — check the books balance), charity intelligence with the Owner\'s directives. The ten invariants §17.5: check each against code (user isolation, GaaS gate on every output, append-only DCS, arms-length, twin pre-validation, torch optionality, single router mount, signal-bus atomicity, plan ≤5-min staleness, KPI gate).' },
]
const results = await pipeline(REGIONS,
  r => agent(COMMON + `\nYOUR REGION (${r.key}): ${r.title}\n${r.brief}`,
    { label: `assess:${r.key}`, phase: 'Assess', schema: FINDINGS }),
  (assessed, r) => {
    if (!assessed || !assessed.findings?.length) return { region: r.key, findings: [], verdicts: [], summary: assessed?.region_summary || '' }
    const listing = assessed.findings.map((f, i) => `[${i}] §${f.section} — ${f.verdict}: claim="${f.vision_claim}" observed="${f.observed}" evidence="${f.evidence}" disclosed=${f.disclosed_to_user || '?'}`).join('\n')
    return agent(COMMON + `\nYOU ARE THE REFUTER for region ${r.key} (${r.title}). An assessor produced these findings:\n${listing}\n\nAttack EVERY finding. Default to refuted=true unless you personally reproduce the gap (execute the route, read the code, count the store). A finding is refuted when the capability IS delivered/disclosed as the vision says, when the evidence does not support the verdict, or when the verdict is the wrong one (say the corrected verdict — findings often need correcting UPWARD to DELIVERED or DOWNWARD when the assessor was too kind). For each index give refuted, corrected_verdict (the verdict you stand behind after checking), reason, evidence.`,
      { label: `refute:${r.key}`, phase: 'Refute', schema: VERDICTS })
      .then(v => ({ region: r.key, findings: assessed.findings, verdicts: v?.verdicts || [], summary: assessed.region_summary }))
  })
return results.filter(Boolean)