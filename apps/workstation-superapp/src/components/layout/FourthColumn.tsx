import React, { useState, useCallback, useEffect, useRef } from 'react';
import axios from 'axios';
import { History, Bot, GitCommit, ChevronRight, ChevronLeft, RefreshCw } from 'lucide-react';
import { CommandCenter } from '@workstation/ui';
import { NativeAgentPanel } from '../NativeAgentPanel';
import { errorMessage } from '../../lib/api';   // W1028 - a failed read said as what it was

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
  // W491 (FU-179) - the log is the PLATFORM's own source history, and an unreadable log is not an
  // empty one; both facts have to reach the panel or it reads as the user's project activity.
  //  W1067 - each list is read on its own, each time the history is opened, and held as unread (null) until its
  //  read answers. The two were read together: one refused read took the other's answer off the column and was
  //  said as both failing; a failed read set off both reads again without end (the reader was rebuilt as its
  //  loading flag fell, and the effect ran it again); and a list read once was never read again while the shell
  //  stayed open
  const [commits, setCommits] = useState<CommitEntry[] | null>(null);
  const [gitMeta, setGitMeta] = useState<{
    repository?: string | null; readable?: boolean | null; unreadable_reason?: string | null;
    repository_commits_total?: number | null;
  } | null>(null);
  const [gitErr, setGitErr] = useState('');
  const [sessions, setSessions] = useState<SessionSummary[] | null>(null);
  const [sessionsErr, setSessionsErr] = useState('');
  const reads = useRef(0);   // the opening each answer belongs to: an earlier opening's answer is not said

  const readDock = useCallback(() => {
    const asked = ++reads.current;
    setSessions(null); setSessionsErr(''); setCommits(null); setGitMeta(null); setGitErr('');
    //  W1028 - a refused read is said by its reason (it said every failure as an unreachable server)
    axios.get('/api/v1/avatar/sessions')
      .then(s => { if (asked === reads.current) setSessions(s.data || []); })
      .catch(e => { if (asked === reads.current) setSessionsErr(`The avatar sessions could not be read: ${errorMessage(e)}`); });
    axios.get('/api/v1/workstation/git-history', { params: { limit: 12 } })
      .then(g => {
        if (asked !== reads.current) return;
        setCommits(g.data.commits || []);
        // W491 (refutation) - `readable: g.data.readable !== false` turned a MISSING field into true; an
        // absent answer is not a positive one, so it stays null and the panel says nothing either way.
        setGitMeta({ repository: g.data.repository ?? null,
                     readable: typeof g.data.readable === 'boolean' ? g.data.readable : null,
                     unreadable_reason: g.data.unreadable_reason ?? null,
                     repository_commits_total: typeof g.data.repository_commits_total === 'number'
                       ? g.data.repository_commits_total : null });
      })
      .catch(e => { if (asked === reads.current) setGitErr(`The platform commits could not be read: ${errorMessage(e)}`); });
  }, []);

  useEffect(() => {
    if (!isCollapsed && activeTab === 'projects') readDock();
  }, [isCollapsed, activeTab, readDock]);

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
            <span className="w-1 origin-bottom rounded-full bg-current h-[40%]" />
            <span className="w-1 origin-bottom rounded-full bg-current h-[70%]" />
            <span className="w-1 origin-bottom rounded-full bg-current h-[55%]" />
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
        {/* W488 (sweep S13.3, C5) — the tooltip said "External AI Agents"; the button opens
            NativeAgentPanel, the IN-HOUSE assistant served by Workstation's own fabric (external is
            opt-in and off by default). The aria-label was already right; the tooltip contradicted it. */}
        <button
          type="button"
          onClick={() => { setActiveTab('agents'); onToggle(); }}
          aria-label="In-house assistant"
          title="In-house assistant — served by Workstation's own fabric"
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
                  <span className="w-0.5 origin-bottom rounded-full bg-current h-[40%]" />
                  <span className="w-0.5 origin-bottom rounded-full bg-current h-[70%]" />
                  <span className="w-0.5 origin-bottom rounded-full bg-current h-[55%]" />
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
            {/* W1067 - each list says its own state: read, being read, or the reason it could not be read */}
            <div className="flex justify-end -mb-3">
              <button
                type="button"
                onClick={readDock}
                aria-label="Read the sessions and the commits again"
                title="Read again"
                className="p-1 rounded-lg text-slate-500 hover:text-aura transition-colors"
              >
                <RefreshCw size={11} />
              </button>
            </div>
            <div>
              <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-2">Active Avatar Sessions</p>
              {sessionsErr
                ? <p role="alert" data-testid="dock-sessions-unread" className="text-[10px] text-amber-400 font-bold leading-relaxed">{sessionsErr}</p>
                : sessions === null
                  ? <p className="text-[10px] text-slate-500 font-bold">Reading the avatar sessions…</p>
                  : sessions.length === 0
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
              <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1"
                 data-testid="git-history-heading">Workstation platform commits</p>
              <p className="text-[9px] text-slate-500 font-bold leading-relaxed mb-2" data-testid="git-history-caption">
                The source history of the Workstation install itself{gitMeta?.repository ? ` (${gitMeta.repository})` : ''} &mdash; not activity in your projects.
              </p>
              {gitErr && (
                <p role="alert" data-testid="git-history-unread" className="text-[10px] text-amber-400 font-bold leading-relaxed mb-2">{gitErr}</p>
              )}
              {!gitErr && commits === null && <p className="text-[10px] text-slate-500 font-bold">Reading the platform commits…</p>}
              {/* W491 (refutation) - the unreadable notice used to be nested inside the empty case, so a
                  log that failed PARTWAY (the parse loop runs whatever git printed before the failure)
                  rendered its partial commits with no indication at all. It is its own statement now. */}
              {gitMeta && gitMeta.readable === false && (
                <p className="text-[10px] text-amber-400 font-bold leading-relaxed mb-2" data-testid="git-history-unreadable">
                  The platform commit log could not be read whole{gitMeta.unreadable_reason ? `: ${gitMeta.unreadable_reason}` : ''}
                  {commits && commits.length > 0 ? ` - the ${commits.length} below are what was readable, not the whole history.` : '.'}
                </p>
              )}
              {commits && commits.length > 0 && (
                <p className="text-[9px] text-slate-600 font-bold mb-2" data-testid="git-history-count">
                  showing {commits.length}
                  {typeof gitMeta?.repository_commits_total === 'number'
                    ? ` of ${gitMeta.repository_commits_total} commits in the repository`
                    : ' commits (the repository total could not be read)'}
                </p>
              )}
              {commits && (commits.length === 0
                ? (gitMeta && gitMeta.readable === false
                    ? null
                    : <p className="text-[10px] text-slate-500 font-bold">No platform commits to show.</p>)
                : commits.map(c => (
                  <div key={c.hash} className="rounded-xl border border-slate-800/60 bg-slate-950/60 p-2.5 mb-2">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <GitCommit size={10} className="shrink-0 text-slate-600" />
                      <code className="text-[9px] font-mono text-slate-600 shrink-0">{c.hash}</code>
                      <span className="text-[9px] font-bold text-slate-400 truncate">{c.author}</span>
                    </div>
                    <p className="text-[10px] text-slate-300 mt-1 leading-relaxed">{c.message}</p>
                  </div>
                )))
              }
            </div>
          </div>
        )}

        {activeTab === 'agents' && <NativeAgentPanel />}
      </div>
    </div>
  );
};
