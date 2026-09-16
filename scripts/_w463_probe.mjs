// W463 — economy approvals release only what they were filed for, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1, ECONOMY_MATERIALITY_WST=1000; virtual WST only):
//   · /economy: a material cycle is held; after a rejection the same cycle says it is asked again when the action
//     changes; a changed cycle files a fresh hold that records the rejection it follows, and the page says such a
//     hold is decided in the Sanctum (a review does not decide it);
//   · The Sanctum lists that hold from the moment it is filed, with its amount and what an approval releases;
//   · /change-control shows the hold's amount; a review holds it for an explicit decision and the page says where
//     that decision is made; (W464) the page offers no review of an economy hold at all — it is CRITICAL, decided by
//     the Owner in the Sanctum — and the API still refuses a review whose amount moved (409, nothing decided); an
//     approved economy hold offers no Implement (running its action releases it);
//   · (stubbed, labelled) a Sanctum vote on an amount the hold no longer carries is refused and shown; a real vote
//     approves it and the cycle then runs once;
//   · (stubbed, labelled) a transfer that posted before its gate raised, and one the gate allowed that was retried,
//     each say so.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8067';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const VSB = `w463-probe-${Date.now().toString(36)}`;
const CCA_VSB = `${VSB}-cca`;
const TITLE = `[economy] material distribution — ${VSB}`;

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
const openSanctum = async (page) => {
  await page.goto(`${BASE}/governance-hub`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('button:has-text("The Sanctum")', { timeout: 60000 });
  await dismissTour(page);
  await page.locator('button:has-text("The Sanctum")').click();
  await page.waitForSelector('text=THE SANCTUM', { timeout: 60000 });
};
// W464 — exact title matches: every economy hold is CRITICAL now, so the Sanctum also lists the hold filed for
// `${VSB}-cca`, whose title starts with this one (a substring match picked that card)
const cardOf = (page) => page.locator('div.glass-card', { has: page.getByText(TITLE, { exact: true }) }).first();
const ccaRow = (page, title) => page.locator('div.bg-white\\/4', { has: page.getByText(title, { exact: true }) }).first();

// ── /economy: held → rejected → asked again ──
await p.goto(`${BASE}/economy?vsb=${VSB}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
await dismissTour(p);
const revenue = p.locator('label:has-text("Revenue (WST, virtual)") + input');
const costs = p.locator('label:has-text("Costs (WST, virtual)") + input');
const runCycle = async (amount) => {
  await dismissTour(p);                                     // the onboarding tour can open late and cover the page
  await revenue.fill(String(amount));
  await costs.fill('0');                                    // the page defaults costs to 1000
  const resp = p.waitForResponse(r => r.url().endsWith('/api/v1/economy/cycle') && r.request().method() === 'POST', { timeout: 60000 });
  await p.locator('button:has-text("Run Metabolic Cycle")').click({ timeout: 30000 });
  const body = await (await resp).json();
  await p.waitForTimeout(400);
  return body;
};
const first = await runCycle(5000);
const holdA = first.governance?.cca_id;
const pageA = await p.evaluate(() => document.body.innerText);
check('a material cycle is held on the page, naming its change request',
  first.cycle === null && !!holdA && /Held for Change Control/i.test(pageA) && pageA.includes(holdA));
const rej = await api(p, `/api/v1/cca/${holdA}/review`, { override_decision: 'rejected', admin_decision_for_critical: true, reviewer_notes: 'w463 probe' });
const again = await runCycle(5000);
const pageR = await p.evaluate(() => document.body.innerText);
const rejectedLine = await p.evaluate(() => document.querySelector('[data-testid="hold-rejected"]')?.innerText || '');
console.log('  rejected line:', rejectedLine);
check('the same cycle after a rejection says it is asked again when the action changes, and what rejected it',
  rej.status === 200 && again.governance?.status === 'rejected_by_change_control' && again.governance?.rejected_by === 'admin_override'
  && /Rejected by Change Control — asked again when the action changes/i.test(pageR)
  && /rejected by an explicit decision for exactly this action/.test(rejectedLine) && !/review it on the/i.test(rejectedLine));
const changed = await runCycle(6000);
const holdB = changed.governance?.cca_id;
const recB = await record(holdB);
check('a changed cycle files a fresh hold that records the rejection it follows',
  changed.cycle === null && holdB && holdB !== holdA && recB?.follows_rejection?.cca_id === holdA
  && changed.governance?.follows_rejection === holdA
  && /FOLLOWS A REJECTION/.test(recB?.description || '') && recB?.est_distributable_wst === 4800);
const instruction = await p.evaluate(() => document.querySelector('[data-testid="hold-follows-rejection"]')?.innerText || '');
console.log('  instruction:', instruction);
check('the economy page says a hold that follows a rejection is decided in the Sanctum, not by a review',
  instruction.includes(holdB) && instruction.includes(holdA) && /Sovereign Sanctum/.test(instruction) && !/review it on the/i.test(instruction));

// ── The Sanctum lists it from the moment it is filed (before any review) ──
const p0 = await ctx.newPage();
await openSanctum(p0);
await p0.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
const early = await cardOf(p0).locator('[data-testid="sanctum-hold-detail"]').innerText().catch(() => '');
console.log('  sanctum (before review):', early);
check('the Sanctum lists the hold before any review, with its amount, what an approval releases, and the rejection it follows',
  /Amount: 4800 WST \(virtual\)/.test(early) && /approving releases one action of at most this amount/.test(early)
  && early.includes(`Follows the rejection of ${holdA}`) && !/applies to this amount only/.test(early));
await p0.close();

// ── /change-control: the amount is shown; a review holds it and says where it is decided ──
const reviewB = await api(p, `/api/v1/cca/${holdB}/review`, { reviewer_notes: 'w463 probe — a review, not a decision' });
await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector(`text=${TITLE}`, { state: 'attached', timeout: 60000 }).catch(() => {});
await dismissTour(p);
const rowB = ccaRow(p, TITLE);
const rowText = await rowB.innerText().catch(() => '');
await rowB.locator('div.cursor-pointer').first().click();
await p.waitForFunction((t) => [...document.querySelectorAll('[data-testid="cca-decision-source"]')].some(e => e.closest('div.bg-white\\/4')?.innerText.includes(t)), TITLE, { timeout: 30000 }).catch(() => {});
const heldLine = await rowB.locator('[data-testid="cca-decision-source"]').innerText().catch(() => '');
console.log('  row:', rowText.replace(/\n/g, ' | ').slice(0, 200), '\n  held line:', heldLine);
check('the Change Control page shows the hold\'s amount, and a review held it for the Sanctum',
  reviewB.json?.hold_reason === 'critical_requires_admin_decision' && /4800 WST \(virtual\)/.test(rowText)
  && /held — awaiting an explicit admin decision/.test(heldLine) && /Sovereign Sanctum/.test(heldLine));

// W464 — the page offers no review of an economy hold (CRITICAL); a review whose amount moved is still refused by the API
const holdE = (await api(p, '/api/v1/economy/cycle', { vsb_id: CCA_VSB, revenue: 5000, costs: 0 })).json?.governance?.cca_id;
await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector(`text=[economy] material distribution — ${CCA_VSB}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const rowE = ccaRow(p, `[economy] material distribution — ${CCA_VSB}`);
const shownE = await rowE.innerText().catch(() => '');
await rowE.locator('div.cursor-pointer').first().click();
await p.waitForSelector('[data-testid="cca-economy-sanctum-note"]', { timeout: 30000 }).catch(() => {});
const reviewButtonsE = await rowE.locator('button:has-text("Request review")').count();
const sanctumNoteE = await rowE.locator('[data-testid="cca-economy-sanctum-note"]').innerText().catch(() => '');
const moved = await api(p, '/api/v1/economy/cycle', { vsb_id: CCA_VSB, revenue: 6000, costs: 0 });   // re-estimated to 4800 behind the page
const staleE = await api(p, `/api/v1/cca/${holdE}/review`, { reviewer_notes: 'w463 probe', expected_est_distributable_wst: 4000 });
const recE = await record(holdE);
console.log('  sanctum note:', sanctumNoteE, '| refused:', staleE.json?.detail?.slice(0, 80));
check('(W464) the page offers no review of an economy hold and says the Owner decides it in the Sanctum; a review of a moved amount is refused (409)',
  /4000 WST \(virtual\)/.test(shownE) && reviewButtonsE === 0 && /decided only by the Owner — in the Governance hub/.test(sanctumNoteE)
  && moved.json?.governance?.cca_id === holdE && staleE.status === 409 && /changed since it was read/.test(staleE.json?.detail || '')
  && recE?.status === 'submitted' && recE?.est_distributable_wst === 4800);

// ── The Sanctum: a stale vote is refused; a real vote decides ──
const p2 = await ctx.newPage();
// STUB (labelled): the queue reports the amount the hold was first filed with (4000), not what it carries now
await p2.route('**/api/v1/cca/queue', async r => {
  const real = await (await r.fetch()).json();
  r.fulfill({ contentType: 'application/json', body: JSON.stringify({ ...real, queue: (real.queue || []).map(c => c.cca_id === holdB ? { ...c, est_distributable_wst: 4000 } : c) }) });
});
await openSanctum(p2);
await p2.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p2);
await cardOf(p2).locator('button:has-text("Sovereign Approve")').click();
await p2.waitForFunction(() => !!document.querySelector('[data-testid="sanctum-error"]'), null, { timeout: 30000 }).catch(() => {});
const staleErr = await p2.locator('[data-testid="sanctum-error"]').innerText().catch(() => '');
const recB2 = await record(holdB);
console.log('  sanctum refusal:', staleErr.slice(0, 160));
check('(stubbed amount) a Sanctum vote on an amount the hold no longer carries is refused, shown, and decides nothing',
  /changed since it was read/.test(staleErr) && recB2?.status === 'under_review');
await p2.close();

await openSanctum(p);
await p.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
const detail = await cardOf(p).locator('[data-testid="sanctum-hold-detail"]').innerText().catch(() => '');
const heading = await p.evaluate(() => document.body.innerText);
console.log('  sanctum detail:', detail);
check('the Sanctum lists the held economy hold with its amount and why it is held',
  /Amount: 4800 WST \(virtual\)/.test(detail) && /Held: critical requires admin decision/.test(detail)
  && /Awaiting an explicit decision/i.test(heading) && !/Pending CRITICAL changes/i.test(heading));
await dismissTour(p);
await cardOf(p).locator('button:has-text("Sovereign Approve")').click();
await p.waitForFunction(async (id) => (await (await fetch(`/api/v1/cca/${id}`)).json()).status === 'approved', holdB, { timeout: 30000, polling: 500 }).catch(() => {});
const recB3 = await record(holdB);

// an approved economy hold offers no Implement on the Change Control page
await p.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector(`text=${TITLE}`, { timeout: 60000 }).catch(() => {});
await dismissTour(p);
const rowB2 = ccaRow(p, TITLE);
await rowB2.locator('div.cursor-pointer').first().click();
await p.waitForSelector('[data-testid="cca-economy-release-note"]', { timeout: 30000 }).catch(() => {});
const approvedRow = await rowB2.innerText().catch(() => '');
const implementButtons = await rowB2.locator('button:has-text("Implement")').count();
check('an approved economy hold offers no Implement, and says running its action releases it',
  recB3?.status === 'approved' && implementButtons === 0 && /run the cycle or transfer it was filed for to release it/.test(approvedRow));

await p.goto(`${BASE}/economy?vsb=${VSB}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
await dismissTour(p);
const ran = await runCycle(6000);
const recB4 = await record(holdB);
check('a real Sanctum vote approves exactly that hold, and the cycle it was filed for then runs once',
  recB3?.status === 'approved' && ran.cycle !== null && recB4?.status === 'implemented');

// ── (stubbed, labelled) transfer outcomes that are not plain success say what happened ──
const transferWith = async (governance) => {
  const pg = await ctx.newPage();
  await pg.route('**/api/v1/economy/living-vsbs', r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({
    living_vsbs: [{ vsb_id: VSB, name: 'Probe sender' }, { vsb_id: `${VSB}-rx`, name: 'Probe receiver' }], total: 2 }) }));
  await pg.route('**/api/v1/economy/transfer', r => r.fulfill({ contentType: 'application/json', body: JSON.stringify({
    transfer: { transfer_id: 'xfer-probe', from_vsb: VSB, to_vsb: `${VSB}-rx`, amount_wst: 300, sender_reserve_fund_after_wst: 700,
                settlement: 'the receiver\'s next metabolic cycle consumes this as intake revenue', disclaimer: 'Virtual/simulated WST — no real funds moved.' },
    governance }) }));
  await pg.goto(`${BASE}/economy?vsb=${VSB}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForSelector('select[aria-label="transfer receiver"]', { timeout: 60000 });
  await dismissTour(pg);
  await pg.selectOption('select[aria-label="transfer receiver"]', `${VSB}-rx`);
  await pg.fill('input[aria-label="transfer amount"]', '300');
  await dismissTour(pg);
  await pg.locator('button:has-text("Transfer")').last().click();
  await pg.waitForFunction(() => /Transfer posted/i.test(document.body.innerText), null, { timeout: 30000 }).catch(() => {});
  const text = await pg.evaluate(() => document.body.innerText);
  await pg.close();
  return text;
};
const raisedAfter = await transferWith({ status: 'gate_raised_after_execution', error: 'probe: checkpoint write failed' });
check('(stubbed) a transfer that posted before its gate raised is shown as posted, and says the gate raised',
  /Transfer posted · xfer-probe/i.test(raisedAfter)   /* the heading is CSS-uppercased, and innerText follows it */
  && /the transfer posted, then the governance gate raised while recording it/.test(raisedAfter));
const retried = await transferWith({ status: 'allowed_action_retried', error: 'probe: pending store lock timed out' });
check('(stubbed) a transfer the gate allowed that raised and was retried says so, and never "gate was unavailable"',
  /Transfer posted · xfer-probe/i.test(retried) && /the gate allowed the transfer and it raised part-way/.test(retried)
  && !/governance gate was unavailable/.test(retried));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
