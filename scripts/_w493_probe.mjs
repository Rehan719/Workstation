// W493 (P1.18 + P2.4 + P2.9, the C4 batch repo-wide) — a present-tense claim about a process must be
// backed by that process actually running, and a control names what it does.
//   node scripts/_w493_probe.mjs http://127.0.0.1:8098
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8098';
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

// ── the levers a page reads before it says "self-running" ────────────────────────────────────────
const hb = await get('/api/v1/heartbeat/status');
const LEVERS = ['auto_evolve', 'auto_economy', 'auto_align', 'auto_compliance', 'auto_ship'];
check('the heartbeat reports every lever a page names', hb.status === 200 && LEVERS.every(k => k in (hb.body || {})));
check('and whether the process itself is running', typeof hb.body?.running === 'boolean');
const leversOn = LEVERS.filter(k => hb.body?.[k] === true);

// ── FU-165: a generation happens on APPLY, never on filing ───────────────────────────────────────
const est = await post('/api/v1/genesis/establish',
  { problem: 'w493 probe venture', ship_output: false, name: 'W493 Probe Co' });
const vid = est.body?.vsb_id;
const before = (await get(`/api/v1/vsb/${vid}`)).body?.generation ?? 0;
const pack1 = await post(`/api/v1/vsb/${vid}/board-pack`, {});
const ev = await post(`/api/v1/vsb/${vid}/evolve`, { trigger: 'w493 probe' });
check('a filed cycle applies nothing', ev.status === 200 && ev.body?.applied === false);
check('and advances no generation', ev.body?.generation === before
  && ((await get(`/api/v1/vsb/${vid}`)).body?.generation ?? 0) === before);
check('the generation figure says what it counts',
  /a filed cycle/.test(String(ev.body?.generation_basis || '')));
check('the cycle that DID run is counted', Number(ev.body?.evolution_cycles_run || 0) >= 1);
check('the outcome names what THIS cycle produced, not a pointer it inherited',
  ev.body?.pending_cca_is_from_an_earlier_cycle === false
  && ['proposals_filed_pending_approval', 'proposals_not_filed', 'no_proposals'].includes(ev.body?.outcome));
check('a filing says the mutation waits on approval',
  ev.body?.outcome !== 'proposals_filed_pending_approval'
  || (Boolean(ev.body?.evolution_pending_cca) && /approves/.test(String(ev.body?.outcome_basis || ''))));
// a second cycle must not report the first cycle's pointer as its own filing
const ev2 = await post(`/api/v1/vsb/${vid}/evolve`, { trigger: 'w493 probe second' });
check('a second cycle is honest about a pointer it inherited',
  ev2.body?.outcome !== 'proposals_filed_pending_approval' || ev2.body?.pending_cca_is_from_an_earlier_cycle === false);
check('an inherited pointer is reported as inherited',
  ev2.body?.pending_cca_is_from_an_earlier_cycle !== true || ev2.body?.outcome === 'no_proposals_pending_earlier_cycle');
// the apply with nothing approved must still answer with the keys every reader uses
const ap = await post(`/api/v1/vsb/${vid}/evolution/apply`, {});
check('a no-op apply answers with the keys a reader needs',
  ['applied', 'cca_id', 'generation'].every(k => k in (ap.body || {})));
check('a no-op apply never claims the generation advanced',
  ap.body?.generation_advanced !== true);

// ── the board pack versions on the evolution state that actually moved ───────────────────────────
const pack2 = await post(`/api/v1/vsb/${vid}/board-pack`, {});
checkIf('a filed cycle changes the board pack, because the cycle count moved',
  pack1.status === 200 && pack2.status === 200 && Boolean(pack1.body?.content_hash),
  pack2.body?.content_hash !== pack1.body?.content_hash);

// ── FU-176: mapping is not acting ────────────────────────────────────────────────────────────────
const al = await post('/api/v1/cognition/align', { execute: false });
check('a mapping pass returns a list, not an absent field',
  Array.isArray(al.body?.gaps_routed) && Array.isArray(al.body?.executed));
check('and executes nothing while execute is false',
  al.body.executed.length === 0 && al.body.gaps_routed.every(g => g?.executed === false));

// ── the pages ────────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const home = await page.content();
check('the landing page no longer calls the organism self-running outright',
  !/generated end-to-end, self-running, in-house/.test(home));
const leverText = await page.locator('[data-testid="autonomy-levers"]').first().innerText().catch(() => '');
checkIf('the landing page states the lever position it read', Boolean(leverText),
  leversOn.length === 0 ? /none is on|could not be read/.test(leverText)
                        : new RegExp(leversOn[0]).test(leverText) || /could not be read/.test(leverText));
