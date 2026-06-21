import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Card, Button } from '@workstation/ui';
import {
  Sparkles, Loader2, CheckCircle2, Circle, AlertCircle,
  Brain, Dna, Bot, ShieldCheck, ChevronRight, ListTree, Clock,
  RefreshCw,
} from 'lucide-react';

// ── SSE helper ────────────────────────────────────────────────────────────────

async function streamPost(
  url: string,
  body: object,
  onChunk: (ev: SpawnEvent) => void,
  onDone: () => void,
  onError: (e: string) => void,
) {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      onError(`HTTP ${res.status}: ${await res.text()}`);
      return;
    }
    const reader = res.body!.getReader();
    const dec = new TextDecoder();
    let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop()!;
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const raw = line.slice(6).trim();
          if (raw === '[DONE]') continue;
          try { onChunk(JSON.parse(raw)); } catch {}
        }
      }
    }
    onDone();
  } catch (e: any) {
    onError(e?.message ?? String(e));
  }
}

// ── Types ─────────────────────────────────────────────────────────────────────

interface SpawnEvent {
  stage: string;
  label: string;
  content: string;
  data?: Record<string, any>;
}

interface VSBEntity {
  vsb_id: string;
  name: string;
  domain: string;
  status: string;
  stage: string;
  created_at: string;
}

interface Director { id?: string; title?: string; name?: string }
interface VSBDetail extends VSBEntity {
  board?: { chief?: { title?: string }; directors?: Director[]; governance?: string };
  economy?: { entity_type?: string; entity_name?: string; currency?: string };
  business_plan_scope?: string;
}
interface OrchRun {
  cascade: { step: number; tier: string; verified: boolean }[];
  validation: { verified_stages: number; stages: number; validated: boolean };
  governance: { status: string };
  digital_twin: { simulation: { verdict: string } };
}

// ── Stage config ──────────────────────────────────────────────────────────────

const STAGE_META: Record<string, { icon: React.FC<any>; color: string }> = {
  init:               { icon: Sparkles,    color: 'text-aura' },
  cognitive:          { icon: Brain,       color: 'text-violet-400' },
  cognitive_complete: { icon: CheckCircle2,color: 'text-emerald-400' },
  mjm:                { icon: ListTree,    color: 'text-highlight' },
  mjm_complete:       { icon: CheckCircle2,color: 'text-emerald-400' },
  gaas:               { icon: ShieldCheck, color: 'text-sky-400' },
  gaas_complete:      { icon: CheckCircle2,color: 'text-emerald-400' },
  ceo_strategy:       { icon: Bot,         color: 'text-aura' },
  ceo_complete:       { icon: CheckCircle2,color: 'text-emerald-400' },
  genome:             { icon: Dna,         color: 'text-pink-400' },
  genome_complete:    { icon: CheckCircle2,color: 'text-emerald-400' },
  swarm:              { icon: Bot,         color: 'text-orange-400' },
  swarm_complete:     { icon: CheckCircle2,color: 'text-emerald-400' },
  complete:           { icon: Sparkles,    color: 'text-aura' },
  error:              { icon: AlertCircle, color: 'text-vital' },
};

// ── Component ─────────────────────────────────────────────────────────────────

