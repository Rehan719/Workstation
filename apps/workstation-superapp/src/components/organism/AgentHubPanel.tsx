/**
 * W443 — the Agent Collaboration Hub's first surface.
 *
 * The hub's 7 backend ops (messages, SSE stream, registry, work-order letterbox) were live,
 * unauthenticated HTTP with zero consumers — a real bus with no riders, and handoffs were
 * write-only files nobody could see. This panel makes the whole thing VISIBLE and honest:
 *   • the participants list splits external registrations (usually empty — said plainly)
 *     from the swarm's live platform roster;
 *   • the message feed shows stored history and live SSE events, and posting reports how
 *     many live subscribers actually received the message;
 *   • the work-order letterbox renders every handoff with its true status — "recorded"
 *     means recorded: no executor is subscribed and nothing runs these automatically.
 */
import React, { useEffect, useRef, useState } from 'react';
import { Card, Button } from '@workstation/ui';
import { Radio, Loader2, AlertCircle, ShieldCheck, Send, Inbox, Users } from 'lucide-react';

interface HubMsg {
  id: string; timestamp: string; sender_id: string; sender_role: string;
  posted_by?: string; channel: string; content: string;
}
interface Handoff {
  handoff_id: string; created_at: string; from_agent: string; to_agent: string;
  task_title: string; task_description: string; priority: string;
  status: string; status_note?: string; filed_by?: string;
}

