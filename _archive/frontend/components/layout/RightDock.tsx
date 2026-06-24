import React, { useEffect, useRef, useState, useCallback } from 'react';
import axios from 'axios';
import { History, Bot, ChevronLeft, ChevronRight, GitCommit } from 'lucide-react';
import { CommandCenter } from '@workstation/ui';
import { widthPxClass, RIGHT_DOCK_COLLAPSED_PX, RIGHT_DOCK_MIN_PX, RIGHT_DOCK_MAX_PX } from '../../lib/progressWidth';

type DockTab = 'channels' | 'projects' | 'agents';

const AUTO_COLLAPSE_MS = 4000;

interface CommitEntry {
  hash: string;
  author: string;
  date: string;
  message: string;
}

interface SessionSummary {
  session_id: string;
  avatar_id: string;
  context: string;
  message_count: number;
  last_message?: string | null;
}

// Real authors whose commits in this repo's own history are external coding
// agents — used only to surface genuine, verifiable past activity. Not a
// live-connection indicator.
const KNOWN_AGENT_AUTHOR_PATTERNS = [
  { pattern: /jules/i, label: 'Google Jules' },
  { pattern: /claude/i, label: 'Claude' },
  { pattern: /copilot/i, label: 'GitHub Copilot' },
];

const ProjectsSessionsContent: React.FC<{ commits: CommitEntry[]; sessions: SessionSummary[]; loading: boolean; error: string }> = ({ commits, sessions, loading, error }) => {
  if (loading) return <p className="text-[10px] text-slate-500 font-bold">Loading…</p>;
  if (error) return <p className="text-[10px] text-amber-400 font-bold leading-relaxed">{error}</p>;

  return (
    <div className="space-y-5">
      <div>
        <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Active Avatar Sessions</p>
        {sessions.length === 0 ? (
          <p className="text-[10px] text-slate-500 font-bold leading-relaxed">No active sessions yet — start a conversation with the avatar to see it here.</p>
        ) : (
          <div className="space-y-2">
            {sessions.map(s => (
              <div key={s.session_id} className="rounded-xl border border-slate-800 bg-slate-950 p-2.5">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[9px] font-black uppercase text-slate-400 truncate">{s.context}</span>
                  <span className="text-[8px] font-bold text-slate-600 shrink-0">{s.message_count} msg</span>
                </div>
                {s.last_message && <p className="text-[10px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">{s.last_message}</p>}
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Recent Project Activity</p>
        {commits.length === 0 ? (
          <p className="text-[10px] text-slate-500 font-bold">No commit history available.</p>
        ) : (
          <div className="space-y-2">
            {commits.map(c => (
              <div key={c.hash} className="rounded-xl border border-slate-800/60 bg-slate-950/60 p-2.5">
                <div className="flex items-center gap-1.5 min-w-0">
                  <GitCommit size={10} className="shrink-0 text-slate-600" />
                  <code className="text-[9px] font-mono text-slate-600 shrink-0">{c.hash}</code>
                  <span className="text-[9px] font-bold text-slate-400 truncate">{c.author}</span>
                </div>
                <p className="text-[10px] text-slate-300 mt-1 leading-relaxed">{c.message}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const ExternalAgentsContent: React.FC<{ commits: CommitEntry[]; loading: boolean; error: string }> = ({ commits, loading, error }) => {
  const detected = KNOWN_AGENT_AUTHOR_PATTERNS
    .map(({ pattern, label }) => ({ label, count: commits.filter(c => pattern.test(c.author)).length }))
    .filter(d => d.count > 0);

  return (
    <div className="space-y-4">
      <p className="text-[10px] font-bold text-slate-500 leading-relaxed">
        No live connection to an external coding agent (e.g. Claude Code, Google Jules) running in VS Code is wired
        into Workstation yet — this is a real, honest status panel, not a fake "connected" indicator.
      </p>

      {loading ? (
        <p className="text-[10px] text-slate-500 font-bold">Checking project history…</p>
      ) : error ? (
        <p className="text-[10px] text-amber-400 font-bold">{error}</p>
      ) : detected.length > 0 ? (
        <div>
          <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Detected in Project History</p>
          <div className="space-y-2">
            {detected.map(d => (
              <div key={d.label} className="rounded-xl border border-slate-800 bg-slate-950 p-2.5 flex items-center justify-between">
                <span className="text-[10px] font-bold text-slate-300">{d.label}</span>
                <span className="text-[8px] font-black uppercase text-emerald-400">{d.count} commit{d.count === 1 ? '' : 's'}</span>
              </div>
            ))}
          </div>
          <p className="text-[9px] text-slate-600 font-bold mt-2 leading-relaxed">
            This reflects real past commits in this repo's git history — not a live session.
          </p>
        </div>
      ) : (
        <div className="rounded-xl border border-slate-800 bg-slate-950 p-2.5">
          <p className="text-[10px] font-bold text-slate-500">No external-agent commits found in recent project history.</p>
        </div>
      )}
    </div>
  );
};

/**
 * Far-right, full-height, auto-collapsing/resizable dock — the same Channels
 * UX pattern extended into its own column, with two new real-data tabs:
 * "Workstation Projects & Sessions" (real git history + real avatar
 * sessions) and "External AI Agents" (an honest, non-fabricated status panel
 * with real evidence of past agent activity pulled from git history).
 */
export const RightDock: React.FC = () => {
  const [collapsed, setCollapsed] = useState(true);
  const [activeTab, setActiveTab] = useState<DockTab>('channels');
  const [widthPx, setWidthPx] = useState(280);

  const [commits, setCommits] = useState<CommitEntry[]>([]);
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [dataLoading, setDataLoading] = useState(false);
  const [dataLoaded, setDataLoaded] = useState(false);
  const [dataError, setDataError] = useState('');

  const containerRef = useRef<HTMLDivElement>(null);
  const collapseTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const dragState = useRef<{ startX: number; startWidth: number } | null>(null);

  const scheduleCollapse = useCallback(() => {
    if (collapseTimer.current) clearTimeout(collapseTimer.current);
    collapseTimer.current = setTimeout(() => setCollapsed(true), AUTO_COLLAPSE_MS);
  }, []);

  useEffect(() => {
    if (!collapsed) scheduleCollapse();
    return () => { if (collapseTimer.current) clearTimeout(collapseTimer.current); };
  }, [collapsed, activeTab, scheduleCollapse]);

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
    }).catch(() => setDataError('Could not load project/session data — backend unreachable.'))
      .finally(() => setDataLoading(false));
  }, [dataLoaded, dataLoading]);

  const openTab = (tab: DockTab) => {
    setActiveTab(tab);
    setCollapsed(false);
    if (tab === 'projects' || tab === 'agents') fetchDockData();
    scheduleCollapse();
  };

  const handleDragStart = (e: React.MouseEvent) => {
    dragState.current = { startX: e.clientX, startWidth: widthPx };
    const handleMove = (moveEvent: MouseEvent) => {
      if (!dragState.current) return;
      const delta = dragState.current.startX - moveEvent.clientX;
      const next = Math.max(RIGHT_DOCK_MIN_PX, Math.min(RIGHT_DOCK_MAX_PX, dragState.current.startWidth + delta));
      setWidthPx(next);
    };
    const handleUp = () => {
      dragState.current = null;
      document.removeEventListener('mousemove', handleMove);
      document.removeEventListener('mouseup', handleUp);
    };
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', handleUp);
  };

  const tabButton = (tab: DockTab, label: string, Icon: React.ElementType) => {
    const isActive = !collapsed && activeTab === tab;
    return (
      <button
        type="button"
        onClick={() => openTab(tab)}
        aria-label={label}
        title={label}
        className={`p-2.5 rounded-xl transition-all ${isActive ? 'bg-aura/15 text-aura' : 'bg-slate-800 text-slate-400 hover:text-aura'}`}
      >
        <Icon size={18} />
      </button>
    );
  };

  return (
    <div
      ref={containerRef}
      className="relative h-full flex shrink-0"
      onMouseEnter={() => { if (collapseTimer.current) clearTimeout(collapseTimer.current); }}
      onMouseLeave={scheduleCollapse}
    >
      {!collapsed && (
        <div
          onMouseDown={handleDragStart}
          className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30 shrink-0"
          role="separator"
          aria-orientation="vertical"
          aria-label="Resize Workstation dock width"
        />
      )}

      <div className={`h-full border-l border-slate-800/60 bg-sovereign/60 backdrop-blur-sm flex flex-col shrink-0 ${collapsed ? widthPxClass(RIGHT_DOCK_COLLAPSED_PX) : widthPxClass(widthPx)}`}>
        <div className="flex flex-col items-center gap-2 py-4 shrink-0 border-b border-slate-800/40">
          <button
            type="button"
            onClick={() => setCollapsed(c => !c)}
            aria-label={collapsed ? 'Expand Workstation dock' : 'Collapse Workstation dock'}
            title={collapsed ? 'Expand' : 'Collapse'}
            className="p-1.5 rounded-lg text-slate-600 hover:text-white transition-colors mb-1"
          >
            {collapsed ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
          </button>
          {tabButton('channels', 'Channels', () => (
            <div className="flex items-end gap-0.5 h-[18px] w-[18px]" aria-hidden="true">
              <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[40%] [animation-delay:0ms] [animation-duration:0.8s]" />
              <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[70%] [animation-delay:180ms] [animation-duration:0.65s]" />
              <span className="w-1 origin-bottom rounded-full bg-current animate-eq-bar h-[55%] [animation-delay:90ms] [animation-duration:0.9s]" />
            </div>
          ))}
          {tabButton('projects', 'Workstation Projects & Sessions', History)}
          {tabButton('agents', 'External AI Agents', Bot)}
        </div>

        {!collapsed && (
          <div className="flex-1 min-h-0 min-w-0">
            {activeTab === 'channels' && (
              <div className="p-3">
                <CommandCenter dropDirection="down" />
              </div>
            )}
            {activeTab === 'projects' && (
              <div className="h-full overflow-y-auto custom-scrollbar p-3">
                <ProjectsSessionsContent commits={commits} sessions={sessions} loading={dataLoading} error={dataError} />
              </div>
            )}
            {activeTab === 'agents' && (
              <div className="h-full overflow-y-auto custom-scrollbar p-3">
                <ExternalAgentsContent commits={commits} loading={dataLoading} error={dataError} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
