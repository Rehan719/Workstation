import React from 'react';
import { LayoutDashboard, MessageSquare, Package, BookOpen, Settings, ShieldCheck } from 'lucide-react';

const navItems = [
  { name: 'Dashboard', icon: LayoutDashboard, id: 'dashboard' },
  { name: 'VSB AI CEO', icon: MessageSquare, id: 'ceo' },
  { name: 'Self Vision', icon: ShieldCheck, id: 'introspection' },
  { name: 'World Mind', icon: BookOpen, id: 'extrospection' },
  { name: 'Mind Forge', icon: ShieldCheck, id: 'evolution' },
  { name: 'BTO Catalog', icon: Package, id: 'bto' },
  { name: 'Knowledge CoEs', icon: BookOpen, id: 'coe' },
  { name: 'QEP Engine', icon: ShieldCheck, id: 'qep' },
  { name: 'Settings', icon: Settings, id: 'settings' },
];

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  return (
    <aside className="w-72 bg-slate-900/50 backdrop-blur-xl border-r border-slate-800 flex flex-col p-6 h-screen sticky top-0">
      <div className="mb-10">
        <h2 className="text-2xl font-black text-aura tracking-tighter">WORKSTATION</h2>
        <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">v138.0 Unified App</p>
      </div>

      <nav className="flex-1 space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setActiveTab(item.id)}
            className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all ${
              activeTab === item.id
                ? 'bg-aura text-sovereign font-bold shadow-lg shadow-aura/20'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            }`}
          >
            <item.icon size={20} />
            <span className="text-sm font-semibold">{item.name}</span>
          </button>
        ))}
      </nav>

      <div className="pt-6 border-t border-slate-800">
        <div className="flex items-center gap-3 px-2">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-aura to-highlight p-[2px]">
            <div className="w-full h-full rounded-full bg-sovereign flex items-center justify-center font-bold text-xs">
              AD
            </div>
          </div>
          <div>
            <p className="text-xs font-bold">Abdullah</p>
            <p className="text-[10px] text-slate-500 uppercase font-bold">Admin</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
