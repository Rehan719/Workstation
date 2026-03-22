import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { AgentVitals, SystemVitals, UserProfile, RealmType, AppMode, GenomicMetadata } from './types';
import { mockAgentVitals, mockSystemVitals, mockUserProfile, mockBTOProducts, BTOProduct, generateSimulationData } from './simulation';

interface AppState {
  currentRealm: RealmType;
  currentMode: AppMode;
  user: UserProfile | null;
  agentVitals: AgentVitals[];
  systemVitals: SystemVitals;
  genomicMetadata: GenomicMetadata;
  products: BTOProduct[];

  // Actions
  setCurrentRealm: (realm: RealmType) => void;
  setCurrentMode: (mode: AppMode) => void;
  setUser: (user: UserProfile | null) => void;
  updateSystemVitals: (vitals: Partial<SystemVitals>) => void;
  updateAgentVitals: (vitals: AgentVitals[]) => void;
  updateGenomicMetadata: (meta: Partial<GenomicMetadata>) => void;
  runSimulation: () => void;
}

export const useStore = create<AppState>()(
  persist(
    (set, get) => ({
      currentRealm: 'UNIFIED',
      currentMode: 'WORK',
      user: mockUserProfile,
      agentVitals: mockAgentVitals,
      systemVitals: mockSystemVitals,
      genomicMetadata: {
        root_hash: 'did:vsb:genome:7e8a9b...',
        integrity_status: 'VERIFIED',
        regulon_count: 142,
        active_transcription_factors: 42,
        methylation_markers: ['REST_ENFORCED', 'PQC_MANDATORY']
      },
      products: mockBTOProducts,

      setCurrentRealm: (realm) => set({ currentRealm: realm }),
      setCurrentMode: (mode) => set({ currentMode: mode }),
      setUser: (user) => set({ user }),
      updateSystemVitals: (vitals) =>
        set((state) => ({ systemVitals: { ...state.systemVitals, ...vitals } })),
      updateAgentVitals: (vitals) => set({ agentVitals: vitals }),
      updateGenomicMetadata: (meta) =>
        set((state) => ({ genomicMetadata: { ...state.genomicMetadata, ...meta } })),
      runSimulation: () => {
        const data = generateSimulationData();
        set({ systemVitals: data.vitals });
      }
    }),
    {
      name: 'workstation-v3-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
