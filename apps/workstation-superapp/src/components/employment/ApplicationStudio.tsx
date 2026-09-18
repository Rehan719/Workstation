import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  FileStack, FileText, Star, Target, ClipboardList, BookOpen, Mic,
  FileSignature, GraduationCap, ShieldCheck, UploadCloud, Trash2, Download,
  CheckSquare, Square, Loader2, Sparkles, Link as LinkIcon, Globe, Linkedin, Wand2,
  Search, Briefcase, MapPin, CircleCheck, ScrollText
} from 'lucide-react';
import { Card, Button } from '@workstation/ui';
import { provenanceBadge } from '../../lib/api';

interface IngestedFile {
  file_id: string;
  filename: string;
  category?: string;
  timestamp: string;
}

interface GeneratedDoc {
  output_id: string;
  output_type: string;
  title: string;
  content: string;
  timestamp: string;
  ai_provenance?: { served_by?: string | null; is_external?: boolean };   // W454 — rendered, not dropped
}

interface ClassificationNotice {
  filename: string;
  label: string;
  confidence: number;
}

// W454 — an ILLUSTRATIVE example listing: no url, no posting date (they were invented), a salary estimate
interface JobListing {
  listing_id: string;
  title: string;
  company: string;
  location: string;
  salary_estimate?: string | null;
  tags: string[];
  description: string;
  illustrative?: boolean;
  basis?: string;
}

const INPUT_SLOTS = [
  { id: 'cv_history', label: 'Old CVs', icon: FileStack },
  { id: 'past_applications', label: 'Past Applications', icon: FileText },
  { id: 'star_examples', label: 'STAR Examples', icon: Star },
  { id: 'job_ad', label: 'Target Job Ad', icon: Target },
  { id: 'job_description', label: 'Job Description', icon: ScrollText },
  { id: 'person_spec', label: 'Person Specification', icon: ClipboardList },
  { id: 'application_guidance', label: 'Application Guidance', icon: BookOpen },
  { id: 'interview_prep_materials', label: 'Interview Prep Materials', icon: Mic },
];

const OUTPUT_TYPES = [
  { id: 'cv', label: 'CV', icon: FileText },
  { id: 'cover_letter', label: 'Cover Letter', icon: FileSignature },
  { id: 'supporting_statement', label: 'Supporting Statement', icon: ClipboardList },
  { id: 'application_form', label: 'Application Forms', icon: FileStack },
  { id: 'interview_prep', label: 'Interview Preparation', icon: Mic },
  { id: 'new_job_prep', label: 'New Job Preparation', icon: GraduationCap },
  { id: 'in_job_support', label: 'In-Job Support', icon: ShieldCheck },
  { id: 'linkedin_profile', label: 'LinkedIn Profile', icon: Linkedin },
];

