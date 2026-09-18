// W471 (P1.14 Board pack + Chief's Opening honesty) — in a real browser against the built bundle on a FRESH backend
// (AI_DISABLE_LOCAL=1: every generation is the native floor). No seed.
//   node scripts/_w471_probe.mjs http://127.0.0.1:8080
//   · /business-plan?scope=w471-probe: "Chief: AI-Generate" on the floor writes NOTHING — the page says so, the opening
//     card wears no badge (nothing was written) and names the five pending fields; the owner-edit form (POST /business-plan/set)
//     sets a concept, it shows as owner-edited and leaves the pending list;
//   · a bare birth's board pack says it is grounded in the founder's problem statement, not a concept (API), and
//     an entity with a concept assembled three times shows one version (API: the ACCEPT clause).
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8080';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const flat = (s) => (s || '').replace(/\s+/g, ' ').trim();
const SCOPE = `w471-probe-${Date.now()}`;   // a fresh plan scope every run
const post = (path, body) => fetch(`${BASE}${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });

// ── the board pack, at the API ──
const bare = await (await post('/api/v1/genesis/establish', { problem: 'w471 probe bare', domain: 'care', name: 'W471ProbeBare' })).json();
const barePack = await post(`/api/v1/vsb/${bare.vsb_id}/board-pack`);
const bareBody = await barePack.json().catch(() => ({}));
console.log('  bare pack:', barePack.status, bareBody.concept_source, String(bareBody.concept_note).slice(0, 80));
check('a bare birth\'s pack says it is grounded in the founder\'s problem statement — no concept recorded yet',
  barePack.status === 200 && bareBody.concept_source === 'challenge' && /no concept recorded yet/.test(String(bareBody.concept_note)));
const withC = await (await post('/api/v1/genesis/establish', { problem: 'w471 probe', domain: 'care', name: 'W471ProbeCo',
  concept: 'halal meal boxes', design: 'd', commercialisation: 'subscription' })).json();
const packs = [];
for (let i = 0; i < 3; i++) packs.push(await (await post(`/api/v1/vsb/${withC.vsb_id}/board-pack`)).json());
const hist = await (await fetch(`${BASE}/api/v1/vsb/${withC.vsb_id}/board-packs`)).json();
console.log('  versions:', packs.map(p => p.version).join(','), '| unchanged:', packs.map(p => p.unchanged).join(','), '| history versions', hist.versions, 'of', hist.total);
check('three assemblies of an unchanged entity show ONE version, unchanged since the first (ACCEPT)',
  packs.every(p => p.version === 1 && p.unchanged === true) && hist.versions === 1 && hist.total >= 3
  && packs[0].quality_assurance.quality.delivery_coverage === 0);

// ── the Chief's Opening, in the browser ──
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
await page.goto(`${BASE}/business-plan?scope=${SCOPE}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.waitForTimeout(1500);
for (let i = 0; i < 3; i++) { await page.keyboard.press('Escape'); await page.waitForTimeout(150); }
await page.locator('button', { hasText: /AI-Generate/i }).first().click();
await page.waitForSelector('[data-testid="plan-generate-note"]', { timeout: 60000 }).catch(() => {});
const note = flat(await page.locator('[data-testid="plan-generate-note"]').innerText().catch(() => ''));
const badge = flat(await page.locator('[data-testid="plan-provenance"]').innerText().catch(() => ''));
const pending = flat(await page.locator('[data-testid="plan-pending"]').innerText().catch(() => ''));
const plan = await (await fetch(`${BASE}/api/v1/business-plan?scope=${SCOPE}`)).json();
console.log('  note:', note.slice(0, 90), '| badge:', badge, '| pending:', pending.slice(0, 120));
check('on the floor the Chief writes nothing: the page says so, the opening wears NO badge (nothing was written) and names the pending fields',
  /structured floor/i.test(note) && /nothing was written/i.test(note) && badge === ''
  && /pending the owned model/i.test(pending) && ['executive_summary', 'concept', 'vision', 'mission', 'strategy'].every(f => pending.includes(f))
  && plan.executive_summary === '' && plan.concept === '');

await page.locator('[data-testid="plan-owner-edit-open"]').click();
await page.waitForSelector('[data-testid="plan-owner-edit"]', { timeout: 10000 });
await page.locator('[data-testid="plan-edit-concept"]').fill('Weekly halal meal boxes for students, set by the founder.');
await page.locator('[data-testid="plan-owner-edit-save"]').click();
await page.waitForFunction(() => document.querySelector('[data-testid="plan-owner-edited"]') !== null, null, { timeout: 15000 }).catch(() => {});
const after = await (await fetch(`${BASE}/api/v1/business-plan?scope=${SCOPE}`)).json();
const edited = await page.locator('[data-testid="plan-owner-edited"]').count();
const pending2 = flat(await page.locator('[data-testid="plan-pending"]').innerText().catch(() => ''));
const card = flat(await page.locator('[data-testid="chiefs-opening"]').innerText().catch(() => ''));
console.log('  after edit: concept =', JSON.stringify(after.concept).slice(0, 60), '| owner-edited chips', edited, '| pending:', pending2.slice(0, 100));
check('the owner-edit surface sets the concept through /business-plan/set: shown owner-edited, no longer pending',
  after.concept.startsWith('Weekly halal meal boxes') && after.owner_edits && after.owner_edits.concept
  && edited >= 1 && !pending2.includes('concept') && /Weekly halal meal boxes/i.test(card));

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
