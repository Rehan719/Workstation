import React from 'react';
import {
  LayoutDashboard, MessageSquare, Package, BookOpen, Settings, ShieldCheck, Heart,
  Zap, Shield, ShoppingBag, Terminal, Rocket, Plus, Gauge, Sparkles, Activity,
  Brain, Network, Palette, FileText, User, Map, Cpu, DollarSign, Radio, Globe,
  GitBranch, Target, Fingerprint, BarChart3, Book, Scale, Briefcase,
  GraduationCap, Trophy, Wifi, Beaker, FlaskConical, History
} from 'lucide-react';
import { useModeStore } from '../../store/modeStore';
import { useTheme } from '../../theme/ThemeContext';

const allNavItems = [
  { name: 'Pulse', icon: Activity, id: 'dashboard' },
  { name: 'AI CEO', icon: MessageSquare, id: 'ceo' },
  {
    name: 'Development',
    icon: Terminal,
    id: 'dev-facet',
    subItems: [
      { name: 'The Forge', icon: Terminal, id: 'forge' },
      { name: 'Digital Reactor', icon: Zap, id: 'reactor' },
      { name: 'Incubator', icon: Beaker, id: 'incubator' },
      { name: 'QEP Reactor', icon: Cpu, id: 'qep' }
    ]
  },
  {
    name: 'Governance',
    icon: Shield,
    id: 'gov-facet',
    subItems: [
      { name: 'Constitution', icon: FileText, id: 'constitution' },
      { name: 'Republic Council', icon: Gavel, id: 'council' },
      { name: 'Entity Control', icon: ShieldCheck, id: 'admin' }
    ]
  },
  {
    name: 'Economy',
    icon: ShoppingBag,
    id: 'eco-facet',
    subItems: [
      { name: 'Marketplace', icon: ShoppingBag, id: 'marketplace' },
      { name: 'BTO Catalog', icon: Package, id: 'bto' },
      { name: 'Offspring Mgmt', icon: GitBranch, id: 'offspring' }
    ]
  },
  { name: 'Settings', icon: Settings, id: 'settings' },
];

import { Gavel } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const { theme, toggleTheme } = useTheme();
  const navItems = allNavItems;

  return (
    <aside className={`w-72 flex flex-col p-6 h-screen sticky top-0 transition-all duration-500 border-r ${
      theme === 'advanced'
        ? 'bg-sovereign border-aura/30 shadow-[0_0_50px_-12px_rgba(100,255,218,0.15)]'
        : 'bg-slate-900/50 backdrop-blur-xl border-slate-800'
    }`}>
      <div className="mb-10 relative">
        <h2 className="text-2xl font-black tracking-tighter text-aura">WORKSTATION</h2>
        <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">Epoch: Eternal Synthesis</p>

        <button onClick={toggleTheme} className="absolute -top-2 -right-2 p-2 rounded-full hover:bg-slate-800/50 text-slate-500 hover:text-aura">
          <Palette size={14} />
        </button>
      </div>

      <nav className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {navItems.map((item: any) => (
          <div key={item.id} className="space-y-1">
            <button
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all focus:outline-none ${
                activeTab === item.id ? 'bg-aura text-sovereign font-bold shadow-lg shadow-aura/20' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
            >
              <item.icon size={20} />
              <span className="text-sm font-semibold">{item.name}</span>
            </button>
            {item.subItems && (
              <div className="ml-10 space-y-1 border-l border-slate-800 pl-4">
                {item.subItems.map((sub: any) => (
                  <button
                    key={sub.id}
                    onClick={() => setActiveTab(sub.id)}
                    className={`w-full text-left py-2 text-xs font-bold transition-colors ${
                      activeTab === sub.id ? 'text-aura' : 'text-slate-500 hover:text-white'
                    }`}
                  >
                    {sub.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>

      <div className="pt-6 border-t border-slate-800 flex items-center gap-3 px-2">
         <div className="w-10 h-10 rounded-full bg-aura/20 flex items-center justify-center font-bold text-xs text-aura">AD</div>
         <div>
            <p className="text-xs font-bold text-white">Abdullah</p>
            <p className="text-[10px] text-slate-500 uppercase font-bold">Guardian</p>
         </div>
      </div>
    </aside>
  );
};
