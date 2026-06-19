import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Activity, Brain, Shield, Zap, Heart, Wind, Cpu, Dna,
  RefreshCw, AlertTriangle, CheckCircle2, Circle, Wifi,
  TrendingUp, Building2, GitMerge, Clock, Radio,
  ChevronRight, Loader2, Play, Settings,
  type LucideIcon
} from 'lucide-react';

// ── Type definitions ──────────────────────────────────────────────────────────

interface OrganismStatus {
  organism: string;
  version: string;
  timestamp: string;
  composite_health: number;
  mode: 'FULL_POWER' | 'NOMINAL' | 'DEGRADED' | 'EMERGENCY';
  health_summary: string;
  systems: {
    immune:        { health: number; threat_level: string; errors_in_window: number; active_responses: number; hot_endpoint?: string };
    nervous:       { arousal_state: string; signal_rate_per_second: number; signals_last_60s: number; by_type: Record<string,number>; total_signals: Record<string,number>; reflex_arcs: number };
    self_healing:  { overall_health: number; open_circuits: number; recent_events: unknown[] };
    metabolic:     { atp_ratio: number };
    circadian:     { cycle: string; is_peak_focus: boolean };
    genome:        { total_genomes: number };
    reconfiguration: { features_active: number; domains_enabled: number; rpm_limit: number; preferred_provider: string };
  };
  operations: {
    lifecycle:     { total_projects: number; by_stage: Record<string,number>; running: number; commercialisation_rate: number; pipeline_health: string };
    vsb:           { total: number; active: number; domains: string[] };
    change_control: { pending: number; approved: number; implemented: number };
  };
  recommended: { temperature: string; should_throttle: boolean; max_parallel_agents: number; priority: string };
}

interface Signal {
  type: string;
  source: string;
  payload: string;
  intensity: number;
  ts: number;
}

