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
    resource_flow: number;    // 0–100
    peristaltic_delay: number; // ms, healthy ≤ 5
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
}

const DEFAULT: WorkstationBiometrics = {
  circadian:      { cycle: 'ACTIVE_FOCUS' },
  cardiovascular: { resource_flow: 100, peristaltic_delay: 5 },
  cognition:      { state: 'STABLE', primary_drive: 'ACHIEVEMENT' },
  communication:  { active_channels: [], neurotransmitter: 'Serotonin', is_active: false },
  systemState:    'IDLE',
  loaded:         false,
};

function deriveSystemState(b: Omit<WorkstationBiometrics, 'systemState' | 'loaded'>): SystemState {
  if (b.communication.is_active)                                          return 'COMMUNICATING';
  if (b.circadian.cycle === 'MAINTENANCE_FOCUS' ||
      b.circadian.cycle === 'MAINTENANCE_REST')                           return 'MAINTENANCE';
  if (b.circadian.cycle === 'ACTIVE_REST')                               return 'RESTING';
  if (b.cardiovascular.resource_flow > 60)                               return 'WORKING';
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

      const next: Omit<WorkstationBiometrics, 'systemState' | 'loaded'> = {
        circadian: {
          cycle: r.circadian?.cycle ?? 'ACTIVE_FOCUS',
        },
        cardiovascular: {
          resource_flow:    r.cardiovascular?.resource_flow    ?? 100,
          peristaltic_delay: r.cardiovascular?.peristaltic_delay ?? 5,
        },
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

      setData({ ...next, systemState: deriveSystemState(next), loaded: true });
    } catch {
      // Backend unavailable — mark loaded so the UI shows default state rather than a spinner
      setData(prev => ({ ...prev, loaded: true }));
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
