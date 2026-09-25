// W491 (P1.18 + P2.4 + P2.6 + P2.8 + P2.9, the C10 batch repo-wide) — a count or a list says what
// population it covers and what actually happened in it.
//   node scripts/_w491_probe.mjs http://127.0.0.1:8096
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8096';
const checks = [];
const notAssessed = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
// W491 refutation - a probe check whose disjunction is satisfied by the fix being ABSENT passes
// precisely when the thing it guards is missing. A check that cannot be made is reported as not
// assessable and counted separately - never folded into the passes.
const checkIf = (name, assessable, ok) => {
  if (!assessable) { notAssessed.push(name); console.log(`NOT ASSESSABLE ${name}: nothing on this page to assess`); return; }
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

// ── a requisition says what it DID, and the counters cover one population ────────────────────────
const casc = await post('/api/v1/swarm/cascade', {
  mission: 'verify regulatory compliance and optimise compute resource allocation', domain: 'enterprise' });
const fr = casc.body?.fabric_requisitions || [];
check('the cascade requisitioned resources', casc.status === 200 && fr.length > 0);
check('no requisition claims a run it cannot back', fr.every(f => !('ran' in f)));
check('every requisition says what kind it is',
  fr.every(f => ['status_read', 'query', 'facility_run'].includes(f.kind) && f.kind_phrase && f.endpoint));
check('every handler is reported as invoked in-process', fr.every(f => f.invocation === 'in_process'));
const sm = casc.body?.fabric_requisitions_summary;
check('the counters cover exactly the requisitioned population',
  sm && sm.requisitioned === fr.length
  && sm.facilities_ran + sm.state_read + sm.blueprints_drafted
     + sm.failed + sm.outcome_not_recorded === sm.requisitioned);
check('the counters count outcomes, and say so',
  /an attempt that raised is neither a run nor a read/.test(String(sm?.basis)));
const ms = casc.body?.management_systems || {};
check('the catalogue is no longer reported as a record of operation', !('integrated' in ms));
check('the catalogue and what operated are separate lists',
  Array.isArray(ms.catalogue) && Array.isArray(ms.operated_this_run)
  && ms.operated_this_run.every(x => ms.catalogue.includes(x))
  && !ms.operated_this_run.includes('backbone'));
check('the operated list says on what basis', /gate returned a verdict/.test(String(ms.operated_basis)));

// ── whose git history the panel shows ───────────────────────────────────────────────────────────
const gh = await get('/api/v1/workstation/git-history?limit=3');
check('the log says whose history it is',
  gh.body?.subject === 'workstation_platform_source' && gh.body?.is_user_project_activity === false);
// (the round's first version asserted `readable === (unreadable_reason === null)`, which restates the
//  server's own line and is true for every possible response - a check that cannot fail)
check('the log states its readability as a boolean with a reason when false',
  typeof gh.body?.readable === 'boolean'
  && (gh.body.readable ? gh.body.unreadable_reason === null : Boolean(gh.body.unreadable_reason)));
check('the log says a user\'s project activity is not tracked here',
  /a user's own project activity is not tracked here/.test(String(gh.body?.basis)));

// ── the books count their own cycles ───────────────────────────────────────────────────────────
const living = await get('/api/v1/economy/living-vsbs');
const rows = living.body?.living_vsbs || [];
check('the roster names what its own tally covers',
  rows.length === 0 || rows.every(r => /autonomous roster/.test(String(r.operating_cycles_basis))));
check('each roster row carries the books\' count or says it could not be read',
  rows.length === 0 || rows.every(r => typeof r.ledger_cycles === 'number'
    || (r.ledger_cycles === null && r.ledger_cycles_unavailable)));
check('the listing says the two counts are different things',
  /`operating_cycles` is this roster's own tally/.test(String(living.body?.cycle_counts_basis)));

// ── the refutation's fixes, over the live API ─────────────────────────────────────────────
// a failure is a field, not a string dressed as content
const aq = await post('/api/v1/ai/query', { query: 'w491 probe' });
check('the ai/query route reports its outcome as a field',
  aq.status === 200 && typeof aq.body?.ok === 'boolean'
  && (aq.body.ok === (aq.body.error === null)));
check('a failed call is not returned as the answer',
  aq.body?.answer === null || !/^\[unavailable:/.test(String(aq.body?.answer)));

// the delegate card reports what RAN, against what was asked and the cap
const dl = await post('/api/v1/swarm/delegate', {
  task: 'w491: report what ran', domain: 'enterprise',
  agent_ids: ['CFO', 'CTO', 'CMO', 'COO', 'CLO', 'CSO'] });
check('the delegate card reports what ran, not what was requested',
  dl.status === 200
  && Array.isArray(dl.body?.agents_engaged) && Array.isArray(dl.body?.agents_requested)
  && dl.body.agents_requested.length === 6
  && dl.body.agents_engaged.length < dl.body.agents_requested.length
  && dl.body.agents_engaged.length === Object.keys(dl.body.agent_responses || {}).length);
check('the agents that did not run are named',
  Array.isArray(dl.body?.agents_not_run) && dl.body.agents_not_run.length > 0
  && /runs at most/.test(String(dl.body?.agents_engaged_basis)));

// a page of commits is not a total
check('the commit log separates the page it fetched from the repository count',
  !Object.prototype.hasOwnProperty.call(gh.body || {}, 'total')
  && gh.body?.returned <= gh.body?.limit
  && (gh.body?.repository_commits_total === null
      || gh.body.repository_commits_total > gh.body.returned));

// ── the pages ──────────────────────────────────────────────────────────────────────────────────
const browser = await chromium.launch();
const page = await browser.newPage();
const crashes = [];
page.on('pageerror', e => crashes.push(String(e)));

await page.goto(`${BASE}/`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
// the fourth column opens on the history tab
const dock = page.locator('[data-testid="git-history-heading"]').first();
if (!(await dock.isVisible().catch(() => false))) {
  await page.locator('button[title="History"], button[aria-label="History"]').first().click().catch(() => {});
  await page.waitForTimeout(700);
}
const home = await page.content();
check('the platform\'s own commit log is not labelled as the user\'s project activity',
  !/Recent Project Activity/.test(home));
const chan = await page.evaluate(() => {
  const ctrls = Array.from(document.querySelectorAll('[aria-label="Channels"], [title="Channels"]'));
  return { found: ctrls.length, animating: ctrls.filter(c => c.querySelector('.animate-eq-bar')).length };
});
checkIf('no Channels control animates as though it were measuring traffic',
  chan.found > 0, chan.animating === 0);
// and the one place bars DO animate is the idle voice visualiser, which says Idle beside them
const voice = await page.evaluate(() => {
  const bar = document.querySelector('.animate-eq-bar');
  if (!bar) return { present: false };
  const box = bar.closest('div')?.parentElement;
  return { present: true, grey: bar.className.includes('text-slate-700'),
           labelled: /idle|listening|speaking/i.test(box?.textContent || '') };
});
checkIf('an animating bar is greyed and labelled with its state',
  voice.present, voice.grey && voice.labelled);

await page.goto(`${BASE}/organism?tab=swarm`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const swarmText = await page.content();
check('the swarm page no longer heads its requisitions as all having RAN',
  !/requisitioned\s*&amp;\s*RAN/.test(swarmText) && !/requisitioned & RAN/.test(swarmText));

// establish one VSB so the living roster has a row - otherwise the roster check is unassessable and
// the page's own count claim never gets exercised
await post('/api/v1/genesis/establish',
  { problem: 'w491 probe courier venture', ship_output: false, name: 'W491 Probe Co' });
// the roster lives on the Economy centre's default tab (/economy), not a standalone route
await page.goto(`${BASE}/economy`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(800);
const econ = await page.content();
checkIf('the roster row distinguishes its own tally from the books',
  /roster-cycles-/.test(econ),
  /roster cycles/.test(econ) && /on the books/.test(econ));

await page.goto(`${BASE}/solutions`, { waitUntil: 'networkidle' }).catch(() => {});
await dismissTour(page);
await page.waitForTimeout(600);
const sol = await page.content();
check('the model control is labelled as a note, not a chooser',
  /AI model note/.test(sol) && !/>AI Model</.test(sol));

check('no page crashed while probing', crashes.length === 0);

await browser.close();
const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} checks passed`);
if (notAssessed.length) console.log(`${notAssessed.length} NOT ASSESSABLE: ${notAssessed.join('; ')}`);
process.exit(passed === checks.length ? 0 : 1);
