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
import { readFileSync } from 'node:fs';

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
  // W399 — surfaces added on 2026-08-31, none of which the smoke covered:
  ['/marketplace',      ['Living Marketplace']],
  ['/vsb-cockpit',      ['VSB Cockpit']],
  ['/ceo?tab=board',    ['Board of Directors', 'Apex Governance']],
  // W437 — the native fabric page gained the primitive console + fabric integrity strip
  ['/native-ai',        ['In-House AI Resources']],
  // W438 — the organism's Anatomy tab: 18 audited-then-wired routes
  ['/organism?tab=anatomy', ['Anatomy', 'Organism']],
  // W439 — QEP in the Religion domain (Owner directive) + the /qep studio
  ['/religion?tab=qep',  ['Quran Education Platform', 'Spire of Inquiry']],
  ['/qep',              ['QEP']],
  // W440 — the VBS management systems, operating (not just their standards cards)
  ['/vsb-cockpit?tab=systems', ['VSB Cockpit']],
  // W443 — the Agent Collaboration Hub's first surface (bus + registry + work-order letterbox)
  ['/ceo?tab=hub',      ['Agent Collaboration Hub']],
];

// The landmark check above passes if ANY landmark is present, which proves the route did not crash
// but says nothing about a section quietly failing to render. These must ALL be present. Each entry
// is a surface that shipped with no coverage and would otherwise regress in silence — the §15
// contracts card, the charity directives, the board charter's invariant, and the marketplace's
// listings layer.
const REQUIRED_SECTIONS = {
  '/economy': ['Service contracts', 'Charity directives', 'Venture Portfolio', 'Close period', 'Transfer WST between your entities', 'Charity candidates'],
  '/ceo?tab=board': ['cannot instruct the board'],
  // W443 — the hub's honesty lines: unoccupied bus + records-only letterbox must stay on screen
  '/ceo?tab=hub': ['no executor is subscribed', 'work-order letterbox'],

  // W444 — all listings render (unpriced badged); pricing/edit lives in the detail drawer
  '/marketplace': ['Listings', 'set its price'],
  // W437 — the console that finally makes the 10 audited primitives reachable, and the integrity strip
  '/native-ai': ['Primitive console', 'Fabric integrity'],
  // W440 — the operating VBS systems panel must render on the cockpit's Living Systems tab
  // 'nothing simulated' renders only from LIVE /vbs/systems data (QMS/DCMS rows), so the guard
  // is data-driven, not just static headings (refuter catch: the h4 needles pass with dead APIs)
  '/vsb-cockpit?tab=systems': ['quality gates', 'document control', 'Mycelial backbone', 'nothing simulated'],
  // W438 — the anatomy surfaces must ALL render: health disclosure, genome lab, wiring truth
  '/organism?tab=anatomy': ['measured only', 'Genome lab', 'wiring truth', 'Change history', 'Reset to defaults'],
  // W439 — the REAL QEP studio must render inside the Religion domain, honestly framed
  '/religion?tab=qep': ['authentic text', 'spaced repetition', 'false witness'],
  // /qep opens on the AI Coach tab: the honest no-phonetic-model banner + the pointer to the
  // live written-text tools must both render
  '/qep': ['Recitation assessment unavailable', 'written-recall', 'Intelligence'],
};

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

    // 1b. required sections must ALL be present, not merely one landmark
    for (const needle of REQUIRED_SECTIONS[route] ?? []) {
      if (!body.toLowerCase().includes(needle.toLowerCase())) {
        failures.push(`${route}: required section missing — ${JSON.stringify(needle)}`);
      }
    }

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
  let text = await page.evaluate(() => document.body.innerText || '');
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
  // Wait for rows rather than sampling once. The page fetches its data after mount, so a single
  // read races the render: under load this reported "the API returned 50 changes but NONE rendered"
  // on a page that was simply still loading, and passed on the very next run. The guard keeps its
  // teeth - if the rows never arrive within the window it still fails - but it no longer fails at
  // random, which is the only way anyone will trust it.
  if (apiCount > 0) {
    await page
      .waitForFunction(
        () => /config_minor|config_major|organism_mutation|immune_reconfiguration|vsb_evolution|genome_edit/i
          .test(document.querySelector("#root")?.innerText || ""),
        { timeout: 20_000 },
      )
      .catch(() => {});
    text = await page.evaluate(() => document.querySelector("#root")?.innerText || "");
  }
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

