// W481 (P1.18 FU-122/FU-231) — the transformation cascade on a FRESH backend: the API by fetch, the
// /transformation page in a real browser against the built bundle.
//   node scripts/_w481_probe.mjs http://127.0.0.1:8089
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8089';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const post = async (p, b) => (await fetch(`${BASE}${p}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(b) })).json();
const dismissTour = async (p) => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(400);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), null, { timeout: 10000 }).catch(() => {});
};

// ── API ──
const r = await post('/api/v1/transformation/orchestrate', { objective: 'w481 probe', scope: 'workstation', owner_id: 'Rehan' });
const st = Object.fromEntries(r.cascade.map(s => [s.step, s]));
check('S1.0 the checks that cannot fail are presence, never verified',
  [1, 2, 3, 4].every(i => st[i].checks === 'presence' && st[i].verified === null));
check('S1.0 stage 7 reports the change-control decision, stage 8 an artifact',
  st[7].checks === 'decision' && st[8].checks === 'artifact');
check('S2.1/S6.0 no delivery check, so the run is NOT ASSESSABLE (not validated)',
  r.validation.validated === null && /DELIVERED/.test(r.validation.validated_basis || '') && r.validation.delivery_verified_stages.length === 0);
check('S6.0 the report no longer claims it ran From Chief To Build-to-Order',
  !/End-to-end transformation cascade ran From Chief To Build-to-Order/.test(r.validation.report));
check('S2.1 a presence-only run leaves the Owner\'s plan alone', r.plan_objective_advanced == null);
const pj = r.digital_twin.projection;
check('S1.1/S2.2/S6.1 a projection with its formula, no verdict, never above the current figure',
  !!pj && !('verdict' in pj) && pj.projected <= pj.current && /not a simulation/.test(pj.note || '') && !('simulation' in r.digital_twin));
const model = await (await fetch(`${BASE}/api/v1/twin/models/${st[8].output.model_id}`)).json();
const m = model.model || model;
check('S8.1 the stored twin is a template, with projections and no trained claim',
  m.trained === false && m.model_type === 'organisational_template' && (m.projections || []).length === 1 && !(m.simulations || []).length);
check('S1.1 no "Chief (owner twin)" component, and the spec names the coverage proxy',
  !m.model_spec.includes('vision_realisation') && m.model_spec.includes('api_surface_coverage')
  && !JSON.stringify(st[8].output.components).toLowerCase().includes('owner twin'));

// ── UI ──
const b = await chromium.launch();
const page = await (await b.newContext({ viewport: { width: 1440, height: 1200 } })).newPage();
await page.goto(`${BASE}/transformation`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1500);
await dismissTour(page);
await page.getByRole('button', { name: /Orchestrate/i }).first().click({ timeout: 20000 }).catch(e => console.log('click failed', String(e).slice(0, 120)));
// this run's own report line is the only text that proves THIS run rendered (the page already lists past runs)
await page.waitForFunction(() => /The cascade ran \d+ stages of the delegation chain/.test(document.body.innerText), null, { timeout: 180000 }).catch(() => {});
const text = await page.evaluate(() => document.body.innerText);
check('S6.0 the page shows NOT ASSESSABLE for a presence-only run, and never a bare VALIDATED',
  /NOT ASSESSABLE/.test(text) && !/(^|\s)VALIDATED(\s|$)/.test(text.replace(/NOT (VALIDATED|ASSESSABLE)/g, '')));
check('S6.1 the Twin sim stat is gone; a projection is shown instead',
  /Twin projection/i.test(text) && !/stable-and-improving/i.test(text));
check('S6.0 the report sentence on the page states what was checked',
  /presence checks that cannot fail/i.test(text));
await page.screenshot({ path: 'C:/tmp/w481p/transformation.png', fullPage: false });
await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
