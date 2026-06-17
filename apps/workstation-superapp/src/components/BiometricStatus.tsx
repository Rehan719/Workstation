/**
 * BiometricStatus — a unified ECG-style biomimetic status widget.
 *
 * Three dots correspond to three real biomimetic rhythms, each with a
 * naturally-derived colour and pulse frequency:
 *
 *   Dot 1 — Cardiovascular  (heartbeat, 60–90 BPM ≈ 0.7–1.0 s per cycle)
 *            green  = healthy flow (>80%), teal = working (40–80%), red = stressed (<40%)
 *
 *   Dot 2 — Cognition       (brainwave rhythm, spaced 300 ms after heartbeat)
 *            violet = FLOURISHING, blue = STABLE, amber = STRESSED
 *
 *   Dot 3 — Communication   (neurotransmitter signal, spaced 600 ms after heartbeat)
 *            cyan  = Dopamine (novelty / reward)
 *            green = Serotonin (stability / focus)
 *            pink  = Oxytocin  (connection / urgency)
 *
 *   ECG icon — Activity (lucide) whose pulse speed mirrors the circadian phase:
 *            ACTIVE_FOCUS 0.8 s | ACTIVE_REST 2.5 s
 *            MAINTENANCE_FOCUS 1.2 s | MAINTENANCE_REST 4 s
 *
 * compact=true  → tight horizontal row of dots + icon (used when the fourth
 *                 column panel is collapsed to its button-rail width)
 * compact=false → badge row + system-state label below (used when expanded)
 */

import React from 'react';
import { Activity } from 'lucide-react';
import type {
  WorkstationBiometrics,
  CircadianCycle,
  CognitionState,
  NeurotransmitterState,
  SystemState,
} from '../hooks/useWorkstationBiometrics';

interface BiometricStatusProps {
  biometrics: WorkstationBiometrics;
  compact?: boolean;
}

// ─── biomimetic mappings ──────────────────────────────────────────────────────

// Circadian cycle → ECG pulse duration (mirrors ultradian rhythm)
function ecgDuration(cycle: CircadianCycle): string {
  switch (cycle) {
    case 'ACTIVE_FOCUS':      return '[animation-duration:0.8s]';
    case 'ACTIVE_REST':       return '[animation-duration:2.5s]';
    case 'MAINTENANCE_FOCUS': return '[animation-duration:1.2s]';
    case 'MAINTENANCE_REST':  return '[animation-duration:4s]';
  }
}

// Cardiovascular resource flow → heartbeat dot colour
function cardioClass(flow: number): string {
  if (flow > 80) return 'bg-emerald-500';   // healthy — green
  if (flow > 40) return 'bg-aura';           // working — teal
  return 'bg-vital';                          // stressed — red
}

// Cardiovascular flow → heartbeat pulse speed (high flow = faster pump)
function cardioDuration(flow: number): string {
  if (flow > 80) return '[animation-duration:0.8s]';   // 75 BPM
  if (flow > 40) return '[animation-duration:1.0s]';   // ~60 BPM
  return '[animation-duration:0.5s]';                   // stressed, rapid
}

// Cognition motivational state → brainwave dot colour
function cognitionClass(state: CognitionState): string {
  switch (state) {
    case 'FLOURISHING': return 'bg-violet-500';
    case 'STABLE':      return 'bg-blue-400';
    case 'STRESSED':    return 'bg-amber-500';
  }
}

// Cognition state → brainwave rhythm (alpha ≈ 1.5 s, theta ≈ 0.5 s, beta ≈ 0.25 s)
function cognitionDuration(state: CognitionState): string {
  switch (state) {
    case 'FLOURISHING': return '[animation-duration:0.5s]';  // beta — high engagement
    case 'STABLE':      return '[animation-duration:1.5s]';  // alpha — calm focus
    case 'STRESSED':    return '[animation-duration:0.3s]';  // high-beta — anxious
  }
}

// Neurotransmitter → communication dot colour
function commClass(nt: NeurotransmitterState): string {
  switch (nt) {
    case 'Dopamine':  return 'bg-cyan-400';   // novelty / reward
    case 'Serotonin': return 'bg-green-400';  // stability / focus
    case 'Oxytocin':  return 'bg-pink-400';   // connection / urgency
  }
}

