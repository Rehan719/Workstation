// W465 — service contracts paid once and said as they are, and the owner-payments store refused rather than read as
// empty, in a real browser against the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1, ECONOMY_MATERIALITY_WST=1000;
// virtual WST only). Seed first with scripts/_w465_probe_seed.py <tag> under the same isolated env, then:
//   node scripts/_w465_probe.mjs http://127.0.0.1:8074 <client_vsb> <provider_vsb>
//   · FU-015: Settle on the page pays once and shows the full transfer id; two settles of one contract at once debit once;
//   · FU-024: a material settlement is shown held for the Owner (never "Settled"), and after the Owner rejects it the
//     page says the payment was rejected — no hold, nothing paid;
//   · FU-016: (stubbed, labelled) an owner-payments or board-pack refusal is shown as a refusal, never as zero figures;
//     a cycle whose owner accrual failed says so, and claims a ledger entry only when one landed; an owner-payments
//     answer for an entity the Owner switched away from is never shown under the new one; a transfer in flight locks
//     the entity picker, and its answer (here a stubbed "do NOT re-run") is shown when it lands.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8074';
const CLIENT = process.argv[3];
const PROVIDER = process.argv[4];
if (!CLIENT || !PROVIDER) { console.error('usage: node scripts/_w465_probe.mjs <base> <client_vsb> <provider_vsb>'); process.exit(2); }
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const TAG = Date.now().toString(36);

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
const reserve = async () => (await api(p, `/api/v1/economy/ledger/${CLIENT}`)).json?.reserve_fund_wst;
const contract = async (id) => ((await api(p, '/api/v1/economy/contracts')).json?.contracts || []).find(c => c.id === id);
const delivered = async (label, price) => {
  const brief = `W465 probe ${label} ${TAG}`;
  const off = await api(p, '/api/v1/economy/contracts', { client_vsb: CLIENT, provider_vsb: PROVIDER, brief, price_wst: price });
  const id = off.json?.id;
  const acc = await api(p, `/api/v1/economy/contracts/${id}/accept`, {});
  const dl = await api(p, `/api/v1/economy/contracts/${id}/deliver`, {});
  if (dl.json?.status !== 'delivered') console.log('  deliver answered', off.status, acc.status, dl.status, JSON.stringify(dl.json).slice(0, 200));
  return { id, brief };
};
const row = (page, brief) => page.locator('div.rounded-xl.border', { has: page.getByText(brief, { exact: true }) }).last();
const openEconomy = async (page, vsb) => {
  await page.goto(`${BASE}/economy?vsb=${vsb}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
  await dismissTour(page);
};
const settleOnPage = async (brief) => {
  await openEconomy(p, CLIENT);
  await p.waitForSelector(`text=${brief}`, { timeout: 60000 });
  await dismissTour(p);
  const r = row(p, brief);
  await r.scrollIntoViewIfNeeded();
  const before = await p.evaluate(() => document.body.innerText.length);
  await r.locator('button:has-text("Settle (client)")').click();
  await p.waitForFunction(() => /Settled — transfer|\[role="alert"\]/.test(document.body.innerText)
    || !!document.querySelector('[role="alert"]') || !!document.querySelector('[role="status"]'), null, { timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(1500);
  void before;
  return {
    status: await p.locator('[role="status"]').allInnerTexts().catch(() => []),
    alerts: await p.locator('[role="alert"]').allInnerTexts().catch(() => []),
    row: await row(p, brief).innerText().catch(() => ''),
  };
};

await p.goto(`${BASE}/economy?vsb=${CLIENT}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
await dismissTour(p);

// ── FU-015: Settle on the page pays once, and the row shows the whole transfer id ──
const A = await delivered('paid', 120);
const r0 = await reserve();
const sA = await settleOnPage(A.brief);
const cA = await contract(A.id);
const r1 = await reserve();
console.log('  settle A:', sA.status.join(' | ').slice(0, 160), '| reserve', r0, '→', r1, '| row:', sA.row.replace(/\n/g, ' ').slice(0, 200));
check('Settle on the page pays once and shows the whole transfer id',
  cA?.status === 'settled' && /^xfer-[0-9a-f]{10}$/.test(cA?.settlement?.transfer_id || '')
  && sA.status.some(t => t.includes(`Settled — transfer ${cA.settlement.transfer_id}`))
  && sA.row.toLowerCase().includes(`transfer ${cA.settlement.transfer_id}`.toLowerCase())
  && Math.round((r0 - r1) * 100) === 12000);

// ── FU-015: two settles of one contract at once debit the client once ──
const B = await delivered('twice', 130);
const r2 = await reserve();
const both = await p.evaluate(async (id) => Promise.all([0, 1].map(async () => {
  const r = await fetch(`/api/v1/economy/contracts/${id}/settle`, { method: 'POST' });
  return { status: r.status, json: await r.json().catch(() => null) };
})), B.id);
const r3 = await reserve();
const cB = await contract(B.id);
console.log('  concurrent:', both.map(x => `${x.status} ${x.json?.status || ''} ${(x.json?.note || x.json?.detail || '').slice(0, 60)}`).join(' || '), '| reserve', r2, '→', r3);
check('two settles of one contract at once pay it once',
  cB?.status === 'settled' && Math.round((r2 - r3) * 100) === 13000 && both.some(x => x.status === 200 && x.json?.status === 'settled')
  && both.every(x => x.status === 200 || (x.status === 409 && /already in progress/.test(x.json?.detail || ''))));

// ── FU-024: a material settlement is held for the Owner — never shown as settled ──
const C = await delivered('material', 2000);
const r4 = await reserve();
const sC = await settleOnPage(C.brief);
const cC = await contract(C.id);
console.log('  held:', sC.alerts.join(' | ').slice(0, 220), '| badge row:', sC.row.replace(/\n/g, ' ').slice(0, 220));
check('a material settlement is shown held for the Owner, with no "Settled" notice and nothing paid',
  cC?.status === 'delivered' && cC?.settlement?.outcome === 'held' && !!cC?.settlement?.cca_id
  && sC.alerts.some(t => /Sovereign Sanctum/.test(t)) && !sC.status.some(t => /Settled/.test(t))
  && /held for the Owner/i.test(sC.row) && Math.round(((await reserve()) - r4) * 100) === 0);

// the Owner rejects it: settling again says the payment was rejected, and pays nothing
const rej = await api(p, `/api/v1/cca/${cC?.settlement?.cca_id}/review`, { override_decision: 'rejected', admin_decision_for_critical: true, reviewer_notes: 'w465 probe — the Owner rejects' });
const sC2 = await settleOnPage(C.brief);
const cC2 = await contract(C.id);
console.log('  rejected:', rej.status, sC2.alerts.join(' | ').slice(0, 220), '| row:', sC2.row.replace(/\n/g, ' ').slice(0, 200));
check('after the Owner rejects it the page says the payment was rejected — no hold to wait for, nothing paid',
  rej.status === 200 && cC2?.status === 'delivered' && cC2?.settlement?.outcome === 'rejected' && cC2?.settlement?.held === false
  && sC2.alerts.some(t => /refused/.test(t) && !/retry after the hold clears/.test(t))
  && /payment rejected/i.test(sC2.row) && !sC2.status.some(t => /Settled/.test(t)) && Math.round(((await reserve()) - r4) * 100) === 0);

// ── FU-016 (stubbed, labelled): refusals are shown as refusals, never as zero figures ──
const stubbed = await ctx.newPage();
await stubbed.route('**/api/v1/economy/owner-payments?*', r => r.fulfill({ status: 503, contentType: 'application/json',
  body: JSON.stringify({ detail: 'probe: the owner-payments store is unreadable (it was not overwritten)' }) }));
await stubbed.route('**/api/v1/economy/board-pack?*', r => r.fulfill({ status: 503, contentType: 'application/json',
  body: JSON.stringify({ detail: 'probe: the board pack could not be built' }) }));
await openEconomy(stubbed, CLIENT);
await stubbed.waitForSelector('[data-testid="owner-payments-error"]', { timeout: 30000 }).catch(() => {});
const opErr = await stubbed.locator('[data-testid="owner-payments-error"]').innerText().catch(() => '');
const bpErr = await stubbed.locator('[data-testid="board-pack-error"]').innerText().catch(() => '');
const payoutButtons = await stubbed.locator('button:has-text("Record virtual payout")').count();
console.log('  refusals:', opErr, '|', bpErr, '| payout buttons', payoutButtons);
check('(stubbed 503) an owner-payments or board-pack refusal is shown as that refusal, with no balance or payout button',
  /owner-payments store is unreadable/.test(opErr) && /board pack could not be built/.test(bpErr) && payoutButtons === 0);
await stubbed.close();

// ── FU-016 (stubbed cycle answer, labelled): a failed owner accrual says so, and claims a ledger entry only when it landed ──
const accrualSays = async (uegLogged) => {
  const pg = await ctx.newPage();
  await pg.route('**/api/v1/economy/cycle', async r => {
    const real = await r.fetch({ postData: JSON.stringify({ vsb_id: CLIENT, entity_type: 'waqf_ltd_hybrid', revenue: 500, costs: 0 }) });
    const d = await real.json();
    if (d.cycle) d.cycle.owner_accrual = { accrued: false, amount_wst: 12.5, error: 'OwnerPaymentsUnavailable: probe', ueg_logged: uegLogged };
    await r.fulfill({ status: real.status(), contentType: 'application/json', body: JSON.stringify(d) });
  });
  await openEconomy(pg, CLIENT);
  await pg.locator('button:has-text("Run Metabolic Cycle")').click();
  await pg.waitForSelector('[data-testid="owner-accrual-failed"]', { timeout: 60000 }).catch(() => {});
  const text = await pg.locator('[data-testid="owner-accrual-failed"]').innerText().catch(() => '');
  await pg.close();
  return text;
};
const landed = await accrualSays(true);
const notLanded = await accrualSays(false);
console.log('  accrual:', landed.slice(0, 200), '||', notLanded.slice(0, 200));
check('(stubbed accrual failure) the cycle says the owner share was not recorded, and names a ledger entry only when it landed',
  /NOT recorded in Owner\s+Payments/.test(landed) && /logged on the constitutional ledger/.test(landed)
  && /ledger entry did not land either/.test(notLanded) && !/logged on the constitutional ledger/.test(notLanded));

// ── FU-016 (stubbed delay, labelled): a late owner-payments answer for the entity switched away from is dropped ──
const sw = await ctx.newPage();
let releaseLate;
const lateGate = new Promise(res => { releaseLate = res; });
await sw.route('**/api/v1/economy/owner-payments?*', async r => {
  if (r.request().url().includes(encodeURIComponent(CLIENT))) {
    await lateGate;   // held until after the switch
    return r.fulfill({ contentType: 'application/json', body: JSON.stringify({ vsb_id: CLIENT, owner: 'Rehan', currency: 'WST (virtual)',
      accrued_total_wst: 987654, paid_out_total_wst: 0, balance_wst: 987654, entries: [], real_money_rails: 'DISABLED', note: 'probe late answer' }) });
  }
  return r.continue();
});
await sw.goto(`${BASE}/economy?vsb=${CLIENT}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await sw.waitForSelector('text=Run Metabolic Cycle', { timeout: 60000 });
await dismissTour(sw);
await sw.waitForFunction((pv) => !!Array.from(document.querySelectorAll('select option')).find(o => o.value === pv), PROVIDER, { timeout: 30000 }).catch(() => {});
const picker = sw.locator('select', { has: sw.locator(`option[value="${PROVIDER}"]`) }).first();
await picker.selectOption(PROVIDER);
await sw.waitForSelector('text=Record virtual payout', { timeout: 30000 }).catch(() => {});
releaseLate();
await sw.waitForTimeout(3000);
const afterSwitch = await sw.evaluate(() => document.body.innerText);
const pickerNow = await picker.inputValue().catch(() => '');
console.log('  switch: picker', pickerNow, '| late figure shown', /987,654/.test(afterSwitch));
check('(stubbed delay) an owner-payments answer for the entity switched away from is never shown under the new one',
  pickerNow === PROVIDER && !/987,654/.test(afterSwitch) && /Record virtual payout/.test(afterSwitch));
await sw.close();

// ── (stubbed delay, labelled) a transfer in flight locks the entity picker, and its answer is shown when it lands ──
const tp = await ctx.newPage();
let releaseTransfer;
const transferGate = new Promise(res => { releaseTransfer = res; });
await tp.route('**/api/v1/economy/transfer', async r => {
  await transferGate;
  return r.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({
    detail: 'probe: Transfer xfer-probe00001 debited the sender (its ledger shows the debit) but has not reached the receiver\'s queue. Do NOT re-run the transfer — a new request debits again.' }) });
});
await tp.goto(`${BASE}/economy?vsb=${CLIENT}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await tp.waitForSelector('select[aria-label="transfer receiver"]', { timeout: 60000 });
await dismissTour(tp);
await tp.selectOption('select[aria-label="transfer receiver"]', PROVIDER);
await tp.fill('input[aria-label="transfer amount"]', '5');
await dismissTour(tp);
const entityPicker = tp.locator('select', { has: tp.locator(`option[value="${PROVIDER}"]`) }).first();
await tp.locator('button:has-text("Transfer")').last().click();
await tp.waitForTimeout(1200);
const lockedDuring = await entityPicker.isDisabled();
releaseTransfer();
await tp.waitForFunction(() => /Do NOT re-run the transfer/.test(document.body.innerText), null, { timeout: 30000 }).catch(() => {});
await tp.waitForTimeout(800);
const unlockedAfter = !(await entityPicker.isDisabled());
const answerShown = /xfer-probe00001[\s\S]*Do NOT re-run the transfer/.test(await tp.evaluate(() => document.body.innerText));
console.log('  transfer lock: disabled during', lockedDuring, '| enabled after', unlockedAfter, '| answer shown', answerShown);
check('(stubbed delay) a transfer in flight locks the entity picker, and its "do NOT re-run" answer is shown when it lands',
  lockedDuring && unlockedAfter && answerShown);
await tp.close();

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
