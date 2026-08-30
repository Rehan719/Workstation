import React, { useState, createContext, useContext, useEffect } from 'react';
import { getPrefs, setPrefs } from '../lib/userPrefs';

// §9 (W357) — REAL adaptive UI, driven by the user's OWN stored preferences (was fabricated
// constants + a dead updateProfile). fontScale genuinely enlarges the interface (an inline root
// font-size, not a decorative class); guidedMode/tone reflect the user's actual choice and persist
// via userPrefs (ws:user-prefs). Honesty-over-polish: every value here is a real, user-set signal.
interface AdaptiveUIState {
  fontScale: 'standard' | 'large';
  guidedMode: boolean;
  tone: 'encouraging' | 'neutral';
  layout: string;                 // derived label the hubs render — now from a real preference
  emotionalAdjustment: string;    // derived label the hubs render — now from a real preference
  setFontScale: (v: 'standard' | 'large') => void;
  setGuidedMode: (v: boolean) => void;
  setTone: (v: 'encouraging' | 'neutral') => void;
}

const AdaptiveUIContext = createContext<AdaptiveUIState | undefined>(undefined);

function readState() {
  const p = getPrefs();
  const fontScale = p.fontScale === 'large' ? 'large' : 'standard';
  const guidedMode = p.guidedMode !== false;         // default on
  const tone = p.tone === 'neutral' ? 'neutral' : 'encouraging';
  return { fontScale, guidedMode, tone } as const;
}

export const AdaptiveUIProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [ui, setUi] = useState(readState);

  // stay in sync when preferences change anywhere (Settings, another tab component)
  useEffect(() => {
    const h = () => setUi(readState());
    window.addEventListener('ws:user-prefs', h);
    return () => window.removeEventListener('ws:user-prefs', h);
  }, []);

  const persist = (patch: Partial<ReturnType<typeof readState>>) => {
    setPrefs({ ...getPrefs(), ...patch });   // fires ws:user-prefs → the effect re-reads
  };

  const value: AdaptiveUIState = {
    fontScale: ui.fontScale,
    guidedMode: ui.guidedMode,
    tone: ui.tone,
    layout: ui.guidedMode ? 'Guided' : 'Advanced',
    emotionalAdjustment: ui.tone === 'neutral' ? 'Neutral' : 'Encouraging',
    setFontScale: (v) => persist({ fontScale: v }),
    setGuidedMode: (v) => persist({ guidedMode: v }),
    setTone: (v) => persist({ tone: v }),
  };

  return (
    <AdaptiveUIContext.Provider value={value}>
      {/* the font scale is a REAL rendered effect, not a label */}
      <div className="adaptive-ui-root" style={{ fontSize: ui.fontScale === 'large' ? '1.15rem' : undefined }}>
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
