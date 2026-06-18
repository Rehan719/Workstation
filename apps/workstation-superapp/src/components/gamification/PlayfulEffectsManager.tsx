import React, { useEffect } from 'react';
import { useGamificationStore } from '../../store/gamificationStore';

// In a real environment, we'd import { Howl } from 'howler';
// For this environment, we'll simulate the audio triggers

export const PlayfulEffectsManager: React.FC = () => {
  const { stats } = useGamificationStore();

  useEffect(() => {
    const handleXPGain = () => {
       // Audio stub — wire Howler here when audio assets are available
    };

    const handleLevelUp = (_e: any) => {
       // Trigger Confetti (simulated)
    };

    const handleQuestComplete = (_e: any) => {
       // Achievement fanfare stub
    };

    window.addEventListener('workstation-xp-gain', handleXPGain);
    window.addEventListener('workstation-level-up', handleLevelUp);
    window.addEventListener('workstation-quest-complete', handleQuestComplete);

    return () => {
      window.removeEventListener('workstation-xp-gain', handleXPGain);
      window.removeEventListener('workstation-level-up', handleLevelUp);
      window.removeEventListener('workstation-quest-complete', handleQuestComplete);
    };
  }, []);

  return null; // Side-effect only component
};
