import React from 'react';
import { useStore } from '@workstation/shared';

export const Button = ({ children, variant = 'primary', className = '', ...props }: any) => {
  const { currentMode } = useStore();

  const styles = {
    primary: 'bg-aura text-sovereign hover:scale-105 shadow-lg shadow-aura/20',
    secondary: 'bg-slate-800 text-white hover:bg-slate-700',
    outline: 'border border-slate-700 text-slate-400 hover:text-white hover:border-aura',
    ghost: 'bg-transparent text-slate-500 hover:text-aura transition-all',
  };

  const modeStyles = {
    REST: 'opacity-80 scale-95 grayscale-[20%]',
    WORK: 'opacity-100 scale-100',
    PLAY: 'opacity-100 animate-bounce-subtle ring-2 ring-aura/30',
  };

  return (
    <button
      className={`px-6 py-3 rounded-xl font-bold transition-all flex items-center gap-2 uppercase tracking-widest text-[10px] disabled:opacity-50 disabled:grayscale ${styles[variant as keyof typeof styles]} ${modeStyles[currentMode as keyof typeof modeStyles]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, className = '', glow = false }: any) => {
  const { currentMode } = useStore();

  return (
    <div className={`p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-xl transition-all hover:border-aura/30 ${glow ? 'shadow-2xl shadow-aura/5' : ''} ${currentMode === 'REST' ? 'grayscale-[30%] opacity-90' : ''} ${className}`}>
      {children}
    </div>
  );
};

export const Badge = ({ children, color = 'aura' }: any) => (
  <span className={`px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-[0.2em] bg-${color}/10 text-${color} border border-${color}/20`}>
    {children}
  </span>
);

export * from './CommandCenter';
export * from './AvatarPlaceholder';
export * from './Nodes';
