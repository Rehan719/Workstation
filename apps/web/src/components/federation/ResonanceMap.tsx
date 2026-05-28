import React from 'react';

export const ResonanceMap: React.FC = () => {
  return (
    <div className="w-full h-full bg-sovereign flex items-center justify-center">
      <div className="relative w-64 h-64">
        <div className="absolute inset-0 border-2 border-aura/20 rounded-full animate-ping-slow"></div>
        <div className="absolute inset-4 border-2 border-vital/20 rounded-full animate-pulse-subtle"></div>
        <div className="absolute inset-8 border-2 border-highlight/20 rounded-full animate-ping-slow"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-4 h-4 bg-aura rounded-full shadow-[0_0_20px_rgba(100,255,218,0.8)]"></div>
        </div>
      </div>
    </div>
  );
};
