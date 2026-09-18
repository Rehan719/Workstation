// W470 (P1.13 catalogue honesty) — the front doors, the hubs and the marketplace agree with the one registry and the
// catalogue API, in a real browser against the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1). No seed: the
// backend reads this repository's own products/ directory, read-only.
//   node scripts/_w470_probe.mjs http://127.0.0.1:8079
//   · /marketplace: the header counts only what a route serves ("N live products · M registered directories" with the
//     same N and M the API answers), the six signature directories carry the legacy badge and no Open button, a source
//     pointer says so, and there are exactly as many Open buttons as live entries;
//   · /domains and /ai-tools: the same total, from the registry; the catalogue names the tools the old list omitted
//     (hadith, experiment design, marking, safeguarding, legal research, salary) and its link opens the real tab;
//   · /science has no QEP Flagship tab; /religion keeps its real QEP tab.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8079';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const flat = (s) => (s || '').replace(/\s+/g, ' ').trim();

const api = await (await fetch(`${BASE}/api/v1/catalog/products`)).json();
const live = api.products.filter(p => p.live).length;
console.log('  api counts:', JSON.stringify(api.counts), 'live by flag', live);

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
const open = async (path) => {
  await page.goto(`${BASE}${path}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(1500);
  for (let i = 0; i < 3; i++) { await page.keyboard.press('Escape'); await page.waitForTimeout(150); }
};

await open('/marketplace');
await page.waitForSelector('[data-testid="catalog-legacy"]', { timeout: 60000 }).catch(() => {});
const mkt = flat(await page.locator('body').innerText());
const legacyBadges = await page.locator('[data-testid="catalog-legacy"]').count();
const sourceBadges = await page.locator('[data-testid="catalog-source"]').count();
const openButtons = await page.locator('button:has-text("Open")').count();
console.log('  marketplace:', mkt.match(/\d+ live products · \d+ registered directories/i)?.[0], '| legacy', legacyBadges, '| source', sourceBadges, '| Open', openButtons);
check('the marketplace header counts what a route serves, with the API\'s own numbers',
  new RegExp(`${api.counts.live} live products · ${api.counts.registered} registered directories`, 'i').test(mkt)
  && api.counts.live === live && api.counts.live < api.counts.registered && !/\d+ Live Products/.test(mkt));
check('the six signature directories are badged legacy, source pointers say so, and Open exists only for live entries',
  legacyBadges === 6 && legacyBadges === api.counts.legacy && sourceBadges === api.counts.source && openButtons === api.counts.live);

await open('/domains');
const dom = flat(await page.locator('body').innerText());
const total = dom.match(/(\d+) tools across 6 domains/i)?.[1];
await open('/ai-tools');
const cat = flat(await page.locator('body').innerText());
const total2 = cat.match(/(\d+) tools across 6 domains/i)?.[1];
console.log('  domains total', total, '| catalogue total', total2);
const omitted = ['Hadith Study', 'Experiment Designer', 'Marking & Feedback', 'Safeguarding Triage', 'Legal Research (IRAC)', 'Salary & Offer Negotiation', 'Quran Education Platform'];
check('both front doors show the same registry total, and the catalogue names every tool the old list omitted',
  !!total && total === total2 && Number(total) >= 25 && omitted.every(n => cat.includes(n)) && dom.includes('Hadith Study'));

await page.locator('a', { hasText: 'Hadith Study' }).first().click();
await page.waitForFunction(() => /hadith study/i.test(document.body.innerText), null, { timeout: 20000 }).catch(() => {});
const hub = flat(await page.locator('body').innerText());          // innerText carries the CSS uppercase: match /i
console.log('  after the catalogue link:', page.url().replace(BASE, ''), '|', /Hadith Study \(Ulum al-Hadith\)/i.test(hub));
check('a catalogue link opens the hub on that tool\'s tab (the registry title is what the hub mounts)',
  /\/religion\?tab=hadith$/.test(page.url()) && /Hadith Study \(Ulum al-Hadith\)/i.test(hub) && /Study hadith/i.test(hub));

await open('/science');
const sci = flat(await page.locator('body').innerText());
const sciQep = await page.locator('button', { hasText: /qep/i }).count();
await open('/religion');
const relQep = await page.locator('button', { hasText: /qep/i }).count();
console.log('  science qep buttons', sciQep, '| religion qep buttons', relQep);
check('the QEP Flagship tab is gone from Science and stays in Religion', sciQep === 0 && !/QEP/.test(sci) && relQep === 1);

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
