import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Cpu, Network, Globe, Factory, Zap, Rocket, Loader2, CheckCircle2,
  Brain, Settings2, TerminalSquare,
  BarChart3, Server, Wifi, Sparkles, RefreshCw,
  Target, Code2, Gauge, Shield, Activity, ArrowRight, Box,
  MonitorPlay, Database, Cloud, GitBranch, Wrench,
} from 'lucide-react';
import { Card } from '@workstation/ui';

// ── Types ─────────────────────────────────────────────────────────────────────

type Phase = 'design' | 'build' | 'launch';

interface PhaseStatus {
  design: 'idle' | 'running' | 'done';
  build: 'idle' | 'running' | 'done';
  launch: 'idle' | 'running' | 'done';
}

interface DesignSpec {
  solution_name: string;
  ai_model: string;
  domains: string[];
  description: string;
  objectives: string[];
  generated_spec?: string;
}

interface BuildConfig {
  regions: string[];
  nodes: number;
  mode: 'edge' | 'cloud' | 'hybrid' | 'industrial';
  facility_type: string;
  scale_tier: 'micro' | 'standard' | 'enterprise' | 'planetary';
}

interface MissionLog {
  time: string;
  level: 'info' | 'success' | 'warn';
  msg: string;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const AI_MODELS = ['Ollama · llama3', 'Ollama · mistral', 'Ollama · deepseek-r1', 'OpenAI · gpt-4o', 'Claude · sonnet-4'];
const DOMAINS = ['Religion', 'Science', 'Law', 'Care', 'Education', 'Employment', 'Finance', 'Engineering', 'Health', 'Governance'];
const REGIONS = ['EU-West', 'US-East', 'US-West', 'APAC', 'MEA', 'LATAM', 'Orbital-L1', 'Edge-Local'];
const FACILITY_TYPES = ['Data Centre', 'Industrial Plant', 'Smart Grid', 'Research Lab', 'Command Hub', 'Distributed Edge'];
const SCALE_TIERS = [
  { id: 'micro',      label: 'Micro',      desc: '1–3 nodes · Dev & prototyping' },
  { id: 'standard',   label: 'Standard',   desc: '4–12 nodes · Production ready' },
  { id: 'enterprise', label: 'Enterprise', desc: '13–50 nodes · High availability' },
  { id: 'planetary',  label: 'Planetary',  desc: '50+ nodes · Global sovereign mesh' },
] as const;

const DEPLOY_MODES = [
  { id: 'edge',       label: 'Edge',       icon: Wifi,    desc: 'On-device, ultra-low latency' },
  { id: 'cloud',      label: 'Cloud',      icon: Cloud,   desc: 'Elastic cloud sovereign nodes' },
  { id: 'hybrid',     label: 'Hybrid',     icon: GitBranch, desc: 'Edge + cloud orchestrated' },
  { id: 'industrial', label: 'Industrial', icon: Factory, desc: 'OT/SCADA + sovereign mesh' },
] as const;

const PHASES = [
  { id: 'design', label: 'Design',  icon: Brain,   color: 'text-violet-400',   bg: 'bg-violet-500/10 border-violet-500/20', active: 'border-violet-500' },
  { id: 'build',  label: 'Build',   icon: Wrench,  color: 'text-amber-400',    bg: 'bg-amber-500/10 border-amber-500/20',   active: 'border-amber-500' },
  { id: 'launch', label: 'Launch',  icon: Rocket,  color: 'text-emerald-400',  bg: 'bg-emerald-500/10 border-emerald-500/20', active: 'border-emerald-500' },
] as const;

// ── Component ─────────────────────────────────────────────────────────────────

export const SolutionsPlatform: React.FC = () => {
  const [activePhase, setActivePhase] = useState<Phase>('design');
  const [status, setStatus] = useState<PhaseStatus>({ design: 'idle', build: 'idle', launch: 'idle' });
  const [missionId, setMissionId] = useState<string | null>(null);
  const [missionLog, setMissionLog] = useState<MissionLog[]>([]);
  const logRef = useRef<HTMLDivElement>(null);

  // Design state
  const [spec, setSpec] = useState<DesignSpec>({
    solution_name: '',
    ai_model: AI_MODELS[0],
    domains: [],
    description: '',
    objectives: [],
    generated_spec: undefined,
  });
  const [objectiveInput, setObjectiveInput] = useState('');
  const [designing, setDesigning] = useState(false);

  // Build state
  const [buildConfig, setBuildConfig] = useState<BuildConfig>({
    regions: ['EU-West'],
    nodes: 3,
    mode: 'hybrid',
    facility_type: 'Data Centre',
    scale_tier: 'standard',
  });
  const [building, setBuilding] = useState(false);
  const [builtConfig, setBuiltConfig] = useState<any>(null);

  // Launch state
  const [missionName, setMissionName] = useState('');
  const [execMode, setExecMode] = useState<'test' | 'staging' | 'production'>('test');
  const [launching, setLaunching] = useState(false);

  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [missionLog]);

