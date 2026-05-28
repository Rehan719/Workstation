import { create } from 'zustand';
import axios from 'axios';

interface GamificationState {
  stats: any;
  quests: any[];
  loading: boolean;
  xpEarnedThisSession: number;
  fetchStats: (userId: string) => Promise<void>;
  fetchQuests: (userId: string) => Promise<void>;
  addXP: (userId: string, amount: number) => Promise<void>;
  completeQuest: (userId: string, questId: string) => Promise<void>;
  clearSessionXP: () => void;
}

export const useGamificationStore = create<GamificationState>((set, get) => ({
  stats: { xp: 0, level: 1, badges: [], completed_quests: [] },
  quests: [],
  loading: false,
  xpEarnedThisSession: 0,
  fetchStats: async (userId) => {
    set({ loading: true });
    try {
      const res = await axios.get(`/api/v280/gamification/stats/${userId}`);
      set({ stats: res.data, loading: false });
    } catch (err) {
      console.warn("Failed to fetch gamification stats, using defaults.");
      set({ loading: false });
    }
  },
  fetchQuests: async (userId) => {
    try {
      const res = await axios.get(`/api/v280/gamification/quests?user_id=${userId}`);
      set({ quests: res.data });
    } catch (err) {
      console.warn("Failed to fetch quests.");
    }
  },
  addXP: async (userId, amount) => {
    try {
      const res = await axios.post(`/api/v280/gamification/xp?user_id=${userId}&amount=${amount}`);
      set((state) => ({
        stats: { ...state.stats, xp: res.data.new_xp, level: res.data.new_level },
        xpEarnedThisSession: state.xpEarnedThisSession + amount
      }));

      // Global sound effect for XP (simulated via store state change)
      if (res.data.leveled_up) {
        window.dispatchEvent(new CustomEvent('workstation-level-up', { detail: { level: res.data.new_level } }));
      } else {
        window.dispatchEvent(new CustomEvent('workstation-xp-gain'));
      }
    } catch (err) {
      console.error("Failed to add XP");
    }
  },
  completeQuest: async (userId, questId) => {
    try {
      const res = await axios.post(`/api/v280/gamification/quests/complete?user_id=${userId}&quest_id=${questId}`);
      if (res.data.status === 'quest_completed') {
        window.dispatchEvent(new CustomEvent('workstation-quest-complete', { detail: { badge: res.data.badge } }));
        await get().fetchStats(userId);
      }
    } catch (err) {
      console.error("Failed to complete quest");
    }
  },
  clearSessionXP: () => set({ xpEarnedThisSession: 0 })
}));
