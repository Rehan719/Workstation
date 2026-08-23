import React, { useState } from 'react';
import { WORKSPACE_DOMAINS } from '../../lib/taxonomy';
import { useSearchParams } from 'react-router-dom';
import { Card, Badge } from '@workstation/ui';
import { Wand2, Play, Download, Copy, Check, Loader2, Code2, Braces, Settings, FileText, Boxes, Cpu } from 'lucide-react';

const ARTEFACT_TYPES = [
  { id: 'code',       label: 'Code',        icon: Code2,    fmt: 'python'   },
  { id: 'schema',     label: 'Data Schema', icon: Braces,   fmt: 'json'     },
  { id: 'config',     label: 'Config',      icon: Settings,  fmt: 'yaml'     },
  { id: 'content',    label: 'Content',     icon: FileText,  fmt: 'markdown' },
  { id: 'model_spec', label: 'Model Spec',  icon: Boxes,     fmt: 'markdown' },
] as const;

const FORMATS = ['python', 'typescript', 'json', 'yaml', 'markdown', 'sql', 'html', 'toml'];
const DOMAINS = WORKSPACE_DOMAINS;   // §17.1 (W321) — one shared workspace list
// §6 user design control — which owned tier serves
const MODELS = [
  { id: 'auto',   label: 'Auto (in-house first)' },
  { id: 'native', label: 'Native floor' },
  { id: 'local',  label: 'Local model (Ollama)' },
];

interface Result {
  artefact_type: string;
  format: string;
  output: string;
  served_by: string;
  is_external: boolean;
  run_id: string;
}