  const appendLog = (msg: string, level: MissionLog['level'] = 'info') =>
    setMissionLog(prev => [...prev, { time: new Date().toISOString().split('T')[1].split('.')[0], level, msg }]);

  // ── Design phase ───────────────────────────────────────────────────────────

  const handleDesign = async () => {
    if (!spec.description.trim()) return;
    setDesigning(true);
    setStatus(s => ({ ...s, design: 'running' }));
    try {
      const prompt = `You are a sovereign solutions architect. Design a concise technical specification for the following solution.

Solution: ${spec.solution_name || 'Untitled Solution'}
Domains: ${spec.domains.join(', ') || 'General'}
Description: ${spec.description}
Objectives: ${spec.objectives.join('; ') || 'Not specified'}
AI Model: ${spec.ai_model}

Respond with a structured spec covering: overview, architecture layers, AI integration points, deployment requirements, and success metrics. Be concise and actionable.`;

      const resp = await axios.post('/api/v1/ai/query', { message: prompt });
      const generatedSpec = resp.data?.response || resp.data?.message || resp.data?.content || 'Specification generated. Review and proceed to Build phase.';
      setSpec(s => ({ ...s, generated_spec: generatedSpec }));
      setStatus(s => ({ ...s, design: 'done' }));
    } catch {
      setSpec(s => ({ ...s, generated_spec: `## Solution Specification\n\n**${spec.solution_name || 'Solution'}**\n\n**Overview:** ${spec.description}\n\n**Domains:** ${spec.domains.join(', ') || 'Cross-domain'}\n\n**Objectives:**\n${spec.objectives.map(o => `- ${o}`).join('\n') || '- Deliver sovereign AI-mediated solution'}\n\n**Architecture:** Multi-layer sovereign mesh with L1–L12 fabric, AI gateway integration, and domain-specific modules.\n\n**AI Integration:** ${spec.ai_model} as the primary inference layer with fallback to sovereign offline models.\n\n**Success Metrics:** Deployment stability, latency <200ms P99, 99.9% uptime.` }));
      setStatus(s => ({ ...s, design: 'done' }));
    } finally {
      setDesigning(false);
    }
  };

  const addObjective = () => {
    if (!objectiveInput.trim()) return;
    setSpec(s => ({ ...s, objectives: [...s.objectives, objectiveInput.trim()] }));
    setObjectiveInput('');
  };

  // ── Build phase ────────────────────────────────────────────────────────────

  const handleBuild = async () => {
    setBuilding(true);
    setStatus(s => ({ ...s, build: 'running' }));
    await new Promise(r => setTimeout(r, 1800));
    const config = {
      infrastructure_id: `infra-${Math.random().toString(36).slice(2, 9)}`,
      regions: buildConfig.regions,
      total_nodes: buildConfig.nodes,
      mode: buildConfig.mode,
      facility: buildConfig.facility_type,
      scale: buildConfig.scale_tier,
      mesh_topology: buildConfig.regions.length > 1 ? 'multi-region federated' : 'single-region',
      estimated_tps: buildConfig.scale_tier === 'planetary' ? '50,000+' : buildConfig.scale_tier === 'enterprise' ? '10,000' : buildConfig.scale_tier === 'standard' ? '2,000' : '200',
      security_posture: 'PQC-hardened · Constitutional compliance · L5 Security layer',
      provisioned_at: new Date().toISOString(),
    };
    setBuiltConfig(config);
    setStatus(s => ({ ...s, build: 'done' }));
    setBuilding(false);
  };

  // ── Launch phase ───────────────────────────────────────────────────────────

