import React, { useState } from 'react';
import { Globe, Map, Languages, Activity, ShieldCheck, HeartPulse, Cpu, BarChart3, ChevronRight, Zap } from 'lucide-react';

export const QEPGlobalPortal: React.FC = () => {
  const [selectedRegion, setSelectedRegion] = useState<string | null>('Middle East');

  const regions = [
    { name: 'Middle East', id: 'ME-001', latency: '25ms', compliance: 'Sharia', health: '99.9%', color: 'bg-indigo-500' },
    { name: 'Europe', id: 'EU-001', latency: '12ms', compliance: 'GDPR', health: '100%', color: 'bg-emerald-500' },
    { name: 'North America', id: 'NA-001', latency: '18ms', compliance: 'CCPA', health: '99.8%', color: 'bg-blue-500' },
    { name: 'Asia Pacific', id: 'AP-001', latency: '42ms', compliance: 'APEC', health: '99.5%', color: 'bg-amber-500' },
    { name: 'Africa', id: 'AF-001', latency: '85ms', compliance: 'AU-Privacy', health: '98.2%', color: 'bg-rose-500' }
  ];

  const languageStats = [
    { lang: 'Arabic', users: '420k', growth: '+12%', color: 'bg-emerald-400' },
    { lang: 'English', users: '380k', growth: '+8%', color: 'bg-blue-400' },
    { lang: 'Urdu', users: '250k', growth: '+15%', color: 'bg-indigo-400' },
    { lang: 'French', users: '120k', growth: '+5%', color: 'bg-rose-400' },
    { lang: 'Indonesian', users: '180k', growth: '+22%', color: 'bg-amber-400' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <Globe className="w-8 h-8 text-indigo-600" />
          Global Scale Observatory
        </h2>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1 text-[10px] font-black text-slate-500 uppercase">
             <HeartPulse className="w-4 h-4 text-emerald-500" />
             Global Health: Optimal
          </div>
          <div className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full uppercase tracking-widest">
            v8.7 Sovereign Signature
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {regions.map((region) => (
          <div
            key={region.name}
            className={`p-5 rounded-2xl border-2 transition-all cursor-pointer shadow-sm ${selectedRegion === region.name ? 'border-indigo-500 bg-indigo-50/30' : 'border-slate-100 bg-white hover:border-indigo-200'}`}
            onClick={() => setSelectedRegion(region.name)}
          >
            <div className="flex justify-between items-start mb-3">
               <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{region.id}</div>
               <div className={`w-2 h-2 rounded-full ${region.color}`}></div>
            </div>
            <div className="text-lg font-black text-slate-800 uppercase tracking-tighter">{region.name}</div>
            <div className="flex justify-between items-center mt-4">
               <div className="text-[10px] font-bold text-slate-500 uppercase">{region.health} Up</div>
               <div className="text-[10px] font-black text-indigo-600 uppercase">{region.latency}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="p-8 bg-slate-900 rounded-3xl border-2 border-slate-800 relative overflow-hidden">
             <div className="relative z-10 space-y-6">
                <div className="flex items-center gap-2 text-indigo-400 mb-2">
                   <Map className="w-6 h-6" />
                   <h3 className="text-sm font-black uppercase tracking-widest text-white">Regional Compliance & Routing ({selectedRegion})</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                   <div className="p-6 bg-slate-800/50 rounded-2xl border border-slate-700 space-y-4">
                      <div className="flex items-center gap-2 mb-2">
                         <ShieldCheck className="w-5 h-5 text-indigo-400" />
                         <span className="text-xs font-black text-white uppercase tracking-widest">Compliance Status</span>
                      </div>
                      <div className="space-y-3">
                         {[
                           { rule: 'GDPR / Privacy Shield', status: 'Enforced' },
                           { rule: 'Digital Services Act', status: 'Enforced' },
                           { rule: 'Regional Data Masking', status: 'Active' },
                           { rule: 'Local Theological Norms', status: 'Aligned' }
                         ].map((rule) => (
                           <div key={rule.rule} className="flex justify-between items-center text-[10px] font-bold uppercase text-slate-400 border-b border-slate-700 pb-2">
                              <span>{rule.rule}</span>
                              <span className="text-emerald-400">{rule.status}</span>
                           </div>
                         ))}
                      </div>
                   </div>

                   <div className="p-6 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 space-y-4">
                      <div className="flex items-center gap-2 mb-2">
                         <Zap className="w-5 h-5 text-indigo-400" />
                         <span className="text-xs font-black text-white uppercase tracking-widest">Routing Optimization</span>
                      </div>
                      <div className="space-y-4">
                         <div className="p-3 bg-slate-800/80 rounded-xl">
                            <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Primary Node</div>
                            <div className="text-xs font-bold text-white uppercase">{selectedRegion?.toUpperCase().replace(' ', '_')}-FED-NODE-01</div>
                         </div>
                         <div className="p-3 bg-slate-800/80 rounded-xl">
                            <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Failover Status</div>
                            <div className="text-xs font-bold text-emerald-400 uppercase">Synchronized & Standby</div>
                         </div>
                      </div>
                   </div>
                </div>

                <div className="p-6 bg-slate-800/30 rounded-2xl border border-slate-700">
                   <div className="flex items-center gap-2 mb-2">
                      <Cpu className="w-4 h-4 text-indigo-400" />
                      <span className="text-xs font-black text-white uppercase tracking-widest">AI Edge Optimization</span>
                   </div>
                   <p className="text-xs text-slate-300 font-medium leading-relaxed italic">
                      "Dynamic content pre-caching active for {selectedRegion}. Predicted regional content popularity at 92.5%, optimizing delivery latency for localized lesson assets."
                   </p>
                </div>
             </div>
             <div className="absolute top-[-20px] right-[-20px] w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl"></div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="p-6 bg-white border-2 border-slate-100 rounded-2xl shadow-sm">
            <h3 className="text-xs font-black text-slate-800 uppercase mb-4 tracking-widest border-b border-slate-100 pb-2 flex items-center gap-2">
               <Languages className="w-4 h-4 text-indigo-600" /> Language Distribution
            </h3>
            <div className="space-y-4">
               {languageStats.map((stat) => (
                 <div key={stat.lang} className="space-y-2">
                    <div className="flex justify-between text-[10px] font-black uppercase text-slate-600">
                       <div className="flex items-center gap-2">
                          <div className={`w-2 h-2 rounded-full ${stat.color}`}></div>
                          {stat.lang}
                       </div>
                       <div className="flex items-center gap-2">
                          <span>{stat.users}</span>
                          <span className="text-emerald-500">{stat.growth}</span>
                       </div>
                    </div>
                    <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                       <div className={`h-full ${stat.color}`} style={{ width: `${(parseInt(stat.users)/5).toFixed(0)}%` }}></div>
                    </div>
                 </div>
               ))}
            </div>
            <button className="w-full mt-4 py-2 bg-slate-900 text-white rounded-lg text-[10px] font-black uppercase hover:bg-black transition-colors">
              AI Translation Pipeline Status
            </button>
          </div>

          <div className="p-6 bg-white border-2 border-slate-100 rounded-2xl shadow-sm">
             <h3 className="text-xs font-black text-slate-800 uppercase mb-4 tracking-widest border-b border-slate-100 pb-2 flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-indigo-600" /> Global Metrics
             </h3>
             <div className="grid grid-cols-2 gap-4">
                <div className="p-3 bg-slate-50 rounded-xl">
                   <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Total Users</div>
                   <div className="text-lg font-black text-slate-800">1.25M</div>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl">
                   <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Avg Latency</div>
                   <div className="text-lg font-black text-slate-800">28ms</div>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl">
                   <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Active Regions</div>
                   <div className="text-lg font-black text-slate-800">5 / 5</div>
                </div>
                <div className="p-3 bg-slate-50 rounded-xl">
                   <div className="text-[10px] font-black text-slate-400 uppercase mb-1">Languages</div>
                   <div className="text-lg font-black text-slate-800">50+</div>
                </div>
             </div>
             <div className="mt-4 flex items-center gap-2 p-2 bg-emerald-50 rounded-lg">
                <Activity className="w-3 h-3 text-emerald-500" />
                <span className="text-[10px] font-black text-emerald-700 uppercase">System status: Distributed Load Optimizing</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};
