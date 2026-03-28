import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, MessageSquare, Package, BookOpen, Settings, ShieldCheck, Heart,
  Zap, Shield, ShoppingBag, Terminal, Rocket, Plus, Gauge, Sparkles, Activity,
  Brain, Network, Palette, FileText, User, Map, Cpu, DollarSign, Radio, Globe,
  GitBranch, Target, Fingerprint, BarChart3, Book, Scale, Briefcase,
  GraduationCap, Trophy, Wifi, Beaker, FlaskConical, History, Microscope, Gavel, Binary, Camera, Watch, Code2, Satellite, Star, Archive, Eye,
  HeartPulse, Workflow, Search, Smartphone, Globe2, Database, Layers
} from 'lucide-react';
import { useStore, RealmType } from '@workstation/shared';

interface NavItem {
  name: string;
  icon: any;
  id: string;
  subItems?: NavItem[];
  realms?: RealmType[];
}

const allNavItems: NavItem[] = [
  { name: 'Dashboard', icon: LayoutDashboard, id: 'dashboard' },

  {
    name: 'Productivity',
    icon: Zap,
    id: 'prod-facet',
    subItems: [
      { name: 'AI CEO', icon: MessageSquare, id: 'ceo' },
      { name: 'BTO Catalog', icon: Package, id: 'bto' },
      { name: 'File Hub', icon: Package, id: 'file-hub' },
      { name: 'Marketplace', icon: ShoppingBag, id: 'marketplace' }
    ]
  },

  {
    name: 'QEP Flagship',
    icon: Layers,
    id: 'qep-facet',
    subItems: [
      { name: 'QEP Dashboard', icon: LayoutDashboard, id: 'qep' },
      { name: 'Religion Hub', icon: Heart, id: 'qep-religion' },
      { name: 'Science Hub', icon: Microscope, id: 'science' },
      { name: 'Education Hub', icon: GraduationCap, id: 'education' },
      { name: 'Law Hub', icon: Gavel, id: 'law' },
      { name: 'Care Hub', icon: HeartPulse, id: 'care' },
      { name: 'Employment', icon: Briefcase, id: 'employment' }
    ]
  },

  {
    name: 'Evolution',
    icon: Brain,
    id: 'evo-facet',
    subItems: [
      { name: 'Genome', icon: Fingerprint, id: 'genome-explorer' },
      { name: 'GRN Mesh', icon: Network, id: 'grn-dashboard' },
      { name: 'Introspection', icon: Brain, id: 'introspection' },
      { name: 'Homeostasis', icon: HeartPulse, id: 'orchestrator' }
    ]
  },

  {
    name: 'Governance',
    icon: Shield,
    id: 'gov-facet',
    subItems: [
      { name: 'Constitution', icon: FileText, id: 'constitution' },
      { name: 'Transparency', icon: History, id: 'transparency' },
      { name: 'Entity Control', icon: ShieldCheck, id: 'admin' },
      { name: 'Audit Dashboard', icon: ShieldCheck, id: 'audit' }
    ]
  },

  {
    name: 'Advanced',
    icon: Settings,
    id: 'adv-facet',
    subItems: [
      { name: 'The Forge', icon: Terminal, id: 'forge' },
      { name: 'AR/VR Lab', icon: Camera, id: 'ar-vr' },
      { name: 'Federation', icon: Map, id: 'fed-map' },
      { name: 'System Settings', icon: Settings, id: 'settings' }
    ]
  }
];

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const { currentRealm, currentMode, user, setCurrentTab } = useStore();
  const navigate = useNavigate();

  const filteredNavItems = allNavItems.filter(item => {
    if (currentRealm === 'UNIFIED') return true;
    if (!item.realms) return true;
    return item.realms.includes(currentRealm);
  });

  return (
    <aside className={`w-full flex flex-col p-6 h-full transition-all duration-500 border-r bg-slate-950 border-slate-900 z-30 ${currentMode === 'REST' ? 'grayscale-[30%] opacity-90' : ''}`}>
      <div className="mb-10 relative">
        <button onClick={() => setCurrentTab('dashboard')} className="flex items-center gap-3 hover:opacity-80 transition-opacity">
           <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-aura to-highlight flex items-center justify-center text-sovereign shadow-lg shadow-aura/10 animate-pulse">
              <Zap size={24} />
           </div>
           <div className="text-left">
              <h2 className="text-xl font-black tracking-tighter text-white uppercase">Workstation</h2>
              <p className="text-[10px] uppercase tracking-[0.2em] text-aura font-black">v3.0 Ultimate</p>
           </div>
        </button>
      </div>

      <nav className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {filteredNavItems.map((item: any) => (
          <div key={item.id} className="space-y-1">
            <button
              onClick={() => {
                if (!item.subItems) {
                  setActiveTab(item.id);
                  navigate(`/${item.id === 'dashboard' ? '' : item.id}`);
                }
              }}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-2xl transition-all focus:outline-none group ${
                activeTab === item.id ? 'bg-aura text-sovereign font-black shadow-xl shadow-aura/20 scale-[1.02]' : 'text-slate-500 hover:text-white hover:bg-slate-900/50'
              }`}
            >
              <item.icon size={18} className={`transition-transform group-hover:scale-110 ${activeTab === item.id ? 'text-sovereign' : 'text-aura/70'}`} />
              <span className="text-xs font-black uppercase tracking-widest">{item.name}</span>
            </button>
            {item.subItems && (
              <div className="ml-6 space-y-1 border-l border-slate-900 pl-4 py-1">
                {item.subItems.map((sub: any) => (
                  <button
                    key={sub.id}
                    onClick={() => {
                      setActiveTab(sub.id);
                      navigate(`/${sub.id}`);
                    }}
                    className={`w-full flex items-center gap-3 py-2 text-[10px] font-black uppercase tracking-[0.15em] transition-all group ${
                      activeTab === sub.id ? 'text-aura' : 'text-slate-600 hover:text-slate-300'
                    }`}
                  >
                    <sub.icon size={14} className={`transition-opacity ${activeTab === sub.id ? 'opacity-100' : 'opacity-40 group-hover:opacity-100'}`} />
                    {sub.name}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>

      <div className="pt-6 border-t border-slate-900 flex items-center gap-4 px-2">
         <div className="w-10 h-10 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center font-black text-[10px] text-aura uppercase tracking-widest">
            {user?.displayName?.substring(0, 2) || 'VSB'}
         </div>
         <div>
            <p className="text-xs font-black text-white uppercase tracking-wider">{user?.displayName || 'Sovereign'}</p>
            <p className="text-[9px] text-aura/50 uppercase font-black tracking-[0.2em]">{user?.role || 'Guest'}</p>
         </div>
      </div>
    </aside>
  );
};
