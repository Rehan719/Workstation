import { create } from 'zustand';
import axios from 'axios';

interface ModeState {
  currentMode: string;
  config: any;
  setMode: (modeId: string) => Promise<void>;
}

export const useModeStore = create<ModeState>((set) => ({
  currentMode: 'strategic',
  config: null,
  setMode: async (modeId) => {
    try {
      const res = await axios.get(`/api/v191/modes/${modeId}`);
      set({ currentMode: modeId, config: res.data });
    } catch (err) {
      console.error("Failed to set mode", err);
    }
  },
}));
