import React, { useState, useRef, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CommandCenter } from '@workstation/ui';
import { useStore } from '@workstation/shared';
import { useResilientWebSocket } from '../../hooks/useResilientWebSocket';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { ArrowUp, Zap, Radio, Sparkles } from 'lucide-react';

interface ShellProps {
  children: (activeTab: string) => React.ReactNode;
}

interface MeshMessage {
  role: 'user' | 'mesh';
  text: string;
  ts: number;
}

const MESH_REPLIES = [
  'Constitutional alignment verified across all 1127 articles. Processing your query via L12 Multi-Modal Fabric…',
  'Sovereign Mesh engaged. Cross-referencing 50+ nodes for optimal synthesis. Response calibrated.',
  'GaaS enforcement active. Query routed through PQC-encrypted channels. Synthesizing output now.',
  'Introspection layer consulted. Recursive optimization complete. Here is your synthesized response.',
  'Federation handshake confirmed. Multi-domain context loaded. Mesh AI is now composing.',
];

export const Shell: React.FC<ShellProps> = ({ children }) => {
  const activeTab = useStore(state => state.currentTab);
  const setActiveTab = useStore(state => state.setCurrentTab);
  const [commandOpen, setCommandOpen] = useState(false);
  const { updateSystemVitals } = useStore();

  const [meshInput, setMeshInput] = useState('');
  const [meshMessages, setMeshMessages] = useState<MeshMessage[]>([]);
  const [meshThinking, setMeshThinking] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { status: wsStatus } = useResilientWebSocket('ws://localhost:8000/api/v154/ws/streams', (data) => {
    if (data.type === 'SYSTEM_VITALS') {
      updateSystemVitals(data.payload);
    }
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [meshMessages, meshThinking]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  };

  const handleSend = () => {
    const text = meshInput.trim();
    if (!text || meshThinking) return;

    const userMsg: MeshMessage = { role: 'user', text, ts: Date.now() };
    setMeshMessages(prev => [...prev, userMsg]);
    setMeshInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    setMeshThinking(true);

    setTimeout(() => {
      const reply = MESH_REPLIES[Math.floor(Date.now() / 1000) % MESH_REPLIES.length];
      setMeshMessages(prev => [...prev, { role: 'mesh', text: reply, ts: Date.now() }]);
      setMeshThinking(false);
    }, 1200);
  };

  return (
    <div className="font-inter flex h-screen flex-col overflow-hidden bg-sovereign text-white">
      <CommandPalette
        open={commandOpen}
        setOpen={setCommandOpen}
        setActiveTab={setActiveTab}
      />

      <CommandCenter />

      <Header wsStatus={wsStatus} />

      <div className="flex min-h-0 flex-1 overflow-hidden">
        <PanelGroup direction="horizontal">
          <Panel defaultSize={20} minSize={15} collapsible className="flex">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
          </Panel>

          <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

          <Panel defaultSize={80} minSize={30}>
            <PanelGroup direction="horizontal">

              {/* Center panel: page content + pinned chat input */}
              <Panel defaultSize={60} minSize={30}>
                <div className="flex flex-col h-full">
                  <main className="custom-scrollbar relative flex-1 overflow-y-auto p-8">
                    <div className="mx-auto max-w-full">
                      {children(activeTab)}
                    </div>
                  </main>

                  {/* Claude-style chat input */}
                  <div className="px-6 pb-5 pt-3 border-t border-slate-800/60 bg-sovereign/60 backdrop-blur-sm shrink-0">
                    <div className="max-w-3xl mx-auto">
                      <div className={`flex items-end gap-3 bg-slate-900/90 border rounded-3xl px-5 py-3.5 shadow-2xl backdrop-blur-md transition-all duration-200 ${meshInput ? 'border-aura/40 shadow-aura/5' : 'border-slate-700/40'}`}>
                        <div className="flex-shrink-0 mb-0.5">
                          <Zap size={14} className={`transition-colors ${meshInput ? 'text-aura' : 'text-slate-700'}`} />
                        </div>
                        <textarea
                          ref={textareaRef}
                          value={meshInput}
                          onChange={(e) => { setMeshInput(e.target.value); autoResize(); }}
                          placeholder="Ask the Sovereign Mesh anything…"
                          rows={1}
                          className="flex-1 bg-transparent text-sm text-white placeholder-slate-600 resize-none focus:outline-none leading-relaxed font-medium min-h-6 max-h-40"
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                              e.preventDefault();
                              handleSend();
                            }
                          }}
                        />
                        <button
                          type="button"
                          onClick={handleSend}
                          disabled={!meshInput.trim() || meshThinking}
                          aria-label="Send message"
                          className={`flex-shrink-0 w-8 h-8 rounded-2xl flex items-center justify-center transition-all duration-150 mb-0.5 ${meshInput.trim() && !meshThinking ? 'bg-aura text-sovereign shadow-lg shadow-aura/20 hover:scale-110 active:scale-95' : 'bg-slate-800 text-slate-600 cursor-not-allowed'}`}
                        >
                          <ArrowUp size={15} />
                        </button>
                      </div>
                      <p className="text-center text-[9px] font-black text-slate-700 uppercase tracking-widest mt-2 select-none">
                        ⌘K Commands · Shift+Enter New Line · L12 Multi-Modal Fabric Active
                      </p>
                    </div>
                  </div>
                </div>
              </Panel>

              <PanelResizeHandle className="w-1 cursor-col-resize bg-slate-900 transition-colors hover:bg-aura/30" />

              {/* Right panel: Sovereign Output / conversation thread */}
              <Panel defaultSize={40} minSize={15} collapsible>
                <aside className="flex flex-col h-full border-l border-slate-800 bg-slate-900/30">
                  <div className="shrink-0 px-8 pt-8 pb-4 flex items-center justify-between">
                    <h3 className="text-xs font-black uppercase tracking-widest text-aura">Sovereign Output</h3>
                    {meshMessages.length > 0 && (
                      <button
                        type="button"
                        onClick={() => setMeshMessages([])}
                        className="text-[9px] font-black uppercase tracking-widest text-slate-600 hover:text-slate-400 transition-colors"
                      >
                        Clear
                      </button>
                    )}
                  </div>

                  {meshMessages.length === 0 && !meshThinking ? (
                    <div className="flex-1 overflow-y-auto px-8 pb-8 space-y-6">
                      <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                        <p className="mb-2 text-[10px] font-bold uppercase text-slate-500">Simulation Engine</p>
                        <p className="text-xs italic text-slate-300">Ready for multi-modal synthesis.</p>
                      </div>
                      <div className="rounded-2xl border border-slate-800/50 bg-slate-950/40 p-4 space-y-3">
                        <p className="text-[10px] font-black uppercase tracking-widest text-slate-600">Mesh AI</p>
                        <p className="text-xs text-slate-500 leading-relaxed">
                          Type a query in the center input to engage the Sovereign Mesh. Responses appear here.
                        </p>
                        <div className="flex items-center gap-2 pt-1">
                          <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                          <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">L12 Fabric standby</span>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="flex-1 overflow-y-auto custom-scrollbar px-6 pb-6 space-y-4">
                      {meshMessages.map((msg, i) => (
                        <div key={i} className={`flex flex-col gap-1 ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                          <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 px-2">
                            {msg.role === 'user' ? 'You' : '⚡ Mesh AI'}
                          </span>
                          <div className={`max-w-[90%] rounded-2xl px-4 py-3 text-xs leading-relaxed font-medium ${
                            msg.role === 'user'
                              ? 'bg-aura/10 border border-aura/20 text-white rounded-tr-sm'
                              : 'bg-slate-950 border border-slate-800 text-slate-300 rounded-tl-sm'
                          }`}>
                            {msg.text}
                          </div>
                        </div>
                      ))}

                      {meshThinking && (
                        <div className="flex flex-col gap-1 items-start">
                          <span className="text-[8px] font-black uppercase tracking-widest text-slate-600 px-2">⚡ Mesh AI</span>
                          <div className="bg-slate-950 border border-slate-800 rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-2">
                            <div className="flex gap-1">
                              <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:0ms]" />
                              <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:150ms]" />
                              <span className="w-1.5 h-1.5 rounded-full bg-aura/60 animate-bounce [animation-delay:300ms]" />
                            </div>
                            <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">Synthesizing…</span>
                          </div>
                        </div>
                      )}

                      <div ref={messagesEndRef} />
                    </div>
                  )}
                </aside>
              </Panel>

            </PanelGroup>
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
};
