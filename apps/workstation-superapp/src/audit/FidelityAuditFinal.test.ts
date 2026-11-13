// W977 (P5.22) — the final audit's workflow script, driven with planted agents.
//
// The final audit (scripts/workflows/fidelity_audit_final.js) runs one assessor and one refuter per census slice through
// the Workflow tool. Nothing in CI can run its agents, so this runs the script itself with planted ones, the way the
// Workflow runtime runs it (its body in an async context, with agent, pipeline and log), and reads what it does: what it
// refuses before any agent runs, what each assessor is told, and the record it returns, which is the one
// scripts/audit_completeness.py joins and judges. It renders no page; it lives with the rendered tests because this is
// the only JavaScript runner the repository's CI declares (vite.config.js says so where the tests are collected).
import { describe, expect, it } from 'vitest';

import source from '../../../../scripts/workflows/fidelity_audit_final.js?raw';

type Call = { prompt: string; label: string; phase: string };
type Planted = (call: Call) => unknown;

const HEAD = 'a'.repeat(40);
const SLICES = {
  slices: [
    { id: 'w977-one', holds: 'a slice of two routes', routes: ['GET /api/v1/w977/one', 'POST /api/v1/w977/one'], pages: [] },
    { id: 'w977-two', holds: 'a slice of one page', routes: [], pages: ['/w977 (W977Page)'] },
    { id: 'w977-three', holds: 'a slice of one route', routes: ['GET /api/v1/w977/three'], pages: [] },
  ],
};
const ARGS = { head: HEAD, date: '2026-11-13', configuration: 'floor', slices: SLICES, base: 'http://127.0.0.1:8099' };

const FOUND = {
  findings: [{ section: 'A planted finding', verdict: 'PARTIAL', tier: 2, why_this_tier: 'planted', vision_claim: 'the claim',
               observed: 'what was seen', evidence: 'where' }],
  region_summary: 'planted', hit_the_cap: false, unlisted_findings: 0, residue: [],
  surfaces_exercised: { routes: ['GET /api/v1/w977/one'], files: [] },
};
const CLEAN = { ...FOUND, findings: [] };
const VERDICTS = {
  verdicts: [{ index: 0, refuted: false, reproduced: true, corrected_verdict: 'PARTIAL', corrected_tier: 2,
               defect_class: 'other', reason: 'planted' }],
  residue: [],
};

// the Workflow runtime, as its reference describes it: the script's body runs in an async context; pipeline runs each
// item through every stage, each stage given (previous result, original item, index), and a stage that throws drops
// that item to null and skips its remaining stages
async function run(args: unknown, planted: Planted) {
  const calls: Call[] = [];
  const logs: string[] = [];
  const agent = async (prompt: string, opts: { label: string; phase: string }) => {
    const call = { prompt, label: opts.label, phase: opts.phase };
    calls.push(call);
    return planted(call);
  };
  const pipeline = (items: unknown[], ...stages: ((prev: unknown, item: unknown, i: number) => unknown)[]) =>
    Promise.all(items.map(async (item, i) => {
      try {
        let v: unknown = item;
        for (const stage of stages) v = await stage(v, item, i);
        return v;
      } catch {
        return null;
      }
    }));
  const body = source.replace(/^export const meta = /m, 'const meta = ');
  const script = new Function('args', 'agent', 'pipeline', 'parallel', 'phase', 'log',
    `return (async () => {\n${body}\n})();`);
  const result = await script(args, agent, pipeline, undefined, () => undefined, (m: string) => logs.push(m));
  return { result, calls, logs };
}

const plantedRun: Planted = c => (c.label.startsWith('assess:') ? (c.label === 'assess:w977-three' ? CLEAN : FOUND) : VERDICTS);

