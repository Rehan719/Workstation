// W442 — drive the economy operations in a real browser against the built bundle: the venture
// portfolio (returns half of §6), the CFO period close, the federation transfer form, and the
// charity candidates pool must render honestly; the close must actually close the books.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8021';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/economy', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });

// dismiss the first-visit onboarding tour
for (let i = 0; i < 3; i++) {
  const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
  if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);
  if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
}
await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});

// wait for the SPECIFIC async panels, not text already on screen (the round's standing lesson)
await p.waitForFunction(() => /Venture Portfolio/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => /Charity candidates/i.test(document.body.innerText), { timeout: 30000 });
const body = () => p.evaluate(() => document.body.innerText.toLowerCase());
let text = await body();

check('venture portfolio renders with honest empty',
  text.includes('venture portfolio') && text.includes('no venture investments yet'));
check('returns disclosed as caller-asserted + cumulative bound',
  text.includes('caller-asserted') && text.includes('cumulative returns bounded'));
check('transfer panel honest precondition (no living receivers)',
  text.includes('transfer wst between your entities') && text.includes('no other living entities'));
check('charity candidates pool with provenance',
  text.includes('charity candidates') && text.includes('curated') && text.includes('score'));
check('live-signals gate disclosed', text.includes('live signal ingestion: disabled'));
check('investment candidates render with demo-set disclosure',
  text.includes('investment candidates') && text.includes('demo set'));

// the CFO close — press it and wait for the books-closed outcome
await p.locator('button:has-text("Close period (CFO)")').click();
await p.waitForFunction(() => /Books closed/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('period close ran through the UI',
  text.includes('books closed') && text.includes('retained earnings'));
check('close reports the UEG truthfully',
  text.includes('ueg-logged.') || text.includes('ueg event did not land'));

// statements card present (P&L / balance sheet / cash flow from the board pack)
check('statements render', text.includes('p&l · this period') && text.includes('balance sheet') && text.includes('cash flow'));

await b.close();
console.log(checks.every(Boolean) ? 'RESULT PASS' : 'RESULT FAIL');
process.exit(checks.every(Boolean) ? 0 : 1);
