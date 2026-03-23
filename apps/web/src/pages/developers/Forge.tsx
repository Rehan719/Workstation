import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  applyEdgeChanges,
  applyNodeChanges,
  Node,
  Edge,
  Connection,
  ReactFlowProvider
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Plus, Save, Play, Rocket, Layers, Wand2, ShieldCheck, Terminal, Cpu, Database, Sparkles, Box, Info, Trash2, Download, FileJson } from 'lucide-react';
import { Button, Card, Badge, ModuleNode, RecombinerNode } from '@workstation/ui';
import { useStore, gaas } from '@workstation/shared';

const nodeTypes = {
  module: ModuleNode,
  recombiner: RecombinerNode,
};

const initialNodes: Node[] = [
  {
    id: 'node-1',
    type: 'module',
    position: { x: 100, y: 100 },
    data: { label: 'Phi-3-Mini', type: 'MODEL' }
  },
  {
    id: 'node-2',
    type: 'module',
    position: { x: 100, y: 250 },
    data: { label: 'Search-Adapter', type: 'ADAPTER' }
  },
  {
    id: 'recombiner-1',
    type: 'recombiner',
    position: { x: 450, y: 175 },
    data: { strategy: 'TIES-Merge' }
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-r1', source: 'node-1', target: 'recombiner-1', animated: true, style: { stroke: '#64ffda' } },
  { id: 'e2-r1', source: 'node-2', target: 'recombiner-1', animated: true, style: { stroke: '#64ffda' } },
];

export const Forge: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const { user } = useStore();

  const onNodesChange = useCallback(
    (changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#64ffda' } }, eds)),
    []
  );

  const handleSimulate = async () => {
    setIsSimulating(true);
    const validation = await gaas.validateAction('AGENT_SIMULATION', user?.did || 'anonymous', { nodeCount: nodes.length });

    if (validation.allowed) {
       setTimeout(() => {
          setSimulationResult({
             fitness: 0.92,
             latency: '42ms',
             compliance: '100%',
             article: validation.article_id
          });
          setIsSimulating(false);
       }, 1500);
    }
  };

  const exportBlueprint = () => {
    const blueprint = {
      version: "3.0.0",
      metadata: {
        name: "Custom-Agent-v3",
        author: user?.did || "anonymous",
        fitness_score: simulationResult?.fitness || 0,
        hash: "did:vsb:blueprint:" + Math.random().toString(16).substring(2)
      },
      architecture: {
        nodes: nodes.map(n => ({ id: n.id, type: n.type, data: n.data })),
        edges: edges.map(e => ({ id: e.id, source: e.source, target: e.target }))
      }
    };

    const blob = new Blob([JSON.stringify(blueprint, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agent-blueprint-v3.json`;
    a.click();
  };

  const addModule = (type: string) => {
    const id = `node-${nodes.length + 1}`;
    const newNode: Node = {
      id,
      type: 'module',
      position: { x: 50, y: 50 + (nodes.length * 50) },
      data: { label: `New ${type}`, type }
    };
    setNodes((nds) => nds.concat(newNode));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] space-y-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-5xl font-black mb-1 text-white tracking-tighter uppercase">The Forge</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Visual Agent Composer • Article 1095 Recombination</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline" onClick={exportBlueprint}><Download size={16} /> Export Blueprint</Button>
           <Button onClick={handleSimulate} disabled={isSimulating}>
              {isSimulating ? <Sparkles size={16} className="animate-spin" /> : <Play size={16} />}
              {isSimulating ? 'Simulating...' : 'Run Digital Reactor'}
           </Button>
           <Button className="bg-white text-sovereign"><Rocket size={16} /> Deploy Agent</Button>
        </div>
      </header>

      <div className="flex-1 flex gap-6 min-h-0">
        <aside className="w-80 flex flex-col gap-6">
           <Card className="p-6 space-y-6 flex-1 overflow-y-auto custom-scrollbar">
              <div>
                 <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Module Palette</h3>
                 <div className="grid grid-cols-2 gap-3">
                    {['MODEL', 'ADAPTER', 'TOOL', 'GUARD', 'GENOME'].map(type => (
                      <button
                        key={type}
                        onClick={() => addModule(type)}
                        className="p-4 rounded-2xl bg-slate-950 border border-slate-800 hover:border-aura/50 transition-all flex flex-col items-center gap-2 group"
                      >
                         <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                            <Plus size={18} />
                         </div>
                         <span className="text-[9px] font-black text-slate-400 group-hover:text-white uppercase tracking-widest">{type}</span>
                      </button>
                    ))}
                 </div>
              </div>

              <div className="pt-6 border-t border-slate-800">
                 <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Standards</h3>
                 <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800">
                       <span className="text-[9px] font-black text-slate-400 uppercase">ACP/A2A v3.0</span>
                       <Badge color="emerald-500">READY</Badge>
                    </div>
                 </div>
              </div>

              {simulationResult && (
                <div className="pt-6 border-t border-slate-800 animate-in fade-in slide-in-from-bottom-4">
                   <h3 className="text-[10px] font-black uppercase text-aura tracking-widest mb-4">Reactor Preview</h3>
                   <div className="p-4 rounded-2xl bg-aura/5 border border-aura/20 space-y-4">
                      <div className="flex justify-between items-end">
                         <span className="text-[10px] font-black text-slate-500 uppercase">Fitness Score</span>
                         <span className="text-xl font-black text-aura">{simulationResult.fitness * 100}%</span>
                      </div>
                      <div className="flex justify-between items-end">
                         <span className="text-[10px] font-black text-slate-500 uppercase">Est. Latency</span>
                         <span className="text-xs font-black text-white">{simulationResult.latency}</span>
                      </div>
                   </div>
                </div>
              )}
           </Card>

           <Card className="p-6 bg-sovereign/40 border-slate-800">
              <div className="flex items-center gap-4 text-slate-400">
                 <Info size={20} />
                 <p className="text-[10px] font-bold uppercase tracking-widest leading-relaxed">Agent blueprints are exported in the v3.0 standard format for third-party adoption.</p>
              </div>
           </Card>
        </aside>

        <main className="flex-1 bg-slate-950/50 rounded-[2.5rem] border border-slate-800 overflow-hidden relative group">
           <ReactFlow
             nodes={nodes}
             edges={edges}
             onNodesChange={onNodesChange}
             onEdgesChange={onEdgesChange}
             onConnect={onConnect}
             nodeTypes={nodeTypes}
             fitView
             className="bg-sovereign"
           >
             <Background color="#1e293b" gap={20} />
             <Controls className="!bg-slate-900 !border-slate-800 !fill-aura" />
             <MiniMap
                nodeStrokeColor={(n) => n.type === 'recombiner' ? '#64ffda' : '#1e293b'}
                nodeColor={(n) => n.type === 'recombiner' ? 'rgba(100, 255, 218, 0.1)' : '#0f172a'}
                maskColor="rgba(0, 0, 0, 0.5)"
                className="!bg-slate-950 !border-slate-800 !rounded-2xl"
             />
           </ReactFlow>

           <div className="absolute top-6 right-6 flex gap-2">
              <button className="p-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-500 hover:text-white transition-all"><FileJson size={18} /></button>
              <button className="p-3 bg-slate-900 border border-slate-800 rounded-xl text-slate-500 hover:text-aura transition-all"><Terminal size={18} /></button>
           </div>
        </main>
      </div>
    </div>
  );
};
