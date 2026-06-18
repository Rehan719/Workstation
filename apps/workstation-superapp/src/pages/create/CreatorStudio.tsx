import React, { useState, useCallback, useRef } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  applyEdgeChanges,
  applyNodeChanges,
  Node,
  Edge,
  Connection
} from 'reactflow';
import 'reactflow/dist/style.css';
import axios from 'axios';
import {
  Wand2, Database, Plus, Save, Play, Sparkles,
  Download, X, ChevronRight, Loader2, CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import componentRegistry from '@workstation/shared/data/component_registry.json';

// ── Types ────────────────────────────────────────────────────────────────────

interface BlueprintResponse {
  status: string;
  blueprint_id: string;
  name: string;
  stage: string;
  realm: string;
  domain: string;
  deliverable: string;
  nodes: Array<{ id: string; label: string; position: { x: number; y: number } }>;
  generated_at: number;
}

const REALMS = [
  'general', 'technology', 'enterprise', 'education',
  'science', 'law', 'care', 'employment', 'religion', 'learning', 'scholarship',
];
const STAGES = ['concept', 'design', 'build', 'launch', 'commercialise'];

// ── Component ────────────────────────────────────────────────────────────────

export const CreatorStudio: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [intent, setIntent]       = useState('');
  const [realm, setRealm]         = useState('enterprise');
  const [stage, setStage]         = useState('concept');
  const [blueprint, setBlueprint] = useState<BlueprintResponse | null>(null);
  const [showDeliverable, setShowDeliverable] = useState(false);
  const [error, setError]         = useState('');
  const deliverableRef            = useRef<HTMLPreElement>(null);

  const onNodesChange = useCallback(
    (changes: any) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes: any) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );
  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    []
  );

  const addNode = (component: any) => {
    const id = `node-${Date.now()}`;
    setNodes((nds) => nds.concat({
      id,
      data: { label: component.name },
      position: { x: 120 + nds.length * 40, y: 150 + nds.length * 40 },
      style: { background: '#0f172a', color: '#64ffda', border: '1px solid #64ffda', borderRadius: 12 },
    }));
  };

  const handleAIGenerate = async () => {
    if (!intent.trim()) return;
    setIsGenerating(true);
    setError('');
    setBlueprint(null);
    try {
      const res = await axios.post<BlueprintResponse>('/api/v290/ceo/generate-blueprint', {
        intent,
        realm,
        stage,
        domain: realm,
      });
      const bp = res.data;
      setBlueprint(bp);
      setShowDeliverable(true);

      // Populate canvas with the pipeline nodes from the AI response
      const newNodes: Node[] = bp.nodes.map((n) => ({
        id: n.id,
        data: { label: n.label },
        position: n.position,
        style: { background: '#0f172a', color: '#64ffda', border: '1px solid #64ffda', borderRadius: 12 },
      }));
      // Auto-connect sequential nodes
      const newEdges: Edge[] = newNodes.slice(1).map((n, i) => ({
        id: `e${i}-${i+1}`,
        source: newNodes[i].id,
        target: n.id,
        animated: true,
        style: { stroke: '#64ffda' },
      }));
      setNodes(newNodes);
      setEdges(newEdges);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? err?.message ?? 'Blueprint generation failed.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExport = () => {
    if (!blueprint) return;
    const content = [
      `# ${blueprint.name}`,
      ``,
      `**Stage:** ${blueprint.stage}  |  **Realm:** ${blueprint.realm}  |  **Domain:** ${blueprint.domain}`,
      `**Generated:** ${new Date(blueprint.generated_at * 1000).toLocaleString()}`,
      ``,
      `---`,
      ``,
      blueprint.deliverable,
    ].join('\n');
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `blueprint-${blueprint.blueprint_id.slice(0,8)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleSaveCanvas = () => {
    const data = { nodes, edges, blueprint: blueprint?.name, generated_at: Date.now() };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `canvas-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="h-[calc(100vh-10rem)] flex flex-col gap-4">
      {/* Header */}
      <header className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tighter uppercase">Creator Studio</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em] mt-0.5">
            AI Blueprint Generator · Concept → Commercialise
          </p>
        </div>
        <div className="flex gap-3">
          <button
            type="button"
            onClick={handleSaveCanvas}
            className="px-4 py-2 border border-slate-800 rounded-xl font-black text-xs text-slate-400 hover:text-white transition-all flex items-center gap-2 uppercase tracking-widest"
          >
            <Save size={14} /> Save Canvas
          </button>
          {blueprint && (
            <button
              type="button"
              onClick={handleExport}
              className="px-4 py-2 bg-aura text-sovereign rounded-xl font-black text-xs flex items-center gap-2 uppercase tracking-widest hover:opacity-90 transition-opacity"
            >
              <Download size={14} /> Export Blueprint
            </button>
          )}
        </div>
      </header>

      <div className="flex-1 flex gap-5 min-h-0">
        {/* Left sidebar — component palette */}
        <aside className="w-56 flex flex-col gap-4 overflow-y-auto pr-1 shrink-0">
          {componentRegistry.categories.map(cat => (
            <div key={cat.id} className="space-y-2">
              <h3 className="text-[9px] font-black uppercase text-slate-500 tracking-[0.2em]">{cat.name}</h3>
              <div className="space-y-1">
                {cat.components.map(comp => (
                  <button
                    key={comp.id}
                    type="button"
                    onClick={() => addNode(comp)}
                    className="w-full p-3 rounded-xl bg-slate-900/40 border border-white/5 hover:border-aura/30 transition-all flex items-center gap-3 group text-left"
                  >
                    <Database size={12} className="text-slate-500 group-hover:text-aura transition-colors shrink-0" />
                    <span className="text-[10px] font-bold text-slate-300 truncate">{comp.name}</span>
                    <Plus size={10} className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                  </button>
                ))}
              </div>
            </div>
          ))}
        </aside>

        {/* Main canvas area */}
        <main className={`flex-1 flex flex-col gap-4 min-w-0 transition-all ${showDeliverable ? 'max-w-[54%]' : 'max-w-full'}`}>
          {/* Intent bar */}
          <div className="shrink-0 p-4 rounded-2xl border border-aura/20 bg-aura/5 flex flex-col gap-3">
            <div className="flex gap-3 items-center">
              <div className="p-2 bg-aura/20 text-aura rounded-xl shrink-0">
                <Sparkles size={16} />
              </div>
              <input
                value={intent}
                onChange={(e) => setIntent(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAIGenerate()}
                placeholder="Describe what you want to build…"
                aria-label="Blueprint intent"
                className="flex-1 bg-transparent border-none outline-none font-bold text-sm placeholder-slate-600 text-white"
              />
            </div>
            <div className="flex gap-3 items-center">
              <select
                value={realm}
                onChange={e => setRealm(e.target.value)}
                aria-label="Realm"
                className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-[10px] font-black uppercase text-white focus:outline-none focus:border-aura"
              >
                {REALMS.map(r => <option key={r} value={r}>{r.charAt(0).toUpperCase()+r.slice(1)}</option>)}
              </select>
              <select
                value={stage}
                onChange={e => setStage(e.target.value)}
                aria-label="Stage"
                className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-[10px] font-black uppercase text-white focus:outline-none focus:border-aura"
              >
                {STAGES.map(s => <option key={s} value={s}>{s.charAt(0).toUpperCase()+s.slice(1)}</option>)}
              </select>
              <button
                type="button"
                onClick={handleAIGenerate}
                disabled={isGenerating || !intent.trim()}
                className="ml-auto px-5 py-1.5 bg-aura text-sovereign font-black rounded-xl flex items-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-40 text-[10px] uppercase tracking-widest"
              >
                {isGenerating ? <Loader2 size={12} className="animate-spin" /> : <Wand2 size={12} />}
                {isGenerating ? 'Generating…' : 'AI Generate'}
              </button>
            </div>
            {error && (
              <p className="text-[10px] text-red-400 px-1">{error}</p>
            )}
            {blueprint && !error && (
              <div className="flex items-center gap-2 text-[9px] font-black text-aura uppercase tracking-widest">
                <CheckCircle2 size={11} />
                {blueprint.name}
                <button
                  type="button"
                  onClick={() => setShowDeliverable(v => !v)}
                  className="ml-auto flex items-center gap-1 text-slate-500 hover:text-white transition-colors"
                >
                  {showDeliverable ? 'Hide' : 'Show'} deliverable
                  <ChevronRight size={10} className={`transition-transform ${showDeliverable ? 'rotate-180' : ''}`} />
                </button>
              </div>
            )}
          </div>

          {/* ReactFlow canvas */}
          <div className="flex-1 bg-slate-950/50 border border-white/5 rounded-[2rem] relative overflow-hidden">
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

            {nodes.length === 0 && !isGenerating && (
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                <Wand2 size={32} className="text-slate-700 mb-3" />
                <p className="text-xs text-slate-600 font-bold">Type an intent above and click AI Generate</p>
                <p className="text-[9px] text-slate-700 mt-1">or drag components from the left palette</p>
              </div>
            )}

            {isGenerating && (
              <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/80 pointer-events-none">
                <Loader2 size={28} className="text-aura animate-spin mb-3" />
                <p className="text-xs text-aura font-black uppercase tracking-widest">AI CEO is synthesising your blueprint…</p>
              </div>
            )}

            <div className="absolute bottom-4 right-4">
              <button
                type="button"
                onClick={handleAIGenerate}
                disabled={isGenerating || !intent.trim()}
                className="flex items-center gap-2 px-5 py-2.5 bg-vital text-white font-black rounded-xl hover:opacity-90 transition-opacity disabled:opacity-40 text-[9px] uppercase tracking-widest shadow-lg shadow-vital/20"
              >
                <Play size={12} fill="currentColor" />
                Run Pipeline
              </button>
            </div>
          </div>
        </main>

        {/* Right panel — deliverable */}
        <AnimatePresence>
          {showDeliverable && blueprint && (
            <motion.div
              initial={{ opacity: 0, width: 0 }}
              animate={{ opacity: 1, width: 380 }}
              exit={{ opacity: 0, width: 0 }}
              className="shrink-0 flex flex-col bg-slate-950 border border-slate-800 rounded-[2rem] overflow-hidden"
            >
              <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800 shrink-0">
                <div>
                  <p className="text-[10px] font-black uppercase tracking-widest text-aura">Blueprint Deliverable</p>
                  <p className="text-[8px] text-slate-500 mt-0.5 capitalize">{blueprint.stage} · {blueprint.realm}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleExport}
                    aria-label="Export blueprint as markdown"
                    className="p-1.5 text-slate-500 hover:text-aura transition-colors"
                  >
                    <Download size={13} />
                  </button>
                  <button
                    type="button"
                    aria-label="Close deliverable panel"
                    onClick={() => setShowDeliverable(false)}
                    className="p-1.5 text-slate-500 hover:text-white transition-colors"
                  >
                    <X size={13} />
                  </button>
                </div>
              </div>
              <div className="flex-1 overflow-y-auto p-5">
                <pre
                  ref={deliverableRef}
                  className="text-[10px] text-slate-300 font-mono leading-relaxed whitespace-pre-wrap"
                >
                  {blueprint.deliverable}
                </pre>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
