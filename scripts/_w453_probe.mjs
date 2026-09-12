// W453 (delivery-plan P1.5) — provenanceBadge class-kill part 2, in a real browser against the built bundle
// on a FRESH backend (AI_DISABLE_LOCAL=1 → the floor serves every call): the migrated badge sites must
// render the helper's AMBER floor chip — never an emerald "in-house" — on a produced deliverable, the
// Law hub's default tool, the Board of Directors' map chip and the Genesis newborn's plan tab.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8036';
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
const open = async (path) => {
  await p.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
  await dismissTour();
};
// the class-kill's proof: every floor chip carries the helper's amber classes, and no chip on the page
// says "in-house" in emerald
const floorChips = () => p.evaluate(() => {
  const els = [...document.querySelectorAll('span')].filter(e => /structured floor — not model analysis/i.test(e.textContent || ''));
  return { amber: els.filter(e => /text-amber-400/.test(e.className)).length, total: els.length,
           greenInHouse: [...document.querySelectorAll('span')].filter(e => /^in-house/i.test((e.textContent || '').trim()) && /text-emerald-400/.test(e.className)).length };
});

// ── 1. Deliverables: the detail chip (was label-only, coloured emerald by is_external) ──
await open('/deliverables');
await p.locator('textarea').first().fill('A halal artisan bakery in Leeds serving students — a short market brief');
await p.locator('button', { hasText: /Produce report/i }).first().click();
await p.waitForFunction(() => /structured floor — not model analysis/i.test(document.body.innerText), { timeout: 90000 });
let c = await floorChips();
console.log('  deliverables chips:', JSON.stringify(c));
check('deliverables: the floor chip is amber via the helper, no emerald in-house chip', c.total >= 1 && c.amber === c.total && c.greenInHouse === 0);

// ── 2. Law hub default tool (was label-only, coloured emerald) ──
await open('/law');
await p.locator('textarea').first().fill('This agreement is between A and B. '.repeat(12));
await p.locator('button', { hasText: /analy/i }).first().click();
await p.waitForFunction(() => /structured floor — not model analysis/i.test(document.body.innerText), { timeout: 120000 });
c = await floorChips();
console.log('  law chips:', JSON.stringify(c));
check('law hub: the analysis chip is amber via the helper', c.total >= 1 && c.amber === c.total && c.greenInHouse === 0);

// ── 3. Board of Directors: a provenance MAP chip (was an inline green "served by native×N · in-house") ──
await open('/board');
const askBtn = p.locator('button', { hasText: /instruct|deliberat|convene|ask/i }).first();
const ta = p.locator('textarea').first();
if (await ta.isVisible().catch(() => false)) {
  await ta.fill('Prioritise the halal bakery launch this quarter');
  await askBtn.click();
  await p.waitForFunction(() => /structured floor — not model analysis|native×/i.test(document.body.innerText), { timeout: 180000 });
  c = await floorChips();
  const text = await p.evaluate(() => document.body.innerText);
  console.log('  board chips:', JSON.stringify(c));
  check('board: the map chip is amber via the helper and never says in-house on the floor', c.amber >= 1 && c.greenInHouse === 0 && !/native×\d+ · in-house/i.test(text));
} else {
  console.log('  board: no textarea found — leg skipped honestly');
  check('board: leg skipped (no input on this route)', false);
}

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
