import React, { useState, useEffect, useRef, useCallback } from 'react';
import { REALMS as CANON_REALMS, REALM_LABELS } from '../../lib/taxonomy';
import { useSearchParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import {
  Plus, Play, ChevronRight, Download, Loader2, Trash2,
  Sparkles, FolderOpen, AlertCircle, CheckCircle2, Clock
} from 'lucide-react';

// ── Types ──────────────────────────────────────────────────────────────────

type Stage = 'concept' | 'prototype' | 'commercialise';
type Status = 'idle' | 'running' | 'done' | 'error';

interface ProjectOutput {
  output_id: string;
  stage: Stage;
  created_at: number;
  download_url: string;
  preview: string;
}

interface Project {
  id: string;
  title: string;
  description: string;
  realm: string;
  domain: string;
  stage: Stage;
  status: Status;
  created_at: number;
  updated_at: number;
  outputs: ProjectOutput[];
}

// ── Constants ──────────────────────────────────────────────────────────────

// §17.1 (W321) — canonical realms from the ONE taxonomy source (domains were listed as realms)
const REALMS = CANON_REALMS.map(v => ({ value: v, label: REALM_LABELS[v] }));

const DOMAINS = [
  { value: 'product',    label: 'Product' },
  { value: 'saas',       label: 'SaaS' },
  { value: 'research',   label: 'Research' },
  { value: 'content',    label: 'Content' },
  { value: 'service',    label: 'Service' },
  { value: 'policy',     label: 'Policy' },
  { value: 'curriculum', label: 'Curriculum' },
];

const STAGE_ORDER: Stage[] = ['concept', 'prototype', 'commercialise'];

const STAGE_COLOUR: Record<Stage, string> = {
  concept:       'text-sky-400 border-sky-400/40 bg-sky-400/10',
  prototype:     'text-amber-400 border-amber-400/40 bg-amber-400/10',
  commercialise: 'text-emerald-400 border-emerald-400/40 bg-emerald-400/10',
};

// ── Helpers ────────────────────────────────────────────────────────────────

const fmt = (ts: number) =>
  new Date(ts * 1000).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: '2-digit' });

// ── Sub-components ─────────────────────────────────────────────────────────

