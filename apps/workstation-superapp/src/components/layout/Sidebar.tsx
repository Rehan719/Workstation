import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, MessageSquare, Package, Settings, ShieldCheck, Heart,
  Shield, ShoppingBag, Terminal, Rocket, Plus, Gauge, Sparkles, Activity,
  Network, Palette, FileText, User, Cpu, DollarSign,
  GitBranch, Target, Fingerprint, BarChart3, Book, Scale, Briefcase,
  GraduationCap, Trophy, Wifi, Beaker, History, Microscope, Gavel, Binary, Code2, Star, Archive, Eye,
  HeartPulse, Workflow, Search, Globe2, Layers, ChevronDown,
  FolderOpen, Folders, Building2, Users, TrendingUp, Copy, Dna, Crown, Coins, Boxes
} from 'lucide-react';
import { useStore, RealmType } from '@workstation/shared';
import { useT } from '../../lib/i18n';

interface NavItem {
  name: string;
  icon: any;
  id: string;
  subItems?: NavItem[];
  realms?: RealmType[];
}

// Vision-aligned IA — the §3A TWO-JOURNEY SPINE leads: ① Work in a Domain (Offering 1 — domain-specific
// AI-mediated tools) and ② Build an Enterprise (Offering 2 — Concept→Commercialisation → a living VSB).
// Beneath sit the supporting Platform (the native-AI fabric, resource fabric & living organism), then
// Governance & Trust and System. Overlapping pages are folded into tabbed hubs. Every id maps to a live
// route in App.tsx.
const allNavItems: NavItem[] = [
  {
    name: 'Home',
    icon: LayoutDashboard,
    id: 'home-facet',
    subItems: [
      { name: 'Dashboard',     icon: LayoutDashboard, id: 'dashboard' },
      { name: 'My Work',       icon: FolderOpen,      id: 'my-work' },
    ]
  },

  {
    // §3A Offering 1 — domain-specific AI-mediated tools & resources, usable now, no enterprise required.
    name: 'Work in a Domain',
    icon: Layers,
    id: 'work-facet',
    subItems: [
      { name: 'Overview',        icon: Layers,        id: 'domains' },
      { name: 'AI Tools',        icon: Sparkles,      id: 'ai-tools' },
      { name: 'Religion',        icon: Heart,         id: 'religion' },
      { name: "Qur'an Platform", icon: Book,          id: 'qep' },
      { name: 'Science',         icon: Microscope,    id: 'science' },
      { name: 'Education',       icon: GraduationCap, id: 'education' },
      { name: 'Law',             icon: Gavel,         id: 'law' },
      { name: 'Care',            icon: HeartPulse,    id: 'care' },
      { name: 'Employment',      icon: Briefcase,     id: 'employment' },
    ]
  },

  {
    // §3A Offering 2 — end-to-end Concept→Commercialisation establishing a living VSB IDBO Enterprise.
    name: 'Build an Enterprise',
    icon: Rocket,
    id: 'build-facet',
    subItems: [
      { name: 'Genesis Journey',    icon: Rocket,     id: 'genesis' },
      { name: 'VSB Cockpit',        icon: Crown,      id: 'vsb-cockpit' },
      { name: 'VSB Spawn Studio',   icon: Building2,  id: 'vsb' },
      { name: 'Business Plan',      icon: FileText,   id: 'business-plan' },
      { name: 'Projects',           icon: Folders,    id: 'projects' },
      { name: 'Deliverables',       icon: FileText,   id: 'deliverables' },
      { name: 'Management Systems', icon: Shield,     id: 'management' },
      { name: 'Capital Fund',       icon: DollarSign, id: 'capital' },
      { name: 'Economy',            icon: Coins,      id: 'economy' },
    ]
  },

  {
    // The supporting fabric both journeys run on: the native AI swarm/models/orchestration (§6), the
    // reconfigurable resource fabric (§7) and the biomimetic living organism (§8).
    name: 'Platform',
    icon: Cpu,
    // The 10 process-intelligence engines (synthesis · nexus · forge · reactor · incubator · factory ·
    // intelligence · authorship · design-dev · solutions) launch one-click from the Resource Fabric hub's
    // "Studios" grid — keeping the nav lean while every engine stays first-class and reachable.
    id: 'platform-facet',
    subItems: [
      { name: 'Native AI',          icon: Cpu,           id: 'native-ai' },
      { name: 'AI CEO',             icon: MessageSquare, id: 'ceo' },
      { name: 'Board of Directors', icon: Crown,         id: 'board' },
      { name: 'Swarm Intelligence', icon: Network,       id: 'swarm-intelligence' },
      { name: 'Visual Composer',    icon: Workflow,      id: 'visual-composer' },
      { name: 'Resource Fabric',    icon: Layers,        id: 'resource-fabric' },
      { name: 'Reactor Studio',     icon: BarChart3,     id: 'reactor-studio' },
      { name: 'Build to Order',     icon: Package,       id: 'bto' },
      { name: 'Digital Twins',      icon: Boxes,         id: 'digital-twins' },
      { name: 'Transformation',     icon: Target,        id: 'transformation' },
      { name: 'Organism',           icon: Activity,      id: 'organism' },
      { name: 'Sovereign Evolution',icon: Dna,           id: 'sovereign-evolution' },
    ]
  },

  {
    name: 'Governance & Trust',
    icon: Shield,
    id: 'gov-facet',
    subItems: [
      { name: 'Governance Hub',         icon: Shield,      id: 'governance-hub' },
      { name: 'Constitution',           icon: FileText,    id: 'constitution' },
      { name: 'Compliance',             icon: ShieldCheck, id: 'compliance' },
      { name: 'Change Control',         icon: GitBranch,   id: 'change-control' },
      { name: 'Operational Excellence', icon: Gauge,       id: 'operations' },
      { name: 'CoE Hub',                icon: Trophy,      id: 'coe' },
    ]
  },

  {
    name: 'System',
    icon: Settings,
    id: 'system-facet',
    subItems: [
      { name: 'Marketplace',     icon: ShoppingBag, id: 'marketplace' },
      { name: 'Wallet',          icon: DollarSign,  id: 'wallet' },
      { name: 'Creator Studio',  icon: Palette,     id: 'creator' },
      { name: 'Contribute',      icon: Plus,        id: 'contribute' },
      { name: 'Entity Control',  icon: ShieldCheck, id: 'admin' },
      { name: 'Settings',        icon: Settings,    id: 'settings' },
    ]
  }
];

const IDBOIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" className="w-7 h-7">
    {/* Outer field — organic irregular membrane, not a perfect circle */}
    <path d="M12 1 C16 0.5 20 4 21.5 8 C23 12 22 17 19.5 20 C17 23 13 24.5 9.5 23 C6 21.5 3 18 2 14 C1 10 2.5 5.5 5.5 3.5 C7.5 2 10 1.2 12 1 Z" strokeWidth="0.4" opacity="0.28" />
    {/* Dendrites — 6 organic C-bezier branches, asymmetric like real neurites */}
    <path d="M10 8.5 C9 6.5 7.5 4.5 6 2.5" strokeWidth="1.3" />
    <path d="M14 8 C15.5 6 17 4.5 18.5 2.5" strokeWidth="1.25" />
    <path d="M8.5 12 C6 11.5 3.5 11.2 1.5 11.5" strokeWidth="1.25" />
    <path d="M15.5 13.5 C18 14 20.5 14.5 22.5 14" strokeWidth="1.2" />
    <path d="M14 15.5 C15.5 18 17.5 20.5 19 22" strokeWidth="1.2" />
    <path d="M10 15.5 C8.5 18 7 20.5 6 22.5" strokeWidth="1.15" />
    {/* Secondary bifurcation — upper-left dendrite splits naturally */}
    <path d="M6 2.5 C5 1.5 4 0.8 3 0.5" strokeWidth="0.75" opacity="0.6" />
    <path d="M6 2.5 C6.2 1.5 6.8 0.8 7.5 0.5" strokeWidth="0.75" opacity="0.6" />
    {/* Synaptic terminals — filled dots, slightly varied sizes */}
    <circle cx="6" cy="2.5" r="1.35" fill="currentColor" fillOpacity="0.85" strokeWidth="0" />
    <circle cx="18.5" cy="2.5" r="1.35" fill="currentColor" fillOpacity="0.85" strokeWidth="0" />
    <circle cx="1.5" cy="11.5" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    <circle cx="22.5" cy="14" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    <circle cx="19" cy="22" r="1.25" fill="currentColor" fillOpacity="0.8" strokeWidth="0" />
    <circle cx="6" cy="22.5" r="1.2" fill="currentColor" fillOpacity="0.75" strokeWidth="0" />
    {/* Cell soma — slightly oval, semi-transparent fill */}
    <ellipse cx="12" cy="12" rx="4.5" ry="4.3" strokeWidth="1.55" fill="currentColor" fillOpacity="0.11" />
    {/* Nucleus — slightly off-center for natural asymmetry */}
    <ellipse cx="11.8" cy="12" rx="2" ry="2.65" strokeWidth="1.05" />
    {/* DNA double helix — two interleaving S-curves */}
    <path d="M11 9.8 C12.5 10.7 11 11.5 12.5 12.4 C14 13.2 12 14 13 14.8" strokeWidth="0.65" />
    <path d="M13 9.8 C11.5 10.7 13 11.5 11.5 12.4 C10 13.2 12 14 11 14.8" strokeWidth="0.65" />
    {/* Mitochondrion — small organelle near soma edge */}
    <ellipse cx="18.5" cy="10.5" rx="1.5" ry="0.85" strokeWidth="0.7" transform="rotate(-30 18.5 10.5)" />
  </svg>
);

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const { currentRealm, currentMode, setCurrentTab, user } = useStore();
  const navigate = useNavigate();
  const { t } = useT();
  const [openGroups, setOpenGroups] = useState<Set<string>>(new Set());

  const toggleGroup = (id: string) => {
    setOpenGroups(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const filteredNavItems = allNavItems.filter(item => {
    if (currentRealm === 'UNIFIED') return true;
    if (!item.realms) return true;
    return item.realms.includes(currentRealm);
  });

  return (
    <aside className={`w-full min-w-0 flex flex-col px-3 pt-3 pb-4 h-full transition-all duration-500 border-r bg-slate-950 border-slate-900 z-30 ${currentMode === 'REST' ? 'grayscale-[30%] opacity-90' : ''}`}>

      <div className="shrink-0 px-2 pt-3 pb-4">
        <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-600 hidden @[110px]:block">Navigation</p>
      </div>

      <nav className="flex-1 space-y-0.5 overflow-y-auto pr-1 custom-scrollbar">
        {filteredNavItems.map((item: any) => {
          const isOpen = openGroups.has(item.id);
          const hasChildren = Boolean(item.subItems?.length);
          const isActive = activeTab === item.id;
          return (
            <div key={item.id}>
              <button
                type="button"
                onClick={() => {
                  if (hasChildren) {
                    toggleGroup(item.id);
                  } else {
                    setActiveTab(item.id);
                    navigate(`/${item.id === 'dashboard' ? '' : item.id}`);
                  }
                }}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all focus:outline-none group ${
                  isActive ? 'bg-aura text-sovereign font-black shadow-xl shadow-aura/20' : 'text-slate-500 hover:text-white hover:bg-slate-900/50'
                }`}
              >
                <item.icon size={16} className={`shrink-0 transition-transform group-hover:scale-110 ${isActive ? 'text-sovereign' : 'text-aura/70'}`} />
                <span className="flex-1 text-left text-[10px] font-black uppercase tracking-widest truncate">{t(`navsec.${item.id}`, item.name)}</span>
                {hasChildren && (
                  <ChevronDown size={12} className={`shrink-0 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''} ${isActive ? 'text-sovereign' : 'text-slate-600'}`} />
                )}
              </button>
              {hasChildren && isOpen && (
                <div className="ml-5 mt-0.5 mb-1 space-y-0.5 border-l border-slate-800 pl-3">
                  {item.subItems.map((sub: any) => (
                    <button
                      key={sub.id}
                      type="button"
                      onClick={() => {
                        setActiveTab(sub.id);
                        navigate(`/${sub.id}`);
                      }}
                      className={`w-full flex items-center gap-2.5 py-1.5 px-2 rounded-lg text-[10px] font-black uppercase tracking-[0.12em] transition-all group ${
                        activeTab === sub.id ? 'text-aura bg-aura/5' : 'text-slate-600 hover:text-slate-300 hover:bg-slate-900/40'
                      }`}
                    >
                      <sub.icon size={12} className={`shrink-0 transition-opacity ${activeTab === sub.id ? 'opacity-100' : 'opacity-40 group-hover:opacity-80'}`} />
                      <span className="truncate">{t(`nav.${sub.id}`, sub.name)}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* User profile — anchored at sidebar bottom; icon-only when narrow, full when wider */}
      <div className="shrink-0 border-t border-slate-800/60 mt-2 py-3 flex items-center">
        {/* Icon centered when sidebar is narrow, left-aligned when wide */}
        <div className="flex items-center gap-2.5 min-w-0 w-full @[110px]:justify-start justify-center">
          <div className="w-8 h-8 @[130px]:w-9 @[130px]:h-9 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center font-black text-[9px] text-aura uppercase tracking-widest shrink-0">
            {(user?.displayName?.substring(0, 2) || 'CO').toUpperCase()}
          </div>
          <div className="min-w-0 hidden @[110px]:block">
            <p className="text-[10px] @[160px]:text-[11px] font-black text-white uppercase tracking-wider break-words leading-tight">{user?.displayName || 'Sovereign'}</p>
            <p className="text-[8px] text-aura/50 uppercase font-black tracking-[0.2em] truncate">{user?.role || 'Guest'}</p>
          </div>
        </div>
      </div>

    </aside>
  );
};
