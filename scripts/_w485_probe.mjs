// W485 (P1.18: FU-097, FU-101, FU-128) — a veto stops the journey, a pack says whose text it
// screened, and exported text carries its provenance. Fresh backend + the page in a real browser.
//   node scripts/_w485_probe.mjs http://127.0.0.1:8092
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8092';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const post = async (p, b) => {
  const r = await fetch(`${BASE}${p}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(b) });
  return { status: r.status, body: await r.json().catch(() => null) };
};
const dismissTour = async (p) => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(400);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), null, { timeout: 10000 }).catch(() => {});
};

// ── the veto stops the journey ──
const blocked = (await post('/api/v1/genesis/journey', {
  problem: 'A fine wine subscription club with casino nights for members', domain: 'commerce',
  establish: true, name: 'W485 probe blocked',
})).body;
const s5 = blocked.stage_5_model_simulate_rank;
check('R1.3 nothing is selected when every candidate is vetoed',
  s5.selected === null && s5.blocked_by_screen === true && (s5.vetoed || []).length > 0);
check('R1.3 the journey status says it was blocked', blocked.status === 'blocked_by_screen');
check('R1.3 no body was composed from the vetoed approach',
  ['phase_2_design_development', 'stage_7_operational_intelligence', 'phase_3_commercialisation']
    .every(k => /every candidate was vetoed/.test(blocked[k] || '')));
check('R1.3 nothing was established', (blocked.established_vsb || {}).blocked_by_screen === true);
check('R1.3 the three uncalled stages are NOT RUN, not floor-served',
  ['design', 'operations', 'commercialisation']
    .every(k => blocked.stage_verifications[k].ran === false && blocked.stage_verifications[k].verified === null));
check('R1.3 nothing is attested about a journey that did not run',
  ['optimised', 'ranked', 'modelled', 'simulated']
    .every(k => blocked.quality_assurance.quality.bar_measured.criteria[k].attested === false));
check('R1.3 the QMS gate has nothing to measure',
  blocked.quality_assurance.quality.qms_gate_passed === null);
check('R1.3 no deliverable is claimed', /No deliverable/.test(blocked.deliverable));

// the establish WRITERS refuse a vetoed candidate — both of them
const vetoed = { id: 'c1', screen: { disqualified: true, verdicts: { sharia_halal: 'fail' } } };
const e1 = await post('/api/v1/genesis/establish', { problem: 'x', domain: 'commerce', selected_candidate: vetoed });
const e2 = await post('/api/v1/genesis/establish/stream', { problem: 'x', domain: 'commerce', selected_candidate: vetoed });
check('(refutation) both establish writers refuse a vetoed candidate',
  e1.status === 409 && e2.status === 409 && e1.body.detail.error === 'blocked_by_screen');

// an ELIGIBLE journey is unaffected
const ok = (await post('/api/v1/genesis/journey', {
  problem: 'Elderly residents struggle to repair small household appliances', domain: 'community',
})).body;
check('an eligible journey still completes',
  ok.status === 'complete' && ok.stage_5_model_simulate_rank.selected
  && ok.stage_5_model_simulate_rank.blocked_by_screen === false);

// ── the board pack says whose text it screened ──
const est = (await post('/api/v1/genesis/establish', {
  problem: 'A community appliance repair service for elderly residents', domain: 'community',
  name: 'W485 Probe Circle',
})).body;
const vid = est.vsb_id || (est.entity || {}).vsb_id;
const pack = (await post(`/api/v1/vsb/${vid}/board-pack`, {})).body;
const pc = ((pack.quality_assurance || {}).quality || {}).compliance || {};
check('R2.3 the pack says WHOSE text the §11 verdict is about', !!pc.screened_subject);
check('R2.3 a pending pack reports its own verdict as not assessable',
  !/^narrative pending/.test(pack.narrative) || (pc.assessable === false && pc.overall === null));
check('R2.3 the §10 bar never certifies the pack compliant off that screen',
  ['compliant', 'safe'].every(k => pack.quality_assurance.quality.bar_measured.criteria[k].met !== true));
check('R2.3 the ENTITY\'s own §11 verdict travels on the pack, with its basis',
  !!pack.entity_compliance && 'verdict' in pack.entity_compliance
  && !!pack.entity_compliance.basis && pack.entity_compliance.known === true);

// ── the page ──
const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', e => errors.push(String(e)));
await page.goto(`${BASE}/genesis`, { waitUntil: 'networkidle' });
await dismissTour(page);
const box = page.locator('textarea').first();
await box.fill('A fine wine subscription club with casino nights for members');
await page.locator('button:has-text("Launch Genesis Journey")').first().click();
// Wait for the RESULT, not for the button's own "Running Sovereign Journey…" label — that is
// present the moment the click lands and made this wait fire immediately.
// Wait for the RUN TO FINISH — the button returns to its idle label. Waiting on body text matched
// the button's own "Running Sovereign Journey…" and static headings, and fired immediately.
await page.waitForFunction(
  () => !/Running Sovereign Journey|Concept .{1,3} living enterprise/i.test(document.body.innerText),
  null, { timeout: 420000 });
await page.waitForTimeout(2000);
const text = await page.locator('body').innerText();
check('PAGE the blocked panel is shown', /Blocked by the .?11 screen/i.test(text));
check('PAGE the page does not say the winner is carried into Design',
  !/the winner is carried into Design/i.test(text));
check('PAGE a vetoed candidate is marked vetoed', /vetoed/i.test(text));
const estBtn = page.locator('button:has-text("Blocked — nothing to establish")').first();
check('PAGE the Establish control is blocked and says so',
  (await estBtn.isVisible().catch(() => false)) && (await estBtn.isDisabled().catch(() => false)));
const unrelated = /ws:\/\/localhost:8010|ERR_CONNECTION_REFUSED/;
check('PAGE no console errors (other than the dev streams socket)',
  errors.filter(e => !unrelated.test(e)).length === 0);
if (errors.length) console.log('   (console:', errors.slice(0, 3), ')');
await browser.close();

const passed = checks.filter(Boolean).length;
console.log(`\nPROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
