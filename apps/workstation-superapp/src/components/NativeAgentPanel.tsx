/**
 * NativeAgentPanel — the in-app assistant, served by Workstation's OWN AI fabric.
 *
 * This replaces ClaudeAgentPanel, which POSTed to /api/v1/claude/chat. That route has never
 * existed, so every send in the Agents tab returned 404 and rendered "⚠️ Not Found" as if the
 * assistant had replied. The panel also advertised Anthropic model tiers ("Sonnet · paid",
 * "Haiku · free") — an external-gateway design that contradicts the native-AI mandate.
 *
 * What it does now:
 *   • GET  /api/v1/native-ai/models    — the OWNED tiers actually available on this host
 *                                        (auto · native floor · whichever local models exist).
 *   • POST /api/v1/native-ai/complete  — the in-house orchestrator.
 *
 * Honesty rules this panel follows:
 *   • It never claims a model it did not use. Every reply is stamped with the `served_by` the
 *     backend reports, so a deterministic-floor answer is visibly a floor answer.
 *   • It offers only tiers the backend says exist. If no local model is installed, the panel says
 *     so rather than presenting a menu that cannot be honoured.
 *   • Failures surface as failures via ApiError — never as an assistant message.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, Loader2, Trash2, AlertTriangle } from 'lucide-react';
import { apiJson, errorMessage } from '../lib/api';

interface Msg {
  role: 'user' | 'assistant';
  content: string;
  servedBy?: string;
  isExternal?: boolean;
}

interface Tier {
  id: string;
  label: string;
  kind: string;
}

const AGENT = 'workstation-assistant';

const SYSTEM_PREAMBLE =
  'You are the assistant embedded in Workstation, a sovereign intelligence platform. ' +
  'Be concise, precise and practical. If you do not know something about this deployment, say so ' +
  'rather than inventing it.';

/** The orchestrator takes a single prompt, so the running conversation is flattened into one. */
function buildPrompt(history: Msg[], next: string): string {
  const turns = history
    .map(m => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`)
    .join('\n\n');
  return `${SYSTEM_PREAMBLE}\n\n${turns ? turns + '\n\n' : ''}User: ${next}\n\nAssistant:`;
}

export const NativeAgentPanel: React.FC = () => {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [tiers, setTiers] = useState<Tier[]>([]);
  const [tier, setTier] = useState<string>('auto');
  const [loadingTiers, setLoadingTiers] = useState(true);
  const [notice, setNotice] = useState('');
  const [sendError, setSendError] = useState('');
  const bottomRef = useRef<HTMLDivElement>(null);

  // Ask the backend which owned resources actually exist here.
  useEffect(() => {
    let cancelled = false;
    apiJson<{ tiers?: Tier[]; local_models?: string[]; default_local?: string | null }>(
      '/api/v1/native-ai/models',
    )
      .then(data => {
        if (cancelled) return;
        setTiers(data.tiers ?? []);
        if (!data.local_models || data.local_models.length === 0) {
          setNotice('No local model is installed on this host — answers come from the deterministic native floor.');
        }
      })
      .catch(e => {
        if (!cancelled) setNotice(`Could not read the owned model list: ${errorMessage(e)}`);
      })
      .finally(() => {
        if (!cancelled) setLoadingTiers(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const send = useCallback(async () => {
    const text = input.trim();
    if (!text || sending) return;

    const history = messages;
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    setInput('');
    setSending(true);
    setSendError('');

    try {
      const res = await apiJson<{ output?: string; served_by?: string; is_external?: boolean }>(
        '/api/v1/native-ai/complete',
        {
          method: 'POST',
          body: { prompt: buildPrompt(history, text), agent: AGENT, model: tier, timeout: 120 },
        },
      );
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: res.output ?? '',
          servedBy: res.served_by,
          isExternal: res.is_external,
        },
      ]);
    } catch (e) {
      // A failed request is a failed request. It does not get rendered as an assistant turn.
      setSendError(errorMessage(e));
    } finally {
      setSending(false);
    }
  }, [input, messages, sending, tier]);

  const selectable = tiers.length > 0 ? tiers : [{ id: 'auto', label: 'Auto (in-house-first)', kind: 'policy' }];

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Owned-tier selector — only what the backend says exists */}
      <div className="shrink-0 px-3 py-2 border-b border-slate-800/50 space-y-1.5">
        <div className="flex gap-1.5 items-center">
          <select
            value={tier}
            onChange={e => setTier(e.target.value)}
            disabled={loadingTiers}
            aria-label="Owned model resource"
            className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-2.5 py-1.5 text-[9px] font-bold text-slate-300 focus:outline-none focus:border-aura transition-colors disabled:opacity-50"
          >
            {selectable.map(t => (
              <option key={t.id} value={t.id}>
                {t.label}
              </option>
            ))}
          </select>

          {messages.length > 0 && (
            <button
              type="button"
              onClick={() => {
                setMessages([]);
                setSendError('');
              }}
              title="Clear conversation"
              aria-label="Clear conversation"
              className="p-2 rounded-xl border border-slate-800 bg-slate-900 text-slate-600 hover:text-vital hover:border-slate-700 transition-all"
            >
              <Trash2 size={12} />
            </button>
          )}
        </div>
      </div>

      {notice && (
        <div className="shrink-0 px-3 py-1.5 bg-amber-500/10 border-b border-amber-500/20">
          <p className="text-[8px] font-bold text-amber-400">{notice}</p>
        </div>
      )}

      <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-3 py-3 space-y-3">
        {messages.length === 0 && !sending && (
          <div className="space-y-2">
            <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-3">
              <p className="text-[9px] font-black uppercase tracking-widest text-aura mb-1">In-house assistant</p>
              <p className="text-[10px] text-slate-400 leading-relaxed">
                Served by Workstation&apos;s own AI fabric. Every reply is stamped with the resource
                that actually produced it.
              </p>
            </div>
            {['What is the current system state?', 'Explain the cognition pipeline', 'Summarise the governance model'].map(
              prompt => (
                <button
                  key={prompt}
                  type="button"
                  onClick={() => setInput(prompt)}
                  className="w-full text-left px-3 py-2 rounded-xl border border-slate-800/60 bg-slate-900/40 text-[9px] text-slate-500 hover:text-slate-300 hover:border-slate-700 transition-colors font-bold"
                >
                  {prompt}
                </button>
              ),
            )}
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`flex flex-col gap-1 ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
            <span className="text-[7px] font-black uppercase tracking-widest text-slate-600 px-1">
              {m.role === 'user'
                ? 'You'
                : `served by ${m.servedBy ?? 'unknown'}${m.isExternal ? ' · external' : ''}`}
            </span>
            <div
              className={`max-w-[95%] rounded-2xl px-3 py-2 text-[10px] leading-relaxed font-medium whitespace-pre-wrap ${
                m.role === 'user'
                  ? 'bg-aura/10 border border-aura/20 text-white rounded-tr-sm'
                  : 'bg-slate-950 border border-slate-800 text-slate-300 rounded-tl-sm'
              }`}
            >
              {m.content}
            </div>
          </div>
        ))}

        {sending && (
          <div className="flex flex-col gap-1 items-start">
            <span className="text-[7px] font-black uppercase tracking-widest text-slate-600 px-1">thinking</span>
            <div className="bg-slate-950 border border-slate-800 rounded-2xl rounded-tl-sm px-3 py-2 flex items-center gap-2">
              <div className="flex gap-1">
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:0ms]" />
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:150ms]" />
                <span className="w-1 h-1 rounded-full bg-aura/60 animate-bounce [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}

        {sendError && (
          <div
            role="alert"
            className="flex items-start gap-2 rounded-xl border border-vital/30 bg-vital/10 px-3 py-2"
          >
            <AlertTriangle size={11} className="text-vital shrink-0 mt-0.5" />
            <p className="text-[9px] font-bold text-vital leading-relaxed">{sendError}</p>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="shrink-0 border-t border-slate-800/60 bg-slate-950/40 px-3 py-2.5 flex gap-2 items-end">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="Ask the in-house assistant… (Enter to send)"
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
      </div>
    </div>
  );
};
