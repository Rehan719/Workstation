// W464 — the Owner's rulings of 2026-09-14, in a real browser against the built bundle on a FRESH backend
// (AI_DISABLE_LOCAL=1, ECONOMY_MATERIALITY_WST=1000; virtual WST only):
//   · FU-012: a HIGH change a review approved shows "awaiting Board ratification" on /change-control with no Implement;
//     /implement refuses it; the Board page lists it, keeps Ratify/Refuse disabled until the decision is recorded as the
//     Owner's direction, and ratifying (then refusing another) moves the records; (stubbed, labelled) a refused
//     ratification call is shown as a refusal, never a success;
//   · FU-013: each decision lands on the constitutional ledger, classified (approval awaiting ratification → review,
//     ratified → recorded, refused → flagged);
//   · FU-014: a material economy hold is CRITICAL — the economy page sends the Owner to the Sanctum (never "review it"),
//     /change-control offers no review of it, and a Sanctum vote releases the cycle.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8071';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const TAG = Date.now().toString(36);
const VSB = `w464-probe-${TAG}`;

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const p = await ctx.newPage();
const dismissTour = async (page) => {
  for (let i = 0; i < 3; i++) {
    const skip = page.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await page.keyboard.press('Escape');
    await page.waitForTimeout(300);
    if (!(await page.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
};
const api = (page, path, body) => page.evaluate(async ([path, body]) => {
  const r = await fetch(path, body === undefined ? {} : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  return { status: r.status, json: await r.json().catch(() => null) };
}, [path, body]);
const record = async (id) => (await api(p, `/api/v1/cca/${id}`)).json;
const ccaRow = (page, title) => page.locator('div.bg-white\\/4', { has: page.getByText(title, { exact: true }) }).first();
const boardRow = (page, id) => page.locator('[data-testid="board-ratification-row"]', { has: page.locator(`text=${id}`) }).first();
const ledger = async (id) => ((await api(p, '/api/v1/gaas/ueg/events?limit=500')).json?.events || [])
  .filter(e => (e.data || {}).cca_id === id);

await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('text=Change Control Agency', { timeout: 60000 });
await dismissTour(p);

// ── FU-012: a review approves a HIGH change — it waits for the Board ──
const submitHigh = async (label) => {
  const title = `W464 probe ${label} ${TAG}`;
  const sub = await api(p, '/api/v1/cca/submit', { title, change_type: 'code_change', description: 'w464 probe', submitted_by: 'w464-probe' });
  const rv = await api(p, `/api/v1/cca/${sub.json?.cca_id}/review`, { reviewer_notes: 'w464 probe — a review' });
  return { title, id: sub.json?.cca_id, tier: sub.json?.impact_tier, review: rv.json };
};
const A = await submitHigh('ratify');
console.log('  review A:', A.tier, A.review?.status, A.review?.decision_source, 'awaiting', A.review?.awaiting_board_ratification);
check('a code_change is HIGH, and a review\'s approval of it waits for Board ratification',
  A.tier === 'HIGH' && A.review?.status === 'approved' && ['model_decision_marker', 'health_threshold_rule'].includes(A.review?.decision_source)
  && A.review?.awaiting_board_ratification === true && A.review?.ueg_logged === true);

await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector(`text=${A.title}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const rowA = ccaRow(p, A.title);
await rowA.locator('div.cursor-pointer').first().click();
await p.waitForSelector('[data-testid="cca-awaiting-ratification"]', { timeout: 30000 }).catch(() => {});
const awaitingLink = await rowA.locator('[data-testid="cca-awaiting-ratification"]').innerText().catch(() => '');
const awaitingHref = await rowA.locator('[data-testid="cca-awaiting-ratification"]').getAttribute('href').catch(() => '');
const decidedLine = await rowA.locator('[data-testid="cca-decision-source"]').innerText().catch(() => '');
const implementA = await rowA.locator('button:has-text("Implement")').count();
const awaitingTab = await p.locator('button:has-text("Awaiting Board")').innerText().catch(() => '');
console.log('  row A:', awaitingLink, '|', decidedLine, '| tab:', awaitingTab.replace(/\n/g, ' '));
const implA = await api(p, `/api/v1/cca/${A.id}/implement?force=true`, {});   // a POST (no body is a GET)
check('/change-control shows it awaiting Board ratification with no Implement, and /implement (even forced) refuses it',
  /awaiting Board ratification/.test(awaitingLink) && awaitingHref === '/ceo?tab=board' && implementA === 0
  && /awaiting Board ratification/.test(decidedLine) && /Awaiting Board\s*\d+/.test(awaitingTab)
  && implA.status === 409 && /ratif/i.test(implA.json?.detail || '') && (await record(A.id))?.status === 'approved');

// ── the Board page ──
const B = await submitHigh('refuse');
await p.goto(`${BASE}/ceo?tab=board`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('[data-testid="board-ratifications"]', { timeout: 60000 }).catch(() => {});
await p.waitForSelector(`[data-testid="board-ratification-row"]:has-text("${A.id}")`, { timeout: 30000 }).catch(() => {});
await dismissTour(p);
const rA = boardRow(p, A.id);
const rowTextA = await rA.innerText().catch(() => '');
const ratifyBtn = rA.locator('[data-testid="board-ratify"]');
const disabledBefore = await ratifyBtn.isDisabled().catch(() => false);
const duty = await p.locator('[data-testid="board-ratification-duty"]').innerText().catch(() => '');
console.log('  board row A:', rowTextA.replace(/\n/g, ' | ').slice(0, 240));
check('the Board page lists the change with what approved it, and Ratify stays disabled until it is recorded as the Owner\'s direction',
  rowTextA.includes(A.title) && /approved by: the (reviewing model|organism-health threshold rule)/.test(rowTextA)
  && /§17\.5 pre-validation:/.test(rowTextA) && disabledBefore === true && /ratif/i.test(duty));

// (stubbed, labelled) the backend refuses the ratification: the page shows the refusal, never a success
const ps = await ctx.newPage();
await ps.route(`**/api/v1/board/ratifications/${A.id}`, r => r.fulfill({ status: 403, contentType: 'application/json',
  body: JSON.stringify({ detail: 'Only an admin may record a Board ratification decision.' }) }));
await ps.goto(`${BASE}/ceo?tab=board`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await ps.waitForSelector(`[data-testid="board-ratification-row"]:has-text("${A.id}")`, { timeout: 60000 }).catch(() => {});
await dismissTour(ps);
await boardRow(ps, A.id).locator('[data-testid="board-ratification-owner-direction"]').check();
await boardRow(ps, A.id).locator('[data-testid="board-ratify"]').click();
await ps.waitForFunction(() => /HTTP 403/.test(document.body.innerText), null, { timeout: 30000 }).catch(() => {});
const stubText = await boardRow(ps, A.id).innerText().catch(() => '');
check('(stubbed 403) a refused ratification is shown as the refusal, and the change still waits',
  /Failed \(HTTP 403\): Only an admin/.test(stubText) && !/RATIFIED/.test(stubText) && (await record(A.id))?.status === 'approved'
  && (await record(A.id))?.board_ratification == null);
await ps.close();

await rA.locator('[data-testid="board-ratification-owner-direction"]').check();
await ratifyBtn.click();
await p.waitForFunction(() => /RATIFIED/.test(document.querySelector('[data-testid="board-ratification-result"]')?.innerText || ''), null, { timeout: 30000 }).catch(() => {});
const ratResult = await p.locator('[data-testid="board-ratification-result"]').innerText().catch(() => '');
const recA = await record(A.id);
const stillListed = await p.locator(`[data-testid="board-ratification-row"]:has-text("${A.id}")`).count();
console.log('  ratified:', ratResult);
check('Ratify records the Board decision on the Owner\'s direction, leaves the queue, and says it reached the ledger',
  /RATIFIED/.test(ratResult) && /constitutional ledger/.test(ratResult) && stillListed === 0
  && recA?.board_ratification?.decision === 'ratified' && recA?.board_ratification?.on_owner_direction === true
  && recA?.awaiting_board_ratification === false);

const rB = boardRow(p, B.id);
await rB.locator('[data-testid="board-ratification-owner-direction"]').check();
await rB.locator('[data-testid="board-refuse"]').click();
await p.waitForFunction(async (id) => (await (await fetch(`/api/v1/cca/${id}`)).json()).status === 'rejected', B.id, { timeout: 30000, polling: 500 }).catch(() => {});
const recB = await record(B.id);
const implB = await api(p, `/api/v1/cca/${B.id}/implement`, {});
check('Refuse rejects the change (decided by the Board\'s refusal) and it can never be implemented',
  recB?.status === 'rejected' && recB?.decision_source === 'board_refusal' && implB.status === 400);
const implA2 = await api(p, `/api/v1/cca/${A.id}/implement`, {});
const recA2 = await record(A.id);
console.log('  implement A after ratification:', implA2.status, implA2.json?.detail || implA2.json?.status);
check('after ratification /implement no longer answers "awaiting ratification"',
  !/ratif/i.test(implA2.json?.detail || '') && (implA2.status === 200 ? recA2?.status === 'implemented' : implA2.status === 409));

// ── FU-013: the decisions are on the ledger, classified ──
const evA = await ledger(A.id), evB = await ledger(B.id);
const lvl = (evs, type) => evs.filter(e => e.data?.type === type).map(e => e.flag?.level);
console.log('  ledger A:', evA.map(e => `${e.data?.type}:${e.flag?.level}`).join(', '), '| B:', evB.map(e => `${e.data?.type}:${e.flag?.level}`).join(', '));
check('each decision is one ledger node, classified: approval awaiting ratification → review, ratified → recorded, refused → flagged',
  JSON.stringify(lvl(evA, 'cca.change_approved')) === '["review"]' && JSON.stringify(lvl(evA, 'board.change_ratified')) === '["recorded"]'
  && JSON.stringify(lvl(evB, 'board.change_ratification_refused')) === '["flagged"]');

// ── FU-014: a material economy hold is CRITICAL, and the Owner decides it in the Sanctum ──
await p.goto(`${BASE}/economy?vsb=${VSB}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
await dismissTour(p);
const runCycle = async (amount) => {
  await dismissTour(p);
  await p.locator('label:has-text("Revenue (WST, virtual)") + input').fill(String(amount));
  await p.locator('label:has-text("Costs (WST, virtual)") + input').fill('0');
  const resp = p.waitForResponse(r => r.url().endsWith('/api/v1/economy/cycle') && r.request().method() === 'POST', { timeout: 60000 });
  await p.locator('button:has-text("Run Metabolic Cycle")').click({ timeout: 30000 });
  const body = await (await resp).json();
  await p.waitForTimeout(400);
  return body;
};
const held = await runCycle(5000);
const hold = held.governance?.cca_id;
const sanctumLine = await p.evaluate(() => document.querySelector('[data-testid="hold-held-sanctum"]')?.innerText || '');
const economyText = await p.evaluate(() => document.body.innerText);
console.log('  economy line:', sanctumLine);
check('a material cycle files a CRITICAL hold and the economy page sends the Owner to the Sanctum, never to request a review',
  held.cycle === null && held.governance?.impact_tier === 'CRITICAL' && sanctumLine.includes(hold) && /Sovereign Sanctum/.test(sanctumLine)
  && !/review it on the/i.test(economyText) && /awaiting the Owner's decision/i.test(economyText));

const TITLE = `[economy] material distribution — ${VSB}`;
await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const rowH = ccaRow(p, TITLE);
const rowHText = await rowH.innerText().catch(() => '');
await rowH.locator('div.cursor-pointer').first().click();
await p.waitForSelector('[data-testid="cca-economy-sanctum-note"]', { timeout: 30000 }).catch(() => {});
check('/change-control shows the hold as CRITICAL, offers no review of it, and names where the Owner decides it',
  /CRITICAL/.test(rowHText) && (await rowH.locator('button:has-text("Request review")').count()) === 0
  && /decided only by the Owner — in the Governance hub’s Sovereign Sanctum/.test(await rowH.locator('[data-testid="cca-economy-sanctum-note"]').innerText().catch(() => '')));

await p.goto(`${BASE}/governance-hub`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('button:has-text("The Sanctum")', { timeout: 60000 });
await dismissTour(p);
await p.locator('button:has-text("The Sanctum")').click();
await p.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const card = p.locator('div.glass-card', { has: p.getByText(TITLE, { exact: true }) }).first();
// the toast is transient: watch for it (and the vote's own response) from before the click
const voteResp = p.waitForResponse(r => r.url().endsWith(`/api/v1/cca/${hold}/review`) && r.request().method() === 'POST', { timeout: 60000 });
const toastWatch = p.waitForFunction(() => [...document.querySelectorAll('[data-workstation-toast]')].some(t => /and the constitutional ledger/.test(t.textContent || '')), null, { timeout: 60000, polling: 100 }).then(() => true).catch(() => false);
await card.locator('button:has-text("Sovereign Approve")').click();
const voteBody = await (await voteResp).json().catch(() => ({}));
const toastSeen = await toastWatch;
console.log('  vote response: ueg_logged', voteBody?.ueg_logged, 'status', voteBody?.status);
await p.waitForFunction(async (id) => (await (await fetch(`/api/v1/cca/${id}`)).json()).status === 'approved', hold, { timeout: 30000, polling: 500 }).catch(() => {});
const aside = await p.evaluate(() => document.body.innerText);
const recH = await record(hold);
const ran = (await api(p, '/api/v1/economy/cycle', { vsb_id: VSB, revenue: 5000, costs: 0 })).json;
console.log('  sanctum vote:', recH?.status, recH?.decision_source, '| toast seen:', toastSeen, '| cycle ran:', !!ran?.cycle);
check('a Sanctum vote is the Owner\'s explicit decision: it approves the hold (no pre-validation), says it reached the ledger, and the cycle runs',
  recH?.status === 'approved' && recH?.decision_source === 'admin_override' && !recH?.twin_prevalidation && toastSeen
  && /when that write lands, on the constitutional ledger/.test(aside) && !/and written to the constitutional ledger/.test(aside)
  && ran?.cycle != null);

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