// -- W429: PDFs are extracted IN THE BROWSER, and nothing is fetched to do it ------------------
// The defining property of AttachDocument is that the file never leaves the machine. pdf.js will
// happily fetch its worker from a CDN if left to resolve one itself, which would quietly trade that
// away - so this asserts the extraction WORKS and that it made no external request while doing it.
// The fixture is generated here rather than committed: a 600-byte hand-built PDF needs no binary in
// the tree and cannot rot.
{
  const NL = String.fromCharCode(10);
  const mkPdf = (text) => {
    const objs = [
      "<< /Type /Catalog /Pages 2 0 R >>",
      "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      "<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ];
    const stream = text
      ? "BT /F1 18 Tf 72 700 Td (" + text + ") Tj ET"
      : "0 0 0 rg 72 700 100 50 re f";          // no text operators at all = a "scanned" page
    objs.push("<< /Length " + stream.length + " >>" + NL + "stream" + NL + stream + NL + "endstream");
    let out = "%PDF-1.4" + NL;
    const offsets = [];
    objs.forEach((body, i) => { offsets.push(out.length); out += (i + 1) + " 0 obj" + NL + body + NL + "endobj" + NL; });
    const xrefAt = out.length;
    out += "xref" + NL + "0 " + (objs.length + 1) + NL + "0000000000 65535 f " + NL;
    offsets.forEach(o => { out += String(o).padStart(10, "0") + " 00000 n " + NL; });
    out += "trailer" + NL + "<< /Size " + (objs.length + 1) + " /Root 1 0 R >>" + NL
        + "startxref" + NL + xrefAt + NL + "%%EOF" + NL;
    return Buffer.from(out, "latin1");
  };

  const external = [];
  const onReq = (r) => {
    const u = r.url();
    if (!u.startsWith(BASE) && !u.startsWith("data:") && !u.startsWith("blob:")) external.push(u);
  };
  page.on("request", onReq);
  await page.goto(`${BASE}/genesis`, { waitUntil: "domcontentloaded", timeout: 45_000 });
  await page.waitForFunction(() => (document.querySelector("#root")?.innerText || "").length > 40,
    { timeout: 20_000 }).catch(() => {});

  if (!(await page.evaluate(() => !!document.querySelector("input[type=file]")))) {
    failures.push("/genesis: no file input - the attach control is gone");
  } else {
    await page.setInputFiles("input[type=file]",
      { name: "probe.pdf", mimeType: "application/pdf", buffer: mkPdf("WORKSTATION PDF PROBE 4271") });
    await page.waitForTimeout(4_000);
    const fields = await page.evaluate(() => [...document.querySelectorAll("textarea")].map(x => x.value).join(" | "));
    if (!/WORKSTATION PDF PROBE 4271/.test(fields)) failures.push("PDF text was not extracted into the field");
    if (!/PDF text layer/.test(fields)) failures.push("the attached block does not state what was read");

    // A scanned PDF has no text layer. Attaching an empty document, or showing a cheerful chip over
    // nothing, would be a small lie about what was read.
    await page.setInputFiles("input[type=file]",
      { name: "scanned.pdf", mimeType: "application/pdf", buffer: mkPdf("") });
    await page.waitForTimeout(4_000);
    const body = await page.evaluate(() => document.querySelector("#root")?.innerText || "");
    if (!/No text layer/.test(body)) failures.push("an image-only PDF was not honestly refused");
    note(`PDF extraction ok (${external.length} external requests)`);
  }
  if (external.length) failures.push(`PDF extraction fetched ${external.length} external URL(s): ${external.slice(0, 2).join(", ")}`);
  page.off("request", onReq);
}

// -- W402: every remaining route must at least render ----------------------------------------
// The checks above go deep on 11 routes. The app has ~71, and a crash on any of the others would
// go unnoticed - today a single unrenderable value (React #31) took down a whole route through the
// error boundary. This pass is shallow but total: every static route renders something, shows no
// error boundary, and logs no console error.
//
// The route list is PARSED FROM App.tsx at run time rather than hardcoded, so a new page is covered
// the moment it is added and this cannot silently drift out of date.
const appSource = readFileSync(new URL("../apps/workstation-superapp/src/App.tsx", import.meta.url), "utf-8");
const swept = [...new Set([...appSource.matchAll(/<Route\s+path="([^"]+)"/g)].map((m) => m[1]))]
  .filter((r) => r !== "/" && !r.includes("*") && !r.includes(":"))
  .filter((r) => !ROUTES.some(([done]) => done.split("?")[0] === r));

note(`sweeping ${swept.length} further routes (render-only)`);
for (const route of swept) {
  const errs = [];
  const onErr = (m) => { if (m.type() === "error") errs.push(m.text().slice(0, 160)); };
  page.on("console", onErr);
  // One retry on a navigation timeout. Sweeping 60+ routes back to back loads the machine, and two
  // consecutive runs failed on DIFFERENT routes (/nexus, then /capital) - that is a timing flake,
  // not a broken page, and a gate that fails at random teaches people to ignore it. A page that
  // genuinely cannot load still fails, because it fails twice.
  let navErr = null;
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      await page.goto(`${BASE}${route}`, { waitUntil: "domcontentloaded", timeout: 45_000 });
      navErr = null;
      break;
    } catch (e) {
      navErr = e;
    }
  }
  if (navErr) {
    failures.push(`${route}: navigation failed twice - ${String(navErr).slice(0, 120)}`);
    page.off("console", onErr);
    continue;
  }
  try {
    await page
      .waitForFunction(() => (document.querySelector("#root")?.innerText || "").trim().length > 40,
                       { timeout: 20_000 })
      .catch(() => {});
    await page.waitForTimeout(500);
    const body = await page.evaluate(() => document.querySelector("#root")?.innerText || "");
    if (/something went wrong|unexpected error occurred/i.test(body)) {
      failures.push(`${route}: an error boundary is showing`);
    } else if (body.trim().length < 120) {
      failures.push(`${route}: near-empty render (${body.trim().length} chars)`);
    }
    // Dev-only noise: the vite origin and the ws stream are not part of this assertion.
    const real = errs.filter((e) => !/favicon|ERR_CONNECTION_REFUSED|WebSocket/i.test(e));
    if (real.length) failures.push(`${route}: console error - ${real[0]}`);
  } catch (e) {
    failures.push(`${route}: render check failed - ${String(e).slice(0, 120)}`);
  }
  page.off("console", onErr);
}

await browser.close();

if (failures.length) {
  console.error(`\nBROWSER SMOKE FAILED — ${failures.length} user-visible problem(s):`);
  for (const f of failures) console.error(`  - ${f}`);
  process.exit(1);
}
console.log(`\nBROWSER SMOKE PASSED — ${ROUTES.length} routes rendered, plus ${swept.length} swept, no console errors, no fabrications.`);