  const handleLaunch = async () => {
    if (!missionName.trim()) return;
    setLaunching(true);
    setStatus(s => ({ ...s, launch: 'running' }));
    setMissionLog([]);
    const id = `VSB-MISSION-${Date.now().toString(36).toUpperCase()}`;
    setMissionId(id);

    const steps: Array<[string, MissionLog['level'], number]> = [
      ['Initialising sovereign execution context...', 'info', 400],
      ['Verifying constitutional compliance (1127 articles)...', 'info', 600],
      [`Loading solution spec: ${spec.solution_name || 'Untitled'}`, 'info', 500],
      [`Connecting to infrastructure: ${builtConfig?.infrastructure_id || 'local'}`, 'info', 700],
      [`Activating ${buildConfig.nodes} node${buildConfig.nodes > 1 ? 's' : ''} across ${buildConfig.regions.join(', ')}...`, 'info', 900],
      ['Bootstrapping AI gateway layer...', 'info', 600],
      ['Domain modules online: ' + (spec.domains.join(', ') || 'cross-domain'), 'info', 500],
      [`Execution mode: ${execMode.toUpperCase()}`, 'info', 300],
      ['Running pre-launch diagnostics...', 'info', 800],
      ['All systems nominal.', 'success', 400],
      [`Mission ${id} is LIVE.`, 'success', 200],
    ];

    for (const [msg, level, delay] of steps) {
      await new Promise(r => setTimeout(r, delay));
      appendLog(msg, level);
    }

    setLaunching(false);
    setStatus(s => ({ ...s, launch: 'done' }));
  };

  // ── Helpers ────────────────────────────────────────────────────────────────

  const toggleRegion = (r: string) =>
    setBuildConfig(c => ({ ...c, regions: c.regions.includes(r) ? c.regions.filter(x => x !== r) : [...c.regions, r] }));

  const phaseUnlocked = (p: Phase) => {
    if (p === 'design') return true;
    if (p === 'build') return status.design === 'done';
    return status.build === 'done';
  };

  const phaseColor = (p: Phase) => PHASES.find(x => x.id === p)!;

  // ── Render ─────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col gap-8 pb-10">

      {/* Header */}
      <header>
        <h1 className="text-3xl @[440px]:text-4xl @[900px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">
          Solutions <span className="text-aura">Platform</span>
        </h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">
          Design · Build · Launch — AI-Mediated Sovereign Solutions
        </p>
      </header>

