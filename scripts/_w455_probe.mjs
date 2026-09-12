// W455 (delivery-plan P1.7) — compliance that reads, in a real browser against the built bundle on a FRESH
// backend (AI_DISABLE_LOCAL=1): the Governance › Compliance tab shows the constitutional row as "not checked"
// for content (never a green "Constitutional gate clear"), the Frameworks card says what each check does,
// a laundering subject fails with an audit hash over the subject; a FAIL deliverable shows on the list row
// and its export carries the verdict on page one.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8042';
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
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), { timeout: 10000 }).catch(() => {});
};
const body = () => p.evaluate(() => document.body.innerText);
const open = async (path) => {
  await p.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
  await dismissTour();
};

// ── 1. Governance › Compliance: the Frameworks card says what each check does ──
await open('/governance-hub?tab=compliance');
await p.waitForFunction(() => /Frameworks/i.test(document.body.innerText) && /not legal advice/i.test(document.body.innerText), { timeout: 30000 });
let text = await body();
check('frameworks card: labels say what each check does (not legal advice · not a certification · does not read content)',
  /not legal advice/i.test(text) && /not a certification/i.test(text) && /does not read content/i.test(text) && !/engine-grade/i.test(text));
check('header copy: it flags, it does not certify', /It flags; it does not certify/i.test(text));

// ── 2. a laundering subject: overall FAIL; the constitutional row is "not checked", never a green pass ──
await p.locator('textarea').first().fill('A scheme to launder cash through shell companies, evade tax and bribe an official');
await p.locator('button', { hasText: /Run Compliance Check/i }).first().click();
await p.waitForFunction(() => /uk legal · fail/i.test(document.body.innerText), { timeout: 60000 });
text = await body();
check('laundering: overall FAIL, uk legal fail with an audit hash over the subject', /^FAIL$/mi.test(text) && /uk legal · fail/i.test(text) && /over the subject/i.test(text));
check('laundering: the constitutional row reads "not checked" with the reason, never "Constitutional gate clear"',
  /constitutional · not checked/i.test(text) && /gates agent actions/i.test(text) && !/Constitutional gate clear/i.test(text));

// ── 3. a subject outside every vocabulary: review — no engine covers this area ──
await p.locator('textarea').first().fill('Lorem ipsum text about gardening tulips in spring');
await p.locator('button', { hasText: /Run Compliance Check/i }).first().click();
await p.waitForFunction(() => /sharia halal · review/i.test(document.body.innerText), { timeout: 60000 });
text = await body();
check('lorem: review with "no engine covers this area", not a green pass', /^REVIEW$/mi.test(text) && /nothing here read this subject/i.test(text));

// ── 4. a FAIL deliverable: the list row says so, the export carries the verdict on page one ──
const d = await p.evaluate(async () => {
  const doc = ['Executive Summary', 'Structure', 'Cash Flow', 'Next Steps'].map(s => `## ${s}\n` + 'We launder cash through shell companies and bribe officials to keep the scheme running. '.repeat(3)).join('\n');
  const r = await fetch('/api/v1/deliverables/produce', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ type: 'report', title: 'w455 probe fail', brief: 'launder cash', content: doc }) });
  return await r.json();
});
await open('/deliverables');
await p.waitForFunction(() => /compliance FAIL/i.test(document.body.innerText), { timeout: 30000 });
text = await body();
check('deliverables list: the failing row wears "compliance FAIL"', /compliance FAIL/i.test(text));
await p.locator('button', { hasText: /w455 probe fail/i }).first().click();
await p.waitForFunction(() => /Download \(carries FAIL verdict\)/i.test(document.body.innerText), { timeout: 30000 });
const md = await p.evaluate(async (id) => await (await fetch(`/api/v1/deliverables/${id}/export?format=md`)).text(), d.id);
const html = await p.evaluate(async (id) => await (await fetch(`/api/v1/deliverables/${id}/export?format=html`)).text(), d.id);
check('export: md and html carry "COMPLIANCE VERDICT: FAIL … NOT cleared for use" on page one',
  /COMPLIANCE VERDICT: FAIL/.test(md.slice(0, 1200)) && /NOT cleared for use/.test(md.slice(0, 1200)) && /COMPLIANCE VERDICT: FAIL/.test(html.slice(0, 1500)));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
