import React from 'react';

/**
 * Honest placeholder for actions whose backend/feature isn't built yet.
 * Use instead of leaving a button with no onClick handler at all — clicking
 * should always give the user feedback, even when the underlying capability
 * is still in development.
 */
export const toast = (msg: string) => {
  const existing = document.querySelectorAll('[data-workstation-toast]');
  const offset = existing.length * 52;
  const el = document.createElement('div');
  el.setAttribute('data-workstation-toast', '');
  el.setAttribute('role', 'status');
  el.setAttribute('aria-live', 'polite');
  el.style.cssText = [
    'position:fixed', `bottom:${24 + offset}px`, 'right:24px', 'z-index:99999',
    'background:#0f172a', 'color:#e2e8f0', 'border:1px solid #1e293b',
    'padding:10px 18px', 'border-radius:12px', 'font-size:10px', 'font-weight:700',
    'text-transform:uppercase', 'letter-spacing:0.1em',
    'box-shadow:0 8px 32px rgba(0,0,0,0.5)', 'max-width:320px', 'line-height:1.4',
    'transition:opacity 0.2s ease', 'opacity:1',
  ].join(';');
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 200); }, 3000);
};

export const notImplemented = (feature: string = 'This action') => {
  const existing = document.querySelectorAll('[data-notimpl-toast]');
  const offset = existing.length * 52;
  const el = document.createElement('div');
  el.setAttribute('data-notimpl-toast', '');
  el.setAttribute('role', 'status');
  el.setAttribute('aria-live', 'polite');
  el.style.cssText = [
    'position:fixed', `bottom:${24 + offset}px`, 'right:24px', 'z-index:99999',
    'background:#0f172a', 'color:#94a3b8', 'border:1px solid #1e293b',
    'padding:10px 18px', 'border-radius:12px', 'font-size:10px', 'font-weight:700',
    'text-transform:uppercase', 'letter-spacing:0.1em',
    'box-shadow:0 8px 32px rgba(0,0,0,0.5)', 'max-width:320px', 'line-height:1.4',
    'transition:opacity 0.2s ease', 'opacity:1',
  ].join(';');
  el.textContent = `${feature} — Coming Soon`;
  document.body.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 200); }, 3000);
};

export const Button = ({ children, variant = 'primary', className = '', type = 'button', ...props }: any) => {
  const styles: Record<string, string> = {
    primary: 'bg-aura text-sovereign hover:scale-105',
    secondary: 'bg-slate-800 text-white hover:bg-slate-700',
    outline: 'border border-slate-700 text-slate-400 hover:text-white hover:border-aura',
    ghost: 'text-slate-400 hover:text-white bg-transparent',
  };

  return (
    <button
      type={type}
      className={`px-6 py-3 rounded-xl font-bold transition-all flex items-center gap-2 ${styles[variant] ?? ''} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const Card = ({ children, className = '', ...props }: any) => (
  <div className={`p-8 rounded-3xl bg-slate-900/40 border border-slate-800 backdrop-blur-sm ${className}`} {...props}>
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
