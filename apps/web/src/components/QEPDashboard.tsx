import React, { useState } from 'react';
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
  BookOpen,
  Cpu,
  Brain,
  MessageCircle,
  Share2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface QEPResult {
  engine: string;
  timestamp: string;
  [key: string]: any;
}

interface QEPDashboardProps {
  domain?: 'religion' | 'science' | 'law' | 'employment' | 'education' | 'care';
}

export const QEPDashboard: React.FC<QEPDashboardProps> = ({ domain = 'religion' }) => {
  const [activeEngine, setActiveEngine] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Record<string, QEPResult>>({});

  const runEngine = async (engine: string) => {
    setLoading(true);
    setActiveEngine(engine);
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      const mockResult: QEPResult = {
        engine,
        timestamp: new Date().toISOString(),
        status: 'OPTIMAL',
        domain_context: domain
      };
      setResults(prev => ({ ...prev, [engine]: mockResult }));
    } finally {
      setLoading(false);
    }
  };

  const engines = [
    { id: 'ESE', name: 'Simulation', icon: Zap, desc: `Model ${domain} scenarios and outcomes.` },
    { id: 'ARO', name: 'Optimisation', icon: RefreshCw, desc: `Dynamically allocate ${domain} resources.` },
    { id: 'BTO', name: 'Orchestrator', icon: Users, desc: `Form specialized ${domain} swarms.` },
    { id: 'DRAD', name: 'Adaptive Fabric', icon: Activity, desc: `Real-time system behavior adjustment.` },
  ];

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-start">
        <div>
          <h2 className="text-4xl font-black text-white tracking-tight uppercase">Quadruple Engine Pillar</h2>
          <p className="text-slate-500 font-bold uppercase text-[10px] tracking-widest mt-2">
            Cross-Domain Flagship v1.0 • {domain.toUpperCase()} Hub
          </p>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {engines.map((engine) => (
          <Card
            key={engine.id}
            className={`p-8 border-2 transition-all cursor-pointer group ${activeEngine === engine.id ? 'border-aura bg-aura/5' : 'border-slate-900 hover:border-aura/30'}`}
            onClick={() => runEngine(engine.id)}
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
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <Card className="p-10 bg-slate-950 border-aura/20">
              <div className="flex justify-between items-center mb-10">
                <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <BarChart3 size={24} className="text-aura" />
                  {activeEngine} Execution Results
                </h3>
                <span className="text-[10px] font-mono text-slate-600">{results[activeEngine].timestamp}</span>
              </div>
              <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                 <p className="text-[10px] font-black text-slate-500 uppercase mb-2">Context: {results[activeEngine].domain_context}</p>
                 <p className="text-xl font-black text-white">Engine running at 100% fidelity for {domain} domain.</p>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
