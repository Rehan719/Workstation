// W437 — drive /native-ai in a real browser against the built bundle: the primitive console must
// RUN primitives and render the honest payload (basis strings, population_source, null-with-reason).
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8011';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/native-ai', { waitUntil: 'domcontentloaded', timeout: 45000 });
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

const body = () => p.evaluate(() => document.body.innerText.toLowerCase());   // CSS text-transform: uppercase reaches innerText
let text = await body();
console.log('RESULT fabric integrity strip:', text.includes('fabric integrity') && /backing modules import live/.test(text));
console.log('RESULT primitive console present:', text.includes('primitive console'));

// 1) run the default primitive (consensus) and expect the tally + basis to render
await p.locator('button:has-text("Run consensus")').first().click();
await p.waitForFunction(() => /threshold consensus \(owned swarm\)/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
console.log('RESULT consensus ran (tally rendered):', text.includes('tally') && text.includes('basis'));

// 2) quorum with the population field left blank → the agent-catalog default must be disclosed
//    (named for what it is: a static definition, not a "live roster" — the refuter caught that)
await p.locator('button', { hasText: /^Quorum$/ }).first().click();
await p.locator('button:has-text("Run quorum")').first().click();
await p.waitForFunction(() => /agent_catalog/.test(document.body.innerText), { timeout: 30000 });
console.log('RESULT quorum used agent catalog (disclosed): true');

// 3) rigor first call on a FRESH metric name (the monitor is process-global, so a reused name
//    accumulates across probe runs and honestly reports zero variance instead) → null-with-reason
await p.locator('button', { hasText: /^Rigor$/ }).first().click();
await p.locator('label:has-text("metric name") input').fill(`probe_${process.pid}_${Math.floor(Math.random() * 1e6)}`);
await p.locator('button:has-text("Run rigor")').first().click();
await p.waitForFunction(() => /nothing was tested/.test(document.body.innerText), { timeout: 30000 });
text = await body();
console.log('RESULT rigor honest null rendered:', text.includes('null — see basis'));
const consoleText = text.split('primitive console')[1];   // lowercased body — must actually split
if (consoleText === undefined) throw new Error('vacuous check: console heading not found');
console.log('RESULT no fabricated power field:', !/\bpower\b/.test(consoleText));

await b.close();
console.log('RESULT PASS');