export const Generator: React.FC = () => {
  const [searchParams] = useSearchParams();
  const urlType = searchParams.get('type') ?? 'content';

  const [artefactType, setArtefactType] = useState(
    ARTEFACT_TYPES.some(t => t.id === urlType) ? urlType : 'content'
  );
  const [format, setFormat] = useState<string>(
    ARTEFACT_TYPES.find(t => t.id === (ARTEFACT_TYPES.some(x => x.id === urlType) ? urlType : 'content'))?.fmt ?? 'markdown'
  );
  const [domain, setDomain] = useState('general');
  const [model, setModel] = useState('auto');
  const [spec, setSpec] = useState('');
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const pickType = (id: string) => {
    setArtefactType(id);
    const t = ARTEFACT_TYPES.find(x => x.id === id);
    if (t) setFormat(t.fmt);
  };

  const handleRun = async () => {
    if (!spec.trim() || running) return;
    setRunning(true); setError(''); setResult(null);
    try {
      const res = await fetch('/api/v1/generator/produce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artefact_type: artefactType, spec, domain, format, model }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setResult(await res.json());
    } catch (err: any) {
      setError(err.message ?? 'Generation failed');
    } finally {
      setRunning(false);
    }
  };

  const handleCopy = async () => {
    if (!result?.output) return;
    await navigator.clipboard.writeText(result.output);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleExport = () => {
    if (!result) return;
    const ext = ({ python: 'py', typescript: 'ts', json: 'json', yaml: 'yaml', markdown: 'md', sql: 'sql', html: 'html', toml: 'toml' } as Record<string, string>)[result.format] ?? 'txt';
    const blob = new Blob([result.output], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `generated-${result.artefact_type}-${result.run_id || Date.now()}.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // owned-resource provenance label
  const provenance = result
    ? (result.is_external ? `External · ${result.served_by}`
       : result.served_by === 'native' ? 'Native floor (in-house)'
       : `Local model · ${result.served_by}`)
    : '';

  return (
    <div className="space-y-8 pb-24">
      <header>
        <h1 className="text-2xl @[480px]:text-3xl @[680px]:text-4xl font-black text-white uppercase tracking-tighter italic break-words">The Generator</h1>
        <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">One targeted artefact · on Workstation's own native swarm</p>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-8">
        {/* Spec form */}
        <main className="@[440px]:col-span-5 space-y-4">
          <Card className="p-6 space-y-5">
            <h3 className="text-base font-black text-white flex items-center gap-3 uppercase tracking-tight">
              <Wand2 size={18} className="text-aura" /> Generate Artefact
            </h3>

            <div>
              <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-2">Artefact Type</label>
              <div className="grid grid-cols-3 gap-2">
                {ARTEFACT_TYPES.map(t => {
                  const Icon = t.icon;
                  const active = artefactType === t.id;
                  return (
                    <button key={t.id} type="button" onClick={() => pickType(t.id)}
                      className={`flex flex-col items-center gap-1.5 py-3 rounded-xl border transition-all ${active ? 'border-aura bg-aura/5 text-white' : 'border-slate-800 bg-slate-950/50 text-slate-400 hover:border-slate-700'}`}>
                      <Icon size={16} className={active ? 'text-aura' : ''} />
                      <span className="text-[8px] font-black uppercase tracking-widest">{t.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Format</label>
                <select value={format} onChange={e => setFormat(e.target.value)} aria-label="Output format"
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura">
                  {FORMATS.map(f => <option key={f} value={f}>{f}</option>)}
                </select>
              </div>
              <div>
                <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Domain</label>
                <select value={domain} onChange={e => setDomain(e.target.value)} aria-label="Domain"
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura">
                  {DOMAINS.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
                </select>
              </div>
            </div>

            <div>
              <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1 flex items-center gap-1.5"><Cpu size={10} /> Owned Resource</label>
              <select value={model} onChange={e => setModel(e.target.value)} aria-label="Owned resource / model preference"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura">
                {MODELS.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
              </select>
            </div>

            <div>
              <label className="text-[9px] font-black uppercase tracking-widest text-slate-500 block mb-1">Specification</label>
              <textarea value={spec} onChange={e => setSpec(e.target.value)} rows={5}
                placeholder="Describe the artefact to generate — e.g. 'a REST endpoint that validates and stores a user record'"
                aria-label="Artefact specification"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-aura resize-none" />
            </div>

            <button type="button" onClick={handleRun} disabled={!spec.trim() || running}
              className="w-full flex items-center justify-center gap-2 py-3 bg-aura text-sovereign rounded-xl font-black uppercase tracking-widest text-xs hover:opacity-90 transition-opacity disabled:opacity-40">
              {running ? <><Loader2 size={14} className="animate-spin" /> Generating…</> : <><Play size={12} /> Generate</>}
            </button>
          </Card>
        </main>

        {/* Output panel */}
        <div className="@[440px]:col-span-7">
          <Card className="p-6 space-y-4 h-full flex flex-col">
            <div className="flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                <h4 className="text-sm font-black text-white uppercase">Artefact</h4>
                {result && (
                  <>
                    <Badge color="aura">{result.artefact_type} · {result.format}</Badge>
                    <Badge color={result.is_external ? 'amber-500' : 'emerald-500'}>{provenance}</Badge>
                  </>
                )}
              </div>
              {result?.output && (
                <div className="flex gap-2">
                  <button type="button" onClick={handleCopy}
                    className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-700 text-slate-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:text-white hover:border-aura/50 transition-colors">
                    {copied ? <><Check size={10} className="text-emerald-400" /> Copied</> : <><Copy size={10} /> Copy</>}
                  </button>
                  <button type="button" onClick={handleExport}
                    className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-700 text-slate-400 rounded-xl text-[9px] font-black uppercase tracking-widest hover:text-white hover:border-aura/50 transition-colors">
                    <Download size={10} /> Export
                  </button>
                </div>
              )}
            </div>

            <div className="flex-1 bg-slate-950 rounded-2xl border border-slate-900 overflow-y-auto p-5 min-h-[340px]">
              {error ? (
                <p className="text-xs text-vital font-mono">[ERROR] {error}</p>
              ) : result?.output ? (
                <pre className="text-[10px] text-slate-300 font-mono leading-relaxed whitespace-pre-wrap">{result.output}</pre>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center gap-3 opacity-40">
                  {running
                    ? <><Loader2 size={28} className="text-aura animate-spin" /><p className="text-xs text-aura font-black uppercase tracking-widest">Generating on the native swarm…</p></>
                    : <><Wand2 size={28} /><p className="text-xs font-black uppercase tracking-widest">Describe an artefact and click Generate</p></>
                  }
                </div>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
