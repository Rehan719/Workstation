import React from 'react';
import { Handle, Position } from 'reactflow';
import { Cpu, Zap, Shield, Database, Sparkles, Binary } from 'lucide-react';

export const ModuleNode = ({ data }: any) => {
  const icons: Record<string, any> = {
    'MODEL': Cpu,
    'ADAPTER': Zap,
    'TOOL': Database,
    'GUARD': Shield,
    'GENOME': Binary
  };
  const Icon = icons[data.type] || Sparkles;

  return (
    <div className={`px-6 py-4 rounded-2xl bg-slate-900/80 border-2 transition-all group ${data.selected ? 'border-aura shadow-2xl shadow-aura/20' : 'border-slate-800 hover:border-slate-700'}`}>
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-slate-800 border-2 border-slate-700 !rounded-full" />

      <div className="flex items-center gap-4">
         <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${data.selected ? 'bg-aura text-sovereign' : 'bg-slate-800 text-aura'} transition-all`}>
            <Icon size={20} />
         </div>
         <div className="text-left">
            <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-0.5">{data.type}</p>
            <p className="text-xs font-black text-white uppercase tracking-wider">{data.label}</p>
         </div>
      </div>

      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-aura border-2 border-slate-900 !rounded-full" />
    </div>
  );
};

export const RecombinerNode = ({ data }: any) => (
  <div className="px-8 py-6 rounded-3xl bg-aura/10 border-2 border-aura shadow-2xl shadow-aura/10 animate-pulse-subtle">
    <Handle type="target" position={Position.Left} className="w-4 h-4 bg-aura border-2 border-slate-900 !rounded-full" />
    <div className="flex flex-col items-center gap-3">
       <div className="w-14 h-14 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
          <Sparkles size={28} />
       </div>
       <div className="text-center">
          <p className="text-xs font-black text-aura uppercase tracking-[0.2em] mb-1">RECOMBINER</p>
          <p className="text-[10px] font-bold text-white uppercase tracking-widest">{data.strategy || 'TIES-Merge'}</p>
       </div>
    </div>
    <Handle type="source" position={Position.Right} className="w-4 h-4 bg-aura border-2 border-slate-900 !rounded-full" />
  </div>
);
