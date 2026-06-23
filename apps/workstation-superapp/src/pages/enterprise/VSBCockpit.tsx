import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Button, Badge } from '@workstation/ui';
import { Building2, Crown, Users, Target, ShieldCheck, Workflow, Loader2, Play, Boxes, ScrollText } from 'lucide-react';

// The VSB Enterprise Cockpit — interact with a generated living VSB IDBO Enterprise: its
// organisational structure, the Chief's digital twin + Board, the living business plan
// (vision / strategy / aims / objectives / roadmap), the living management systems (BMS/QMS/DCS/EMS),
// and a one-click end-to-end transformation run (Chief → Build-to-Order + products/services catalogue).
// All data is live from the in-house backend; nothing is fabricated.

interface VSBRow { vsb_id: string; name?: string; domain?: string; has_board?: boolean; entity_type?: string }
type Dict = Record<string, any>;

const TABS = [
  ['org', 'Organisation', Building2],
  ['chief', 'Chief & Board', Crown],
  ['plan', 'Business Plan', Target],
  ['systems', 'Living Systems', ShieldCheck],
  ['transform', 'Transformation', Workflow],
] as const;

export const VSBCockpit: React.FC = () => {
  const [vsbs, setVsbs] = useState<VSBRow[]>([]);
  const [selected, setSelected] = useState<string>('');
  const [detail, setDetail] = useState<Dict | null>(null);
  const [plan, setPlan] = useState<Dict | null>(null);
  const [standards, setStandards] = useState<Dict[]>([]);
  const [tab, setTab] = useState<string>('org');
  const [loading, setLoading] = useState(false);
  const [tx, setTx] = useState<Dict | null>(null);
  const [txRunning, setTxRunning] = useState(false);

  useEffect(() => {
    axios.get('/api/v1/vsb').then(r => {
      const ents: VSBRow[] = r.data.entities || [];
      setVsbs(ents);
      const first = (ents.find(e => e.has_board) || ents[0]);
      if (first) setSelected(first.vsb_id);
    }).catch(() => {});
    axios.get('/api/v1/mgmt/standards').then(r => setStandards(r.data.standards || [])).catch(() => {});
  }, []);

  useEffect(() => {
    if (!selected) return;
    setLoading(true); setTx(null);
    Promise.all([
      axios.get(`/api/v1/vsb/${selected}`).then(r => r.data).catch(() => null),
      axios.get('/api/v1/business-plan', { params: { scope: selected } }).then(r => r.data).catch(() => null),
    ]).then(([d, p]) => { setDetail(d); setPlan(p); setLoading(false); });
  }, [selected]);

  const runTransformation = async () => {
    if (!selected) return;
    setTxRunning(true); setTx(null);
    try {
      const objective = plan?.mission || detail?.challenge || `Advance ${detail?.name || 'the venture'}`;
      const r = await axios.post('/api/v1/transformation/orchestrate',
        { objective, scope: selected, owner_id: detail?.owner_id || 'Owner', deep: false });
      setTx(r.data);
    } catch { /* keep */ }
    setTxRunning(false);
  };

  const board = detail?.board || {};
  const chief = board.chief || {};
  const directors: Dict[] = board.directors || [];
  const swarm = detail?.native_swarm || {};

  return (
    <div className="space-y-8 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Living VSB Enterprise</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">VSB Cockpit</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Interact with a generated living VSB IDBO Enterprise — its organisational structure, the Chief's
          digital twin &amp; Board, the living business plan, the management systems (BMS · QMS · DCS · EMS),
          and an end-to-end transformation run. All live from Workstation's <span className="text-highlight">own</span> in-house systems.
        </p>
      </header>

      {/* VSB selector */}
      <Card className="p-5 flex items-center gap-4 flex-wrap">
        <Building2 size={18} className="text-highlight" />
        <select aria-label="Select VSB" value={selected} onChange={e => setSelected(e.target.value)}
          className="flex-1 min-w-[240px] bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white">
          {vsbs.length === 0 && <option value="">No established VSBs yet — spawn one in the VSB Spawn Studio</option>}
          {vsbs.map(v => <option key={v.vsb_id} value={v.vsb_id}>{v.name || v.vsb_id}{v.domain ? ` · ${v.domain}` : ''}{v.has_board ? ' ✓' : ''}</option>)}
        </select>
        {loading && <Loader2 size={16} className="animate-spin text-highlight" />}
      </Card>

      {detail && (
        <>
          <div className="flex gap-2 flex-wrap p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
            {TABS.map(([id, label, Icon]) => (
              <button key={id} type="button" onClick={() => setTab(id)}
                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center gap-2 ${tab === id ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>
                <Icon size={13} /> {label}
              </button>
            ))}
          </div>

          {/* Organisation */}
          {tab === 'org' && (
            <div className="space-y-4">
              <Card className="p-6 space-y-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h3 className="text-lg font-black text-white">{detail.name}</h3>
                  <div className="flex gap-2">
                    {detail.domain && <Badge color="highlight">{detail.domain}</Badge>}
                    {detail.status && <Badge color="emerald-500">{detail.status}</Badge>}
                    {detail.stage && <Badge color="aura">{detail.stage}</Badge>}
                  </div>
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed">{detail.challenge}</p>
                <p className="text-[9px] font-mono text-slate-600">{detail.vsb_id} · realm: {detail.realm} · owner: {detail.owner_id}</p>
              </Card>
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2"><Workflow size={14} /> Organisational hierarchy (apex → operational delivery)</h4>
                <div className="flex flex-wrap items-center gap-2 text-[10px] font-black uppercase tracking-wider">
                  {['Chief of Board', 'Board of Directors', 'AI CEO', 'C-Suite', 'Centres of Excellence', 'Business Transformation Office', 'Build-to-Order'].map((t, i, a) => (
                    <React.Fragment key={t}>
                      <span className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">{t}</span>
                      {i < a.length - 1 && <span className="text-highlight">→</span>}
                    </React.Fragment>
                  ))}
                </div>
                {swarm.org && (
                  <p className="text-[10px] text-slate-500 mt-4">Native delivery swarm: <span className="text-aura font-bold">{swarm.name || swarm.cascade_id}</span> · {(swarm.stages || []).length} stages · posture {swarm.posture || 'in-house'}</p>
                )}
              </Card>
            </div>
          )}

          {/* Chief & Board */}
          {tab === 'chief' && (
            <div className="space-y-4">
              <Card className="p-6 space-y-2 border-aura/30">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-aura flex items-center gap-2"><Crown size={14} /> Chief of the Board (Owner's digital twin)</h4>
                <p className="text-white font-black">{chief.title || chief.name || `Chief — Digital Twin of ${board.owner || detail.owner_id}`}</p>
                {chief.role && <p className="text-[11px] text-slate-500">{chief.role}</p>}
                {board.vision_summary && <p className="text-[11px] text-slate-400 leading-relaxed mt-2">{board.vision_summary}</p>}
                {board.governance && <p className="text-[9px] font-mono text-slate-600 mt-2">{typeof board.governance === 'string' ? board.governance : JSON.stringify(board.governance)}</p>}
              </Card>
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Users size={14} /> Board of Directors ({directors.length})</h4>
                <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-3">
                  {directors.length === 0 && <p className="text-slate-600 text-xs">No directors recorded.</p>}
                  {directors.map((d, i) => (
                    <div key={i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <p className="font-black text-white text-sm">{d.title || d.name || d.role || `Director ${i + 1}`}</p>
                      {(d.specialism || d.theme || d.focus) && <p className="text-[10px] text-slate-500 mt-1">{d.specialism || d.theme || d.focus}</p>}
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {/* Business Plan */}
          {tab === 'plan' && plan && (
            <div className="space-y-4">
              {[['Mission', plan.mission], ['Vision', plan.vision], ['Strategy', plan.strategy]].map(([label, val]) => (
                <Card key={label as string} className="p-6">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-2">{label}</h4>
                  <p className="text-sm text-slate-300 leading-relaxed">{(val as string) || <span className="text-slate-600">Not set.</span>}</p>
                </Card>
              ))}
              {Array.isArray(plan.aims) && plan.aims.length > 0 && (
                <Card className="p-6">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-2">Aims</h4>
                  <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">{plan.aims.map((a: string, i: number) => <li key={i}>{a}</li>)}</ul>
                </Card>
              )}
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-3">Objectives &amp; Roadmap ({(plan.objectives || []).length})</h4>
                <div className="space-y-3">
                  {(plan.objectives || []).map((o: Dict, i: number) => (
                    <div key={o.id || i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="flex items-center justify-between gap-2 flex-wrap">
                        <p className="font-black text-white text-sm">{o.title}</p>
                        <div className="flex items-center gap-2">
                          {o.timeline && <span className="text-[9px] font-black uppercase text-slate-500">{o.timeline}</span>}
                          {o.status && <Badge color={o.status === 'done' ? 'emerald-500' : 'aura'}>{o.status}</Badge>}
                        </div>
                      </div>
                      <div className="mt-2 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div className="h-full bg-highlight" style={{ width: `${Math.max(0, Math.min(100, o.progress_pct || 0))}%` }} />
                      </div>
                    </div>
                  ))}
                  {(plan.objectives || []).length === 0 && <p className="text-slate-600 text-xs">No objectives yet.</p>}
                </div>
              </Card>
            </div>
          )}

          {/* Living Systems */}
          {tab === 'systems' && (
            <Card className="p-6">
              <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2"><ShieldCheck size={14} /> Living management systems (BMS · QMS · DCS · EMS …)</h4>
              <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-3">
                {standards.map((s, i) => (
                  <div key={s.id || i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                    <p className="font-black text-white text-sm">{s.name || s.id}</p>
                    {s.standard && <p className="text-[10px] font-mono text-aura/60 mt-1">{s.standard}</p>}
                    {s.description && <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">{s.description}</p>}
                  </div>
                ))}
                {standards.length === 0 && <p className="text-slate-600 text-xs">Management systems unavailable.</p>}
              </div>
            </Card>
          )}

          {/* Transformation */}
          {tab === 'transform' && (
            <div className="space-y-4">
              <Card className="p-6">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <div>
                    <h4 className="text-sm font-black text-white uppercase tracking-wide">End-to-end Transformation</h4>
                    <p className="text-[11px] text-slate-500 mt-1">Run the whole org cascade for this VSB: Chief of the Board → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order, governed arms-length and simulated on a digital twin — in-house.</p>
                  </div>
                  <Button type="button" onClick={runTransformation} disabled={txRunning} className="bg-highlight text-sovereign flex items-center gap-2 text-xs shrink-0">
                    {txRunning ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run transformation
                  </Button>
                </div>
              </Card>
              {tx && (
                <>
                  <Card className="p-6">
                    <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Cascade ({(tx.cascade || []).length} stages · {tx.validation?.validated ? 'validated' : 'partial'})</h4>
                    <div className="space-y-2">
                      {(tx.cascade || []).map((s: Dict, i: number) => (
                        <div key={i} className="flex items-start gap-3 text-[11px]">
                          <span className="text-highlight font-black shrink-0">{s.step}.</span>
                          <div>
                            <span className="text-white font-black uppercase tracking-wide">{s.tier}</span>
                            {s.delegates_to && <span className="text-slate-600"> → {s.delegates_to}</span>}
                            <p className="text-slate-500">{s.action}</p>
                          </div>
                          {s.verified && <ShieldCheck size={12} className="text-emerald-400 ml-auto shrink-0 mt-0.5" />}
                        </div>
                      ))}
                    </div>
                  </Card>
                  <div className="grid grid-cols-1 @[700px]:grid-cols-2 gap-4">
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Boxes size={14} /> Operational delivery resources</h4>
                      <div className="flex flex-wrap gap-1.5">{(tx.operational_delivery_resources || []).map((r: string, i: number) => <span key={i} className="px-2 py-1 rounded-md bg-slate-800 text-[9px] font-black uppercase text-slate-300">{r}</span>)}</div>
                    </Card>
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><ScrollText size={14} /> Products / Services catalogue ({(tx.products_services_catalogue || []).length})</h4>
                      <ul className="text-[11px] text-slate-300 space-y-1">{(tx.products_services_catalogue || []).slice(0, 10).map((p: Dict, i: number) => <li key={i}>· {p.name}</li>)}</ul>
                    </Card>
                  </div>
                  {tx.digital_twin?.simulation && (
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Digital-twin simulation</h4>
                      <p className="text-[11px] text-slate-400">Projected realisation: <span className="text-highlight font-black">{String(tx.digital_twin.simulation.projected_realisation ?? '—')}</span> · governance: {tx.governance?.status}</p>
                    </Card>
                  )}
                </>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};
