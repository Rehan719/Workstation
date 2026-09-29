/**
 * §P2.10(d) — THE DELIVERY METHOD, ON A SURFACE.
 *
 * The discipline that produced this delivery used to live outside the product. This page renders it as the
 * platform now holds it: every lesson with the DEFECT that produced it, and whether anything actually
 * enforces it.
 *
 * THE THING THIS PAGE MUST NOT DO, which is the item's own stated risk: present the method as a compliance
 * badge. So the headline figure is the SHARE THAT IS ENFORCED, read from the response rather than written
 * here — a figure in a comment ages into a false statement, and this one already had — and each unenforced
 * lesson shows the reason no tool covers it. A reader who leaves this page believing the platform checks its
 * own discipline would have been misled by it.
 *
 * W509 adds the DEFECT CLASSES: a lesson is a rule for whoever is working, a class is a shape a screen can
 * look for. Three of the six can be found mechanically and three cannot, and the section says which — a
 * taxonomy that showed only the findable ones would read as the whole taxonomy.
 */
import React, { useEffect, useState } from 'react';
import { Card } from '@workstation/ui';
import { BookOpen, ShieldCheck, ShieldAlert, Loader2, AlertCircle, Wrench, Search, RefreshCw, TrendingUp } from 'lucide-react';

interface Lesson {
  id: string;
  group: string;
  rule: string;
  defect: string;
  apply: string;
  enforced_by?: string | null;
  why_not_enforced?: string | null;
}

interface Mechanism {
  id: string;
  group: string;
  name: string;
  what: string;
  entry_points?: string[];
  known_limit?: string;
}

// W509 — every group the register holds needs a label here. A group with no entry falls back to its raw
// slug, which reads as a bug beside its Title-Case siblings; the guard asserts the register's `groups` list
// and the lessons' actual groups match, so a new group cannot be added without being reachable on the filter.
const GROUP_LABEL: Record<string, string> = {
  preparation: 'Preparation',
  planning: 'Planning',
  forecasting: 'Forecasting',
  measurement: 'Measurement',
  execution: 'Execution',
  verification: 'Verification',
  diagnosing: 'Diagnosing',
  correcting: 'Correcting',
  delivery: 'Delivery',
  learning: 'Learning',
  handover: 'Handover',
};

interface DefectClass {
  id: string;
  name: string;
  also_called?: string;
  shape: string;
  how_to_find: string;
  the_fix: string;
  not_this_class?: string;
  why_it_is_severe?: string;
  measured?: string;
}