// W470 — the title is the registry's (the Employment hub passes toolsFor('/employment')['studio'].title)
export const ApplicationStudio: React.FC<{ title: string }> = ({ title }) => {
  const [uploads, setUploads] = useState<IngestedFile[]>([]);
  const [uploadingSlot, setUploadingSlot] = useState<string | null>(null);
  const [classifying, setClassifying] = useState(false);
  const [classificationNotices, setClassificationNotices] = useState<ClassificationNotice[]>([]);
  const [companyWebsite, setCompanyWebsite] = useState('');
  const [linkedinUrl, setLinkedinUrl] = useState('');
  const [instructions, setInstructions] = useState('');
  const [selectedOutputs, setSelectedOutputs] = useState<string[]>([]);
  const [generating, setGenerating] = useState(false);
  const [results, setResults] = useState<GeneratedDoc[] | null>(null);
  const [jobQuery, setJobQuery] = useState('');
  const [jobSearching, setJobSearching] = useState(false);
  const [jobResults, setJobResults] = useState<JobListing[] | null>(null);
  const [jobSearchMeta, setJobSearchMeta] = useState<{ query: string; basis?: string; total?: number; ai_provenance?: { served_by?: string | null; is_external?: boolean } } | null>(null);
  const [jobSearchError, setJobSearchError] = useState('');
  const [usingListingUrl, setUsingListingUrl] = useState<string | null>(null);
  const [usedListingUrls, setUsedListingUrls] = useState<string[]>([]);

  const fetchUploads = async () => {
    try {
      const resp = await axios.get('/api/v1/ingest/list');
      setUploads(resp.data);
    } catch (e) {
      // Non-fatal: leave existing uploads list as-is.
    }
  };

  useEffect(() => {
    fetchUploads();
  }, []);

  const handleUpload = async (slotId: string, e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    setUploadingSlot(slotId);
    try {
      for (const file of Array.from(files)) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('category', slotId);
        await axios.post('/api/v1/ingest/', formData);
      }
      await fetchUploads();
    } catch (err) {
      alert('Upload failed.');
    } finally {
      setUploadingSlot(null);
      e.target.value = '';
    }
  };

  const handleAutoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    setClassifying(true);
    try {
      const notices: ClassificationNotice[] = [];
      for (const file of Array.from(files)) {
        const formData = new FormData();
        formData.append('file', file);
        const resp = await axios.post('/api/v1/career/uploads/auto', formData);
        const category: string = resp.data.classification.category;
        const label = INPUT_SLOTS.find(s => s.id === category)?.label || 'Uncategorized';
        notices.push({
          filename: resp.data.filename,
          label,
          confidence: resp.data.classification.confidence,
        });
      }
      setClassificationNotices(notices);
      await fetchUploads();
    } catch (err) {
      alert('Auto-categorization failed.');
    } finally {
      setClassifying(false);
      e.target.value = '';
    }
  };

  const handleDelete = async (fileId: string) => {
    try {
      await axios.delete(`/api/v1/ingest/${fileId}`);
      await fetchUploads();
    } catch (err) {
      alert('Could not remove file.');
    }
  };

  const toggleOutput = (id: string) => {
    setSelectedOutputs(prev => prev.includes(id) ? prev.filter(o => o !== id) : [...prev, id]);
  };

  const allOutputsSelected = selectedOutputs.length === OUTPUT_TYPES.length;
  const toggleSelectAllOutputs = () => {
    setSelectedOutputs(allOutputsSelected ? [] : OUTPUT_TYPES.map(o => o.id));
  };

  const handleGenerate = async () => {
    if (selectedOutputs.length === 0) return alert('Select at least one output to generate.');
    setGenerating(true);
    setResults(null);
    try {
      const fileIds = uploads
        .filter(u => INPUT_SLOTS.some(s => s.id === u.category))
        .map(u => u.file_id);
      const resp = await axios.post('/api/v1/career/generate', {
        file_ids: fileIds,
        company_website: companyWebsite,
        linkedin_url: linkedinUrl,
        instructions,
        output_types: selectedOutputs,
      });
      setResults(resp.data.results);
    } catch (err) {
      alert('Generation failed.');
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = (doc: GeneratedDoc) => {
    const blob = new Blob([doc.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${doc.output_type}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleJobSearch = async () => {
    setJobSearching(true);
    setJobSearchError('');
    setJobResults(null);
    try {
      const fileIds = uploads
        .filter(u => INPUT_SLOTS.some(s => s.id === u.category))
        .map(u => u.file_id);
      const resp = await axios.post('/api/v1/career/job-search', {
        file_ids: fileIds,
        instructions,
        query: jobQuery,
        limit: 12,
      });
      setJobResults(resp.data.results);
      setJobSearchMeta({ query: resp.data.query, basis: resp.data.basis, total: resp.data.total, ai_provenance: resp.data.ai_provenance });
    } catch (err) {
      setJobSearchError('Example-listing synthesis failed. Try again.');
    } finally {
      setJobSearching(false);
    }
  };

  const handleUseListing = async (listing: JobListing) => {
    setUsingListingUrl(listing.listing_id);
    try {
      await axios.post('/api/v1/career/job-search/use', {
        title: listing.title,
        company: listing.company,
        location: listing.location,
        listing_id: listing.listing_id,
        description: listing.description,
        salary_estimate: listing.salary_estimate ?? null,
      });
      setUsedListingUrls(prev => [...prev, listing.listing_id]);
      await fetchUploads();
    } catch (err) {
      alert('Could not attach this listing as the Target Job Ad.');
    } finally {
      setUsingListingUrl(null);
    }
  };

  return (
    <div className="space-y-10">
      <div>
        <h3 className="text-2xl font-black text-white uppercase tracking-tight mb-2">{title}</h3>
        <p className="text-slate-500 font-bold text-sm">Upload your materials, then generate tailored application outputs.</p>
      </div>

      <div id="input-materials-section" className="space-y-4">
        <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Input Materials</label>
        <div className="grid grid-cols-1 @lg:grid-cols-2 @3xl:grid-cols-3 gap-4">
          {INPUT_SLOTS.map(slot => {
            const slotFiles = uploads.filter(u => u.category === slot.id);
            return (
              <div key={slot.id} className="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-300">
                    <slot.icon size={14} className="text-aura" />
                    <span className="text-[10px] font-black uppercase tracking-widest">{slot.label}</span>
                  </div>
                  <label
                    htmlFor={`upload-${slot.id}`}
                    className="flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-aura rounded-lg text-[9px] font-black uppercase tracking-widest cursor-pointer transition-colors"
                  >
                    {uploadingSlot === slot.id ? <Loader2 size={11} className="animate-spin" /> : <UploadCloud size={11} />}
                    Upload
                  </label>
                  <input
                    id={`upload-${slot.id}`}
                    type="file"
                    multiple
                    className="hidden"
                    onChange={(e) => handleUpload(slot.id, e)}
                  />
                </div>
                {slotFiles.length > 0 ? (
                  <ul className="space-y-1.5">
                    {slotFiles.map(f => (
                      <li key={f.file_id} className="flex items-center justify-between gap-2 text-[10px] text-slate-400 font-bold">
                        <span className="truncate">{f.filename}</span>
                        <button type="button" onClick={() => handleDelete(f.file_id)} aria-label={`Remove ${f.filename}`} title={`Remove ${f.filename}`} className="text-slate-600 hover:text-red-400 shrink-0">
                          <Trash2 size={11} />
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-[10px] text-slate-600 font-bold">No files yet.</p>
                )}
              </div>
            );
          })}
        </div>

        {(() => {
          const uncategorized = uploads.filter(u => u.category === 'uncategorized');
          return (
            <div className="p-4 rounded-2xl bg-slate-900 border border-dashed border-slate-700 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-300">
                  <Wand2 size={14} className="text-aura" />
                  <span className="text-[10px] font-black uppercase tracking-widest">Miscellaneous (Auto-Categorize)</span>
                </div>
                <label
                  htmlFor="upload-misc-auto"
                  className="flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-aura rounded-lg text-[9px] font-black uppercase tracking-widest cursor-pointer transition-colors"
                >
                  {classifying ? <Loader2 size={11} className="animate-spin" /> : <UploadCloud size={11} />}
                  Upload
                </label>
                <input
                  id="upload-misc-auto"
                  type="file"
                  multiple
                  className="hidden"
                  onChange={handleAutoUpload}
                />
              </div>
              <p className="text-[10px] text-slate-500 font-bold leading-relaxed">
                Drop uncategorised material here — content is analysed and automatically filed into the matching category above.
              </p>
              {classificationNotices.length > 0 && (
                <ul className="space-y-1.5">
                  {classificationNotices.map((n, i) => (
                    <li key={`${n.filename}-${i}`} className="text-[10px] text-aura font-bold">
                      "{n.filename}" classified as <span className="text-white">{n.label}</span> ({Math.round(n.confidence * 100)}% confidence)
                    </li>
                  ))}
                </ul>
              )}
              {uncategorized.length > 0 && (
                <div className="pt-2 border-t border-slate-800 space-y-1.5">
                  <p className="text-[9px] text-slate-500 font-black uppercase tracking-widest">Unresolved ({uncategorized.length})</p>
                  <ul className="space-y-1.5">
                    {uncategorized.map(f => (
                      <li key={f.file_id} className="flex items-center justify-between gap-2 text-[10px] text-slate-400 font-bold">
                        <span className="truncate">{f.filename}</span>
                        <button type="button" onClick={() => handleDelete(f.file_id)} aria-label={`Remove ${f.filename}`} title={`Remove ${f.filename}`} className="text-slate-600 hover:text-red-400 shrink-0">
                          <Trash2 size={11} />
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })()}
      </div>

      <div className="grid grid-cols-1 @lg:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
            <Globe size={11} /> Company Website
          </label>
          <input
            value={companyWebsite}
            onChange={(e) => setCompanyWebsite(e.target.value)}
            placeholder="https://company.com"
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura"
          />
        </div>
        <div className="space-y-2">
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
            <Linkedin size={11} /> LinkedIn Profile Link
          </label>
          <input
            value={linkedinUrl}
            onChange={(e) => setLinkedinUrl(e.target.value)}
            placeholder="https://linkedin.com/in/your-profile"
            className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura"
          />
        </div>
      </div>

      <div className="space-y-2">
        <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
          <LinkIcon size={11} /> Instructions
        </label>
        <textarea
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
          placeholder="e.g. Targeting a Senior Backend Engineer role, emphasise leadership and distributed systems experience..."
          rows={4}
          className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura resize-none"
        />
      </div>

      <div id="job-search-engine-section" className="space-y-4 p-5 rounded-2xl bg-slate-900 border border-slate-800">
        <div>
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
            <Briefcase size={11} /> Job Search Engine
          </label>
          <p className="text-[10px] text-slate-500 font-bold mt-1 leading-relaxed">
            AI-synthesised example listings — <b>not a live job board</b>. They illustrate the kind of role your materials point to (or your search terms); no listing links to a real advert, and every employer, role and figure must be verified independently before you rely on it.
          </p>
        </div>
        <div className="flex gap-2">
          <input
            value={jobQuery}
            onChange={(e) => setJobQuery(e.target.value)}
            placeholder="Optional: override search terms (e.g. remote senior react developer)"
            className="flex-1 bg-slate-950 border border-slate-800 rounded-2xl p-4 text-xs text-white outline-none focus:border-aura"
            onKeyDown={(e) => { if (e.key === 'Enter') handleJobSearch(); }}
          />
          <Button onClick={handleJobSearch} disabled={jobSearching} className="bg-aura text-sovereign px-5 shrink-0">
            {jobSearching ? <Loader2 className="animate-spin" size={16} /> : <Search size={16} />}
          </Button>
        </div>

        {jobSearchError && <p className="text-[10px] text-red-400 font-bold">{jobSearchError}</p>}

        {jobSearchMeta && (
          <div className="flex flex-wrap items-center gap-2">
            <p className="text-[9px] text-slate-500 font-black uppercase tracking-widest">
              Synthesised {jobSearchMeta.total ?? 0} illustrative listing{jobSearchMeta.total === 1 ? '' : 's'} for "{jobSearchMeta.query}" — no sources searched
            </p>
            {jobSearchMeta.ai_provenance && (() => { const b = provenanceBadge(jobSearchMeta.ai_provenance?.served_by, jobSearchMeta.ai_provenance?.is_external); return <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${b.cls}`} title={b.title}>{b.label}</span>; })()}
          </div>
        )}

        {jobResults && jobResults.length === 0 && (
          <p className="text-[10px] text-slate-600 font-bold">
            {jobSearchMeta?.ai_provenance?.served_by === 'native'
              ? 'No example listings were synthesised — the deterministic native floor served this search and cannot compose listings; an owned model is needed for examples.'
              : 'No example listings were synthesised. Try broadening your terms.'}
          </p>
        )}

        {jobResults && jobResults.length > 0 && (
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
            {jobResults.map(listing => {
              const used = usedListingUrls.includes(listing.listing_id);
              return (
                <div key={listing.listing_id} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="text-xs font-black text-white truncate">{listing.title}</p>
                      <p className="text-[10px] text-slate-400 font-bold flex items-center gap-1.5 mt-0.5">
                        {listing.company} <span className="text-slate-600">·</span>
                        <MapPin size={9} className="inline" /> {listing.location || 'Not specified'}
                        {listing.salary_estimate && <><span className="text-slate-600">·</span> est. {listing.salary_estimate}</>}
                      </p>
                    </div>
                    <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-amber-500/15 text-amber-400 shrink-0" title={listing.basis || 'AI-synthesised example — not a live advert'}>illustrative · no live URL</span>
                  </div>
                  <p className="text-[10px] text-slate-500 leading-relaxed line-clamp-3">{listing.description}</p>
                  {used ? (
                    <span className="inline-flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest text-emerald-400">
                      <CircleCheck size={12} /> Attached as Target Job Ad (illustrative)
                    </span>
                  ) : (
                    <button
                      type="button"
                      onClick={() => handleUseListing(listing)}
                      disabled={usingListingUrl === listing.listing_id}
                      className="flex items-center gap-1.5 px-2.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-aura rounded-lg text-[9px] font-black uppercase tracking-widest transition-colors"
                    >
                      {usingListingUrl === listing.listing_id ? <Loader2 size={11} className="animate-spin" /> : <Target size={11} />}
                      Use as Target Job Ad
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Outputs ({selectedOutputs.length} selected)</label>
          <button type="button" onClick={toggleSelectAllOutputs} className="flex items-center gap-1.5 text-[9px] font-black uppercase tracking-widest text-aura hover:text-white transition-colors">
            {allOutputsSelected ? <CheckSquare size={12} /> : <Square size={12} />}
            {allOutputsSelected ? 'Clear All' : 'Select All'}
          </button>
        </div>
        <div className="grid grid-cols-2 @2xl:grid-cols-4 gap-3">
          {OUTPUT_TYPES.map(o => {
            const active = selectedOutputs.includes(o.id);
            const activeClass = 'p-3 rounded-2xl border flex flex-col items-center gap-2 transition-all bg-aura text-sovereign border-aura';
            const inactiveClass = 'p-3 rounded-2xl border flex flex-col items-center gap-2 transition-all bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700';
            return active ? (
              <button type="button" key={o.id} onClick={() => toggleOutput(o.id)} aria-pressed="true" className={activeClass}>
                <o.icon size={18} />
                <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{o.label}</span>
              </button>
            ) : (
              <button type="button" key={o.id} onClick={() => toggleOutput(o.id)} aria-pressed="false" className={inactiveClass}>
                <o.icon size={18} />
                <span className="text-[8px] font-black uppercase tracking-widest text-center leading-tight">{o.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      <Button onClick={handleGenerate} disabled={generating || selectedOutputs.length === 0} className="w-full bg-white text-sovereign py-6 shadow-2xl shadow-white/5">
        {generating ? <Loader2 className="animate-spin mr-2" /> : <Sparkles className="mr-2" size={18} />}
        {generating ? 'Generating...' : `Generate${selectedOutputs.length > 1 ? ` (${selectedOutputs.length} outputs)` : ''}`}
      </Button>

      {results && (
        <div className="space-y-4 pt-6 border-t border-slate-800">
          {results.map(doc => (
            <div key={doc.output_id} className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between gap-2 flex-wrap">
                <p className="text-xs font-black text-aura uppercase tracking-widest flex items-center gap-2">{doc.title}
                  {/* W454 — every generated document says who served it (it rendered with no provenance) */}
                  {doc.ai_provenance && (() => { const b = provenanceBadge(doc.ai_provenance?.served_by, doc.ai_provenance?.is_external); return <span className={`text-[8px] font-black normal-case tracking-normal px-1.5 py-0.5 rounded ${b.cls}`} title={b.title}>{b.label}</span>; })()}
                </p>
                <button
                  type="button"
                  onClick={() => handleDownload(doc)}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-aura text-sovereign rounded-lg text-[9px] font-black uppercase tracking-widest"
                >
                  <Download size={11} /> Download
                </button>
              </div>
              <pre className="text-[11px] text-slate-300 font-mono whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto bg-slate-950/50 rounded-xl p-4">
                {doc.content}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
