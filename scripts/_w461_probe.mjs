// W461 — transformation stage verification is honest, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1): /transformation → Orchestrate renders the cascade with three states
// (✓ verified · — not assessable · ○ checked and not verified), "n/m assessable", and a badge that says
// VALIDATED only when the run validated; the not-assessable stages carry their basis as a tooltip.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8061';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 1000 } })).newPage();
const dismissTour = async () => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
};

await p.goto(BASE + '/transformation', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => /Orchestrate/i.test(document.body.innerText), null, { timeout: 60000 });
await dismissTour();
let response = null;
p.on('response', async r => { if (r.url().endsWith('/api/v1/transformation/orchestrate') && r.request().method() === 'POST') response = await r.json().catch(() => null); });
await p.locator('button', { hasText: /^\s*Orchestrate\s*$/i }).first().click();
await p.waitForFunction(() => /Transformation Cascade/i.test(document.body.innerText), null, { timeout: 120000 });
await p.waitForTimeout(800);
const text = await p.evaluate(() => document.body.innerText);
const v = response?.validation || {};
console.log('  validation:', JSON.stringify({ stages: v.stages, assessable: v.assessable_stages, verified: v.verified_stages, validated: v.validated }));

const notAssessable = await p.evaluate(() => [...document.querySelectorAll('[aria-label="not assessable"]')].map(e => e.closest('[title]')?.getAttribute('title') || ''));
console.log('  not-assessable rows:', notAssessable.length, '·', notAssessable.map(t => t.slice(0, 60)));
check('the not-assessable stages render as "—" with their basis (the static delegation maps among them)',
  notAssessable.length === (v.stages - v.assessable_stages) && notAssessable.filter(t => /static delegation map/.test(t)).length === 2);
check('the stat reads "verified/assessable assessable", not "verified/all stages"',
  new RegExp(`${v.verified_stages}/${v.assessable_stages} assessable`).test(text));
check('the badge says VALIDATED only because the run validated (and never PARTIAL)',
  v.validated === true ? /\bVALIDATED\b/.test(text) && !/NOT VALIDATED/.test(text.split('Transformation Cascade')[1]?.slice(0, 200) || '') : /NOT VALIDATED/.test(text));
const glyphs = await p.evaluate(() => {
  const card = [...document.querySelectorAll('h3')].find(h => /Transformation Cascade/i.test(h.innerText))?.closest('div.p-6, [class*="rounded"]')?.parentElement;
  const rows = [...(card || document).querySelectorAll('div[title]')].filter(r => /^\d/.test(r.innerText.trim()));
  return { rows: rows.length,
           ticks: rows.filter(r => r.querySelector('svg.text-emerald-400')).length,
           dashes: rows.filter(r => r.querySelector('[aria-label="not assessable"]')).length };
});
console.log('  cascade rows:', JSON.stringify(glyphs));
check('the page paints exactly the verified stages green and the not-assessable ones as dashes',
  glyphs.rows === v.stages && glyphs.ticks === v.verified_stages && glyphs.dashes === v.stages - v.assessable_stages);

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
