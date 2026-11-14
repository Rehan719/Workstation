import { silenceIsRight } from '../../components/ReadFailures';   // W961 (FU-1181)
import { errorMessage } from '../../lib/api';   // W1015 - a caught failure, said as what it was
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { REALMS as CANON_REALMS, REALM_LABELS, DOMAIN_LABELS } from '../../lib/taxonomy';
import { useSearchParams } from 'react-router-dom';
import { getPrefs } from '../../lib/userPrefs';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { downloadExport } from '../../lib/download';
// W495 (FU-131, S12.6) - the shared provenance helpers, so this page labels output the same way
// every other surface does rather than inventing its own wording
import { axiosDetail, provenanceBadge, provenanceLine } from '../../lib/api';   // W1011: axiosDetail
import { refusalOf } from '../../lib/stream';   // W1012
import { AskPerson } from '../../components/AskPerson';   // W968 (P5.14 clause 6)
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
  // W495 (FU-131, S12.6) - the run's done frame reports these and the record dropped them, so a
  // deterministic-floor scaffold was listed as an "AI deliverable" with nothing saying what composed it
  served_by?: string | null;
  is_external?: boolean;
  provenance_basis?: string;
}

interface Project {
  id: string;
  title: string;
  description: string;
  first_description?: string | null;
  first_description_at?: number | null;
  // W867 (FU-1043) - whether it waits on a person: derived by the server on each read from the pending proposals
  waiting_on_person?: { waiting?: boolean | null; on?: { proposal_id: string; what: string; since: number }[]; where?: string; basis?: string } | null;
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

//  W1044 - the status is said in words as well as by its icon's colour
const StatusDot: React.FC<{ status: Status }> = ({ status }) => {
  const said = { role: 'img', 'aria-label': `status: ${status}` };
  if (status === 'running') return <Loader2 size={10} className="animate-spin text-aura" {...said} />;
  if (status === 'done')    return <CheckCircle2 size={10} className="text-emerald-400" {...said} />;
  if (status === 'error')   return <AlertCircle  size={10} className="text-red-400" {...said} />;
  return <Clock size={10} className="text-slate-600" {...said} />;
};

// ── Create-project form ────────────────────────────────────────────────────

interface CreateFormProps {
  onCreated: (p: Project) => void;
  onCancel: () => void;
  initialRealm?: string;      // W505: a taxonomy DOMAIN on the hub-CTA path, a canonical realm from the picker
  initialDomain?: string;
  taxonomyRealm?: string;     // W505 (P2.5): the canonical realm axis, carried separately
}

// W786 (FU-969) - a plain New project opened on 'technology', a legacy value outside the taxonomy, and the picker then
// listed it as the subject; it opens on the first canonical realm. A hub's CTA still passes its own domain.
const CreateForm: React.FC<CreateFormProps> = ({ onCreated, onCancel, initialRealm = CANON_REALMS[0], initialDomain = 'product', taxonomyRealm = '' }) => {
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
      // W505 (P2.5) — both axes. An empty taxonomy_realm lets the API keep its own default rather than
      // this form inventing one.
      const res = await axios.post<Project>('/api/v1/projects/', {
        title: title.trim(), description: description.trim(), realm, domain,
        ...(taxonomyRealm ? { taxonomy_realm: taxonomyRealm } : {}),
      });
      onCreated(res.data);
    } catch (err: any) {
      //  W1044 - the fallback says what happened: a fixed sentence said nothing of a server that was not reached, or
      //  that answered without a reason
      setError(axiosDetail(err, `Could not create the project: ${errorMessage(err)}`));
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
          {/* W662 (FU-724) - this field holds a DOMAIN when a hub opened the form and a REALM when the picker
              did. It showed "Enterprise" while holding "care". It now shows what it holds. */}
          <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Subject</label>
          <select
            value={realm}
            onChange={e => setRealm(e.target.value)}
            aria-label="Project subject"
            data-testid="project-subject"
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura transition-colors"
          >
            {!REALMS.some(r => r.value === initialRealm) && (
              <option key={initialRealm} value={initialRealm}>
                {DOMAIN_LABELS[initialRealm] ? `${DOMAIN_LABELS[initialRealm]} (domain)` : `${initialRealm} (subject)`}
              </option>
            )}
            {REALMS.map(r => <option key={r.value} value={r.value}>{r.label} (realm)</option>)}
          </select>
          {!REALMS.some(r => r.value === initialRealm) && realm !== initialRealm && (
            <p data-testid="project-subject-note" className="text-[9px] text-amber-400">
              This project will be filed under the realm you chose, not under {DOMAIN_LABELS[initialRealm] ?? initialRealm}.
            </p>
          )}
        </div>
        <div className="space-y-1">
          <label className="text-[9px] font-black uppercase tracking-widest text-slate-500">Area</label>
          <select
            value={domain}
            onChange={e => setDomain(e.target.value)}
            aria-label="Project area"
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-aura transition-colors"
          >
            {DOMAINS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
          </select>
        </div>
      </div>

      {error && <p data-testid="project-create-error" className="text-[9px] text-red-400 font-bold">{error}</p>}

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
  // W495 (FU-131, S12.6) - the done frame reports these and the page discarded them
  const [streamServedBy, setStreamServedBy] = useState<string | null | undefined>(undefined);
  const [streamIsExternal, setStreamIsExternal] = useState(false);
  const [streaming,  setStreaming]    = useState(false);
  const [error,      setError]        = useState('');
  const [advancing,  setAdvancing]    = useState(false);
  const [deleting,   setDeleting]     = useState(false);
  const [asking,     setAsking]       = useState(false);   // W968 - the question before a delete
  const streamRef = useRef<HTMLPreElement>(null);
  const readerRef = useRef<ReadableStreamDefaultReader | null>(null);

  const handleExportMarkdown = () => {
    if (!streamText) return;
    // W495 (FU-131, S12.6) - the exported file carried no provenance at all, so a floor-composed
    // scaffold left the product as a document with a "Generated" date and nothing else. The label
    // travels INTO the file (the W490 rule).
    const prov = provenanceLine(streamServedBy, streamIsExternal);
    const header = `# ${project.title}\n**Stage:** ${project.stage} | **Domain:** ${project.realm} | **Area:** ${project.domain}\n**Generated:** ${new Date().toISOString().slice(0,10)}\n${prov}\n\n---\n\n`;
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
      //  W1012 - a refused run says the server's status and reason in lib/stream.ts's sentence: a field check's list
      //  read "[object Object]", and a refusal whose body was not JSON said the parser's words
      if (!response.ok) throw new Error(await refusalOf(response));
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
          // W492 (FU-216) — the error frame used to be re-raised INSIDE this try, so the page's
          // own "malformed event — skip" catch swallowed the backend's error frame: the optimistic
          // status 'running' was never corrected, the spinner kept turning and the Run button stayed
          // disabled while the API had already persisted status 'error'. Only the PARSE is tolerated
          // here; a well-formed error frame is handled outside it.
          let payload: any = null;
          try {
            payload = JSON.parse(line.slice(6));
          } catch { continue; }          // genuinely malformed event — skip
          if (payload.error) {
            setError(String(payload.error));
            onUpdate({ ...project, status: 'error' });
            setStreaming(false);
            return;
          }
          if (payload.token !== undefined) {
            setStreamText(prev => prev + String(payload.token).replace(/\\n/g, '\n'));
          } else if (payload.done) {
            setStreamServedBy(payload.served_by ?? null);
            setStreamIsExternal(Boolean(payload.is_external));
            // Reload full project to get outputs list updated
            //  W1044 - the run completed and the server saved its output, so a failed re-read is said as that. It fell
            //  to the catch below as the run's own failure, which marked the project as in error over a saved output
            try {
              const updated = await axios.get<Project>(`/api/v1/projects/${project.id}`);
              onUpdate(updated.data);
            } catch (e) {
              onUpdate({ ...project, status: 'done' });
              setError(`The run completed and its output was saved, but the project could not be read again to show it: ${errorMessage(e)}`);
            }
            setStreaming(false);
            return;
          }
        }
      }
      // W492 (FU-216) — the reader can finish without a `done` frame ever arriving (a dropped or
      // truncated stream). The optimistic status 'running' then stood forever, so re-read the
      // project and report whatever the API actually holds rather than leaving a spinner turning.
      //  W959 (FU-1181) - a failed re-read is said just below ("could not be re-read"), so it reads as no answer
      const after = await axios.get<Project>(`/api/v1/projects/${project.id}`).then(r => r, () => null);
      if (after) {
        onUpdate(after.data);
        // W492 (refutation) - 'idle' is the status the backend actually writes when a run is reset or
        // goes stale (projects/api.py:273, :399, :438); it was the one outcome this said nothing about,
        // so a run that ended without completing looked like a run that had simply finished.
        const st = after.data.status;
        if (st === 'error') setError('The run ended in an error (the stream closed without completing).');
        else if (st === 'running') setError('The stream closed before the run reported completion — the project is still marked running.');
        else if (st === 'idle') setError('The stream closed without completing and the run was reset — nothing was produced for this stage.');
      } else {
        setError('The stream closed before completing, and the project could not be re-read.');
      }
    } catch (err: any) {
      setError(errorMessage(err));
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
      // W867 (FU-1043) - the project now waits on a person: re-read it so the page says so without a reload. A
      // failed re-read leaves the confirmation standing, and the next read of the list says it.
      try { const again = await axios.get(`/api/v1/projects/${project.id}`); onUpdate(again.data); } catch { silenceIsRight('a failed re-read leaves the confirmation standing, and the next read of the list says it')(); }
    } catch (err: any) {
      //  W1044 - by what happened: the fallback said the project was not ready yet, of a call that reached no server
      setError(axiosDetail(err, `Could not propose the advance: ${errorMessage(err)}`));
    } finally {
      setAdvancing(false);
    }
  };

  const handleDelete = async () => {
    setAsking(false);
    setDeleting(true);
    try {
      //  W971 - the server deletes only with the title typed back, which the question above held the act for
      await axios.delete(`/api/v1/projects/${project.id}`, { params: { confirm_title: project.title } });
      onDelete(project.id);
    } catch (err: any) {
      setError(axiosDetail(err, `Delete failed: ${errorMessage(err)}`));   // W1044 - and by what happened
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
          {typeof project.first_description === 'string' && project.first_description !== project.description && (
            <p data-testid="project-first-words" className="text-[10px] text-slate-400 mt-1 leading-relaxed">
              What you first wrote{typeof project.first_description_at === 'number' ? ` (${new Date(project.first_description_at * 1000).toLocaleDateString()})` : ''}: {project.first_description}
            </p>
          )}
          {project.first_description == null && (
            <p data-testid="project-first-words-not-kept" className="text-[10px] text-slate-500 mt-1 leading-relaxed">
              The words this project was first described in were not kept: it was made before they were recorded.
            </p>
          )}
          {/* W867 (FU-1043) - WHETHER THIS PROJECT WAITS ON A PERSON, as the server read it from the proposals pending
              for it. A state it could not read is said; nothing waiting prints nothing. */}
          {project.waiting_on_person?.waiting === true && (project.waiting_on_person.on ?? []).map(w => (
            <p key={w.proposal_id} data-testid="project-waiting-on-person" className="text-[10px] font-bold text-amber-400 mt-1 leading-relaxed"
               title={project.waiting_on_person?.basis}>
              Waiting on a person: {w.what}, raised {new Date(w.since * 1000).toLocaleString()}. It is decided in {project.waiting_on_person?.where}.
            </p>
          ))}
          {project.waiting_on_person?.waiting === null && (
            <p data-testid="project-waiting-not-known" className="text-[10px] text-amber-400 mt-1 leading-relaxed">{project.waiting_on_person.basis}</p>
          )}
          <div className="flex items-center gap-2 mt-2">
            {/* W628 (FU-537) — a project's `realm` field holds the taxonomy DOMAIN and `domain` a sub-area; labelled as what they are */}
            <span className="text-[9px] font-bold text-slate-600 uppercase" title="domain · area (the project record stores the domain in its 'realm' field)">{project.realm} · {project.domain}</span>
            <StagePill stage={project.stage} />
            <StatusDot status={project.status} />
          </div>
        </div>
        <button
          type="button"
          onClick={() => setAsking(true)}
          disabled={deleting || streaming}
          title="Delete project"
          aria-label="Delete project"
          className="shrink-0 p-2 rounded-xl border border-slate-800 text-slate-600 hover:text-red-400 hover:border-red-400/30 transition-colors disabled:opacity-30"
        >
          {deleting ? <Loader2 size={12} className="animate-spin" /> : <Trash2 size={12} />}
        </button>
      </div>
      {/* W968 (P5.14 clause 6) - a delete that cannot be undone waits for the project's title, typed back */}
      {asking && (
        <AskPerson question={`Delete the project "${project.title}"?`} kind="confirmation"
          options={[
            { id: 'delete', label: 'Delete the project', differs: "the project's record is removed from this platform, and a proposal still pending for it is marked as for a deleted project", undo: 'it cannot be undone: no copy of the record is kept' },
            { id: 'keep', label: 'Keep it', differs: 'nothing changes', undo: 'there is nothing to undo', recommended: true },
          ]}
          typeBack={{ optionId: 'delete', text: project.title, label: "Type the project's title to delete it" }}
          onChoose={id => { if (id === 'delete') void handleDelete(); else setAsking(false); }} />
      )}

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
          <p data-testid="project-message" className={`text-[10px] leading-relaxed ${error.startsWith('✓') ? 'text-emerald-300' : 'text-red-300'}`}>{error}</p>
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
              {/* W495 (FU-131, S12.6) - the stream's done frame carries served_by and is_external and
                  this panel ignored both, so floor-composed text read as a generated deliverable. */}
              {!streaming && streamServedBy !== undefined && (() => {
                const b = provenanceBadge(streamServedBy, streamIsExternal);
                return <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`}
                             title={b.title} data-testid="project-stream-provenance">{b.label}</span>;
              })()}
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
                  {/* W495 (FU-131, S12.6) - every saved output says what composed it */}
                  {(() => {
                    const b = provenanceBadge(out.served_by, out.is_external);
                    return <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`}
                                 title={out.provenance_basis || b.title}
                                 data-testid={`project-output-provenance-${out.output_id}`}>{b.label}</span>;
                  })()}
                </div>
                {/* Ledger cluster 5 — a raw <a download> to /api/... skips the bearer layer and
                    401s under auth; downloadExport fetches through the patched window.fetch. */}
                <button
                  type="button"
                  onClick={() => downloadExport(out.download_url, String(out.output_id ?? 'output'))
                    .catch((e: any) => alert(`Download failed: ${errorMessage(e)}`))}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-aura/30 text-aura text-[8px] font-black uppercase tracking-widest hover:bg-aura/10 transition-colors"
                >
                  <Download size={9} /> Download
                </button>
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
            {/* W495 (FU-131, S12.6) - on the deterministic floor the run composes a structured
                scaffold; the badge on each output says which it was. */}
            Press <span className="text-aura font-black">Run {project.stage}</span> to produce this project's first stage document. Each output is labelled with what composed it.
          </p>
        </div>
      )}
    </div>
  );
};

