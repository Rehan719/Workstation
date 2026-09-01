/**
 * Interactive button / user-journey sweep.
 *
 * v1 of this script reported "864 controls, 0 failing" — and was BLIND. 10 global chrome controls
 * (sidebar + header) render on all 72 routes, so with a 12-label cap ~10 of every route's 12 slots
 * were the SAME nav buttons, clicked 72 times each. Only 62 labels were page-specific. The zero
 * described the nav bar, not the pages.
 *
 * So: pass 1 enumerates labels everywhere WITHOUT clicking and derives the global chrome set
 * (any label on >= 50% of routes); pass 2 clicks only page-specific controls, plus the chrome once.
 * A self-test proves the response detector can fire before any result is trusted.
 */
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';

const BASE = process.argv[2] || 'http://localhost:8010';
const app = readFileSync(new URL('../apps/workstation-superapp/src/App.tsx', import.meta.url), 'utf-8');
const routes = [...new Set([...app.matchAll(/<Route\s+path="([^"]+)"/g)].map(m => m[1]))]
  .filter(r => !r.includes('*') && !r.includes(':'));

const UNSAFE = /delete|remove|clear|reset|purge|deregister|retire|reject|approve|publish|send|pay|purchase|settle|apply|sign|submit|confirm|establish|spawn|deploy|buy|transfer|payout|donate/i;

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 950 } });
const page = await ctx.newPage();

const labelsOf = () => page.evaluate(() => [...document.querySelectorAll('button')]
  .filter(b => b.offsetParent !== null && !b.disabled)
  .map(b => (b.getAttribute('aria-label') || b.textContent || '').trim().replace(/\s+/g, ' '))
  .filter(t => t && t.length < 60));

const settle = async (ms = 500) => {
  await page.waitForFunction(() => (document.querySelector('#root')?.innerText || '').trim().length > 40,
    { timeout: 20000 }).catch(() => {});
  await page.waitForTimeout(ms);
};

// ── SELF-TEST: prove the response detector fires before trusting any zero. ──
const probe = [];
const probeOn = r => { if (r.url().startsWith(BASE) && r.status() >= 400) probe.push(r.status()); };
page.on('response', probeOn);
await page.goto(BASE + '/', { waitUntil: 'domcontentloaded', timeout: 45000 });
await page.evaluate(b => fetch(b + '/api/v1/__definitely_not_a_route__').catch(() => {}), BASE);
await page.waitForTimeout(1200);
page.off('response', probeOn);
if (!probe.length) { console.log('SELF-TEST FAILED: response detector never fired. Aborting.'); await browser.close(); process.exit(2); }
console.log('self-test ok - detector fired on a deliberate bad path (' + probe[0] + ')\n');

// ── PASS 1 — enumerate only. ──
const seen = new Map();
for (const route of routes) {
  try {
    await page.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await settle(250);
    for (const l of new Set(await labelsOf())) seen.set(l, (seen.get(l) || 0) + 1);
  } catch { /* pass 2 records nav failures */ }
}
const CHROME = new Set([...seen].filter(([, n]) => n >= routes.length * 0.5).map(([l]) => l));
console.log('pass 1: ' + seen.size + ' distinct labels; ' + CHROME.size + ' are global chrome (excluded from per-route budget)\n');

// ── PASS 2 — click page-specific controls. ──
const report = [];
let chromeDone = false;
for (const route of routes) {
  const consoleErrors = [], netFails = [];
  const onC = m => { if (m.type() === 'error') consoleErrors.push(m.text().slice(0, 160)); };
  const onR = r => { const u = r.url(); if (u.startsWith(BASE) && r.status() >= 400) netFails.push(r.status() + ' ' + u.replace(BASE, '')); };
  page.on('console', onC); page.on('response', onR);
  try {
    await page.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await settle();
    let targets = [...new Set(await labelsOf())].filter(l => !CHROME.has(l));
    if (!chromeDone) { targets = [...targets, ...CHROME]; chromeDone = true; }
    targets = targets.slice(0, 16);

    const results = [];
    for (const label of targets) {
      if (UNSAFE.test(label)) { results.push({ label, outcome: 'skipped-unsafe' }); continue; }
      const before = await page.evaluate(() => (document.querySelector('#root')?.innerText || '').length);
      const eB = consoleErrors.length, nB = netFails.length;
      try {
        await page.evaluate(l => {
          const b = [...document.querySelectorAll('button')].find(x =>
            ((x.getAttribute('aria-label') || x.textContent || '').trim().replace(/\s+/g, ' ')) === l
            && x.offsetParent !== null && !x.disabled);
          if (b) b.click();
        }, label);
        await page.waitForTimeout(1100);
      } catch { results.push({ label, outcome: 'click-threw' }); continue; }
      const after = await page.evaluate(() => (document.querySelector('#root')?.innerText || '').length);
      const body = await page.evaluate(() => document.querySelector('#root')?.innerText || '');
      const boundary = /something went wrong|unexpected error occurred/i.test(body);
      const newNet = netFails.slice(nB);
      let outcome = 'changed';
      if (boundary) outcome = 'ERROR-BOUNDARY';
      else if (newNet.some(n => n.startsWith('5'))) outcome = 'SERVER-ERROR';
      else if (newNet.length) outcome = 'CLIENT-ERROR';
      else if (consoleErrors.length > eB) outcome = 'CONSOLE-ERROR';
      else if (after === before) outcome = 'no-visible-change';
      results.push({ label, outcome, net: newNet.slice(0, 3), err: consoleErrors.slice(eB, eB + 1) });
      if (boundary) { await page.goto(BASE + route, { waitUntil: 'domcontentloaded' }).catch(() => {}); await settle(400); }
    }
    report.push({ route, tested: targets.length, results });
    const bad = results.filter(r => ['ERROR-BOUNDARY', 'SERVER-ERROR', 'CLIENT-ERROR', 'CONSOLE-ERROR', 'click-threw'].includes(r.outcome)).length;
    const noop = results.filter(r => r.outcome === 'no-visible-change').length;
    console.log('  ' + route.padEnd(26) + String(targets.length).padStart(2) + ' page-btns  ' + (bad ? 'BAD:' + bad + '  ' : '') + (noop ? 'noop:' + noop : ''));
  } catch (e) {
    report.push({ route, error: String(e).slice(0, 120) });
    console.log('  ' + route.padEnd(26) + 'NAV FAILED');
  }
  page.off('console', onC); page.off('response', onR);
}
await browser.close();
writeFileSync('C:/tmp/button_sweep.json', JSON.stringify({ chrome: [...CHROME], report }, null, 1));
const allBad = report.flatMap(r => (r.results || []).filter(x => ['ERROR-BOUNDARY', 'SERVER-ERROR', 'CLIENT-ERROR', 'CONSOLE-ERROR', 'click-threw'].includes(x.outcome)).map(x => ({ route: r.route, ...x })));
console.log('\nroutes: ' + report.length + '   page-specific controls tested: ' + report.reduce((a, r) => a + (r.tested || 0), 0) + '   failing: ' + allBad.length);
for (const b of allBad.slice(0, 30)) console.log('  ! ' + b.route + '  "' + b.label + '"  ' + b.outcome + '  ' + (b.net || []).join(',') + ' ' + (b.err || []).join('').slice(0, 90));
