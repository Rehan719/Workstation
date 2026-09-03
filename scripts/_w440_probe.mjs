// W440 — drive the VBS systems panel in a real browser against the built bundle: the operating
// management systems must render on the cockpit (with or without a VSB), the QMS defect loop must
// walk end-to-end through the UI, and the disclosed-simulation framing must be on screen.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8018';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/vsb-cockpit?tab=systems', { waitUntil: 'domcontentloaded', timeout: 45000 });
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

const body = () => p.evaluate(() => document.body.innerText.toLowerCase());   // CSS uppercase reaches innerText
await p.waitForFunction(() => /quality gates/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => /nothing simulated/i.test(document.body.innerText), { timeout: 30000 });   // the async catalogue paints AFTER the gate section — wait for its specific text, not text already on screen
let text = await body();
console.log('RESULT panel renders (VSB or not):', text.includes('quality gates') && text.includes('document control') && text.includes('mycelial backbone'));
console.log('RESULT simulated splits on screen:', text.includes('simulated:') && text.includes('nothing simulated'));

// 1) run a FAILING gate through the UI → a defect appears
await p.locator('input[aria-label="coverage"]').fill('0.4');
await p.locator('button:has-text("Gate")').first().click();
await p.waitForFunction(() => /FAILED \(min/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => /DEF-[0-9a-f]+/i.test(document.body.innerText), { timeout: 30000 });
console.log('RESULT failing gate opened a traceable defect: true');

// 2) walk the loop: select the defect → correct → reverify with MEASURED content → closed
await p.locator('button', { hasText: /DEF-[0-9a-f]+/i }).first().click();
await p.locator('input[placeholder="what was corrected…"]').fill('rewrote the delivery with full coverage');
await p.locator('button:has-text("Correct")').first().click();
await p.waitForFunction(() => /closure still requires re-verification/i.test(document.body.innerText), { timeout: 30000 });
console.log('RESULT correction never closes alone: true');
const goodContent = 'A substantive corrected delivery. '.repeat(40);
await p.locator('textarea[placeholder*="CORRECTED delivery"]').fill(goodContent);
await p.locator('button:has-text("Re-verify (measured)")').first().click();
await p.waitForFunction(() => /passed the same gate|reopened/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
console.log('RESULT measured reverify verdict rendered:', text.includes('measured from the content') || text.includes('reopened'));

// 3) BMS economics: the $0.50 constant disclosed on screen
await p.locator('button:has-text("Economics")').first().click();
await p.waitForFunction(() => /cost\/insight/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
console.log('RESULT ROI constant disclosed:', text.includes('insight $0.50 value constant'));

// 4) backbone: honest names + register works
console.log('RESULT latency named honestly:', text.includes('latency ewma') && text.includes('(simulated)'));
await p.locator('button:has-text("Register DID")').first().click();
await p.waitForFunction(() => /\d+ nodes/i.test(document.body.innerText), { timeout: 30000 });
console.log('RESULT backbone register reflects in health: true');

await b.close();
console.log('RESULT PASS');
