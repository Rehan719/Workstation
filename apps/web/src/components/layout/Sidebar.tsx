import React from 'react';
import {
  LayoutDashboard, MessageSquare, Package, BookOpen, Settings, ShieldCheck, Heart,
  Zap, Shield, ShoppingBag, Terminal, Rocket, Plus, Gauge, Sparkles, Activity,
  Brain, Network, Palette, FileText, User, Map, Cpu, DollarSign, Radio, Globe,
  GitBranch, Target, Fingerprint, BarChart3, Book, Scale, Briefcase,
  GraduationCap, Trophy, Wifi, Beaker, FlaskConical, History, Microscope, Gavel, Binary, Camera, Watch, Code2, Satellite, Star, Archive, Eye,
  HeartPulse, Workflow, Search, Smartphone, Globe2, Database
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
    name: 'VSB AI CEO',
    icon: MessageSquare,
    id: 'ceo-facet',
    realms: ['ENTERPRISE', 'GENOME', 'UNIFIED'],
    subItems: [
      { name: 'Direct Chat', icon: MessageSquare, id: 'ceo' },
      { name: 'Debate Log', icon: History, id: 'debate' }
    ]
  },

  {
    name: 'Sovereign Domains',
    icon: Globe,
    id: 'domain-facet',
    subItems: [
      { name: 'Religion', icon: Heart, id: 'religion' },
      { name: 'Science', icon: Microscope, id: 'science' },
      { name: 'Law', icon: Gavel, id: 'law' },
      { name: 'Employment', icon: Briefcase, id: 'employment' },
      { name: 'Education', icon: GraduationCap, id: 'education' },
      { name: 'Care', icon: HeartPulse, id: 'care' }
    ]
  },

  {
    name: 'Development',
    icon: Terminal,
    id: 'dev-facet',
    realms: ['DEVELOPER', 'UNIFIED'],
    subItems: [
      { name: 'The Forge', icon: Terminal, id: 'forge' },
      { name: 'Digital Reactor', icon: Zap, id: 'reactor' },
      { name: 'Incubator', icon: Beaker, id: 'incubator' },
      { name: 'Petri Dish', icon: FlaskConical, id: 'petri' },
      { name: 'QEP Reactor', icon: Cpu, id: 'qep' },
      { name: 'Factory', icon: Database, id: 'factory' },
      { name: 'Pipelines', icon: Workflow, id: 'pipelines' }
    ]
  },

  {
    name: 'Civilisation',
    icon: Network,
    id: 'civ-facet',
    subItems: [
      { name: 'Federation Map', icon: Map, id: 'fed-map' },
      { name: 'Homeostasis', icon: HeartPulse, id: 'orchestrator' },
      { name: 'Orbital Command', icon: Satellite, id: 'orbital' },
      { name: 'Cosmic Command', icon: Star, id: 'cosmic' },
      { name: 'Seeding Portal', icon: Rocket, id: 'seeding' },
      { name: 'Interstellar Diplomacy', icon: Globe2, id: 'diplomacy' },
      { name: 'Marketplace', icon: ShoppingBag, id: 'marketplace' },
      { name: 'Treaty Dashboard', icon: FileText, id: 'treaties' },
      { name: 'Offspring Mgmt', icon: GitBranch, id: 'offspring' }
    ]
  },

  {
    name: 'Platforms',
    icon: Smartphone,
    id: 'plat-facet',
    subItems: [
      { name: 'AR/VR Lab', icon: Camera, id: 'ar-vr' },
      { name: 'Wearable Sync', icon: Watch, id: 'wearables' },
      { name: 'Embodiment Studio', icon: Eye, id: 'embodiment' },
      { name: 'Voice Control', icon: Radio, id: 'voice' }
    ]
  },

  {
    name: 'Genomic Core',
    icon: Binary,
    id: 'genomic-facet',
    realms: ['DEVELOPER', 'SCHOLAR', 'UNIFIED'],
    subItems: [
      { name: 'Genome Explorer', icon: Search, id: 'genome-explorer' },
      { name: 'GRN Dashboard', icon: Network, id: 'grn-dashboard' },
      { name: 'Methylation', icon: Fingerprint, id: 'methylation' },
      { name: 'Transcriptional', icon: Radio, id: 'transcriptional' },
      { name: 'Phenotype Preview', icon: Eye, id: 'phenotype' }
    ]
  },

  {
    name: 'Governance',
    icon: Shield,
    id: 'gov-facet',
    subItems: [
      { name: 'Constitution', icon: FileText, id: 'constitution' },
      { name: 'Republic Council', icon: Gavel, id: 'council' },
      { name: 'Entity Control', icon: ShieldCheck, id: 'admin' },
      { name: 'Sovereign Vault', icon: Archive, id: 'vault' },
      { name: 'Realm Foundry', icon: Globe, id: 'realm-editor' },
      { name: 'Transparency', icon: History, id: 'transparency' }
    ]
  },

  { name: 'File Hub', icon: Package, id: 'file-hub' },
  { name: 'GaaS Audit', icon: ShieldCheck, id: 'audit' },
  { name: 'UVAID / GSE', icon: Sparkles, id: 'uvaid' },
  { name: 'Text Index', icon: FileText, id: 'text-index' },
  { name: 'Contributor Portal', icon: Code2, id: 'contribute' },
  { name: 'System Settings', icon: Settings, id: 'settings' },
];

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const { currentRealm, currentMode, user } = useStore();

  const filteredNavItems = allNavItems.filter(item => {
    if (currentRealm === 'UNIFIED') return true;
    if (!item.realms) return true;
    return item.realms.includes(currentRealm);
  });

  return (
    <aside className={`w-72 flex flex-col p-6 h-screen sticky top-0 transition-all duration-500 border-r bg-slate-950/80 backdrop-blur-3xl border-slate-900 ${currentMode === 'REST' ? 'grayscale-[30%] opacity-90' : ''}`}>
      <div className="mb-10 relative">
        <div className="flex items-center gap-3">
           <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-aura to-highlight flex items-center justify-center text-sovereign shadow-lg shadow-aura/10 animate-pulse">
              <Zap size={24} />
           </div>
           <div>
              <h2 className="text-xl font-black tracking-tighter text-white uppercase">Workstation</h2>
              <p className="text-[10px] uppercase tracking-[0.2em] text-aura font-black">v3.0 Ultimate</p>
           </div>
        </div>
      </div>

      <nav className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
        {filteredNavItems.map((item: any) => (
          <div key={item.id} className="space-y-1">
            <button
              onClick={() => {
                if (!item.subItems) setActiveTab(item.id);
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
                    onClick={() => setActiveTab(sub.id)}
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
