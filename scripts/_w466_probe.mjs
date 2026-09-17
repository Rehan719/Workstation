// W466 — a stranded inter-VSB transfer (the sender debited, the receiver never credited) is completed once from the page,
// in a real browser against the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1; virtual WST only). Seed first with
// scripts/_w466_probe_seed.py <tag> under the same isolated env (it leaves one REAL stranded debit), then:
//   node scripts/_w466_probe.mjs http://127.0.0.1:8075 <sender> <receiver> <transfer_id>
//   · the REAL seeded stranded debit is listed on load from the ledger (it survives a reload or an entity switch) with
//     Transfer disabled; Complete calls the REAL completion route: the receiver is credited once, a second completion
//     credits nothing, and nothing is left open;
//   · (stubbed transfer answer, labelled — the 503 the route sends when the receiver's queue stayed busy) the panel says
//     the sender was debited, offers Complete at once, and will not send the transfer again;
//   · (stubbed unreadable-ledger check, labelled) Transfer stays locked until a check has read the ledger, and Check
//     again clears it;
//   · (stubbed bodiless 500, labelled) a failure with no JSON never reads as "nothing posted" and offers no Complete;
//   · (stubbed 500, labelled) a transfer that posted in full before the request failed offers no Complete.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8075';
const [SENDER, RECEIVER, XID] = [process.argv[3], process.argv[4], process.argv[5]];
if (!SENDER || !RECEIVER || !XID) { console.error('usage: node scripts/_w466_probe.mjs <base> <sender> <receiver> <transfer_id>'); process.exit(2); }
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
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

