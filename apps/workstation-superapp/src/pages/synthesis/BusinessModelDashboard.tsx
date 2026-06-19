import React from 'react';
import { Card, Badge, Button, toast } from '@workstation/ui';
import { BarChart3, TrendingUp, Users, Zap, ShieldCheck, PieChart, ArrowUpRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export const BusinessModelDashboard: React.FC<{ data: any }> = ({ data }) => {
  const chartData = [
    { name: 'Year 1', value: data.projections.year_1 },
    { name: 'Year 3', value: data.projections.year_3 },
    { name: 'Year 5', value: data.projections.year_5 },
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
         <StatCard label="Market Size" value="$4.2B" icon={TrendingUp} color="text-aura" />
         <StatCard label="ROI Efficiency" value="+28%" icon={Zap} color="text-highlight" />
         <StatCard label="Swarm Multiplier" value="2.4x" icon={Users} color="text-vital" />
         <StatCard label="GaaS Alignment" value="0.99" icon={ShieldCheck} color="text-emerald-500" />
      </div>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
         <Card className="@[440px]:col-span-8 p-8 border-slate-900 bg-slate-950/40">
            <h3 className="text-sm font-black text-white uppercase tracking-widest mb-10 flex items-center gap-3">
               <BarChart3 size={18} className="text-aura" />
               Revenue Projections (LTSA Offering)
            </h3>
            <div className="h-[300px] w-full">
               <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                     <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                     <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#475569', fontSize: 10, fontWeight: 'bold'}} />
                     <YAxis axisLine={false} tickLine={false} tick={{fill: '#475569', fontSize: 10, fontWeight: 'bold'}} />
                     <Tooltip
                        contentStyle={{backgroundColor: '#020617', border: '1px solid #1e293b', borderRadius: '12px'}}
                        itemStyle={{color: '#64ffda', fontSize: '10px', fontWeight: 'black', textTransform: 'uppercase'}}
                     />
                     <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                        {chartData.map((entry, index) => (
                           <Cell key={`cell-${index}`} fill={index === 2 ? '#64ffda' : '#1e293b'} />
                        ))}
                     </Bar>
                  </BarChart>
               </ResponsiveContainer>
            </div>
         </Card>

         <Card className="@[440px]:col-span-4 p-8 bg-aura/5 border-aura/20 flex flex-col justify-between">
            <div>
               <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Market Strategy</h3>
               <p className="text-xs text-slate-400 font-bold leading-relaxed">
                  The <span className="text-white">Long-Term Safety Assurance (LTSA)</span> model prioritizes early adopter integration with a 30% reduction in attrition targets.
               </p>
            </div>
            <div className="space-y-4 pt-10">
               <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                  <span>Adoption Velocity</span>
                  <span className="text-aura">High</span>
               </div>
               <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
                  <div className="h-full bg-aura w-3/4" />
               </div>
               <Button onClick={() => toast('PDF export coming in next release — strategy data available via the AI CEO chat')} className="w-full bg-white text-sovereign text-[9px] uppercase font-black py-4">Download Strategy PDF</Button>
            </div>
         </Card>
      </div>

      <Card className="p-8 border-slate-900 bg-slate-950/20">
         <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6 flex items-center gap-3">
            <PieChart size={18} className="text-highlight" />
            QEP Simulation Parameters
         </h3>
         <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <SimParam label="ESE Adoption" value="Early Adopter" detail="15% Market Share" />
            <SimParam label="ARO Efficiency" value="SciPy Optimized" detail="28% Gain" />
            <SimParam label="BTO Velocity" value="Swarm Active" detail="2.4x Multiplier" />
         </div>
      </Card>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color }: any) => (
  <Card className="p-6 flex items-center gap-6 bg-slate-950/40 border-slate-900">
     <div className={`p-4 rounded-2xl bg-slate-900 border border-slate-800 ${color}`}>
        <Icon size={24} />
     </div>
     <div>
        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
        <p className="text-2xl font-black text-white">{value}</p>
     </div>
  </Card>
);

const SimParam = ({ label, value, detail }: any) => (
  <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800">
     <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">{label}</p>
     <p className="text-sm font-black text-white uppercase">{value}</p>
     <p className="text-[9px] text-aura font-bold mt-2">{detail}</p>
  </div>
);
