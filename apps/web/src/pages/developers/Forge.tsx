import React, { useState, useCallback } from 'react';
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
import { Plus, Save, Play, Rocket, Terminal, Download, FileJson, Search, Sparkles } from 'lucide-react';
import { Button, Card, Badge } from '@workstation/ui';
import { useStore, gaas } from '@workstation/shared';

const initialNodes: Node[] = [
  {
    id: 'node-1',
    type: 'default',
    position: { x: 100, y: 100 },
    data: { label: 'Phi-3-Mini (MODEL)' },
    style: { background: '#0f172a', color: '#64ffda', border: '1px solid #64ffda' }
  },
  {
    id: 'node-2',
    type: 'default',
    position: { x: 100, y: 250 },
    data: { label: 'Search-Adapter (TOOL)' },
    style: { background: '#0f172a', color: '#38bdf8', border: '1px solid #38bdf8' }
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: 'node-1', target: 'node-2', animated: true, style: { stroke: '#64ffda' } },
];

export const Forge: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isSimulating, setIsSimulating] = useState(false);
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

    setTimeout(() => {
       setIsSimulating(false);
       alert(`Simulation Complete! GaaS Score: ${validation.score || 0.99}`);
    }, 1500);
  };

  const exportBlueprint = () => {
    const blueprint = { nodes, edges, version: '3.0.0-galactic' };
    const blob = new Blob([JSON.stringify(blueprint, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `agent-blueprint.json`;
    a.click();
  };

  const addNode = (label: string) => {
    const id = `node-${nodes.length + 1}`;
    const newNode: Node = {
      id,
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label },
      style: { background: '#0f172a', color: '#fff', border: '1px solid #1e293b' }
    };
    setNodes((nds) => nds.concat(newNode));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] space-y-6">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-5xl font-black mb-1 text-white tracking-tighter uppercase">The Forge</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Visual Agent Composer • Galactic Era Standard</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline" onClick={exportBlueprint}><Download size={16} /> Export</Button>
           <Button onClick={handleSimulate} disabled={isSimulating}>
              {isSimulating ? <Sparkles size={16} className="animate-spin" /> : <Play size={16} />}
              {isSimulating ? 'Simulating...' : 'Run Reactor'}
           </Button>
           <Button className="bg-white text-sovereign"><Rocket size={16} /> Deploy</Button>
        </div>
      </header>

      <div className="flex-1 flex gap-6 min-h-0">
        <aside className="w-64 space-y-6">
           <Card className="p-6">
              <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Modules</h3>
              <div className="space-y-2">
                 {['LLM Core', 'Memory', 'Search Tool', 'Guardrail'].map(m => (
                   <button key={m} onClick={() => addNode(m)} className="w-full p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs font-bold text-slate-400 hover:text-white hover:border-aura/50 transition-all text-left flex items-center gap-3">
                      <Plus size={14} /> {m}
                   </button>
                 ))}
              </div>
           </Card>
           <Card className="p-6">
              <div className="flex items-center gap-2 text-aura mb-4">
                 <Terminal size={16} />
                 <span className="text-[10px] font-black uppercase tracking-widest">A2A v3.0</span>
              </div>
              <p className="text-[10px] text-slate-500 font-bold leading-relaxed">Agent Communication Protocol active. Blueprints are interoperable.</p>
           </Card>
        </aside>

        <main className="flex-1 bg-slate-950/50 rounded-[2.5rem] border border-slate-800 overflow-hidden relative">
           <ReactFlow
             nodes={nodes}
             edges={edges}
             onNodesChange={onNodesChange}
             onEdgesChange={onEdgesChange}
             onConnect={onConnect}
             fitView
             className="bg-sovereign"
           >
             <Background color="#1e293b" gap={20} />
             <Controls />
             <MiniMap nodeColor="#0f172a" maskColor="rgba(0,0,0,0.5)" className="!bg-slate-950 !border-slate-800" />
           </ReactFlow>
        </main>
      </div>
    </div>
  );
};
