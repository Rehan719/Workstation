import React, { useEffect } from 'react';
import { useStore } from '@workstation/shared';

export const PlayfulEffectsManager: React.FC = () => {
  const { currentMode } = useStore();

  useEffect(() => {
    const handleXPGain = () => {
       console.log("🔊 Playing 'xp_gain' chime.");
    };

    const handleLevelUp = (e: any) => {
       console.log(`🎉 Level Up! Playing 'celebration' fanfare.`);
    };

    const handleQuestComplete = (e: any) => {
       console.log(`🏆 Quest Complete! Playing 'achievement' sound.`);
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

  return null;
};
