// W449 (delivery-plan P1.1) — drive the living-QMS gate's three honest states in a real browser against
// the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1 → the floor serves every gateway call): a
// produced deliverable, a domain tool, an org cascade and a Genesis journey must each show the slate
// "QMS —" (not assessable) chip — never a green "pass" beside the amber floor badge — and the domain
// tool's coverage is now measured against the prompt's own sections.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8026';
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
const body = () => p.evaluate(() => document.body.innerText.toLowerCase());
const open = async (path) => {
  await p.goto(BASE + path, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, { timeout: 20000 });
  await dismissTour();
};

// ── 1. Deliverables: produce on the floor → the gate chip is "—", with its basis in the title ──
await open('/deliverables');
await p.locator('textarea').first().fill('A halal artisan bakery in Leeds serving students — a short market brief');
await p.locator('button', { hasText: /Produce report/i }).first().click();
// wait for the SPECIFIC outcome element (rule 22): the gate chip of the selected deliverable
await p.waitForFunction(() => /Living-QMS gate: —/i.test(document.body.innerText), { timeout: 90000 });
let text = await body();
check('deliverable: gate chip is "—" (not assessable), not pass', text.includes('living-qms gate: —') && !text.includes('living-qms gate: pass'));
check('deliverable: floor badge amber beside it', text.includes('structured floor — not model analysis'));
const chipTitle = await p.locator('span', { hasText: /Living-QMS gate: —/ }).first().getAttribute('title');
check('deliverable: the chip carries the not-assessable basis', /not assessable/i.test(chipTitle || ''));

// ── 2. A domain tool (Education › Curriculum Designer, defaults pre-filled): "QMS —", never "QMS pass" ──
await open('/education?tab=curriculum');
await p.locator('button', { hasText: /Design curriculum/i }).first().click();
await p.waitForFunction(() => /QMS —/.test(document.body.innerText), { timeout: 120000 });
text = await body();
check('domain tool: gate chip is "qms —", not "qms pass" or "qms flagged"',
  text.includes('qms —') && !text.includes('qms pass') && !text.includes('qms flagged'));

// ── 3. Org cascade (Living Organisation › Swarm): "QMS gate —" on the run ──
await open('/ceo?tab=swarm');
await p.locator('input[placeholder*="mission" i], textarea[placeholder*="mission" i]').first().fill('w449 probe: launch a halal meal-prep pilot in Leeds');
await p.locator('button', { hasText: /^Cascade$/ }).first().click();
await p.waitForFunction(() => /QMS gate: —/i.test(document.body.innerText), { timeout: 240000 });
text = await body();
check('cascade: gate chip is "qms gate: —", not pass', text.includes('qms gate: —') && !text.includes('qms gate: pass'));

// ── 4. Genesis journey: the same chip on the flagship surface (stage checks already said so since W436) ──
await open('/genesis');
await p.locator('textarea').first().fill('Beekeepers in Somerset lose colonies to varroa and cannot afford lab testing');
await p.locator('button', { hasText: /begin|run|start|journey/i }).first().click();
await p.waitForFunction(() => /Living-QMS gate: —/i.test(document.body.innerText), { timeout: 300000 });
text = await body();
check('genesis: gate chip is "living-qms gate: —" beside the not-assessable stage checks',
  text.includes('living-qms gate: —') && !text.includes('living-qms gate: pass'));

// ── 5. Refuter F1 — the Genesis page's "Report" button saves the floor journey VERBATIM as a deliverable.
//      The gate had been told only served_by="verbatim-ingest" and certified it PASS. Now the page
//      posts the journey's provenance and the stored deliverable says not assessable (floor origin).
await p.locator('button', { hasText: /Report/ }).first().click();
await p.waitForFunction(async () => {
  const r = await fetch('/api/v1/deliverables').then(x => x.json()).catch(() => null);
  return !!(r?.deliverables || []).find(d => (d.title || '').startsWith('Genesis:'));
}, null, { timeout: 60000 });
const gen = await p.evaluate(async () => {
  const r = await fetch('/api/v1/deliverables').then(x => x.json());
  const row = (r.deliverables || []).find(d => (d.title || '').startsWith('Genesis:'));
  return await fetch(`/api/v1/deliverables/${row.id}`).then(x => x.json());
});
const gq = gen?.quality_assurance?.quality || {};
console.log('  saved journey deliverable:', gen?.ai_provenance?.served_by, JSON.stringify(gen?.ai_provenance?.source_served_by), gq.qms_gate_passed, (gq.qms_basis || '').slice(0, 60));
check('genesis → deliverable: verbatim ingest carries the floor origin and is not assessable (never pass)',
  gen?.ai_provenance?.served_by === 'verbatim-ingest' && !!gen?.ai_provenance?.source_served_by?.native
  && gq.qms_gate_passed === null && /floor-served/.test(gq.qms_basis || ''));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