// ── Main page ──────────────────────────────────────────────────────────────

export const ProjectsHub: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const urlRealm  = searchParams.get('realm')  ?? CANON_REALMS[0];   // W786 (FU-969) - not the legacy 'technology'
  const urlDomain = searchParams.get('domain') ?? 'product';
  // W505 (P2.5) — the canonical realm a hub CTA carried, kept apart from `realm` above (which is a
  // taxonomy DOMAIN on that path). Falls back to the user's preference, then to the API's own default.
  const urlTaxRealm = searchParams.get('taxonomyRealm') ?? (getPrefs().defaultRealm ?? '');
  const openNew   = searchParams.get('new') === '1';

  const queryClient = useQueryClient();

  // Project list — tanstack-query for caching + background refetch
  const {
    data: projectsData,
    isLoading: loading,
    isError: hasFetchError,
    error: listError,
  } = useQuery<Project[]>({
    queryKey: ['projects'],
    queryFn: () => axios.get<Project[]>('/api/v1/projects/').then(r => r.data ?? []),
  });
  //  W1044 - said with its reason: one fixed sentence asked whether the backend was running, of a server that answered
  const fetchError = hasFetchError ? `The projects could not be read, so the list is not what is there: ${errorMessage(listError)}` : '';

  const [projects,   setProjects]   = useState<Project[]>([]);
  const [selected,   setSelected]   = useState<Project | null>(null);
  const [showCreate, setShowCreate] = useState(openNew);

  // Sync query data into local state (local state allows optimistic mutations)
  //  W1044 - only an answer is copied. A default of [] was a new list on every render while the list was unread, so
  //  this set it on every render and the page rendered again without end: while the read was pending, and after
  //  it had failed
  useEffect(() => { if (projectsData) setProjects(projectsData); }, [projectsData]);

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
            {/* W620 (FU-483, M2 v8 R2.3) — a Project is not the §4 lifecycle and never becomes a VSB; it said neither */}
            <p className="text-[9px] text-slate-500 mt-1" data-testid="projects-scope-note">
              AI deliverable projects (concept → prototype → commercialise). Not the §4 enterprise lifecycle: a project never becomes a living VSB — Genesis establishes those.
            </p>
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
              <p data-testid="projects-unread" className="text-[9px] text-red-400 font-bold">{fetchError}</p>
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
                {p.waiting_on_person?.waiting === true && (
                  <span data-testid="project-list-waiting" className="text-[8px] font-bold text-amber-400" title={p.waiting_on_person.basis}>waiting on a person</span>
                )}
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
              taxonomyRealm={urlTaxRealm}
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
