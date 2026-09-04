// W443 — drive the Agent Hub tab in a real browser against the built bundle: the participants
// split must render honestly, a posted message must arrive over the live SSE stream, and the
// work-order letterbox must show a filed handoff moving recorded → done through the UI.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8022';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
await p.goto(BASE + '/ceo?tab=hub', { waitUntil: 'domcontentloaded', timeout: 45000 });
await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });

// dismiss the first-visit onboarding tour
for (let i = 0; i < 3; i++) {
  const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
  if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
  await p.keyboard.press('Escape');
  await p.waitForTimeout(400);
  if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
}
await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});

// wait for the panel's async pieces — the SPECIFIC texts, never text already on screen
await p.waitForFunction(() => /Agent Collaboration Hub/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => /platform roster/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => /stream connected/i.test(document.body.innerText), { timeout: 30000 });
const body = () => p.evaluate(() => document.body.innerText.toLowerCase());
let text = await body();

check('panel renders with honest occupancy framing',
  text.includes('agent collaboration hub') && text.includes('no platform module consumes hub messages'));
check('participants split: empty registrations said plainly + live roster',
  text.includes('no external agent session has registered') && text.includes('platform roster'));
check('letterbox honesty on screen',
  text.includes('work-order letterbox') && text.includes('no executor is subscribed'));

// post a message through the UI — it must arrive back over the live SSE stream
await p.locator('input[aria-label="hub message"]').fill('w443 probe salaam');
await p.locator('button:has-text("Post")').click();
await p.waitForFunction(() => /Delivered live to \d+ subscriber/i.test(document.body.innerText), { timeout: 30000 });
await p.waitForFunction(() => {
  const cards = [...document.querySelectorAll('p')].filter(x => x.textContent === 'w443 probe salaam');
  return cards.length > 0;
}, { timeout: 30000 });
text = await body();
check('posted message delivered over live SSE (including this panel)',
  text.includes('including this panel') && text.includes('w443 probe salaam'));

// file a handoff via the API (agents file handoffs; the UI is the letterbox view), reload, move it
const filed = await p.evaluate(async () => {
  const r = await fetch('/api/v1/hub/claude-code-handoff', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ from_agent: 'w443-probe', task_title: 'Probe work-order',
                           task_description: 'verify the letterbox renders and statuses move' }),
  });
  return { ok: r.ok, body: await r.json() };
});
check('handoff filed via API returns recorded + honest note',
  filed.ok && filed.body.status === 'recorded' && /no executor is subscribed/i.test(filed.body.note));

await p.reload({ waitUntil: 'domcontentloaded' });
await p.waitForFunction(() => /Probe work-order/i.test(document.body.innerText), { timeout: 30000 });
await p.locator('button:has-text("claim")').first().click();
await p.waitForFunction(() => /in_progress/i.test(document.body.innerText), { timeout: 30000 });
await p.locator('button:has-text("mark done")').first().click();
await p.waitForFunction(() => {
  const t = document.body.innerText;
  return /Probe work-order/i.test(t) && /\bdone\b/i.test(t) && !/in_progress/i.test(t);
}, { timeout: 30000 });
check('work-order moved recorded → in_progress → done through the UI', true);

await b.close();
console.log(checks.every(Boolean) ? 'RESULT PASS' : 'RESULT FAIL');
process.exit(checks.every(Boolean) ? 0 : 1);
