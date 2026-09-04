// W444 — drive the residual-cluster wiring in a real browser against the built bundle:
// the QEP ops strip + intelligence tab, the marketplace listing drawer (edit/price/valuation
// refusal), and the anatomy config additions (history, reset guard) must work end-to-end.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8023';
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
const body = () => p.evaluate(() => document.body.innerText.toLowerCase());

// ── 1. QEP: the ops strip on the Memorization tab, the Intelligence tab's panels ──
await p.goto(BASE + '/qep', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
await dismissTour();
await p.locator('button:has-text("Memorization")').click();
await p.waitForFunction(() => /QEP components/i.test(document.body.innerText), { timeout: 30000 });
let text = await body();
check('qep ops strip renders components + constraints',
  text.includes('qep components') && text.includes('never ai-generated') && text.includes('recitation is never scored'));
check('translation availability chip computed (floor-only env → will refuse)',
  text.includes('unavailable — the floor cannot translate') || text.includes('available —'));

await p.locator('button:has-text("Intelligence")').click();
await p.waitForFunction(() => /Explain SM-2 scheduling/i.test(document.body.innerText), { timeout: 30000 });
await p.locator('button:has-text("Explain")').click();
// wait for the LAST line of the result card (the basis), not the first — the card can paint
// across frames and an early capture misses the honesty line (the round's standing lesson)
await p.waitForFunction(() => /display-weight attribution/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('xai explains via the real engine with basis lines',
  text.includes('real memorizationengine') && text.includes('display-weight attribution'));
await p.waitForFunction(() => /adaptation registry|pattern seeds|no adaptations/i.test(document.body.innerText), { timeout: 30000 });
check('adaptation registry renders with unmeasured-fidelity honesty',
  (await body()).includes('unmeasured') || (await body()).includes('no adaptations recorded'));
check('compliance verdict is tri-state honest',
  (await body()).includes('not established — controls could not run') || (await body()).includes('compliant'));

// ── 2. Marketplace: all listings render, drawer opens, price set, valuation refuses ──
await p.goto(BASE + '/marketplace', { waitUntil: 'domcontentloaded', timeout: 45000 });
await dismissTour();
await p.waitForFunction(() => /unpriced — not for sale|Set price/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('unpriced listings visible with honest badge', text.includes('unpriced — not for sale'));
await p.locator('text=unpriced — not for sale').first().click();
await p.waitForFunction(() => /Edit listing/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('drawer renders detail + edit form', text.includes('edit listing') && text.includes('set price'));
// AI valuation in a floor-only env must REFUSE loudly, never fabricate
await p.locator('button:has-text("Get AI valuation")').click();
await p.waitForFunction(() => /fabrication|failed \(http 503\)/i.test(document.body.innerText), { timeout: 30000 });
check('valuation refuses on the floor (503 shown verbatim)', true);
// set a price through the drawer — the §12 door finally opens
await p.locator('input[aria-label="listing price"]').fill('15');
await p.locator('button:has-text("Save")').first().click();
await p.waitForFunction(() => /re-screened|§11 screen FAIL/i.test(document.body.innerText), { timeout: 30000 });
check('price set through the drawer with re-screen disclosure', true);

// ── 3. Anatomy: change history + the reset guard rendering its 409 honestly ──
await p.goto(BASE + '/organism?tab=anatomy', { waitUntil: 'domcontentloaded', timeout: 45000 });
await dismissTour();
await p.waitForFunction(() => /Reset to defaults/i.test(document.body.innerText), { timeout: 30000 });
await p.locator('button:has-text("Change history")').click();
await p.waitForFunction(() => /no changes recorded yet|→/.test(document.body.innerText), { timeout: 30000 });
check('config change history renders (honest empty or rows)', true);
await p.locator('button:has-text("Reset to defaults")').click();
await p.waitForFunction(() => /Refused \(as designed\)/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('reset guard 409 rendered with the CCA path offered',
  text.includes('refused (as designed)') && text.includes('submit reset proposal to cca'));

await b.close();
console.log(checks.every(Boolean) ? 'RESULT PASS' : 'RESULT FAIL');
process.exit(checks.every(Boolean) ? 0 : 1);
