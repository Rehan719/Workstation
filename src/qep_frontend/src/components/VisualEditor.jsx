import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MousePointer2, Code, Eye, RefreshCw, Layers, Save, Share2, Rocket } from 'lucide-react';

const VisualEditor = () => {
  const [mode, setMode] = useState('preview'); // preview, select, code
  const [selectedElement, setSelectedElement] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [prompt, setPrompt] = useState('Dhikr Counter');

  const elements = [
    { id: 'h1', type: 'H', content: 'Welcome to your App' },
    { id: 't1', type: 'T', content: 'Generated from: ' + prompt },
    { id: 'b1', type: 'B', content: 'Click Me' }
  ];

  const handleGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => setIsGenerating(false), 2000);
  };

  return (
    <div className="bg-white/90 backdrop-blur-2xl rounded-3xl border border-white shadow-2xl overflow-hidden flex flex-col h-[800px]">
      <div className="bg-slate-900 text-white p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="flex bg-white/10 p-1 rounded-lg">
            <button
              onClick={() => setMode('preview')}
              className={`p-2 rounded-md transition-all ${mode === 'preview' ? 'bg-amber-500 text-slate-900' : 'hover:bg-white/5'}`}
            >
              <Eye size={16} />
            </button>
            <button
              onClick={() => setMode('select')}
              className={`p-2 rounded-md transition-all ${mode === 'select' ? 'bg-amber-500 text-slate-900' : 'hover:bg-white/5'}`}
            >
              <MousePointer2 size={16} />
            </button>
            <button
              onClick={() => setMode('code')}
              className={`p-2 rounded-md transition-all ${mode === 'code' ? 'bg-amber-500 text-slate-900' : 'hover:bg-white/5'}`}
            >
              <Code size={16} />
            </button>
          </div>
          <div className="h-6 w-px bg-white/20"></div>
          <div className="flex gap-2 text-[10px] font-black uppercase tracking-widest text-white/40">
            <span className={isGenerating ? "text-amber-500 animate-pulse" : ""}>GitHub Sync: Active</span>
          </div>
        </div>

        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold transition-all">
            <Save size={14} />
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold transition-all">
            <Share2 size={14} />
          </button>
          <button className="flex items-center gap-2 px-6 py-2 bg-amber-500 text-slate-900 rounded-lg text-xs font-black shadow-lg shadow-amber-500/20 hover:bg-amber-400">
            <Rocket size={14} />
            Instant Publish
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 bg-slate-50 relative p-12 overflow-y-auto">
          {mode === 'code' ? (
            <div className="font-mono text-sm bg-slate-900 text-emerald-400 p-8 rounded-xl h-full overflow-auto">
              <pre>{`// Generated Code for ${prompt}\n\nimport React from 'react';\n\nexport default function App() {\n  return (\n    <div className="p-8">\n      <h1 className="text-3xl font-bold">Welcome</h1>\n      <p>Content goes here...</p>\n    </div>\n  );\n}`}</pre>
            </div>
          ) : (
            <div className="max-w-2xl mx-auto space-y-8 bg-white p-12 rounded-2xl shadow-sm border border-slate-200 min-h-full relative">
              <div className="absolute top-4 left-4 text-[8px] font-black uppercase opacity-20">WYSIWYG MODE</div>

              {elements.map(el => (
                <div
                  key={el.id}
                  onClick={() => mode === 'select' && setSelectedElement(el.id)}
                  className={`relative p-4 transition-all ${
                    mode === 'select' ? 'hover:outline hover:outline-2 hover:outline-amber-500 cursor-pointer' : ''
                  } ${selectedElement === el.id ? 'outline outline-2 outline-amber-500 bg-amber-50' : ''}`}
                >
                   {mode === 'select' && (
                     <div className="absolute -top-3 -left-3 bg-amber-500 text-white text-[8px] px-1 rounded font-black">{el.type}</div>
                   )}
                   {el.type === 'H' && <h1 className="text-4xl font-black text-slate-900">{el.content}</h1>}
                   {el.type === 'T' && <p className="text-slate-600 leading-relaxed">{el.content}</p>}
                   {el.type === 'B' && <button className="px-8 py-3 bg-slate-900 text-white font-bold rounded-xl">{el.content}</button>}
                </div>
              ))}

              <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 flex flex-col items-center justify-center text-slate-400 gap-2 hover:border-amber-500 hover:text-amber-500 transition-all cursor-pointer">
                <Layers size={24} />
                <span className="text-[10px] font-black uppercase">+ Drag Component from Palette</span>
              </div>
            </div>
          )}
        </div>

        <div className="w-80 border-l border-slate-200 bg-white p-8 space-y-8 overflow-y-auto">
          <div>
             <h4 className="text-[10px] font-black uppercase text-slate-400 mb-6">Prompt-to-App AI Architect</h4>
             <div className="space-y-4">
                <input
                  type="text"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-amber-500"
                  placeholder="Describe your app..."
                />
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating}
                  className="w-full py-4 bg-slate-900 text-white font-black rounded-xl text-xs flex items-center justify-center gap-2 hover:bg-slate-800 disabled:opacity-50"
                >
                  {isGenerating ? <RefreshCw className="animate-spin" size={14} /> : "Generate App"}
                </button>
                <div className="text-[9px] text-center text-slate-400 italic font-medium">
                  Target Generation Time: <span className="text-amber-600 font-bold">{"<30 Seconds"}</span> | Article 145 Compliant
                </div>
             </div>
          </div>

          <div className="pt-8 border-t border-slate-100">
            <h4 className="text-[10px] font-black uppercase text-slate-400 mb-6">Component Properties</h4>
            {selectedElement ? (
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-slate-500 uppercase">Text Content</label>
                  <input type="text" className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs" defaultValue="Welcome" />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-slate-500 uppercase">Visual Style</label>
                  <select className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs">
                    <option>Bold / Hero</option>
                    <option>Subtle / Body</option>
                  </select>
                </div>
              </div>
            ) : (
              <div className="text-xs text-slate-400 italic">Select an element to edit properties</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualEditor;
