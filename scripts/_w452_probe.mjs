// W452 (delivery-plan P1.4) — Mode 3 review gates GATE, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1): on the Genesis page a founder gates the design stage and rejects it;
// the panel now says what that does; the Cockpit's Ship button is refused with the gate named (legible,
// never "[object Object]"); approving the gate lets the ship through.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8034';
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

// ── 1. Genesis: a named journey that establishes on completion (so the newborn has a body and a repo) ──
await open('/genesis');
await p.locator('textarea').first().fill('I keep 40 beehives in Somerset and lose colonies to varroa every winter');
await p.getByLabel('Establish living VSB on completion').check();
await p.getByLabel('Enterprise name').first().fill('Somerset Hive Health');
await p.locator('button', { hasText: /Launch Journey → Establish VSB/ }).first().click();
await p.waitForFunction(() => /vsb-[0-9a-f]{10}/.test(document.body.innerText) && /Human review gates/i.test(document.body.innerText), { timeout: 300000 });
const vid = ((await body()).match(/vsb-[0-9a-f]{10}/) || [])[0];
console.log('  newborn:', vid);

// ── 2. the panel: gate Solution Design, reject it; the copy says what a gate does ──
await p.locator('button', { hasText: /Human review gates \(Mode 3\)/ }).first().click();
await p.waitForFunction(() => /tap a stage to gate\/ungate/i.test(document.body.innerText), { timeout: 30000 });
let text = await body();
check('panel copy: says a pending/rejected gate BLOCKS ship, evolve, cascades and orchestration (409)', /blocks this enterprise's lifecycle movers/i.test(text) && /409/.test(text));
await p.locator('button', { hasText: /^Solution Design/ }).first().click();
await p.waitForFunction(() => /Solution Design · pending/i.test(document.body.innerText), { timeout: 30000 });
await p.locator('button[title="Reject"]').first().click();
await p.waitForFunction(() => /Solution Design · rejected/i.test(document.body.innerText), { timeout: 30000 });
check('panel: the design gate reads rejected', /Solution Design · rejected/i.test(await body()));

// ── 3. the API: every mover refuses with the gate named ──
const results = await p.evaluate(async (id) => {
  const post = async (u, b) => { const r = await fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b ?? {}) }); return { s: r.status, d: (await r.json().catch(() => ({}))).detail }; };
  return {
    ship: await post(`/api/v1/vsb/${id}/repo/ship`),
    evolve: await post(`/api/v1/vsb/${id}/evolve`, { trigger: 'probe' }),
    cascade: await post('/api/v1/swarm/cascade', { mission: 'probe', scope: id }),
  };
}, vid);
console.log('  api:', JSON.stringify(results).slice(0, 300));
check('api: ship, evolve and the org cascade are 409 with {gate: design, status: rejected, blocks_progress}',
  ['ship', 'evolve', 'cascade'].every(k => results[k].s === 409 && results[k].d?.gate === 'design' && results[k].d?.status === 'rejected' && results[k].d?.blocks_progress === true));

// ── 4. the Cockpit: the Ship button is refused legibly ──
await open(`/vsb-cockpit?vsb=${vid}&tab=transform`);
await p.locator('button', { hasText: /Ship the repo/i }).first().scrollIntoViewIfNeeded();
await p.locator('button', { hasText: /Ship the repo/i }).first().click();
await p.waitForFunction(() => /review gate blocks progress/i.test(document.body.innerText), { timeout: 60000 });
text = await body();
check('cockpit: the refusal names the gate and its status, not "[object Object]"', /gate 'design' is rejected/i.test(text) && !/object Object/.test(text));

// ── 5. approve → the ship goes through ──
const approved = await p.evaluate(async (id) => {
  await fetch(`/api/v1/vsb/${id}/review-gates/design/decision`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ decision: 'approve', note: 'probe' }) });
  const r = await fetch(`/api/v1/vsb/${id}/repo/ship`, { method: 'POST' });
  return { s: r.status, j: await r.json() };
}, vid);
check('approved: the ship is 200 and coherent', approved.s === 200 && approved.j?.coherent_whole === true);

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
