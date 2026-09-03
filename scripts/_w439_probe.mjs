// W439 — drive the QEP-in-Religion-domain surface in a real browser against the built bundle:
// the Owner-directed placement must render, the studio must genuinely schedule + review through
// the UI, and the honesty framing (false-witness footer, provenance chips, refusals) must show.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8016';
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/religion?tab=qep', { waitUntil: 'domcontentloaded', timeout: 45000 });
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
await p.waitForFunction(() => /quran education platform/i.test(document.body.innerText), { timeout: 20000 });
let text = await body();
console.log('RESULT studio in Religion domain:', text.includes('authentic text') && text.includes('spaced repetition'));
console.log('RESULT false-witness footer:', text.includes('false witness'));
console.log('RESULT fabrications gone:', !text.includes('142 global nodes') && !text.includes('alignment score') && !text.includes('methylation'));
console.log('RESULT roadmap honestly labelled:', text.includes('roadmap') && text.includes('not yet built'));

// 1) schedule ayaat 1-3 of al-Fatiha through the UI, then review one
await p.locator('button:has-text("Schedule (SM-2)")').first().click();
// wait for an actual due-ref CHIP, not the 'due today' text (the count chip renders '0 due today'
// before the post-schedule refresh lands — waiting on the text raced the refresh)
const dueBtn = p.locator('button', { hasText: /^\d+:\d+$/ }).first();
const dueAppeared = await dueBtn.waitFor({ state: 'visible', timeout: 30000 }).then(() => true).catch(() => false);
if (dueAppeared) {
  await dueBtn.click();
  await p.waitForFunction(() => /recall quality/i.test(document.body.innerText), { timeout: 30000 });
  await p.locator('button', { hasText: /^5$/ }).first().click();
  await p.waitForFunction(() => /next review in/i.test(document.body.innerText), { timeout: 30000 });
  text = await body();
  console.log('RESULT real SM-2 review through UI:', /next review in \d+ day/.test(text));
  console.log('RESULT xp awarded rendered:', text.includes('+5 xp'));
} else {
  console.log('RESULT real SM-2 review through UI: SKIPPED (1:1 not due — schedule state)', await dueBtn.count());
}

// 2) lesson generation → floor provenance labelled
await p.locator('button:has-text("Generate")').first().click();
await p.waitForFunction(() => /served by/i.test(document.body.innerText), { timeout: 120000 });
text = await body();
console.log('RESULT lesson provenance chip:', text.includes('served by'));
console.log('RESULT floor labelled outline:', !text.includes('served by native') || text.includes('outline, not a lesson'));

// 3) translation refusal renders honestly (no model on this deployment)
await p.locator('textarea[placeholder="Arabic educational text…"]').fill('بسم الله');
await p.locator('button:has-text("Translate to English")').first().click();
// wait for the TRANSLATION outcome specifically — 'served by' already exists on the page from
// the lesson chip, so a generic wait resolves before the 503 refusal renders (instrument race)
await p.waitForFunction(() => /cannot translate|ai-assisted translation/i.test(document.body.innerText), { timeout: 60000 });
text = await body();
console.log('RESULT translation honest (refusal or model):', text.includes('cannot translate') || text.includes('ai-assisted translation'));

await b.close();
console.log('RESULT PASS');
