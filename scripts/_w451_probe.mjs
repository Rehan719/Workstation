// W451 (delivery-plan P1.3) — the AI CEO chat on the fabric, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1 → the floor serves): the default tab of the Living Organisation hub
// must answer through the owned gateway with per-message provenance (amber floor badge), a pill that reads
// from that provenance (never "Planetary Strategy Active"), no persona/roleplay copy, and no canned
// offline advisory.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8031';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
const ROLEPLAY = /planetary strategy|galactic|guardian|sovereign mesh|offline mode|multi-dimensional/i;

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

// ── 1. /ceo (the hub's default tab): no roleplay copy, no hard-wired pill ──
await p.goto(BASE + '/ceo', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
await dismissTour();
let text = await body();
check('default tab: no persona / roleplay copy and no "Planetary Strategy Active" pill before any answer', !ROLEPLAY.test(text) && /no answer yet/i.test(text));

// ── 2. ask the CEO: the answer streams from the fabric and says the floor served it ──
await p.locator('input[placeholder*="Ask the AI CEO" i]').first().fill('What should we prioritise this quarter?');
await p.keyboard.press('Enter');
await p.waitForFunction(() => /structured floor — not model analysis/i.test(document.body.innerText) && !/Synthesis in progress/i.test(document.body.innerText), { timeout: 120000 });
text = await body();
const badges = (text.match(/structured floor — not model analysis/gi) || []).length;
console.log('  floor badges on page:', badges);
check('answer: per-message amber floor badge + the pill reads from provenance', badges >= 2);
check('answer: grounded-in line names the record it drew on', /grounded in \d+ directives? · \d+ objectives? · scope workstation/i.test(text));
check('answer: no roleplay, no canned advisory, no invented articles', !ROLEPLAY.test(text) && !/Article \d+/.test(text));
const t0 = Date.now();
const evs = await p.evaluate(async () => {
  const r = await fetch('/api/v138/ceo/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: 'status of the plan?' }) });
  const txt = await r.text();
  return txt.split('\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)));
});
console.log('  api: events', evs.length, 'in', Date.now() - t0, 'ms; final =', JSON.stringify(evs[evs.length - 1]).slice(0, 160));
check('api: the terminal frame carries served_by=native + grounding and the stream is not char-by-char theatre',
  evs[evs.length - 1]?.done === true && evs[evs.length - 1]?.served_by === 'native' && !!evs[evs.length - 1]?.grounding && evs.length < 400 && (Date.now() - t0) < 15000);
const tools = await p.evaluate(async () => (await fetch('/api/v138/ceo/tools/register?name=x&description=y', { method: 'POST' })).status);
check('api: the lambda tool-registration route is gone', tools === 404 || tools === 405);

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
