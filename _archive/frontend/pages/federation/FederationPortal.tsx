import React, { useState } from 'react';
import { Network, Shield, Zap, Search, LayoutGrid, Activity } from 'lucide-react';
import { WorkstationExplorer } from './WorkstationExplorer';
import { FederationGovernance } from './Governance';
import { HomeostaticOrchestrator } from './Performance';
import { TwinManagement } from './TwinManagement';
import { TreatyStudio } from './TreatyStudio';
import { GlobalSearch } from './GlobalSearch';

export const FederationPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState('pulse');

  return (
    <div className="space-y-10">
      <header className="flex justify-between items-center bg-slate-900/60 p-8 rounded-[2.5rem] border border-slate-800 backdrop-blur-xl">
        <div>
          <h1 className="text-4xl font-black mb-1">Federation Portal</h1>
          <p className="text-slate-500 uppercase tracking-widest text-[10px] font-black">Civilization v145.0 • Global Central Command</p>
        </div>
        <div className="flex gap-4">
           <PortalNavBtn id="pulse" label="Pulse" active={activeTab === 'pulse'} onClick={setActiveTab} icon={Activity} />
           <PortalNavBtn id="explorer" label="Explorer" active={activeTab === 'explorer'} onClick={setActiveTab} icon={Network} />
           <PortalNavBtn id="search" label="Search" active={activeTab === 'search'} onClick={setActiveTab} icon={Search} />
           <PortalNavBtn id="governance" label="Governance" active={activeTab === 'governance'} onClick={setActiveTab} icon={Shield} />
           <PortalNavBtn id="treaties" label="Treaties" active={activeTab === 'treaties'} onClick={setActiveTab} icon={Zap} />
           <PortalNavBtn id="forge" label="Forge" active={activeTab === 'forge'} onClick={setActiveTab} icon={LayoutGrid} />
        </div>
      </header>

      <div className="min-h-[600px]">
         {activeTab === 'pulse' && <CivilizationalPulse />}
         {activeTab === 'explorer' && <WorkstationExplorer />}
         {activeTab === 'search' && <GlobalSearch />}
         {activeTab === 'governance' && <FederationGovernance />}
         {activeTab === 'treaties' && <TreatyStudio />}
         {activeTab === 'forge' && <TwinManagement />}
         {activeTab === 'performance' && <HomeostaticOrchestrator />}
      </div>
    </div>
  );
};

const CivilizationalPulse = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 @[440px]:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-4">
    <StatBox label="Total Federated Nodes" value="1,420" delta="+12 today" color="text-aura" />
    <StatBox label="Aggregate Health" value="99.98%" delta="Stable" color="text-vital" />
    <StatBox label="Civilizational WST" value="1.4M" delta="+8.4% APY" color="text-highlight" />

    <div className="@[440px]:col-span-2 p-10 rounded-[3rem] bg-slate-900/40 border border-slate-800 h-96 flex items-center justify-center">
       <p className="text-slate-700 font-black uppercase tracking-[0.4em] text-sm italic">Global Neural Resonance Feed...</p>
    </div>

    <div className="p-10 rounded-[3rem] bg-slate-900/40 border border-slate-800 space-y-6">
       <h3 className="font-bold uppercase tracking-widest text-xs text-slate-500">Recent Treaties</h3>
       {[1,2,3].map(i => (
         <div key={i} className="p-4 bg-slate-800/30 rounded-2xl border border-slate-700/50 flex justify-between items-center">
            <span className="text-xs font-bold">Node-Alpha ↔ Node-Gamma</span>
            <span className="text-[10px] font-black text-vital uppercase">Enforced</span>
         </div>
       ))}
    </div>
  </div>
);

const StatBox = ({ label, value, delta, color }: any) => (
  <div className="p-8 rounded-[2.5rem] bg-slate-900/40 border border-slate-800">
    <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest mb-4">{label}</p>
    <div className={`text-4xl font-black ${color}`}>{value}</div>
    <p className="text-[10px] text-slate-600 mt-2 font-bold italic">{delta}</p>
  </div>
);

const PortalNavBtn = ({ id, label, active, onClick, icon: Icon }: any) => (
  <button
    onClick={() => onClick(id)}
    className={`flex items-center gap-2 px-6 py-3 rounded-2xl font-bold transition-all ${
      active ? 'bg-aura text-sovereign shadow-lg shadow-aura/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'
    }`}
  >
    <Icon size={18} />
    <span className="text-xs uppercase">{label}</span>
  </button>
);
