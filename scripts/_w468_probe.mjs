// W468 — a VSB ledger that cannot be read whole is refused and said so on both economy pages, in a real browser against
// the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1; virtual WST only). Seed first with
// scripts/_w468_probe_seed.py <tag> under the same isolated env (it leaves one REAL unreadable ledger: a byte-order mark
// in front of valid books), then:
//   node scripts/_w468_probe.mjs http://127.0.0.1:8076 <unreadable> <readable> <the probe's DATA_DIR>
//   · Economy page: the board pack says the ledger could not be read (never zero figures); Run Metabolic Cycle answers
//     with the server's reason (nothing ran); and a readable entity's pack whose ledger became unreadable before Close
//     period was clicked says nothing was closed (the probe writes that one byte-order mark itself, then restores the file);
//     and the living roster shows the entity whose last heartbeat visit raised (the seed leaves one such visit);
//   · Cockpit, economy tab: the ledger panel says why it cannot show balances (never "No ledger yet"), a cycle refused by
//     the server shows the server's reason (never "backend unreachable"), and switching to a readable entity shows its
//     balances with no stale error;
//   · a revenue beyond the cycle's bound (1e15 WST) is refused with its reason, not a bare status;
//   · (stubbed network failure, labelled) a cycle whose request never reached the backend says so.
// Afterwards the seed's sha256 of the unreadable file is compared by the caller: nothing was written to it.
import { readFileSync, writeFileSync } from 'node:fs';
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8076';
const [BAD, GOOD, DATA_DIR] = [process.argv[3], process.argv[4], process.argv[5]];
if (!BAD || !GOOD || !DATA_DIR) {
  console.error('usage: node scripts/_w468_probe.mjs <base> <unreadable> <readable> <probe DATA_DIR>'); process.exit(2);
}
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const dismissTour = async (page) => {
  for (let i = 0; i < 3; i++) {
    const skip = page.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    if (!(await page.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
};
const flat = (s) => (s || '').replace(/\s+/g, ' ').trim();

// ── the Economy page ──
const e = await ctx.newPage();
await e.goto(`${BASE}/economy?vsb=${BAD}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await e.waitForSelector('[data-testid="board-pack-error"]', { timeout: 60000 }).catch(() => {});
await dismissTour(e);
const packErr = flat(await e.locator('[data-testid="board-pack-error"]').innerText().catch(() => ''));
console.log('  board pack:', packErr.slice(0, 200));
check('the board pack says the ledger could not be read, rather than showing empty books',
  packErr.includes('could not be read whole') && packErr.includes('not shown rather than showing empty books'));

await e.getByRole('button', { name: 'Run Metabolic Cycle' }).click();
await e.getByText(/No cycle ran and nothing was posted/).first().waitFor({ timeout: 30000 }).catch(() => {});
const cycleErr = flat(await e.getByText(/No cycle ran and nothing was posted/).first().innerText().catch(() => ''));
console.log('  cycle:', cycleErr.slice(0, 200));
check('Run Metabolic Cycle shows the server\'s reason (no cycle ran, nothing was posted), not a bare status code',
  cycleErr.includes('could not be read whole') && !/^HTTP 503$/.test(cycleErr));

const visitErr = e.locator('[data-testid="living-visit-error"]');
await visitErr.first().waitFor({ timeout: 30000 }).catch(() => {});
const visitErrTitle = (await visitErr.first().getAttribute('title').catch(() => '')) || '';
console.log('  living roster:', await visitErr.count(), 'raised-visit badge(s) |', visitErrTitle.slice(0, 120));
check('the living roster shows the entity whose last heartbeat visit raised, with the raise (never a clean, freshly tended row)',
  (await visitErr.count()) === 1 && visitErrTitle.includes('TimeoutError'));
const packFigures = await e.getByText('Revenue (cumulative)').count();
check('no board pack figures are shown for the unreadable ledger (so there is nothing to close from it)', packFigures === 0);
await e.close();

// the board pack of a READABLE entity was loaded, then its ledger became unreadable before Close was clicked: the
// server refuses, the page says nothing was closed, and the file is untouched (restored afterwards for the cockpit checks)
const goodLedger = `${DATA_DIR}/economy/${GOOD}_ledger.json`;
const goodBytes = readFileSync(goodLedger);
const e2 = await ctx.newPage();
await e2.goto(`${BASE}/economy?vsb=${GOOD}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await e2.getByRole('button', { name: 'Close period (CFO)' }).waitFor({ timeout: 60000 });
await dismissTour(e2);
const broken = Buffer.concat([Buffer.from([0xef, 0xbb, 0xbf]), goodBytes]);
let closeErr = '', closedMsg = -1, untouched = false;
writeFileSync(goodLedger, broken);
try {
  await e2.getByRole('button', { name: 'Close period (CFO)' }).click();
  await e2.getByText(/Nothing was closed/).first().waitFor({ timeout: 30000 }).catch(() => {});
  closeErr = flat(await e2.getByText(/Nothing was closed/).first().innerText().catch(() => ''));
  closedMsg = await e2.getByText(/Books closed/).count();
  untouched = readFileSync(goodLedger).equals(broken);
} finally {
  writeFileSync(goodLedger, goodBytes);           // restored whatever happened, for the cockpit checks
}
console.log('  close:', closeErr.slice(0, 200), '| file untouched', untouched);
check('Close period on a ledger that became unreadable says nothing was closed, shows no "Books closed", and writes nothing',
  closeErr.includes('could not be read whole') && closedMsg === 0 && untouched);
await e2.close();

// ── the Cockpit, economy tab ──
const c = await ctx.newPage();
await c.goto(`${BASE}/vsb-cockpit?vsb=${BAD}&tab=economy`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await c.waitForSelector('[data-testid="ledger-error"]', { timeout: 60000 }).catch(() => {});
await dismissTour(c);
const ledgerErr = flat(await c.locator('[data-testid="ledger-error"]').innerText().catch(() => ''));
const noLedgerYet = await c.getByText('No ledger yet').count();
console.log('  cockpit ledger:', ledgerErr.slice(0, 200), '| "No ledger yet" shown', noLedgerYet);
check('the cockpit ledger panel says why it shows no balances (never "No ledger yet")',
  ledgerErr.includes('could not be read whole') && ledgerErr.includes('No balances are shown') && noLedgerYet === 0);

await c.fill('input[aria-label="Revenue for this economic cycle in virtual WST"]', '5');
await dismissTour(c);
await c.getByRole('button', { name: 'Run economic cycle' }).click();
await c.getByText(/No cycle ran and nothing was posted/).first().waitFor({ timeout: 30000 }).catch(() => {});
const cockpitCycle = flat(await c.getByText(/No cycle ran and nothing was posted/).first().innerText().catch(() => ''));
const unreachable = await c.getByText(/backend unreachable/).count();
console.log('  cockpit cycle:', cockpitCycle.slice(0, 200), '| "backend unreachable" shown', unreachable);
check('a cycle the server refused shows its reason in the cockpit, never "backend unreachable"',
  cockpitCycle.includes('could not be read whole') && unreachable === 0
  && (await c.locator('[data-testid="ledger-error"]').count()) === 1);

await dismissTour(c);
await c.selectOption('select[aria-label="Select VSB"]', GOOD);
await c.waitForTimeout(2500);
const goodErr = await c.locator('[data-testid="ledger-error"]').count();
const goodRevenue = flat(await c.getByText(/Total revenue:/).first().innerText().catch(() => ''));
const staleRefusal = await c.getByText(/No cycle ran and nothing was posted/).count();
console.log('  readable entity:', goodRevenue.slice(0, 160), '| ledger-error shown', goodErr, '| stale refusal shown', staleRefusal);
check('switching to an entity with readable books shows its balances, with neither the ledger error nor the other entity\'s cycle refusal left on screen',
  goodErr === 0 && staleRefusal === 0 && /Total revenue: 5,000/.test(goodRevenue));

// ── a figure beyond the cycle's bound is refused (422) with its reason, never a bare status ──
await dismissTour(c);
await c.fill('input[aria-label="Revenue for this economic cycle in virtual WST"]', '10000000000000000');
await c.getByRole('button', { name: 'Run economic cycle' }).click();
await c.getByText(/less than or equal to/).first().waitFor({ timeout: 30000 }).catch(() => {});
const bound = flat(await c.getByText(/less than or equal to/).first().innerText().catch(() => ''));
console.log('  bound:', bound.slice(0, 200));
check('a revenue beyond the cycle\'s bound is refused with its reason, naming the field (never a bare "HTTP 422")',
  bound.startsWith('The cycle failed: revenue:') && !/HTTP 422/.test(bound));

// ── (stubbed network failure, labelled) a request that never reached the backend says so ──
await c.route('**/api/v1/economy/cycle', r => r.abort('connectionrefused'));
await dismissTour(c);
await c.getByRole('button', { name: 'Run economic cycle' }).click();
await c.getByText(/The cycle failed — backend unreachable/).first().waitFor({ timeout: 30000 }).catch(() => {});
const aborted = await c.getByText(/The cycle failed — backend unreachable/).count();
console.log('  stubbed abort: shown', aborted);
check('(stubbed network failure) a cycle request that never reached the backend says the backend was unreachable', aborted >= 1);
await c.close();

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
