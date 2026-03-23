import { create } from 'zustand';
import { AgentVitals, SystemVitals, UserProfile, RealmType, ModeType } from './types';
import { mockAgentVitals, mockSystemVitals, mockUserProfile, mockBTOProducts, BTOProduct, generateSimulationData } from './simulation';

export interface AppState {
  currentRealm: RealmType;
  currentMode: ModeType;
  user: UserProfile | null;
  agentVitals: AgentVitals[];
  systemVitals: SystemVitals;
  products: BTOProduct[];
  genomicMetadata: any;
  setCurrentRealm: (realm: RealmType) => void;
  setCurrentMode: (mode: ModeType) => void;
  setUser: (user: UserProfile | null) => void;
  updateSystemVitals: (vitals: Partial<SystemVitals>) => void;
  updateAgentVitals: (vitals: AgentVitals[]) => void;
  runSimulation: () => void;
}

export const useStore = create<AppState>((set, get) => ({
  currentRealm: 'UNIFIED',
  currentMode: 'ACTIVE',
  user: mockUserProfile,
  genomicMetadata: {
    fidelity: 0.9998,
    lastMutation: 'JUST_NOW',
    activeOperons: 12
  },
  agentVitals: mockAgentVitals,
  systemVitals: mockSystemVitals,
  products: mockBTOProducts,
  setCurrentRealm: (realm) => set({ currentRealm: realm }),
  setCurrentMode: (mode) => set({ currentMode: mode }),
  setUser: (user) => set({ user }),
  updateSystemVitals: (vitals) =>
    set((state) => ({ systemVitals: { ...state.systemVitals, ...vitals } })),
  updateAgentVitals: (vitals) => set({ agentVitals: vitals }),
  runSimulation: () => {
    const data = generateSimulationData();
    set({ systemVitals: data.vitals });
  }
}));
