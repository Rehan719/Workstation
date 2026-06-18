import React, { useState } from 'react';
import { Card, Badge } from '@workstation/ui';
import { Beaker, Trophy, Plus, X, FlaskConical, TrendingUp, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const DOMAINS = ['general','technology','enterprise','education','science','law','care','employment'];

interface TournamentVariant {
  variant_id: string;
  rank: number;
  fitness_score: number;
  response: string;
  strengths: string;
  weaknesses: string;
}

interface TournamentResult {
  tournament_id: string;
  name: string;
  variants_evaluated: number;
  winner: TournamentVariant;
  leaderboard: TournamentVariant[];
  analysis: string;
  completed_at: number;
}

interface TournamentRecord {
  id: string;
  name: string;
  domain: string;
  base_prompt: string;
  variants: number;
  status: 'pending' | 'running' | 'done' | 'error';
  result?: TournamentResult;
  error?: string;
}

export const Incubator: React.FC = () => {
  const [tournaments, setTournaments] = useState<TournamentRecord[]>([]);
  const [selected,    setSelected]    = useState<string | null>(null);
  const [showNew,     setShowNew]     = useState(false);

  // Form state
  const [name,       setName]       = useState('');
  const [domain,     setDomain]     = useState('general');
  const [basePrompt, setBasePrompt] = useState('');
  const [variants,   setVariants]   = useState(3);
  const [fitness,    setFitness]    = useState('relevance, clarity, commercial value, originality');

  const updateTournament = (id: string, patch: Partial<TournamentRecord>) =>
    setTournaments(ts => ts.map(t => t.id === id ? { ...t, ...patch } : t));

  const handleCreate = () => {
    if (!name.trim() || !basePrompt.trim()) return;
    const id = `t-${Date.now()}`;
    setTournaments(ts => [...ts, { id, name, domain, base_prompt: basePrompt, variants, status: 'pending' }]);
    setSelected(id);
    setShowNew(false);
    setName(''); setBasePrompt('');
  };

  const handleRun = async (id: string) => {
    const t = tournaments.find(x => x.id === id);
    if (!t || t.status === 'running') return;
    updateTournament(id, { status: 'running', result: undefined, error: undefined });
    try {
      const { data } = await axios.post<TournamentResult>('/api/v1/incubator/evolve', {
        name: t.name,
        base_prompt: t.base_prompt,
        domain: t.domain,
        variants: t.variants,
        fitness_criteria: fitness,
      });
      updateTournament(id, { status: 'done', result: data });
    } catch (err: any) {
      updateTournament(id, { status: 'error', error: err.response?.data?.detail ?? err.message });
    }
  };

  const selectedT = tournaments.find(t => t.id === selected);

  return (
    <div className="space-y-8 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black text-white uppercase tracking-tighter italic break-words">The Incubator</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">AI Prompt Evolution · Tournament Engine</p>
        </div>
        <button type="button" onClick={() => setShowNew(true)}
          className="flex items-center gap-2 px-5 py-2.5 bg-aura text-sovereign rounded-xl font-black text-xs uppercase tracking-widest hover:opacity-90 transition-opacity">
          <Plus size={14} /> New Tournament
        </button>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
        {/* Tournament list */}
        <aside className="@[440px]:col-span-4 space-y-3">
          <h3 className="text-[9px] font-black uppercase text-slate-500 tracking-[0.2em] px-1">Tournaments</h3>
          {tournaments.length === 0 && (
            <Card className="p-6 text-center">
              <Beaker size={24} className="text-slate-700 mx-auto mb-3" />
              <p className="text-xs text-slate-500 font-bold">No tournaments yet.</p>
              <p className="text-[9px] text-slate-600 mt-1">Create a tournament to evolve your best prompts.</p>
            </Card>
          )}
          {tournaments.map(t => (
            <motion.div key={t.id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
              onClick={() => setSelected(t.id)}
              className={`p-4 rounded-2xl border cursor-pointer transition-all ${selected === t.id ? 'border-aura bg-aura/5' : 'border-slate-800 bg-slate-950/50 hover:border-slate-700'}`}>
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-3 min-w-0">
                  <Beaker size={14} className="text-aura shrink-0" />
                  <div className="min-w-0">
                    <p className="text-xs font-black text-white uppercase truncate">{t.name}</p>
                    <p className="text-[8px] text-slate-500 capitalize">{t.domain} · {t.variants} variants</p>
                  </div>
                </div>
                <Badge color={t.status === 'done' ? 'emerald-500' : t.status === 'running' ? 'aura' : t.status === 'error' ? 'vital' : 'slate-500'}>
                  {t.status === 'running' ? 'Evolving…' : t.status}
                </Badge>
              </div>
              {t.result && (
                <div className="mt-3 pt-3 border-t border-slate-800 flex items-center gap-2">
                  <Trophy size={10} className="text-yellow-500" />
                  <span className="text-[9px] text-yellow-500 font-black">Winner V{t.result.winner.rank} · {(t.result.winner.fitness_score * 100).toFixed(0)}%</span>
                </div>
              )}
            </motion.div>
          ))}
        </aside>

        {/* Result panel */}
        <main className="@[440px]:col-span-8">
          {selectedT ? (
            <Card className="p-6 space-y-5 min-h-[400px] flex flex-col">
              <div className="flex items-start justify-between shrink-0">
                <div>
                  <h4 className="text-sm font-black text-white uppercase">{selectedT.name}</h4>
                  <p className="text-[9px] text-slate-500 mt-0.5">{selectedT.domain} · {selectedT.variants} variants</p>
                </div>
                {selectedT.status !== 'running' && (
                  <button type="button" onClick={() => handleRun(selectedT.id)}
                    className="flex items-center gap-2 px-4 py-2 bg-aura text-sovereign rounded-xl text-[9px] font-black uppercase tracking-widest hover:opacity-90">
                    <FlaskConical size={12} /> {selectedT.status === 'done' ? 'Re-run' : 'Run Evolution'}
                  </button>
                )}
              </div>

              {selectedT.status === 'running' && (
                <div className="flex-1 flex flex-col items-center justify-center gap-4 opacity-70">
                  <Loader2 size={36} className="text-aura animate-spin" />
                  <p className="text-xs text-aura font-black uppercase tracking-widest">Evolving {selectedT.variants} variants…</p>
                  <p className="text-[9px] text-slate-500">This may take 30–60 seconds</p>
                </div>
              )}

              {selectedT.status === 'error' && (
                <div className="flex-1 flex flex-col items-center justify-center gap-3">
                  <p className="text-xs text-red-400 font-bold">Evolution failed</p>
                  <p className="text-[9px] text-slate-500">{selectedT.error}</p>
                </div>
              )}

              {selectedT.status === 'pending' && (
                <div className="flex-1 flex flex-col items-center justify-center gap-3 opacity-40">
                  <Beaker size={36} />
                  <p className="text-xs font-black uppercase tracking-widest">Ready to evolve</p>
                  <p className="text-[9px] text-slate-500">Click "Run Evolution" to start the tournament</p>
                </div>
              )}

              {selectedT.status === 'done' && selectedT.result && (
                <div className="flex-1 space-y-5 overflow-y-auto">
                  {/* Winner card */}
                  <div className="p-5 rounded-2xl bg-yellow-500/5 border border-yellow-500/30">
                    <div className="flex items-center gap-3 mb-3">
                      <Trophy size={16} className="text-yellow-500" />
                      <span className="text-[10px] font-black uppercase text-yellow-500 tracking-widest">Winner — Variant {selectedT.result.winner.rank}</span>
                      <span className="ml-auto text-[10px] font-black text-yellow-500">{(selectedT.result.winner.fitness_score * 100).toFixed(0)}%</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed line-clamp-4">{selectedT.result.winner.response}</p>
                    <div className="mt-3 grid grid-cols-2 gap-3">
                      <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                        <p className="text-[8px] font-black text-emerald-400 uppercase mb-1">Strengths</p>
                        <p className="text-[9px] text-slate-400">{selectedT.result.winner.strengths}</p>
                      </div>
                      <div className="p-2 rounded-xl bg-red-500/10 border border-red-500/20">
                        <p className="text-[8px] font-black text-red-400 uppercase mb-1">Weaknesses</p>
                        <p className="text-[9px] text-slate-400">{selectedT.result.winner.weaknesses}</p>
                      </div>
                    </div>
                  </div>

                  {/* Leaderboard */}
                  <div>
                    <h5 className="text-[9px] font-black uppercase text-slate-500 tracking-[0.2em] mb-3">Leaderboard</h5>
                    <div className="space-y-2">
                      {selectedT.result.leaderboard.map(v => (
                        <div key={v.variant_id} className="flex items-center gap-3 p-3 rounded-xl bg-slate-950 border border-slate-800">
                          <span className="text-[9px] font-black text-slate-500 w-5">#{v.rank}</span>
                          <div className="flex-1 min-w-0">
                            <p className="text-[9px] text-slate-400 truncate">{v.response.slice(0, 80)}…</p>
                          </div>
                          <div className="flex items-center gap-2 shrink-0">
                            <progress
                              value={v.fitness_score}
                              max={1}
                              aria-label={`Fitness score ${(v.fitness_score * 100).toFixed(0)}%`}
                              className="w-20 h-1.5 appearance-none rounded-full overflow-hidden [&::-webkit-progress-bar]:bg-slate-800 [&::-webkit-progress-value]:bg-aura [&::-moz-progress-bar]:bg-aura"
                            />
                            <span className="text-[9px] font-black text-aura">{(v.fitness_score * 100).toFixed(0)}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Analysis */}
                  {selectedT.result.analysis && (
                    <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
                      <div className="flex items-center gap-2 mb-2">
                        <TrendingUp size={12} className="text-aura" />
                        <span className="text-[9px] font-black uppercase text-slate-400 tracking-widest">Evolution Analysis</span>
                      </div>
                      <p className="text-[10px] text-slate-400 leading-relaxed">{selectedT.result.analysis}</p>
                    </div>
                  )}
                </div>
              )}
            </Card>
          ) : (
            <Card className="p-12 flex flex-col items-center justify-center text-center opacity-40 min-h-[400px]">
              <Beaker size={36} className="mb-4" />
              <p className="text-sm font-black uppercase tracking-widest">Select a tournament</p>
              <p className="text-[9px] text-slate-500 mt-2">or create a new one to evolve your prompts</p>
            </Card>
          )}
        </main>
      </div>

      {/* New tournament modal */}
      <AnimatePresence>
        {showNew && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-6">
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }}
              className="bg-slate-950 border border-slate-800 rounded-[2rem] p-8 w-full max-w-lg space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-black text-white uppercase tracking-tight">New Tournament</h3>
                <button type="button" aria-label="Close" onClick={() => setShowNew(false)} className="text-slate-500 hover:text-white"><X size={18} /></button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Tournament Name</label>
                  <input value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Growth Hypothesis Round 1"
                    aria-label="Tournament name"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-aura" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Domain</label>
                    <select value={domain} onChange={e => setDomain(e.target.value)} aria-label="Domain"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura">
                      {DOMAINS.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase()+d.slice(1)}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Variants (2–5)</label>
                    <input type="number" min={2} max={5} value={variants}
                      onChange={e => setVariants(Math.min(5, Math.max(2, parseInt(e.target.value) || 2)))}
                      aria-label="Number of variants"
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura" />
                  </div>
                </div>
                <div>
                  <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Base Prompt / Task</label>
                  <textarea value={basePrompt} onChange={e => setBasePrompt(e.target.value)} rows={4}
                    placeholder="Describe the task you want to evolve the best response for…"
                    aria-label="Base prompt"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-aura resize-none" />
                </div>
                <div>
                  <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Fitness Criteria</label>
                  <input value={fitness} onChange={e => setFitness(e.target.value)} aria-label="Fitness criteria"
                    className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-aura" />
                </div>
              </div>

              <button type="button" onClick={handleCreate} disabled={!name.trim() || !basePrompt.trim()}
                className="w-full py-3 bg-aura text-sovereign rounded-xl font-black uppercase tracking-widest text-xs hover:opacity-90 transition-opacity disabled:opacity-40">
                Create Tournament
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
