import React from 'react';

export const Button = ({ children, variant = 'primary', ...props }: any) => {
  const styles = {
    primary: 'bg-aura text-sovereign hover:scale-105',
    secondary: 'bg-slate-800 text-white hover:bg-slate-700',
    outline: 'border border-slate-700 text-slate-400 hover:text-white hover:border-aura',
  };

  return (
    <button
      className={`px-6 py-3 rounded-xl font-bold transition-all flex items-center gap-2 ${styles[variant as keyof typeof styles]}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, className = '' }: any) => (
  <div className={`p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm ${className}`}>
    {children}
  </div>
);

export const Badge = ({ children, color = 'aura', className = '' }: any) => {
  const colors = {
    aura: 'bg-aura/10 text-aura border-aura/20',
    highlight: 'bg-highlight/10 text-highlight border-highlight/20',
    vital: 'bg-vital/10 text-vital border-vital/20',
    sovereign: 'bg-sovereign/10 text-white border-sovereign/20',
    'emerald-500': 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20',
  };

  return (
    <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border ${colors[color as keyof typeof colors] || colors.aura} ${className}`}>
      {children}
    </span>
  );
};

export const ModuleNode = ({ data }: any) => (
  <div className="p-5 rounded-2xl bg-slate-950 border-2 border-slate-900 shadow-2xl min-w-[150px]">
    <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">{data.type}</p>
    <p className="text-sm font-black text-white uppercase">{data.label}</p>
  </div>
);

export const RecombinerNode = ({ data }: any) => (
  <div className="p-6 rounded-full bg-aura/5 border-2 border-aura border-dashed flex items-center justify-center w-32 h-32 animate-pulse shadow-xl shadow-aura/10">
    <p className="text-[10px] font-black text-aura uppercase tracking-widest">{data.strategy}</p>
  </div>
);

export * from './CommandCenter';
export * from './AvatarPlaceholder';
export * from './RealmSelector';
