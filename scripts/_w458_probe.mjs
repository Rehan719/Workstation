// W458 (delivery-plan P1.10) — "disabled ≠ failed" and status honesty, in a real browser against the
// built bundle on a FRESH backend (AI_DISABLE_LOCAL=1, so the local model is disabled by configuration):
//   · the headline card says the deterministic floor is active and shows the ROW the verdict came from;
//   · a completion run from the page reports "tried: native";
//   · a completion routed to the LOCAL tier reports "ollama (disabled by config, skipped)" — the local
//     tier button is (correctly) not offered under the flag, so it is routed through the page's own API
//     the way the tier button would;
//   · after it the organism recorded NO ai_failure and the card STILL says floor, naming the successful
//     native row — before W458 the same call dropped immune health to 0.9 and flipped the card to a
//     green "Real model: ollama".
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8052';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();

const dismissTour = async () => {
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(400);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), null, { timeout: 10000 }).catch(() => {});
};
const card = () => p.evaluate(() => {
  const el = document.querySelector('[data-testid="native-status-basis"]');
  return { basis: el ? el.innerText : '', card: el ? el.closest('div[class*="rounded"]')?.innerText || '' : '' };
});
const api = (path, init) => p.evaluate(async ([u, i]) => {
  const r = await fetch(u, i ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(i) } : undefined);
  return await r.json();
}, [path, init || null]);

const open = async () => {
  await p.goto(BASE + '/native-ai', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, null, { timeout: 60000 });
  await dismissTour();
  await p.waitForFunction(() => !!document.querySelector('[data-testid="native-status-basis"]'), null, { timeout: 90000 });
};

await open();
let { basis, card: headline } = await card();
console.log('  basis (fresh):', basis.slice(0, 150));
check('fresh backend: the card says the deterministic floor is active, and the basis says no completion has served yet',
  /Deterministic floor active/i.test(headline) && /no successful completion has been recorded yet/i.test(basis));
const imm0 = await api('/api/v1/organism/systems');
check('fresh backend: the organism has recorded no ai_failure', !(imm0?.immune?.by_type || {}).ai_failure && imm0?.immune?.health === 1);

// a completion run from the page itself (the Auto tier is what the page offers under the flag)
await p.locator('textarea[placeholder="Prompt for the native AI…"]').fill('Say hello in five words.');
await p.locator('button', { hasText: /Run completion/i }).first().click();
await p.waitForFunction(() => /tried:/i.test(document.body.innerText), null, { timeout: 120000 });
const tried1 = (await p.evaluate(() => document.body.innerText)).match(/tried:[^\n]*/i)?.[0] || '';
console.log(' ', tried1);
check('a completion run from the page reports the floor as the resource that served', /tried:\s*native/i.test(tried1));

// the LOCAL tier is not offered under the flag (local_models() is empty), so route it through the
// page's own API exactly as that button would
const tiers = (await api('/api/v1/native-ai/models')).tiers.map(t => t.id);
check('the local tier is honestly absent from the page while the local model is disabled', !tiers.includes('local'));
const local = await api('/api/v1/native-ai/complete', { prompt: 'Say hello in five words.', model: 'local' });
console.log('  resources_tried:', JSON.stringify(local.resources_tried));
check('a completion routed to the disabled local model reports it SKIPPED, and the floor serves',
  local.served_by === 'native' && /^ollama \(disabled by config, skipped\)$/.test((local.resources_tried || [])[0] || ''));
const imm1 = await api('/api/v1/organism/systems');
console.log('  immune after:', JSON.stringify(imm1.immune).slice(0, 140));
const brk = (imm1?.self_healing?.circuits || {})['model:ollama'] || {};   // consulting the breaker creates a zero-failure entry
console.log('  breaker model:ollama:', JSON.stringify(brk));
check('the disabled model is not scored as a failure: no ai_failure, immune health still 1.0, no breaker failure',
  !(imm1?.immune?.by_type || {}).ai_failure && imm1?.immune?.health === 1
  && (brk.total_failures || 0) === 0 && (brk.failures_in_window || 0) === 0);
const mh = await api('/api/v1/operations/model-health');
check('the learning loop holds no row for the model that was never attempted',
  !(mh.models || []).some(m => m.name === 'ollama') && /never attempted/i.test(mh.rule || ''));

// reload: the card follows the most recent completion that actually SERVED
await open();
({ basis, card: headline } = await card());
console.log('  basis (after):', basis.slice(0, 190));
check('after: the card still says floor and names the SUCCESSFUL native row it read',
  /Deterministic floor active/i.test(headline) && !/Real model:/i.test(headline)
  && /most recent SUCCESSFUL recorded completion was served by native/i.test(basis));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