export const DeliveryMethod: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);
  const [group, setGroup] = useState<string>('all');
  // the classes are a SEPARATE read: the method rendering must not disappear because this one failed, and a
  // failure here must not be shown as "there are no classes"
  const [classes, setClasses] = useState<any>(null);
  const [classErr, setClassErr] = useState<string | null>(null);
  // W509 — three independent reads. A failure in one must not blank the others, and must never render as
  // "there is nothing here": the method, the classes, the loop's state and the pace discipline are four
  // different facts and a missing one is said, not implied.
  const [loop, setLoop] = useState<any>(null);
  const [loopErr, setLoopErr] = useState<string | null>(null);
  const [pace, setPace] = useState<any>(null);
  const [paceErr, setPaceErr] = useState<string | null>(null);

  useEffect(() => {
    const get = (url: string, ok: (b: any) => void, bad: (m: string) => void) =>
      fetch(url)
        .then(async r => {
          const b = await r.json();
          if (!r.ok) throw new Error(typeof b.detail === 'string' ? b.detail : `HTTP ${r.status}`);
          return b;
        })
        .then(ok)
        .catch(e => bad(e?.message ?? String(e)));
    get('/api/v1/method/learning', setLoop, setLoopErr);
    get('/api/v1/method/forecast', setPace, setPaceErr);
  }, []);

  useEffect(() => {
    fetch('/api/v1/method/defect-classes')
      .then(async r => {
        const b = await r.json();
        if (!r.ok) throw new Error(typeof b.detail === 'string' ? b.detail : `HTTP ${r.status}`);
        return b;
      })
      .then(setClasses)
      .catch(e => setClassErr(e?.message ?? String(e)));
  }, []);

  useEffect(() => {
    fetch('/api/v1/method')
      .then(async r => {
        const b = await r.json();
        if (!r.ok) throw new Error(typeof b.detail === 'string' ? b.detail : `HTTP ${r.status}`);
        return b;
      })
      .then(setData)
      .catch(e => setErr(e?.message ?? String(e)));
  }, []);

  if (err) {
    return (
      <Card className="p-6">
        <p role="alert" data-testid="method-unavailable" className="text-[11px] font-bold text-vital flex items-start gap-2">
          <AlertCircle size={14} className="mt-0.5 shrink-0" />
          {/* the method could not be read — NOT "the platform has no method". Different statements. */}
          The delivery method could not be read, so nothing about it is shown: {err}. This is not a statement
          that the platform holds no method.
        </p>
      </Card>
    );
  }
  if (!data) {
    return <Card className="p-6"><Loader2 size={16} className="animate-spin text-slate-500" /></Card>;
  }

  const lessons: Lesson[] = data.lessons ?? [];
  const mechanisms: Mechanism[] = data.mechanisms ?? [];
  const enf = data.enforcement ?? {};
  const groups: string[] = data.groups ?? [];
  const shown = group === 'all' ? lessons : lessons.filter(l => l.group === group);

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-2">
          <BookOpen size={14} /> The delivery method · held by the arms-length agency
        </h3>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          Every rule here was produced by a defect, and each one names it — a rule with no defect behind it is
          an opinion. The method is amended only through Change Control: a confirmed defect becomes a{' '}
          <span className="text-white font-bold">candidate</span>, and the agency ratifies it.
        </p>

        {/* THE HEADLINE IS THE HONEST ONE: how little of this a tool can catch. */}
        <div className="flex flex-wrap gap-2 mt-4" data-testid="method-enforcement">
          <span className="text-[9px] font-black uppercase px-2 py-1 rounded bg-emerald-500/10 text-emerald-400">
            {enf.mechanically_enforced} of {enf.lessons_total} mechanically enforced
          </span>
          <span className="text-[9px] font-black uppercase px-2 py-1 rounded bg-amber-500/10 text-amber-400">
            {enf.judgement_only} judgement only
          </span>
        </div>
        <p className="text-[10px] text-amber-400 font-bold mt-2 leading-relaxed" data-testid="method-not-a-badge">
          {/* the item's own named risk, refused on the surface that would otherwise carry it */}
          This is not a compliance badge. Most of the method is judgement a change record cannot expose, so a
          method check answers NOT ASSESSABLE for most requirements — and each lesson below that nothing
          enforces says why no tool covers it.
        </p>
        {enf.basis && <p className="text-[10px] text-slate-500 mt-2 leading-relaxed">{enf.basis}</p>}
      </Card>

      <div className="flex items-center gap-2 flex-wrap">
        {['all', ...groups].map(g => (
          <button
            key={g}
            type="button"
            onClick={() => setGroup(g)}
            className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
              group === g ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-white'
            }`}
          >
            {g === 'all' ? `All ${lessons.length}` : `${GROUP_LABEL[g] ?? g} ${lessons.filter(l => l.group === g).length}`}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {shown.map(l => {
          const enforced = Boolean((l.enforced_by ?? '').trim());
          return (
            <Card key={l.id} className="p-5" data-testid="method-lesson">
              <div className="flex items-start justify-between gap-3 flex-wrap">
                <div className="flex items-center gap-2">
                  <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-500">
                    {l.id}
                  </span>
                  <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-400">
                    {GROUP_LABEL[l.group] ?? l.group}
                  </span>
                </div>
                {enforced ? (
                  <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 flex items-center gap-1">
                    <ShieldCheck size={11} /> enforced
                  </span>
                ) : (
                  <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 flex items-center gap-1">
                    <ShieldAlert size={11} /> judgement only
                  </span>
                )}
              </div>

              <p className="text-[12px] font-bold text-white mt-3 leading-relaxed">{l.rule}</p>

              {/* THE DEFECT, always shown. It is the evidence for the rule, and a reader must be able to
                  judge the rule by it rather than by how the rule is phrased. */}
              <p className="text-[10px] text-slate-500 mt-2 leading-relaxed" data-testid="method-defect">
                <span className="font-black uppercase tracking-widest text-slate-600">The defect that produced it · </span>
                {l.defect}
              </p>
              <p className="text-[10px] text-slate-400 mt-2 leading-relaxed">
                <span className="font-black uppercase tracking-widest text-slate-600">How to apply it · </span>
                {l.apply}
              </p>

              <p className="text-[10px] mt-2 leading-relaxed">
                {enforced ? (
                  <span className="text-emerald-400 flex items-start gap-1">
                    <Wrench size={11} className="mt-0.5 shrink-0" />
                    <span><span className="font-black uppercase tracking-widest">Caught by · </span>{l.enforced_by}</span>
                  </span>
                ) : (
                  <span className="text-amber-400/90">
                    <span className="font-black uppercase tracking-widest">Nothing enforces this · </span>
                    {l.why_not_enforced || 'no reason is recorded, which is itself a gap'}
                  </span>
                )}
              </p>
            </Card>
          );
        })}
      </div>

      {/* W509 — WHICH OF THESE RULES IS FAILING. A register that cannot show that is a document. */}
      <Card className="p-6" data-testid="method-learning">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 flex items-center gap-2">
          <RefreshCw size={14} /> The learning loop · which of these rules is failing
        </h3>
        {loopErr ? (
          <p role="alert" data-testid="learning-unavailable" className="text-[11px] font-bold text-vital">
            The loop's state could not be read, so no breach is shown: {loopErr}. This is not a statement that
            no rule has been breached.
          </p>
        ) : !loop ? (
          <Loader2 size={14} className="animate-spin text-slate-500" />
        ) : (
          <>
            <p className="text-[10px] text-slate-400 leading-relaxed">{loop.loop}</p>
            {(loop.breached ?? []).length === 0 ? (
              <p className="text-[10px] text-slate-400 mt-3 leading-relaxed" data-testid="learning-none-recorded">
                {/* NOT "no rule has been broken" — a different statement, and the one nothing can support */}
                No breach has been <span className="text-white font-bold">recorded</span> against any rule.
                Nothing observes a breach, so this is not a statement that none has happened.
              </p>
            ) : (
              <div className="space-y-2 mt-3">
                {(loop.breached ?? []).map((b: any) => (
                  <div key={b.lesson_id} data-testid="learning-breach"
                       className="flex items-start gap-2 text-[10px] leading-relaxed">
                    <span className={`font-black uppercase px-2 py-0.5 rounded shrink-0 ${
                      b.at_or_over_threshold ? 'bg-vital/15 text-vital' : 'bg-amber-500/10 text-amber-400'}`}>
                      {b.breaches_recorded}×
                    </span>
                    <span className="min-w-0">
                      <span className="font-mono text-slate-500">{b.lesson_id}</span> · {b.rule}
                      {b.at_or_over_threshold && (
                        <span className="block text-vital mt-0.5">
                          At the threshold and nothing enforces it — a change has been raised asking for a
                          tool, because a rule broken after being written is a mechanism failure.
                        </span>
                      )}
                    </span>
                  </div>
                ))}
              </div>
            )}
            <p className="text-[10px] text-amber-400/90 mt-3 leading-relaxed" data-testid="learning-limit">
              {loop.what_this_cannot_see}
            </p>
          </>
        )}
      </Card>

      {/* W509 — what the PACE figure cannot know. The projection itself lives on the plan surface: two
          surfaces showing two rates would be two records disagreeing about one fact. */}
      <Card className="p-6" data-testid="method-pace-discipline">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 flex items-center gap-2">
          <TrendingUp size={14} /> Forecasting · what the pace figure cannot know
        </h3>
        {paceErr ? (
          <p role="alert" data-testid="pace-unavailable" className="text-[11px] font-bold text-vital">
            The forecasting discipline could not be read: {paceErr}. No rate is substituted.
          </p>
        ) : !pace ? (
          <Loader2 size={14} className="animate-spin text-slate-500" />
        ) : (
          <>
            <p className="text-[10px] text-slate-400 leading-relaxed">
              The projection is computed by{' '}
              <span className="font-mono text-slate-500">{pace.projection_computed_by}</span> and served at{' '}
              <span className="font-mono text-slate-500">{pace.also_served_at}</span>. {pace.what_this_adds}.
            </p>
            {pace.which_rate_measures_completion && (
              <p className="text-[10px] text-white mt-3 leading-relaxed" data-testid="pace-lever">
                <span className="font-black uppercase tracking-widest text-slate-600">The lever · </span>
                {pace.which_rate_measures_completion.rows_per_round} rows per round and{' '}
                {pace.which_rate_measures_completion.items_per_round} items per round — and only{' '}
                <span className="text-emerald-400 font-bold">{pace.which_rate_measures_completion.the_lever}</span>{' '}
                measures completion. {pace.which_rate_measures_completion.why}
              </p>
            )}
            {pace.the_count_overstates?.why_it_is_an_upper_bound && (
              <p className="text-[10px] text-amber-400/90 mt-2 leading-relaxed" data-testid="pace-overstates">
                <span className="font-black uppercase tracking-widest">The count over-states · </span>
                {pace.the_count_overstates.why_it_is_an_upper_bound}
              </p>
            )}
            {pace.cost_of_a_round && (
              <p className="text-[10px] text-slate-400 mt-2 leading-relaxed" data-testid="pace-cost">
                <span className="font-black uppercase tracking-widest text-slate-600">
                  What a round costs · dominated by {pace.cost_of_a_round.dominated_by} ·{' '}
                </span>
                {(pace.cost_of_a_round.components ?? []).join(' · ')}. {pace.cost_of_a_round.wall_clock_is_not_work}
              </p>
            )}
            {Object.keys(pace.blocked_by_ruling?.items ?? {}).length > 0 && (
              <p className="text-[10px] text-sky-400/90 mt-2 leading-relaxed" data-testid="pace-blocked">
                <span className="font-black uppercase tracking-widest">Blocked by ruling · </span>
                {Object.entries(pace.blocked_by_ruling.items).map(([k, v]) => `${k} behind ${v}`).join(' · ')}.
                {' '}{pace.blocked_by_ruling.consequence}
              </p>
            )}
            <p className="text-[10px] text-slate-500 mt-2 leading-relaxed" data-testid="pace-limit">{pace.limits}</p>
          </>
        )}
      </Card>

      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 flex items-center gap-2">
          <Search size={14} /> The defect classes · shapes, not rules
        </h3>
        {classErr ? (
          <p role="alert" data-testid="classes-unavailable" className="text-[11px] font-bold text-vital">
            {/* not "there are no classes" — a different statement */}
            The defect classes could not be read, so none are shown: {classErr}. This is not a statement that
            the method holds no classes.
          </p>
        ) : !classes ? (
          <Loader2 size={14} className="animate-spin text-slate-500" />
        ) : (
          <>
            <p className="text-[10px] text-slate-400 leading-relaxed">{classes.about}</p>
            <p className="text-[10px] text-amber-400 font-bold mt-2 leading-relaxed" data-testid="classes-basis">
              {/* the honest headline of the section, exactly as the enforcement share is for the lessons */}
              {classes.basis}
            </p>
            <div className="space-y-4 mt-4">
              {(classes.defect_classes ?? []).map((c: DefectClass) => (
                <div key={c.id} data-testid="defect-class">
                  <p className="text-[11px] font-bold text-white">
                    <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-slate-900 text-slate-500 mr-2">
                      {c.id}
                    </span>
                    {c.name}
                    {c.also_called && (
                      <span className="text-[9px] text-slate-600 uppercase tracking-widest ml-2">· {c.also_called}</span>
                    )}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">{c.shape}</p>
                  <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                    <span className="font-black uppercase tracking-widest text-slate-600">How it is found · </span>
                    {c.how_to_find}
                  </p>
                  {c.measured && (
                    <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">
                      <span className="font-black uppercase tracking-widest text-slate-600">Measured · </span>
                      {c.measured}
                    </p>
                  )}
                  <p className="text-[10px] text-emerald-400/90 mt-1 leading-relaxed">
                    <span className="font-black uppercase tracking-widest">The fix · </span>{c.the_fix}
                  </p>
                  {/* what is NOT in the class. Without it a screen re-proposes settled cases every sweep. */}
                  {c.not_this_class && (
                    <p className="text-[10px] text-sky-400/90 mt-1 leading-relaxed" data-testid="class-exclusions">
                      <span className="font-black uppercase tracking-widest">Not this class · </span>
                      {c.not_this_class}
                    </p>
                  )}
                </div>
              ))}
            </div>
            {(classes.not_screenable ?? []).length > 0 && (
              <div className="mt-5 pt-4 border-t border-slate-800" data-testid="classes-not-screenable">
                <p className="text-[9px] font-black uppercase tracking-widest text-amber-400 mb-2">
                  No screen can find these — they are not reported clear
                </p>
                {(classes.not_screenable ?? []).map((n: any) => (
                  <p key={n.defect_class} className="text-[10px] text-slate-400 leading-relaxed mt-1">
                    <span className="font-mono text-slate-500">{n.defect_class}</span> · {n.why}
                  </p>
                ))}
              </div>
            )}
          </>
        )}
      </Card>

      <Card className="p-6">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-3">
          The mechanisms · and what each one cannot do
        </h3>
        <div className="space-y-4">
          {mechanisms
            .filter(m => group === 'all' || m.group === group)
            .map(m => (
              <div key={m.id} data-testid="method-mechanism">
                <p className="text-[11px] font-bold text-white">
                  {m.name} <span className="text-[9px] text-slate-600 uppercase tracking-widest">· {GROUP_LABEL[m.group] ?? m.group}</span>
                </p>
                <p className="text-[10px] text-slate-400 mt-1 leading-relaxed">{m.what}</p>
                {(m.entry_points ?? []).length > 0 && (
                  <p className="text-[9px] text-slate-600 mt-1 font-mono">{(m.entry_points ?? []).join('  ·  ')}</p>
                )}
                {/* a mechanism with no stated limit is one nobody has tested — so the limit is rendered,
                    not hidden behind a link */}
                <p className="text-[10px] text-amber-400/90 mt-1 leading-relaxed" data-testid="method-mechanism-limit">
                  <span className="font-black uppercase tracking-widest">Known limit · </span>{m.known_limit}
                </p>
              </div>
            ))}
        </div>
      </Card>
    </div>
  );
};
