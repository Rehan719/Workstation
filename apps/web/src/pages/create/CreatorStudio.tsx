import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, Save, Play, Rocket, Database, Layers, Settings2, HelpCircle, Sparkles, Wand2 } from 'lucide-react';
import axios from 'axios';
import componentRegistry from '../../../../packages/shared/data/component_registry.json';

export const CreatorStudio: React.FC = () => {
  const [nodes, setNodes] = useState<any[]>([]);

  const [isGenerating, setIsGenerating] = useState(false);
  const [intent, setIntent] = useState('');

  const addNode = (component: any) => {
    const newNode = {
      id: `node-${Date.now()}`,
      type: component.id,
      name: component.name,
      icon: component.icon,
      position: { x: 100, y: 100 + nodes.length * 80 }
    };
    setNodes([...nodes, newNode]);
  };

  const handleAIGenerate = async () => {
    if (!intent.trim()) return;
    setIsGenerating(true);
    try {
       const res = await axios.post('/api/v290/ceo/generate-blueprint', { intent });
       const newNodes = res.data.nodes.map((n: any, i: number) => ({
          id: n.id,
          name: n.type,
          type: n.type,
          position: { x: 100, y: 100 + i * 120 }
       }));
       setNodes(newNodes);
    } catch (err) {
       console.error("AI Generation failed");
    } finally {
       setIsGenerating(false);
    }
  };

  return (
    <div className="h-[calc(100vh-10rem)] flex flex-col gap-6">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-black mb-1 neon-text">Creator Studio</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest">Visual Reactor Foundry v150.0</p>
        </div>
        <div className="flex gap-4">
           <button className="px-6 py-3 border border-slate-800 rounded-xl font-bold flex items-center gap-2 text-slate-400 hover:text-white transition-all">
             <Save size={18} />
             Save Blueprint
           </button>
           <button className="px-6 py-3 bg-aura text-sovereign font-black rounded-xl flex items-center gap-2 hover:scale-105 transition-all shadow-lg shadow-aura/20">
             <Rocket size={18} />
             Publish to Marketplace
           </button>
        </div>
      </header>

      <div className="flex-1 flex gap-8 min-h-0">
        {/* Component Palette */}
        <aside className="w-80 flex flex-col gap-8">
           {componentRegistry.categories.map(cat => (
             <div key={cat.id} className="space-y-4">
                <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-[0.2em]">{cat.name}</h3>
                <div className="space-y-2">
                   {cat.components.map(comp => (
                     <button
                       key={comp.id}
                       onClick={() => addNode(comp)}
                       className="w-full p-4 rounded-2xl bg-slate-900/40 border border-white/5 hover:border-aura/30 hover:bg-slate-900/60 transition-all flex items-center gap-4 group text-left"
                     >
                       <div className="p-2 bg-surface rounded-lg text-slate-500 group-hover:text-aura transition-colors">
                          <Layers size={18} />
                       </div>
                       <span className="text-xs font-bold">{comp.name}</span>
                       <Plus size={14} className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                     </button>
                   ))}
                </div>
             </div>
           ))}
        </aside>

        {/* Visual Canvas (Simulated React Flow) */}
        <main className="flex-1 flex flex-col gap-6">
           <div className="p-6 glass-card border-aura/30 bg-aura/5 flex gap-4 items-center shadow-lg shadow-aura/5">
              <div className="p-3 bg-aura/20 text-aura rounded-xl">
                 <Sparkles size={20} />
              </div>
              <input
                 value={intent}
                 onChange={(e) => setIntent(e.target.value)}
                 placeholder="Describe what you want to build (e.g. 'Climate data analyzer')..."
                 className="flex-1 bg-transparent border-none outline-none font-bold text-lg placeholder-slate-600"
              />
              <button
                onClick={handleAIGenerate}
                disabled={isGenerating}
                className="px-6 py-2 bg-aura text-sovereign font-black rounded-xl flex items-center gap-2 hover:scale-105 transition-all disabled:opacity-50"
              >
                <Wand2 size={16} />
                {isGenerating ? 'Synthesizing...' : 'AI Generate'}
              </button>
           </div>

        <div className="flex-1 bg-sovereign/40 border border-white/5 rounded-[2.5rem] relative overflow-hidden group">
           <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(100,255,218,0.03)_0%,transparent_70%)]"></div>
           <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(#ffffff22 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>

           <div className="relative h-full p-10">
              {nodes.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center gap-6 text-center">
                   <div className="w-20 h-20 rounded-full bg-aura/10 flex items-center justify-center text-aura animate-pulse">
                      <HelpCircle size={40} />
                   </div>
                   <div className="space-y-2">
                      <h3 className="text-2xl font-black">Empty Canvas</h3>
                      <p className="text-slate-500 font-bold max-w-xs">Drag and drop components from the palette to start building your reactor.</p>
                   </div>
                </div>
              ) : (
                <div className="space-y-4">
                   {nodes.map((node, i) => (
                     <motion.div
                       key={node.id}
                       initial={{ opacity: 0, x: -20 }}
                       animate={{ opacity: 1, x: 0 }}
                       className="w-72 p-6 glass-card border-aura/20 bg-aura/5 flex items-center gap-4 relative"
                     >
                        <div className="p-3 bg-surface rounded-xl text-aura">
                           <Layers size={20} />
                        </div>
                        <div>
                           <p className="text-[10px] font-black text-slate-500 uppercase">Node {i+1}</p>
                           <p className="font-bold">{node.name}</p>
                        </div>
                        <Settings2 size={16} className="ml-auto text-slate-600 hover:text-white cursor-pointer" />

                        {i < nodes.length - 1 && (
                          <div className="absolute top-full left-1/2 -translate-x-1/2 h-4 w-[2px] bg-aura/30"></div>
                        )}
                     </motion.div>
                   ))}
                </div>
              )}
           </div>

           {/* Sandbox Controls */}
           <div className="absolute bottom-8 right-8">
              <button className="flex items-center gap-3 px-8 py-4 bg-vital text-white font-black rounded-2xl hover:scale-105 transition-all shadow-xl shadow-vital/20 uppercase tracking-widest text-xs">
                <Play size={18} fill="currentColor" />
                Run Sandbox
              </button>
           </div>
        </div>
        </main>
      </div>
    </div>
  );
};
