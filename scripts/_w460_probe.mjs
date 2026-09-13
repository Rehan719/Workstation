// W460 (delivery-plan P1.12) — the Visual Composer is retired and no surface claims compliance nobody
// evaluated, in a real browser against the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1):
//   · the built bundle carries none of the retired claims ("GaaS COMPLIANT", the fictional model names,
//     "Current session conforms to", "Every action is governed", "GaaS Alignment");
//   · /visual-composer and /ceo?tab=composer both land on /native-ai?focus=cascade-designer, and the
//     designer is on screen even when the fabric status call fails;
//   · the Living Organisation hub has no Composer tab and links to the designer;
//   · the designer refuses to save a cascade with no complete stage, saves and runs a real one;
//   · a blocked constitutional action shows FLAGGED in the Governance Hub; a harmless one shows CHAINED.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const BASE = process.argv[2] || 'http://localhost:8060';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };

// 1 — the built bundle
const assets = 'apps/workstation-superapp/dist/assets';
const js = fs.readdirSync(assets).filter(f => f.endsWith('.js')).map(f => fs.readFileSync(path.join(assets, f), 'utf-8')).join('\n');
const gone = ['GaaS COMPLIANT', 'Nematron', 'Nemoclaw', 'Current session conforms to', 'Every action is governed', 'GaaS Alignment'];
const found = gone.filter(s => js.includes(s));
console.log('  retired strings still in the bundle:', found);
check('the built bundle carries none of the retired claims, and does carry the real designer', found.length === 0 && js.includes('Design a bespoke swarm cascade'));

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } });
const p = await ctx.newPage();
const dismissTour = async () => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(300);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
};
const api = (u, body) => p.evaluate(async ([u, body]) => {
  const r = await fetch(u, body ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) } : undefined);
  return { status: r.status, body: await r.json().catch(() => null) };
}, [u, body || null]);

// 2 — both retired routes land on the designer
for (const route of ['/visual-composer', '/ceo?tab=composer']) {
  await p.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => !!document.getElementById('cascade-designer'), null, { timeout: 60000 }).catch(() => {});
  await dismissTour();
  // the page scrolls once its loading settles (the status call can take ~3 s on a cold model probe) —
  // wait for the OUTCOME (in view), not for the element to exist
  await p.waitForFunction(() => { const r = document.getElementById('cascade-designer')?.getBoundingClientRect(); return !!r && r.top < window.innerHeight && r.bottom > 0; }, null, { timeout: 20000 }).catch(() => {});
  const url = p.url();
  const inView = await p.evaluate(() => { const r = document.getElementById('cascade-designer')?.getBoundingClientRect(); return !!r && r.top < window.innerHeight && r.bottom > 0; });
  console.log(`  ${route} → ${url} · designer in view: ${inView}`);
  check(`${route} lands on the real cascade designer`, url.includes('/native-ai?focus=cascade-designer') && inView);
}

// the designer survives a failed status call
const p2 = await ctx.newPage();
await p2.route('**/api/v1/native-ai/status', r => r.abort());
await p2.goto(BASE + '/native-ai?focus=cascade-designer', { waitUntil: 'domcontentloaded', timeout: 45000 });
const survives = await p2.waitForFunction(() => !!document.getElementById('cascade-designer'), null, { timeout: 60000 }).then(() => true).catch(() => false);
check('the designer still renders when the fabric status call fails', survives);
await p2.close();

// 3 — the hub
await p.goto(BASE + '/ceo', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => !!document.querySelector('[data-testid="swarm-designer-link"]'), null, { timeout: 60000 }).catch(() => {});
await dismissTour();
const tabs = await p.evaluate(() => [...document.querySelectorAll('button')].map(x => x.innerText.trim().toUpperCase()).filter(t => ['AI CEO', 'BOARD', 'SWARM', 'AGENT HUB', 'COMPOSER'].includes(t)));
const link = await p.evaluate(() => document.querySelector('[data-testid="swarm-designer-link"]')?.getAttribute('href'));
console.log('  hub tabs:', tabs, '· link:', link);
check('the hub has no Composer tab and links to the designer', !tabs.includes('COMPOSER') && tabs.includes('AI CEO') && link === '/native-ai?focus=cascade-designer');

// 4 — the designer refuses an empty cascade, saves and runs a real one
await p.goto(BASE + '/native-ai?focus=cascade-designer', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => !!document.getElementById('cascade-designer'), null, { timeout: 60000 });
await dismissTour();
const card = p.locator('#cascade-designer');
const removeBtns = card.locator('button[aria-label^="Remove stage"]');
while (await removeBtns.count()) { await removeBtns.first().click(); }
const saveBtn = card.locator('button', { hasText: /Save cascade/i });
check('Save is disabled while the cascade has no complete stage', await saveBtn.isDisabled());
const emptyApi = await api('/api/v1/resources/swarm/define', { name: 'w460 empty', stages: [] });
check('the API refuses an empty cascade (400) with the reason', emptyApi.status === 400 && /at least one stage/i.test(emptyApi.body?.detail || ''));
await card.locator('button', { hasText: /Add stage/i }).click();
await card.locator('input[placeholder="role"]').first().fill('analyst');
await card.locator('input[placeholder="instruction for this agent…"]').first().fill('List the top three risks of a community meal service.');
await card.locator('input[placeholder="Cascade name…"]').fill('W460 probe cascade');
await saveBtn.click();
await p.waitForFunction(() => /W460 probe cascade/.test(document.body.innerText), null, { timeout: 30000 }).catch(() => {});
const saved = (await api('/api/v1/resources/swarm')).body;
const mine = (Array.isArray(saved) ? saved : saved?.swarms || saved?.cascades || []).find(c => c.name === 'W460 probe cascade');
console.log('  saved cascade:', mine?.id, mine?.stages?.length);
const ran = mine ? await api('/api/v1/resources/swarm/run', { swarm_id: mine.id }) : { status: 0 };
check('a real cascade saves from the page and runs', !!mine && mine.stages.length === 1 && ran.status === 200);

// 5 — the Governance Hub flags what is adverse and chains what is not
await api('/api/v1/gaas/intercept', { action_type: 'w460_probe', requires_human: true, human_approved: false });
await p.goto(BASE + '/governance-hub', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => /UEG Events/i.test(document.body.innerText), null, { timeout: 60000 }).catch(() => {});
await dismissTour();
await p.waitForTimeout(1500);
const flaggedRow = await p.evaluate(() => [...document.querySelectorAll('div')].some(d => /POLICY_GATE_HALT|CIRCUIT_BREAKER_TRIP/i.test(d.innerText) && /FLAGGED/.test(d.innerText) && d.innerText.length < 400));
check('a blocked action’s halt reads FLAGGED in the Governance Hub', flaggedRow);
await api('/api/v1/gaas/breaker/reset', {});
await api('/api/v1/gaas/intercept', { action_type: 'w460_harmless_probe' });
await p.reload({ waitUntil: 'domcontentloaded' });
await p.waitForTimeout(2500);
const chained = await p.evaluate(() => [...document.querySelectorAll('.event-level')].map(e => ({ t: e.innerText, cls: e.className })));
console.log('  level badges:', chained.slice(0, 4));
check('a genuinely allowed action reads CHAINED, and nothing recorded is painted green', chained.some(c => /CHAINED/i.test(c.t)) && chained.filter(c => /CHAINED/i.test(c.t)).every(c => !/emerald/.test(c.cls)));
await api('/api/v1/gaas/breaker/reset', {});

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