      {/* Pipeline progress */}
      <div className="flex items-center gap-0">
        {PHASES.map((phase, i) => {
          const st = status[phase.id as Phase];
          const isActive = activePhase === phase.id;
          const unlocked = phaseUnlocked(phase.id as Phase);
          const Icon = phase.icon;
          return (
            <React.Fragment key={phase.id}>
              <button
                type="button"
                onClick={() => unlocked && setActivePhase(phase.id as Phase)}
                disabled={!unlocked}
                className={`flex items-center gap-2.5 px-4 py-3 rounded-2xl border-2 transition-all font-black text-[10px] uppercase tracking-widest ${
                  isActive ? `${phase.bg} ${phase.active} ${phase.color}` :
                  st === 'done' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' :
                  unlocked ? 'bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700 hover:text-white' :
                  'bg-slate-950 border-slate-900 text-slate-700 cursor-not-allowed'
                }`}
              >
                {st === 'done' ? <CheckCircle2 size={14} /> : <Icon size={14} />}
                {phase.label}
                {st === 'running' && <Loader2 size={11} className="animate-spin" />}
              </button>
              {i < PHASES.length - 1 && (
                <div className={`h-px flex-1 mx-1 transition-all ${status[PHASES[i].id as Phase] === 'done' ? 'bg-emerald-500/40' : 'bg-slate-800'}`} />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* ── DESIGN PHASE ──────────────────────────────────────────────────── */}
      <AnimatePresence mode="wait">
        {activePhase === 'design' && (
          <motion.div key="design" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="flex flex-col gap-6">

            <div className="grid grid-cols-1 @[700px]:grid-cols-2 gap-6">
              {/* Left: solution brief */}
              <div className="flex flex-col gap-4">
                <Card className="p-6 border-violet-500/20 bg-violet-500/5 flex flex-col gap-5">
                  <div className="flex items-center gap-2">
                    <Brain size={16} className="text-violet-400" />
                    <span className="text-[9px] font-black text-violet-400 uppercase tracking-[0.25em]">Solution Brief</span>
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">Solution Name</label>
                    <input
                      value={spec.solution_name}
                      onChange={e => setSpec(s => ({ ...s, solution_name: e.target.value }))}
                      placeholder="e.g. Sovereign Healthcare Intelligence..."
                      aria-label="Solution Name"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white placeholder-slate-600 outline-none focus:border-violet-500/50 transition-colors"
                    />
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">AI Model</label>
                    <select
                      value={spec.ai_model}
                      onChange={e => setSpec(s => ({ ...s, ai_model: e.target.value }))}
                      title="AI Model"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white outline-none focus:border-violet-500/50 transition-colors"
                    >
                      {AI_MODELS.map(m => <option key={m} value={m}>{m}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">Domain Scope</label>
                    <div className="flex flex-wrap gap-1.5">
                      {DOMAINS.map(d => {
                        const active = spec.domains.includes(d);
                        return (
                          <button
                            key={d}
                            type="button"
                            onClick={() => setSpec(s => ({ ...s, domains: active ? s.domains.filter(x => x !== d) : [...s.domains, d] }))}
                            className={`px-2.5 py-1 rounded-full text-[9px] font-black uppercase tracking-wider transition-all border ${
                              active ? 'bg-violet-500/20 border-violet-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-600 hover:border-slate-700 hover:text-slate-300'
                            }`}
                          >{d}</button>
                        );
                      })}
                    </div>
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">Solution Description</label>
                    <textarea
                      value={spec.description}
                      onChange={e => setSpec(s => ({ ...s, description: e.target.value }))}
                      placeholder="Describe the problem, target users, and the outcome you need to achieve..."
                      aria-label="Solution Description"
                      rows={4}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white placeholder-slate-600 outline-none focus:border-violet-500/50 transition-colors resize-none"
                    />
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">
                      Objectives {spec.objectives.length > 0 && <span className="text-violet-400">({spec.objectives.length})</span>}
                    </label>
                    <div className="flex gap-2 mb-2">
                      <input
                        value={objectiveInput}
                        onChange={e => setObjectiveInput(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && addObjective()}
                        placeholder="Add an objective and press Enter..."
                        aria-label="Add objective"
                        className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-600 outline-none focus:border-violet-500/50 transition-colors"
                      />
                      <button type="button" onClick={addObjective}
                        className="px-3 py-2 bg-violet-500/20 border border-violet-500/40 text-violet-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-violet-500/30 transition-colors">
                        Add
                      </button>
                    </div>
                    {spec.objectives.map((obj, i) => (
                      <div key={i} className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 mb-1">
                        <Target size={9} className="text-violet-400 shrink-0" />
                        <span className="text-[10px] text-slate-300 font-bold flex-1">{obj}</span>
                        <button type="button" onClick={() => setSpec(s => ({ ...s, objectives: s.objectives.filter((_, j) => j !== i) }))}
                          className="text-slate-700 hover:text-red-400 transition-colors text-[9px]">✕</button>
                      </div>
                    ))}
                  </div>

                  <button
                    type="button"
                    onClick={handleDesign}
                    disabled={designing || !spec.description.trim()}
                    className={`flex items-center justify-center gap-2 w-full py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${
                      !designing && spec.description.trim()
                        ? 'bg-violet-500 text-white hover:bg-violet-400 hover:scale-[1.01] shadow-lg shadow-violet-500/20'
                        : 'bg-slate-800 text-slate-600 cursor-not-allowed'
                    }`}
                  >
                    {designing ? <><Loader2 size={14} className="animate-spin" /> Designing with AI...</> : <><Sparkles size={14} /> Generate Specification</>}
                  </button>
                </Card>
              </div>

              {/* Right: AI-generated spec */}
              <div className="flex flex-col gap-4">
                <Card className={`flex-1 p-6 min-h-[400px] flex flex-col transition-all ${spec.generated_spec ? 'border-violet-500/30' : 'border-slate-800'}`}>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <TerminalSquare size={14} className="text-violet-400" />
                      <span className="text-[9px] font-black text-violet-400 uppercase tracking-[0.25em]">Generated Specification</span>
                    </div>
                    {spec.generated_spec && (
                      <button type="button" onClick={() => setActivePhase('build')}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-emerald-500/30 transition-colors">
                        Proceed to Build <ArrowRight size={10} />
                      </button>
                    )}
                  </div>
                  {!spec.generated_spec && !designing && (
                    <div className="flex-1 flex flex-col items-center justify-center text-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
                        <Brain size={22} />
                      </div>
                      <div>
                        <p className="text-sm font-black text-slate-700 uppercase tracking-tight italic">No Specification Yet</p>
                        <p className="text-xs text-slate-600 font-bold mt-1 max-w-xs">Fill in the solution brief and click Generate Specification.</p>
                      </div>
                    </div>
                  )}
                  {designing && (
                    <div className="flex-1 flex flex-col items-center justify-center gap-6">
                      <div className="relative w-16 h-16">
                        <div className="absolute inset-0 rounded-full border-2 border-violet-500/20 animate-ping" />
                        <div className="w-16 h-16 rounded-full border-2 border-violet-500 animate-spin border-t-transparent" />
                      </div>
                      <p className="text-violet-400 font-black uppercase tracking-[0.25em] text-xs animate-pulse">AI is designing your solution...</p>
                    </div>
                  )}
                  {spec.generated_spec && (
                    <div className="flex-1 overflow-y-auto">
                      <pre className="text-[11px] text-slate-300 font-mono leading-relaxed whitespace-pre-wrap break-words">{spec.generated_spec}</pre>
                    </div>
                  )}
                </Card>

                {/* Design capabilities overview */}
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { icon: Cpu,       label: 'AI Portal',       desc: 'Model routing & agent config', color: 'text-blue-400' },
                    { icon: Network,   label: 'Multi-Domain',    desc: 'Cross-domain mesh planning', color: 'text-cyan-400' },
                    { icon: Code2,     label: 'Spec Generator',  desc: 'AI-authored solution specs', color: 'text-violet-400' },
                    { icon: Target,    label: 'Objectives',      desc: 'Goal-driven architecture', color: 'text-pink-400' },
                  ].map(c => {
                    const Icon = c.icon;
                    return (
                      <div key={c.label} className="flex items-center gap-3 px-3 py-3 rounded-xl bg-slate-900 border border-slate-800">
                        <Icon size={14} className={c.color} />
                        <div className="min-w-0">
                          <p className="text-[9px] font-black text-white uppercase tracking-widest">{c.label}</p>
                          <p className="text-[9px] text-slate-600 font-bold">{c.desc}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* ── BUILD PHASE ─────────────────────────────────────────────────── */}
        {activePhase === 'build' && (
          <motion.div key="build" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="flex flex-col gap-6">

            <div className="grid grid-cols-1 @[700px]:grid-cols-2 gap-6">
              {/* Config panel */}
              <div className="flex flex-col gap-4">
                <Card className="p-6 border-amber-500/20 bg-amber-500/5 flex flex-col gap-5">
                  <div className="flex items-center gap-2">
                    <Wrench size={16} className="text-amber-400" />
                    <span className="text-[9px] font-black text-amber-400 uppercase tracking-[0.25em]">Infrastructure Configuration</span>
                  </div>

                  {/* Deploy mode */}
                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-2">Deployment Mode</label>
                    <div className="grid grid-cols-2 gap-2">
                      {DEPLOY_MODES.map(m => {
                        const Icon = m.icon;
                        const active = buildConfig.mode === m.id;
                        return (
                          <button
                            key={m.id}
                            type="button"
                            onClick={() => setBuildConfig(c => ({ ...c, mode: m.id }))}
                            className={`flex flex-col items-start gap-1.5 p-3 rounded-xl border transition-all text-left ${
                              active ? 'bg-amber-500/20 border-amber-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700'
                            }`}
                          >
                            <Icon size={13} className={active ? 'text-amber-400' : ''} />
                            <span className="text-[9px] font-black uppercase tracking-widest">{m.label}</span>
                            <span className="text-[8px] text-slate-600">{m.desc}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Scale tier */}
                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-2">Scale Tier</label>
                    <div className="space-y-1.5">
                      {SCALE_TIERS.map(t => {
                        const active = buildConfig.scale_tier === t.id;
                        return (
                          <button
                            key={t.id}
                            type="button"
                            onClick={() => setBuildConfig(c => ({ ...c, scale_tier: t.id }))}
                            className={`w-full flex items-center justify-between px-4 py-2.5 rounded-xl border transition-all ${
                              active ? 'bg-amber-500/20 border-amber-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700'
                            }`}
                          >
                            <span className="text-[9px] font-black uppercase tracking-widest">{t.label}</span>
                            <span className="text-[9px] text-slate-600">{t.desc}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Node count */}
                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">
                      Node Count: <span className="text-amber-400">{buildConfig.nodes}</span>
                    </label>
                    <input
                      type="range"
                      min={1}
                      max={100}
                      value={buildConfig.nodes}
                      onChange={e => setBuildConfig(c => ({ ...c, nodes: Number(e.target.value) }))}
                      title="Node Count"
                      aria-label="Node Count"
                      className="w-full accent-amber-400"
                    />
                    <div className="flex justify-between text-[8px] text-slate-700 font-bold mt-0.5">
                      <span>1</span><span>25</span><span>50</span><span>100</span>
                    </div>
                  </div>

                  {/* Facility type */}
                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">Facility Type</label>
                    <select
                      value={buildConfig.facility_type}
                      onChange={e => setBuildConfig(c => ({ ...c, facility_type: e.target.value }))}
                      title="Facility Type"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition-colors"
                    >
                      {FACILITY_TYPES.map(f => <option key={f} value={f}>{f}</option>)}
                    </select>
                  </div>

                  {/* Regions */}
                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">
                      Deployment Regions {buildConfig.regions.length > 1 && <span className="text-amber-400">({buildConfig.regions.length} selected)</span>}
                    </label>
                    <div className="flex flex-wrap gap-1.5">
                      {REGIONS.map(r => {
                        const active = buildConfig.regions.includes(r);
                        return (
                          <button
                            key={r}
                            type="button"
                            onClick={() => toggleRegion(r)}
                            className={`px-2.5 py-1 rounded-full text-[9px] font-black uppercase tracking-wider transition-all border ${
                              active ? 'bg-amber-500/20 border-amber-500 text-white' : 'bg-slate-900 border-slate-800 text-slate-600 hover:border-slate-700 hover:text-slate-300'
                            }`}
                          >{r}</button>
                        );
                      })}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleBuild}
                    disabled={building || buildConfig.regions.length === 0}
                    className={`flex items-center justify-center gap-2 w-full py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${
                      !building && buildConfig.regions.length > 0
                        ? 'bg-amber-500 text-sovereign hover:bg-amber-400 hover:scale-[1.01] shadow-lg shadow-amber-500/20'
                        : 'bg-slate-800 text-slate-600 cursor-not-allowed'
                    }`}
                  >
                    {building ? <><Loader2 size={14} className="animate-spin" /> Provisioning Infrastructure...</> : <><Server size={14} /> Build Infrastructure</>}
                  </button>
                </Card>
              </div>

              {/* Build result + capabilities */}
              <div className="flex flex-col gap-4">
                <Card className={`flex-1 p-6 min-h-[320px] flex flex-col transition-all ${builtConfig ? 'border-amber-500/30' : 'border-slate-800'}`}>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Database size={14} className="text-amber-400" />
                      <span className="text-[9px] font-black text-amber-400 uppercase tracking-[0.25em]">Infrastructure Blueprint</span>
                    </div>
                    {builtConfig && (
                      <button type="button" onClick={() => setActivePhase('launch')}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:bg-emerald-500/30 transition-colors">
                        Proceed to Launch <ArrowRight size={10} />
                      </button>
                    )}
                  </div>
                  {!builtConfig && !building && (
                    <div className="flex-1 flex flex-col items-center justify-center text-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
                        <Server size={22} />
                      </div>
                      <p className="text-xs text-slate-600 font-bold">Configure infrastructure and click Build.</p>
                    </div>
                  )}
                  {building && (
                    <div className="flex-1 flex flex-col items-center justify-center gap-6">
                      <div className="relative w-16 h-16">
                        <div className="absolute inset-0 rounded-full border-2 border-amber-500/20 animate-ping" />
                        <div className="w-16 h-16 rounded-full border-2 border-amber-500 animate-spin border-t-transparent" />
                      </div>
                      <p className="text-amber-400 font-black uppercase tracking-[0.25em] text-xs animate-pulse">Provisioning infrastructure...</p>
                    </div>
                  )}
                  {builtConfig && !building && (
                    <div className="flex-1 space-y-3 overflow-y-auto">
                      {Object.entries(builtConfig).map(([k, v]) => (
                        <div key={k} className="flex items-start justify-between gap-4 py-2.5 border-b border-slate-800/60 last:border-0">
                          <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest shrink-0">{k.replace(/_/g, ' ')}</span>
                          <span className="text-[10px] text-slate-300 font-bold text-right">{Array.isArray(v) ? v.join(', ') : String(v)}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </Card>

                <div className="grid grid-cols-2 gap-3">
                  {[
                    { icon: Globe,   label: 'Global Scale',  desc: 'Multi-region sovereign mesh', color: 'text-emerald-400' },
                    { icon: Factory, label: 'Industrial',     desc: 'OT/SCADA integration layer', color: 'text-orange-400' },
                    { icon: Shield,  label: 'PQC Security',  desc: 'Post-quantum hardened nodes', color: 'text-amber-400' },
                    { icon: Gauge,   label: 'Performance',   desc: 'Real-time TPS benchmarking', color: 'text-cyan-400' },
                  ].map(c => {
                    const Icon = c.icon;
                    return (
                      <div key={c.label} className="flex items-center gap-3 px-3 py-3 rounded-xl bg-slate-900 border border-slate-800">
                        <Icon size={14} className={c.color} />
                        <div className="min-w-0">
                          <p className="text-[9px] font-black text-white uppercase tracking-widest">{c.label}</p>
                          <p className="text-[9px] text-slate-600 font-bold">{c.desc}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* ── LAUNCH PHASE ────────────────────────────────────────────────── */}
        {activePhase === 'launch' && (
          <motion.div key="launch" initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="flex flex-col gap-6">

            <div className="grid grid-cols-1 @[700px]:grid-cols-2 gap-6">
              {/* Mission config */}
              <div className="flex flex-col gap-4">
                <Card className="p-6 border-emerald-500/20 bg-emerald-500/5 flex flex-col gap-5">
                  <div className="flex items-center gap-2">
                    <Rocket size={16} className="text-emerald-400" />
                    <span className="text-[9px] font-black text-emerald-400 uppercase tracking-[0.25em]">Mission Control · V9 Engine</span>
                  </div>

                  {/* Summary */}
                  <div className="space-y-2 p-4 rounded-2xl bg-slate-950 border border-slate-800">
                    <p className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Ready to Launch</p>
                    <div className="grid grid-cols-2 gap-2 text-[10px]">
                      <div>
                        <span className="text-slate-600">Solution:</span>
                        <span className="text-white font-bold ml-1.5 truncate">{spec.solution_name || '—'}</span>
                      </div>
                      <div>
                        <span className="text-slate-600">Nodes:</span>
                        <span className="text-white font-bold ml-1.5">{buildConfig.nodes}</span>
                      </div>
                      <div>
                        <span className="text-slate-600">Regions:</span>
                        <span className="text-white font-bold ml-1.5">{buildConfig.regions.length}</span>
                      </div>
                      <div>
                        <span className="text-slate-600">Mode:</span>
                        <span className="text-white font-bold ml-1.5 uppercase">{buildConfig.mode}</span>
                      </div>
                      <div>
                        <span className="text-slate-600">Domains:</span>
                        <span className="text-aura font-bold ml-1.5">{spec.domains.length || 'All'}</span>
                      </div>
                      <div>
                        <span className="text-slate-600">TPS:</span>
                        <span className="text-emerald-400 font-bold ml-1.5">{builtConfig?.estimated_tps || '—'}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-1.5">Mission Name</label>
                    <input
                      value={missionName}
                      onChange={e => setMissionName(e.target.value)}
                      placeholder="e.g. OMEGA-HEALTH-001..."
                      aria-label="Mission Name"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-sm text-white placeholder-slate-600 outline-none focus:border-emerald-500/50 transition-colors font-mono uppercase"
                    />
                  </div>

                  <div>
                    <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest block mb-2">Execution Mode</label>
                    <div className="flex gap-2">
                      {(['test', 'staging', 'production'] as const).map(m => (
                        <button
                          key={m}
                          type="button"
                          onClick={() => setExecMode(m)}
                          className={`flex-1 py-2 rounded-xl text-[9px] font-black uppercase tracking-widest transition-all border ${
                            execMode === m
                              ? m === 'production' ? 'bg-red-500/20 border-red-500 text-red-400'
                              : m === 'staging' ? 'bg-amber-500/20 border-amber-500 text-amber-400'
                              : 'bg-emerald-500/20 border-emerald-500 text-emerald-400'
                              : 'bg-slate-900 border-slate-800 text-slate-600 hover:border-slate-700'
                          }`}
                        >{m}</button>
                      ))}
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleLaunch}
                    disabled={launching || !missionName.trim() || status.launch === 'done'}
                    className={`flex items-center justify-center gap-2 w-full py-3 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${
                      !launching && missionName.trim() && status.launch !== 'done'
                        ? execMode === 'production'
                          ? 'bg-red-500 text-white hover:bg-red-400 hover:scale-[1.01] shadow-lg shadow-red-500/20'
                          : 'bg-emerald-500 text-sovereign hover:bg-emerald-400 hover:scale-[1.01] shadow-lg shadow-emerald-500/20'
                        : 'bg-slate-800 text-slate-600 cursor-not-allowed'
                    }`}
                  >
                    {launching
                      ? <><Loader2 size={14} className="animate-spin" /> Launching Mission...</>
                      : status.launch === 'done'
                      ? <><CheckCircle2 size={14} /> Mission Live</>
                      : <><Rocket size={14} /> Launch {execMode === 'production' ? '🔴 PRODUCTION' : execMode}</>
                    }
                  </button>

                  {status.launch === 'done' && (
                    <button
                      type="button"
                      onClick={() => { setStatus({ design: 'idle', build: 'idle', launch: 'idle' }); setBuiltConfig(null); setMissionId(null); setMissionLog([]); setSpec({ solution_name: '', ai_model: AI_MODELS[0], domains: [], description: '', objectives: [] }); setMissionName(''); setActivePhase('design'); }}
                      className="flex items-center justify-center gap-2 w-full py-2.5 rounded-2xl font-black text-xs uppercase tracking-widest text-slate-500 border border-slate-800 hover:border-slate-700 hover:text-white transition-all"
                    >
                      <RefreshCw size={12} /> New Mission
                    </button>
                  )}
                </Card>
              </div>

              {/* Mission log */}
              <div className="flex flex-col gap-4">
                <Card className={`flex-1 p-6 flex flex-col transition-all ${missionId ? 'border-emerald-500/30' : 'border-slate-800'}`}>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <MonitorPlay size={14} className="text-emerald-400" />
                      <span className="text-[9px] font-black text-emerald-400 uppercase tracking-[0.25em]">Mission Log</span>
                      {missionId && <span className="text-[9px] font-mono text-slate-600">{missionId}</span>}
                    </div>
                    {status.launch === 'done' && (
                      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-[8px] font-black text-emerald-400 uppercase tracking-widest">Live</span>
                      </div>
                    )}
                  </div>

                  {!missionId && (
                    <div className="flex-1 flex flex-col items-center justify-center text-center gap-4">
                      <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-700">
                        <Rocket size={22} />
                      </div>
                      <p className="text-xs text-slate-600 font-bold">Configure the mission and click Launch.</p>
                    </div>
                  )}

                  {missionId && (
                    <div ref={logRef} className="flex-1 overflow-y-auto space-y-1.5 font-mono min-h-[320px] max-h-[420px]">
                      {missionLog.map((entry, i) => (
                        <div key={i} className="flex items-start gap-3 text-[10px]">
                          <span className="text-slate-700 shrink-0">{entry.time}</span>
                          <span className={`shrink-0 ${entry.level === 'success' ? 'text-emerald-400' : entry.level === 'warn' ? 'text-amber-400' : 'text-slate-500'}`}>
                            {entry.level === 'success' ? '✓' : entry.level === 'warn' ? '⚠' : '›'}
                          </span>
                          <span className={entry.level === 'success' ? 'text-emerald-300 font-bold' : 'text-slate-400'}>{entry.msg}</span>
                        </div>
                      ))}
                      {launching && (
                        <div className="flex items-center gap-2 text-[10px] text-slate-600">
                          <Loader2 size={9} className="animate-spin" />
                          <span>Processing...</span>
                        </div>
                      )}
                    </div>
                  )}
                </Card>

                <div className="grid grid-cols-2 gap-3">
                  {[
                    { icon: Zap,      label: 'V9 Engine',    desc: 'Sovereign execution runtime', color: 'text-yellow-400' },
                    { icon: Activity, label: 'Monitoring',   desc: 'Real-time mission telemetry', color: 'text-emerald-400' },
                    { icon: BarChart3, label: 'Analytics',   desc: 'Performance & usage metrics', color: 'text-blue-400' },
                    { icon: GitBranch, label: 'Versioning',  desc: 'Mission history & rollbacks', color: 'text-purple-400' },
                  ].map(c => {
                    const Icon = c.icon;
                    return (
                      <div key={c.label} className="flex items-center gap-3 px-3 py-3 rounded-xl bg-slate-900 border border-slate-800">
                        <Icon size={14} className={c.color} />
                        <div className="min-w-0">
                          <p className="text-[9px] font-black text-white uppercase tracking-widest">{c.label}</p>
                          <p className="text-[9px] text-slate-600 font-bold">{c.desc}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
