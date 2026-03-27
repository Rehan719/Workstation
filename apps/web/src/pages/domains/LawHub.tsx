import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Layers, Landmark, History } from 'lucide-react';
import { motion } from 'framer-motion';
import { QEPDashboard } from '../../components/QEPDashboard';
import { QEPImmersiveTools } from '../../components/QEPImmersiveTools';
import { useAdaptiveUI } from '../../components/AdaptiveUIProvider';

export const LawHub: React.FC = () => {
  const { layout, emotionalAdjustment } = useAdaptiveUI();
  const [activeTab, setActiveTab] = useState('compliance');

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase">Bastion of Order</h1>
          <div className="flex items-center gap-4">
             <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Legal Framework • Constitutional Mesh • Law Hub</p>
             <Badge color="highlight" className="text-[8px]">{layout} MODE</Badge>
             <Badge color="aura" className="text-[8px]">{emotionalAdjustment} TONE</Badge>
          </div>
        </div>
        <div className="flex gap-4">
           <Button variant="outline"><History size={18} /> Precedent</Button>
           <Button className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Landmark size={18} /> New Treaty
           </Button>
        </div>
      </header>

      <Card className="p-10 space-y-10">
         <div className="flex justify-between items-center border-b border-white/5 pb-8">
            <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
               <Layers size={24} className="text-aura" />
               Legislative Engines
            </h3>
            <div className="flex gap-4 p-1 rounded-2xl bg-slate-900 border border-slate-800">
               <button onClick={() => setActiveTab('compliance')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'compliance' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>Compliance</button>
               <button onClick={() => setActiveTab('qep')} className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'qep' ? 'bg-slate-800 text-aura shadow-lg' : 'text-slate-500 hover:text-white'}`}>QEP Flagship</button>
            </div>
         </div>

         <div className="space-y-12">
            {activeTab === 'qep' ? (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-12">
                 <QEPDashboard domain="law" />
                 <div className="pt-12 border-t border-white/5">
                    <h3 className="text-3xl font-black text-white mb-10 uppercase tracking-tighter">Constitutional Simulation</h3>
                    <QEPImmersiveTools domain="law" />
                 </div>
              </motion.div>
            ) : (
              <div className="p-20 text-center border-2 border-dashed border-slate-900 rounded-[3rem]">
                 <p className="text-slate-600 font-black uppercase tracking-widest">Awaiting legal data ingestion...</p>
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};
