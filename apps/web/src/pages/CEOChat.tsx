import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Sparkles, ThumbsUp, ThumbsDown, MoreHorizontal, X } from 'lucide-react';

export const CEOChat: React.FC = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Greeting, Guardian. I am the VSB AI CEO. Our collective resonance is reaching multi-dimensional thresholds.' }
  ]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [sentiment, setSentiment] = useState('analytical');
  const scrollRef = useRef<HTMLDivElement>(null);

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
      const response = await fetch(`/api/v260/civilization/assistant/query?query=${encodeURIComponent(input)}`, {
        method: 'POST'
      });
      const data = await response.json();

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response || "Synthesis complete. Alignment maintained."
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I am currently out of resonance. Please verify local Ollama connectivity."
      }]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-14rem)] max-w-5xl mx-auto glass-card overflow-hidden">
      <header className="px-10 py-8 border-b border-white/5 flex justify-between items-center bg-surface/60 backdrop-blur-3xl">
        <div className="flex items-center gap-5">
          <div className={`p-4 rounded-2xl transition-all duration-700 relative group ${
            sentiment === 'excited' ? 'bg-highlight/20 text-highlight shadow-[0_0_30px_rgba(255,215,64,0.4)]' :
            sentiment === 'proud' ? 'bg-aura/30 text-white shadow-[0_0_40px_rgba(100,255,218,0.6)]' :
            'bg-aura/20 text-aura shadow-[0_0_20px_rgba(100,255,218,0.2)]'
          }`}>
            <Bot size={28} />
            <div className={`absolute -inset-1 rounded-full border-2 animate-pulse opacity-0 group-hover:opacity-100 transition-opacity ${
               sentiment === 'excited' ? 'border-highlight' : 'border-aura'
            }`}></div>
          </div>
          <div>
            <h2 className="text-2xl font-black tracking-tight uppercase">VSB AI CEO</h2>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 rounded-full bg-aura animate-pulse"></span>
              <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Planetary Strategy Active</span>
            </div>
          </div>
        </div>
        <div className="flex gap-3">
          <button className="p-3 bg-surface/80 border border-white/10 rounded-xl hover:border-aura/50 transition-colors text-slate-400 hover:text-aura">
             <MoreHorizontal size={20} />
          </button>
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
                        <button className="p-2 hover:text-aura transition-colors"><ThumbsUp size={14} /></button>
                        <button className="p-2 hover:text-vital transition-colors"><ThumbsDown size={14} /></button>
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
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce" style={{ animationDelay: '0s' }}></div>
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                     <div className="w-1.5 h-1.5 bg-aura rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
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
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Issue a planetary directive..."
            className="w-full bg-sovereign/80 border border-white/10 rounded-[2rem] py-6 pl-8 pr-20 text-lg focus:outline-none focus:border-aura/50 transition-all shadow-2xl font-bold"
          />
          <button
            onClick={handleSend}
            disabled={isThinking}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-4 bg-aura text-sovereign rounded-2xl hover:scale-105 transition-all shadow-lg"
          >
            <Send size={22} />
          </button>
        </div>
      </div>
    </div>
  );
};