// Communication activity → signal pulse speed
function commDuration(isActive: boolean, nt: NeurotransmitterState): string {
  if (!isActive) return '[animation-duration:4s]';              // idle — very slow
  if (nt === 'Oxytocin') return '[animation-duration:0.4s]';   // urgent — rapid
  if (nt === 'Dopamine') return '[animation-duration:0.6s]';   // active — fast
  return '[animation-duration:1.2s]';                           // Serotonin — steady
}

// ECG icon colour follows the dominant signal
function ecgColor(b: WorkstationBiometrics): string {
  if (b.communication.is_active) {
    switch (b.communication.neurotransmitter) {
      case 'Dopamine':  return 'text-cyan-400';
      case 'Oxytocin':  return 'text-pink-400';
      case 'Serotonin': return 'text-green-400';
    }
  }
  switch (b.cognition.state) {
    case 'FLOURISHING': return 'text-violet-400';
    case 'STRESSED':    return 'text-amber-400';
    default:            return 'text-emerald-400';
  }
}

// Derived system state → short display label
function stateLabel(s: SystemState): string {
  switch (s) {
    case 'WORKING':       return 'Work';
    case 'COMMUNICATING': return 'Comm';
    case 'RESTING':       return 'Rest';
    case 'MAINTENANCE':   return 'Maint';
    case 'IDLE':          return 'Idle';
  }
}

// ─── component ────────────────────────────────────────────────────────────────

export const BiometricStatus: React.FC<BiometricStatusProps> = ({
  biometrics: b,
  compact = false,
}) => {
  const cardioCol  = cardioClass(b.cardiovascular.resource_flow);
  const cardioDur  = cardioDuration(b.cardiovascular.resource_flow);
  const cogCol     = cognitionClass(b.cognition.state);
  const cogDur     = cognitionDuration(b.cognition.state);
  const commCol    = commClass(b.communication.neurotransmitter);
  const commDur    = commDuration(b.communication.is_active, b.communication.neurotransmitter);
  const ecgDur     = ecgDuration(b.circadian.cycle);
  const iconColor  = ecgColor(b);
  const label      = stateLabel(b.systemState);

  // Single layout that works at any container width:
  //   < ~56px  → vertical dots + icon only (no label, no pill)
  //   ≥ ~56px  → vertical dots + icon + state label below
  //   ≥ ~90px  → switch to horizontal pill + label (more room)
  // The `compact` prop is kept for API compatibility but no longer changes structure —
  // the @container queries handle the transition automatically.
  return (
    <div className="w-full h-full flex items-center justify-center" aria-label={`Mesh ${label}`}>
      {/* Narrow: vertical stack */}
      <div className="flex flex-col items-center gap-1 @[90px]:hidden">
        <span
          className={`w-1.5 h-1.5 rounded-full shrink-0 ${cardioCol} animate-pulse ${cardioDur}`}
          title="Cardiovascular"
        />
        <Activity
          size={11}
          className={`shrink-0 ${iconColor} animate-pulse ${ecgDur}`}
          aria-hidden="true"
        />
        <span
          className={`w-1.5 h-1.5 rounded-full shrink-0 ${cogCol} animate-pulse ${cogDur} [animation-delay:300ms]`}
          title="Cognition"
        />
        <span
          className={`w-1.5 h-1.5 rounded-full shrink-0 ${commCol} animate-pulse ${commDur} [animation-delay:600ms]`}
          title="Communication"
        />
        <span className="hidden @[56px]:block text-[7px] font-black uppercase tracking-widest text-slate-500 mt-0.5">
          {label}
        </span>
      </div>

      {/* Wide: horizontal pill + label */}
      <div className="hidden @[90px]:flex flex-col items-center gap-1">
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-slate-700/60 bg-slate-900/60">
          <span
            className={`w-1.5 h-1.5 rounded-full shrink-0 ${cardioCol} animate-pulse ${cardioDur}`}
            title="Cardiovascular"
          />
          <Activity
            size={12}
            className={`shrink-0 ${iconColor} animate-pulse ${ecgDur}`}
            aria-hidden="true"
          />
          <span
            className={`w-1.5 h-1.5 rounded-full shrink-0 ${cogCol} animate-pulse ${cogDur} [animation-delay:300ms]`}
            title="Cognition"
          />
          <span
            className={`w-1.5 h-1.5 rounded-full shrink-0 ${commCol} animate-pulse ${commDur} [animation-delay:600ms]`}
            title="Communication"
          />
        </div>
        <span className="text-[8px] font-black uppercase tracking-widest text-slate-400 truncate">
          {label}
        </span>
      </div>
    </div>
  );
};
