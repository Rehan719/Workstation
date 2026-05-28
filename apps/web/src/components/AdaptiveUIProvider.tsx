import React, { useState, createContext, useContext, useEffect } from 'react';

interface AdaptiveUIState {
  theme: string;
  fontSize: string;
  layout: string;
  emotionalAdjustment: string;
  updateProfile: (profile: any) => void;
}

const AdaptiveUIContext = createContext<AdaptiveUIState | undefined>(undefined);

export const AdaptiveUIProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [uiState, setUiState] = useState({
    theme: 'Sovereign_Dark',
    fontSize: 'Standard',
    layout: 'Guided',
    emotionalAdjustment: 'Encouraging'
  });

  const updateProfile = (profile: any) => {
    // Cross-Domain Adaptive Logic powered by DRAD engine
    const age = profile.age || 25;
    const skill = profile.skill || 'Intermediate';
    const role = profile.role || 'Guardian';

    setUiState({
      theme: age < 12 ? 'Playful_Light' : 'Sovereign_Dark',
      fontSize: age > 60 ? 'Large' : 'Standard',
      layout: (skill === 'Expert' || role === 'CEO') ? 'Advanced' : 'Guided',
      emotionalAdjustment: profile.emotion === 'Frustrated' ? 'Gentle' : 'Encouraging'
    });
  };

  return (
    <AdaptiveUIContext.Provider value={{ ...uiState, updateProfile }}>
      <div className={`adaptive-ui-root v1-baseline font-size-${uiState.fontSize.toLowerCase()}`}>
        {children}
      </div>
    </AdaptiveUIContext.Provider>
  );
};

export const useAdaptiveUI = () => {
  const context = useContext(AdaptiveUIContext);
  if (!context) throw new Error('useAdaptiveUI must be used within AdaptiveUIProvider');
  return context;
};
