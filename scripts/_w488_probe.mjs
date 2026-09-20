// W488 (P1.18, the C5 batch + its refutation) — the page and the API say the same thing.
// Fresh backend + the real pages in a real browser: the plan's refusal REACHES the Owner (it used to
// crash the page and blank a tab), the form the economy actually used is the one the picker marks, and
// the BTO/management surfaces no longer promise what the floor does not do.
//   node scripts/_w488_probe.mjs http://127.0.0.1:8093
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8093';
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

// ── the API's own answers first ────────────────────────────────────────────────────────────────
const SCOPE = 'w488probe';
const CORRUPT = '{"scope": "w488probe", "objectives": [';
// seed a real plan, then corrupt it through the API's own path
const seeded = await post('/api/v1/business-plan/objective', {
  scope: SCOPE, title: 'w488 probe objective', kpi: 'k', timeline: 't', owner_role: 'AI CEO' });
check('seed a plan through the API', seeded.status === 200);
// …then corrupt it on disk: the probe is given the backend's DATA_DIR so it breaks the real file the
// running server reads, exactly as a truncated write or a bad disk would.
import fs from 'node:fs';
import path from 'node:path';
const DATA = process.argv[3];
if (!DATA) { console.log('RESULT probe needs the backend DATA_DIR as argv[3]:', false); process.exit(1); }
const planFile = path.join(DATA, 'business_plans', `${SCOPE}.json`);
fs.writeFileSync(planFile, CORRUPT, 'utf-8');

const refused = await get(`/api/v1/business-plan?scope=${SCOPE}`);
check('the API refuses an unreadable plan with 503', refused.status === 503);
check('the refusal names the file and promises nothing was written',
  /could not be read whole/.test(String(refused.body?.detail)) && /never replaced/.test(String(refused.body?.detail)));
const listed = await get('/api/v1/business-plan/list');
const row = (listed.body?.plans || []).find(r => r.scope === SCOPE);
check('the listing keeps the unreadable plan as a row, marked unreadable',
  listed.status === 200 && row && row.readable === false && row.objectives === null);
check('the listing says its counts are partial',
  listed.body?.unreadable_total >= 1 && /readable only/.test(String(listed.body?.counts_cover)));
check('the file was NOT overwritten by any of that', fs.readFileSync(planFile, 'utf-8') === CORRUPT);

// the Board's apex directive over an unreadable plan says why it did not land
const directive = await post('/api/v1/board/chief/instruct', {
  owner: 'Rehan', instruction: 'w488 probe directive', scope: SCOPE, cascade_to_ceo: true });
check('the directive still records, and says the objectives were NOT added',
  directive.status === 200 && directive.body?.objectives_added === 0
  && /were NOT added/.test(String(directive.body?.objectives_not_added_reason)));

// the economy disclosure: a claim that was ignored, and NO claim at all
const REG = 'vsb-w488probe';
// the living roster is a store, not a route: the probe seeds it through the economy's own registration
// path by writing the roster file the backend reads (same DATA_DIR), then lets the API resolve it.
const rosterFile = path.join(DATA, 'living_vsbs.json');
let roster = {};
try { roster = JSON.parse(fs.readFileSync(rosterFile, 'utf-8')); } catch { roster = {}; }
roster[REG] = { vsb_id: REG, name: 'W488 Probe', entity_type: 'waqf_ltd_hybrid', owner: 'Rehan' };
fs.writeFileSync(rosterFile, JSON.stringify(roster, null, 2), 'utf-8');
const claimed = await get(`/api/v1/economy/waterfall?vsb_id=${REG}&entity_type=charity`);
const unclaimed = await get(`/api/v1/economy/waterfall?vsb_id=${REG}`);
check('a form the registry overrode is reported as ignored',
  claimed.body?.claim_ignored === true && claimed.body?.claimed_entity_type === 'charity');
check('a request that claimed NO form is told no form was requested',
  unclaimed.body?.claim_ignored === false && unclaimed.body?.claimed_entity_type === null
  && /no form was requested/.test(String(unclaimed.body?.form_note)));

// ── then the pages that must repeat those answers ──────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/business-plan?scope=${SCOPE}`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.waitForTimeout(800);
const panel = page.locator('[data-testid="plan-unreadable"]');
check('the Business Plan page shows the refusal', await panel.isVisible().catch(() => false));
const panelText = await panel.textContent().catch(() => '');
check('the page repeats the API\'s own words (the file could not be read whole)',
  /could not be read whole/.test(panelText || ''));
check('the page says nothing was overwritten', /not (be )?overwritten|not replaced/i.test(panelText || ''));
const boundary = await page.locator('text=Render Error').isVisible().catch(() => false);
check('the page did NOT crash into the error boundary', boundary === false);
check('no uncaught render error', crashes.length === 0);

// the VSB Economy picker marks the form actually in force
await page.goto(`${BASE}/economy?vsb=${REG}`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.waitForTimeout(1200);
const inForce = page.locator('[data-testid="form-in-force"]');
check('the economy page states the form in force', await inForce.isVisible().catch(() => false));
const charityCard = page.locator('[data-testid="form-card-charity"]');
if (await charityCard.isVisible().catch(() => false)) {
  await charityCard.click();
  await page.waitForTimeout(1500);
  const banner = page.locator('[data-testid="form-claim-ignored"]');
  check('picking a form the registry overrides says so', await banner.isVisible().catch(() => false));
  const bText = await banner.textContent().catch(() => '');
  check('the banner names the form actually used', /waqf_ltd_hybrid/.test(bText || ''));
  check('the picked card is marked NOT used', /NOT used/.test(await page.content()));
} else {
  check('picking a form the registry overrides says so (charity card present)', false);
  check('the banner names the form actually used', false);
  check('the picked card is marked NOT used', false);
}

// the BTO page composes a blueprint and says nothing is provisioned
await page.goto(`${BASE}/bto`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.waitForTimeout(600);
const btoText = await page.content();
check('the BTO page does not claim provisioning',
  !/AI-Mediated Provisioning/.test(btoText) && !/Provision your blueprint/.test(btoText));
check('the BTO page says it composes a blueprint', /Compose your blueprint/.test(btoText));

// the management-systems hub promises a frame, not a certifiable document
await page.goto(`${BASE}/management`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.waitForTimeout(600);
const msText = await page.content();
check('the management hub calls its output a draft frame',
  /frames to complete, not finished documents/.test(msText));
check('no management panel promises a finished document',
  !/Generate an ISO 9001:2015-aligned Quality Management System with policies/.test(msText));

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
process.exit(passed === checks.length ? 0 : 1);