const StagePill: React.FC<{ stage: Stage }> = ({ stage }) => (
  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-[9px] font-black uppercase tracking-widest ${STAGE_COLOUR[stage]}`}>
    {stage}
  </span>
);

const StatusDot: React.FC<{ status: Status }> = ({ status }) => {
  if (status === 'running') return <Loader2 size={10} className="animate-spin text-aura" />;
  if (status === 'done')    return <CheckCircle2 size={10} className="text-emerald-400" />;
  if (status === 'error')   return <AlertCircle  size={10} className="text-red-400" />;
  return <Clock size={10} className="text-slate-600" />;
};

// ── Create-project form ────────────────────────────────────────────────────

interface CreateFormProps {
  onCreated: (p: Project) => void;
  onCancel: () => void;
  initialRealm?: string;
  initialDomain?: string;
}

const CreateForm: React.FC<CreateFormProps> = ({ onCreated, onCancel, initialRealm = 'technology', initialDomain = 'product' }) => {
  const [title,       setTitle]       = useState('');
  const [description, setDescription] = useState('');
  const [realm,       setRealm]       = useState(initialRealm);
  const [domain,      setDomain]      = useState(initialDomain);
  const [saving,      setSaving]      = useState(false);
  const [error,       setError]       = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !description.trim()) { setError('Title and description are required.'); return; }
    setSaving(true);
    setError('');
    try {
      const res = await axios.post<Project>('/api/v1/projects/', { title: title.trim(), description: description.trim(), realm, domain });
      onCreated(res.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Failed to create project.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border border-aura/30 rounded-2xl bg-slate-950/80 p-6 space-y-4">
      <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura">New Project</p>

      <div className="space-y-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Title</label>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="e.g. AI-powered legal research assistant"
          className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder:text-slate-600 focus:outline-none focus:border-aura transition-colors"
        />
      </div>

      <div className="space-y-1">
        <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Description</label>
        <textarea
          value={description}
          onChange={e => setDescription(e.target.value)}
          rows={3}
          placeholder="What does this project do, for whom, and why does it matter?"
          className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder:text-slate-600 focus:outline-none focus:border-aura transition-colors resize-none custom-scrollbar"
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Realm</label>
          <select
            value={realm}
            onChange={e => setRealm(e.target.value)}
            aria-label="Project realm"
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura transition-colors"
          >
            {REALMS.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
        </div>
        <div className="space-y-1">
          <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Domain</label>
          <select
            value={domain}
            onChange={e => setDomain(e.target.value)}
            aria-label="Project domain"
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura transition-colors"
          >
            {DOMAINS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
          </select>
        </div>
      </div>

      {error && <p className="text-[9px] text-red-400 font-bold">{error}</p>}

      <div className="flex gap-2 pt-1">
        <button
          type="submit"
          disabled={saving}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-aura text-sovereign text-[10px] font-black uppercase tracking-widest disabled:opacity-40 hover:opacity-90 transition-opacity"
        >
          {saving ? <Loader2 size={12} className="animate-spin" /> : <Plus size={12} />}
          Create Project
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2.5 rounded-xl border border-slate-700 text-slate-400 text-[10px] font-black uppercase tracking-widest hover:border-slate-600 transition-colors"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

// ── Project detail panel ───────────────────────────────────────────────────

interface DetailPanelProps {
  project: Project;
  onUpdate: (p: Project) => void;
  onDelete: (id: string) => void;
}

const DetailPanel: React.FC<DetailPanelProps> = ({ project, onUpdate, onDelete }) => {
  const [streamText, setStreamText]   = useState('');
  const [streaming,  setStreaming]    = useState(false);
  const [error,      setError]        = useState('');
  const [advancing,  setAdvancing]    = useState(false);
  const [deleting,   setDeleting]     = useState(false);
  const streamRef = useRef<HTMLPreElement>(null);
  const readerRef = useRef<ReadableStreamDefaultReader | null>(null);

  const handleExportMarkdown = () => {
    if (!streamText) return;
    const header = `# ${project.title}\n**Stage:** ${project.stage} | **Realm:** ${project.realm} | **Domain:** ${project.domain}\n**Generated:** ${new Date().toISOString().slice(0,10)}\n\n---\n\n`;
    const blob = new Blob([header + streamText], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project.title.toLowerCase().replace(/\s+/g, '-')}-${project.stage}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Auto-scroll during streaming
  useEffect(() => {
    if (streaming && streamRef.current) {
      streamRef.current.scrollTop = streamRef.current.scrollHeight;
    }
  }, [streamText, streaming]);

  // Cleanup reader on unmount
  useEffect(() => () => { readerRef.current?.cancel(); }, []);

  const handleRun = useCallback(async () => {
    setError('');
    setStreamText('');
    setStreaming(true);
    onUpdate({ ...project, status: 'running' });

    try {
      const response = await fetch(`/api/v1/projects/${project.id}/run`, { method: 'POST' });
      if (!response.ok) {
        const body = await response.json();
        throw new Error(body.detail ?? `HTTP ${response.status}`);
      }
      if (!response.body) throw new Error('No response body');

      const reader = response.body.getReader();
      readerRef.current = reader;
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const payload = JSON.parse(line.slice(6));
            if (payload.token !== undefined) {
              setStreamText(prev => prev + payload.token.replace(/\\n/g, '\n'));
            } else if (payload.done) {
              // Reload full project to get outputs list updated
              const updated = await axios.get<Project>(`/api/v1/projects/${project.id}`);
              onUpdate(updated.data);
              setStreaming(false);
              return;
            } else if (payload.error) {
              throw new Error(payload.error);
            }
          } catch { /* malformed event — skip */ }
        }
      }
    } catch (err: any) {
      setError(err?.message ?? 'Stream failed');
      onUpdate({ ...project, status: 'error' });
    } finally {
      setStreaming(false);
    }
  }, [project, onUpdate]);

  const handleAdvance = async () => {
    setAdvancing(true);
    setError('');
    try {
      // Submit to governance — stage advances only after approval in GovernanceHub
      await axios.post(`/api/v1/projects/${project.id}/propose-advance`);
      setError('');
      // Show inline confirmation (not an error)
      setError('✓ Proposal submitted — go to Governance Hub to approve or reject.');
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Cannot propose advance yet.');
    } finally {
      setAdvancing(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete project "${project.title}"? This cannot be undone.`)) return;
    setDeleting(true);
    try {
      await axios.delete(`/api/v1/projects/${project.id}`);
      onDelete(project.id);
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Delete failed.');
      setDeleting(false);
    }
  };

  const canAdvance = project.stage !== 'commercialise' && project.outputs.some(o => o.stage === project.stage);
  const currentStageIdx = STAGE_ORDER.indexOf(project.stage);

  return (
    <div className="flex flex-col h-full min-h-0 gap-4">

      {/* Header */}
      <div className="shrink-0 flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h2 className="text-sm font-black text-white truncate">{project.title}</h2>
          <p className="text-[10px] text-slate-500 mt-0.5 leading-relaxed line-clamp-2">{project.description}</p>
          <div className="flex items-center gap-2 mt-2">
            <span className="text-[9px] font-bold text-slate-600 uppercase">{project.realm} · {project.domain}</span>
            <StagePill stage={project.stage} />
            <StatusDot status={project.status} />
          </div>
        </div>
        <button
          type="button"
          onClick={handleDelete}
          disabled={deleting || streaming}
          title="Delete project"
          aria-label="Delete project"
          className="shrink-0 p-2 rounded-xl border border-slate-800 text-slate-600 hover:text-red-400 hover:border-red-400/30 transition-colors disabled:opacity-30"
        >
          {deleting ? <Loader2 size={12} className="animate-spin" /> : <Trash2 size={12} />}
        </button>
      </div>

      {/* Stage rail */}
      <div className="shrink-0 flex items-center gap-1">
        {STAGE_ORDER.map((s, i) => (
          <React.Fragment key={s}>
            <span className={`text-[8px] font-black uppercase tracking-widest px-2 py-1 rounded-lg border transition-colors ${
              i < currentStageIdx  ? 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10' :
              i === currentStageIdx ? STAGE_COLOUR[s] :
              'text-slate-700 border-slate-800 bg-transparent'
            }`}>{s}</span>
            {i < STAGE_ORDER.length - 1 && (
              <ChevronRight size={10} className={i < currentStageIdx ? 'text-emerald-400' : 'text-slate-700'} />
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Action bar */}
      <div className="shrink-0 flex gap-2">
        <button
          type="button"
          onClick={handleRun}
          disabled={streaming || project.status === 'running'}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-aura text-sovereign text-[9px] font-black uppercase tracking-widest disabled:opacity-40 hover:opacity-90 transition-opacity"
        >
          {streaming ? <Loader2 size={11} className="animate-spin" /> : <Play size={11} />}
          {streaming ? 'Running…' : `Run ${project.stage}`}
        </button>

        {canAdvance && (
          <button
            type="button"
            onClick={handleAdvance}
            disabled={advancing}
            className="flex items-center gap-2 px-4 py-2 rounded-xl border border-aura/40 text-aura text-[9px] font-black uppercase tracking-widest disabled:opacity-40 hover:bg-aura/10 transition-colors"
          >
            {advancing ? <Loader2 size={11} className="animate-spin" /> : <ChevronRight size={11} />}
            Propose Advance
          </button>
        )}
      </div>

      {error && (
        <div className={`shrink-0 flex items-start gap-2 rounded-xl border px-3 py-2 ${error.startsWith('✓') ? 'border-emerald-500/30 bg-emerald-500/10' : 'border-red-500/30 bg-red-500/10'}`}>
          <AlertCircle size={12} className={`shrink-0 mt-0.5 ${error.startsWith('✓') ? 'text-emerald-400' : 'text-red-400'}`} />
          <p className={`text-[10px] leading-relaxed ${error.startsWith('✓') ? 'text-emerald-300' : 'text-red-300'}`}>{error}</p>
        </div>
      )}

      {/* Live stream output */}
      {(streaming || streamText) && (
        <div className="shrink-0 border border-aura/20 rounded-2xl overflow-hidden">
          <div className="flex items-center justify-between gap-2 px-4 py-2 border-b border-aura/20 bg-aura/5">
            <div className="flex items-center gap-2">
              {streaming
                ? <><div className="w-5 h-5 rounded-full border-2 border-aura animate-spin border-t-transparent" /><span className="text-[9px] font-black uppercase tracking-[0.3em] text-aura">Generating…</span></>
                : <><Sparkles size={12} className="text-aura" /><span className="text-[9px] font-black uppercase tracking-[0.3em] text-aura">Latest output</span></>
              }
            </div>
            {!streaming && streamText && (
              <button
                type="button"
                onClick={handleExportMarkdown}
                className="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-aura/30 text-aura text-[8px] font-black uppercase tracking-widest hover:bg-aura/10 transition-colors"
              >
                <Download size={9} /> Export .md
              </button>
            )}
          </div>
          <pre
            ref={streamRef}
            className="p-4 text-xs text-slate-300 font-mono whitespace-pre-wrap break-words max-h-72 overflow-y-auto custom-scrollbar leading-relaxed"
          >
            {streamText}
            {streaming && <span className="inline-block w-1.5 h-3 bg-aura animate-pulse ml-0.5" />}
          </pre>
        </div>
      )}

      {/* Saved outputs */}
      {project.outputs.length > 0 && (
        <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar space-y-2">
          <p className="text-[9px] font-black uppercase tracking-widest text-slate-600 mb-1">Saved Outputs ({project.outputs.length})</p>
          {[...project.outputs].reverse().map(out => (
            <div key={out.output_id} className="border border-slate-800 rounded-xl p-3 space-y-2">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <StagePill stage={out.stage} />
                  <span className="text-[8px] text-slate-600">{fmt(out.created_at)}</span>
                </div>
                <a
                  href={out.download_url}
                  download
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-aura/30 text-aura text-[8px] font-black uppercase tracking-widest hover:bg-aura/10 transition-colors"
                >
                  <Download size={9} /> Download
                </a>
              </div>
              <p className="text-[10px] text-slate-400 leading-relaxed line-clamp-3">{out.preview}</p>
            </div>
          ))}
        </div>
      )}

      {project.outputs.length === 0 && !streaming && !streamText && (
        <div className="flex-1 flex flex-col items-center justify-center gap-3 text-center py-8">
          <Sparkles size={20} className="text-slate-700" />
          <p className="text-[10px] text-slate-600 leading-relaxed max-w-[200px]">
            Press <span className="text-aura font-black">Run {project.stage}</span> to generate your first AI deliverable for this project.
          </p>
        </div>
      )}
    </div>
  );
};

// ── Main page ──────────────────────────────────────────────────────────────

export const ProjectsHub: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const urlRealm  = searchParams.get('realm')  ?? 'technology';
  const urlDomain = searchParams.get('domain') ?? 'product';
  const openNew   = searchParams.get('new') === '1';

  const queryClient = useQueryClient();

  // Project list — tanstack-query for caching + background refetch
  const {
    data: projectsData = [],
    isLoading: loading,
    isError: hasFetchError,
  } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => axios.get<Project[]>('/api/v1/projects/').then(r => r.data ?? []),
  });
  const fetchError = hasFetchError ? 'Could not load projects. Is the backend running?' : '';

  const [projects,   setProjects]   = useState<Project[]>([]);
  const [selected,   setSelected]   = useState<Project | null>(null);
  const [showCreate, setShowCreate] = useState(openNew);

  // Sync query data into local state (local state allows optimistic mutations)
  useEffect(() => { setProjects(projectsData); }, [projectsData]);

  // Clear the ?new=1 param once we've consumed it
  useEffect(() => {
    if (openNew) {
      searchParams.delete('new');
      setSearchParams(searchParams, { replace: true });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleCreated = (p: Project) => {
    setProjects(prev => [p, ...prev]);
    setSelected(p);
    setShowCreate(false);
    queryClient.invalidateQueries({ queryKey: ['projects'] });
  };

  const handleUpdate = useCallback((updated: Project) => {
    setProjects(prev => prev.map(p => p.id === updated.id ? updated : p));
    setSelected(prev => prev?.id === updated.id ? updated : prev);
  }, []);

  const handleDelete = useCallback((id: string) => {
    setProjects(prev => prev.filter(p => p.id !== id));
    setSelected(prev => prev?.id === id ? null : prev);
  }, []);

  return (
    <div className="flex h-full min-h-0 gap-0">

      {/* Left column — project list */}
      <div className="w-72 shrink-0 flex flex-col h-full border-r border-slate-800 bg-slate-950/40">
        <div className="shrink-0 px-4 pt-6 pb-3 flex items-center justify-between">
          <div>
            <h1 className="text-xs font-black uppercase tracking-[0.3em] text-white">Projects</h1>
            <p className="text-[9px] text-slate-600 mt-0.5">AI-powered product workflows</p>
          </div>
          <button
            type="button"
            onClick={() => { setShowCreate(true); setSelected(null); }}
            title="New project"
            aria-label="New project"
            className="p-2 rounded-xl bg-aura text-sovereign hover:opacity-90 transition-opacity"
          >
            <Plus size={13} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar px-2 pb-4 space-y-1">
          {loading && (
            <div className="flex items-center gap-2 px-3 py-4 text-slate-600 text-[10px]">
              <Loader2 size={12} className="animate-spin" /> Loading…
            </div>
          )}

          {fetchError && (
            <div className="px-3 py-3 rounded-xl border border-red-500/20 bg-red-500/10 mx-1">
              <p className="text-[9px] text-red-400 font-bold">{fetchError}</p>
            </div>
          )}

          {!loading && !fetchError && projects.length === 0 && (
            <div className="flex flex-col items-center gap-3 py-8 text-center">
              <FolderOpen size={20} className="text-slate-700" />
              <p className="text-[9px] text-slate-600 leading-relaxed max-w-[160px]">
                No projects yet. Click <span className="text-aura font-black">+</span> to create your first AI project.
              </p>
            </div>
          )}

          {projects.map(p => (
            <button
              key={p.id}
              type="button"
              onClick={() => { setSelected(p); setShowCreate(false); }}
              className={`w-full text-left px-3 py-3 rounded-xl border transition-all ${
                selected?.id === p.id
                  ? 'border-aura/40 bg-aura/10'
                  : 'border-slate-800/60 bg-slate-900/30 hover:border-slate-700 hover:bg-slate-900/60'
              }`}
            >
              <div className="flex items-start justify-between gap-1 mb-1">
                <span className="text-[10px] font-black text-white line-clamp-1 flex-1">{p.title}</span>
                <StatusDot status={p.status} />
              </div>
              <div className="flex items-center gap-1.5">
                <StagePill stage={p.stage} />
                <span className="text-[8px] text-slate-600">{p.realm}</span>
              </div>
              <p className="text-[9px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">{p.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Right panel — create form or project detail */}
      <div className="flex-1 min-w-0 overflow-y-auto custom-scrollbar p-8">
        {showCreate && (
          <div className="max-w-lg">
            <CreateForm
              onCreated={handleCreated}
              onCancel={() => setShowCreate(false)}
              initialRealm={urlRealm}
              initialDomain={urlDomain}
            />
          </div>
        )}

        {!showCreate && selected && (
          <DetailPanel
            key={selected.id}
            project={selected}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
          />
        )}

        {!showCreate && !selected && (
          <div className="h-full flex flex-col items-center justify-center gap-4 text-center">
            <Sparkles size={32} className="text-slate-800" />
            <div>
              <p className="text-sm font-black text-slate-600 uppercase tracking-widest">Select a project</p>
              <p className="text-[10px] text-slate-700 mt-1">or create a new one to start generating AI deliverables</p>
            </div>
            <button
              type="button"
              onClick={() => setShowCreate(true)}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-aura text-sovereign text-[10px] font-black uppercase tracking-widest hover:opacity-90 transition-opacity"
            >
              <Plus size={12} /> New Project
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
