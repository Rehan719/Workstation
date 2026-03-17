import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Sparkles } from 'lucide-react';

export const CEOChat: React.FC = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Greeting, Guardian. I am the VSB AI CEO. How shall we direct the evolution of the workstation today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');

    // Simulate response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `I have analyzed your request regarding "${input}". Aligning C-Suite resources for synthesis...`
      }]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] max-w-4xl mx-auto bg-slate-900/40 border border-slate-800 rounded-3xl overflow-hidden backdrop-blur-md">
      <header className="px-8 py-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/60">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-aura/20 rounded-2xl text-aura">
            <Bot size={24} />
          </div>
          <div>
            <h2 className="text-xl font-bold">VSB AI CEO</h2>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-vital animate-pulse"></span>
              <span className="text-[10px] font-black text-slate-500 uppercase">Strategic Mode Active</span>
            </div>
          </div>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-slate-800 rounded-xl text-xs font-bold hover:bg-slate-700 transition-colors">
          <Sparkles size={14} className="text-highlight" />
          Strategic Report
        </button>
      </header>

      <div className="flex-1 overflow-y-auto p-8 space-y-6 scroll-smooth">
        <AnimatePresence>
          {messages.map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex gap-4 max-w-[80%] ${m.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                  m.role === 'user' ? 'bg-highlight/20 text-highlight' : 'bg-aura/20 text-aura'
                }`}>
                  {m.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className={`p-4 rounded-2xl text-sm leading-relaxed ${
                  m.role === 'user' ? 'bg-highlight/10 border border-highlight/20' : 'bg-slate-800/50 border border-slate-700'
                }`}>
                  {m.content}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div className="p-6 bg-slate-900/60 border-t border-slate-800">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Issue a command or ask for strategic guidance..."
            className="w-full bg-sovereign border border-slate-700 rounded-2xl py-4 pl-6 pr-16 text-sm focus:outline-none focus:border-aura transition-all"
          />
          <button
            onClick={handleSend}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-3 bg-aura text-sovereign rounded-xl hover:scale-105 transition-transform"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};
