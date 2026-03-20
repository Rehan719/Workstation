import { create } from 'zustand';

export const useStore = create((set) => ({
  currentRealm: 'UNIFIED',
  user: { displayName: 'Guardian' },
  systemVitals: {
    cpu: 45.2,
    memory: 12.8,
    activeAgents: 24,
    swarmHealth: 0.96,
  },
  setCurrentRealm: (realm) => set({ currentRealm: realm }),
}));
