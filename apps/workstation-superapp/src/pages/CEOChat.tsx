import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, ThumbsUp, ThumbsDown, MoreHorizontal, X, WifiOff, RefreshCw, ChevronLeft, FolderPlus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const CEOChat: React.FC = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Greeting, Guardian. I am the VSB AI CEO. Our collective resonance is reaching multi-dimensional thresholds.' }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [sentiment, setSentiment] = useState('analytical');
  const [showMenu, setShowMenu] = useState(false);
  const [feedback, setFeedback] = useState<Record<number, 'up' | 'down'>>({});
  const [aiStatus, setAiStatus] = useState<'online' | 'fallback' | 'offline'>('online');
  const scrollRef = useRef<HTMLDivElement>(null);

  const getAvatarColor = () => {
    switch (sentiment) {
      case 'joyful': return 'text-emerald-400';
      case 'frustrated': return 'text-vital';
      case 'curious': return 'text-highlight';
      default: return 'text-aura';
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isThinking]);

  const handleSend = async () => {
    if (!input.trim() || isThinking) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsThinking(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 35000);

      const response = await fetch('/api/v138/ceo/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, context: messages }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = { role: 'assistant', content: '' };

      if (input.toLowerCase().includes("great") || input.toLowerCase().includes("good")) setSentiment('joyful');
      else if (input.toLowerCase().includes("error") || input.toLowerCase().includes("fail")) setSentiment('frustrated');
      else if (input.toLowerCase().includes("how") || input.toLowerCase().includes("why")) setSentiment('curious');
      else setSentiment('analytical');

      setMessages(prev => [...prev, assistantMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        for (const line of chunk.split('\n')) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              assistantMessage.content += data.content;
              setMessages(prev => {
                const updated = [...prev];
                updated[updated.length - 1] = { ...assistantMessage };
                return updated;
              });
              if (data.done) break;
            } catch {
              // malformed SSE line — skip
            }
          }
        }
      }

      // Detect when backend fell back to simulation (Ollama was offline)
      if (assistantMessage.content.includes('(Ollama Offline)') || assistantMessage.content.includes('Simulated synthesis')) {
        setAiStatus('fallback');
      } else {
        setAiStatus('online');
      }
    } catch (error: any) {
      const isTimeout = error?.name === 'AbortError' || error?.message?.includes('timeout');
      setAiStatus('offline');
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: isTimeout
          ? "Request timed out — the AI engine is taking too long to respond. It may still be loading the model. Please try again in a moment."
          : "The AI backend is currently unreachable. Ensure the Workstation backend server is running, then retry.",
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleClearConversation = () => {
    setMessages([{ role: 'assistant', content: 'Greeting, Guardian. I am the VSB AI CEO. Our collective resonance is reaching multi-dimensional thresholds.' }]);
    setFeedback({});
    setShowMenu(false);
  };

  const handleExportTranscript = () => {
    const blob = new Blob([JSON.stringify(messages, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ceo-transcript-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setShowMenu(false);
  };

  const handleFeedback = (index: number, type: 'up' | 'down') => {
    setFeedback(prev => ({ ...prev, [index]: prev[index] === type ? undefined as any : type }));
  };

  return (
    <div className="flex flex-col h-[calc(100vh-14rem)] max-w-5xl mx-auto glass-card overflow-hidden">
      <header className="px-10 py-6 border-b border-white/5 flex justify-between items-center bg-surface/60 backdrop-blur-3xl">
        <div className="flex items-center gap-5">
          {/* Back / close */}
          <button
            type="button"
            onClick={() => navigate('/')}
            aria-label="Back to dashboard"
            title="Back to dashboard"
            className="p-2.5 bg-surface/80 border border-white/10 rounded-xl hover:border-aura/50 transition-colors text-slate-400 hover:text-aura shrink-0"
          >
            <ChevronLeft size={18} />
          </button>

          <div className={`p-1 rounded-2xl transition-all duration-700 relative group bg-aura/20 shadow-[0_0_20px_rgba(100,255,218,0.2)] overflow-hidden`}>
            <div className="w-14 h-14 bg-slate-950 rounded-xl flex items-center justify-center relative">
               <Bot size={28} className={`${getAvatarColor()} relative z-10 transition-colors duration-500`} />
               <motion.div
                 animate={{ scale: [1, 1.2, 1], opacity: [0.2, 0.4, 0.2] }}
                 transition={{ duration: 4, repeat: Infinity }}
                 className="absolute inset-0 bg-aura rounded-full blur-xl"
               ></motion.div>
            </div>
          </div>
          <div>
            <h2 className="text-xl font-black tracking-tight uppercase">VSB AI CEO</h2>
            <div className="flex items-center gap-2 mt-1">
              {aiStatus === 'online' && (
                <><span className="w-2 h-2 rounded-full bg-aura animate-pulse" /><span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Planetary Strategy Active</span></>
              )}
              {aiStatus === 'fallback' && (
                <><WifiOff size={11} className="text-amber-500" /><span className="text-[10px] font-black text-amber-500 uppercase tracking-widest">Fallback Mode — Ollama Offline</span></>
              )}
              {aiStatus === 'offline' && (
                <><WifiOff size={11} className="text-vital" /><span className="text-[10px] font-black text-vital uppercase tracking-widest">AI Offline</span></>
              )}
            </div>
          </div>
        </div>

        <div className="flex gap-2 relative items-center">
          {/* Create Project CTA appears after first CEO exchange */}
          {messages.length > 1 && (
            <button
              type="button"
              onClick={() => navigate('/projects?realm=enterprise&domain=saas&new=1')}
              title="Create a project from this discussion"
              aria-label="Create project"
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border border-aura/40 text-aura hover:bg-aura/10 transition-colors"
            >
              <FolderPlus size={12} /> New Project
            </button>
          )}
          {aiStatus !== 'online' && (
            <button
              type="button"
              onClick={async () => {
                    // Ledger cluster 3 — this used to just flip the pill to 'online', showing a dead
                    // backend as healthy. It now performs a REAL health check.
                    setAiStatus('offline');   // neutral while the check runs
                    try {
                      const r = await fetch('/api/v1/native-ai/status');
                      setAiStatus(r.ok ? 'online' : 'offline');
                    } catch { setAiStatus('offline'); }
                  }}
              title="Retry connection"
              aria-label="Retry connection"
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border border-amber-500/30 text-amber-500 hover:bg-amber-500/10 transition-colors"
            >
              <RefreshCw size={12} /> Retry
            </button>
          )}
          <button
            type="button"
            aria-label="More options"
            title="More options"
            onClick={() => setShowMenu(prev => !prev)}
            className="p-3 bg-surface/80 border border-white/10 rounded-xl hover:border-aura/50 transition-colors text-slate-400 hover:text-aura"
          >
             <MoreHorizontal size={18} />
          </button>
          <button
            type="button"
            aria-label="Close CEO chat"
            title="Close"
            onClick={() => navigate('/')}
            className="p-3 bg-surface/80 border border-white/10 rounded-xl hover:border-vital/50 transition-colors text-slate-400 hover:text-vital"
          >
            <X size={18} />
          </button>
          {showMenu && (
            <div className="absolute right-0 top-full mt-2 w-56 bg-surface border border-white/10 rounded-xl shadow-2xl overflow-hidden z-20">
              <button
                type="button"
                onClick={handleExportTranscript}
                className="w-full text-left px-5 py-3 text-xs font-bold text-slate-300 hover:bg-white/5 hover:text-aura transition-colors"
              >
                Export Transcript
              </button>
              <button
                type="button"
                onClick={handleClearConversation}
                className="w-full text-left px-5 py-3 text-xs font-bold text-slate-300 hover:bg-white/5 hover:text-vital transition-colors"
              >
                Clear Conversation
              </button>
            </div>
          )}
        </div>
      </header>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-10 space-y-8 custom-scrollbar">
        <AnimatePresence initial={false}>
          {messages.map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-6 max-w-[80%] ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-lg ${
                  m.role === 'user' ? 'bg-highlight/20 text-highlight' : 'bg-surface border border-white/5 text-aura'
                }`}>
                  {m.role === 'user' ? <User size={24} /> : <Bot size={24} />}
                </div>
                <div className="space-y-3">
                   <div className={`p-6 rounded-[2rem] text-sm font-bold leading-relaxed shadow-xl ${
                     m.role === 'user'
                       ? 'bg-highlight/10 border border-highlight/20 text-white rounded-tr-none'
                       : 'bg-surface/80 border border-white/10 text-slate-200 rounded-tl-none'
                   }`}>
                     {m.content}
                   </div>
                   {m.role === 'assistant' && (
                     <div className="flex gap-3 ml-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          type="button"
                          aria-label="Helpful"
                          title="Helpful"
                          onClick={() => handleFeedback(i, 'up')}
                          className={`p-2 transition-colors ${feedback[i] === 'up' ? 'text-aura' : 'hover:text-aura'}`}
                        ><ThumbsUp size={14} fill={feedback[i] === 'up' ? 'currentColor' : 'none'} /></button>
                        <button
                          type="button"
                          aria-label="Not helpful"
                          title="Not helpful"
                          onClick={() => handleFeedback(i, 'down')}
                          className={`p-2 transition-colors ${feedback[i] === 'down' ? 'text-vital' : 'hover:text-vital'}`}
                        ><ThumbsDown size={14} fill={feedback[i] === 'down' ? 'currentColor' : 'none'} /></button>
                     </div>
                   )}
                </div>
              </div>
            </motion.div>
          ))}
          {isThinking && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
               <div className="flex gap-4 items-center p-6 bg-aura/5 border border-aura/10 rounded-[2rem] rounded-tl-none">
                  <div className="flex gap-1">
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce"></div>
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce [animation-delay:0.2s]"></div>
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                  <span className="text-[10px] font-black text-aura uppercase tracking-widest">Synthesis in progress...</span>
               </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="p-8 bg-surface/60 border-t border-white/5 backdrop-blur-3xl">
        <div className="relative max-w-4xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Issue a planetary directive..."
            className="w-full bg-sovereign/80 border border-white/10 rounded-[2rem] py-6 pl-8 pr-20 text-lg focus:outline-none focus:border-aura/50 transition-all shadow-2xl font-bold"
          />
          <button
            type="button"
            onClick={handleSend}
            disabled={isThinking}
            aria-label="Send message"
            title="Send message"
            className="absolute right-3 top-1/2 -translate-y-1/2 p-4 bg-aura text-sovereign rounded-2xl hover:scale-105 transition-all shadow-lg"
          >
            <Send size={22} />
          </button>
        </div>
      </div>
    </div>
  );
};
