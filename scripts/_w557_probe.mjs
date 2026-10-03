// W557 (P2.16) — the companion surface: the three states must be REACHABLE ON THE PAGE, and nothing on
// it may claim an alignment the kernel did not evaluate.
//
//   python scripts/_w557_probe_seed.py          # seeds the three record shapes through the kernel
//   node scripts/_w557_probe.mjs http://127.0.0.1:5173
//
// THE CLAUSE THAT DECIDES THIS PROBE. "No escalations" and "no escalation list" are different facts, and
// the second one is the ordinary state on a deployment with no model. A page that drew the same thing
// for both would tell a reader their request had been screened and cleared when nothing had read it.
import { chromium } from 'playwright';

const BASE = process.argv[2] || 'http://127.0.0.1:5173';
const checks = [];
const notAssessed = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const checkIf = (name, assessable, ok) => {
  if (!assessable) { notAssessed.push(name); console.log(`NOT ASSESSABLE ${name}`); return; }
  checks.push(ok); console.log(`RESULT ${name}:`, ok);
};

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(`${BASE}/horizon-companion`, { waitUntil: 'networkidle' });
await page.waitForSelector('[data-testid="companion-record"]', { timeout: 20000 }).catch(() => {});

const cards = page.locator('[data-testid="companion-record"]');
const n = await cards.count();
check('the companion surface renders the recorded requests', n >= 3);

const texts = [];
for (let i = 0; i < n; i++) texts.push(await cards.nth(i).innerText());
const all = texts.join('\n---\n');

// ── 1. THE NOT-COMPRESSED STATE, which is the ordinary one here ─────────────────────────────────
check('the not-compressed state is reachable on the page',
  /Not compressed/i.test(all));
check('and it carries the kernel\'s own reason rather than a bare label',
  /composes structured output from the request/i.test(all)
  || /NO COMPRESSOR WAS CALLED/i.test(all));

// ── 2. THE NO-ESCALATION STATE — the compression ANSWERED, and the answer was none ──────────────
check('the no-escalation state is reachable on the page',
  /None raised\s*—\s*the compression answered/i.test(all));

// ── 3. AND IT IS NOT THE SAME AS NO LIST AT ALL. This is the clause: an absent list is not an
//       empty one, and the page must say so in words a reader can act on.
check('an absent escalation list renders as NOT EVALUATED, not as "none"',
  /Not evaluated/i.test(all));
check('and the page states that the absence is not an absence of escalations',
  /absence is not an absence of escalations/i.test(all));

// ── 4. NOTHING CLAIMS AN ALIGNMENT THE KERNEL DID NOT EVALUATE ──────────────────────────────────
const termNodes = page.locator('[data-testid="decision-term"]');
const termCount = await termNodes.count();
const termTexts = [];
for (let i = 0; i < termCount; i++) termTexts.push(await termNodes.nth(i).innerText());
check('every decision term is shown, including the ones nothing evaluated', termCount >= 3);
check('an unevaluated term renders as NOT EVALUATED and never as a pass',
  termTexts.some(t => /Not evaluated/i.test(t))
  && !termTexts.some(t => /Not evaluated/i.test(t) && /\bpassed\b|\bcleared\b|\bok\b/i.test(t)));
// the three term states must be DISTINGUISHABLE, or the column carries no information
check('the three term states are distinguishable on the page',
  termTexts.some(t => /FIRED/.test(t))
  && termTexts.some(t => /did not fire/i.test(t))
  && termTexts.some(t => /Not evaluated/i.test(t)));

// ── 5. THE OWNER'S OWN ENTRY, absent, in the item's own words ───────────────────────────────────
check('an unset reflection tag renders as "no station assigned"',
  /No station assigned/i.test(all));
// ASSERT THE ABSENCE OF A VALUE, NOT THE ABSENCE OF WORDS. The first version of this check scanned the
// block for "suggested|inferred|auto-generated" and failed — on the kernel's own basis, which says "no
// suggestion is persisted as a value, and nothing is inferred from the observation's text". It forbade
// the vocabulary the honest sentence needs in order to DENY the thing: the same shape as a fix comment
// quoting the literal its own guard forbids. What matters is that no VALUE is rendered where the user's
// words would go, so that is what is checked.
const reflection = await page.locator('[data-testid="companion-reflection"]').first().innerText();
check('an unset tag renders no value at all — the quoted form appears only when the user has set one',
  /No station assigned/i.test(reflection) && !/[“"].+[”"]/.test(reflection));
check('and the page carries the kernel\'s own statement that no AI writes this field',
  /no AI ever writes it/i.test(reflection));

// ── 6. CONSUMPTION IS NOT BUILT, AND THE PAGE SAYS SO RATHER THAN SHOWING A ZERO ────────────────
const consumption = await page.locator('[data-testid="companion-consumption"]').first().innerText();
check('consumption renders as NOT RECORDED', /Not recorded/i.test(consumption));
check('and no zero stands in for an unmeasured cost',
  !/\b0(\.0+)?\s*(ms|s|tokens|wst)?\b/i.test(consumption.replace(/P2\.15/g, '')));

await browser.close();

const passed = checks.filter(Boolean).length;
console.log(`\n${passed}/${checks.length} check(s) passed; ${notAssessed.length} NOT ASSESSABLE` +
  (notAssessed.length ? ` (${notAssessed.join(', ')})` : ''));
if (passed !== checks.length) process.exit(1);
