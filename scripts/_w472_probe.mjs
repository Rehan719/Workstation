// W472 (P1.15 stores that refuse, never replace) — in a real browser against the built bundle on a FRESH backend
// (AI_DISABLE_LOCAL=1; virtual WST only). The probe writes malformed bytes into the backend's OWN data directory (the
// stores this round made strict) and checks that the writers refuse, the bytes stand, and the pages say so.
//   node scripts/_w472_probe.mjs http://127.0.0.1:8081 <the probe's DATA_DIR>
//   · the living roster with a byte-order mark: /economy says "Living roster unavailable" (never an empty roster), the
//     API refuses a registration, and the file's bytes are unchanged;
//   · the compliance history unreadable: the roster rows say the standing is unknown, and an autonomous visit HOLDS;
//   · the Owner's waterfall overrides unreadable: POST /economy/waterfall answers 503 and the store is unchanged;
//   · a VSB ledger with a byte-order mark: /ledger answers 503, POST …/repair quarantines and recovers it losslessly,
//     and the balances read as before.
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8081';
const DATA_DIR = process.argv[3];
if (!DATA_DIR) { console.error('usage: node scripts/_w472_probe.mjs <base> <probe DATA_DIR>'); process.exit(2); }
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const flat = (s) => (s || '').replace(/\s+/g, ' ').trim();
const post = (path, body) => fetch(`${BASE}${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) });
const BOM = Buffer.from([0xef, 0xbb, 0xbf]);

// a living entity, a screened history, an owner override, a ledger with postings
const est = await (await post('/api/v1/genesis/establish', { problem: 'w472 probe', domain: 'care', name: 'W472ProbeCo',
  concept: 'c', design: 'd', commercialisation: 'm', ship_output: false })).json();
const vid = est.vsb_id;
await post('/api/v1/economy/cycle', { vsb_id: vid, revenue: 150 });
await post('/api/v1/economy/waterfall', { vsb_id: vid, entity_type: 'waqf_ltd_hybrid', proportions: { owner: 0.2, self_investment: 0.3, capital_fund: 0.2, user_projects: 0.2, charity: 0.1 } });
const roster = join(DATA_DIR, 'living_vsbs.json');
const history = join(DATA_DIR, 'vsb_compliance_history.json');
const overrides = join(DATA_DIR, 'economy_waterfall_overrides.json');
const ledger = join(DATA_DIR, 'economy', `${vid}_ledger.json`);
console.log('  stores:', [roster, history, overrides, ledger].map(f => existsSync(f)).join(','));

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
const open = async () => {
  await page.goto(`${BASE}/economy`, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(2000);
  for (let i = 0; i < 3; i++) { await page.keyboard.press('Escape'); await page.waitForTimeout(150); }
};

// ── the roster ──
const rosterGood = readFileSync(roster);
writeFileSync(roster, Buffer.concat([BOM, rosterGood]));
try {
  await open();
  const msg = flat(await page.locator('[data-testid="roster-unavailable"]').innerText().catch(() => ''));
  const api = await (await fetch(`${BASE}/api/v1/economy/living-vsbs`)).json();
  const reg = await post('/api/v1/genesis/establish', { problem: 'w472 while unreadable', domain: 'care', name: 'W472WhileCo', ship_output: false });
  const bytesStand = readFileSync(roster).equals(Buffer.concat([BOM, rosterGood]));
  console.log('  roster:', msg, '| api unavailable:', String(api.roster_unavailable).slice(0, 60), '| establish', reg.status, '| bytes stand', bytesStand);
  check('an unreadable living roster is said on /economy and by the API, and a registration never overwrites it',
    /Living roster unavailable/i.test(msg) && /could not be read whole/.test(String(api.roster_unavailable)) && api.living_vsbs.length === 0 && bytesStand);
} finally { writeFileSync(roster, rosterGood); }

// ── the compliance history ──
const histGood = existsSync(history) ? readFileSync(history) : null;
writeFileSync(history, Buffer.from('{"truncated": '));
try {
  await open();
  const msg = flat(await page.locator('[data-testid="history-unavailable"]').innerText().catch(() => ''));
  const api = await (await fetch(`${BASE}/api/v1/economy/living-vsbs`)).json();
  const row = (api.living_vsbs || []).find(r => r.vsb_id === vid) || {};
  console.log('  history:', msg.slice(0, 80), '| row standing:', JSON.stringify(row.compliance).slice(0, 100));
  check('an unreadable compliance history is said on /economy, and each entity\'s standing is unknown, not clean',
    /Compliance history unavailable/i.test(msg) && row.compliance && row.compliance.history_unavailable && row.compliance.never_screened === null);
} finally { if (histGood) writeFileSync(history, histGood); }

// ── the Owner's overrides ──
const ovGood = readFileSync(overrides);
writeFileSync(overrides, Buffer.from('[1, 2, 3]'));
try {
  const r = await post('/api/v1/economy/waterfall', { vsb_id: vid, entity_type: 'waqf_ltd_hybrid', proportions: { owner: 0.1, self_investment: 0.4, capital_fund: 0.2, user_projects: 0.2, charity: 0.1 } });
  const d = await r.json().catch(() => ({}));
  const st = await (await fetch(`${BASE}/api/v1/economy/status?vsb_id=${vid}`)).json().catch(() => ({}));
  console.log('  overrides:', r.status, String(d.detail).slice(0, 70), '| status source:', st.waterfall_source, '| bytes stand', readFileSync(overrides).toString() === '[1, 2, 3]');
  check('unreadable waterfall overrides: the Owner\'s save is refused (503), the store is unchanged, the status says overrides_unavailable',
    r.status === 503 && /could not be read whole/.test(String(d.detail)) && readFileSync(overrides).toString() === '[1, 2, 3]'
    && st.waterfall_source === 'overrides_unavailable' && /could not be read whole/.test(String(st.overrides_error)));
} finally { writeFileSync(overrides, ovGood); }

// ── the ledger's repair path ──
const ledGood = readFileSync(ledger);
const before = await (await fetch(`${BASE}/api/v1/economy/ledger/${vid}`)).json();
writeFileSync(ledger, Buffer.concat([BOM, ledGood]));
const refused = (await fetch(`${BASE}/api/v1/economy/ledger/${vid}`)).status;
const rep = await (await post(`/api/v1/economy/ledger/${vid}/repair`)).json();
const after = await (await fetch(`${BASE}/api/v1/economy/ledger/${vid}`)).json();
const quarantined = readdirSync(join(DATA_DIR, 'economy')).some(f => f.startsWith(`${vid}_ledger.quarantine-`));
console.log('  ledger: refused', refused, '| repaired', rep.repaired, '| lost', JSON.stringify(rep.lost), '| quarantine on disk', quarantined);
check('a ledger with a byte-order mark is refused, then repaired losslessly: quarantined, recovered, balances as before',
  refused === 503 && rep.repaired === true && quarantined && JSON.stringify(after.balances) === JSON.stringify(before.balances));

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
