// W459 (delivery-plan P1.11) — Change Control enforced, in a real browser against the built bundle on a
// FRESH backend (AI_DISABLE_LOCAL=1, auth OFF — the shipped default):
//   · a CONSTITUTIONAL change submitted from the page is CRITICAL, and an incidental override of it is
//     REFUSED (403) with the record unmoved; the page's own "Request review" button on that card HOLDS it
//     (no model verdict, and a CRITICAL change is never decided by the health rule) and the expanded card
//     says so. (A 403 cannot be produced from this page with auth OFF — no button sends an override — so
//     the refusal is asserted on the API, and its on-page wording is covered by the guard, not here.)
//   · the exact body the Sanctum's sovereign vote now sends (with the explicit admin decision) succeeds,
//     sent through the API rather than by clicking the Sanctum, and the record's decision entry names
//     the principal — never "cca_ai" (the button's body itself is pinned by the guard's source check);
//   · a MEDIUM review served by the floor is labelled "organism-health threshold rule (not the model)"
//     on the page, and its text begins "DECIDED BY RULE, NOT BY THE MODEL";
//   · the §17.5 line says "no twin model — health gate only" instead of claiming a forward simulation;
//   · the page's own copy no longer promises an AI review of every change.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://localhost:8055';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 1000 } })).newPage();

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
const api = (path, body, method) => p.evaluate(async ([u, i, m]) => {
  const r = await fetch(u, i || m ? { method: m || 'POST', headers: { 'Content-Type': 'application/json' }, body: i ? JSON.stringify(i) : undefined } : undefined);
  return { status: r.status, body: await r.json().catch(() => null) };
}, [path, body || null, method || null]);
const body = () => p.evaluate(() => document.body.innerText);

