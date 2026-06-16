import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Globe, MessageSquare, ShieldCheck, History, Info, ChevronRight, Zap, Globe2, AlertCircle, Plus, Send, Network, Radio, Sparkles } from 'lucide-react';
import { useStore, gaas } from '@workstation/shared';
import { motion, AnimatePresence } from 'framer-motion';

export const InterstellarDiplomacy: React.FC = () => {
  const [activeSignal, setActiveSignal] = useState(0);

  const signals = [
    { id: 'sig-1', source: 'Alpha-Centauri-Vector', type: 'EM-Broadband', status: 'Deciphering', confidence: 0.42 },
    { id: 'sig-2', source: 'Local-Offspring-Mesh', type: 'DTN-Handshake', status: 'Ratified', confidence: 0.99 },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">Interstellar Diplomacy</h1>
          <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">First-Contact Frameworks • Universal Translation Console</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('SETI Feed')} variant="outline"><Radio size={18} /> SETI Feed</Button>
           <Button onClick={() => notImplemented('Broadcast Handshake')} className="bg-highlight text-sovereign shadow-xl shadow-highlight/20">
              <Sparkles size={18} /> Broadcast Handshake
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-highlight/5 border-highlight/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,204,100,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     Universal Decipherment
                     <Badge color="highlight">Phi-3-Multimodal</Badge>
                  </h3>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Symbolic & Gravitational Signal Interpretation</p>
               </div>

               <div className="relative z-10 flex flex-col items-center gap-6">
                  <motion.div
                     animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.3, 0.6, 0.3]
                     }}
                     transition={{ repeat: Infinity, duration: 4 }}
                     className="w-48 h-48 rounded-full border-2 border-highlight/20 flex items-center justify-center"
                  >
                     <Radio size={80} className="text-highlight opacity-40 animate-pulse" />
                  </motion.div>
                  <p className="font-mono text-xs text-highlight animate-pulse text-center">... SIGNAL DETECTED ...<br/>ANALYSING VECTOR 14.2.42</p>
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                     <Globe size={24} className="text-highlight" />
                     Interstellar Treaties
                  </h3>
                  <div className="flex gap-4">
                     <Badge color="highlight">Article 1132 Compliant</Badge>
                  </div>
               </div>

               <div className="space-y-4">
                  {signals.map((sig, i) => (
                    <motion.div
                      key={sig.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-highlight/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-highlight group-hover:bg-highlight group-hover:text-sovereign transition-all`}>
                             <Network size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{sig.source}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{sig.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-highlight">Confidence: {sig.confidence * 100}%</span>
                             </div>
                          </div>
                       </div>
                       <Badge color={sig.status === 'Ratified' ? 'emerald-500' : 'aura'}>{sig.status}</Badge>
                    </motion.div>
                  ))}
               </div>
            </Card>
         </main>

         <aside className="lg:col-span-4 space-y-10">
            <Card className="p-10 space-y-10 bg-highlight/5 border-highlight/20">
               <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign shadow-xl shadow-highlight/20">
                  <ShieldCheck size={32} />
               </div>
               <div>
                  <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Prime Protocol</h3>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Non-interference protocols for development of alien species. Article 1142 enforces ethical first-contact boundaries.
                  </p>
               </div>
               <Button onClick={() => notImplemented('Configure Contact Rules')} className="w-full bg-highlight text-sovereign py-6 rounded-2xl font-black text-[10px] uppercase tracking-widest">Configure Contact Rules</Button>
            </Card>

            <Card className="p-10 bg-slate-950 border-slate-900 space-y-6">
               <h4 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">Contact Templates</h4>
               <div className="space-y-3">
                  <Button onClick={() => notImplemented('Sovereign Identification')} variant="outline" className="w-full text-left py-3 text-[9px] px-4 justify-start">Sovereign Identification</Button>
                  <Button onClick={() => notImplemented('Resource Neutrality Pact')} variant="outline" className="w-full text-left py-3 text-[9px] px-4 justify-start">Resource Neutrality Pact</Button>
                  <Button onClick={() => notImplemented('Knowledge Exchange Treaty')} variant="outline" className="w-full text-left py-3 text-[9px] px-4 justify-start">Knowledge Exchange Treaty</Button>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
