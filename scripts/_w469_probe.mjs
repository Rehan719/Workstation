// W469 — the delivery plan is live on /transformation: the card reads PLAN NOW from the real plan and register, refreshes
// itself every minute, and keeps the last good plan when a refresh fails. Runs in a real browser against the built
// bundle on a FRESH backend (AI_DISABLE_LOCAL=1). No seed: the backend reads this repository's own
// docs/FOLLOWUPS.json and docs/FABLE_DELIVERY_PROMPT.md, read-only.
//   node scripts/_w469_probe.mjs http://127.0.0.1:8077
//   · the card shows the REAL plan: the next item, done per phase, and the items the moved rows ride (P1.15, P2.9);
//   · (stubbed second answer, labelled) the card refreshes by itself within the minute and shows the new next item and
//     an unscheduled row;
//   · (stubbed failed third answer, labelled) a refresh that fails keeps the plan on screen and says the refresh failed.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8077';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const flat = (s) => (s || '').replace(/\s+/g, ' ').trim();

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
let calls = 0;
await page.route('**/api/v1/plan/followups', async (route) => {
  calls += 1;
  if (calls === 1) return route.continue();
  if (calls === 2) {                       // the backend's real answer, changed the way a finished round would change it
    const res = await route.fetch();
    const d = await res.json();
    d.plan.done += 1;
    const moved = d.plan.open_items.shift();
    d.plan.next = d.plan.open_items[0];
    d.plan.phases[0].done += 1;
    d.counts.unscheduled = 1;
    d.unscheduled = [{ id: 'FU-999', title: 'a probe row riding no open item', why: 'stubbed', severity: 'low', slot: moved.slot, source: 'probe' }];
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(d) });
  }
  return route.abort('connectionrefused');
});
await page.goto(`${BASE}/transformation`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.waitForSelector('[data-testid="plan-next"]', { timeout: 60000 }).catch(() => {});
for (let i = 0; i < 3; i++) { await page.keyboard.press('Escape'); await page.waitForTimeout(200); }

const card = page.locator('[data-testid="followups-card"]');
const first = flat(await card.innerText().catch(() => ''));
const next1 = flat(await page.locator('[data-testid="plan-next"]').innerText().catch(() => ''));
console.log('  next:', next1, '| stamp:', flat(await page.locator('[data-testid="plan-live-stamp"]').innerText().catch(() => '')).slice(0, 120));
check('the card reads the real plan: "Delivery plan — live", the next item, and done per phase',
  /Delivery plan — live/i.test(first) && next1.startsWith('Next: P1.13 Catalogue honesty')   // the title is CSS-uppercased
  && /Done 12 of 43 items — P1 12\/16 · P2 0\/9 · P3 0\/12 · P4 0\/6/.test(first));
check('the moved follow-ups show on the items that own them (P1.15 stores, P2.9 economy flows), none unscheduled',
  first.includes('P1.15 — Stores that refuse, never replace') && first.includes("P2.9 — The economy's flows told as they happened")
  && first.includes('FU-042') && first.includes('FU-034') && (await page.locator('[data-testid="plan-unscheduled"]').count()) === 0);

// the minute refresh, with no reload and no click
await page.waitForFunction(() => (document.querySelector('[data-testid="plan-next"]')?.textContent || '').includes('P1.14'),
  null, { timeout: 75000 }).catch(() => {});
const next2 = flat(await page.locator('[data-testid="plan-next"]').innerText().catch(() => ''));
const unsched = flat(await page.locator('[data-testid="plan-unscheduled"]').innerText().catch(() => ''));
console.log('  after refresh:', next2, '| unscheduled:', unsched.slice(0, 100), '| calls', calls);
check('(stubbed second answer) the card refreshed by itself within the minute: the new next item and the unscheduled row',
  calls >= 2 && next2.startsWith('Next: P1.14') && unsched.includes('FU-999'));

// a refresh that fails keeps the plan and says so
await page.waitForFunction(() => (document.querySelector('[data-testid="plan-live-stamp"]')?.textContent || '').includes('the last refresh failed'),
  null, { timeout: 75000 }).catch(() => {});
const stamp3 = flat(await page.locator('[data-testid="plan-live-stamp"]').innerText().catch(() => ''));
const next3 = flat(await page.locator('[data-testid="plan-next"]').innerText().catch(() => ''));
console.log('  after failed refresh:', stamp3.slice(0, 160), '| next still:', next3, '| calls', calls);
check('(stubbed failed third answer) the plan stays on screen and the card says the last refresh failed',
  calls >= 3 && stamp3.includes('the last refresh failed') && next3.startsWith('Next: P1.14'));

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
