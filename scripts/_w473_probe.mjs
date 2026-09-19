// W473 (P1.16 canon and suite hygiene) — the Command Center prints nothing it does not measure, in a real browser
// against the built bundle on a FRESH backend (AI_DISABLE_LOCAL=1). No seed.
//   node scripts/_w473_probe.mjs http://127.0.0.1:8082
//   · the Command Center's three former literals ("in WORK mode for 4 hours", "3D Holographic Engine — Loading...",
//     "Real-time stream initializing via libp2p...") are gone from the served bundle, and the honest lines are in it;
//   · the mandate docs are served nowhere (a docs check is the suite's); this probe is the UI half only.
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8082';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };

const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1100 } });
const page = await ctx.newPage();
const bundleTexts = [];
page.on('response', async (res) => {
  const url = res.url();
  if (/\/assets\/.*\.js$/.test(url)) { try { bundleTexts.push(await res.text()); } catch { /* ignore */ } }
});
await page.goto(`${BASE}/`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1500);
const all = bundleTexts.join('\n');
console.log('  bundle chunks read:', bundleTexts.length, '| total chars', all.length);
const gone = ['in WORK mode for 4 hours', 'Holographic Engine — Loading', 'initializing via libp2p'];
const there = ['Nothing measures your session length', 'not built; nothing is loading', 'No real-time stream is connected'];
console.log('  gone:', gone.map(s => !all.includes(s)).join(','), '| there:', there.map(s => all.includes(s)).join(','));
check('the served bundle carries none of the three unmeasured Command Center literals',
  bundleTexts.length > 0 && gone.every(s => !all.includes(s)));
check('the served bundle carries the honest lines in their place', there.every(s => all.includes(s)));

await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