const AgentHubPanel: React.FC = () => {
  const [agents, setAgents] = useState<any>(null);
  const [msgs, setMsgs] = useState<HubMsg[]>([]);
  // W443 refuter catch: a failed message load was swallowed into msgs=[] and rendered the
  // honest-looking "quiet bus" empty state — a false statement over a failed read.
  const [msgsFailed, setMsgsFailed] = useState(false);
  const [handoffs, setHandoffs] = useState<Handoff[] | null>(null);
  const [loadErr, setLoadErr] = useState('');
  // 'sse' = live EventSource; 'polling' = auth mode fallback (EventSource cannot carry the
  // bearer header, so under auth the stream 401s — refuter catch); 'off' = no live channel
  const [feedMode, setFeedMode] = useState<'off' | 'sse' | 'polling'>('off');
  const [draft, setDraft] = useState('');
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState('');
  const [err, setErr] = useState('');
  const esRef = useRef<EventSource | null>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const jget = (url: string) => fetch(url).then(r => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  });

  const loadMsgs = () =>
    jget('/api/v1/hub/messages?limit=30')
      .then(d => { setMsgs(d); setMsgsFailed(false); })
      .catch(() => setMsgsFailed(true));

  const loadAll = () => {
    setLoadErr('');
    jget('/api/v1/hub/agents').then(setAgents).catch(e => setLoadErr(`Hub unreachable — ${e.message}`));
    loadMsgs();
    jget('/api/v1/hub/handoffs?limit=20').then(d => setHandoffs(d.handoffs)).catch(() => setHandoffs(null));
  };

  useEffect(() => {
    loadAll();
    // live feed — a real SSE stream (single-process, at-most-once; a 'gap' event means this
    // client was slow and missed history). EventSource cannot send the auth bearer header, so
    // when the stream errors (e.g. auth enabled → 401) we fall back to honest 10s polling
    // through fetch, which the app's auth layer does cover.
    const es = new EventSource('/api/v1/hub/stream');
    esRef.current = es;
    es.onopen = () => {
      setFeedMode('sse');
      if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null; }
    };
    es.onerror = () => {
      setFeedMode(prev => {
        if (prev !== 'polling' && !pollRef.current) {
          pollRef.current = setInterval(loadMsgs, 10000);
        }
        return 'polling';
      });
    };
    es.onmessage = e => {
      try {
        const payload = JSON.parse(e.data);
        if (payload.event === 'message' && payload.data) {
          setMsgs(prev => [payload.data, ...prev].slice(0, 50));
        }
      } catch { /* heartbeats/gaps are not renderable messages */ }
    };
    return () => { es.close(); if (pollRef.current) clearInterval(pollRef.current); };
  }, []);

  const post = async () => {
    setBusy(true); setNotice(''); setErr('');
    try {
      const r = await fetch('/api/v1/hub/message', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender_id: 'owner-console', sender_role: 'USER', content: draft }),
      });
      const d = await r.json();
      if (!r.ok) { setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); setBusy(false); return; }
      // W443 refuter catch: "(including this panel)" was claimed unconditionally — it is only
      // true when THIS panel's stream is actually connected; and without the SSE echo the
      // poster's own message never appeared until a remount, so refetch when not live.
      setNotice(d.delivered_to_live_subscribers > 0
        ? `Delivered live to ${d.delivered_to_live_subscribers} subscriber(s)${feedMode === 'sse' ? ' (including this panel)' : ''}.`
        : 'Stored — no live subscribers received it (nothing on the platform consumes hub messages by itself).');
      setDraft('');
      if (feedMode !== 'sse') loadMsgs();
    } catch (e: any) { setErr(e?.message ?? String(e)); }
    setBusy(false);
  };

  const moveStatus = async (id: string, status: 'in_progress' | 'done') => {
    setErr('');
    try {
      const r = await fetch(`/api/v1/hub/handoffs/${id}/status`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });
      if (!r.ok) { const d = await r.json(); setErr(typeof d.detail === 'string' ? d.detail : `HTTP ${r.status}`); return; }
      jget('/api/v1/hub/handoffs?limit=20').then(d => setHandoffs(d.handoffs)).catch(() => {});
    } catch (e: any) { setErr(e?.message ?? String(e)); }
  };

  return (
    <div className="space-y-6">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-1">Respiratory layer · Agent Hub</p>
        <h2 className="text-2xl font-black tracking-tight text-white uppercase italic">Agent Collaboration Hub</h2>
        <p className="text-slate-500 text-xs font-bold mt-1 max-w-3xl leading-relaxed">
          A real file-backed message bus with a live SSE stream — shown exactly as occupied as it is.
          <span className="text-amber-400"> No platform module consumes hub messages yet; work-orders are records, not executions.</span>
        </p>
        {loadErr && <p role="alert" className="text-[10px] font-bold text-vital mt-2">{loadErr}</p>}
      </header>

      {/* participants */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-3">
          <Users size={13} /> Participants
        </h3>
        <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-4">
          <div>
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1.5">Registered sessions</p>
            {(agents?.registered?.length ?? 0) === 0
              ? <p className="text-[10px] text-slate-600 italic">none — no external agent session has registered on the hub</p>
              : agents.registered.map((a: any) => (
                <p key={a.agent_id} className="text-[10px] text-slate-300 font-mono">
                  {a.agent_id} <span className="text-slate-600">· {a.role} · last active {String(a.last_active).slice(0, 19)}</span>
                </p>
              ))}
          </div>
          <div>
            <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1.5">Platform roster (swarm, live)</p>
            <div className="flex flex-wrap gap-1.5">
              {(agents?.platform_roster ?? []).map((a: any) => (
                <span key={a.id} className="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-800 text-[9px] font-bold text-slate-400" title={a.expertise}>
                  {a.role}
                </span>
              ))}
            </div>
          </div>
        </div>
        {agents?.note && <p className="text-[9px] text-slate-600 italic mt-3">{agents.note}</p>}
      </Card>

      {/* message feed + post */}
      <Card className="p-5">
        <div className="flex items-center justify-between gap-3 flex-wrap mb-3">
          <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2">
            <Radio size={13} /> Message bus
          </h3>
          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${feedMode === 'sse' ? 'bg-emerald-500/15 text-emerald-400' : feedMode === 'polling' ? 'bg-amber-500/15 text-amber-400' : 'bg-slate-800 text-slate-500'}`}>
            {feedMode === 'sse' ? 'stream connected (SSE)'
              : feedMode === 'polling' ? 'polling every 10s — live SSE unavailable (auth mode or stream error)'
              : 'connecting…'}
          </span>
        </div>
        <div className="flex items-end gap-2 mb-4">
          <div className="flex-1">
            <input value={draft} onChange={e => setDraft(e.target.value)} aria-label="hub message"
              placeholder="post to the general channel as USER…"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-highlight/50" />
          </div>
          <Button onClick={post} disabled={busy || !draft.trim()} className="flex items-center gap-1.5 bg-highlight text-sovereign text-[10px]">
            {busy ? <Loader2 size={12} className="animate-spin" /> : <Send size={12} />} Post
          </Button>
        </div>
        {notice && <p className="text-emerald-400 text-[10px] font-bold mb-2 flex items-center gap-1.5"><ShieldCheck size={12} /> {notice}</p>}
        {err && <p className="text-vital text-[10px] font-bold mb-2 flex items-center gap-1.5"><AlertCircle size={12} /> {err}</p>}
        <div className="space-y-1.5 max-h-72 overflow-y-auto">
          {msgsFailed && <p role="alert" className="text-[10px] font-bold text-vital">message feed unavailable — the read failed (this is not a quiet bus)</p>}
          {!msgsFailed && msgs.length === 0 && <p className="text-[10px] text-slate-600 italic">no messages — the bus is real, and currently quiet</p>}
          {msgs.map(m => (
            <div key={m.id} className="p-2.5 rounded-lg bg-slate-950 border border-slate-900">
              <div className="flex items-center justify-between gap-2 text-[9px] font-mono text-slate-600">
                <span><span className="text-slate-400 font-bold">{m.sender_id}</span> · {m.sender_role} · #{m.channel}</span>
                <span>{String(m.timestamp).slice(0, 19)}</span>
              </div>
              <p className="text-xs text-slate-300 mt-1 whitespace-pre-wrap break-words">{m.content}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* work-order letterbox */}
      <Card className="p-5">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-500 flex items-center gap-2 mb-1">
          <Inbox size={13} /> Work-order letterbox (handoffs)
        </h3>
        <p className="text-[10px] text-slate-500 font-bold mb-3">
          Structured work-orders filed via the hub. <span className="text-amber-400">Records only — no executor is
          subscribed; nothing runs these automatically.</span> A person (or a future consumer behind an Owner
          approval gate) moves their status here.
        </p>
        {handoffs === null && <p className="text-[10px] text-slate-600 italic">letterbox unavailable</p>}
        {handoffs !== null && handoffs.length === 0 && <p className="text-[10px] text-slate-600 italic">no work-orders filed</p>}
        <div className="space-y-2">
          {(handoffs ?? []).map(h => (
            <div key={h.handoff_id} className="p-3 rounded-xl bg-slate-950 border border-slate-900">
              <div className="flex items-center justify-between gap-2 flex-wrap">
                <p className="text-sm font-black text-white truncate">{h.task_title}</p>
                <div className="flex items-center gap-1.5 shrink-0">
                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${h.priority === 'critical' ? 'bg-vital/15 text-vital' : h.priority === 'high' ? 'bg-amber-500/15 text-amber-400' : 'bg-slate-800 text-slate-400'}`}>{h.priority}</span>
                  <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${h.status === 'done' ? 'bg-emerald-500/15 text-emerald-400' : h.status === 'in_progress' ? 'bg-aura/15 text-aura' : 'bg-slate-800 text-slate-400'}`}>{h.status}</span>
                </div>
              </div>
              <p className="text-[10px] text-slate-500 mt-1 line-clamp-2">{h.task_description}</p>
              <div className="flex items-center justify-between gap-2 mt-1.5">
                <p className="text-[9px] font-mono text-slate-600">{h.from_agent} → {h.to_agent} · {String(h.created_at).slice(0, 19)}</p>
                <div className="flex items-center gap-1.5">
                  {h.status === 'recorded' && (
                    <button type="button" onClick={() => moveStatus(h.handoff_id, 'in_progress')}
                      className="text-[9px] font-black uppercase text-aura hover:underline">claim</button>
                  )}
                  {h.status !== 'done' && (
                    <button type="button" onClick={() => moveStatus(h.handoff_id, 'done')}
                      className="text-[9px] font-black uppercase text-emerald-400 hover:underline">mark done</button>
                  )}
                </div>
              </div>
              {h.status_note && <p className="text-[9px] text-slate-600 italic mt-1">{h.status_note}</p>}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default AgentHubPanel;
