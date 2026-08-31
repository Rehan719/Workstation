import React, { useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import { History, Bot, GitCommit, ChevronRight, ChevronLeft } from 'lucide-react';
import { CommandCenter } from '@workstation/ui';
import { NativeAgentPanel } from '../NativeAgentPanel';

type DockTab = 'channels' | 'projects' | 'agents';

interface CommitEntry { hash: string; author: string; date: string; message: string; }
interface SessionSummary { session_id: string; avatar_id: string; context: string; message_count: number; last_message?: string | null; }


interface FourthColumnProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

export const FourthColumn: React.FC<FourthColumnProps> = ({ isCollapsed, onToggle }) => {
  // Default to 'projects' so the panel opens on history when first expanded
  const [activeTab, setActiveTab] = useState<DockTab>('projects');
  const [commits, setCommits] = useState<CommitEntry[]>([]);
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [dataLoading, setDataLoading] = useState(false);
  const [dataLoaded, setDataLoaded] = useState(false);
  const [dataError, setDataError] = useState('');

  const fetchDockData = useCallback(() => {
    if (dataLoaded || dataLoading) return;
    setDataLoading(true);
    Promise.all([
      axios.get('/api/v1/workstation/git-history', { params: { limit: 12 } }),
      axios.get('/api/v1/avatar/sessions'),
    ]).then(([g, s]) => {
      setCommits(g.data.commits || []);
      setSessions(s.data || []);
      setDataLoaded(true);
    }).catch(() => setDataError('Could not load data — backend unreachable.'))
      .finally(() => setDataLoading(false));
  }, [dataLoaded, dataLoading]);

  useEffect(() => {
    if (!isCollapsed && activeTab === 'projects') fetchDockData();
  }, [isCollapsed, activeTab, fetchDockData]);

  // Compact button rail shown when panel is collapsed
  if (isCollapsed) {
    return (
      <div className="flex flex-col items-center gap-3 py-4 px-1.5 h-full border-l border-slate-800/60 bg-sovereign/60 backdrop-blur-sm">
        <button
          type="button"
          onClick={onToggle}
          aria-label="Expand fourth column"
          title="Expand"
          className="p-2 rounded-lg text-slate-500 hover:text-aura transition-colors"
        >
          <ChevronLeft size={14} />
        </button>

        {/* Channels */}
        <button
          type="button"
          onClick={() => { setActiveTab('channels'); onToggle(); }}
          aria-label="Channels"
          title="Channels"
          className="p-2 rounded-lg text-slate-500 hover:text-aura transition-colors"
        >
          <div className="flex items-end gap-0.5 h-[14px] w-[14px]" aria-hidden="true">
            <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[40%] [animation-delay:0ms] [animation-duration:0.8s]" />
            <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[70%] [animation-delay:180ms] [animation-duration:0.65s]" />
            <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[55%] [animation-delay:90ms] [animation-duration:0.9s]" />
          </div>
        </button>

        {/* History / Projects */}
        <button
          type="button"
          onClick={() => { setActiveTab('projects'); onToggle(); }}
          aria-label="Projects & Sessions"
          title="Projects & Sessions"
          className="p-2 rounded-lg text-slate-500 hover:text-aura transition-colors"
        >
          <History size={14} />
        </button>

        {/* Agents */}
        <button
          type="button"
          onClick={() => { setActiveTab('agents'); onToggle(); }}
          aria-label="In-house assistant"
          title="External AI Agents"
          className="p-2 rounded-lg text-slate-500 hover:text-aura transition-colors"
        >
          <Bot size={14} />
        </button>
      </div>
    );
  }

  // Expanded: full content
  return (
    <div className="flex flex-col h-full border-l border-slate-800/60 bg-sovereign/60 backdrop-blur-sm @container min-w-0">
      {/* Tab nav */}
      <div className="shrink-0 border-b border-slate-800/40">
        <div className="flex items-stretch gap-px p-1.5">
          <button
            type="button"
            onClick={onToggle}
            aria-label="Collapse fourth column"
            title="Collapse"
            className="p-2 rounded-lg text-slate-500 hover:text-aura transition-colors shrink-0"
          >
            <ChevronRight size={14} />
          </button>

          {([
            {
              id: 'channels' as DockTab,
              label: 'Channels',
              icon: (
                <div className="flex items-end gap-0.5 h-[12px] w-[12px] shrink-0" aria-hidden="true">
                  <span className="w-0.5 origin-bottom rounded-full bg-current animate-eq-bar h-[40%] [animation-delay:0ms] [animation-duration:0.8s]" />
                  <span className="w-0.5 origin-bottom rounded-full bg-current animate-eq-bar h-[70%] [animation-delay:180ms] [animation-duration:0.65s]" />
                  <span className="w-0.5 origin-bottom rounded-full bg-current animate-eq-bar h-[55%] [animation-delay:90ms] [animation-duration:0.9s]" />
                </div>
              ),
            },
            { id: 'projects' as DockTab, label: 'History', icon: <History size={12} className="shrink-0" /> },
            { id: 'agents'   as DockTab, label: 'Agents',  icon: <Bot size={12} className="shrink-0" /> },
          ] as const).map(tab => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id)}
              aria-label={tab.label}
              title={tab.label}
              className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg transition-all ${
                activeTab === tab.id
                  ? 'bg-aura/15 text-aura'
                  : 'text-slate-500 hover:text-slate-300 hover:bg-slate-800/50'
              }`}
            >
              {tab.icon}
              <span className="text-[9px] font-black uppercase tracking-widest truncate @[160px]:inline hidden">
                {tab.label}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar p-3">
        {activeTab === 'channels' && <CommandCenter tiled />}

        {activeTab === 'projects' && (
          <div className="space-y-5">
            {dataLoading && <p className="text-[10px] text-slate-500 font-bold">Loading…</p>}
            {dataError && <p className="text-[10px] text-amber-400 font-bold leading-relaxed">{dataError}</p>}
            {!dataLoading && !dataError && (
              <>
                <div>
                  <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Active Avatar Sessions</p>
                  {sessions.length === 0
                    ? <p className="text-[10px] text-slate-500 font-bold leading-relaxed">No active sessions yet.</p>
                    : sessions.map(s => (
                      <div key={s.session_id} className="rounded-xl border border-slate-800 bg-slate-950 p-2.5 mb-2">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-[9px] font-black uppercase text-slate-400 truncate">{s.context}</span>
                          <span className="text-[8px] font-bold text-slate-600 shrink-0">{s.message_count} msg</span>
                        </div>
                        {s.last_message && <p className="text-[10px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">{s.last_message}</p>}
                      </div>
                    ))
                  }
                </div>
                <div>
                  <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Recent Project Activity</p>
                  {commits.length === 0
                    ? <p className="text-[10px] text-slate-500 font-bold">No commit history available.</p>
                    : commits.map(c => (
                      <div key={c.hash} className="rounded-xl border border-slate-800/60 bg-slate-950/60 p-2.5 mb-2">
                        <div className="flex items-center gap-1.5 min-w-0">
                          <GitCommit size={10} className="shrink-0 text-slate-600" />
                          <code className="text-[9px] font-mono text-slate-600 shrink-0">{c.hash}</code>
                          <span className="text-[9px] font-bold text-slate-400 truncate">{c.author}</span>
                        </div>
                        <p className="text-[10px] text-slate-300 mt-1 leading-relaxed">{c.message}</p>
                      </div>
                    ))
                  }
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === 'agents' && <NativeAgentPanel />}
      </div>
    </div>
  );
};