interface SignalFeed {
  arousal_state: string;
  signal_rate_per_second: number;
  signals: Signal[];
  count: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const MODE_META: Record<string, { label: string; color: string; glow: string }> = {
  FULL_POWER: { label: 'Full Power',  color: 'text-green-400',  glow: 'shadow-green-500/30' },
  NOMINAL:    { label: 'Nominal',     color: 'text-blue-400',   glow: 'shadow-blue-500/30'  },
  DEGRADED:   { label: 'Degraded',    color: 'text-yellow-400', glow: 'shadow-yellow-500/30'},
  EMERGENCY:  { label: 'Emergency',   color: 'text-red-400',    glow: 'shadow-red-500/40'   },
};

const THREAT_COLOR: Record<string, string> = {
  NONE:     'text-green-400',
  LOW:      'text-blue-400',
  MODERATE: 'text-yellow-400',
  HIGH:     'text-orange-400',
  CRITICAL: 'text-red-500',
};

const AROUSAL_COLOR: Record<string, string> = {
  DORMANT:     'text-slate-400',
  RESTING:     'text-blue-400',
  ALERT:       'text-yellow-400',
  HYPERACTIVE: 'text-red-400',
};

const SIGNAL_COLOR: Record<string, string> = {
  sensory:   'bg-blue-500/20 text-blue-300 border-blue-500/30',
  motor:     'bg-green-500/20 text-green-300 border-green-500/30',
  reflex:    'bg-red-500/20 text-red-300 border-red-500/30',
  cognitive: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
};

function HealthBar({ value, className = '' }: { value: number; className?: string }) {
  const pct = Math.round(value * 100);
  const color = value >= 0.8 ? 'bg-green-400' : value >= 0.5 ? 'bg-blue-400' : value >= 0.2 ? 'bg-yellow-400' : 'bg-red-500';
  return (
    <div className={`h-2 rounded-full bg-white/10 overflow-hidden ${className}`}>
      <motion.div
        className={`h-full rounded-full ${color}`}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      />
    </div>
  );
}

function SystemCard({
  icon: Icon, title, children, accent = 'border-white/10'
}: {
  icon: LucideIcon;
  title: string;
  children: React.ReactNode;
  accent?: string;
}) {
  return (
    <div className={`bg-white/5 border ${accent} rounded-xl p-4 flex flex-col gap-3`}>
      <div className="flex items-center gap-2 text-sm font-semibold text-white/70 uppercase tracking-wider">
        <Icon size={14} className="opacity-60" />
        {title}
      </div>
      {children}
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export const OrganismDashboard: React.FC = () => {
  const [status, setStatus] = useState<OrganismStatus | null>(null);
  const [signals, setSignals] = useState<SignalFeed | null>(null);
  const [loading, setLoading] = useState(true);
  const [homeostasisLoading, setHomeostasisLoading] = useState(false);
  const [homeostasisResult, setHomeostasisResult] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('');

  const loadAll = useCallback(() => {
    Promise.all([
      axios.get<OrganismStatus>('/api/v1/organism/status', { validateStatus: () => true }),
      axios.get<SignalFeed>('/api/v1/organism/signals?n=30', { validateStatus: () => true }),
    ]).then(([statusRes, sigRes]) => {
      if (statusRes.status === 200 && statusRes.data) setStatus(statusRes.data);
      if (sigRes.status === 200 && sigRes.data) setSignals(sigRes.data);
      setLastUpdated(new Date().toLocaleTimeString());
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadAll();
    const t = setInterval(loadAll, 10000);
    return () => clearInterval(t);
  }, [loadAll]);

  const triggerHomeostasis = async () => {
    setHomeostasisLoading(true);
    setHomeostasisResult(null);
    try {
      const res = await axios.post('/api/v1/organism/homeostasis', { reason: 'manual_dashboard' });
      const d = res.data;
      const adj = d.adjustments_made?.length ?? 0;
      setHomeostasisResult(
        `Homeostasis complete. ${adj} adjustment${adj !== 1 ? 's' : ''} made. Mode: ${d.organism_mode}.` +
        (d.ai_recommendation ? `\n\n${d.ai_recommendation}` : '')
      );
    } catch {
      setHomeostasisResult('Homeostasis call failed — check organism status.');
    } finally {
      setHomeostasisLoading(false);
      loadAll();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-white/40">
        <Loader2 size={28} className="animate-spin mr-3" />
        <span className="font-mono text-sm tracking-widest uppercase">Connecting to IDBO Organism...</span>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="p-8 text-red-400 font-mono">
        Organism status unavailable — backend may be starting up.
      </div>
    );
  }

  const mode = MODE_META[status.mode] ?? MODE_META.NOMINAL;
  const { systems, operations, recommended } = status;

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">

      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center gap-3">
            <Wifi size={22} className="text-green-400 animate-pulse" />
            IDBO Organism
          </h1>
          <p className="text-sm text-white/40 mt-1 font-mono">
            {status.organism} v{status.version} &nbsp;·&nbsp; Updated {lastUpdated}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={loadAll}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-white/50 hover:text-white/80 transition-colors"
            title="Refresh"
          >
            <RefreshCw size={15} />
          </button>
          <button
            onClick={triggerHomeostasis}
            disabled={homeostasisLoading}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-purple-600/30 hover:bg-purple-600/50 text-purple-300 border border-purple-500/30 text-sm font-semibold transition-all disabled:opacity-50"
          >
            {homeostasisLoading ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
            Trigger Homeostasis
          </button>
        </div>
      </div>

      {/* ── Composite Health Banner ─────────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className={`bg-white/5 border border-white/10 rounded-2xl p-5 shadow-lg ${mode.glow}`}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-3">
            <span className={`text-lg font-black uppercase tracking-widest ${mode.color}`}>
              {mode.label}
            </span>
            <span className="text-white/30 text-sm">|</span>
            <span className="text-white/60 text-sm font-mono">
              {systems.circadian.cycle.replace('_', ' ')}
              {systems.circadian.is_peak_focus && (
                <span className="ml-2 text-green-400 text-xs">PEAK FOCUS</span>
              )}
            </span>
          </div>
          <span className="text-3xl font-black text-white">
            {Math.round(status.composite_health * 100)}<span className="text-sm font-normal text-white/40">%</span>
          </span>
        </div>
        <HealthBar value={status.composite_health} />
        <p className="text-xs text-white/40 mt-2 font-mono">{status.health_summary}</p>

        {/* Recommended behaviour chips */}
        <div className="flex gap-2 mt-3 flex-wrap">
          <span className={`px-2 py-0.5 rounded text-xs font-mono border ${recommended.should_throttle ? 'bg-red-500/15 text-red-300 border-red-500/30' : 'bg-green-500/15 text-green-300 border-green-500/30'}`}>
            {recommended.should_throttle ? 'THROTTLE' : 'FULL THROUGHPUT'}
          </span>
          <span className="px-2 py-0.5 rounded text-xs font-mono bg-white/5 text-white/50 border border-white/10">
            {recommended.max_parallel_agents} parallel agents
          </span>
          <span className="px-2 py-0.5 rounded text-xs font-mono bg-white/5 text-white/50 border border-white/10">
            temp: {recommended.temperature}
          </span>
          <span className="px-2 py-0.5 rounded text-xs font-mono bg-white/5 text-white/50 border border-white/10">
            {systems.reconfiguration.preferred_provider} provider
          </span>
          <span className="px-2 py-0.5 rounded text-xs font-mono bg-white/5 text-white/50 border border-white/10">
            {systems.reconfiguration.rpm_limit} RPM
          </span>
        </div>
      </motion.div>

      {/* ── Homeostasis result ──────────────────────────────────────────── */}
      <AnimatePresence>
        {homeostasisResult && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-purple-900/20 border border-purple-500/30 rounded-xl p-4 text-sm text-purple-200 font-mono whitespace-pre-wrap"
          >
            {homeostasisResult}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── Biomimetic Systems Grid ─────────────────────────────────────── */}
      <div>
        <h2 className="text-xs uppercase tracking-widest text-white/30 font-semibold mb-3">Biomimetic Systems</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">

          {/* Immune */}
          <SystemCard icon={Shield} title="Immune" accent={systems.immune.health < 0.5 ? 'border-red-500/30' : 'border-white/10'}>
            <div className="text-2xl font-black text-white">{Math.round(systems.immune.health * 100)}%</div>
            <HealthBar value={systems.immune.health} />
            <div className="flex justify-between text-xs text-white/40 font-mono">
              <span className={THREAT_COLOR[systems.immune.threat_level] ?? 'text-white/40'}>
                {systems.immune.threat_level}
              </span>
              <span>{systems.immune.errors_in_window} errors</span>
            </div>
          </SystemCard>

          {/* Nervous */}
          <SystemCard icon={Brain} title="Nervous" accent="border-white/10">
            <div className="flex items-end gap-1">
              <span className="text-2xl font-black text-white">{systems.nervous.signals_last_60s}</span>
              <span className="text-xs text-white/40 mb-1">signals/60s</span>
            </div>
            <div className="text-xs font-mono space-y-0.5">
              <div className={`${AROUSAL_COLOR[systems.nervous.arousal_state] ?? 'text-white/50'} font-semibold`}>
                {systems.nervous.arousal_state}
              </div>
              <div className="text-white/30">{systems.nervous.signal_rate_per_second.toFixed(2)} sig/s</div>
              <div className="text-white/30">{systems.nervous.reflex_arcs} reflex arcs</div>
            </div>
          </SystemCard>

          {/* Self-Healing */}
          <SystemCard icon={Heart} title="Self-Healing" accent={systems.self_healing.open_circuits > 0 ? 'border-yellow-500/30' : 'border-white/10'}>
            <div className="text-2xl font-black text-white">{Math.round(systems.self_healing.overall_health * 100)}%</div>
            <HealthBar value={systems.self_healing.overall_health} />
            <div className="text-xs font-mono text-white/40">
              {systems.self_healing.open_circuits === 0
                ? <span className="text-green-400">All circuits closed</span>
                : <span className="text-yellow-400">{systems.self_healing.open_circuits} circuit{systems.self_healing.open_circuits !== 1 ? 's' : ''} open</span>
              }
            </div>
          </SystemCard>

          {/* Metabolic */}
          <SystemCard icon={Zap} title="Metabolic" accent="border-white/10">
            <div className="flex items-end gap-1">
              <span className="text-2xl font-black text-white">{Math.round(systems.metabolic.atp_ratio * 100)}%</span>
            </div>
            <HealthBar value={systems.metabolic.atp_ratio} />
            <div className="text-xs font-mono text-white/30">ATP ratio</div>
          </SystemCard>

          {/* Circadian */}
          <SystemCard icon={Clock} title="Circadian" accent="border-white/10">
            <div className="text-sm font-black text-white">{systems.circadian.cycle.replace(/_/g, ' ')}</div>
            <div className={`text-xs font-mono ${systems.circadian.is_peak_focus ? 'text-green-400' : 'text-white/40'}`}>
              {systems.circadian.is_peak_focus ? 'Peak focus window' : 'Off-peak window'}
            </div>
          </SystemCard>

          {/* Genome */}
          <SystemCard icon={Dna} title="Genome" accent="border-white/10">
            <div className="text-2xl font-black text-white">{systems.genome.total_genomes}</div>
            <div className="text-xs font-mono text-white/30">encoded genomes</div>
          </SystemCard>

          {/* Reconfiguration */}
          <SystemCard icon={Settings} title="Reconfig" accent="border-white/10">
            <div className="text-xs font-mono space-y-1">
              <div className="flex justify-between">
                <span className="text-white/40">Features active</span>
                <span className="text-white">{systems.reconfiguration.features_active}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/40">Domains on</span>
                <span className="text-white">{systems.reconfiguration.domains_enabled}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/40">RPM limit</span>
                <span className="text-white">{systems.reconfiguration.rpm_limit}</span>
              </div>
            </div>
          </SystemCard>

          {/* Nervous signal types */}
          <SystemCard icon={Activity} title="Signal Types" accent="border-white/10">
            {Object.entries(systems.nervous.by_type).length > 0 ? (
              <div className="text-xs font-mono space-y-1">
                {Object.entries(systems.nervous.by_type).map(([type, count]) => (
                  <div key={type} className="flex justify-between">
                    <span className={SIGNAL_COLOR[type]?.split(' ')[1] ?? 'text-white/40'}>{type}</span>
                    <span className="text-white">{count as number}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-xs text-white/30 font-mono">No signals yet</div>
            )}
          </SystemCard>

        </div>
      </div>

      {/* ── Operations: Lifecycle + VSB + CCA ──────────────────────────── */}
      <div>
        <h2 className="text-xs uppercase tracking-widest text-white/30 font-semibold mb-3">Operations</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">

          {/* Lifecycle pipeline */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs font-semibold text-white/60 uppercase tracking-wider mb-4">
              <TrendingUp size={13} className="opacity-60" />
              Concept → Commercialise
            </div>
            <div className="flex items-center gap-1 mb-3">
              {(['concept', 'prototype', 'commercialise'] as const).map((stage, i) => {
                const count = operations.lifecycle.by_stage[stage] ?? 0;
                return (
                  <React.Fragment key={stage}>
                    {i > 0 && <ChevronRight size={12} className="text-white/20 flex-shrink-0" />}
                    <div className={`flex-1 text-center p-2 rounded-lg ${count > 0 ? 'bg-blue-500/20 border border-blue-500/30' : 'bg-white/3 border border-white/5'}`}>
                      <div className="text-lg font-black text-white">{count}</div>
                      <div className="text-xs text-white/40 capitalize">{stage}</div>
                    </div>
                  </React.Fragment>
                );
              })}
            </div>
            <div className="flex justify-between text-xs font-mono text-white/40">
              <span>{operations.lifecycle.total_projects} total</span>
              <span className={`${operations.lifecycle.pipeline_health === 'FLOURISHING' ? 'text-green-400' : 'text-white/40'}`}>
                {operations.lifecycle.pipeline_health}
              </span>
              <span>{Math.round(operations.lifecycle.commercialisation_rate * 100)}% commercial</span>
            </div>
          </div>

          {/* VSB entities */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs font-semibold text-white/60 uppercase tracking-wider mb-4">
              <Building2 size={13} className="opacity-60" />
              VSB Entities
            </div>
            <div className="flex gap-4 mb-3">
              <div className="text-center">
                <div className="text-3xl font-black text-white">{operations.vsb.total}</div>
                <div className="text-xs text-white/40">total</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-black text-green-400">{operations.vsb.active}</div>
                <div className="text-xs text-white/40">active</div>
              </div>
            </div>
            {operations.vsb.domains.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {operations.vsb.domains.slice(0, 6).map(d => (
                  <span key={d} className="px-2 py-0.5 rounded text-xs bg-blue-500/15 text-blue-300 border border-blue-500/20 font-mono">
                    {d}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Change Control Agency */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-4">
            <div className="flex items-center gap-2 text-xs font-semibold text-white/60 uppercase tracking-wider mb-4">
              <GitMerge size={13} className="opacity-60" />
              Change Control Agency
            </div>
            <div className="grid grid-cols-3 gap-2 text-center">
              {[
                { label: 'Pending',     count: operations.change_control.pending,     color: 'text-yellow-400' },
                { label: 'Approved',    count: operations.change_control.approved,    color: 'text-green-400'  },
                { label: 'Implemented', count: operations.change_control.implemented, color: 'text-blue-400'   },
              ].map(({ label, count, color }) => (
                <div key={label} className="bg-white/5 rounded-lg p-2">
                  <div className={`text-2xl font-black ${color}`}>{count}</div>
                  <div className="text-xs text-white/40">{label}</div>
                </div>
              ))}
            </div>
            {operations.change_control.pending > 0 && (
              <div className="mt-3 flex items-center gap-2 text-xs text-yellow-300 font-mono bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-2">
                <AlertTriangle size={12} />
                {operations.change_control.pending} change{operations.change_control.pending !== 1 ? 's' : ''} awaiting review
              </div>
            )}
          </div>

        </div>
      </div>

      {/* ── Signal Feed ────────────────────────────────────────────────── */}
      {signals && signals.signals.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xs uppercase tracking-widest text-white/30 font-semibold flex items-center gap-2">
              <Radio size={12} className="opacity-60 animate-pulse" />
              Nervous System Signal Feed
            </h2>
            <span className={`text-xs font-mono ${AROUSAL_COLOR[signals.arousal_state] ?? 'text-white/40'}`}>
              {signals.arousal_state} &middot; {signals.signal_rate_per_second.toFixed(2)} sig/s
            </span>
          </div>
          <div className="bg-white/3 border border-white/8 rounded-xl p-3 max-h-52 overflow-y-auto space-y-1">
            {signals.signals.slice(0, 25).map((sig, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.02 }}
                className="flex items-center gap-2 text-xs font-mono"
              >
                <span className={`px-1.5 py-0.5 rounded border text-[10px] uppercase ${SIGNAL_COLOR[sig.type] ?? 'bg-white/5 text-white/40 border-white/10'}`}>
                  {sig.type}
                </span>
                <span className="text-white/30 flex-shrink-0 w-32 truncate">{sig.source}</span>
                <span className="text-white/50 flex-1 truncate">{sig.payload}</span>
                <span className="text-white/20 flex-shrink-0">
                  {(sig.intensity * 100).toFixed(0)}%
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};

export default OrganismDashboard;
