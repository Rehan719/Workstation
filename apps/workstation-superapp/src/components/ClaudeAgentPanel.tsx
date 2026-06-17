/**
 * ClaudeAgentPanel — a direct Claude chat embedded in the fourth column's
 * Agents tab.
 *
 * Model strategy:
 *   • On mount, GET /api/v1/claude/status to check whether an Anthropic API
 *     key is configured in the backend.
 *   • If authenticated → default to claude-sonnet-4-6 (paid).
 *   • Otherwise        → default to claude-haiku-4-5-20251001 (free/cheapest).
 *   • The user can always switch with the model toggle.
 *
 * Messages are sent to POST /api/v1/claude/chat with the full history so
 * the model has context across the conversation.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { Send, Loader2, Trash2 } from 'lucide-react';

interface Msg { role: 'user' | 'assistant'; content: string; }

const MODELS = {
  free: { id: 'claude-haiku-4-5-20251001', label: 'Haiku', note: 'free · fast' },
  paid: { id: 'claude-sonnet-4-6',          label: 'Sonnet', note: 'paid · smart' },
} as const;

type ModelKey = keyof typeof MODELS;

const SYSTEM_PROMPT =
  'You are Claude, an AI assistant embedded in Workstation — a sovereign intelligence platform. ' +
  'Be concise, precise, and practical. You have awareness of the Workstation context (realms, avatar, cognition layers) and can discuss or assist with any task the user brings.';

export const ClaudeAgentPanel: React.FC = () => {
  const [messages, setMessages]   = useState<Msg[]>([]);
  const [input, setInput]         = useState('');
  const [sending, setSending]     = useState(false);
  const [modelKey, setModelKey]   = useState<ModelKey>('free');
  const [status, setStatus]       = useState<'checking' | 'ready' | 'error'>('checking');
  const [statusNote, setStatusNote] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  // Probe backend; auto-select paid model if API key is present
  useEffect(() => {
    axios.get('/api/v1/claude/status', { timeout: 3000 })
      .then(res => {
        const authenticated: boolean = res.data?.authenticated ?? false;
        setModelKey(authenticated ? 'paid' : 'free');
        setStatus('ready');
      })
      .catch(err => {
        const code = err?.response?.status;
        if (code === 401 || code === 403) {
          setStatusNote('API key not configured — using free tier.');
          setModelKey('free');
          setStatus('ready');
        } else {
          // 404 or network error: backend endpoint not yet wired; still let the
          // user attempt sends so they see the real error inline.
          setModelKey('free');
          setStatus('ready');
        }
      });
  }, []);

  // Scroll to newest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || sending) return;

    const userMsg: Msg = { role: 'user', content: text };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInput('');
    setSending(true);

    try {
      const res = await axios.post('/api/v1/claude/chat', {
        model: MODELS[modelKey].id,
        system: SYSTEM_PROMPT,
        messages: nextMessages.map(m => ({ role: m.role, content: m.content })),
      }, { timeout: 60000 });

      const reply: string = res.data?.content ?? res.data?.response ?? '(no response)';
      setMessages(prev => [...prev, { role: 'assistant', content: reply }]);
    } catch (err: any) {
      const detail = err?.response?.data?.detail ?? err?.message ?? 'Claude is unreachable.';
      setMessages(prev => [...prev, { role: 'assistant', content: `⚠️ ${detail}` }]);
    } finally {
      setSending(false);
    }
  }, [input, messages, modelKey, sending]);

  const clear = () => { setMessages([]); };

  const model = MODELS[modelKey];

  return (
    <div className="flex flex-col h-full min-h-0">

      {/* Toolbar */}
      <div className="shrink-0 px-3 py-2 border-b border-slate-800/50 space-y-1.5">
        {/* Model tiles */}
        <div className="flex gap-1.5">
          {(Object.entries(MODELS) as [ModelKey, typeof MODELS[ModelKey]][]).map(([key, m]) => (
            <button
              key={key}
              type="button"
              onClick={() => setModelKey(key)}
              className={`flex-1 flex flex-col items-start px-2.5 py-1.5 rounded-xl border transition-all ${
                modelKey === key
                  ? 'bg-aura/10 border-aura/40 text-aura'
                  : 'bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700 hover:text-slate-300'
              }`}
            >
              <span className="text-[9px] font-black uppercase tracking-widest">{m.label}</span>
              <span className="text-[8px] font-bold opacity-70">{m.note}</span>
            </button>
          ))}

          {messages.length > 0 && (
            <button
              type="button"
              onClick={clear}
              title="Clear conversation"
              aria-label="Clear conversation"
              className="p-2 rounded-xl border border-slate-800 bg-slate-900 text-slate-600 hover:text-vital hover:border-slate-700 transition-all"
            >
              <Trash2 size={12} />
            </button>
          )}
        </div>
      </div>

      {/* Status note */}
      {statusNote && (
        <div className="shrink-0 px-3 py-1.5 bg-amber-500/10 border-b border-amber-500/20">
          <p className="text-[8px] font-bold text-amber-400">{statusNote}</p>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-3 py-3 space-y-3">
        {messages.length === 0 && !sending && (
          <div className="space-y-2">
            <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-3">
              <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1">Claude · {model.label}</p>
              <p className="text-[10px] text-slate-400 leading-relaxed">
                Ask anything — code, analysis, strategy, or Workstation-specific context.
              </p>
            </div>
            {/* Starter prompts */}
            {[
              'What is the current system state?',
              'Help me debug this component',
              'Explain the cognition pipeline',
            ].map(prompt => (
              <button
                key={prompt}
                type="button"
                onClick={() => { setInput(prompt); }}
                className="w-full text-left px-3 py-2 rounded-xl border border-slate-800/60 bg-slate-900/40 text-[9px] text-slate-500 hover:text-slate-300 hover:border-slate-700 transition-colors font-bold"
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col gap-1 ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
            <span className="text-[7px] font-black uppercase tracking-widest text-slate-600 px-1">
              {m.role === 'user' ? 'You' : '⚡ Claude'}
            </span>
            <div className={`max-w-[95%] rounded-2xl px-3 py-2 text-[10px] leading-relaxed font-medium ${
              m.role === 'user'
                ? 'bg-aura/10 border border-aura/20 text-white rounded-tr-sm'
                : 'bg-slate-950 border border-slate-800 text-slate-300 rounded-tl-sm'
            }`}>
              {m.content}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex flex-col gap-1 items-start">
            <span className="text-[7px] font-black uppercase tracking-widest text-slate-600 px-1">⚡ Claude</span>
            <div className="bg-slate-950 border border-slate-800 rounded-2xl rounded-tl-sm px-3 py-2 flex items-center gap-2">
              <div className="flex gap-1">
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:0ms]" />
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:150ms]" />
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="shrink-0 border-t border-slate-800/60 bg-slate-950/40 px-3 py-2.5 flex gap-2 items-end">
        {status === 'checking' ? (
          <div className="flex items-center gap-2 text-[9px] text-slate-500 font-bold w-full py-1">
            <Loader2 size={10} className="animate-spin" /> Connecting to Claude…
          </div>
        ) : (
          <>
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
              }}
              placeholder="Message Claude… (Enter to send)"
              rows={2}
              className="flex-1 resize-none bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-[10px] text-white placeholder:text-slate-600 focus:outline-none focus:border-aura transition-colors leading-relaxed custom-scrollbar"
            />
            <button
              type="button"
              onClick={send}
              disabled={!input.trim() || sending}
              title="Send message"
              aria-label="Send message"
              className="p-2 rounded-xl bg-aura text-sovereign disabled:opacity-30 hover:opacity-90 transition-opacity shrink-0"
            >
              {sending ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
            </button>
          </>
        )}
      </div>
    </div>
  );
};
