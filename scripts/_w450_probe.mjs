// W450 (delivery-plan P1.2) — drive the flagship flow in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1 → the floor serves every gateway call): a Genesis journey that
// establishes on completion must NOT ship under a fallback name; the newborn card asks the founder
// to name the enterprise; naming ships the body; the shipped site and the Cockpit Plan tab carry the
// founder's words plus an honest pending state — and zero engine vocabulary anywhere.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8029';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
const ENGINE = /INKASHAF|SAMAJH|\bSOCH\b|\bAQAL\b|native structured|acting as:|structured [a-z -]+frame for|VSB — /i;

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
const body = () => p.evaluate(() => document.body.innerText);
const open = async (path) => {
  await p.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
  await dismissTour();
};

// ── 1. Genesis → establish on completion: a slug name marked pending, nothing shipped under it ──
await open('/genesis');
await p.locator('textarea').first().fill('I keep 40 beehives in Somerset and lose colonies to varroa every winter and cannot afford lab testing');
await p.getByLabel('Establish living VSB on completion').check();
await p.locator('button', { hasText: /Launch Journey → Establish VSB/ }).first().click();
await p.waitForFunction(() => /working name — pending yours/i.test(document.body.innerText), { timeout: 300000 });
let text = await body();
const vid = (text.match(/vsb-[0-9a-f]{10}/) || [])[0];
console.log('  newborn:', vid, '| name line:', (text.match(/\n([^\n]*)\nworking name/i) || [])[1]);
// (a placeholder is not innerText — check the visible copy and the button, rule 22)
check('newborn card: working name pending, the founder is asked to name it', /Name the enterprise and its body ships/i.test(text) && /Name & ship/.test(text) && !!vid);
check('newborn card: no fallback "VSB — <problem>" name anywhere on the page', !/VSB — I keep/i.test(text));
check('newborn card: the pending body fields are named', /Pending the owned model: .*concept/i.test(text));
const shipBefore = await p.evaluate(async (id) => (await fetch(`/api/v1/vsb/${id}/repo/ship`)).status, vid);
check('nothing shipped under the slug (ship manifest absent)', shipBefore === 404);

// ── 2. Name & ship ──
await p.getByLabel('Enterprise name').last().fill('Somerset Hive Health');
await p.locator('button', { hasText: /^Name & ship$/ }).first().click();
await p.waitForFunction(() => !/working name — pending yours/i.test(document.body.innerText) && /Somerset Hive Health/.test(document.body.innerText), { timeout: 240000 });
const shipped = await p.evaluate(async (id) => await (await fetch(`/api/v1/vsb/${id}/repo/ship`)).json(), vid);
check('naming ships the body as one coherent whole', shipped?.coherent_whole === true && shipped?.stale === false);
const index = await p.evaluate(async (id) => await (await fetch(`/api/v1/vsb/${id}/website/page/index`)).text(), vid);
const about = await p.evaluate(async (id) => await (await fetch(`/api/v1/vsb/${id}/website/page/about`)).text(), vid);
console.log('  index bytes:', index.length, '| about has pending:', /content pending the owned model/.test(about));
check('shipped site: the founder\'s name and words, an honest pending state, zero engine vocabulary',
  /Somerset Hive Health/.test(index) && /beehives in Somerset/.test(index) && /content pending the owned model/.test(about)
  && !ENGINE.test(index) && !ENGINE.test(about) && !/quality-gated/.test(index));

// ── 3. Generate VSB Repository after the ship: the site is not regressed ──
await p.locator('button', { hasText: /Generate VSB Repository/ }).first().click();
await p.waitForFunction(() => /file/i.test(document.body.innerText), { timeout: 120000 });
await p.waitForTimeout(1500);
const index2 = await p.evaluate(async (id) => await (await fetch(`/api/v1/vsb/${id}/website/page/index`)).text(), vid);
const ship2 = await p.evaluate(async (id) => await (await fetch(`/api/v1/vsb/${id}/repo/ship`)).json(), vid);
check('re-generating the repo leaves the shipped site byte-identical and the ship fresh', index2 === index && ship2?.stale === false);

// ── 4. Cockpit Plan tab: the body's provenance badged, pending fields named, no scaffold ──
await open(`/vsb-cockpit?vsb=${vid}&tab=plan`);
await p.waitForFunction(() => /pending the owned model/i.test(document.body.innerText), { timeout: 60000 });
text = await body();
check('cockpit plan tab: floor badge + pending fields, founder\'s words, no engine scaffold',
  /pending the owned model: .*concept/i.test(text) && /structured floor — not model analysis/i.test(text)
  && /beehives in Somerset/i.test(text) && !ENGINE.test(text));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
