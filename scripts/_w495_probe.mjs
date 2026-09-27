// W495 (P1.18, the residue batch) — a score nothing computed is not a fitness, a switch wired to
// nothing is not a parameter, and a count map is not a token.
//   node scripts/_w495_probe.mjs http://127.0.0.1:8100
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8100';
const checks = [];
const notAssessed = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
// a check that cannot be made is reported, never folded into the passes
const checkIf = (name, assessable, ok) => {
  if (!assessable) { notAssessed.push(name); console.log(`NOT ASSESSABLE ${name}`); return; }
  checks.push(ok); console.log(`RESULT ${name}:`, ok);
};
const post = async (p, b) => {
  const r = await fetch(`${BASE}${p}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(b) });
  return { status: r.status, body: await r.json().catch(() => null) };
};
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

// ── FU-127 / S8.0: the tournament scores nothing it did not score ────────────────────────────────
const ev = await post('/api/v1/incubator/evolve', {
  name: 'W495 probe', base_prompt: 'Write a launch tagline for a halal bakery',
  domain: 'general', variants: 3, iterations: 2,
});
const lb = ev.body?.leaderboard || [];
check('the tournament answers whether anything scored the variants',
  ev.status === 200 && typeof ev.body?.scored === 'boolean' && typeof ev.body?.winner_basis === 'string');
// the floor scores nothing, so this run is the unscored state; a run that DID score is the other arm
checkIf('an unscored tournament returns no winner, no rank and no fitness',
  ev.body?.scored === false,
  ev.body?.winner === null && lb.length === 3
    && lb.every(v => v.rank === null && v.fitness_score === null && v.scored === false && (v.score_basis || '').length > 20));
checkIf('a scored tournament ranks and scores every row it returns',
  ev.body?.scored === true,
  lb.every(v => typeof v.rank === 'number' && typeof v.fitness_score === 'number'));
check('the tournament names what served it',
  !!ev.body?.ai_provenance && Object.values(ev.body.ai_provenance.served_by || {}).some(n => n > 0));
check('the page-requested generations are the generations run', ev.body?.generations_run === 2);

// the composite must not chart what nothing scored
const comp = await post('/api/v1/reactor/composite', { subject: 'halal bakery in Leeds', domain: 'general', variants: 3 });
check('the composite reports how many variants were scored',
  comp.status === 200 && typeof comp.body?.evolution?.variants_scored === 'number');
checkIf('an unscored composite plots no chart and says why',
  comp.body?.evolution?.scored === false,
  comp.body?.studio === null && comp.body?.evolution?.winner_fitness === null
    && /NO CHART/.test(comp.body?.studio_basis || '') && /NO WINNER/.test(comp.body?.studio_basis || ''));

// ── FU-127 / S8.7: the reactor run carries its provenance and honours the one real parameter ─────
const sse = await fetch(`${BASE}/api/v1/reactor/run`, {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ domain: 'care', params: {}, label: 'care narrative', model: 'native' }),
});
const sseText = await sse.text();
const doneLine = (sseText.split('\n').filter(l => l.includes('"done"')).pop() || '');
let done = null; try { done = JSON.parse(doneLine.slice(6)); } catch { /* keep null */ }
check('the reactor done frame names what served the trace',
  sse.status === 200 && !!done && typeof done.served_by === 'string' && done.served_by.length > 0);
check('the reactor asks for no fabricated measurements',
  !/quality score/i.test(sseText) && !/data volume/i.test(sseText));

// ── FU-127 / S4.2: a count map is not a token ────────────────────────────────────────────────────
const exp = await post('/api/v1/reactor/experiment', {
  subject: 'our halal meal-service pricing model', domain: 'general',
  scenarios: ['Raise prices 10%', 'Hold prices', 'Introduce a budget tier'],
});
const sb = exp.body?.ai_provenance?.served_by;
check('the experiment returns provenance as a count MAP (the shape the badge must handle)',
  exp.status === 200 && !!sb && typeof sb === 'object' && !Array.isArray(sb));
check('the experiment carries a QMS gate verdict under quality.quality_assurance',
  exp.body?.quality_assurance?.quality?.qms_gate_passed !== undefined);

// ── the fabric row forwards the scored count ─────────────────────────────────────────────────────
const cre = await post('/api/v1/resources/compose', {
  name: 'W495 reactor row', resource_ids: ['reactor'], usage_area: 'synthesis',
  config: { reactor: { subject: 'halal bakery in Leeds', variants: 3 } },
});
let fabRow = null;
if (cre.status === 200 && cre.body?.id) {
  const run = await post(`/api/v1/resources/compositions/${cre.body.id}/run`, { objective: 'halal bakery in Leeds' });
  fabRow = (run.body?.real_resource_runs || []).find(r => r.resource === 'reactor') || null;
}
checkIf('the fabric reactor row says how many variants were scored', !!fabRow,
  typeof fabRow?.variants_scored === 'number'
    && (fabRow.variants_scored > 0 || /NO CHART/.test(fabRow.studio_basis || '')));

// ── the pages ────────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
page.on('pageerror', e => console.log('PAGEERROR', e.message));

// /incubator — the unscored tournament as the user sees it
await page.goto(`${BASE}/incubator`, { waitUntil: 'networkidle' });
await dismissTour(page);
await page.locator('button:has-text("New Tournament")').first().click();
await page.locator('input[aria-label="Tournament name"]').fill('W495 page probe');
await page.locator('textarea[aria-label="Base prompt"]').fill('Write a launch tagline for a halal bakery');
const genField = page.locator('input[aria-label="Number of generations"]');
check('the incubator offers the generations the backend honours', await genField.isVisible().catch(() => false));
await page.locator('button:has-text("Create Tournament")').click();
await page.locator('button:has-text("Run Evolution")').click();
await page.locator('text=/No winner/i').first().waitFor({ timeout: 120000 }).catch(() => {});
const incubText = await page.locator('body').innerText();
check('the incubator page states that no variant was scored', /No winner .{0,3} no variant was scored/i.test(incubText));
check('the incubator page shows no invented 95% leaderboard',
  !/\b95%/.test(incubText) && !/\b90%/.test(incubText) && !/\b85%/.test(incubText));
check('the incubator page labels the unranked variants as produced, not ranked',
  /Variants produced \(unranked\)/i.test(incubText) && /not scored/i.test(incubText));
check('the incubator page names what served the run',
  /structured floor/i.test(incubText) || /no model call recorded/i.test(incubText) || /in-house/i.test(incubText));
check('the incubator page prints no Strengths sentence nobody wrote',
  !/Strong analytical depth/i.test(incubText) && !/Could be more concise/i.test(incubText));

// /reactor — the four dead switches are gone and the trace names what wrote it
await page.goto(`${BASE}/reactor`, { waitUntil: 'networkidle' });
await dismissTour(page);
const reactorText = await page.locator('body').innerText();
check('the reactor page offers no switch that is wired to nothing',
  !/Article 1095/i.test(reactorText) && !/Latency Stress/i.test(reactorText)
  && !/Byzantine/i.test(reactorText) && !/In-House Fabric/i.test(reactorText));
check('the reactor page offers the one parameter the run honours',
  await page.locator('#reactor-serving').isVisible().catch(() => false));
check('the reactor page does not call the narrative a real simulation',
  !/Real AI Domain Simulation/i.test(reactorText));
await page.locator('button:has-text("Launch Reactor")').first().click();
await page.locator('text=/Narrative complete/i').first().waitFor({ timeout: 120000 }).catch(() => {});
const ranText = await page.locator('body').innerText();
check('the finished reactor run says what completed and that nothing executed',
  /Narrative complete/i.test(ranText) && /Nothing was executed/i.test(ranText)
  && !/Simulation complete/i.test(ranText));
check('the finished reactor run names what served it',
  /structured floor/i.test(ranText) || /no model call recorded/i.test(ranText) || /in-house/i.test(ranText));

// /fabric — the map-shaped provenance badge on a floor-served experimentation run
await page.goto(`${BASE}/resource-fabric`, { waitUntil: 'networkidle' });
await dismissTour(page);
// each resource card is a select-button with a small Run button beside it inside div.relative; the
// card is itself a <button>, so a has-text("Run") locator matches the CARD and only selects it
const expRun = page.locator('div.relative', { hasText: 'Reactor · Experimentation' })
  .locator('button:text-is("Run")').first();
if (await expRun.count()) await expRun.click().catch(() => {});
await page.waitForTimeout(1000);
const runBtn = page.locator('button:has-text("Run experiment")').first();
const panelOpen = await runBtn.isVisible().catch(() => false);
// the submit stays disabled until the primary field is filled, so the subject is entered first
if (panelOpen) await page.locator('textarea').first().fill('our halal meal-service pricing model').catch(() => {});
const canRun = panelOpen && await runBtn.isEnabled().catch(() => false);
console.log('fabric: the experimentation run panel is open:', panelOpen, '| runnable:', canRun);
if (canRun) {
  await runBtn.click();
  await page.locator('text=/Result/').first().waitFor({ timeout: 180000 }).catch(() => {});
  await page.waitForTimeout(3000);
}
const fabText = canRun ? await page.locator('body').innerText() : '';
checkIf('the floor-served experimentation result is not badged as an in-house model', canRun,
  !/\[object Object\]/.test(fabText) && !/in-house · \[object/.test(fabText));
checkIf('the floor-served experimentation result names the floor', canRun, /structured floor/i.test(fabText));
checkIf('the experimentation result carries its QMS verdict', canRun, /QMS/.test(fabText));

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed` + (notAssessed.length ? `; ${notAssessed.length} not assessable: ${notAssessed.join(', ')}` : ''));
process.exit(passed === checks.length ? 0 : 1);
