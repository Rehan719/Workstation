import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { Play, Pause, SkipForward, SkipBack, Volume2, Maximize2, X, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Slide {
  id: number;
  title: string;
  content: string;
  narration: string;
  animation?: string;
  sound?: string;
  visual?: string;
}

export const PresentationPlayer: React.FC<{ slides: Slide[]; onClose: () => void }> = ({ slides, onClose }) => {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [playing, setPlaying] = useState(true);
  const [progress, setProgress] = useState(0);

  const currentSlide = slides[currentIdx];

  useEffect(() => {
    if (!playing) return;

    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          if (currentIdx < slides.length - 1) {
            setCurrentIdx(c => c + 1);
            return 0;
          } else {
            setPlaying(false);
            return 100;
          }
        }
        return prev + 2; // ~5 seconds per slide
      });
    }, 100);

    return () => clearInterval(interval);
  }, [playing, currentIdx, slides.length]);

  return (
    <div className="fixed inset-0 z-[100] bg-sovereign flex flex-col p-10 animate-in fade-in duration-500">
      <header className="flex justify-between items-center mb-10">
         <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-aura flex items-center justify-center text-sovereign shadow-2xl shadow-aura/20">
               <Sparkles size={24} />
            </div>
            <div>
               <h2 className="text-xl font-black text-white uppercase tracking-tighter">AI CEO Presentation</h2>
               <p className="text-[10px] text-aura font-black uppercase tracking-widest">Sovereign Studio v1.0 • Autonomous Narration Active</p>
            </div>
         </div>
         <button onClick={onClose} className="p-4 rounded-full bg-slate-900 border border-slate-800 text-slate-500 hover:text-white transition-all">
            <X size={24} />
         </button>
      </header>

      <div className="flex-1 flex gap-10 min-h-0">
         {/* Slide Content */}
         <Card className="flex-1 p-20 bg-slate-950/40 border-slate-900 relative overflow-hidden flex flex-col justify-center text-center">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.02)_0%,transparent_70%)]" />

            <AnimatePresence mode="wait">
               <motion.div
                 key={currentIdx}
                 initial={{ opacity: 0, scale: 0.95, y: 20 }}
                 animate={{ opacity: 1, scale: 1, y: 0 }}
                 exit={{ opacity: 0, scale: 1.05, y: -20 }}
                 transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
                 className="relative z-10 space-y-10"
               >
                  <h1 className="text-7xl font-black text-white tracking-tighter uppercase italic leading-tight">
                    {currentSlide.title}
                  </h1>
                  <p className="text-2xl text-slate-400 font-bold max-w-4xl mx-auto leading-relaxed">
                    {currentSlide.content}
                  </p>
                  {currentSlide.visual && (
                    <div className="w-64 h-64 bg-slate-900 border border-slate-800 rounded-3xl mx-auto flex items-center justify-center italic text-slate-700 uppercase font-black text-[10px] tracking-widest">
                       [ {currentSlide.visual.split('/').pop()} ]
                    </div>
                  )}
               </motion.div>
            </AnimatePresence>
         </Card>

         {/* Narration Sidebar */}
         <div className="w-96 flex flex-col gap-6">
            <Card className="p-8 bg-aura/5 border-aura/20">
               <div className="flex items-center gap-3 text-aura mb-6">
                  <Volume2 size={18} />
                  <span className="text-[10px] font-black uppercase tracking-[0.2em]">AI Narration Script</span>
               </div>
               <p className="text-sm text-slate-300 font-bold leading-relaxed italic">
                  "{currentSlide.narration}"
               </p>
            </Card>

            <Card className="flex-1 p-8 bg-slate-950 border-slate-900 overflow-y-auto custom-scrollbar">
               <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-6">Presentation Outline</h3>
               <div className="space-y-4">
                  {slides.map((s, i) => (
                    <div
                      key={s.id}
                      onClick={() => { setCurrentIdx(i); setProgress(0); }}
                      className={`p-4 rounded-xl border transition-all cursor-pointer ${i === currentIdx ? 'bg-aura/10 border-aura' : 'bg-slate-900 border-slate-800 opacity-40 hover:opacity-100'}`}
                    >
                       <p className="text-[10px] font-black text-white uppercase tracking-widest truncate">{i+1}. {s.title}</p>
                    </div>
                  ))}
               </div>
            </Card>
         </div>
      </div>

      {/* Controls */}
      <footer className="mt-10 flex items-center gap-10">
         <div className="flex items-center gap-4">
            <button onClick={() => { setCurrentIdx(c => Math.max(0, c - 1)); setProgress(0); }} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"><SkipBack size={20} /></button>
            <button
              onClick={() => setPlaying(!playing)}
              className="w-20 h-20 rounded-3xl bg-white text-sovereign flex items-center justify-center shadow-2xl shadow-white/10 hover:scale-105 transition-transform"
            >
               {playing ? <Pause size={32} /> : <Play size={32} className="ml-1" />}
            </button>
            <button onClick={() => { setCurrentIdx(c => Math.min(slides.length - 1, c + 1)); setProgress(0); }} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"><SkipForward size={20} /></button>
         </div>

         <div className="flex-1 space-y-3">
            <div className="flex justify-between text-[10px] font-black uppercase text-slate-500 tracking-widest">
               <span>Slide {currentIdx + 1} of {slides.length}</span>
               <span>{progress.toFixed(0)}% Synchronized</span>
            </div>
            <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
               <motion.div
                 className="h-full bg-aura"
                 animate={{ width: `${progress}%` }}
                 transition={{ duration: 0.1 }}
               />
            </div>
         </div>

         <button className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"><Maximize2 size={20} /></button>
      </footer>
    </div>
  );
};
