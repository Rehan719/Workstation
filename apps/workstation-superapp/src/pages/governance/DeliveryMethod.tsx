/**
 * §P2.10(d) — THE DELIVERY METHOD, ON A SURFACE.
 *
 * The discipline that produced this delivery used to live outside the product. This page renders it as the
 * platform now holds it: every lesson with the DEFECT that produced it, and whether anything actually
 * enforces it.
 *
 * THE THING THIS PAGE MUST NOT DO, which is the item's own stated risk: present the method as a compliance
 * badge. So the headline figure is the SHARE THAT IS ENFORCED — 14 of 36 at the time of writing — and each
 * unenforced lesson shows the reason no tool covers it. A reader who leaves this page believing the platform
 * checks its own discipline would have been misled by it.
 */
import React, { useEffect, useState } from 'react';
import { Card } from '@workstation/ui';
import { BookOpen, ShieldCheck, ShieldAlert, Loader2, AlertCircle, Wrench } from 'lucide-react';

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

const GROUP_LABEL: Record<string, string> = {
  planning: 'Planning',
  measurement: 'Measurement',
  execution: 'Execution',
  verification: 'Verification',
  delivery: 'Delivery',
};

export const DeliveryMethod: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);
  const [group, setGroup] = useState<string>('all');

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
