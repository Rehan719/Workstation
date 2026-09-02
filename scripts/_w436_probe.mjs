// W436 — drive /genesis in a real browser against the built bundle: run a journey and assert the
// four item-1 surfaces render. Floor-served journeys complete in seconds, so this is cheap.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8011';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/genesis', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });

// dismiss the first-visit onboarding tour — its overlay intercepts pointer events. A fresh
// browser context always triggers it (it auto-runs once for new visitors), so the probe must
// close it the way a person would.
for (let i = 0; i < 3; i++) {
  const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
  if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);
  if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
}
await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});

// fill the problem and run
const ta = p.locator('textarea').first();
await ta.fill('Beekeepers in Konya lose hives to varroa mites and cannot afford lab testing');
const runBtn = p.locator('button', { hasText: /begin|run|start|journey/i }).first();
console.log('RESULT run button:', await runBtn.innerText().catch(() => 'NOT FOUND'));
await runBtn.click();

// wait for the result (floor journeys are fast; allow 240s)
await p.waitForFunction(() => /Sovereign Journey Complete/i.test(document.body.innerText), { timeout: 240000 });
const body = await p.evaluate(() => document.body.innerText);

const checks = [
  ['(a) provenance banner',        /What served this journey/i],
  ['(a) floor wording',            /deterministic native floor served \d+ of these calls/i],
  ['(a) stages note',              /not assessable/i],
  ['(c) chip floor-served count',  /floor-served, not assessable/i],
  ['(c) 0\/0 verified',           /0\/0 verified/i],
  ['(b) §10 bar chip',             /§10 bar:/i],
];
for (const [name, re] of checks) console.log('RESULT', re.test(body) ? 'PASS' : 'FAIL', name);

// (d) — identical candidates must show the note INSTEAD of ranked cards
const noteShown = /no comparison was possible|identical/i.test(body);
const rankedShown = /selected/i.test(body) && /score \d/i.test(body);
console.log('RESULT (d) comparison note shown:', noteShown, '| ranked cards visible:', rankedShown);
await b.close();
