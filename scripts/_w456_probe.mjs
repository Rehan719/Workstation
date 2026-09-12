// W456 (delivery-plan P1.8) — the tafsir surface completes §11, in a real browser against the built bundle on
// a FRESH backend (AI_DISABLE_LOCAL=1 → the floor serves): /religion?tab=tafsir for 2:1-20 shows the sourced
// Arabic (or the honest "source unreachable" line), the range note (covers 2:1-10), the floor note (no
// translation offered on the floor), the scholar disclaimer, the amber floor badge — and no "Translation"
// heading over floor text.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8047';
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

await p.goto(BASE + '/religion?tab=tafsir', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, null, { timeout: 60000 });
await dismissTour();
await p.waitForFunction(() => /Generate tafsir/i.test(document.body.innerText), null, { timeout: 90000 });
await p.getByLabel(/Surah/i).first().fill('2');
await p.getByLabel(/Ayah \(start\)/i).first().fill('1');
await p.getByLabel(/Ayah \(end/i).first().fill('20');
await p.locator('button', { hasText: /Generate tafsir/i }).first().click();
await p.waitForFunction(() => /Range: range capped at 10 ayaat/i.test(document.body.innerText) || /Request failed|HTTP \d{3}/i.test(document.body.innerText), null, { timeout: 240000 });
console.log('  page has range note:', /Range: range capped/i.test(await body()), '| error text:', ((await body()).match(/Request failed[^\n]*|HTTP \d{3}[^\n]*/) || [''])[0]);
const text = await body();
const extra = await p.evaluate(() => document.querySelector('[data-testid="tafsir-extra"]')?.innerText || '');
const rtl = await p.evaluate(() => { const e = document.querySelector('[data-testid="tafsir-extra"] [dir="rtl"]'); return e ? { arabic: /[؀-ۿ]/.test(e.textContent || ''), lang: e.getAttribute('lang') } : null; });
const pre = await p.evaluate(() => document.querySelector('pre')?.innerText || '');
console.log('  rtl block:', JSON.stringify(rtl), '| extra:', extra.slice(0, 160).replace(/\n/g, ' | '));
check('reference + range note reach the screen: Surah 2:1-10, covers 2:1-10 not the requested end 20', /Surah 2:1-10/i.test(extra) && /covers 2:1-10/i.test(extra));   // innerText carries the CSS uppercase
check('the sourced Arabic renders right-to-left (or the honest source-unreachable line)', (rtl && rtl.arabic && rtl.lang === 'ar') || /source is unreachable/i.test(extra));
check('the Arabic source line names alquran.cloud or says unavailable — never AI-generated', /alquran\.cloud|unavailable/i.test(extra) && /never AI-generated/i.test(extra));
check('the floor note: no translation or transliteration offered on the floor; study with a qualified teacher', /no translation or transliteration is offered/i.test(extra) && /qualified teacher/i.test(extra));
check('withheld on the floor: Transliteration · Translation', /Withheld on the floor: Transliteration · Translation/i.test(extra));
check('the tafsir text carries no Translation / Transliteration heading over floor text', !/^\s*(##\s*)?Translation/mi.test(pre) && !/^\s*(##\s*)?Transliteration/mi.test(pre));
check('the scholar disclaimer and the amber floor badge are on the page', /NOT a scholarly tafsir/i.test(text) && /structured floor — not model analysis/i.test(text));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