export const VSBSpawnStudio: React.FC = () => {
  const [challenge, setChallenge] = useState('');
  const [domain, setDomain] = useState('enterprise');
  const [scope, setScope] = useState('build');
  const [spawning, setSpawning] = useState(false);
  const [events, setEvents] = useState<SpawnEvent[]>([]);
  const [error, setError] = useState('');
  const [entities, setEntities] = useState<VSBEntity[]>([]);
  const [loadingEntities, setLoadingEntities] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const [detail, setDetail] = useState<Record<string, VSBDetail>>({});
  const [orch, setOrch] = useState<Record<string, OrchRun>>({});
  const [orchBusy, setOrchBusy] = useState<string | null>(null);
  const feedRef = useRef<HTMLDivElement>(null);

  const fetchEntities = async () => {
    setLoadingEntities(true);
    try {
      const r = await axios.get('/api/v1/vsb');
      setEntities(r.data.entities ?? []);
    } catch {}
    setLoadingEntities(false);
  };

  const openDetail = async (vsbId: string) => {
    setSelected(prev => (prev === vsbId ? null : vsbId));
    if (!detail[vsbId]) {
      try {
        const r = await axios.get(`/api/v1/vsb/${vsbId}`);
        setDetail(prev => ({ ...prev, [vsbId]: r.data }));
      } catch {}
    }
  };
  const orchestrateVsb = async (vsbId: string) => {
    setOrchBusy(vsbId);
    try {
      const r = await axios.post('/api/v1/transformation/orchestrate', { scope: vsbId, owner_id: 'Rehan' });
      setOrch(prev => ({ ...prev, [vsbId]: r.data }));
    } catch {}
    setOrchBusy(null);
  };

  useEffect(() => { fetchEntities(); }, []);

  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [events]);

  const handleSpawn = async () => {
    if (!challenge.trim()) return;
    setSpawning(true);
    setEvents([]);
    setError('');

    await streamPost(
      '/api/v1/vsb/spawn',
      { challenge, domain, scope, owner_id: 'default' },
      (ev) => setEvents(prev => [...prev, ev]),
      () => {
        setSpawning(false);
        fetchEntities();
      },
      (e) => { setError(e); setSpawning(false); },
    );
  };

  const DOMAINS = ['enterprise', 'science', 'law', 'care', 'education', 'career', 'religion'];
  const SCOPES  = ['concept', 'build', 'commercialise'];

  return (
    <div className="space-y-10 pb-24">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2">Enterprise Realm</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">
          VSB Spawn Studio
        </h1>
        <p className="text-slate-500 font-bold mt-2 max-w-xl leading-relaxed">
          Spawn a Virtual Sovereign Business from a challenge. Runs through the full
          intelligence pipeline: Nine Cognitive Engines → MJM → GaaS → CEO Strategy → Genome.
        </p>
      </header>

      {/* Input form */}
      <Card className="p-8 space-y-6">
        <div>
          <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">
            Challenge / Business Concept
          </label>
          <textarea
            value={challenge}
            onChange={e => setChallenge(e.target.value)}
            placeholder="Describe the business challenge or opportunity you want to address..."
            rows={4}
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-aura/50 resize-none"
          />
        </div>

        <div className="flex flex-wrap gap-6">
          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Domain</label>
            <div className="flex flex-wrap gap-2">
              {DOMAINS.map(d => (
                <button
                  key={d}
                  type="button"
                  onClick={() => setDomain(d)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    domain === d
                      ? 'bg-aura/20 text-aura border border-aura/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {d}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-400 mb-2 block">Scope</label>
            <div className="flex gap-2">
              {SCOPES.map(s => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setScope(s)}
                  className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${
                    scope === s
                      ? 'bg-highlight/20 text-highlight border border-highlight/40'
                      : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 pt-2">
          <Button
            onClick={handleSpawn}
            disabled={spawning || !challenge.trim()}
            className="flex items-center gap-2"
          >
            {spawning ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
            {spawning ? 'Spawning VSB...' : 'Spawn VSB Entity'}
          </Button>
          {error && (
            <p className="text-vital text-xs font-bold flex items-center gap-2">
              <AlertCircle size={14} /> {error}
            </p>
          )}
        </div>
      </Card>

      {/* Live pipeline feed */}
      {events.length > 0 && (
        <Card className="p-6">
          <h3 className="text-sm font-black uppercase tracking-widest text-slate-400 mb-4">
            Pipeline Feed
          </h3>
          <div
            ref={feedRef}
            className="space-y-3 max-h-[400px] overflow-y-auto pr-2"
          >
            {events.map((ev, i) => {
              const meta = STAGE_META[ev.stage] ?? { icon: Circle, color: 'text-slate-500' };
              const Icon = meta.icon;
              return (
                <div key={i} className="flex gap-3 items-start p-3 rounded-xl bg-slate-950/50 border border-slate-900">
                  <Icon size={16} className={`mt-0.5 shrink-0 ${meta.color}`} />
                  <div className="min-w-0">
                    <p className="text-[10px] font-black uppercase tracking-widest text-slate-400">
                      {ev.label}
                    </p>
                    <p className="text-sm text-slate-300 mt-0.5 leading-relaxed line-clamp-3">
                      {ev.content}
                    </p>
                    {ev.data?.vsb_id && (
                      <p className="text-[9px] font-mono text-aura mt-1">
                        ID: {ev.data.vsb_id}
                      </p>
                    )}
                  </div>
                </div>
              );
            })}
            {spawning && (
              <div className="flex items-center gap-2 p-3 text-slate-500">
                <Loader2 size={14} className="animate-spin" />
                <span className="text-xs font-bold">Processing next stage...</span>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Existing VSB entities */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-sm font-black uppercase tracking-widest text-white">
            Spawned Entities ({entities.length})
          </h3>
          <button
            type="button"
            onClick={fetchEntities}
            className="p-2 rounded-lg hover:bg-slate-800 text-slate-500 hover:text-white transition-all"
          >
            <RefreshCw size={14} className={loadingEntities ? 'animate-spin' : ''} />
          </button>
        </div>

        {entities.length === 0 ? (
          <p className="text-slate-600 text-sm font-bold uppercase tracking-widest text-center py-10">
            No VSB entities yet. Spawn your first one above.
          </p>
        ) : (
          <div className="space-y-3">
            {entities.map(e => (
              <React.Fragment key={e.vsb_id}>
              <div
                onClick={() => openDetail(e.vsb_id)}
                className="flex items-center justify-between p-4 rounded-xl bg-slate-950/60 border border-slate-900 hover:border-aura/20 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-xl bg-aura/10 flex items-center justify-center">
                    <Bot size={14} className="text-aura" />
                  </div>
                  <div>
                    <p className="font-black text-white text-sm">{e.name || e.vsb_id}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-[9px] font-bold uppercase text-slate-500">{e.domain}</span>
                      <span className="text-slate-700">•</span>
                      <span className="text-[9px] font-bold uppercase text-slate-500">{e.stage}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`text-[9px] font-black uppercase px-2 py-1 rounded-lg ${
                    e.status === 'active'
                      ? 'bg-emerald-500/10 text-emerald-400'
                      : 'bg-slate-800 text-slate-500'
                  }`}>
                    {e.status || 'spawned'}
                  </span>
                  <div className="flex items-center gap-1 text-[9px] text-slate-600">
                    <Clock size={10} />
                    {e.created_at ? new Date(e.created_at).toLocaleDateString() : '—'}
                  </div>
                  <ChevronRight size={14} className={`text-slate-700 transition-transform ${selected === e.vsb_id ? 'rotate-90' : ''}`} />
                </div>
              </div>
              {selected === e.vsb_id && (
                <VSBDetailPanel d={detail[e.vsb_id]} orch={orch[e.vsb_id]}
                  busy={orchBusy === e.vsb_id} onOrchestrate={() => orchestrateVsb(e.vsb_id)} />
              )}
              </React.Fragment>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

// ── Per-VSB org detail: Board · Economy · Living Plan · Transformation cascade ──
const VSBDetailPanel: React.FC<{
  d?: VSBDetail; orch?: OrchRun; busy: boolean; onOrchestrate: () => void;
}> = ({ d, orch, busy, onOrchestrate }) => {
  if (!d) return <div className="ml-4 px-4 py-3 text-[10px] text-slate-600 font-bold uppercase tracking-widest">Loading org…</div>;
  const directors = d.board?.directors ?? [];
  return (
    <div className="ml-4 mb-2 p-4 rounded-xl bg-slate-950 border border-aura/15 space-y-4">
      <div>
        <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1.5">Board of Directors (arms-length)</p>
        <p className="text-xs font-bold text-white">{d.board?.chief?.title ?? 'Chief — Owner digital twin'}</p>
        <div className="flex flex-wrap gap-1.5 mt-1.5">
          {directors.map((dir, i) => (
            <span key={i} className="text-[9px] font-bold px-2 py-0.5 rounded bg-slate-900 text-slate-400">{dir.title ?? dir.name ?? dir.id}</span>
          ))}
          {directors.length === 0 && <span className="text-[9px] text-slate-600">No directors recorded</span>}
        </div>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <p className="text-[9px] font-black uppercase tracking-widest text-emerald-400 mb-1">Economy</p>
          <p className="text-[11px] text-slate-300 font-bold">{d.economy?.entity_name ?? d.economy?.entity_type ?? '—'}</p>
          <p className="text-[9px] text-slate-600">{d.economy?.currency ?? 'WST (virtual)'}</p>
        </div>
        <div>
          <p className="text-[9px] font-black uppercase tracking-widest text-highlight mb-1">Living Business Plan</p>
          <a href={`/business-plan?scope=${d.business_plan_scope ?? d.vsb_id}`} className="text-[11px] text-aura font-bold underline">Open plan →</a>
        </div>
      </div>
      <div>
        <Button onClick={onOrchestrate} disabled={busy} className="flex items-center gap-2 bg-aura text-sovereign text-xs">
          {busy ? <Loader2 size={13} className="animate-spin" /> : <Sparkles size={13} />} Orchestrate transformation (Chief → BTO)
        </Button>
        {orch && (
          <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[9px] font-black uppercase text-slate-400">
                {orch.validation.verified_stages}/{orch.validation.stages} stages · gov {orch.governance.status} · twin {orch.digital_twin.simulation.verdict}
              </span>
              <span className={`text-[9px] font-black uppercase px-2 py-0.5 rounded ${orch.validation.validated ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                {orch.validation.validated ? 'VALIDATED' : 'PARTIAL'}
              </span>
            </div>
            <div className="flex flex-wrap gap-1">
              {orch.cascade.map(s => (
                <span key={s.step} className="text-[8px] font-bold px-1.5 py-0.5 rounded bg-slate-950 text-slate-500 flex items-center gap-1">
                  {s.verified ? <CheckCircle2 size={8} className="text-emerald-400" /> : <Circle size={8} />}{s.tier.split(' ')[0]}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
