import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  applyEdgeChanges,
  applyNodeChanges,
  Node,
  Edge,
  Connection
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import { Wand2, ShieldCheck, Terminal, Cpu, Database, Plus, Save, Play, Sparkles, HelpCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import componentRegistry from '../../../../packages/shared/data/component_registry.json';

export const CreatorStudio: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [intent, setIntent] = useState('');

  const onNodesChange = useCallback(
    (changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [setNodes]
  );
  const onEdgesChange = useCallback(
    (changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [setEdges]
  );
  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  );

  const addNode = (component: any) => {
    const newNode: Node = {
      id: `node-${Date.now()}`,
      data: { label: component.name },
      position: { x: 100, y: 100 + nodes.length * 50 },
      className: 'bg-slate-900 border-aura border-2 rounded-xl text-white font-bold p-4 shadow-lg'
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const handleAIGenerate = async () => {
    if (!intent.trim()) return;
    setIsGenerating(true);
    try {
       const res = await axios.post('/api/v290/ceo/generate-blueprint', { intent });
       const newNodes: Node[] = res.data.nodes.map((n: any, i: number) => ({
          id: n.id,
          data: { label: n.type },
          position: { x: 100 + (i * 200), y: 200 },
          className: 'bg-slate-900 border-aura border-2 rounded-xl text-white font-bold p-4 shadow-lg'
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
          <h1 className="text-4xl font-black mb-1 neon-text">Reality Forge</h1>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest text-highlight">Universe Scale Creation v153.0 (ReactFlow Enabled)</p>
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
        <aside className="w-80 flex flex-col gap-8 overflow-y-auto pr-2 custom-scrollbar">
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
                          <Database size={18} />
                       </div>
                       <span className="text-xs font-bold text-slate-300">{comp.name}</span>
                       <Plus size={14} className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity" />
                     </button>
                   ))}
                </div>
             </div>
           ))}
        </aside>

        <main className="flex-1 flex flex-col gap-6">
           <div className="p-6 glass-card border-aura/30 bg-aura/5 flex gap-4 items-center shadow-lg shadow-aura/5">
              <div className="p-3 bg-aura/20 text-aura rounded-xl">
                 <Sparkles size={20} />
              </div>
              <input
                 value={intent}
                 onChange={(e) => setIntent(e.target.value)}
                 placeholder="Describe what you want to build (e.g. 'Climate data analyzer')..."
                 className="flex-1 bg-transparent border-none outline-none font-bold text-lg placeholder-slate-600 text-white"
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

           <div className="flex-1 bg-slate-950/50 border border-white/5 rounded-[2.5rem] relative overflow-hidden group">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                fitView
              >
                <Background color="#1e293b" gap={20} />
                <Controls />
              </ReactFlow>

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
