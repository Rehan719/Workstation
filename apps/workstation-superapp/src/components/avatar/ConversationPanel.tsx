import React, { useEffect, useRef } from 'react';
import { ArrowUp, ImagePlus, Loader2, Trash2 } from 'lucide-react';
import type { UseAvatarSessionReturn } from '../../hooks/useAvatarSession';

interface ConversationPanelProps {
  avatar: UseAvatarSessionReturn;
}

// Minimal, dependency-free "rich text" renderer: supports **bold**, `inline
// code`, and "- " bullet lines. Real formatting (not literal markdown syntax
// left in raw text) without pulling in a markdown library.
function renderRichText(text: string): React.ReactNode {
  return text.split('\n').map((line, li) => {
    const trimmed = line.trimStart();
    const isBullet = trimmed.startsWith('- ');
    const content = isBullet ? trimmed.slice(2) : line;
    const parts = content.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).filter(Boolean);
    const rendered = parts.map((part, pi) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={pi} className="font-bold text-white">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return <code key={pi} className="px-1 py-0.5 rounded bg-black/30 text-aura font-mono text-[11px]">{part.slice(1, -1)}</code>;
      }
      return <React.Fragment key={pi}>{part}</React.Fragment>;
    });
    return (
      <div key={li} className={isBullet ? 'flex gap-2 pl-1' : ''}>
        {isBullet && <span className="text-aura">•</span>}
        <span>{rendered}</span>
      </div>
    );
  });
}

/**
 * Footer-center conversation panel — the real, scrollable, rich-text user
 * <-> avatar history (replaces the old fake "Sovereign Mesh" canned-reply
 * chat), with an input row that fills the remaining width. Fed by the same
 * shared `avatar` session as the VoiceVisualizer and AvatarWidget.
 */
export const ConversationPanel: React.FC<ConversationPanelProps> = ({ avatar }) => {
  const {
    messages, input, setInput, sending, notice, context,
    sendMessage, clearConversation, pendingImage, setPendingImage, handleImageFile,
  } = avatar;

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  };

  const handleSend = () => {
    if (!input.trim() && !pendingImage) return;
    sendMessage();
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleImagePick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    handleImageFile(file);
    e.target.value = '';
  };

  return (
    <div className="h-full w-full flex flex-col min-h-0 min-w-0">
      <div className="flex-1 overflow-y-auto custom-scrollbar min-h-0 space-y-3 pr-1">
        {messages.length > 0 && messages.map((m, i) => (
            <div key={i} className={`flex flex-col gap-1 ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
              <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 px-1">
                {m.role === 'user' ? 'You' : 'Avatar'}
              </span>
              <div className={`max-w-[92%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed font-medium space-y-1 ${
                m.role === 'user' ? 'bg-aura/10 border border-aura/20 text-white rounded-tr-sm' : 'bg-slate-950 border border-slate-800 text-slate-300 rounded-tl-sm'
              }`}>
                {m.imageDataUrl && <img src={m.imageDataUrl} alt="Attached" className="rounded-lg mb-2 max-h-32 object-cover" />}
                {renderRichText(m.content)}
              </div>
            </div>
          ))
        }
        {sending && (
          <div className="flex items-center gap-2 text-[10px] text-slate-500 font-bold px-1">
            <Loader2 size={12} className="animate-spin" /> Thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {notice && (
        <div className="shrink-0 mt-2 px-3 py-2 text-[10px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-xl">
          {notice}
        </div>
      )}

      {pendingImage && (
        <div className="shrink-0 mt-2 flex items-center gap-2">
          <img src={pendingImage} alt="Pending attachment" className="h-9 w-9 rounded-lg object-cover border border-aura/30" />
          <button type="button" onClick={() => setPendingImage(null)} className="text-[9px] font-black uppercase text-slate-500 hover:text-red-400">Remove</button>
        </div>
      )}

      <div className="shrink-0 mt-2 flex items-end gap-2">
        <div className="flex-1 flex items-end gap-2 bg-slate-900/90 border rounded-3xl px-4 py-2.5 shadow-2xl backdrop-blur-md transition-all duration-200 border-slate-700/40 focus-within:border-aura/40 min-w-0">
          <input ref={fileInputRef} type="file" accept="image/*" className="hidden" aria-label="Attach image" onChange={handleImagePick} />
          <button type="button" onClick={() => fileInputRef.current?.click()} aria-label="Attach image" title="Attach image" className="shrink-0 p-1.5 rounded-xl text-slate-500 hover:text-aura transition-colors">
            <ImagePlus size={15} />
          </button>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => { setInput(e.target.value); autoResize(); }}
            placeholder="Message the avatar…"
            rows={1}
            className="flex-1 min-w-0 bg-transparent text-sm text-white placeholder-slate-600 resize-none focus:outline-none leading-relaxed font-medium min-h-6 max-h-40"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
        </div>
        <button
          type="button"
          onClick={handleSend}
          disabled={(!input.trim() && !pendingImage) || sending}
          aria-label="Send message to avatar"
          title="Send message to avatar"
          className={`flex-shrink-0 w-9 h-9 rounded-2xl flex items-center justify-center transition-all duration-150 ${(input.trim() || pendingImage) && !sending ? 'bg-aura text-sovereign shadow-lg shadow-aura/20 hover:scale-110 active:scale-95' : 'bg-slate-800 text-slate-600 cursor-not-allowed'}`}
        >
          <ArrowUp size={15} />
        </button>
        {messages.length > 0 && (
          <button type="button" onClick={clearConversation} aria-label="Clear chat history" title="Clear chat history" className="flex-shrink-0 w-9 h-9 rounded-2xl flex items-center justify-center bg-slate-800 text-slate-600 hover:text-red-400 hover:bg-red-500/10 transition-all">
            <Trash2 size={14} />
          </button>
        )}
      </div>

      {messages.length === 0 && (
        <p className="shrink-0 mt-1.5 text-[10px] text-slate-600 font-bold leading-relaxed">
          Ask anything — text, voice, or attach an image. Responses are tailored to the{' '}
          <span className="text-aura/70">{context}</span> context you're currently in.
        </p>
      )}
    </div>
  );
};
