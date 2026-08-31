/**
 * Browser smoke — the guard the response-shape tests cannot provide.
 *
 * Round 11 fixed a governance page that rendered permanently empty, handlers that fabricated
 * success, and a customer-facing app that displayed engine scaffolding. Every one of those passed
 * the backend suite and CI: the endpoints returned 200 with real bytes. They were only found by
 * loading the pages and reading what was on screen. This does that, automatically.
 *
 * Deliberately NARROW and deterministic (option B — smoke, not a full ledger replay):
 *   - loads the core §3A routes and asserts each renders its own landmark content
 *   - fails on ANY unhandled console error or failed same-origin request
 *   - fails if a known fabricated marker ever appears in rendered text
 *   - asserts the Change Control page shows real structure (the cluster-1 defect class)
 * It does NOT run AI generations: those take minutes on the owned model and would make the smoke
 * both slow and non-deterministic. Model behaviour is verified separately (§6).
 *
 * Usage:  node scripts/browser_smoke.mjs [baseURL]
 * Exit 0 = clean, 1 = a real user-visible problem.
 */
import { chromium } from 'playwright';

const BASE = process.argv[2] || process.env.SMOKE_BASE_URL || 'http://localhost:8010';

// Strings that only ever existed to make an unbuilt capability look real (Round 11, W374).
const FABRICATIONS = [
  'All systems nominal',
  'Engine running at 100',
  'CERT-87a1b2c3',
  'Historical_Makkah_360',
  '142 cross-realm',
  'Provisioning infrastructure',
];

// route → a landmark string that proves the page rendered its OWN content, not a blank shell
const ROUTES = [
  ['/',                 ['Workstation', 'Command']],
  ['/domains',          ['Domain']],
  ['/deliverables',     ['Deliverable']],
  ['/change-control',   ['Change Control']],
  ['/genesis',          ['Genesis']],
  ['/economy',          ['Economy', 'Metabolism']],
  ['/my-work',          ['My Work']],
  ['/governance-hub',   ['Governance']],
];

const failures = [];
const note = (m) => console.log(`  ${m}`);

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await ctx.newPage();

for (const [route, landmarks] of ROUTES) {
  const consoleErrors = [];
  const badRequests = [];
  const onConsole = (msg) => { if (msg.type() === 'error') consoleErrors.push(msg.text().slice(0, 200)); };
  const onResponse = (res) => {
    const u = res.url();
    if (u.startsWith(BASE) && res.status() >= 500) badRequests.push(`${res.status()} ${u.replace(BASE, '')}`);
  };
  page.on('console', onConsole);
  page.on('response', onResponse);

  try {
    // 'networkidle' is the wrong condition for this app: several pages poll
    // /api/v1/biometrics/status on an interval, so the network may never go idle and the
    // navigation times out at random under load. That produced a red /domains on a run where the
    // page rendered perfectly. Wait for the document instead, then for the app to actually paint
    // something into #root — which is what we are really asserting.
    await page.goto(`${BASE}${route}`, { waitUntil: 'domcontentloaded', timeout: 45_000 });
    await page.waitForFunction(
      () => (document.querySelector('#root')?.innerText || '').trim().length > 40,
      { timeout: 30_000 },
    );
    await page.waitForTimeout(1200);           // let deferred renders settle
    const body = await page.evaluate(() => document.body.innerText || '');

    // 1. the page rendered its own content (not a blank shell / crashed boundary)
    const hit = landmarks.find((l) => body.toLowerCase().includes(l.toLowerCase()));
    if (!hit) failures.push(`${route}: none of ${JSON.stringify(landmarks)} rendered — blank or crashed page`);

    // 2. no fabricated marker is shown to a user
    for (const f of FABRICATIONS) {
      if (body.includes(f)) failures.push(`${route}: fabricated marker on screen — ${JSON.stringify(f)}`);
    }

    // 3. React error boundaries / hard crashes
    if (/something went wrong|unexpected error occurred/i.test(body)) {
      failures.push(`${route}: an error boundary is showing`);
    }

    // 4. the page did not error in the console, and no 5xx came back
    if (consoleErrors.length) failures.push(`${route}: console errors — ${consoleErrors.slice(0, 3).join(' | ')}`);
    if (badRequests.length) failures.push(`${route}: server errors — ${[...new Set(badRequests)].slice(0, 3).join(' | ')}`);

    note(`${route.padEnd(18)} ok  (${body.length} chars rendered)`);
  } catch (err) {
    failures.push(`${route}: navigation failed — ${String(err).slice(0, 160)}`);
    note(`${route.padEnd(18)} FAILED`);
  } finally {
    page.off('console', onConsole);
    page.off('response', onResponse);
  }
}

// The cluster-1 class specifically: the governance surface must show real structure, never a bare
// shell. It rendered permanently empty for months because the UI read keys the API never returned.
try {
  await page.goto(`${BASE}/change-control`, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  await page.waitForFunction(
    () => (document.querySelector('#root')?.innerText || '').trim().length > 40,
    { timeout: 30_000 },
  );
  await page.waitForTimeout(1000);
  const text = await page.evaluate(() => document.body.innerText || '');
  const hasStats = /pending/i.test(text) && /approved/i.test(text);
  if (!hasStats) failures.push('/change-control: the stats row did not render');

  // The assertion that actually BITES: compare the page against what the BACKEND holds.
  //
  // An earlier version accepted "rows OR the honest empty state" — and passed when the cluster-1
  // defect was deliberately reintroduced, because reading the wrong key yields an empty list and
  // the page then shows its (honest, correct) empty state. Accepting that made the guard blind to
  // the exact class it exists for. If the API returns changes, they MUST be on screen.
  const apiCount = await page.evaluate(async () => {
    try {
      const r = await fetch('/api/v1/cca');
      if (!r.ok) return -1;
      const d = await r.json();
      return Array.isArray(d.changes) ? d.changes.length : -1;
    } catch { return -1; }
  });
  // snake_case ONLY: rows render the raw change_type ("config_minor"), while the static tier legend
  // renders prose ("CRITICAL — Constitutional Change"). An earlier list included /constitutional/,
  // which matched the LEGEND and reported rows on a page that had none — the guard passed while the
  // defect was reintroduced. Chrome must never be able to satisfy a data assertion.
  const ROW_TOKENS = /config_minor|config_major|organism_mutation|immune_reconfiguration|vsb_evolution|genome_edit/i;
  const rowsOnScreen = ROW_TOKENS.test(text);
  const honestEmpty = /no change requests yet/i.test(text);

  if (apiCount > 0 && !rowsOnScreen) {
    failures.push(`/change-control: the API returned ${apiCount} changes but NONE rendered — ` +
                  'the governance surface is showing an empty page over real data');
  } else if (apiCount === 0 && !honestEmpty) {
    failures.push('/change-control: no data and no honest empty state — the page says nothing');
  } else if (apiCount < 0) {
    failures.push('/change-control: could not read /api/v1/cca to verify the page against its data');
  }
  note(`/change-control    verified against data (api=${apiCount}, rows=${rowsOnScreen}, empty=${honestEmpty})`);
} catch (err) {
  failures.push(`/change-control structure check failed — ${String(err).slice(0, 160)}`);
}

await browser.close();

if (failures.length) {
  console.error(`\nBROWSER SMOKE FAILED — ${failures.length} user-visible problem(s):`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}
console.log(`\nBROWSER SMOKE PASSED — ${ROUTES.length} routes rendered, no console errors, no fabrications.`);
