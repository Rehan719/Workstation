import React from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Globe, Users, MessageSquare, Zap, Shield, Camera, MousePointer2, Smartphone, Monitor, Info, Activity } from 'lucide-react';
import { motion } from 'framer-motion';

export const ARVRSandbox: React.FC = () => {
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter break-words">Immersive Lab</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">AR/VR Prototypes • WebXR Council Chambers • Phase 3</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('VR Mode')} variant="outline"><Camera size={18} /> VR Mode</Button>
           <Button onClick={() => notImplemented('Join Council Meeting')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Users size={18} /> Join Council Meeting
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8">
            <Card className="h-[600px] flex flex-col justify-center items-center relative overflow-hidden bg-slate-950 border-aura/20 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-3xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     3D Council Chamber
                     <Badge color="aura">WebXR Active</Badge>
                  </h3>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Immersive Multi-Agent Participation Lab</p>
               </div>

               {/* 3D Simulation Stub */}
               <div className="relative z-10 flex flex-col items-center gap-8">
                  <div className="w-96 h-96 rounded-full border-2 border-aura/10 flex items-center justify-center animate-pulse-slow">
                     <div className="w-72 h-72 rounded-full border border-aura/20 flex items-center justify-center">
                        <Users size={120} className="text-aura opacity-20" />
                     </div>
                  </div>
                  <div className="flex gap-6">
                     {[1, 2, 3, 4, 5].map(i => (
                        <div key={i} className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:scale-110 transition-transform">
                           <Users size={20} />
                        </div>
                     ))}
                  </div>
               </div>

               <div className="absolute bottom-10 flex gap-6 z-10">
                  <Button onClick={() => notImplemented('Hand Tracking')} variant="outline" className="px-8 py-3"><MousePointer2 size={16} /> Hand Tracking</Button>
                  <Button onClick={() => notImplemented('Mobile AR Sync')} variant="outline" className="px-8 py-3"><Smartphone size={16} /> Mobile AR Sync</Button>
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Zap size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Spatial Mesh</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Navigate the planetary mesh in 3D. Click and drag nodes to inspect real-time cytokine propagation paths.
                  </p>
               </div>
               <Button onClick={() => notImplemented('Launch 3D Explorer')} className="w-full bg-aura text-sovereign py-5 rounded-2xl font-black text-[10px] uppercase tracking-widest">Launch 3D Explorer</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Hardware Vitals</h4>
               <div className="space-y-4">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Frame Rate</span>
                     <span className="text-emerald-500">90 FPS</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Latency</span>
                     <span className="text-white">&lt;11ms</span>
                  </div>
               </div>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Spatial computing modules are built on Three.js and WebXR for cross-device immersion.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
