import { create } from 'zustand';
import { AgentVitals, SystemVitals, UserProfile, RealmType } from './types';
import { mockAgentVitals, mockSystemVitals, mockUserProfile, mockBTOProducts, BTOProduct, generateSimulationData } from './simulation';

interface AppState {
  currentRealm: RealmType;
  user: UserProfile | null;
  agentVitals: AgentVitals[];
  systemVitals: SystemVitals;
  products: BTOProduct[];
  setCurrentRealm: (realm: RealmType) => void;
  setUser: (user: UserProfile | null) => void;
  updateSystemVitals: (vitals: Partial<SystemVitals>) => void;
  updateAgentVitals: (vitals: AgentVitals[]) => void;
  runSimulation: () => void;
}

export const useStore = create<AppState>((set, get) => ({
  currentRealm: 'UNIFIED',
  user: mockUserProfile,
  agentVitals: mockAgentVitals,
  systemVitals: mockSystemVitals,
  products: mockBTOProducts,
  setCurrentRealm: (realm) => set({ currentRealm: realm }),
  setUser: (user) => set({ user }),
  updateSystemVitals: (vitals) =>
    set((state) => ({ systemVitals: { ...state.systemVitals, ...vitals } })),
  updateAgentVitals: (vitals) => set({ agentVitals: vitals }),
  runSimulation: () => {
    const data = generateSimulationData();
    set({ systemVitals: data.vitals });
  }
}));
