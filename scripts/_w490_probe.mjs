// W490 (P1.18 + P2.3 + P2.4 + P2.6 + P2.9, the C7 batch repo-wide) — floor-served output says so
// wherever it goes: on the screen, in the file that leaves, and in the API that feeds both.
//   node scripts/_w490_probe.mjs http://127.0.0.1:8095
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8095';
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
const text = async (p) => {
  const r = await fetch(`${BASE}${p}`);
  return { status: r.status, body: await r.text() };
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

// ── the API says what served each output ────────────────────────────────────────────────────────
const assess = await post('/api/v1/transformation/assess', {});
check('the assessment carries what served it',
  assess.status === 200 && typeof assess.body?.ai_provenance?.served_by !== 'undefined');

const bp = await post('/api/v290/ceo/generate-blueprint',
  { intent: 'w490 probe', realm: 'enterprise', stage: 'concept', domain: 'enterprise' });
check('the blueprint carries what composed it',
  bp.status === 200 && Boolean(bp.body?.ai_provenance?.served_by));

const solve = await post('/api/v1/intelligence/solve', { problem: 'w490 probe', domain: 'general' });
check('the engine list says what it actually is',
  /not one call per engine/.test(String(solve.body?.engines_used_basis)));
check('the call count is counted, not asserted',
  solve.body?.calls_attempted === 3
  && solve.body?.calls_made === 3 - (solve.body?.provenance?.failed_calls ?? 0));
check('a floor-served run says so in its summary',
  /structured floor/.test(String(solve.body?.run_summary)));

// the deliverable export: every format says the same thing, and the card cannot contradict itself
const made = await post('/api/v1/deliverables/produce', {
  type: 'report', title: 'W490 probe', brief: 'probe', content: '## Objective\nA probe deliverable.\n' });
const did = made.body?.id;
check('a deliverable was produced', made.status === 200 && Boolean(did));
if (did) {
  const md = await text(`/api/v1/deliverables/${did}/export?format=md`);
  check('the markdown export does not credit the AI fabric for floor output',
    md.status === 200 && !/own AI fabric/.test(md.body));
  check('the markdown export names what composed it',
    /not model analysis|composed in-house by|supplied verbatim|no call is recorded/.test(md.body));
  const svg = await text(`/api/v1/deliverables/${did}/export?format=svg`);
  const footer = (svg.body.match(/>([^<]*Workstation IDBO[^<]*)</) || [])[1] || '';
  check('the SVG card footer agrees with its own subtitle',
    svg.status === 200 && /structured floor|composed in-house|verbatim|not recorded/.test(footer));
  check('the SVG card footer no longer says in-house for floor output', !/in-house/.test(footer));
  const rows = await get('/api/v1/deliverables');
  const row = (rows.body?.deliverables || rows.body || []).find?.(r => r.id === did);
  check('the list row carries is_external so it can match the detail pane',
    row ? Object.prototype.hasOwnProperty.call(row, 'is_external') : false);
}

// a verbatim ingest is not a composition claim
const ing = await post('/api/v1/deliverables/produce', {
  type: 'report', title: 'W490 ingest', brief: 'probe', content: '## A\nCaller text.\n',
  source_served_by: 'verbatim-ingest' });
if (ing.body?.id) {
  const imd = await text(`/api/v1/deliverables/${ing.body.id}/export?format=md`);
  check('a verbatim ingest is not exported as composed in-house',
    !/composed in-house by verbatim-ingest/.test(imd.body));
}

// ── the pages ───────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/organism?tab=cognition`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(600);
const ciText = await page.content();
check('the cognition page no longer heads its engine list "Ran:"', !/>Ran: </.test(ciText));

await page.goto(`${BASE}/settings`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(600);
const setText = await page.content();
check('settings no longer claims nothing is inferred from your activity',
  !/nothing is inferred from your activity/.test(setText));
check('settings names the two recall surfaces and warns about the shared store',
  /AI CEO chat/.test(setText) && /SHARED space/.test(setText));

await page.goto(`${BASE}/deliverables`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const delText = await page.content();
check('the deliverables row shows a provenance badge, not a raw token',
  /structured floor|supplied verbatim|provenance not recorded|in-house ·/.test(delText));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
process.exit(passed === checks.length ? 0 : 1);
