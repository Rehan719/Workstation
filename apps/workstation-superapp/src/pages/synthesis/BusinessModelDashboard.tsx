import React from 'react';
import { Card, Badge, Button, toast } from '@workstation/ui';
import { BarChart3, TrendingUp, Users, Zap, PieChart, ArrowUpRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// W407 — the four stat cards below were HARDCODED ("$4.2B", "+28%", "2.4x", "0.99") and rendered
// identically whatever the model returned, and the chart read data.projections.* unconditionally.
// Upstream, synthesis/api.py used to graft a fixed template's sim_results and the literal
// projections {4.5e7, 2.1e8, 8.4e8} onto real model output when the model omitted them, so a
// genuine result and invented financials were rendered side by side with nothing distinguishing
// them. Both ends now report absence as absence.
const fmtMoney = (n: unknown): string => {
  if (typeof n !== "number" || !isFinite(n)) return "—";
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  return `$${n.toLocaleString()}`;
};
const fmtPct = (n: unknown): string =>
  typeof n === "number" && isFinite(n) ? `${(n * 100).toFixed(0)}%` : "—";
const fmtNum = (n: unknown, suffix = ""): string =>
  typeof n === "number" && isFinite(n) ? `${n}${suffix}` : "—";

// W489 — the four sim_results keys synthesis/api.py actually asks the model for, each with the one
// figure worth showing. A key the model omitted is not rendered; nothing here supplies a default.
const SIM_KEYS: [string, string, (v: any) => string][] = [
  ['ese_adoption', 'ESE Adoption', v => fmtPct(v?.early_adopter?.market_share)],
  ['aro_efficiency', 'ARO Efficiency', v => fmtPct(v?.resource_optimization_gain)],
  ['bto_roadmap', 'BTO Velocity', v => fmtNum(v?.implementation_speed_multiplier, 'x')],
  ['drad_resilience', 'DRAD Resilience', v => fmtNum(v?.adaptation_latency_ms, 'ms')],
];

export const BusinessModelDashboard: React.FC<{ data: any }> = ({ data }) => {
  const sim = data?.sim_results ?? null;
  const proj = data?.projections ?? null;
  const chartData = proj
    ? [
        { name: "Year 1", value: proj.year_1 },
        { name: "Year 3", value: proj.year_3 },
        { name: "Year 5", value: proj.year_5 },
      ].filter(d => typeof d.value === "number")
    : [];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {(data?.sim_results_note || data?.projections_note || data?.generated === false) && (
        <p role="status" className="text-[10px] font-bold text-amber-400 leading-relaxed">
          {data?.detail || data?.sim_results_note || data?.projections_note}
        </p>
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         <StatCard label="Market Size" value={fmtMoney(data?.market_size)} icon={TrendingUp} color="text-aura" />
         <StatCard label="ROI Efficiency" value={fmtPct(sim?.aro_efficiency?.resource_optimization_gain)} icon={Zap} color="text-highlight" />
         <StatCard label="Swarm Multiplier" value={fmtNum(sim?.bto_roadmap?.implementation_speed_multiplier, "x")} icon={Users} color="text-vital" />
         {/* W460 (P1.12) — a green "GaaS Alignment" card showed a number the MODEL invented in its JSON; the
             constitutional gate never scored this plan. Removed rather than relabelled. */}
      </div>
      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
         <Card className="@[440px]:col-span-8 p-8 border-slate-900 bg-slate-950/40">
            <h3 className="text-sm font-black text-white uppercase tracking-widest mb-10 flex items-center gap-3">
               <BarChart3 size={18} className="text-aura" />
               Revenue Projections (LTSA Offering)
            </h3>
            {chartData.length === 0 ? (
               <p className="text-xs text-slate-500 italic py-10">
                  The model returned no financial projections, so none are charted.
               </p>
            ) : (
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
            )}
         </Card>

         <Card className="@[440px]:col-span-4 p-8 bg-aura/5 border-aura/20 flex flex-col justify-between">
            <div>
               {/* W489 (sweep S5.13, C3) — these were JSX LITERALS: a hard-coded attrition-reduction
                   figure, a constant adoption verdict and a three-quarters-full meter, all rendered
                   whatever the model returned and even when it returned nothing (generated:false),
                   directly beneath the amber note saying no parseable simulation came back. They were
                   the removed template's numbers, surviving in markup after the module that produced
                   them started stamping itself measured:false. The strategy text is now the model's
                   own or absent; the meter is gone, because nothing measures adoption velocity. */}
               {/* (refutation) The first cut of this read `data.market_strategy` — a field NO writer in
                   the repo emits — so the card permanently said the model returned nothing while the
                   model's real market_summary and roi_analysis were rendered nowhere at all. Reading a
                   field that does not exist is the same defect as inventing one. These two are what
                   synthesis/api.py actually asks the model for. */}
               <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6">Market Summary</h3>
               {data?.market_summary || data?.roi_analysis ? (
                 <div className="space-y-3">
                   {data?.market_summary && (
                     <p className="text-xs text-slate-400 font-bold leading-relaxed">{data.market_summary}</p>
                   )}
                   {data?.roi_analysis && (
                     <p className="text-[11px] text-slate-500 font-bold leading-relaxed">
                       <span className="text-slate-400 uppercase tracking-widest text-[9px] block mb-1">ROI analysis</span>
                       {data.roi_analysis}
                     </p>
                   )}
                 </div>
               ) : (
                 <p className="text-xs text-slate-500 font-bold leading-relaxed" data-testid="no-market-strategy">
                   The model returned no market summary, so none is shown.
                 </p>
               )}
            </div>
            <div className="space-y-4 pt-10">
               <Button onClick={() => toast('PDF export coming in next release — strategy data available via the AI CEO chat')} className="w-full bg-white text-sovereign text-[9px] uppercase font-black py-4">Download Strategy PDF</Button>
            </div>
         </Card>
      </div>

      {/* W489 (sweep S5.13, C3) — this card held three hard-coded parameters (a market share, an
          efficiency gain and a velocity multiplier) copied from a template that has since been
          deleted, rendered even when the model returned nothing at all. It now shows the simulation's
          OWN parameters, and says so when there are none rather than showing someone else's numbers
          as this run's. */}
      <Card className="p-8 border-slate-900 bg-slate-950/20">
         <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6 flex items-center gap-3">
            <PieChart size={18} className="text-highlight" />
            Simulation Parameters
         </h3>
         {/* (refutation) The first cut read a parameters array on sim_results that no writer emits, so this
             card permanently claimed no parameters were returned on the very screen whose StatCards
             render sim_results.aro_efficiency and sim_results.bto_roadmap. These four are the keys
             synthesis/api.py actually specifies; each renders only when the model supplied it. */}
         {sim && SIM_KEYS.some(([k]) => sim[k] != null) ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
               {SIM_KEYS.filter(([k]) => sim[k] != null).map(([k, label, pick]) => (
                  <SimParam key={k} label={label} value={pick(sim[k])} detail={k} />
               ))}
            </div>
         ) : (
            <p className="text-xs text-slate-500 font-bold leading-relaxed" data-testid="no-sim-parameters">
               No simulation parameters were returned{data?.generated === false ? ' — the model produced no simulation for this model' : ''}.
               Nothing is shown here rather than a set of example figures.
            </p>
         )}
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