const openWithTransferAnswer = async (fulfil) => {
  const pg = await ctx.newPage();
  await pg.route('**/api/v1/economy/transfer', fulfil);
  await pg.goto(`${BASE}/economy?vsb=${SENDER}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await pg.waitForSelector('select[aria-label="transfer receiver"]', { timeout: 60000 });
  await dismissTour(pg);
  await pg.selectOption('select[aria-label="transfer receiver"]', RECEIVER);
  await pg.fill('input[aria-label="transfer amount"]', '42');
  await dismissTour(pg);
  await pg.getByRole('button', { name: 'Transfer', exact: true }).click();
  await pg.waitForTimeout(1500);
  return pg;
};

// ── the REAL stranded debit is listed on load (from the ledger), survives an entity switch, and completes once ──
const p = await ctx.newPage();
await p.goto(`${BASE}/economy?vsb=${SENDER}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForSelector('select[aria-label="transfer receiver"]', { timeout: 60000 });
await dismissTour(p);
await p.waitForSelector('[data-testid="transfer-stranded"]', { timeout: 30000 }).catch(() => {});
const onLoad = await p.locator('[data-testid="transfer-stranded"]').allInnerTexts().catch(() => []);
const sendDisabledOnLoad = await p.getByRole('button', { name: 'Transfer', exact: true }).isDisabled();
const picker = p.locator('select', { has: p.locator(`option[value="${RECEIVER}"]`) }).first();
await picker.selectOption(RECEIVER);
await p.waitForTimeout(1500);
await picker.selectOption(SENDER);
await p.waitForSelector('[data-testid="transfer-stranded"]', { timeout: 30000 }).catch(() => {});
const afterSwitch = await p.locator('[data-testid="transfer-stranded"]').allInnerTexts().catch(() => []);
console.log('  on load:', onLoad.map(x => x.replace(/\n/g, ' ').slice(0, 140)), '| send disabled', sendDisabledOnLoad, '| after switch', afterSwitch.length);
check('the real stranded debit is listed on load from the ledger (with its amount and receiver), Transfer is disabled, and it survives an entity switch',
  onLoad.length === 1 && onLoad[0].includes(XID) && onLoad[0].includes('42 WST') && onLoad[0].includes(RECEIVER)
  && sendDisabledOnLoad && afterSwitch.length === 1 && afterSwitch[0].includes(XID));
await dismissTour(p);
await p.locator('[data-testid="transfer-complete"]').first().click();
await p.waitForSelector('[data-testid="transfer-complete-result"], [data-testid="transfer-complete-error"]', { timeout: 30000 }).catch(() => {});
const completed = await p.locator('[data-testid="transfer-complete-result"]').innerText().catch(() => '');
const completeErr = await p.locator('[data-testid="transfer-complete-error"]').innerText().catch(() => '');
await p.waitForTimeout(1500);
const again = await api(p, `/api/v1/economy/transfers/${XID}/complete`, { from_vsb: SENDER });
const listed = await api(p, `/api/v1/economy/transfers/open?from_vsb=${SENDER}`);
console.log('  complete:', completed || completeErr, '| again:', again.status, again.json?.status, '| open now', (listed.json?.open || []).length);
check('Complete credits the receiver once through the real route; a second completion credits nothing; nothing is left open',
  /^Completed · /.test(completed) && completed.includes(XID) && !completeErr
  && again.status === 200 && again.json?.status === 'already_credited'
  && (listed.json?.open || []).length === 0 && (await p.locator('[data-testid="transfer-stranded"]').count()) === 0);
await p.close();

// ── (stubbed 503, labelled) a debited-uncredited answer offers Complete at once and blocks a second send ──
const FAKE = 'xfer-probe00002';
const p2 = await openWithTransferAnswer(r => r.fulfill({ status: 503, contentType: 'application/json',
  headers: { 'X-Transfer-Id': FAKE, 'X-Transfer-Debited': 'true', 'X-Transfer-Receiver': 'not_credited' },
  body: JSON.stringify({ detail: `store_lock timeout on economy_pending_transfers.json.lock. Transfer ${FAKE} debited the sender (its ledger shows the debit) but has not reached the receiver's queue. Do NOT re-run the transfer — a new request debits again.` }) }));
const strandedBox = await p2.locator('[data-testid="transfer-stranded"]').innerText().catch(() => '');
const sendDisabled = await p2.getByRole('button', { name: 'Transfer', exact: true }).isDisabled();
console.log('  stubbed stranded:', strandedBox.replace(/\n/g, ' ').slice(0, 160), '| send disabled', sendDisabled);
check('(stubbed 503) the panel says the sender was debited, offers Complete, and will not send the transfer again',
  strandedBox.includes(FAKE) && /Do not send it again/i.test(strandedBox.replace(/\s+/g, ' ')) && sendDisabled
  && (await p2.locator('[data-testid="transfer-complete"]').count()) === 1);
await p2.close();

// ── (stubbed 503 on the open-leg check, labelled) a check that could not read the ledger keeps Transfer locked, and
//    "Check again" unlocks it once a check has read the ledger ──
const u = await ctx.newPage();
await u.route('**/api/v1/economy/transfers/open*', r => r.fulfill({ status: 200, contentType: 'application/json',
  body: JSON.stringify({ from_vsb: SENDER, open: [], credited_unclosed: [], settling: [], ledger_unreadable: true, receiver_queue_unreadable: false }) }));
await u.goto(`${BASE}/economy?vsb=${SENDER}`, { waitUntil: 'domcontentloaded', timeout: 45000 });
await u.waitForSelector('select[aria-label="transfer receiver"]', { timeout: 60000 });
await dismissTour(u);
await u.selectOption('select[aria-label="transfer receiver"]', RECEIVER);
await u.fill('input[aria-label="transfer amount"]', '5');
await u.waitForSelector('[data-testid="transfer-open-retry"]', { timeout: 30000 }).catch(() => {});
const lockedUnchecked = await u.getByRole('button', { name: 'Transfer', exact: true }).isDisabled();
const retryShown = (await u.locator('[data-testid="transfer-open-retry"]').count()) === 1;
await u.unroute('**/api/v1/economy/transfers/open*');
await dismissTour(u);
await u.locator('[data-testid="transfer-open-retry"]').click();
await u.waitForTimeout(1500);
const unlockedAfterCheck = !(await u.getByRole('button', { name: 'Transfer', exact: true }).isDisabled());
console.log('  unchecked: locked', lockedUnchecked, '| retry', retryShown, '| unlocked after a readable check', unlockedAfterCheck);
check('(stubbed unreadable-ledger check) Transfer stays locked until a check has read the ledger, and Check again clears it',
  lockedUnchecked && retryShown && unlockedAfterCheck);
await u.close();

// ── (stubbed bodiless 500) never "nothing posted", no Complete ──
const q = await openWithTransferAnswer(r => r.fulfill({ status: 500, contentType: 'text/plain', body: 'Internal Server Error' }));
const qText = await q.evaluate(() => document.body.innerText);
console.log('  bodiless:', (qText.match(/The transfer failed[^\n]*/) || [''])[0].slice(0, 200));
check('(stubbed bodiless 500) the panel says the transfer may have debited the sender and offers no Complete',
  /The transfer failed \(HTTP 500\) and returned no details — it may have debited/.test(qText)
  && (await q.locator('[data-testid="transfer-complete"]').count()) === 0);
await q.close();

// ── (stubbed 500 for a transfer that posted in full) no Complete ──
const s = await openWithTransferAnswer(r => r.fulfill({ status: 500, contentType: 'application/json',
  headers: { 'X-Transfer-Id': XID, 'X-Transfer-Debited': 'true', 'X-Transfer-Receiver': 'credited' },
  body: JSON.stringify({ detail: `Transfer ${XID} posted — the sender was debited and the receiver credited — but the request then failed (OSError: probe). Nothing is missing; do NOT re-run it.` }) }));
const sText = await s.evaluate(() => document.body.innerText);
check('(stubbed 500, posted in full) the panel shows that it posted and offers no Complete',
  /Nothing is missing; do NOT re-run it/.test(sText) && (await s.locator('[data-testid="transfer-complete"]').count()) === 0);
await s.close();

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
