// W454 (delivery-plan P1.6) — Employment default-tab honesty, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1): the hub opens on the CV tools; the Application Studio's job search says
// "not a live job board", renders illustrative listings with no live link and a provenance badge, and every
// generated document carries the badge.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8038';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();

const dismissTour = async () => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(400);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});
};
const body = () => p.evaluate(() => document.body.innerText);
const open = async (path) => {
  await p.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
  await dismissTour();
};

// ── 1. the hub's default tab is the CV tools ──
await open('/employment');
let text = await body();
check('default tab: the CV Tailor tool, not the Application Studio', /Target role/i.test(text) && !/Job Search Engine/i.test(text));

// ── 2. the Application Studio: honest copy before any search ──
await open('/employment?tab=studio');
await p.waitForFunction(() => /Job Search Engine/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('studio copy: "not a live job board" and no "Live, real-time search" claim', /not a live job board/i.test(text) && !/Live, real-time search/i.test(text));

// ── 3. a search on the floor: the honest empty state, no sources, the floor badge ──
await p.locator('input[placeholder*="override search terms" i]').first().fill('halal bakery operations manager Leeds');
await p.keyboard.press('Enter');
await p.waitForFunction(() => /Synthesised \d+ illustrative listing|No example listings were synthesised/i.test(document.body.innerText), { timeout: 120000 });
text = await body();
const listings = (text.match(/illustrative · no live URL/gi) || []).length;
const links = await p.evaluate(() => [...document.querySelectorAll('#job-search-engine-section a[href^="http"]')].length);
console.log('  listings:', listings, '| live links in the panel:', links);
check('search on the floor: "no sources searched", the floor badge, the honest empty state', /no sources searched/i.test(text) && links === 0 && /structured floor — not model analysis/i.test(text) && /cannot compose listings/i.test(text));

// ── 3b. the listing CARDS (refuter F4: the floor synthesises none, so the cards are driven by a stubbed
//      response shaped exactly like a model-served one — the backend shaping is proved by pytest) ──
await p.route('**/api/v1/career/job-search', route => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
  results: [{ listing_id: 'stub1', title: 'Bakery Operations Manager', company: 'Bakehouse', location: 'Leeds', salary_estimate: '£32k', tags: ['ops'], description: 'Run the bakery.', illustrative: true, basis: 'AI-synthesised example — not a live advert' }],
  query: 'ops', sources_used: [], illustrative: true, basis: 'AI-synthesised example listings — not a live job board', total: 1,
  ai_provenance: { posture: 'in-house-first', served_by: 'ollama:test', is_external: false } }) }));
await p.locator('input[placeholder*="override search terms" i]').first().fill('ops');
await p.keyboard.press('Enter');
await p.waitForFunction(() => /illustrative · no live URL/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
const links2 = await p.evaluate(() => [...document.querySelectorAll('#job-search-engine-section a[href^="http"]')].length);
check('listing cards: the illustrative chip, the salary as an estimate, no live link, the model badge', /illustrative · no live URL/i.test(text) && /est\. £32k/i.test(text) && links2 === 0 && /in-house · ollama:test/i.test(text));
await p.unroute('**/api/v1/career/job-search');
// F1 — 'Use as Target Job Ad' really attaches the listing as a job_ad upload
await p.locator('button', { hasText: /Use as Target Job Ad/i }).first().click();
await p.waitForFunction(() => /Attached as Target Job Ad/i.test(document.body.innerText), { timeout: 30000 });
const attached = await p.evaluate(async () => (await (await fetch('/api/v1/ingest/list?category=job_ad')).json()).length);
check('use: the listing is really attached as a job_ad upload the generator reads', attached >= 1);

// ── 4. a generated document carries the badge ──
const res = await p.evaluate(async () => {
  const r = await fetch('/api/v1/career/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ file_ids: [], instructions: 'bakery operations manager', output_types: ['cv'] }) });
  return await r.json();
});
check('api: a generated document carries ai_provenance', !!res?.results?.[0]?.ai_provenance?.served_by);
const js = await p.evaluate(async () => await (await fetch('/api/v1/career/job-search', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: 'developer', limit: 3 }) })).json());
check('api: the job search is illustrative, no url/published on any row, no sources', js?.illustrative === true && Array.isArray(js?.sources_used) && js.sources_used.length === 0 && (js.results || []).every(r => !('url' in r) && !('published' in r)));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
