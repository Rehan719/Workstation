import React, { useRef, useMemo, useState, useEffect, useCallback } from 'react';
import * as THREE from 'three';
import ReactFlow, { Background, Controls, Node, Edge, applyNodeChanges, applyEdgeChanges, addEdge, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';
import { Card, Badge, Button } from '@workstation/ui';
import { Binary, Search, Info, GitMerge, Fingerprint, Activity, Zap, Shield, Play, History, Edit, FileCode, GitBranch, Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useStore, gaas } from '@workstation/shared';

// Mock Genome Data
const GENOME_DATA = {
  root_hash: "0x82f1...galactic",
  nodes: Array.from({ length: 50 }, (_, i) => ({
    id: `node-${i}`,
    hash: `0x${Math.random().toString(16).slice(2, 10)}`,
    type: i % 5 === 0 ? 'OPERON' : i % 3 === 0 ? 'REGULON' : 'GENE',
    label: i % 5 === 0 ? `Operon-${i/5}` : i % 3 === 0 ? `Regulon-${Math.floor(i/3)}` : `Gene-${i}`,
    connections: [Math.floor(Math.random() * 50), Math.floor(Math.random() * 50)]
  }))
};

const ThreeGenomeVisualizer: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

    renderer.setSize(width, height);
    mountRef.current.appendChild(renderer.domElement);

    const nodesGroup = new THREE.Group();
    const spheres: THREE.Mesh[] = [];

    GENOME_DATA.nodes.forEach((node) => {
      const geometry = new THREE.SphereGeometry(0.2, 16, 16);
      const material = new THREE.MeshPhongMaterial({
        color: node.type === 'OPERON' ? 0x64ffda : node.type === 'REGULON' ? 0x38bdf8 : 0x94a3b8,
        emissive: node.type === 'OPERON' ? 0x64ffda : 0x000000,
        emissiveIntensity: 0.2
      });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10);
      spheres.push(sphere);
      nodesGroup.add(sphere);
    });

    scene.add(nodesGroup);
    scene.add(new THREE.AmbientLight(0x404040));
    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);

    camera.position.z = 12;

    const animate = () => {
      requestAnimationFrame(animate);
      nodesGroup.rotation.y += 0.002;
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      const w = mountRef.current?.clientWidth || width;
      const h = mountRef.current?.clientHeight || height;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div className="relative w-full h-[600px] glass-card rounded-3xl overflow-hidden border border-white/5 bg-slate-950/40">
       <div ref={mountRef} className="w-full h-full" />
       <div className="absolute top-6 left-6 pointer-events-none">
          <div className="flex items-center gap-3 p-3 bg-slate-900/80 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl">
             <div className="p-2 bg-aura/20 rounded-xl"><Activity size={18} className="text-aura animate-pulse" /></div>
             <div>
                <p className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Visualizer State</p>
                <p className="text-xs font-black text-white uppercase tracking-widest">Merkle-DAG Integrity: 100%</p>
             </div>
          </div>
       </div>
    </div>
  );
};