const openCCA = async () => {
  await p.goto(BASE + '/change-control', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').length > 40, null, { timeout: 60000 });
  await dismissTour();
  await p.waitForFunction(() => /Change Control Agency/i.test(document.body.innerText), null, { timeout: 60000 });
};

await openCCA();
let text = await body();
check('the page no longer promises that every change is AI-reviewed',
  !/AI-reviewed, and logged/i.test(text) && /each record says what decided it/i.test(text));

// submit a CONSTITUTIONAL change from the page's own form
await p.locator('button', { hasText: /Submit Change Request/i }).first().click();
await p.locator('input[placeholder="Brief change title"]').fill('W459 probe — constitutional');
await p.locator('select').first().selectOption('constitutional');
await p.locator('textarea').first().fill('probe: an incidental override of a CRITICAL change must be refused');
await p.locator('button', { hasText: /^\s*Submit\s*$|Submit Request|Submit change/i }).last().click().catch(() => {});
await p.waitForTimeout(1500);
const all = await api('/api/v1/cca', null, 'GET');
const mine = (all.body?.changes || []).find(c => (c.title || '').includes('W459 probe — constitutional'));
console.log('  submitted:', mine && mine.cca_id, mine && mine.impact_tier);
check('a constitutional change submitted from the page is CRITICAL and sits in the queue',
  !!mine && mine.impact_tier === 'CRITICAL' && mine.status === 'submitted');

// an incidental override is refused, and the record does not move
const refused = await api(`/api/v1/cca/${mine.cca_id}/review`, { override_decision: 'approved' });
const after = await api(`/api/v1/cca/${mine.cca_id}`, null, 'GET');
console.log('  incidental override →', refused.status, JSON.stringify(refused.body).slice(0, 120));
check('an incidental override of a CRITICAL change is refused (403) and the record does not move',
  refused.status === 403 && after.body.status === 'submitted' && after.body.decision === null
  && !(after.body.audit_trail || []).some(e => ['approved', 'rejected'].includes(e.event)));

// the page's own review button on that CRITICAL card: it is "Request review", and it HOLDS the change
await openCCA();
const expand = async (title) => {
  await p.getByText(title, { exact: false }).first().click();
  await p.waitForTimeout(1200);
};
await expand('W459 probe — constitutional');
const reviewBtn = p.locator('button', { hasText: /Request review/i }).first();
await reviewBtn.waitFor({ timeout: 20000 }).catch(() => {});
const noAiReview = (await p.locator('button', { hasText: /AI Review/i }).count()) === 0;
const hasRequest = (await reviewBtn.count()) > 0;
if (hasRequest) await reviewBtn.click();
// wait for the RECORD to be held (not a fixed sleep — under_review/decision null also exists mid-review),
// then read the SAME expanded card with no reload: its detail must refetch itself when the row moves
let heldRec = {};
for (let i = 0; i < 60; i++) {
  heldRec = (await api(`/api/v1/cca/${mine.cca_id}`, null, 'GET')).body;
  if (heldRec.decision_source === 'held_awaiting_admin') break;
  await p.waitForTimeout(500);
}
await p.waitForFunction(() => /held — awaiting/i.test(document.querySelector('[data-testid="cca-decision-source"]')?.innerText || ''),
  null, { timeout: 30000 }).catch(() => {});
const heldText = await p.evaluate(() => document.body.innerText);
const heldSrc = await p.evaluate(() => document.querySelector('[data-testid="cca-decision-source"]')?.innerText || '');
console.log('  after "Request review":', heldRec.status, heldRec.decision, '| source line:', heldSrc);
check('the card’s "Request review" (never "AI Review") HOLDS the CRITICAL change, the card says it is held (not "decided by") and where to decide it',
  noAiReview && hasRequest && heldRec.status === 'under_review' && heldRec.decision === null
  && heldRec.decision_source === 'held_awaiting_admin' && heldRec.hold_reason === 'critical_requires_admin_decision'
  && /HELD — a CRITICAL change is decided only by an explicit admin decision/i.test(heldText)
  && /held — awaiting an explicit admin decision/i.test(heldSrc) && !/decided by/i.test(heldSrc)
  && /Sovereign Sanctum/i.test(heldSrc));

// the Sanctum's sovereign vote carries the explicit admin decision — and it is attributed
const voted = await api(`/api/v1/cca/${mine.cca_id}/review`,
  { override_decision: 'approved', admin_decision_for_critical: true, reviewer_notes: 'Sovereign vote — Owner decision from the Sanctum' });
const rec = (await api(`/api/v1/cca/${mine.cca_id}`, null, 'GET')).body;
const decision = (rec.audit_trail || []).filter(e => ['approved', 'rejected'].includes(e.event)).pop() || {};
console.log('  decision entry:', JSON.stringify(decision));
check('an explicit admin decision is accepted and attributed to the principal, never to "cca_ai"',
  voted.status === 200 && decision.by === 'single-user-mode' && decision.by_verified === false
  && decision.decided_by === 'admin_override' && !JSON.stringify(rec.audit_trail).includes('cca_ai'));

// a MEDIUM review served by the floor is labelled as the rule it is
const med = await api('/api/v1/cca/submit', { title: 'W459 probe — medium', change_type: 'config_major', description: 'probe: what decided this review' });
const rv = await api(`/api/v1/cca/${med.body.cca_id}/review`, {});
const medRec = (await api(`/api/v1/cca/${med.body.cca_id}`, null, 'GET')).body;
console.log('  decision_source:', rv.body?.decision_source);
await openCCA();
await expand('W459 probe — medium');
await p.waitForFunction(() => !!document.querySelector('[data-testid="cca-decision-source"]'), null, { timeout: 30000 }).catch(() => {});
const medSrc = await p.evaluate(() => document.querySelector('[data-testid="cca-decision-source"]')?.innerText || '');
console.log('  medium source line:', medSrc);
check('a review with no model verdict is labelled the organism-health threshold rule — in the record AND on the card',
  rv.body?.decision_source === 'health_threshold_rule'
  && medRec.review_result.startsWith('DECIDED BY RULE, NOT BY THE MODEL')
  && /decided by: organism-health threshold rule \(not the model\)/i.test(medSrc));

// the §17.5 line on screen says there is no twin model
const high = await api('/api/v1/cca/submit', { title: 'W459 probe — high', change_type: 'security_change', description: 'probe: the twin line' });
await api(`/api/v1/cca/${high.body.cca_id}/review`, { override_decision: 'approved' });
await openCCA();
await p.locator('div', { hasText: /W459 probe — high/ }).last().click().catch(() => {});
await p.waitForFunction(() => !!document.querySelector('[data-testid="cca-twin-line"]'), null, { timeout: 30000 }).catch(() => {});
const twinLine = await p.evaluate(() => document.querySelector('[data-testid="cca-twin-line"]')?.innerText || '');
const srcLine = await p.evaluate(() => document.querySelector('[data-testid="cca-decision-source"]')?.innerText || '');
console.log('  twin line:', twinLine, '| source line:', srcLine);
check('the §17.5 line on screen says there is no twin model, and the decision source is shown',
  /no twin model — health gate only/i.test(twinLine) && !/forward simulation/i.test(twinLine)
  && /an explicit admin decision/i.test(srcLine));

await b.close();
const pass = checks.filter(Boolean).length;
console.log(`\n${pass}/${checks.length} checks passed`);
process.exit(pass === checks.length ? 0 : 1);
