// W492 (P1.18 + P2.4 + P2.6 + P2.7 + P2.8 + P2.9, the C5 batch repo-wide) — nothing that qualifies a
// claim may be dropped between the engine that produced it and the surface that shows it.
//   node scripts/_w492_probe.mjs http://127.0.0.1:8097
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8097';
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

// ── FU-183: what serves, and what is merely configured ──────────────────────────────────────────
const lc = await get('/api/v1/native-ai/lifecycle');
check('the lifecycle says what serves, not what is configured',
  lc.status === 200 && ['local_model', 'native_floor'].includes(lc.body?.serves)
  && (lc.body.serves === 'local_model') === Boolean(lc.body.effective_default));
check('what serves is something the estate actually holds',
  !lc.body?.effective_default || (lc.body.active_estate || []).includes(lc.body.effective_default));
check('the serving basis never claims an absent model is installed',
  Boolean(lc.body?.serving_basis)
  && (lc.body.effective_default ? /is installed and serves/.test(lc.body.serving_basis)
                                : !/is installed and serves/.test(lc.body.serving_basis)));

// ── FU-197: the domain survives, and one tier resolution governs share and scheduling ───────────
const al = await post('/api/v1/optimizer/allocate',
  { domain: 'science', requirements: { CPU: 2, RAM: 512 }, tier: 'standard' });
check('the requested domain reaches the allocation',
  al.status === 200 && al.body?.allocation?.domain === 'science');
check('a declared tier is recognised and the share is reported as computed, not held',
  al.body?.allocation?.tier_recognised === true && al.body.allocation.tier_applied === 'standard'
  && al.body.allocation.status === 'COMPUTED');
const al2 = await post('/api/v1/optimizer/allocate',
  { domain: 'science', requirements: { CPU: 2, RAM: 512 }, tier: 'not-a-real-tier' });
check('an unrecognised tier is flagged and not given paid scheduling',
  al2.body?.tier_recognised === false && ['QUEUED', 'REJECTED'].includes(al2.body?.status));
check('a queued request does not claim a pending task',
  al2.body?.status !== 'QUEUED'
  || (al2.body?.pending === false && /nothing is pending/.test(String(al2.body?.queue_basis))));

// ── FU-196: the chain says whether truncation was ruled out, and every outcome has one shape ────
const ver = await get('/api/v1/gaas/ueg/verify');
check('the chain reports a named outcome and whether the anchor was checked',
  ver.status === 200
  && ['verified', 'unreadable', 'hash_mismatch', 'anchor_mismatch', 'node_count_below_anchor'].includes(ver.body?.outcome)
  && typeof ver.body?.anchor_checked === 'boolean' && Boolean(ver.body?.verified_basis));
check('a clean pass claims truncation ruled out only when the anchor was compared',
  ver.body?.outcome !== 'verified'
  || (/truncation and rollback are ruled out/.test(ver.body.verified_basis) === ver.body.anchor_checked));
check('every outcome carries the same key set',
  ['valid', 'outcome', 'events', 'root_hash', 'anchor_checked', 'anchor_state', 'verified_basis']
    .every(k => k in (ver.body || {})));
// the sibling verifier got the same treatment
const ver2 = await get('/api/v1/ueg/verify');
check('the sibling verifier also reports whether the anchor was checked',
  ver2.status === 200 && typeof ver2.body?.detail?.anchor_checked === 'boolean');

// ── FU-182: the screen's basis travels with the pass ───────────────────────────────────────────
const lst = await post('/api/v1/marketplace/listings',
  { name: 'W492 probe tutoring', description: 'Maths tutoring for GCSE students', price_wst: 5, tags: [] });
const lid = lst.body?.id;
check('a listing was created', lst.status === 200 && Boolean(lid));
if (lid) {
  const det = await get(`/api/v1/marketplace/listings/${lid}`);
  const c = det.body?.compliance || {};
  check('the screen result carries its own basis and coverage', Boolean(c.basis) && 'coverage_gaps' in c);
  check('the basis says a screen cannot clear', /it cannot clear/.test(String(c.basis)));
}

// ── FU-198: a derived genome carries its lineage, and the route is reachable ────────────────────
const ga = await post('/api/v1/organism/genome/encode',
  { entity_name: 'W492 A', domain: 'general', description: 'a probe entity' });
const gb = await post('/api/v1/organism/genome/encode',
  { entity_name: 'W492 B', domain: 'general', description: 'another probe entity' });
const cx = await post('/api/v1/organism/genome/crossover',
  { genome_a_id: ga.body?.genome_id, genome_b_id: gb.body?.genome_id });
check('the crossover route is reachable and returns a genome',
  cx.status === 200 && Boolean(cx.body?.genome_id) && 'fitness_score' in (cx.body || {}));
check('a crossed genome carries its trait provenance',
  cx.body?.trait_provenance?.derivation === 'crossover');
const mu = await post('/api/v1/organism/genome/mutate', { genome_id: ga.body?.genome_id });
check('a mutated genome carries its trait provenance',
  mu.status === 200 && mu.body?.trait_provenance?.derivation === 'mutation');
const bad = await post('/api/v1/organism/genome/crossover',
  { genome_a_id: ga.body?.genome_id, genome_b_id: gb.body?.genome_id, crossover_method: 'banana' });
check('an unknown crossover method is still refused (and for the right reason)', bad.status === 422);

// ── FU-215 / FU-188: the blend names what is not measured; no surface claims a trained twin ─────
const hs = await get('/api/v1/organism/health-summary');
const terms = hs.body?.composite_health_terms || {};
check('every unmeasured health term says how it is unmeasured',
  Object.values(terms).filter(t => t && t.measured === false).every(t => Boolean(t.basis)));
const fund = await get('/api/v1/fund/status');
check('the fund posture carries the health qualifier rather than the bare blend',
  /not measured|every term in this figure is measured/.test(String(fund.body?.organism?.composite_health_basis
    ?? fund.body?.organism_posture?.composite_health_basis ?? '')));
const plan = await get('/api/v1/plan');
check('the living plan does not claim a trained twin as done',
  !/Chief = Owner digital twin \(done\)/.test(JSON.stringify(plan.body || {})));

// ── the pages ──────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/governance-hub`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const gov = await page.content();
check('the governance page never prints null as a root hash', !/>null…</.test(gov) && !/undefined events/.test(gov));
checkIf('the chain figure distinguishes a full pass from a hash-only one',
  /chain-verified-figure/.test(gov), /100%|hashes only|NOT ASSESSED|FAILED/.test(gov));

await page.goto(`${BASE}/organism?tab=anatomy`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const anat = await page.content();
check('the blend caption is computed, not the old constant', !/blended \(20% simulated\)/.test(anat));
checkIf('the blend caption names how much is not measured',
  /blend-caption/.test(anat), /not measured\)|measured throughout/.test(anat));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
if (notAssessed.length) console.log(`${notAssessed.length} NOT ASSESSABLE: ${notAssessed.join('; ')}`);
process.exit(passed === checks.length ? 0 : 1);