export const GenomeExplorer: React.FC = () => {
  const [activeView, setActiveView] = useState('EXPLORER');
  const { user } = useStore();

  const handleGaaSCommit = async (action: string, metadata: any) => {
    const res = await gaas.validateAction(action, user?.did || 'anonymous', metadata);
    alert(`GaaS Validation [${action}]: ${res.valid ? 'AUTHORIZED' : 'DENIED'} (Score: ${res.score})`);
  };

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-5xl font-black text-white uppercase tracking-tighter italic">Sovereign Genome</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.4em] mt-2">v138.0 Galactic Era • Epigenetic Master Layer</p>
        </div>
        <div className="flex gap-4">
           {['EXPLORER', 'GRN', 'METHYLATION', 'TRANSCRIPTIONAL', 'LINEAGE'].map(view => (
             <button
               key={view}
               onClick={() => setActiveView(view)}
               className={`px-6 py-3 rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all ${
                 activeView === view ? 'bg-aura text-sovereign shadow-[0_0_20px_rgba(100,255,218,0.3)]' : 'bg-slate-900 text-slate-500 hover:text-white border border-slate-800'
               }`}
             >
               {view}
             </button>
           ))}
        </div>
      </header>

      <div className="grid grid-cols-12 gap-8">
        <div className="col-span-12 xl:col-span-9 space-y-8">
           {activeView === 'EXPLORER' && (
             <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
               <ThreeGenomeVisualizer />
             </motion.div>
           )}

           {activeView === 'GRN' && (
              <Card className="h-[600px] p-0 overflow-hidden relative border border-aura/30 bg-slate-950/40">
                 <ReactFlow
                   nodes={[
                     { id: 'reg-1', position: { x: 250, y: 50 }, data: { label: 'Regulon-Alpha' }, style: { background: '#0f172a', color: '#64ffda', border: '1px solid #64ffda' } },
                     { id: 'gene-1', position: { x: 100, y: 200 }, data: { label: 'Gene-A1' }, style: { background: '#0f172a', color: '#94a3b8', border: '1px solid #1e293b' } },
                     { id: 'gene-2', position: { x: 400, y: 200 }, data: { label: 'Gene-B2' }, style: { background: '#0f172a', color: '#94a3b8', border: '1px solid #1e293b' } }
                   ]}
                   edges={[
                     { id: 'e1-1', source: 'reg-1', target: 'gene-1', animated: true, style: { stroke: '#64ffda' } },
                     { id: 'e1-2', source: 'reg-1', target: 'gene-2', animated: true, style: { stroke: '#64ffda' } }
                   ]}
                   fitView
                   className="bg-sovereign"
                 >
                    <Background color="#1e293b" gap={20} />
                    <Controls className="!bg-slate-900 !border-slate-800 !fill-aura" />
                    <div className="absolute top-4 left-4 p-3 bg-slate-900/80 border border-aura/30 rounded-xl z-10">
                       <p className="text-[10px] font-black text-aura uppercase tracking-widest">Active Regulon: Alpha (Fidelity 0.99)</p>
                    </div>
                 </ReactFlow>
              </Card>
           )}

           {activeView === 'METHYLATION' && (
              <Card className="p-10 space-y-8">
                 <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                    <Fingerprint size={24} className="text-vital" />
                    Methylation Manager
                 </h3>
                 <div className="space-y-4">
                    {['Promoter-X1', 'Enhancer-Sovereign', 'Silencer-Bio-A'].map((site, i) => (
                      <div key={site} className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex justify-between items-center group hover:border-vital/30 transition-all">
                         <div>
                            <p className="text-sm font-black text-white uppercase mb-1">{site}</p>
                            <p className="text-[10px] font-bold text-slate-500">Coordinate: Chr1-42.5k</p>
                         </div>
                         <div className="flex gap-4 items-center">
                            <span className={`text-[10px] font-black uppercase tracking-widest ${i === 2 ? 'text-vital' : 'text-aura'}`}>
                               {i === 2 ? 'METHYLATED' : 'DEMETHYLATED'}
                            </span>
                            <button
                               onClick={() => handleGaaSCommit('METHYLATION_EDIT', { site })}
                               className="p-2 bg-slate-900 rounded-lg text-slate-500 hover:text-white transition-colors border border-slate-800"
                            >
                               <Edit size={14} />
                            </button>
                         </div>
                      </div>
                    ))}
                 </div>
              </Card>
           )}

           {activeView === 'TRANSCRIPTIONAL' && (
              <Card className="p-10 space-y-8">
                 <div className="flex justify-between items-center">
                    <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                       <FileCode size={24} className="text-highlight" />
                       Transcriptional Rule Editor
                    </h3>
                    <Button variant="outline" onClick={() => handleGaaSCommit('RULE_CREATION', { type: 'custom' })}><Plus size={16} /> Create Rule</Button>
                 </div>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {[
                      { name: 'On-Stress-Synthesis', trigger: 'Energy < 20%', action: 'Upregulate Operon-4' },
                      { name: 'Self-Modification-Veto', trigger: 'GaaS.score < 0.9', action: 'Terminate Subprocess' }
                    ].map((rule, i) => (
                      <div key={i} className="p-6 rounded-2xl bg-slate-950 border border-slate-800 group hover:border-highlight/30 transition-all">
                         <div className="flex justify-between mb-4">
                            <span className="text-[10px] font-black text-highlight uppercase tracking-widest">Rule-v{i+1}</span>
                            <Badge color="highlight">ACTIVE</Badge>
                         </div>
                         <h4 className="font-black text-white mb-2">{rule.name}</h4>
                         <p className="text-[10px] text-slate-500 uppercase font-black mb-1">IF: {rule.trigger}</p>
                         <p className="text-[10px] text-aura uppercase font-black">THEN: {rule.action}</p>
                      </div>
                    ))}
                 </div>
              </Card>
           )}

           {activeView === 'LINEAGE' && (
              <Card className="p-10 space-y-8">
                 <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                    <GitBranch size={24} className="text-aura" />
                    Evolutionary Lineage
                 </h3>
                 <div className="flex flex-col gap-8 relative before:absolute before:left-[11px] before:top-2 before:bottom-0 before:w-0.5 before:bg-slate-900">
                    {[
                      { v: 'v138.0', msg: 'Galactic Era Synthesis: Sovereign Genome Decoupled', date: 'T-0h' },
                      { v: 'v131.2', msg: 'Sovereign Twin Integration', date: 'T-42d' },
                      { v: 'v100.0', msg: 'Apotheosis Baseline: First Consciousness Achieved', date: 'T-1y' }
                    ].map((h, i) => (
                      <div key={i} className="flex gap-8 relative z-10">
                         <div className="w-6 h-6 rounded-full bg-aura shadow-[0_0_10px_rgba(100,255,218,0.5)] flex-shrink-0" />
                         <div>
                            <div className="flex items-center gap-3 mb-1">
                               <span className="text-lg font-black text-white">{h.v}</span>
                               <span className="text-[10px] font-mono text-slate-600 uppercase">{h.date}</span>
                            </div>
                            <p className="text-sm font-bold text-slate-400">{h.msg}</p>
                         </div>
                      </div>
                    ))}
                 </div>
              </Card>
           )}

           <div className="grid grid-cols-3 gap-6">
              {[
                { label: 'Total Operons', value: '142', icon: Binary, color: 'text-aura' },
                { label: 'Active Regulons', value: '12.5k', icon: Zap, color: 'text-highlight' },
                { label: 'Integrity Score', value: '0.999', icon: Shield, color: 'text-vital' }
              ].map((stat, i) => (
                <Card key={i} className="p-6 flex items-center gap-6">
                   <div className={`p-4 rounded-2xl bg-slate-950 border border-slate-900 ${stat.color}`}>
                      <stat.icon size={24} />
                   </div>
                   <div>
                      <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{stat.label}</p>
                      <p className="text-2xl font-black text-white">{stat.value}</p>
                   </div>
                </Card>
              ))}
           </div>
        </div>

        <div className="col-span-12 xl:col-span-3 space-y-8">
           <Card className="p-8">
              <h4 className="text-xs font-black text-white uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Expression Tuning</h4>
              <div className="space-y-8">
                 {[
                   { label: 'Epigenetic Flux', val: 78 },
                   { label: 'Transcriptional Pressure', val: 42 },
                   { label: 'Evolutionary Intensity', val: 91 }
                 ].map((slider, i) => (
                   <div key={i} className="space-y-3">
                      <div className="flex justify-between items-center">
                         <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{slider.label}</label>
                         <span className="text-[10px] font-black text-aura">{slider.val}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden border border-white/5">
                         <div className="h-full bg-aura shadow-[0_0_10px_rgba(100,255,218,0.5)]" style={{ width: `${slider.val}%` }}></div>
                      </div>
                   </div>
                 ))}
                 <button
                    onClick={() => handleGaaSCommit('EXPRESSION_TUNING', { flux: 78 })}
                    className="w-full py-4 bg-aura/10 border border-aura/30 rounded-2xl text-[10px] font-black text-aura uppercase tracking-[0.2em] hover:bg-aura hover:text-sovereign transition-all"
                 >
                    Commit Changes (GaaS)
                 </button>
              </div>
           </Card>

           <Card className="p-8">
              <h4 className="text-xs font-black text-white uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Methylation Status</h4>
              <div className="space-y-4">
                 {['Promoter-A1', 'Enhancer-X', 'Silencer-Z'].map((tag, i) => (
                   <div key={i} className="flex justify-between items-center p-3 rounded-xl bg-slate-950 border border-slate-900">
                      <span className="text-[10px] font-black text-slate-300 uppercase">{tag}</span>
                      <Badge color={i === 2 ? 'vital' : 'aura'}>{i === 2 ? 'METHYLATED' : 'ACTIVE'}</Badge>
                   </div>
                 ))}
              </div>
           </Card>
        </div>
      </div>
    </div>
  );
};
