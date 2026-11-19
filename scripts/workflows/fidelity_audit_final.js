// Workstation IDBO — THE FINAL AUDIT (P5.22): uncapped and census-partitioned.
// A Claude Code *Workflow* script (see the Workflow tool / workflow-authoring reference), not a Node program.
//
// WHAT IT IS. The Owner ruled on 2026-10-12 that the final audit is UNCAPPED and CENSUS-PARTITIONED, built and guarded
// in its own round, calibrated first, and run after Phase 5 and the sign-in readiness round; on 2026-11-06 he chartered
// it as P5.22, run in BOTH configurations, the native floor and the local model. fidelity_audit_v7.js assessed six
// hand-drawn regions with a cap on findings. This assesses every slice of the census (docs/AUDIT_SLICES.json, held to
// the census by scripts/audit_census_partition.py), one assessor and one refuter per slice, and sets NO CAP: an
// assessor lists every finding it makes, and one that stops early says so (hit_the_cap, unlisted_findings), which
// leaves the audit incomplete rather than read as clean.
//
// ONE RUN IS ONE CONFIGURATION, against a backend booted from the commit it names. Run it against a backend serving
// from the floor (AI_DISABLE_LOCAL=1) and again against one serving from the local model, then join the two records,
// or one record and why the other configuration did not run:
//   python scripts/audit_surface_census.py ... > census.json
//   python scripts/audit_census_partition.py census.json docs/AUDIT_SLICES.json --surfaces > slices.json
//   Workflow({ scriptPath: 'scripts/workflows/fidelity_audit_final.js',
//              args: { base: 'http://127.0.0.1:8031', head: '<the full commit id>', date: '<YYYY-MM-DD>',
//                      configuration: 'floor', slices: <slices.json> } })                     -> floor.json
//   ... the same with configuration 'local_model', against the local model's backend         -> local_model.json
//   python scripts/audit_completeness.py record floor.json local_model.json > run.json
//   python scripts/audit_completeness.py run.json <the full commit id>      # COMPLETE, or each reason it is not
//
// NOT RUN BY THE ROUND THAT BUILT IT. It is guarded by a driven test (FidelityAuditFinal.test.ts, which runs this
// script with planted agents), it is calibrated on planted defects before it is trusted (FU-993), and running it is
// the item's own work, after the rounds the ruling names.

export const meta = {
  name: 'fidelity-audit-final',
  description: 'P5.22 - the final audit: every census slice assessed and refuted, uncapped, in one named configuration',
  phases: [{ title: 'Assess' }, { title: 'Refute' }],
}

const A = (typeof args === 'object' && args) || {}
const BASE = A.base || 'http://127.0.0.1:8024'
const HEAD = String(A.head || '')
const DATE = String(A.date || '')
const CONFIGURATION = String(A.configuration || '')
const REPO = A.repo || 'the working directory you run in (the repository root)'
const SLICES = (A.slices && Array.isArray(A.slices.slices)) ? A.slices.slices : []
const CONFIGURATIONS = ['floor', 'local_model']

//  Refused before any agent runs. An audit that cannot name the commit it measured is not a measurement; a verdict is
//  dated the day it ran; a record must say which configuration it measured; and a run handed no slices, or a slice with
//  no surface, would examine nothing and could still read as clean.
if (!/^[0-9a-f]{40}$/.test(HEAD)) {
  throw new Error('fidelity_audit_final needs args.head, the full commit id the backend was booted from: an audit that cannot name the commit it measured is not a measurement')
}
if (!/^\d{4}-\d{2}-\d{2}$/.test(DATE)) {
  throw new Error('fidelity_audit_final needs args.date (YYYY-MM-DD): a fidelity verdict is dated the day it ran')
}
if (!CONFIGURATIONS.includes(CONFIGURATION)) {
  throw new Error(`fidelity_audit_final needs args.configuration, one of ${CONFIGURATIONS.join(' or ')}: the record must say which configuration it measured`)
}
if (!SLICES.length || SLICES.some(s => !s || !s.id || !Array.isArray(s.routes) || !Array.isArray(s.pages)
                                     || s.routes.length + s.pages.length === 0)) {
  throw new Error('fidelity_audit_final needs args.slices, every slice with its surfaces (scripts/audit_census_partition.py --surfaces): it examined nothing without them, and a slice with no surface is a slice nothing assessed')
}

const SERVED = CONFIGURATION === 'floor'
  ? `AI_DISABLE_LOCAL=1, so only the deterministic native floor serves model calls. That is this configuration, not a
defect; what IS assessable is whether every floor-served surface DISCLOSES that the floor served it.`
  : `the local model serves model calls, as on the Owner's own machine. That is this configuration; what IS assessable is
whether every surface a model served says which model and build served it, and whether what it composed is held to the
same disclosures as the floor's.`

