import React, { useState, useEffect, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Search, X, ArrowRight,
  LayoutDashboard, MessageSquare, Package, DollarSign, Sparkles, ShoppingBag, Archive,
  Cpu, Network, Globe, Factory, Zap,
  Heart, Microscope, GraduationCap, Gavel, HeartPulse, Briefcase,
  Fingerprint, Brain,
  FileText, History, ShieldCheck,
  Terminal, Camera, Map, FolderOpen, Settings
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '@workstation/shared';

interface SearchEntry {
  id: string;
  label: string;
  description: string;
  category: string;
  icon: React.ElementType;
  route: string;
}

const SEARCH_INDEX: SearchEntry[] = [
  { id: 'dashboard',       label: 'Dashboard',         description: 'Command center overview',              category: 'Core',        icon: LayoutDashboard, route: '/' },
  { id: 'ceo',             label: 'AI CEO',             description: 'Consult your autonomous executive',    category: 'Productivity', icon: MessageSquare,   route: '/ceo' },
  { id: 'bto',             label: 'Build to Order',      description: 'BTO configurator & sovereign entity builder',  category: 'Productivity', icon: Package,    route: '/bto' },
  { id: 'capital',         label: 'Capital Fund',       description: 'Investment allocation & reporting',    category: 'Productivity', icon: DollarSign,      route: '/capital' },
  { id: 'synthesis',       label: 'Synthesis Studio',   description: 'Ingest knowledge & generate reports', category: 'Productivity', icon: Sparkles,        route: '/synthesis' },
  { id: 'marketplace',     label: 'Marketplace',        description: 'Agents, products & build-to-order',   category: 'Productivity', icon: ShoppingBag,     route: '/marketplace' },
  { id: 'solutions',        label: 'Solutions Platform', description: 'Design · Build · Launch AI-mediated solutions', category: 'Productivity', icon: Zap,       route: '/solutions' },
  { id: 'qep-religion',    label: 'Religion',           description: 'Quran Education Platform hub',        category: 'Domains',     icon: Heart,           route: '/qep-religion' },
  { id: 'science',         label: 'Science',            description: 'Scientific research & discovery',     category: 'Domains',     icon: Microscope,      route: '/science' },
  { id: 'education',       label: 'Education',          description: 'Learning & teaching platform',        category: 'Domains',     icon: GraduationCap,   route: '/education' },
  { id: 'law',             label: 'Law',                description: 'Legal research & governance',         category: 'Domains',     icon: Gavel,           route: '/law' },
  { id: 'care',            label: 'Care',               description: 'Health & wellbeing services',         category: 'Domains',     icon: HeartPulse,      route: '/care' },
  { id: 'employment',      label: 'Employment',         description: 'Career, CVs & job marketplace',       category: 'Domains',     icon: Briefcase,       route: '/employment' },
  { id: 'genome-explorer', label: 'Genome',             description: 'System evolution & GRN mesh',         category: 'Evolution',   icon: Fingerprint,     route: '/genome-explorer' },
  { id: 'grn-dashboard',   label: 'GRN Mesh',           description: 'Gene regulatory network dashboard',   category: 'Evolution',   icon: Network,         route: '/grn-dashboard' },
  { id: 'introspection',   label: 'Introspection',      description: 'Cognitive self-analysis & memory',    category: 'Evolution',   icon: Brain,           route: '/introspection' },
  { id: 'orchestrator',    label: 'Homeostasis',        description: 'Organism balance & vital signs',      category: 'Evolution',   icon: HeartPulse,      route: '/orchestrator' },
  { id: 'constitution',    label: 'Constitution',       description: 'Constitutional articles & law',       category: 'Governance',  icon: FileText,        route: '/constitution' },
  { id: 'transparency',    label: 'Transparency',       description: 'Audit trail & transparency log',      category: 'Governance',  icon: History,         route: '/transparency' },
  { id: 'admin',           label: 'Entity Control',     description: 'User & entity management panel',      category: 'Governance',  icon: ShieldCheck,     route: '/admin' },
  { id: 'governance-hub',  label: 'Governance Hub',     description: 'Audit, Sovereign Vault & The Sanctum',category: 'Governance',  icon: ShieldCheck,     route: '/governance-hub' },
  { id: 'forge',           label: 'The Forge',          description: 'Developer tooling & pipelines',       category: 'Advanced',    icon: Terminal,        route: '/forge' },
  { id: 'ar-vr',           label: 'AR/VR Lab',          description: 'Immersive spatial computing lab',     category: 'Advanced',    icon: Camera,          route: '/ar-vr' },
  { id: 'fed-map',         label: 'Federation',         description: 'Multi-node federation map',           category: 'Advanced',    icon: Map,             route: '/fed-map' },
  { id: 'file-hub',        label: 'File Hub',           description: 'Sovereign file management system',    category: 'Advanced',    icon: FolderOpen,      route: '/file-hub' },
  { id: 'settings',        label: 'System Settings',    description: 'Platform configuration & preferences',category: 'Advanced',    icon: Settings,        route: '/settings' },
];

interface SearchMeshModalProps {
  open: boolean;
  onClose: () => void;
}

export const SearchMeshModal: React.FC<SearchMeshModalProps> = ({ open, onClose }) => {
  const [query, setQuery] = useState('');
  const [focused, setFocused] = useState(0);
  const navigate = useNavigate();
  const { setCurrentTab } = useStore();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setQuery('');
      setFocused(0);
      setTimeout(() => inputRef.current?.focus(), 30);
    }
  }, [open]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!open) return;
      if (e.key === 'Escape') { onClose(); return; }
      if (e.key === 'ArrowDown') { e.preventDefault(); setFocused(f => Math.min(f + 1, filteredFlat.length - 1)); }
      if (e.key === 'ArrowUp') { e.preventDefault(); setFocused(f => Math.max(f - 1, 0)); }
      if (e.key === 'Enter' && filteredFlat[focused]) go(filteredFlat[focused]);
    };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, focused, query]);

  const filteredFlat = query.trim()
    ? SEARCH_INDEX.filter(e =>
        e.label.toLowerCase().includes(query.toLowerCase()) ||
        e.description.toLowerCase().includes(query.toLowerCase()) ||
        e.category.toLowerCase().includes(query.toLowerCase())
      )
    : SEARCH_INDEX;

  const grouped = filteredFlat.reduce<Record<string, SearchEntry[]>>((acc, item) => {
    (acc[item.category] ??= []).push(item);
    return acc;
  }, {});

  const go = (entry: SearchEntry) => {
    setCurrentTab(entry.id);
    navigate(entry.route);
    onClose();
  };

  if (!open) return null;

  let globalIdx = 0;

  return (
    <AnimatePresence>
      <div
        className="fixed inset-0 z-[300] flex items-start justify-center pt-[14vh] bg-sovereign/80 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.96, y: -16 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.96 }}
          transition={{ duration: 0.15 }}
          className="w-full max-w-2xl bg-slate-950 border border-slate-800 rounded-3xl shadow-2xl overflow-hidden"
          onClick={e => e.stopPropagation()}
        >
          {/* Search input */}
          <div className="flex items-center gap-3 px-6 py-4 border-b border-slate-800">
            <Search size={17} className="text-aura shrink-0" />
            <input
              ref={inputRef}
              value={query}
              onChange={e => { setQuery(e.target.value); setFocused(0); }}
              placeholder="Search Sovereign Mesh…"
              className="flex-1 bg-transparent border-none outline-none text-base font-bold placeholder-slate-600 text-white"
            />
            {query && (
              <button type="button" onClick={() => setQuery('')} aria-label="Clear search" title="Clear search" className="p-1 text-slate-600 hover:text-white transition-colors">
                <X size={14} />
              </button>
            )}
            <button type="button" onClick={onClose} aria-label="Close search" title="Close search" className="p-1.5 text-slate-600 hover:text-white transition-colors border-l border-slate-800 pl-3 ml-1">
              <X size={16} />
            </button>
          </div>

          {/* Results */}
          <div className="max-h-[420px] overflow-y-auto custom-scrollbar p-3">
            {filteredFlat.length === 0 ? (
              <p className="text-center text-slate-600 font-bold text-sm py-10">No results for "{query}"</p>
            ) : (
              Object.entries(grouped).map(([category, items]) => (
                <div key={category} className="mb-3">
                  <p className="text-[9px] font-black uppercase tracking-[0.25em] text-slate-600 px-3 mb-1.5">{category}</p>
                  {items.map(item => {
                    const idx = globalIdx++;
                    return (
                      <button
                        key={item.id}
                        onClick={() => go(item)}
                        onMouseEnter={() => setFocused(idx)}
                        className={`w-full flex items-center gap-4 px-4 py-2.5 rounded-xl transition-all group text-left ${
                          focused === idx ? 'bg-aura/10' : 'hover:bg-slate-900/60'
                        }`}
                      >
                        <div className={`p-2 rounded-lg shrink-0 transition-colors ${focused === idx ? 'bg-aura/10 text-aura' : 'bg-slate-900 text-slate-500'}`}>
                          <item.icon size={15} />
                        </div>
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-black text-white truncate">{item.label}</p>
                          <p className="text-[10px] text-slate-500 font-bold truncate">{item.description}</p>
                        </div>
                        <ArrowRight size={13} className={`shrink-0 transition-colors ${focused === idx ? 'text-aura' : 'text-slate-700'}`} />
                      </button>
                    );
                  })}
                </div>
              ))
            )}
          </div>

          {/* Footer hints */}
          <div className="px-6 py-3 border-t border-slate-800 flex items-center gap-5 text-[10px] font-black text-slate-600">
            <span><kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-[9px] mr-1">↑↓</kbd>Navigate</span>
            <span><kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-[9px] mr-1">↵</kbd>Open</span>
            <span><kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-[9px] mr-1">Esc</kbd>Close</span>
            <span className="ml-auto text-slate-700">{filteredFlat.length} results</span>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
