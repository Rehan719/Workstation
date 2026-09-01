/**
 * Re-test only the controls the sweep called "no-visible-change", with a detector that can SEE
 * selection state. The sweep compared #root innerText length, which cannot move when a chip or tab
 * changes only styling — so its 331 "no-visible-change" results conflate genuinely-inert controls
 * with working selectors. Signature here: innerText + concatenated button classNames +
 * aria-pressed/aria-selected/aria-current. Each control is tested from a FRESH page load, because in
 * the sweep clicks accumulated state and later controls were judged against an already-changed page.
 */
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';
const BASE = process.argv[2] || 'http://localhost:8010';
const d = JSON.parse(readFileSync('C:/tmp/button_sweep.json', 'utf-8'));
const targets = [];
for (const r of d.report) for (const x of (r.results || []))
  if (x.outcome === 'no-visible-change') targets.push([r.route, x.label]);
console.log('re-testing ' + targets.length + ' controls from fresh loads\n');

const b = await chromium.launch();
const p = await (await b.newContext({ viewport: { width: 1440, height: 950 } })).newPage();
const sig = () => p.evaluate(() => {
  const r = document.querySelector('#root');
  const bs = [...document.querySelectorAll('button')];
  return (r?.innerText || '').replace(/\d+/g, '#')                       // ignore live counters
    + '||' + bs.map(x => x.className).join('|')
    + '||' + bs.map(x => (x.getAttribute('aria-pressed') || '') + (x.getAttribute('aria-selected') || '') + (x.getAttribute('aria-current') || '')).join('|');
});
const inert = [];
let responded = 0, missing = 0;
for (const [route, label] of targets) {
  try {
    await p.goto(BASE + route, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await p.waitForFunction(() => (document.querySelector('#root')?.innerText || '').trim().length > 40, { timeout: 15000 }).catch(() => {});
    await p.waitForTimeout(450);
    const before = await sig();
    const found = await p.evaluate(l => {
      const x = [...document.querySelectorAll('button')].find(y => ((y.getAttribute('aria-label') || y.textContent || '').trim().replace(/\s+/g, ' ')) === l && y.offsetParent !== null && !y.disabled);
      if (x) { x.click(); return true; } return false;
    }, label);
    if (!found) { missing++; continue; }
    await p.waitForTimeout(900);
    const after = await sig();
    if (after === before) inert.push({ route, label }); else responded++;
  } catch { missing++; }
}
await b.close();
writeFileSync('C:/tmp/inert.json', JSON.stringify(inert, null, 1));
console.log('responded (state changed): ' + responded);
console.log('not found / nav issue:     ' + missing);
console.log('GENUINELY INERT:           ' + inert.length);
const byRoute = {};
for (const i of inert) (byRoute[i.route] ||= []).push(i.label);
for (const [rt, ls] of Object.entries(byRoute).sort((a, b) => b[1].length - a[1].length))
  console.log('  ' + String(ls.length).padStart(2) + '  ' + rt.padEnd(24) + ls.slice(0, 5).map(l => l.slice(0, 24)).join(', '));
