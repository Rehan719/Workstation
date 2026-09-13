// W462 — the follow-up register is visible where the plan is read, in a real browser against the built
// bundle on a FRESH backend (AI_DISABLE_LOCAL=1):
//   · GET /api/v1/plan/followups serves the register with integrity ok, and /api/v1/plan carries its counts;
//   · /transformation renders the "Scheduled follow-ups" card with the API's own counts, the next plan
//     item, every scheduled row id and the Owner-gated rows under "Awaiting the Owner";
//   · (stubbed, labelled) a register out of step with the plan shows the problem, and a failed call says
//     the register could not be loaded — never an empty "0 open".
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8065';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } });
const p = await ctx.newPage();
const dismissTour = async (page) => {
  for (let i = 0; i < 3; i++) {
    const skip = page.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    if (!(await page.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
};

await p.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 45000 });
const api = await p.evaluate(async () => (await fetch('/api/v1/plan/followups')).json());
const plan = await p.evaluate(async () => (await fetch('/api/v1/plan')).json());
console.log('  counts:', api.counts, '· next:', api.next_plan_item, '· integrity:', api.integrity);
check('the API serves the register with integrity ok, and /plan carries the same counts',
  api.available === true && api.integrity.ok === true && api.counts.open > 0 && plan.followups?.open === api.counts.open);

await p.goto(BASE + '/transformation', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => !!document.querySelector('[data-testid="followups-card"]'), null, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const card = await p.evaluate(() => document.querySelector('[data-testid="followups-card"]')?.innerText || '');
const ids = api.schedule.flatMap(s => s.items.map(r => r.id));
const owner = api.awaiting_owner.map(r => r.id);
console.log('  card head:', card.slice(0, 160).replace(/\n/g, ' | '));
check('the card shows the API\'s own counts and the next plan item',
  card.includes(`${api.counts.open} open`) && card.includes(`${api.counts.scheduled} scheduled`) && card.includes(`next plan item ${api.next_plan_item}`));
check('every scheduled row and every Owner-gated row is on the card',
  ids.length > 0 && ids.every(id => card.includes(id)) && /never scheduled without your instruction/i.test(card) && owner.every(id => card.includes(id)));
check('slots are shown in the plan order the API gives',
  api.schedule.map(s => card.indexOf(`${s.slot} —`)).every((v, i, a) => v >= 0 && (i === 0 || v > a[i - 1])));

// stubbed: out of step, and unreachable
const p2 = await ctx.newPage();
await p2.route('**/api/v1/plan/followups', r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({
  ...api, integrity: { ok: false, problems: ['FU-999: rides on P1.1, already DONE W449 — that round closed without doing it'] } }) }));
await p2.goto(BASE + '/transformation', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p2.waitForFunction(() => /out of step with the plan/i.test(document.querySelector('[data-testid="followups-card"]')?.innerText || ''), null, { timeout: 60000 }).catch(() => {});
const bad = await p2.evaluate(() => document.querySelector('[data-testid="followups-card"]')?.innerText || '');
check('(stubbed) a register out of step says so and names the problem', /out of step with the plan/i.test(bad) && bad.includes('FU-999'));
await p2.close();
const p4 = await ctx.newPage();
await p4.route('**/api/v1/plan/followups', r => r.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ detail: 'probe 500' }) }));
await p4.goto(BASE + '/transformation', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p4.waitForFunction(() => /could not be loaded/i.test(document.querySelector('[data-testid="followups-card"]')?.innerText || ''), null, { timeout: 60000 }).catch(() => {});
const err500 = await p4.evaluate(() => document.querySelector('[data-testid="followups-card"]')?.innerText || '');
check('(stubbed) a backend answering 500 is named as HTTP 500, not "unreachable"', /HTTP 500/.test(err500) && !/unreachable/i.test(err500));
await p4.close();
const p3 = await ctx.newPage();
await p3.route('**/api/v1/plan/followups', r => r.abort());
await p3.goto(BASE + '/transformation', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p3.waitForFunction(() => !!document.querySelector('[data-testid="followups-card"]'), null, { timeout: 60000 }).catch(() => {});
const down = await p3.evaluate(() => document.querySelector('[data-testid="followups-card"]')?.innerText || '');
check('(stubbed) an unreachable register says it could not be loaded, never "0 open"', /could not be loaded/i.test(down) && !/\b0 open\b/.test(down));
await p3.close();

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
