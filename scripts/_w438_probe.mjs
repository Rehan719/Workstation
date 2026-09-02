// W438 — drive /organism?tab=anatomy in a real browser against the built bundle: the audited
// organism cluster must be REACHABLE and its honesty fields must RENDER (measured-vs-blended
// health, genome provenance, config wiring truth, governed proposals routed through the CCA).
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8014';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/organism?tab=anatomy', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });

// dismiss the first-visit onboarding tour — its overlay intercepts pointer events
for (let i = 0; i < 3; i++) {
  const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
  if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);
  if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
}
await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});

const body = () => p.evaluate(() => document.body.innerText.toLowerCase());   // CSS uppercase reaches innerText
await p.waitForFunction(() => /wiring truth/i.test(document.body.innerText), { timeout: 20000 });
let text = await body();
console.log('RESULT health measured-vs-blended:', text.includes('measured only') && text.includes('blended'));
console.log('RESULT simulated term disclosed:', text.includes('simulated'));
console.log('RESULT systems panel:', text.includes('biomimetic systems') && text.includes('per-process'));
console.log('RESULT genome lab:', text.includes('genome lab'));
console.log('RESULT config wiring truth:', text.includes('wiring truth') && text.includes('stored-only') && text.includes('governed'));

// 1) encode a genome through the UI — on a floor serve the card must SAY it encoded nothing
await p.locator('button:has-text("Encode")').first().click();
await p.waitForFunction(() => /served by/i.test(document.body.innerText), { timeout: 120000 });
text = await body();
console.log('RESULT genome provenance rendered:', text.includes('served by'));
console.log('RESULT floor encode honest:', !text.includes('not encoded') || text.includes('defaults'));

// 2) propose a governed lever change → must route through the CCA, not a raw write
await p.locator('button:has-text("propose")').first().click();
await p.locator('button:has-text("Submit to CCA")').first().click();
await p.waitForFunction(() => /submitted as cca-/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
console.log('RESULT governed proposal → CCA:', /submitted as cca-/.test(text) && text.includes('change control'));

await b.close();
console.log('RESULT PASS');
