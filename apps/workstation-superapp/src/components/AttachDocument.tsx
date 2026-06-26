import React, { useRef, useState } from 'react';
import { Paperclip, X } from 'lucide-react';

// §9 / §4.1 — "bring your own data": a reusable control to attach a text-based document. The file is read
// in-browser (it never leaves the request) and its content is handed back to the caller as a ready-to-insert
// block, so it flows into whatever field/endpoint the caller already uses (no new POST fields, strict
// domain schemas respected). Used by DomainTool (all 18 domain tools) and Genesis "Describe".
export const TEXT_DOC_EXT = ['.txt', '.md', '.markdown', '.csv', '.tsv', '.json', '.log', '.yaml', '.yml', '.xml', '.html', '.htm'];
const MAX_DOC_BYTES = 200 * 1024; // keep prompts sane; larger files are truncated with a note

// Append a document block to existing field text (blank-line separated).
export function appendDocBlock(existing: string, block: string): string {
  const e = (existing || '').trim();
  return e ? `${e}\n\n${block}` : block;
}

interface AttachDocumentProps {
  onText: (block: string, meta: { name: string; truncated: boolean }) => void;
  hint?: string;
  className?: string;
}

export const AttachDocument: React.FC<AttachDocumentProps> = ({ onText, hint, className }) => {
  const fileRef = useRef<HTMLInputElement>(null);
  const [attached, setAttached] = useState<{ name: string; truncated: boolean } | null>(null);
  const [err, setErr] = useState('');

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (e.target) e.target.value = ''; // allow re-selecting the same file
    if (!file) return;
    setErr('');
    const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
    const looksText = TEXT_DOC_EXT.includes(ext) || file.type.startsWith('text/') || file.type === 'application/json';
    if (!looksText) { setErr(`Unsupported file type. Attach a text document (${TEXT_DOC_EXT.join(', ')}).`); return; }
    const reader = new FileReader();
    reader.onload = () => {
      let text = String(reader.result ?? '');
      const truncated = text.length > MAX_DOC_BYTES;
      if (truncated) text = text.slice(0, MAX_DOC_BYTES) + '\n…[truncated]';
      const block = `--- Attached document: ${file.name} ---\n${text}`;
      const meta = { name: file.name, truncated };
      setAttached(meta);
      onText(block, meta);
    };
    reader.onerror = () => setErr('Could not read the file.');
    reader.readAsText(file);
  };

  return (
    <div className={`space-y-1.5 ${className ?? ''}`}>
      <input ref={fileRef} type="file" onChange={onChange}
        accept={[...TEXT_DOC_EXT, 'text/*', 'application/json'].join(',')} className="hidden" aria-hidden="true" tabIndex={-1} />
      <div className="flex items-center gap-2 flex-wrap">
        <button type="button" onClick={() => fileRef.current?.click()}
          className="text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white flex items-center gap-1.5">
          <Paperclip size={11} /> Attach document
        </button>
        {attached && (
          <span className="text-[9px] font-bold text-aura flex items-center gap-1.5 bg-aura/10 px-2 py-1 rounded-lg">
            {attached.name}{attached.truncated ? ' (truncated)' : ''}
            <button type="button" aria-label="Clear attached note" onClick={() => setAttached(null)} className="text-slate-500 hover:text-white"><X size={10} /></button>
          </span>
        )}
        <span className="text-[9px] text-slate-600">{hint ?? 'your own data — read in-browser, stays with this request'}</span>
      </div>
      {err && <p className="text-[9px] text-amber-400 font-bold">{err}</p>}
    </div>
  );
};
