// W479 (P1.18 FU-121/FU-153) — the intelligence engines on a FRESH backend (AI_DISABLE_LOCAL=1, so every call is the
// structured floor): the streams by fetch, the Authorship and Nexus pages in a real browser against the built bundle.
//   node scripts/_w479_probe.mjs http://127.0.0.1:8088
import { chromium } from 'playwright';
const BASE = process.argv[2] || 'http://127.0.0.1:8088';
const checks = [];
const check = (name, ok) => { checks.push(ok); console.log(`RESULT ${name}:`, ok); };
const stream = async (path, body) => {
  const r = await fetch(`${BASE}${path}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
  const t = await r.text();
  return t.split('\n').filter(l => l.startsWith('data: ')).map(l => JSON.parse(l.slice(6)));
};

const dismissTour = async (p) => {   // the first-visit onboarding tour's overlay intercepts pointer events
  for (let i = 0; i < 3; i++) {
    const skip = p.locator('[data-test-id="button-skip"], [aria-label="Skip"], button:has-text("Skip")').first();
    if (await skip.isVisible().catch(() => false)) { await skip.click().catch(() => {}); break; }
    await p.keyboard.press('Escape');
    await p.waitForTimeout(400);
    if (!(await p.locator('.react-joyride__overlay').isVisible().catch(() => false))) break;
  }
  await p.waitForFunction(() => !document.querySelector('.react-joyride__overlay'), null, { timeout: 10000 }).catch(() => {});
};

// ── API halves ──
const topic = 'Urban tree canopy and summer heat admissions';
const ap = await stream('/api/v1/intelligence/authorship', { topic, rigor: 'rigorous' });
const apr = ap.filter(e => typeof e.data?.stage_num === 'number');
check('S5.6 authorship with rigor: 9 stage results numbered 1..9; config is not one', apr.map(e => e.data.stage_num).join() === '1,2,3,4,5,6,7,8,9' && ap.some(e => e.stage === 'config'));
check('S5.4 every stage says the floor served it', apr.every(e => e.data.served_by === 'native' && e.data.failed === false));
check('S5.4 the user topic reaches every floor stage', apr.every(e => e.content.toLowerCase().includes(topic.toLowerCase())));
check('S5.4 the completion line names the floor, not "complete"', /structured floor/.test(ap.at(-1).content) && !/pipeline complete/i.test(ap.at(-1).content));
const bdp = await stream('/api/v1/intelligence/bdp', { challenge: 'A hive weight monitor for small beekeepers' });
check('S6.3 no "primed" event when nothing was primed', !bdp.some(e => e.stage === 'cognitive_prime'));
check('S6.2 BDP: 8 stage results, each with provenance', bdp.filter(e => typeof e.data?.stage_num === 'number' && e.data.served_by).length === 8);
const nx = await stream('/api/v1/intelligence/nexus', { challenge: 'Design a research study on varroa mite resistance', domain: 'science' });
const sel = nx.find(e => e.stage === 'engine_selected');
check('S4.4 Auto on the floor: "Not selected: defaulted to BDP" with the reason', /^Not selected: defaulted to BDP, because no model was available/.test(sel?.content || '') && sel.data.decision.decided === false);
check('S4.4 no "Autonomously selecting"', !nx.some(e => /Autonomously selecting/.test(e.content)));
const fin = nx.find(e => e.stage === 'nexus_complete')?.data || {};
check('S4.5 the Nexus counts what ran (12 calls, all floor; 6 lenses in one prompt)', fin.run?.calls === 12 && fin.run?.floor_calls === 12 && fin.cognitive_lenses === 6 && !('cognitive_engines' in fin));

// ── UI halves (served bundle, real browser) ──
const b = await chromium.launch();
const page = await (await b.newContext({ viewport: { width: 1440, height: 1100 } })).newPage();
await page.goto(`${BASE}/authorship`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1500);
await dismissTour(page);
const hdr = await page.textContent('body');
check('S5.5 the Authorship header no longer claims nine engines + MJM', !/Nine Cognitive Engines/.test(hdr) && /No cognitive lenses or MJM run here/.test(hdr));
await page.fill('textarea', topic);
await page.getByRole('button', { name: 'rigorous' }).first().click();
await page.getByRole('button', { name: /Run APIE/ }).click();
await page.waitForFunction(() => /Authorship Pipeline Finished/i.test(document.body.innerText), null, { timeout: 180000 }).catch(() => {});
const body = await page.evaluate(() => document.body.innerText);
check('S5.6 the page reads "9 of 9 Stages", never "10 of 9"', /9 of 9 Stages/i.test(body) && !/10 of 9/.test(body));
check('S5.4 each card carries the floor badge, not a green tick', (body.match(/structured floor — not model analysis/gi) || []).length >= 9);
check('S5.4 the finished banner states what ran', /9 of 9 stages ran\. 9 composed by the structured floor/.test(body));
await page.screenshot({ path: 'C:/tmp/w479p/authorship.png', fullPage: false });
await page.goto(`${BASE}/nexus`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1500);
await dismissTour(page);
const nh = await page.evaluate(() => document.body.innerText);
check('S4.4 the Auto tile no longer says AI selects', !/AI selects the optimal engine/.test(nh));
await page.fill('textarea', 'Design a research study on varroa mite resistance');
await page.getByRole('button', { name: /Activate Synthesis Nexus/ }).click();
await page.waitForFunction(() => /layers ran ·/i.test(document.body.innerText), null, { timeout: 240000 }).catch(() => {});
const nb = await page.evaluate(() => document.body.innerText);
check('S4.4 the banner says the engine was not selected, and why', /Not selected: defaulted to\s*BDP/i.test(nb) && /no model was available/i.test(nb));
check('S4.5 the layer cards say one prompt, counts from the run', /one prompt headed by 6 lenses/i.test(nb) && /4 of 4 layers ran/i.test(nb) && !/6 cognitive engines/i.test(nb));
await page.screenshot({ path: 'C:/tmp/w479p/nexus.png', fullPage: false });
await b.close();
const passed = checks.filter(Boolean).length;
console.log(`PROBE ${passed}/${checks.length}`);
process.exit(passed === checks.length ? 0 : 1);
