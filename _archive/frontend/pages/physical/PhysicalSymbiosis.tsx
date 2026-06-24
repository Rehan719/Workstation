import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Cpu, Zap, Activity, Globe, Wifi, Settings, Thermometer, Droplets, Wind, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';
import { notImplemented } from '@workstation/ui';

export const PhysicalSymbiosis: React.FC = () => {
  const [devices, setDevices] = useState<any[]>([]);
  const [telemetry, setTelemetry] = useState<any>(null);

  useEffect(() => {
    axios.get('/api/v290/iot/devices').then(res => setDevices(res.data));
    const interval = setInterval(() => {
      axios.get('/api/v290/iot/telemetry/dev-001').then(res => setTelemetry(res.data));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-12">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black mb-1 break-words">Physical-Digital Symbiosis</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">IoT & Smart City Integration v150.0</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <div className="px-6 py-3 bg-vital/10 border border-vital/30 rounded-xl flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-vital animate-pulse"></div>
              <span className="text-xs font-black text-vital uppercase tracking-widest">IoT Bridge Active</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-8">
        <div className="@[440px]:col-span-2 space-y-8">
           <section className="p-10 glass-card bg-aura/5 border-aura/20">
              <h3 className="text-2xl font-black mb-8 flex items-center gap-3">
                 <Activity size={24} className="text-aura" />
                 Live Telemetry
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                 {telemetry?.values.map((v: any) => (
                   <div key={v.label} className="p-6 bg-sovereign rounded-2xl border border-white/5 space-y-2">
                      <p className="text-[10px] font-black text-slate-500 uppercase">{v.label}</p>
                      <p className="text-3xl font-black text-white">{v.value.toFixed(1)}<span className="text-xs text-aura ml-1">{v.unit}</span></p>
                   </div>
                 ))}
                 <div className="p-6 bg-sovereign rounded-2xl border border-white/5 flex items-center justify-center">
                    <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest italic">Waiting for pulse...</p>
                 </div>
              </div>
           </section>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {devices.map(dev => (
                <div key={dev.id} className="p-8 glass-card border-white/5 hover:border-white/10 transition-all flex flex-col">
                   <div className="flex justify-between items-start mb-6">
                      <div className="p-4 bg-surface rounded-2xl text-slate-500">
                         {dev.type === 'sensor' ? <Wifi size={24} /> : <Settings size={24} />}
                      </div>
                      <span className={`text-[10px] font-black px-3 py-1.5 rounded-full border uppercase tracking-widest ${
                        dev.status === 'online' ? 'bg-vital/10 text-vital border-vital/20' : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}>
                         {dev.status}
                      </span>
                   </div>
                   <h4 className="text-xl font-bold mb-1">{dev.name}</h4>
                   <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mb-6">{dev.protocol} Protocol</p>
                   <button type="button" onClick={() => notImplemented('Configure Device')} className="w-full py-4 bg-white/5 border border-white/10 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-white/10 transition-all mt-auto">Configure Device</button>
                </div>
              ))}
           </div>
        </div>

        <aside className="space-y-8">
           <section className="p-8 glass-card border-highlight/20 bg-highlight/5">
              <h3 className="text-xl font-bold mb-6">Discovery Swarm</h3>
              <p className="text-xs text-slate-400 font-bold leading-relaxed mb-8">
                 Your reactors are currently interfaced with the **Planetary Stewardship Network**. 1,420 nodes reporting environmental fidelity.
              </p>
              <div className="h-48 bg-sovereign rounded-2xl border border-white/5 flex items-center justify-center relative overflow-hidden group">
                 <Globe size={48} className="text-highlight/20 group-hover:scale-150 group-hover:text-highlight/40 transition-all duration-1000" />
                 <div className="absolute inset-0 border-2 border-highlight/10 rounded-2xl animate-pulse"></div>
              </div>
           </section>

           <section className="p-8 glass-card border-vital/20">
              <div className="flex items-center gap-3 mb-6">
                 <ShieldCheck size={20} className="text-vital" />
                 <h3 className="text-lg font-bold">PQC Security Layer</h3>
              </div>
              <p className="text-xs text-slate-500 font-bold leading-relaxed">
                 All IoT telemetry is encrypted via Kyber-1024 at the edge. No classical leakage detected.
              </p>
           </section>
        </aside>
      </div>
    </div>
  );
};
