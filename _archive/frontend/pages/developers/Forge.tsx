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
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import { Plus, Play, Rocket, Terminal, Download, Sparkles, Wrench, CheckCircle2, ChevronDown, ChevronUp } from 'lucide-react';
import { Button, Card, toast } from '@workstation/ui';

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

interface BlueprintResult {
  deliverable: string;
  blueprint_id: string;
  name: string;
  stage: string;
}

export const Forge: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [isSimulating, setIsSimulating] = useState(false);
  const [showToolWizard, setShowToolWizard] = useState(false);
  const [blueprint, setBlueprint] = useState<BlueprintResult | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [toolName, setToolName] = useState('');
  const [toolDesc, setToolDesc] = useState('');

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
    setBlueprint(null);
    const nodeLabels = nodes.map(n => n.data?.label ?? n.id).join(', ');
    const intent = `Simulate and analyse this agent pipeline: ${nodeLabels}. Provide a blueprint for connecting these components into a working agentic workflow.`;
    try {
      const res = await axios.post<BlueprintResult>('/api/v290/ceo/generate-blueprint', {
        intent,
        realm: 'developer',
        stage: 'design',
        domain: 'technology',
      });
      setBlueprint(res.data);
      setShowResult(true);
      toast('Blueprint generated — AI analysis complete.');
    } catch {
      toast('Backend offline — start the API server to run real simulations.');
    } finally {
      setIsSimulating(false);
    }
  };

  const exportBlueprint = () => {
    const data = blueprint
      ? { blueprint_id: blueprint.blueprint_id, name: blueprint.name, deliverable: blueprint.deliverable, nodes, edges }
      : { nodes, edges, version: '3.0.0-forge' };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `forge-blueprint.json`;
    a.click();
  };

  const deployToSynthesis = () => {
    if (!blueprint?.deliverable) { toast('Run simulation first to generate a blueprint.'); return; }
    const md = `# Forge Blueprint\n\n${blueprint.deliverable}`;
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `forge-blueprint.md`;
    a.click();
    toast('Blueprint exported as Markdown — import into Synthesis Studio.');
  };

  const addNode = (label: string) => {
    const id = `node-${Date.now()}`;
    setNodes((nds) => nds.concat({
      id,
      position: { x: 120 + nds.length * 40, y: 100 + nds.length * 40 },
      data: { label },
      style: { background: '#0f172a', color: '#fff', border: '1px solid #1e293b' },
    }));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] space-y-6">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-5xl font-black mb-1 text-white tracking-tighter uppercase break-words">The Forge</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Visual Agent Composer · AI-Powered Blueprint</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
          <Button onClick={() => setShowToolWizard(true)} variant="outline" className="border-aura/30 text-aura"><Wrench size={16} /> Tool Wizard</Button>
          <Button variant="outline" onClick={exportBlueprint}><Download size={16} /> Export JSON</Button>
          <Button onClick={handleSimulate} disabled={isSimulating}>
            {isSimulating ? <Sparkles size={16} className="animate-spin" /> : <Play size={16} />}
            {isSimulating ? 'Generating…' : 'Run AI Blueprint'}
          </Button>
          <Button onClick={deployToSynthesis} className="bg-white text-sovereign"><Rocket size={16} /> Deploy MD</Button>
        </div>
      </header>

      {/* AI Blueprint result panel */}
      {blueprint && (
        <Card className="border-aura/30 bg-aura/5">
          <button
            type="button"
            onClick={() => setShowResult(r => !r)}
            className="w-full flex items-center justify-between p-6 text-left"
          >
            <div className="flex items-center gap-3">
              <CheckCircle2 size={18} className="text-emerald-400" />
              <span className="font-black text-white text-sm uppercase tracking-widest">AI Blueprint: {blueprint.name}</span>
            </div>
            {showResult ? <ChevronUp size={16} className="text-aura" /> : <ChevronDown size={16} className="text-aura" />}
          </button>
          {showResult && (
            <div className="px-6 pb-6">
              <pre className="text-xs text-slate-300 bg-slate-950 rounded-2xl p-6 whitespace-pre-wrap leading-relaxed font-mono overflow-auto max-h-64 border border-slate-800">
                {blueprint.deliverable}
              </pre>
            </div>
          )}
        </Card>
      )}

      <div className="flex-1 flex gap-6 min-h-0">
        <aside className="w-64 space-y-6">
          <Card className="p-6">
            <h3 className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">Modules</h3>
            <div className="space-y-2">
              {['LLM Core', 'Memory', 'Search Tool', 'Guardrail', 'Classifier', 'Router'].map(m => (
                <button type="button" key={m} onClick={() => addNode(m)} className="w-full p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs font-bold text-slate-400 hover:text-white hover:border-aura/50 transition-all text-left flex items-center gap-3">
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
            <p className="text-[10px] text-slate-500 font-bold leading-relaxed">Agent Communication Protocol active. AI CEO analyses node topology and generates real blueprints.</p>
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

      {showToolWizard && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-10">
          <Card className="max-w-2xl w-full p-12 space-y-10 border-aura/30 shadow-[0_0_50px_rgba(100,255,218,0.1)]">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-4xl font-black text-white uppercase tracking-tighter">Tool Creation Wizard</h3>
                <p className="text-aura font-black text-[10px] uppercase tracking-[0.4em] mt-2">v0.3 Dynamic Integration</p>
              </div>
              <button type="button" onClick={() => setShowToolWizard(false)} className="p-3 bg-slate-900 rounded-xl text-slate-500 hover:text-white">Close</button>
            </div>
            <div className="space-y-6">
              <div className="space-y-3">
                <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest pl-2">Tool Name</label>
                <input
                  value={toolName}
                  onChange={e => setToolName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-900 rounded-2xl p-5 text-white font-bold"
                  placeholder="e.g. fetch_planetary_data"
                />
              </div>
              <div className="space-y-3">
                <label className="text-[10px] font-black text-slate-500 uppercase tracking-widest pl-2">Description</label>
                <textarea
                  value={toolDesc}
                  onChange={e => setToolDesc(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-900 rounded-2xl p-5 text-white font-bold h-32"
                  placeholder="Describe what the tool does for the AI CEO…"
                />
              </div>
              <Button
                className="w-full bg-aura text-sovereign py-6 rounded-2xl font-black uppercase text-xs tracking-widest"
                onClick={() => {
                  if (toolName.trim()) {
                    addNode(`${toolName.trim()} (TOOL)`);
                    toast(`Tool "${toolName}" registered and added to canvas.`);
                    setToolName('');
                    setToolDesc('');
                    setShowToolWizard(false);
                  }
                }}
              >
                Register Tool
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
