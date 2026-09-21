import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export type CircadianCycle =
  | 'ACTIVE_FOCUS'
  | 'ACTIVE_REST'
  | 'MAINTENANCE_FOCUS'
  | 'MAINTENANCE_REST';

export type CognitionState = 'FLOURISHING' | 'STABLE' | 'STRESSED';
export type NeurotransmitterState = 'Dopamine' | 'Serotonin' | 'Oxytocin';
export type SystemState = 'WORKING' | 'COMMUNICATING' | 'RESTING' | 'IDLE' | 'MAINTENANCE';

export interface WorkstationBiometrics {
  circadian: {
    cycle: CircadianCycle;
  };
  cardiovascular: {
    // W489 — host CPU HEADROOM (100 − cpu%), i.e. the host's spare capacity. High means the host is
    // IDLE. It is not a measure of the platform's workload and must not be used to label one.
    resource_flow: number;    // 0–100
    peristaltic_delay: number; // host memory percent ÷ 20 — a load index, not milliseconds
    host_cpu_percent?: number;
    resource_flow_basis?: string;
    peristaltic_delay_basis?: string;
  };
  // W489 — the platform's OWN work, which is what a 'working' label is derived from
  workload?: {
    platform_busy: boolean;
    active_projects: number;
    open_channels: number;
    basis?: string;
  };
  cognition: {
    state: CognitionState;
    primary_drive: string;
  };
  communication: {
    active_channels: string[];
    neurotransmitter: NeurotransmitterState;
    is_active: boolean;
  };
  systemState: SystemState;
  loaded: boolean;
  live: boolean;   // W329 — true ONLY when the readings came from the backend (never for defaults)
}

const DEFAULT: WorkstationBiometrics = {
  circadian:      { cycle: 'ACTIVE_FOCUS' },
  cardiovascular: { resource_flow: 100, peristaltic_delay: 5 },   // never shown as live (live:false)
  cognition:      { state: 'STABLE', primary_drive: 'ACHIEVEMENT' },
  communication:  { active_channels: [], neurotransmitter: 'Serotonin', is_active: false },
  systemState:    'IDLE',
  loaded:         false,
  live:           false,
};

function deriveSystemState(b: Omit<WorkstationBiometrics, 'systemState' | 'loaded' | 'live'>): SystemState {
  if (b.communication.is_active)                                          return 'COMMUNICATING';
  if (b.circadian.cycle === 'MAINTENANCE_FOCUS' ||
      b.circadian.cycle === 'MAINTENANCE_REST')                           return 'MAINTENANCE';
  if (b.circadian.cycle === 'ACTIVE_REST')                               return 'RESTING';
  // W489 (sweep S11.14, C3) — THE LABEL WAS INVERTED. This read `resource_flow > 60`, and
  // resource_flow is 100 − host CPU%: the condition was true exactly when the host was IDLE, so a
  // machine doing nothing displayed 'Work' (and 'Mesh Work' to a screen reader). Working is now
  // derived from the platform's own running projects and open channels. When the backend does not
  // report that (an older payload), no work is claimed — IDLE is the honest default.
  if (b.workload?.platform_busy)                                         return 'WORKING';
  return 'IDLE';
}

export function useWorkstationBiometrics(pollIntervalMs = 6000): WorkstationBiometrics {
  const [data, setData] = useState<WorkstationBiometrics>(DEFAULT);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const fetch = async () => {
    try {
      const res = await axios.get('/api/v1/biometrics/status', { timeout: 3000, validateStatus: () => true });
      if (res.status !== 200) {
        setData(prev => ({ ...prev, loaded: true }));
        return;
      }
      const r = res.data ?? {};

      const next: Omit<WorkstationBiometrics, 'systemState' | 'loaded' | 'live'> = {
        circadian: {
          cycle: r.circadian?.cycle ?? 'ACTIVE_FOCUS',
        },
        cardiovascular: {
          resource_flow:    r.cardiovascular?.resource_flow    ?? 100,
          peristaltic_delay: r.cardiovascular?.peristaltic_delay ?? 5,
          host_cpu_percent: r.cardiovascular?.host_cpu_percent,
          resource_flow_basis: r.cardiovascular?.resource_flow_basis,
          peristaltic_delay_basis: r.cardiovascular?.peristaltic_delay_basis,
        },
        // W489 — carried through, because the state label is derived from it
        workload: r.workload ? {
          platform_busy: Boolean(r.workload.platform_busy),
          active_projects: Number(r.workload.active_projects ?? 0),
          open_channels: Number(r.workload.open_channels ?? 0),
          basis: r.workload.basis,
        } : undefined,
        cognition: {
          state:         r.cognition?.state         ?? 'STABLE',
          primary_drive: r.cognition?.primary_drive ?? 'ACHIEVEMENT',
        },
        communication: {
          active_channels: r.communication?.active_channels ?? [],
          neurotransmitter: r.communication?.neurotransmitter ?? 'Serotonin',
          is_active: (r.communication?.active_channels ?? []).length > 0,
        },
      };

      setData({ ...next, systemState: deriveSystemState(next), loaded: true, live: true });
    } catch {
      // Backend unavailable — loaded (no spinner) but NOT live: the chrome must not fabricate health
      setData(prev => ({ ...prev, loaded: true, live: false }));
    }
  };

  useEffect(() => {
    fetch();
    timerRef.current = setInterval(fetch, pollIntervalMs);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pollIntervalMs]);

  return data;
}
