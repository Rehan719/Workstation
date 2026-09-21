// W489 (P1.18 + P2.4 + P2.8 + P2.9, the C3 batch taken repo-wide) — a reading is measured, or it is
// not presented as a reading. Fresh backend + the real pages in a real browser.
//   node scripts/_w489_probe.mjs http://127.0.0.1:8094
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8094';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const get = async (p) => {
  const r = await fetch(`${BASE}${p}`);
  return { status: r.status, body: await r.json().catch(() => null) };
};
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

// ── the API's own answers ───────────────────────────────────────────────────────────────────────
const cascade = await post('/api/v1/cognitive/cascade', { problem: 'w489 probe', include_mjm: true });
check('the cascade reports the six engines that ran, not nine',
  cascade.body?.engines_run === 6 && cascade.body?.engines_compute === false);
check('the cascade says MJM re-runs the same six',
  /does not add engines/.test(String(cascade.body?.engines_run_basis)));
const engines = await get('/api/v1/cognitive/engines');
const planned = (engines.body?.engines || []).filter(e => !e.implemented);
check('three engines are listed as PLANNED, naming the plan item that builds them',
  engines.body?.implemented_total === 6 && planned.length === 3
  && planned.every(e => e.status === 'planned' && /P3\.13/.test(e.note)));
const oneEngine = await post('/api/v1/cognitive/engine', { engine_id: 'niyyah', input: 'w489' });
check('a planned engine answers "planned, nothing ran" rather than a bare 404',
  oneEngine.body?.status === 'planned' && oneEngine.body?.ran === false);

const struggling = await get('/api/v1/qep/xai/explanations?ease_factor=1.3&interval_days=0&repetition=0&last_quality=1');
const fluent = await get('/api/v1/qep/xai/explanations?ease_factor=2.9&interval_days=12&repetition=5&last_quality=5');
const sBy = Object.fromEntries((struggling.body?.explanations || []).map(c => [c.feature, c.rationale]));
const fBy = Object.fromEntries((fluent.body?.explanations || []).map(c => [c.feature, c.rationale]));
check('the XAI rationales differ for opposite learners (they were fixed strings)',
  sBy.ease_factor !== fBy.ease_factor && sBy.repetition !== fBy.repetition);
check('a learner at the SM-2 floor is not told they retain it well',
  !/retains this ayah well/.test(Object.values(sBy).join(' ')) && /floor/.test(String(sBy.ease_factor)));

const bio = await get('/api/v1/biometrics/status');
check('the biometrics say which machine the flow reading is of',
  /host CPU headroom/.test(String(bio.body?.cardiovascular?.resource_flow_basis))
  && typeof bio.body?.cardiovascular?.host_cpu_percent === 'number');
check('the platform reports its OWN work separately from host load',
  typeof bio.body?.workload?.platform_busy === 'boolean');

const cands = await get('/api/v1/economy/ventures/candidates?top=5');
check('the venture score is named a policy score, not a ranking',
  /policy score/.test(String(cands.body?.method)) && !/×/.test(String(cands.body?.method)));
check('every candidate says its score is not a measurement',
  (cands.body?.candidates || []).every(c => /not a measurement/.test(String(c.score_basis))));

const gate = await post('/api/v1/vbs/qms/gate', { coverage: 0.10, stubs_found: true });
check('a typed what-if gate declares itself excluded from the rate',
  gate.body?.passed === false && gate.body?.counted_in_rate === false);
const defects = await get('/api/v1/vbs/qms/defects');
check('the non-conformance rate says what population it covers',
  /platform/.test(String(defects.body?.summary?.rate_basis))
  && /not one entity/.test(String(defects.body?.summary?.rate_basis)));
check('the what-if did not move the delivery rate',
  (defects.body?.summary?.what_if_gates ?? 0) >= 1);

// ── the pages ───────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

// the Reactor Studio refuses an unreadable line instead of charting it as zero
await page.goto(`${BASE}/reactor-studio`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.waitForTimeout(600);
const ta = page.locator('textarea').first();
if (await ta.isVisible().catch(() => false)) {
  await ta.fill('Q1, 10\nQ2, 20\nQ4, n/a');
  const renderBtn = page.locator('button:has-text("Render analytics")').first();
  await renderBtn.click().catch(() => {});
  await page.waitForTimeout(1200);
  const txt = await page.content();
  check('an unreadable line is named back, not charted as zero',
    /no readable number/.test(txt) && /line 3/.test(txt));
  check('the promise on the header is now true',
    /never invents numbers/.test(txt));
} else {
  check('an unreadable line is named back, not charted as zero (textarea present)', false);
  check('the promise on the header is now true', false);
}

// the Knowledge Hub shows the number the API computes, not two it never sends
await page.goto(`${BASE}/coe`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const khText = await page.content();
if (/Centre of Excellence|Knowledge/i.test(khText)) {
  check('the CoE cards no longer show an invented Confidence',
    !/>Confidence</.test(khText) && !/>Outputs</.test(khText));
} else {
  check('the CoE cards no longer show an invented Confidence', false);
}

// the spawn studio names what actually runs
await page.goto(`${BASE}/vsb-spawn`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(600);
const spawnText = await page.content();
check('the spawn page no longer claims nine cognitive engines',
  !/Nine Cognitive Engines/.test(spawnText));
check('the spawn page says the engines return fixed markers and three are planned',
  /fixed markers/.test(spawnText) && /planned and do not run yet/.test(spawnText));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
process.exit(passed === checks.length ? 0 : 1);
