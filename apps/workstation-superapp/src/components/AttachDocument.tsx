import React, { useRef, useState } from 'react';
import { Paperclip, X } from 'lucide-react';

// §9 / §4.1 — "bring your own data": a reusable control to attach a text-based document. The file is read
// in-browser (it never leaves the request) and its content is handed back to the caller as a ready-to-insert
// block, so it flows into whatever field/endpoint the caller already uses (no new POST fields, strict
// domain schemas respected). Used by DomainTool (all 18 domain tools) and Genesis "Describe".
export const TEXT_DOC_EXT = ['.txt', '.md', '.markdown', '.csv', '.tsv', '.json', '.log', '.yaml', '.yml', '.xml', '.html', '.htm'];
const MAX_DOC_BYTES = 200 * 1024; // keep prompts sane; larger files are truncated with a note

// §4.1 (W429) — PDFs, extracted IN THE BROWSER. A research report is the spec's own first example of
// "uploaded data" and is normally a PDF, so it could not be attached at all.
//
// Deliberately not a server upload endpoint: this control's defining property is that the file never
// leaves the machine, and a server route would trade that away for convenience. Measured cost of
// keeping it (spiked before writing this): the main bundle stays at 1.96 MB because pdfjs loads via
// dynamic import() — a separate 0.35 MB chunk plus a 1.31 MB worker, both emitted as LOCAL hashed
// assets with no CDN reference, and fetched only when someone actually attaches a PDF.
export const PDF_DOC_EXT = ['.pdf'];

async function extractPdfText(file: File): Promise<{ text: string; pages: number; pagesWithText: number }> {
  // Both imports are dynamic so nothing here is in the initial bundle. `?url` makes Vite emit the
  // worker as a local asset and hand back its path — the alternative (letting pdf.js resolve its own
  // worker) fetches from a CDN, which would break the never-leaves-the-browser guarantee.
  const [pdfjs, workerUrl] = await Promise.all([
    import('pdfjs-dist'),
    import('pdfjs-dist/build/pdf.worker.min.mjs?url').then(m => m.default),
  ]);
  pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;
  const doc = await pdfjs.getDocument({ data: await file.arrayBuffer() }).promise;
  const parts: string[] = [];
  let pagesWithText = 0;
  for (let i = 1; i <= doc.numPages; i++) {
    const tc = await (await doc.getPage(i)).getTextContent();
    const page = tc.items.map((it: any) => ('str' in it ? it.str : '')).join(' ').trim();
    if (page) pagesWithText++;
    parts.push(page);
    if (parts.join(NEWLINE).length > MAX_DOC_BYTES) break;   // stop early rather than read a 400-page book
  }
  return { text: parts.join(NEWLINE).trim(), pages: doc.numPages, pagesWithText };
}

const NEWLINE = String.fromCharCode(10);

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
  const [busy, setBusy] = useState(false);   // a PDF takes real time; a silent pause reads as broken

  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (e.target) e.target.value = ''; // allow re-selecting the same file
    if (!file) return;
    setErr('');
    const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();

    // §4.1 (W429) — PDFs are extracted here, before the text-format refusal below.
    if (ext === '.pdf' || file.type === 'application/pdf') {
      setBusy(true);
      try {
        const { text, pages, pagesWithText } = await extractPdfText(file);
        if (!text) {
          // A scanned or image-only PDF has NO text layer. Attaching an empty document — or a
          // cheerful "attached" chip over nothing — would be a small lie about what was read.
          setErr(`No text layer in ${file.name} (${pages} page${pages === 1 ? '' : 's'}). It looks scanned `
                 + `or image-only, so there is nothing to extract in the browser. Paste the text instead.`);
          return;
        }
        const truncated = text.length > MAX_DOC_BYTES;
        const body = truncated ? text.slice(0, MAX_DOC_BYTES) + NEWLINE + '…[truncated]' : text;
        // The header states what was actually read, so a partial extraction is never presented as
        // the whole document.
        const block = `--- Attached document: ${file.name} (PDF text layer, `
          + `${pagesWithText}/${pages} page${pages === 1 ? '' : 's'} with text) ---` + NEWLINE + body;
        const meta = { name: file.name, truncated };
        setAttached(meta);
        onText(block, meta);
      } catch {
        setErr(`Could not read ${file.name}. If it is password-protected or damaged, paste the text instead.`);
      } finally {
        setBusy(false);
      }
      return;
    }

    const looksText = TEXT_DOC_EXT.includes(ext) || file.type.startsWith('text/') || file.type === 'application/json';
    if (!looksText) { setErr(`Unsupported file type. Attach a text document (${TEXT_DOC_EXT.join(', ')}) or a PDF.`); return; }
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
        accept={[...TEXT_DOC_EXT, ...PDF_DOC_EXT, 'text/*', 'application/json', 'application/pdf'].join(',')}
        className="hidden" aria-hidden="true" tabIndex={-1} />
      <div className="flex items-center gap-2 flex-wrap">
        <button type="button" onClick={() => fileRef.current?.click()} disabled={busy}
          className="text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-50 flex items-center gap-1.5">
          <Paperclip size={11} /> {busy ? 'Reading PDF…' : 'Attach document'}
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
