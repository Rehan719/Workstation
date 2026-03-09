import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, Users, Shield, Cpu, Zap } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import DigitalTwinVisualizer from '../components/twins/DigitalTwinVisualizer';

const SynergyConsole = () => {
  const [activeWorkflow, setActiveWorkflow] = useState(null);

  const workflows = [
    { id: 'startup', name: 'Startup Ecosystem Mega-Twin', reactors: ['Biz', 'Law', 'Career', 'Market'], status: 'SIMULATING' },
    { id: 'edu', name: 'Educational Impact Mega-Twin', reactors: ['K-12', 'HigherEd', 'JobSearch'], status: 'OPTIMIZING' },
    { id: 'fatwa', name: 'Fatwa Impact Mega-Twin', reactors: ['Fiqh', 'Hadith', 'Finance', 'Dawah'], status: 'READY' },
    { id: 'gdpr', name: 'Regulatory Compliance Mega-Twin', reactors: ['Compliance', 'CorpLaw', 'Tax'], status: 'READY' }
  ];

  return (
    <div className="flex h-screen bg-slate-950 text-white font-sans overflow-hidden">
      {/* Sidebar: Virtual Task Forces */}
      <div className="w-80 border-r border-white/10 bg-slate-900/50 backdrop-blur-2xl p-6 overflow-y-auto">
        <div className="flex items-center gap-3 mb-8">
          <div className="p-2 bg-amber-500 rounded-lg text-slate-900">
            <Activity size={20} />
          </div>
          <h2 className="text-xl font-black uppercase tracking-tighter">Synergy Console</h2>
        </div>

        <div className="space-y-4">
          <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Active Mega-Twins</p>
          {workflows.map(wf => (
            <motion.div
              key={wf.id}
              whileHover={{ x: 5 }}
              onClick={() => setActiveWorkflow(wf)}
              className={`p-4 rounded-xl border cursor-pointer transition-all ${activeWorkflow?.id === wf.id ? 'border-amber-500 bg-amber-500/10' : 'border-white/5 bg-white/5'}`}
            >
              <h3 className="text-sm font-bold mb-2">{wf.name}</h3>
              <div className="flex gap-1 flex-wrap mb-3">
                {wf.reactors.map(r => (
                  <span key={r} className="text-[8px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400 font-mono">{r}</span>
                ))}
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[9px] font-black text-amber-500 animate-pulse">{wf.status}</span>
                <Users size={12} className="text-slate-500" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Main: Immersive Digital Twin View */}
      <div className="flex-1 relative">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-amber-950/20" />

        <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
          <DigitalTwinVisualizer twinData={activeWorkflow} />
          <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
        </Canvas>

        {/* HUD: Optimization & Metrics */}
        <div className="absolute top-8 right-8 w-72 space-y-6">
          <div className="p-6 bg-slate-900/80 backdrop-blur-xl border border-white/10 rounded-2xl">
             <div className="flex justify-between items-center mb-4">
                <p className="text-xs font-black uppercase text-slate-400">ARO Telemetry</p>
                <Cpu size={14} className="text-blue-500" />
             </div>
             <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-[10px] mb-1">
                    <span>GPU Acceleration</span>
                    <span>94%</span>
                  </div>
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500 w-[94%]" />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-[10px] mb-1">
                    <span>API Quota (Enterprise)</span>
                    <span>82/1000</span>
                  </div>
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 w-[8%]" />
                  </div>
                </div>
             </div>
          </div>

          <div className="p-6 bg-slate-900/80 backdrop-blur-xl border border-white/10 rounded-2xl">
             <div className="flex justify-between items-center mb-4">
                <p className="text-xs font-black uppercase text-slate-400">BTO Dynamics</p>
                <Users size={14} className="text-amber-500" />
             </div>
             <div className="space-y-2">
                <div className="flex items-center gap-2 text-[10px]">
                  <Zap size={10} className="text-amber-500" />
                  <span>Leader: AI Commander v100</span>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                  <Shield size={10} className="text-emerald-500" />
                  <span>Truth Consensus: VERIFIED</span>
                </div>
             </div>
          </div>
        </div>

        {/* Bottom Bar: Synergistic Actions */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-4">
           <button className="px-8 py-3 bg-amber-500 text-slate-900 rounded-xl font-black text-xs uppercase tracking-widest shadow-lg shadow-amber-500/20 hover:scale-105 transition-transform">
             Inject "What-If" Scenario
           </button>
           <button className="px-8 py-3 bg-white/5 border border-white/10 text-white rounded-xl font-black text-xs uppercase tracking-widest hover:bg-white/10 transition-colors">
             Export Twin State
           </button>
        </div>
      </div>
    </div>
  );
};

export default SynergyConsole;
