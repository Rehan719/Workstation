// W475 (P1.17 The second truth pass) — the fourteen ledger-v4 entries, the UI halves in a real browser against the
// built bundle on a FRESH backend (AI_DISABLE_LOCAL=1), the API halves by fetch. No seed.
//   node scripts/_w475_probe.mjs http://127.0.0.1:8084
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8084';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const j = async (path, opts) => { const r = await fetch(`${BASE}${path}`, opts); return { status: r.status, body: await r.json().catch(() => ({})) }; };
const post = (path, body) => j(path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });

// ── API halves ──
const avoids = await post('/api/v1/compliance/check', { subject: 'A UK savings app compliant with Sharia that avoids riba and offers profit-sharing' });
const sh = (avoids.body.verdicts || []).find(v => v.framework === 'sharia_halal') || {};
check('R1.0 a subject that AVOIDS riba is review, not fail, with the phrase quoted', sh.status === 'review' && /avoids riba/.test(sh.reason || '') && avoids.body.overall !== 'fail');
const offered = await post('/api/v1/compliance/check', { subject: 'fund it via riba interest-bearing loans' });
check('R1.0 an offered haram term still fails', offered.body.overall === 'fail');
const tf = await post('/api/v1/religion/quran-tafsir', { surah: 2, ayah_start: 285, ayah_end: 286 });
check('R1.1 the floor tafsir body carries no Arabic (the sourced text stands apart)', !/[؀-ۿ]/.test(tf.body.tafsir || '') && !/AUTHENTIC ARABIC TEXT/.test(tf.body.tafsir || ''));
const qms = await post('/api/v1/mgmt/qms/generate', { organisation_name: 'Zed Bakery', domain: 'food', products_services: 'sourdough bread' });
check('R1.2 the QMS document carries provenance and a floor note', !!(qms.body.ai_provenance && qms.body.ai_provenance.served_by && qms.body.ai_provenance.floor_note));
const est = await post('/api/v1/genesis/establish', { problem: 'probe living text', domain: 'enterprise', name: 'ProbeLivingCo', concept: 'c', design: 'd', commercialisation: 'm' });
check('R2.0 establishment says the economy lever is OFF instead of "tends"', est.body.living && est.body.living.autonomous_cycles === false && /OFF/.test(est.body.living.autonomous_operation || ''));
const lst = await j('/api/v1/economy/living-vsbs');
check('R2.0 the roster listing says whether any cycle runs', lst.body.autonomous_cycles === false && /Self-run/.test(lst.body.autonomous_cycles_note || ''));
const tree = await post('/api/v1/native-ai/tree', { goal: 'Plan a halal bakery launch' });
const tg = (tree.body.governance || {}).qms_passed, td = tree.body.decision || {};
check('R4.1 no proceed on a gate that could not assess', tg !== null || (td.recommendation === null && /not assessable/.test(td.basis || '')));
const sim = await post('/api/v1/resources/compose/simulate', { name: 'probe-rig', resource_ids: ['bdp', 'cognitive_cascade'], usage_area: 'design' });
check('R4.2 commit_ready is null when the gate could not assess', sim.body.simulation && sim.body.simulation.quality.qms_gate_passed === null && sim.body.commit_ready === null);
const cat = await j('/api/v1/catalog/products');
check('R5.0 enterprise-file-hub is not counted live', (cat.body.products || []).every(p => !(p.slug === 'enterprise-file-hub' && p.status === 'live')));
const real = await j('/api/v1/transformation/realisation');
check('R6.0 the realisation figure names what it measures', /API surface coverage/.test(real.body.measure || ''));

// ── UI halves (served bundle) ──
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
const bundleTexts = [];
page.on('response', async (res) => { if (/\/assets\/.*\.js$/.test(res.url())) { try { bundleTexts.push(await res.text()); } catch { /* ignore */ } } });
await page.goto(`${BASE}/`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1500);
const all = bundleTexts.join('\n');
const gone = ['WebRTC stream synchronized', 'Sovereign Avatar Active', 'Resonance drop predicted', 'Energy surplus detected', 'Digital Twin of ${', 'overall realised'];
const there = ['no stream connected', 'No forecast is computed', 'nothing was calibrated', 'gate could not assess', 'API surface coverage', 'no digital-twin model is trained', 'not assessable'];
console.log('  bundle chunks read:', bundleTexts.length, '| gone:', gone.map(s => !all.includes(s)).join(','), '| there:', there.map(s => all.includes(s)).join(','));
check('the served bundle carries none of the invented readings', bundleTexts.length > 0 && gone.every(s => !all.includes(s)));
check('the served bundle carries the honest lines in their place', there.every(s => all.includes(s)));
await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