await page.goto(`${BASE}/organism?tab=cognition`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const cog = await page.content();
check('the cognition page does not claim it self-aligns', !/self-aligns<\/span>:/.test(cog));
check('it says mapping only', /Mapping only: naming an owner is not acting on it/.test(cog));
checkIf('and when the lever is off the page says so',
  hb.body?.auto_align === false, /the lever is OFF/.test(cog));

await page.goto(`${BASE}/ceo?tab=swarm`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(1200);
const swarm = await page.content();
check('the swarm page never declares itself online', !/Swarm intelligence online/.test(swarm));
check('the feed is not presented as a live stream', !/Emergence Event Stream/.test(swarm));
// with a live backend the read succeeds, so the UNREADABLE panels must be absent and no panel may
// claim emptiness while the first read is still out
const swarmState = await page.evaluate(() => ({
  unreadable: Boolean(document.querySelector('[data-testid="swarm-runs-unreadable"], [data-testid="swarm-runs-panel-unreadable"], [data-testid="cascade-runs-unreadable"]')),
  loading: Boolean(document.querySelector('[data-testid="emergence-loading"]')),
  empty: Boolean(document.querySelector('[data-testid="swarm-runs-empty"]')),
}));
check('a readable run list is not reported as unreadable', swarmState.unreadable === false);
check('the feed does not claim empty and loading at once', !(swarmState.loading && swarmState.empty));

await page.goto(`${BASE}/vsb-cockpit?tab=transform`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(1400);
const ck = await page.content();
check('the cascade control does not claim a twin simulation',
  /no twin model is simulated/.test(ck) && !/simulated on a digital twin/.test(ck));

await page.goto(`${BASE}/vsb-cockpit?tab=economy`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(1400);
const cke = await page.content();
check('the endowment rule stated is the rule that exists',
  !/the endowment base is protected/.test(cke) && /requires a non-zero capital_fund/.test(cke));

await page.goto(`${BASE}/economy?tab=overview`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const econ = await page.content();
check('the economy surface says one entity per beat', !/re-screens every entity each beat/.test(econ));

await page.goto(`${BASE}/employment`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const hub = await page.content();
check('a saved preference badge says it gates nothing yet',
  /no affordance on this hub is gated on it yet/.test(hub));
// the disclosure travels with the badge in the DOM: the shared Badge used to drop `title` silently
const titled = await page.evaluate(() =>
  Array.from(document.querySelectorAll('[title]')).some(e => /saved pref|gated on it yet/i.test(e.getAttribute('title') || '')));
checkIf('a badge disclosure carried as a tooltip reaches the DOM',
  /MODE \(saved pref\.\)/.test(hub), titled);

await page.goto(`${BASE}/contribute`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(700);
const cb = await page.content();
check('the contribute page names the bodies that exist',
  /governed by the Board and Change Control/.test(cb)
  && !/Steering Committee/.test(cb) && !/AI-led Council/.test(cb));

await page.goto(`${BASE}/settings`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(700);
const st = await page.content();
check('settings does not claim the preferences drive affordances',
  !/guidance and tone drive the affordances shown on the domain hubs/.test(st)
  && /nothing yet changes with them/.test(st));

// the state the whole fix is about: a lever SET while the process is STOPPED. It cannot be observed
// on a default backend (levers off, heartbeat beating), so the probe drives it rather than skipping it.
await post('/api/v1/heartbeat/configure', { auto_align: true });
await post('/api/v1/heartbeat/stop', {});
const hb2 = await get('/api/v1/heartbeat/status');
await page.goto(`${BASE}/`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const leverText2 = await page.locator('[data-testid="autonomy-levers"]').first().innerText().catch(() => '');
checkIf('a set lever with a stopped heartbeat is not called running',
  hb2.body?.auto_align === true && hb2.body?.running === false && Boolean(leverText2),
  /STOPPED/.test(leverText2) && !/Self-running levers on/.test(leverText2));

// and the cognition page, which carries the same claim, says the same thing in the same state
await page.goto(`${BASE}/organism?tab=cognition`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(900);
const cog2 = await page.content();
checkIf('the cognition page says the lever is on but the heartbeat is stopped',
  hb2.body?.auto_align === true && hb2.body?.running === false,
  /the lever is on but the heartbeat is STOPPED/.test(cog2));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
if (notAssessed.length) console.log(`${notAssessed.length} NOT ASSESSABLE: ${notAssessed.join('; ')}`);
process.exit(passed === checks.length ? 0 : 1);