const TIERS = `
TIER — as much weight as the verdict:
  1  A TRUTH DEFECT ON A REACHED SURFACE. The system tells a user something untrue, fabricates a figure, or
     certifies what it could not assess. "Reached" means a person actually gets there — an API-only surface's
     reached form is its response body and the stored record.
  2  AN INVISIBLE SHORTFALL. It is partial, and the surface does NOT say so.
  3  A CAPABILITY GAP THAT IS DISCLOSED, or a surface nobody reaches.
  0  DELIVERED — no tier. Use 0 only with verdict DELIVERED.
THREE THINGS THAT ARE NOT TIER 1, because each has been wrongly tiered before:
  · what serves model calls is the CONFIGURATION, not a defect. What IS assessable is whether the surface SAYS
    what served it.
  · an OMISSION is not an assertion. A blank field discloses nothing untrue; a field asserting an outcome the
    platform did not produce does.
  · a shortfall the surface itself states is tier 3, however large. The tier is about what a reader is told,
    not about how much is missing.
Give why_this_tier for EVERY finding: the specific sentence or figure a reader is shown, and why that lands on
the tier you chose rather than the one above or below it.`

const COMMON = `
Repo: ${REPO} (HEAD ${HEAD}, ${DATE}). Cite files by their path RELATIVE to the repo root. A backend booted from that
commit is LIVE at ${BASE} (single-user mode, AUTH off). CONFIGURATION: ${CONFIGURATION} — ${SERVED}
The built frontend is served by the same backend at ${BASE}/ (use curl for routes; read apps/workstation-superapp/src for
what the UI renders — you cannot drive a browser, so reason from the source about what a user sees, and say so).
THE VISION is docs/WORKSTATION_IDBO_WHOLE_VISION.md — read the sections your slice's surfaces serve, plus §1 and §15 for
the principles. APPENDIX A (the Quran Education Platform) is in scope wherever your slice reaches it. Its A.9 lists SIX
things the inherited QEP vision assumes that §11 FORBIDS — recitation scoring, generated Qur'an Arabic, translation of
sacred text, emotion inference, Fitrah-as-measurement, and an AI Ask-a-Scholar. Those are RATIFIED BOUNDARIES, not gaps:
never report them MISSING or STUB. A surface that refuses one of them, and says so, is DELIVERED. A.12's five Owner
rulings are open by decision, not by neglect, and what A.10 excludes is never a shortfall. YOU ARE BARRED from four
sources: the vision's own §16, docs/VISION_FIDELITY_LEDGER.md and its earlier editions (reading one would make this a
review of it rather than a fresh measurement), docs/AUTONOMOUS_PROGRESS.md (a record of intent, not proof), and the
delivery plan's own DONE markers in docs/FABLE_DELIVERY_PROMPT.md (an item marked done is a claim to be tested).
Assess the SYSTEM: execute routes, read handlers and components, count stores.
Verdict vocabulary — DELIVERED (works as the vision says, verified by execution); PARTIAL (works with a shortfall — say
whether the shortfall is DISCLOSED to the user at the surface); API_ONLY (backend exists, no UI reaches it); STUB (a
surface that pretends); MISSING (nothing implements it); DOC_OVERCLAIM (the vision or a canon doc claims more than the
system does).
${TIERS}
THERE IS NO CAP. List every finding you make, most consequential first (rank by how much a real person is misled or
blocked), and report DELIVERED where you verified it — the honest picture needs both. If you have to stop before you have
listed everything you found, set hit_the_cap to true and unlisted_findings to the NUMBER you found and did not list: that
leaves this audit incomplete, which is the truth, where a short list read as complete would not be. Otherwise set
hit_the_cap to false and unlisted_findings to 0.
STATE YOUR COVERAGE. In surfaces_exercised list every API route you actually CALLED (as "METHOD /path", the route
template, not the filled-in id) and every page or component file you actually READ (repo-relative path). Only what you
executed or opened — not what you know exists. A surface of your slice you did not reach is not a clean surface, and this
list is how a reader tells the two apart.
EVERY finding's \`section\` is its ONE-LINE TITLE — a sentence naming what is wrong, not a section number.
RESIDUE. In \`residue\` list, one line each, every record your probes left in a live store (what and where), and anything
you observed that is NOT one of your findings and a person should read: a defect outside your slice, a privacy or
data-handling observation, a store that was not isolated. THIS LIST IS PRINTED IN A PUBLIC LEDGER: say what KIND of data
you saw and what kind of place held it, never its content, a person's name, or a path under a home directory. An empty
list says you left nothing and saw nothing else; it is read, so do not leave it empty by default.`