describe('the final audit\'s workflow, driven with planted agents', () => {
  it('declares its two phases and its name', () => {
    expect(source).toContain("name: 'fidelity-audit-final'");
    expect(source).toContain("phases: [{ title: 'Assess' }, { title: 'Refute' }]");
  });

  it('refuses, before any agent runs, a run that cannot name its commit, date, configuration or slices', async () => {
    const bad: [Record<string, unknown>, string][] = [
      [{ ...ARGS, head: undefined }, 'needs args.head, the full commit id'],
      [{ ...ARGS, head: 'abc1234' }, 'needs args.head, the full commit id'],
      [{ ...ARGS, date: undefined }, 'needs args.date (YYYY-MM-DD)'],
      [{ ...ARGS, configuration: 'cloud' }, 'needs args.configuration, one of floor or local_model'],
      [{ ...ARGS, slices: undefined }, 'needs args.slices'],
      [{ ...ARGS, slices: { slices: [] } }, 'needs args.slices'],
      [{ ...ARGS, slices: { slices: [{ id: 'empty', routes: [], pages: [] }] } }, 'a slice with no surface'],
    ];
    for (const [args, said] of bad) {
      let calls = 0;
      await expect(run(args, () => { calls += 1; return FOUND; })).rejects.toThrow(said);
      expect(calls).toBe(0);
    }
  });

  it('gives each slice one assessor, told every surface it holds, the configuration, and that there is no cap', async () => {
    const { calls } = await run(ARGS, plantedRun);
    const assess = calls.filter(c => c.phase === 'Assess');
    expect(assess.map(c => c.label)).toEqual(['assess:w977-one', 'assess:w977-two', 'assess:w977-three']);
    const one = assess[0].prompt;
    for (const s of [...SLICES.slices[0].routes, `HEAD ${HEAD}`, '2026-11-13', 'CONFIGURATION: floor',
                     'AI_DISABLE_LOCAL=1', 'THERE IS NO CAP', 'http://127.0.0.1:8099']) expect(one).toContain(s);
    expect(assess[1].prompt).toContain('/w977 (W977Page)');
    expect(one).not.toMatch(/Up to \d+ findings|THE CAP IS/);
    const local = await run({ ...ARGS, configuration: 'local_model' }, plantedRun);
    expect(local.calls[0].prompt).toContain('CONFIGURATION: local_model');
    expect(local.calls[0].prompt).toContain('the local model serves model calls');
    expect(local.calls[0].prompt).not.toContain('AI_DISABLE_LOCAL=1');
  });

  it('refutes each slice that found something, and returns the record the completeness check reads', async () => {
    const { result, calls, logs } = await run(ARGS, plantedRun);
    const refute = calls.filter(c => c.phase === 'Refute');
    expect(refute.map(c => c.label)).toEqual(['refute:w977-one', 'refute:w977-two']);
    expect(refute[0].prompt).toContain('[0] A planted finding — PARTIAL · tier 2');
    expect(Object.keys(result).sort()).toEqual(['configuration', 'date', 'measured_commit', 'slices']);
    expect(result).toMatchObject({ measured_commit: HEAD, date: '2026-11-13', configuration: 'floor' });
    expect(result.slices.map((s: { region: string }) => s.region)).toEqual(['w977-one', 'w977-two', 'w977-three']);
    for (const s of result.slices) {
      expect(s).toMatchObject({ configuration: 'floor', measured_commit: HEAD, status: 'ok', hit_the_cap: false,
                                unlisted_findings: 0, surfaces_exercised: FOUND.surfaces_exercised });
    }
    expect(result.slices[0].verdicts).toEqual(VERDICTS.verdicts);
    expect(result.slices[2]).toMatchObject({ findings: [], verdicts: [] });
    expect(logs).toEqual(['all 3 slice(s) returned, in the floor configuration; completeness is decided by scripts/audit_completeness.py']);
  });

  it('a slice whose assessor or refuter returned nothing, or whose stage threw, is failed with the reason and never left out', async () => {
    const { result, logs } = await run(ARGS, c => {
      if (c.label === 'assess:w977-one') return null;
      if (c.label === 'assess:w977-three') throw new Error('planted: the agent died');
      if (c.label === 'refute:w977-two') return null;
      return FOUND;
    });
    expect(result.slices.map((s: { region: string; status: string }) => [s.region, s.status])).toEqual(
      [['w977-one', 'failed'], ['w977-two', 'failed'], ['w977-three', 'failed']]);
    expect(result.slices[0].error).toBe('the assessor returned nothing, so nothing in this slice was assessed');
    expect(result.slices[1].error).toBe('the refuter returned nothing, so no finding was refuted or upheld');
    expect(result.slices[1].findings).toEqual(FOUND.findings);
    expect(result.slices[2].error).toBe('the slice was dropped before it finished: a stage threw');
    for (const s of result.slices) expect(s).toMatchObject({ configuration: 'floor', measured_commit: HEAD, verdicts: [] });
    expect(logs).toEqual(['3 of 3 slice(s) did not complete (w977-one, w977-two, w977-three); the audit is not complete until each is run again']);
  });
});
