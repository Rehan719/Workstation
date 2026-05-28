import React from 'react';
import { Card, Badge } from '@workstation/ui';
import { FlaskConical, Beaker, Zap, Activity } from 'lucide-react';

export const PetriDish: React.FC = () => {
  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-4xl font-black text-white uppercase tracking-tighter italic">Petri Dish</h1>
        <p className="text-highlight font-black uppercase text-[10px] tracking-[0.3em]">Micro-Scale Agent Evolution • Emergent Behavior Sandbox</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <Card className="p-8 space-y-4">
          <div className="w-12 h-12 rounded-xl bg-highlight/20 flex items-center justify-center text-highlight">
            <Activity size={24} />
          </div>
          <h3 className="text-xl font-black text-white uppercase">Active Culture A-14</h3>
          <p className="text-sm text-slate-400">Observing self-organizing gossip protocols in 50 low-parameter agents.</p>
          <Badge color="highlight">In Vitro</Badge>
        </Card>
      </div>
    </div>
  );
};
