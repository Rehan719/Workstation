// W494 (P1.18, the gate's own batch) — a verdict is not an assessment if it cannot come out otherwise,
// and a figure is decided on what was measured.
//   node scripts/_w494_probe.mjs http://127.0.0.1:8100
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
const get = async (p) => {
  const r = await fetch(`${BASE}${p}`);
  return { status: r.status, body: await r.json().catch(() => null) };
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

// ── FU-116 / FU-110: the mode is the measured score's mode, whatever the blend says ──────────────
const st = await get('/api/v1/organism/status');
const m = st.body?.composite_health_measured_only;
const expected = (v, cycle) => (v >= 0.8 && cycle === 'ACTIVE_FOCUS') ? 'FULL_POWER'
  : v >= 0.5 ? 'NOMINAL' : v >= 0.2 ? 'DEGRADED' : 'EMERGENCY';
check('the organism reports a measured-only score and the weight it covers',
  st.status === 200 && typeof m === 'number' && typeof st.body.composite_health_measured_weight === 'number');
check('the mode is the one the MEASURED score implies, not the blend',
  st.body?.mode === expected(m, st.body?.systems?.circadian?.cycle ?? st.body?.circadian?.cycle));
check('and it says so', /MEASURED-only/.test(String(st.body?.mode_basis || '')));
check('the blended figure carries its basis',
  /is measured/.test(String(st.body?.composite_health_basis || '')));
// the blend could not have refused: with self-healing untracked it cannot fall below 0.4
checkIf('the blend is demonstrably higher than the measured score it replaced',
  typeof st.body?.composite_health === 'number' && m < 1,
  st.body.composite_health > m);

// ── FU-117: the metabolic term only rises, so nothing may gate on it ────────────────────────────
const hs = await get('/api/v1/organism/health-summary');
const met = st.body?.systems?.metabolic ?? st.body?.metabolic;
checkIf('the metabolic term says it cannot fall', Boolean(met), met?.can_fall === false && met?.measured === false);
checkIf('and says thresholds written against it cannot fire', Boolean(met?.basis), /cannot fire/.test(met.basis));
check('the health summary states the measured share',
  /of the composite's weight is measured/.test(String(hs.body?.health_summary ?? st.body?.health_summary ?? '')));

// ── FU-107: a governance gate that can refuse ───────────────────────────────────────────────────
const cca = await post('/api/v1/cca/submit', { change_type: 'config_minor', title: 'w494 probe',
  description: 'a LOW change, to read the health gate', rationale: 'the gate must name what decided' });
check('the change record carries a health gate that names what decided it',
  cca.status === 200 && (await get(`/api/v1/cca/${cca.body.cca_id}`)).body?.health_gate?.decided_on
    === 'composite_health_measured_only');

// ── FU-109: a viability verdict that can come out otherwise ─────────────────────────────────────
const petri = await post('/api/v1/petri/culture',
  { specimen: 'sell ice to penguins at a premium, financed with riba loans', domain: 'enterprise' });
check('a floor-served culture is not judged viable',
  petri.status === 200 && petri.body?.viable === null && /NOT ASSESSABLE/.test(petri.body?.viable_basis || ''));

// ── FU-139: "connected" counts mounted routes ───────────────────────────────────────────────────
const wir = await get('/api/v1/cognition/wiring');
check('the wiring figure says it is not a measurement',
  wir.body?.coherence_measured === false && /MOUNTED-ROUTE count/.test(wir.body?.coherence_basis || ''));
check('every tier says what its tick means',
  (wir.body?.tiers || []).every(t => Boolean(t.connected_basis)));

// ── FU-141: whose breaker ───────────────────────────────────────────────────────────────────────
const gaas = await get('/api/v1/gaas/status');
check('the breaker figures name every driver they cover',
  Array.isArray(gaas.body?.circuit_breaker_covers)
  && gaas.body.circuit_breaker_covers.includes('POST /api/v1/gaas/intercept')
  && gaas.body.circuit_breaker_covers.some(c => /resource fabric/.test(c))
  && /not a platform-wide/.test(gaas.body?.circuit_breaker_scope || '')
  && !/and nothing else/.test(gaas.body?.circuit_breaker_scope || ''));

// ── FU-103: an efficiency verdict with one reachable branch is withheld ──────────────────────────
// (read through the cascade, which is where it is shown)
const casc = await post('/api/v1/swarm/cascade', { mission: 'w494 probe: a small community tool library', scope: 'workstation' });
const bms = casc.body?.management_systems?.bms;
checkIf('the BMS efficiency verdict is withheld, with its reason', Boolean(bms),
  bms.status === 'not_assessed' && bms.status_measured === false && /can only ever come out/.test(bms.status_basis || ''));
// ── FU-130: the intent gate says what it screened ───────────────────────────────────────────────
checkIf('the cascade verdict says the delivery was not screened', Boolean(casc.body?.governance),
  casc.body.governance.content_screened === false && /content was NOT screened/.test(casc.body.governance.scope || ''));
checkIf('and it keeps every key its readers depend on', Boolean(casc.body?.governance),
  ['status', 'checkpoint', 'node', 'arms_length'].every(k => k in casc.body.governance));

// ── FU-135: a voter that could not assess abstains ──────────────────────────────────────────────
const tree = await post('/api/v1/native-ai/tree', { goal: 'w494 probe: a halal compliance review service' });
const val = tree.body?.validation;
checkIf('a floor-served synthesis is not certified as integrated', Boolean(val),
  val.integrated === null && /NOT ASSESSABLE/.test(val.integrated_basis || ''));

// ── FU-147: BUILT means a passed gate ───────────────────────────────────────────────────────────
const cat = await get('/api/v1/catalog/products');
const slug = (cat.body?.products || cat.body?.items || []).find(p => p?.live)?.slug;
const bto = slug ? await post('/api/v1/bto/build',
  { entity_name: 'W494 Probe Co', product_resources: [slug], domain: 'enterprise' }) : { body: null };
checkIf('a composed document is not counted as delivered', Boolean(bto.body?.built?.length),
  bto.body.built.every(b => b.status !== 'BUILT' || b.qms_gate_passed === true)
  && typeof bto.body.delivered_basis === 'string');

// ── the pages ───────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const home = await page.content();
check('the landing page prints the measured figure', /% measured health/.test(home));
checkIf('and names the blend as the blend', /home-composite-health-basis/.test(home),
  /The blended composite is/.test(home) && !/of that figure is not measured/.test(home));

await page.goto(`${BASE}/organism`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const org = await page.content();
check('the organism headline is the measured figure', /composite-health-headline/.test(org) && /measured/.test(org));
check('and the mode says what decided it', /mode-basis/.test(org));
check('the hub caption names the blend', !/of this figure is not measured/.test(org));

await page.goto(`${BASE}/organism?tab=cognition`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const cog = await page.content();
check('the wiring count is not printed as a coherence percentage', !/% coherence/.test(cog));
check('it says what it counts', /tiers have a route mounted/.test(cog));

await page.goto(`${BASE}/ceo?tab=swarm`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(1200);
const swarm = await page.content();
check('the chart no longer calls its axis measured', !/QMS coverage vs run duration \(measured\)/.test(swarm));
checkIf('the BMS chip carries its simulated label', /bms-chip/.test(swarm), /\(sim\)/.test(swarm));
checkIf('the cascade verdict is not painted as a judgement', /cascade-gov-chip/.test(swarm),
  /intent gate:/.test(swarm) && /content not screened/.test(swarm));

// the breaker card lives on the Constitution tab; the hub opens on Governance, and a probe that
// never renders the region reports a true claim as false (the same miss as W493's cockpit tabs)
await page.goto(`${BASE}/governance-hub?tab=constitution`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const gov = await page.content();
check('the breaker card states its scope on the card', /gaas-breaker-scope/.test(gov) && /These figures cover/.test(gov));

await page.goto(`${BASE}/solutions`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const sol = await page.content();
check('the platform page names no engine that does not exist',
  !/V9 Engine/.test(sol) && !/Real-time mission telemetry/.test(sol));
check('and it does not claim a readiness nothing tested', !/Readiness check PASSED/.test(sol));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
if (notAssessed.length) console.log(`${notAssessed.length} NOT ASSESSABLE: ${notAssessed.join('; ')}`);
process.exit(passed === checks.length ? 0 : 1);
