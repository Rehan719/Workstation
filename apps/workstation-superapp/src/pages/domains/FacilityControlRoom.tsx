import React, { useState, useEffect, useRef } from 'react';
import {
  Settings,
  ShieldAlert,
  Zap,
  Lightbulb,
  TestTube,
  FlaskConical,
  Factory,
  CheckCircle,
  AlertTriangle,
  Cpu,
  Download,
  Smartphone,
  Globe,
  ShoppingCart,
  Boxes,
  ClipboardList,
  RefreshCcw,
  ExternalLink
} from 'lucide-react';

const FacilityCard = ({ id, name, icon: Icon, status, metrics, onOpen }) => (
  <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/50 transition-all cursor-pointer group" onClick={onOpen}>
    <div className="flex justify-between items-start mb-4">
      <div className="p-3 bg-cyan-500/10 rounded-lg text-cyan-400 group-hover:scale-110 transition-transform">
        <Icon size={24} />
      </div>
      <span className={`px-2 py-1 rounded text-xs font-bold ${
        status === 'online' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'
      }`}>
        {status.toUpperCase()}
      </span>
    </div>
    <h3 className="text-xl font-bold text-white mb-2">{name}</h3>
    <div className="space-y-2">
      {Object.entries(metrics).map(([key, val]) => (
        <div key={key} className="flex justify-between text-sm">
          <span className="text-slate-400 capitalize">{key.replace('_', ' ')}:</span>
          <span className="text-cyan-300 font-mono">{val}</span>
        </div>
      ))}
    </div>
  </div>
);

