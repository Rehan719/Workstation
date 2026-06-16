import React, { useState, useEffect } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { MessageSquare, Users, TrendingUp, ShieldAlert, CheckCircle } from 'lucide-react';
import { motion } from 'framer-motion';

export const DebateLog: React.FC = () => {
  const [log, setLog] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/v138/ceo/meeting/log')
      .then(res => res.json())
      .then(data => setLog(Array.isArray(data) ? data : []))
      .catch(() => setLog([]));
  }, []);

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter italic">C-Suite Debate Log</h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.4em] mt-2">v0.1 Asynchronous Consensus Monitoring</p>
      </header>

      <div className="grid grid-cols-1 gap-6">
        {log.map((entry, i) => (
          <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
             <Card className="p-6 border-slate-800 bg-slate-950/40">
                <div className="flex justify-between items-start mb-4">
                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-xl bg-aura/10 flex items-center justify-center text-aura font-black">
                         {entry.agent?.[0]}
                      </div>
                      <div>
                         <p className="text-sm font-black text-white uppercase">{entry.agent}</p>
                         <p className="text-[10px] text-slate-500 font-mono">{entry.timestamp}</p>
                      </div>
                   </div>
                   <Badge color={entry.vote === 'APPROVE' ? 'emerald-500' : 'vital'}>{entry.vote}</Badge>
                </div>
                <p className="text-slate-400 text-sm leading-relaxed">{entry.argument}</p>
             </Card>
          </motion.div>
        ))}
        {log.length === 0 && (
           <Card className="p-12 text-center border-dashed border-slate-800">
              <MessageSquare className="mx-auto text-slate-700 mb-4" size={48} />
              <p className="text-slate-500 font-bold uppercase text-xs tracking-widest">No active debates detected in this epoch.</p>
           </Card>
        )}
      </div>
    </div>
  );
};
