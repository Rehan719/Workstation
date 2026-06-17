import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, BarChart3, PieChart, Activity, CheckCircle2, ChevronRight, FileJson } from 'lucide-react';

export const UVAIDDashboard: React.FC = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setResult({
        fidelity: 0.9998,
        entropy: 0.24,
        synthesis_ready: true,
        patterns: ["Recursive Logic detected", "Cross-Domain Alignment found"]
      });
      setAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="space-y-12 animate-in fade-in duration-1000">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6 border-b border-white/5 pb-8">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black neon-text !text-aura mb-2 break-words">UVAID / GSE</h1>
          <p className="text-slate-500 font-bold text-lg">Universal Visionary Artificial Intelligence & Grand Synthesis Engine.</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <div className="px-6 py-3 bg-aura/10 border border-aura/30 rounded-xl flex items-center gap-3">
              <Activity size={18} className="text-aura" />
              <span className="text-xs font-black text-aura uppercase tracking-widest">Synthesis Engine Online</span>
           </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <ToolCard title="Data Ingestion" description="Ingest multi-modal data streams for civilizational analysis." icon={FileJson} />
        <ToolCard title="Visionary Synthesis" description="Predictive modeling of large-scale organizational patterns." icon={BarChart3} />
        <ToolCard title="GSE Deployment" description="Commit synthesized data to the planetary knowledge graph." icon={CheckCircle2} />
      </div>

      <section className="p-12 glass-card flex flex-col items-center justify-center gap-8 min-h-[400px] border-aura/20">
         {!result && !analyzing && (
           <div className="text-center space-y-6">
             <div className="w-24 h-24 rounded-full bg-aura/10 border border-aura/30 flex items-center justify-center mx-auto group cursor-pointer hover:scale-110 transition-transform" onClick={handleUpload}>
                <Upload size={40} className="text-aura group-hover:animate-bounce" />
             </div>
             <div className="space-y-2">
                <h3 className="text-2xl font-black text-white">Upload Synthesis Source</h3>
                <p className="text-slate-400 font-bold max-w-md mx-auto">Drop a JSON, CSV, or Neural Manifest to begin the Grand Synthesis.</p>
             </div>
             <button onClick={handleUpload} className="px-10 py-4 bg-aura text-sovereign font-black rounded-2xl hover:scale-105 transition-all">Begin Ingestion</button>
           </div>
         )}

         {analyzing && (
            <div className="text-center space-y-8">
               <div className="w-20 h-20 border-4 border-aura/20 border-t-aura rounded-full animate-spin mx-auto"></div>
               <p className="text-aura font-black uppercase tracking-[0.3em] animate-pulse">Analyzing Frequencies...</p>
            </div>
         )}

         {result && (
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="w-full space-y-8">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black">Synthesis Report</h3>
                  <button onClick={() => setResult(null)} className="text-slate-500 hover:text-white font-bold text-xs uppercase tracking-widest">Clear Analysis</button>
               </div>
               <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="p-8 rounded-3xl bg-surface border border-white/5 space-y-6">
                     <div className="flex justify-between items-end">
                        <p className="text-[10px] font-black text-slate-500 uppercase">System Fidelity</p>
                        <p className="text-3xl font-black text-aura">{(result.fidelity * 100).toFixed(2)}%</p>
                     </div>
                     <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full bg-aura shadow-[0_0_15px_rgba(100,255,218,0.5)]" style={{ width: '99.98%' }}></div>
                     </div>
                  </div>
                  <div className="p-8 rounded-3xl bg-surface border border-white/5">
                     <p className="text-[10px] font-black text-slate-500 uppercase mb-4">Detected Patterns</p>
                     <div className="space-y-3">
                        {result.patterns.map((p: string, i: number) => (
                          <div key={i} className="flex items-center gap-3 text-sm font-bold text-slate-300 bg-white/5 p-3 rounded-xl border border-white/5">
                             <ChevronRight size={14} className="text-aura" />
                             {p}
                          </div>
                        ))}
                     </div>
                  </div>
               </div>
            </motion.div>
         )}
      </section>
    </div>
  );
};

const ToolCard = ({ title, description, icon: Icon }: any) => (
  <div className="p-8 glass-card group border-white/5 hover:border-aura/30">
    <div className="w-12 h-12 rounded-xl bg-surface border border-white/5 flex items-center justify-center mb-6 group-hover:bg-aura group-hover:text-sovereign transition-all">
      <Icon size={24} />
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-xs text-slate-500 font-bold leading-relaxed">{description}</p>
  </div>
);
