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

export * from './CommandCenter';
export * from './AvatarPlaceholder';
export * from './RealmSelector';
