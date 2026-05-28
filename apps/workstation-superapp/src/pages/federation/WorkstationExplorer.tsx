import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Network, Activity, ShieldCheck } from 'lucide-react';

export const WorkstationExplorer: React.FC = () => {
  const [nodes, setNodes] = useState<any[]>([]);

  useEffect(() => {
    axios.get('/api/v220/federation/nodes').then(res => setNodes(res.data));
  }, []);

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black mb-2">Workstation Explorer</h1>
        <p className="text-slate-500">Interactive visualization of the global Workstation federation and treaty network.</p>
      </header>

      <div className="relative h-[600px] bg-sovereign rounded-3xl border border-slate-800 overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
           <p className="text-slate-700 font-black uppercase tracking-[0.3em] text-sm animate-pulse">Establishing Neural Link...</p>
        </div>

        {nodes.map((node, i) => (
          <div
            key={node.id}
            className="absolute p-4 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl cursor-pointer hover:border-aura transition-all"
            style={{ left: node.pos[0], top: node.pos[1] }}
          >
            <div className="flex items-center gap-3">
               <div className={`w-3 h-3 rounded-full ${node.health > 0.9 ? 'bg-vital' : 'bg-rose-500'} animate-pulse`}></div>
               <span className="font-bold">Node-{node.id}</span>
            </div>
            <p className="text-[10px] text-slate-500 mt-2 font-black uppercase">{node.status} • Health: {(node.health * 100).toFixed(0)}%</p>
          </div>
        ))}

        <div className="absolute bottom-8 right-8 p-6 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl space-y-4">
          <h4 className="text-xs font-black uppercase text-slate-400">Federation Vitals</h4>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Network size={14} className="text-aura" />
              <span className="text-xs font-bold">{nodes.length} Active Nodes</span>
            </div>
            <div className="flex items-center gap-1">
              <ShieldCheck size={14} className="text-vital" />
              <span className="text-xs font-bold">12 Treaties</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
