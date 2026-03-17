import React from 'react';
import { LayoutDashboard, MessageSquare, Package, BookOpen, Settings, ShieldCheck, Heart, Zap, Shield, ShoppingBag, Terminal, Rocket, Plus, Gauge, Sparkles, Activity, Brain, Network, Palette } from 'lucide-react';
import { useModeStore } from '../../store/modeStore';
import { useTheme } from '../../theme/ThemeContext';

const allNavItems = [
  { name: 'Pulse', icon: Activity, id: 'dashboard' },
  { name: 'AI CEO', icon: MessageSquare, id: 'ceo' },
  {
    name: 'The Mind',
    icon: Brain,
    id: 'mind',
    subItems: [
      { name: 'Self Vision', icon: ShieldCheck, id: 'introspection' },
      { name: 'World Mind', icon: BookOpen, id: 'extrospection' },
      { name: 'Mind Forge', icon: ShieldCheck, id: 'evolution' }
    ]
  },
  {
    name: 'Governance',
    icon: Shield,
    id: 'gov-facet',
    subItems: [
      { name: 'Fed Portal', icon: Network, id: 'fed-portal' },
      { name: 'Constitution', icon: Shield, id: 'governance' }
    ]
  },
  {
    name: 'Economy',
    icon: ShoppingBag,
    id: 'eco-facet',
    subItems: [
      { name: 'Wallet', icon: ShieldCheck, id: 'wallet' },
      { name: 'Marketplace', icon: ShoppingBag, id: 'marketplace' },
      { name: 'BTO Catalog', icon: Package, id: 'bto' }
    ]
  },
  { name: 'Evolution', icon: Sparkles, id: 'evolution-facet' },
  { name: 'Settings', icon: Settings, id: 'settings' },
];

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const { config } = useModeStore();
  const { theme, toggleTheme } = useTheme();
  const navItems = config ? allNavItems.filter(item => config.nav.includes(item.id)) : allNavItems;

  return (
    <aside className={`w-72 flex flex-col p-6 h-screen sticky top-0 transition-all duration-500 border-r ${
      theme === 'advanced'
        ? 'bg-sovereign border-aura/30 shadow-[0_0_50px_-12px_rgba(100,255,218,0.15)]'
        : 'bg-slate-900/50 backdrop-blur-xl border-slate-800'
    }`}>
      <div className="mb-10 relative">
        <h2 className={`text-2xl font-black tracking-tighter transition-all ${
          theme === 'advanced' ? 'text-aura drop-shadow-[0_0_10px_rgba(100,255,218,0.5)]' : 'text-aura'
        }`}>WORKSTATION</h2>
        <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold text-center">Civilization v146.0</p>

        <button
          onClick={toggleTheme}
          className="absolute -top-2 -right-2 p-2 rounded-full hover:bg-slate-800/50 transition-colors text-slate-500 hover:text-aura"
          title="Toggle UI Theme"
          aria-label="Toggle UI Theme"
        >
          <Palette size={14} />
        </button>
      </div>

      <nav className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {navItems.map((item: any) => (
          <div key={item.id} className="space-y-1">
            <button
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all focus:outline-none focus:ring-2 focus:ring-aura ${
                activeTab === item.id
                  ? theme === 'advanced'
                    ? 'bg-aura text-sovereign font-bold shadow-[0_0_20px_rgba(100,255,218,0.4)] scale-[1.02]'
                    : 'bg-aura text-sovereign font-bold shadow-lg shadow-aura/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
              }`}
              aria-label={item.name}
            >
              <item.icon size={20} aria-hidden="true" />
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
