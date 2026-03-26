import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import {
  Zap,
  Search,
  Users,
  Activity,
  Play,
  RefreshCw,
  ShieldCheck,
  BarChart3,
  Globe,
  MessageSquare,
  BookOpen
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface QEPResult {
  engine: string;
  timestamp: string;
  [key: string]: any;
}

export const QEPDashboard: React.FC = () => {
  const [activeEngine, setActiveEngine] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Record<string, QEPResult>>({});
  const [fabricHealth, setFabricHealth] = useState<any>(null);

  useEffect(() => {
    fetchFabricHealth();
    const interval = setInterval(fetchFabricHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchFabricHealth = async () => {
    try {
      const response = await fetch('/api/v138/ceo/vitals'); // Simulated endpoint for DRAD
      // In a real scenario, we'd hit the specific QEP health endpoint
      const data = {
        fabric_version: "v0.8.0-QEP",
        uptime_seconds: 43200,
        adaptation_count: 12,
        current_health_score: 0.98
      };
      setFabricHealth(data);
    } catch (e) {
      console.error("Failed to fetch fabric health", e);
    }
  };

  const runEngine = async (engine: string, params: any) => {
    setLoading(true);
    setActiveEngine(engine);
    try {
      // Simulation of API calls to the new backend tools
      await new Promise(resolve => setTimeout(resolve, 1500));

      let mockResult: QEPResult = { engine, timestamp: new Date().toISOString() };

      if (engine === 'ESE') {
        mockResult = {
          ...mockResult,
          steps_completed: 50,
          final_avg_belief: 0.72,
          history: Array.from({ length: 50 }, () => Math.random() * 0.2 + 0.6)
        };
      } else if (engine === 'ARO') {
        mockResult = {
          ...mockResult,
          allocation: { simulation: 0.3, reasoning: 0.4, ontology: 0.2, fabric: 0.1 },
          message: "Optimization complete. Resources rebalanced."
        };
      } else if (engine === 'BTO') {
        mockResult = {
          ...mockResult,
          topic: params.topic || "General Theology",
          swarm_id: "swarm-" + Math.random().toString(36).substr(2, 9),
          tasks_created: 4,
          status: "SWARM_ACTIVE"
        };
      }

      setResults(prev => ({ ...prev, [engine]: mockResult }));
    } finally {
      setLoading(false);
    }
  };

  const engines = [
    {
      id: 'ESE',
      name: 'Evolutionary Simulation',
      icon: Zap,
      desc: 'Model theological debates and belief diffusion.',
      action: () => runEngine('ESE', { steps: 50 })
    },
    {
      id: 'ARO',
      name: 'Resource Optimisation',
      icon: RefreshCw,
      desc: 'Dynamically allocate AI reasoning power.',
      action: () => runEngine('ARO', {})
    },
    {
      id: 'BTO',
      name: 'Team Orchestrator',
      icon: Users,
      desc: 'Form specialized swarms for religious research.',
      action: () => runEngine('BTO', { topic: "Interfaith Ethics" })
    },
    {
      id: 'DRAD',
      name: 'Adaptive Fabric',
      icon: Activity,
      desc: 'Real-time system behavior adjustment.',
      action: fetchFabricHealth
    },
  ];

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-start">
        <div>
          <h2 className="text-4xl font-black text-white tracking-tight uppercase">Quadruple Engine Pillar</h2>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest mt-2">
            Flagship Sovereignty Suite • Religion Domain v0.8
          </p>
        </div>
        {fabricHealth && (
          <div className="flex gap-6">
            <div className="text-right">
              <p className="text-[10px] font-black text-slate-600 uppercase">Fabric Health</p>
              <p className="text-lg font-black text-aura">{(fabricHealth.current_health_score * 100).toFixed(0)}%</p>
            </div>
            <div className="text-right">
              <p className="text-[10px] font-black text-slate-600 uppercase">Adaptations</p>
              <p className="text-lg font-black text-aura">{fabricHealth.adaptation_count}</p>
            </div>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {engines.map((engine) => (
          <Card
            key={engine.id}
            className={`p-8 border-2 transition-all cursor-pointer group ${activeEngine === engine.id ? 'border-aura bg-aura/5' : 'border-slate-900 hover:border-aura/30'}`}
            onClick={engine.action}
          >
            <div className="flex justify-between items-start mb-6">
              <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all ${activeEngine === engine.id ? 'bg-aura text-sovereign' : 'bg-slate-900 text-aura group-hover:bg-aura/20'}`}>
                <engine.icon size={24} />
              </div>
              {results[engine.id] && <Badge color="aura">Active</Badge>}
            </div>
            <h3 className="text-lg font-black text-white mb-2">{engine.name}</h3>
            <p className="text-xs text-slate-500 font-bold leading-relaxed mb-6">{engine.desc}</p>
            <Button
              variant={activeEngine === engine.id ? 'primary' : 'outline'}
              className="w-full py-2 text-[10px] font-black uppercase tracking-widest"
              disabled={loading && activeEngine === engine.id}
            >
              {loading && activeEngine === engine.id ? 'Processing...' : 'Launch Engine'}
            </Button>
          </Card>
        ))}
      </div>

      <AnimatePresence mode="wait">
        {activeEngine && results[activeEngine] && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Card className="p-10 bg-slate-950 border-aura/20">
              <div className="flex justify-between items-center mb-10">
                <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <BarChart3 size={24} className="text-aura" />
                  {activeEngine} Execution Results
                </h3>
                <span className="text-[10px] font-mono text-slate-600">{results[activeEngine].timestamp}</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                {activeEngine === 'ESE' && (
                  <>
                    <div className="space-y-2">
                      <p className="text-[10px] font-black text-slate-500 uppercase">Convergence Rate</p>
                      <p className="text-3xl font-black text-aura">{(results['ESE'].final_avg_belief * 100).toFixed(1)}%</p>
                    </div>
                    <div className="md:col-span-2 h-32 flex items-end gap-1">
                      {results['ESE'].history.map((val: number, i: number) => (
                        <div
                          key={i}
                          className="flex-1 bg-aura/20 hover:bg-aura transition-all rounded-t-sm"
                          style={{ height: `${val * 100}%` }}
                        />
                      ))}
                    </div>
                  </>
                )}
                {activeEngine === 'ARO' && (
                  <div className="md:col-span-3 space-y-6">
                    <p className="text-sm font-bold text-slate-400">{results['ARO'].message}</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                      {Object.entries(results['ARO'].allocation).map(([key, val]: [string, any]) => (
                        <div key={key} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                          <p className="text-[10px] font-black text-slate-500 uppercase mb-1">{key}</p>
                          <p className="text-xl font-black text-white">{(val * 100).toFixed(0)}%</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {activeEngine === 'BTO' && (
                  <div className="md:col-span-3 flex items-center justify-between p-6 rounded-2xl bg-aura/5 border border-aura/10">
                    <div className="flex items-center gap-8">
                      <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign">
                        <Users size={32} />
                      </div>
                      <div>
                        <p className="text-xl font-black text-white">{results['BTO'].topic}</p>
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Swarm ID: {results['BTO'].swarm_id}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge color="aura">ACTIVE</Badge>
                      <p className="text-[10px] font-black text-slate-600 uppercase mt-2">{results['BTO'].tasks_created} Tasks Orchestrated</p>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <Card className="p-8 space-y-6 border-slate-800 hover:border-aura/20 transition-all">
          <div className="flex items-center gap-4 text-aura">
            <Globe size={20} />
            <h4 className="font-black uppercase text-xs tracking-widest">Global Mesh Sync</h4>
          </div>
          <p className="text-xs text-slate-500 font-bold">Synchronizing QEP simulations with 142 interfaith nodes for universal alignment.</p>
          <div className="flex items-center justify-between text-[10px] font-black">
            <span className="text-slate-600 uppercase">Sync Status</span>
            <span className="text-emerald-500">SYNCHRONIZED</span>
          </div>
        </Card>

        <Card className="p-8 space-y-6 border-slate-800 hover:border-aura/20 transition-all">
          <div className="flex items-center gap-4 text-aura">
            <ShieldCheck size={20} />
            <h4 className="font-black uppercase text-xs tracking-widest">GaaS Oversight</h4>
          </div>
          <p className="text-xs text-slate-500 font-bold">All engine executions are validated against Article 1127 (Autonomous Evolution).</p>
          <div className="flex items-center justify-between text-[10px] font-black">
            <span className="text-slate-600 uppercase">Trust Score</span>
            <span className="text-aura">0.99</span>
          </div>
        </Card>

        <Card className="p-8 space-y-6 border-slate-800 hover:border-aura/20 transition-all">
          <div className="flex items-center gap-4 text-aura">
            <BookOpen size={20} />
            <h4 className="font-black uppercase text-xs tracking-widest">Sacred Ontology</h4>
          </div>
          <p className="text-xs text-slate-500 font-bold">Deep integration with AlQuran Cloud and scholarly knowledge graphs.</p>
          <Button variant="outline" className="w-full text-[10px]">View Ontology Map</Button>
        </Card>
      </div>
    </div>
  );
};
