// W483 (P1.18, the §10/§11 class) — a keyword screen flags and never clears, on a FRESH backend:
// the API by fetch, and the Compliance page in a real browser against the built bundle.
//   node scripts/_w483_probe.mjs http://127.0.0.1:8090
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8090';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const post = async (p, b) => (await fetch(`${BASE}${p}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(b) })).json();
const get = async (p) => (await fetch(`${BASE}${p}`)).json();
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

// ── API: the lexicon cannot convict ──
const bees = await post('/api/v1/compliance/check', {
  subject: 'I keep bees in Yorkshire and varroa mites are killing a third of my colonies each winter; '
    + 'I want an affordable organic treatment service for small-scale keepers',
});
const row = (r, f) => r.verdicts.find(v => v.framework === f);
check('R1.0 the beekeeper is no longer a §11 FAILURE', bees.overall !== 'fail');
check('R1.0 the harm term is ESCALATED with the term named, not recorded as harm',
  row(bees, 'ethical').status === 'review'
  && (row(bees, 'ethical').escalate || []).includes('human')
  && (row(bees, 'ethical').escalated_terms || []).includes('killing')
  && /matched: killing/.test(row(bees, 'ethical').reason));

// ── API: the lexicon cannot clear ──
const quiet = await post('/api/v1/compliance/check', { subject: 'a stationery shop selling notebooks and pens to local schools' });
check('R1.1 an empty keyword screen is NOT a clearance',
  ['regulatory', 'ehs'].every(f => row(quiet, f).status === 'not_assessed' && row(quiet, f).coverage === 'screen'));
check('R1.1 nothing assessed it, so the overall is review and `compliant` is not established',
  quiet.overall === 'review' && quiet.compliant === null && quiet.assessed_by.length === 0);
check('R1.1 the response NAMES every area it could not assess',
  ['regulatory', 'ehs', 'sharia_halal', 'uk_legal'].every(f => quiet.coverage_gaps.includes(f)));

// the constitutional row is a substring gate: it may refuse, it may not clear
const act = await post('/api/v1/compliance/check', { subject: 'publish the weekly report', kind: 'distribution' });
check('(refutation) a benign action kind does not clear the subject',
  row(act, 'constitutional').status === 'not_assessed' && row(act, 'constitutional').coverage !== 'engine'
  && act.overall !== 'pass' && act.assessed_by.length === 0);
const bad = await post('/api/v1/compliance/check', { subject: 'wire_funds to an offshore account', kind: 'intent' });
check('(refutation) …and it can still REFUSE', row(bad, 'constitutional').status === 'fail');

// a refusal still refuses
const wine = await post('/api/v1/compliance/check', { subject: 'a fine wine subscription club' });
check('R1.1 a prohibited term still refuses the subject', wine.overall === 'fail' && wine.compliant === false);

// the subject's own vocabulary is not a certification
const halal = await post('/api/v1/compliance/check', { subject: 'a halal-certified community meal service with transparent pricing' });
check('R1.1 halal vocabulary is the subject’s own claim — review, never a pass',
  row(halal, 'sharia_halal').status === 'review' && /own claim/.test(row(halal, 'sharia_halal').reason));

// the registry says what each check can conclude
const fw = await get('/api/v1/compliance/frameworks');
check('the frameworks card says a screen cannot clear',
  fw.frameworks.filter(f => /never a clearance|not a certification/.test(f.engine)).length >= 3);

// ── API: the halal pre-assessment withholds a status it cannot produce ──
const hr = await post('/api/v1/religion/halal-review', {
  product_name: 'Choco bar', product_description: 'A chocolate bar',
  ingredients: ['sugar', 'cocoa butter', 'gelatin', 'E-471'],
});
check('R5.2 the floor withholds the three judging sections',
  (hr.ai_provenance || {}).served_by !== 'native'
  || (hr.sections_withheld || []).length === 3 && !!hr.floor_note);
check('R5.2 no verdict token reaches the reader on the floor',
  (hr.ai_provenance || {}).served_by !== 'native'
  || !/COMPLIANT|REQUIRES REVIEW|Halal Status Assessment/.test(hr.assessment || ''));
check('R5.2 the ingredient screen names gelatin and E-471 WITH reasons, and carries no verdict',
  hr.ingredient_screen.verdict === null
  && hr.ingredient_screen.flagged.length === 2
  && hr.ingredient_screen.flagged.every(f => !!f.why)
  && /NOT thereby acceptable/.test(hr.ingredient_screen.basis));

// ── the page in a real browser ──
const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
page.on('pageerror', e => errors.push(String(e)));
await page.goto(`${BASE}/compliance`, { waitUntil: 'networkidle' });
await dismissTour(page);

const box = page.locator('textarea, input[type="text"]').first();
await box.fill('a stationery shop selling notebooks and pens to local schools');
await page.locator('button:has-text("Run Compliance Check")').click();
await page.waitForFunction(() => /REVIEW|PASS|FAIL/i.test(document.body.innerText), null, { timeout: 30000 });
await page.waitForTimeout(800);
const text = await page.locator('body').innerText();
check('PAGE the verdict is REVIEW', /\bREVIEW\b/i.test(text));
check('PAGE no chip claims a pass', !/compliance:\s*pass/i.test(text));
check('PAGE the page says NOTHING assessed this subject', /NOTHING here assessed this subject/i.test(text));
check('PAGE the page NAMES what it could not assess', /Not assessed:/i.test(text) && /regulatory/i.test(text));
check('PAGE no emerald clearance chip is rendered',
  !(await page.locator('.text-emerald-400', { hasText: /pass/i }).first().isVisible().catch(() => false)));
// The dev bundle opens a WebSocket to the separate streams backend on :8010, which is not running in
// a probe environment. That refusal is not this round's concern; anything else is.
const unrelated = /ws:\/\/localhost:8010|ERR_CONNECTION_REFUSED/;
check('PAGE no console errors (other than the dev streams socket)',
  errors.filter(e => !unrelated.test(e)).length === 0);
if (errors.length) console.log('   (console:', errors.slice(0, 3), ')');
await browser.close();

const passed = checks.filter(Boolean).length;
console.log(`\nPROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