const FINDINGS = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  section: { type: 'string' }, verdict: { type: 'string' },
  tier: { type: 'number' }, why_this_tier: { type: 'string' },
  vision_claim: { type: 'string' }, observed: { type: 'string' }, evidence: { type: 'string' },
  disclosed_to_user: { type: 'string' }, severity: { type: 'string' }, smallest_honest_fix: { type: 'string' } },
  required: ['section', 'verdict', 'tier', 'why_this_tier', 'vision_claim', 'observed', 'evidence'] } },
  region_summary: { type: 'string' }, hit_the_cap: { type: 'boolean' },
  unlisted_findings: { type: 'number' },
  residue: { type: 'array', items: { type: 'string' } },
  surfaces_exercised: { type: 'object', properties: {
    routes: { type: 'array', items: { type: 'string' } },
    files: { type: 'array', items: { type: 'string' } } }, required: ['routes', 'files'] } },
  required: ['findings', 'region_summary', 'hit_the_cap', 'unlisted_findings', 'surfaces_exercised', 'residue'] }

const VERDICTS = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
  index: { type: 'number' }, refuted: { type: 'boolean' }, reproduced: { type: 'boolean' },
  corrected_verdict: { type: 'string' }, corrected_tier: { type: 'number' },
  defect_class: { type: 'string' },
  reason: { type: 'string' }, evidence: { type: 'string' } },
  required: ['index', 'refuted', 'reproduced', 'corrected_verdict', 'corrected_tier', 'defect_class', 'reason'] } },
  residue: { type: 'array', items: { type: 'string' } } },
  required: ['verdicts', 'residue'] }

function slicePrompt(s) {
  return `
YOUR SLICE (${s.id}): ${s.holds || 'the surfaces listed below'}
It holds ${s.routes.length} API route(s) and ${s.pages.length} page(s) of the census, and the audit is complete only when
every slice has assessed every surface it holds. Exercise each of them; a surface you could not reach is named in
region_summary, never passed over.
API ROUTES (${s.routes.length}):
${s.routes.join('\n')}
PAGES (${s.pages.length}):
${s.pages.join('\n')}`
}

function refutePrompt(s, assessed) {
  const listing = assessed.findings.map((f, i) => `[${i}] ${f.section} — ${f.verdict} · tier ${f.tier}: claim="${f.vision_claim}" observed="${f.observed}" evidence="${f.evidence}" disclosed=${f.disclosed_to_user || 'unstated'} why_this_tier="${f.why_this_tier}"`).join('\n')
  return COMMON + `
YOU ARE THE REFUTER for slice ${s.id} (${s.holds || 'its surfaces'}), in the ${CONFIGURATION} configuration. An assessor
produced these findings:
${listing}

Attack EVERY finding. Default to refuted=true unless you personally reproduce the gap against the live backend or the
source. reproduced says whether you did. Give corrected_verdict and corrected_tier for every finding, the tier YOU stand
behind, and a defect_class: availability (the surface offers a capability whose required resource is not available
here), false_statement (a statement false for another reason), missing_control (a control that should refuse, gate or
record is absent), mixed (one half availability, one half another false statement), or other. One of those five words.`
}

//  Every slice comes back as a record the completeness check reads: its id as \`region\` (the field the ledger renderer
//  reads), the configuration, the commit, and a status. A slice whose assessor or refuter returned nothing, or whose
//  stage threw, is FAILED with the reason; it is never left out, and never read as a slice with no finding.
function failed(s, error, assessed) {
  return { region: s.id, configuration: CONFIGURATION, measured_commit: HEAD, status: 'failed', error,
           findings: (assessed && assessed.findings) || [], verdicts: [] }
}

const results = await pipeline(SLICES,
  s => agent(COMMON + slicePrompt(s), { label: `assess:${s.id}`, phase: 'Assess', schema: FINDINGS }),
  (assessed, s) => {
    if (!assessed) return failed(s, 'the assessor returned nothing, so nothing in this slice was assessed')
    const done = { region: s.id, configuration: CONFIGURATION, measured_commit: HEAD, status: 'ok',
                   findings: assessed.findings || [], summary: assessed.region_summary || '',
                   hit_the_cap: assessed.hit_the_cap, unlisted_findings: assessed.unlisted_findings,
                   surfaces_exercised: assessed.surfaces_exercised, residue: assessed.residue || [] }
    if (!done.findings.length) return { ...done, verdicts: [], refuter_residue: [] }
    return agent(refutePrompt(s, assessed), { label: `refute:${s.id}`, phase: 'Refute', schema: VERDICTS })
      .then(v => v ? { ...done, verdicts: v.verdicts || [], refuter_residue: v.residue || [] }
                   : failed(s, 'the refuter returned nothing, so no finding was refuted or upheld', assessed))
  })

const slices = results.map((r, i) => r || failed(SLICES[i], 'the slice was dropped before it finished: a stage threw'))
const notDone = slices.filter(r => r.status !== 'ok').map(r => r.region)
log(notDone.length
  ? `${notDone.length} of ${slices.length} slice(s) did not complete (${notDone.join(', ')}); the audit is not complete until each is run again`
  : `all ${slices.length} slice(s) returned, in the ${CONFIGURATION} configuration; completeness is decided by scripts/audit_completeness.py`)

return { measured_commit: HEAD, date: DATE, configuration: CONFIGURATION, slices }
