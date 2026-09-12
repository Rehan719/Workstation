// W457 (delivery-plan P1.9) — Care scoring computes, in a real browser against the built bundle on a FRESH
// backend (AI_DISABLE_LOCAL=1 → the floor serves the narrative): /care?tab=risk with the assessor's
// observations renders a computed "NEWS2 6 · medium · urgent ward-based response" block FIRST, with its
// components, the published-table basis and the amber floor badge on the narrative. Then a PARTIAL set
// (RR + SpO2 only) renders "NEWS2 ≥ 3" with NO band chip and the missing list.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8049';
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
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), null, { timeout: 10000 }).catch(() => {});
};
const body = () => p.evaluate(() => document.body.innerText);

await p.goto(BASE + '/care?tab=risk', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, null, { timeout: 60000 });
await dismissTour();
await p.waitForFunction(() => /Assess risk/i.test(document.body.innerText), null, { timeout: 90000 });
let text = await body();
check('copy: the score is computed in-house from the published table; no "AI scores the risk" claim', /computed in-house from the published table/i.test(text) && !/AI scores and interprets the risk/i.test(text));
await p.getByLabel(/Observations \/ data/i).first().fill('resp_rate: 22\nspo2: 94\noxygen: air\nsystolic_bp: 105\npulse: 95\ntemp: 38.2\nconsciousness: alert');
await p.locator('button', { hasText: /Assess risk/i }).first().click();
await p.waitForFunction(() => !!document.querySelector('[data-testid="care-score"]'), null, { timeout: 180000 });
text = await body();
const block = await p.evaluate(() => document.querySelector('[data-testid="care-score"]')?.innerText || '');
const order = await p.evaluate(() => { const s = document.querySelector('[data-testid="care-score"]'); const pre = document.querySelector('pre'); return s && pre ? (s.compareDocumentPosition(pre) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0 : false; });
console.log('  block:', block.slice(0, 200).replace(/\n/g, ' | '));
check('the computed score block: NEWS2 6 · medium · key threshold for urgent response', /NEWS2 6/i.test(block) && /medium/i.test(block) && /key threshold for urgent response/i.test(block));
check('the components with their points (RR 22 → 2, SpO2 94 → 1, SBP 105 → 1, pulse 95 → 1, temp 38.2 → 1)', /respiratory rate: 22 → 2/i.test(block) && /spo2 scale 1: 94 → 1/i.test(block) && /systolic bp: 105 → 1/i.test(block) && /pulse: 95 → 1/i.test(block) && /temperature: 38.2 → 1/i.test(block));
check('the published-table basis and the decision-aid line', /Royal College of Physicians, 2017/i.test(block) && /clinical judgement by a qualified professional/i.test(block));
check('the score block renders BEFORE the narrative', order === true);
check('the narrative wears the amber floor badge and the in-house disclaimer', /structured floor — not model analysis/i.test(text) && /computed in-house from the published table/i.test(text));

// a partial set — a lower bound, no banded verdict
await p.getByLabel(/Observations \/ data/i).first().fill('resp_rate: 22\nspo2: 94');
await p.locator('button', { hasText: /Assess risk/i }).first().click();
await p.waitForFunction(() => /NEWS2 ≥ 3/.test(document.querySelector('[data-testid="care-score"]')?.innerText || ''), null, { timeout: 180000 });
const block2 = await p.evaluate(() => document.querySelector('[data-testid="care-score"]')?.innerText || '');
console.log('  block2:', block2.slice(0, 200).replace(/\n/g, ' | '));
check('a partial set renders "NEWS2 ≥ 3", no band chip, the missing list and "no band until"', /NEWS2 ≥ 3/.test(block2) && !/\bLOW\b/.test(block2) && /missing: .*pulse/i.test(block2) && /no band until/i.test(block2));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