const FabricationPlantDashboard = () => {
  const [selectedFacility, setSelectedFacility] = useState(null);
  const [orderProgress, setOrderProgress] = useState(0);
  const [activeOrder, setActiveOrder] = useState(null);
  const [orderStep, setOrderStep] = useState('');
  const progressBarRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (progressBarRef.current) {
      progressBarRef.current.style.width = `${orderProgress}%`;
    }
  }, [orderProgress]);

  const facilities = [
    {
      id: 'engines',
      name: 'Digital Engines',
      icon: Cpu,
      status: 'online',
      metrics: { throughput: '2.5k/hr', uptime: '99.99%', load: '65%' }
    },
    {
      id: 'reactors',
      name: 'Validation Reactors',
      icon: Zap,
      status: 'online',
      metrics: { accuracy: '100%', safety: 'Enforced', load: '12%' }
    },
    {
      id: 'incubators',
      name: 'Concept Incubators',
      icon: Lightbulb,
      status: 'online',
      metrics: { graduation: '82%', new_ideas: '15', speed: 'High' }
    },
    {
      id: 'petri_dishes',
      name: 'Testing Petri Dishes',
      icon: TestTube,
      status: 'online',
      metrics: { isolation: '100%', stability: '99.8%', active: '3' }
    },
    {
      id: 'laboratories',
      name: 'Research Labs',
      icon: FlaskConical,
      status: 'online',
      metrics: { publications: '12', ontology: '+15%', status: 'Active' }
    },
    {
      id: 'factories',
      name: 'Production Factories',
      icon: Factory,
      status: 'online',
      metrics: { yield: '99.9%', custom_orders: '42', backlog: 'Zero' }
    }
  ];

  const blueprints = [
    { id: 'BP-001', name: 'High-Throughput Engine', domain: 'Science', status: 'Exported' },
    { id: 'BP-002', name: 'Theological Reactor', domain: 'Law', status: 'Exported' },
    { id: 'BP-003', name: 'Concept Incubator', domain: 'Enterprise', status: 'Ready' }
  ];

  const handlePlaceOrder = () => {
    setActiveOrder({ id: 'BTO-786-ALIF', level: 5, type: 'Tafsir', lang: 'English' });
    setOrderProgress(0);
    setOrderStep('INTAKE');

    let progress = 0;
    const interval = setInterval(() => {
      progress += 5;
      setOrderProgress(progress);

      if (progress < 20) setOrderStep('INTAKE (Digital Engines)');
      else if (progress < 40) setOrderStep('REFINING (Digital Engines)');
      else if (progress < 60) setOrderStep('INCUBATION (Incubators)');
      else if (progress < 80) setOrderStep('VALIDATION (Reactors)');
      else if (progress < 95) setOrderStep('ASSEMBLY (Factories)');
      else setOrderStep('DELIVERY (Digital Engines)');

      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 400);
  };

  return (
    <div className="min-h-screen bg-black text-slate-200 p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-black text-white tracking-tighter flex items-center gap-3">
            <Boxes className="text-cyan-500" /> KNOWLEDGE FABRICATION PLANT
          </h1>
          <p className="text-slate-500">QEP v8.9 Sovereign Signature | Industrial-Scale Knowledge Manufacturing</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-800 text-sm flex items-center gap-2">
            <RefreshCcw size={14} className="text-cyan-500 animate-spin-slow" />
            <span className="text-slate-500 uppercase">Plant Status:</span>
            <span className="text-green-400 font-bold uppercase tracking-widest">Operating</span>
          </div>
          <div className="bg-cyan-500 text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-2 shadow-lg shadow-cyan-500/20">
            <Boxes size={16} /> VSB FABRICATION ACTIVE
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Left Column: BTO & Blueprints */}
        <div className="xl:col-span-1 space-y-8">
          {/* BTO Order Section */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 backdrop-blur-sm">
            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
               <ShoppingCart className="text-cyan-500" /> CUSTOM BTO ORDER
            </h2>
            <div className="space-y-4 mb-8">
              <div>
                <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-2">Content Type</label>
                <select aria-label="Content Type" title="Content Type" className="w-full bg-black border border-slate-800 rounded-lg p-3 text-sm text-white focus:border-cyan-500 outline-none">
                  <option>Tafsir (Standard)</option>
                  <option>Hifz Tracking</option>
                  <option>Arabic Grammar</option>
                  <option>Tajweed Visuals</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                 <div>
                    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-2">Level</label>
                    <select aria-label="Level" title="Level" className="w-full bg-black border border-slate-800 rounded-lg p-3 text-sm text-white focus:border-cyan-500 outline-none">
                      {[...Array(10)].map((_, i) => <option key={i+1}>Level {i+1}</option>)}
                    </select>
                 </div>
                 <div>
                    <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest block mb-2">Language</label>
                    <select aria-label="Language" title="Language" className="w-full bg-black border border-slate-800 rounded-lg p-3 text-sm text-white focus:border-cyan-500 outline-none">
                      <option>English</option>
                      <option>Urdu</option>
                      <option>Indonesian</option>
                      <option>French</option>
                    </select>
                 </div>
              </div>
            </div>

            <button
              onClick={handlePlaceOrder}
              disabled={activeOrder && orderProgress < 100}
              className="w-full py-4 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed text-black font-black rounded-xl transition-all uppercase tracking-widest shadow-lg active:scale-95"
            >
              Start Fabrication Order
            </button>

            {activeOrder && (
              <div className="mt-8 pt-8 border-t border-slate-800">
                <div className="flex justify-between items-center mb-2">
                   <span className="text-xs font-bold text-cyan-400">{activeOrder.id}</span>
                   <span className="text-[10px] font-mono text-slate-500">{orderProgress}%</span>
                </div>
                <div className="h-2 w-full bg-black rounded-full overflow-hidden mb-3">
                   <div
                    ref={progressBarRef}
                    className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 transition-all duration-300"
                   />
                </div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] animate-pulse">
                  CURRENT FACILITY: {orderStep}
                </p>
              </div>
            )}
          </div>

          {/* Blueprint Library */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 backdrop-blur-sm">
            <h2 className="text-2xl font-black text-white mb-6 flex items-center gap-3">
               <ClipboardList className="text-cyan-500" /> BLUEPRINT LIBRARY
            </h2>
            <div className="space-y-4">
              {blueprints.map(bp => (
                <div key={bp.id} className="p-4 bg-black/40 border border-slate-800 rounded-xl group hover:border-cyan-500/30 transition-all cursor-pointer">
                  <div className="flex justify-between items-start mb-2">
                    <div className="text-sm font-bold text-slate-200">{bp.name}</div>
                    <span className="px-2 py-0.5 bg-cyan-500/10 text-cyan-400 text-[10px] font-black rounded">{bp.status}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-slate-500 uppercase tracking-widest font-mono">TARGET: {bp.domain.toUpperCase()}</span>
                    <ExternalLink size={14} className="text-slate-600 group-hover:text-cyan-500" />
                  </div>
                </div>
              ))}
            </div>
            <button className="w-full mt-6 py-3 border border-slate-700 hover:border-slate-500 text-slate-400 hover:text-white rounded-lg text-xs font-black uppercase tracking-widest transition-all">
              Export All Blueprints
            </button>
          </div>
        </div>

        {/* Right Columns: Facility Grid */}
        <div className="xl:col-span-2 space-y-8">
           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {facilities.map(f => (
                <FacilityCard key={f.id} {...f} onOpen={() => setSelectedFacility(f)} />
              ))}
           </div>

           {/* Plant Event Log (from v8.8) */}
           <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
             <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <ShieldAlert className="text-yellow-500" /> RECENT PLANT EVENTS
             </h2>
             <div className="space-y-4">
               <div className="p-4 bg-black/50 border-l-4 border-cyan-500 rounded-r-lg">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-bold text-cyan-500 uppercase tracking-widest text-[10px]">BTO COMPLETED</span>
                    <span className="text-[10px] text-slate-600 font-mono">2 mins ago</span>
                  </div>
                  <p className="text-sm text-slate-300 font-medium">BTO-902-AL-KAHF fabrication cycle successful. Delivered to Edge Distribution.</p>
               </div>
               <div className="p-4 bg-black/50 border-l-4 border-yellow-500 rounded-r-lg opacity-80">
                  <div className="flex justify-between mb-1">
                    <span className="text-xs font-bold text-yellow-500 uppercase tracking-widest text-[10px]">REACTOR CONTAINMENT</span>
                    <span className="text-[10px] text-slate-600 font-mono">1 hour ago</span>
                  </div>
                  <p className="text-sm text-slate-300 font-medium">Theological ambiguity flag in 'Attributes of Allah' module. Resolved via HITL.</p>
               </div>
             </div>
           </div>
        </div>
      </div>

      {/* Facility Detail Modal */}
      {selectedFacility && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 w-full max-w-2xl rounded-3xl p-10 relative shadow-2xl overflow-hidden">
            <div className="absolute top-0 right-0 p-12 opacity-5 pointer-events-none">
               <selectedFacility.icon size={200} />
            </div>

            <button className="absolute top-6 right-6 text-slate-500 hover:text-white transition-colors" onClick={() => setSelectedFacility(null)}>✕</button>

            <div className="flex items-center gap-6 mb-10">
              <div className="p-6 bg-cyan-500/20 rounded-2xl text-cyan-400">
                <selectedFacility.icon size={48} />
              </div>
              <div>
                <h2 className="text-4xl font-black text-white tracking-tighter">{selectedFacility.name.toUpperCase()}</h2>
                <div className="flex gap-4 mt-2">
                   <p className="text-cyan-500 font-mono tracking-widest text-[10px]">FACILITY ID: {selectedFacility.id.toUpperCase()}-089</p>
                   <p className="text-slate-500 font-mono tracking-widest text-[10px]">SOP: INDUSTRIAL-v8.9</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-10">
              <div className="bg-black/60 p-6 rounded-2xl border border-slate-800">
                <div className="text-[10px] text-slate-500 font-black uppercase tracking-widest mb-2">Throughput Trend</div>
                <div className="h-16 flex items-end gap-1">
                  {(['h-[45%]', 'h-[72%]', 'h-[38%]', 'h-[85%]', 'h-[55%]', 'h-[91%]',
                    'h-[62%]', 'h-[48%]', 'h-[78%]', 'h-[33%]', 'h-[88%]', 'h-[65%]'] as const).map((h, i) => (
                    <div key={i} className={`bg-cyan-500/40 flex-1 rounded-t-sm ${h}`} />
                  ))}
                </div>
              </div>
              <div className="bg-black/60 p-6 rounded-2xl border border-slate-800 flex flex-col justify-center">
                <div className="text-[10px] text-slate-500 font-black uppercase tracking-widest mb-2">Active Workloads</div>
                <div className="text-3xl font-black text-white font-mono">1,402 <span className="text-xs text-slate-500">OPS/MIN</span></div>
              </div>
            </div>

            <div className="space-y-4">
               <button className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-white font-black rounded-xl transition-all uppercase tracking-widest text-xs">
                  Generate Industrial Blueprint
               </button>
               <button
                className="w-full py-4 border border-slate-700 hover:bg-white/5 text-slate-500 hover:text-white font-black rounded-xl transition-all uppercase tracking-widest text-xs"
                onClick={() => setSelectedFacility(null)}
               >
                Return to Plant Overview
               </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FabricationPlantDashboard;
