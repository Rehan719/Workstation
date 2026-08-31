import React, { useEffect, useState } from 'react';
import { downloadExport } from '../../lib/download';
import axios from 'axios';
import { Card, Button, Badge } from '@workstation/ui';
import { Building2, Crown, Users, Target, ShieldCheck, Workflow, Loader2, Play, Boxes, ScrollText, MessageCircle, Send, Coins, Mic, Volume2, Paperclip, Download } from 'lucide-react';

// The VSB Enterprise Cockpit — interact with a generated living VSB IDBO Enterprise: its
// organisational structure, the Chief's digital twin + Board, the living business plan
// (vision / strategy / aims / objectives / roadmap), the living management systems (BMS/QMS/DCS/EMS),
// and a one-click end-to-end transformation run (Chief → Build-to-Order + products/services catalogue).
// All data is live from the in-house backend; nothing is fabricated.

interface VSBRow { vsb_id: string; name?: string; domain?: string; has_board?: boolean; entity_type?: string }
type Dict = Record<string, any>;

const TABS = [
  ['org', 'Organisation', Building2],
  ['chief', 'Chief & Board', Crown],
  ['plan', 'Business Plan', Target],
  ['deliverables', 'Deliverables', ScrollText],
  ['systems', 'Living Systems', ShieldCheck],
  ['economy', 'Economy', Coins],
  ['transform', 'Transformation', Workflow],
  ['chat', 'Converse', MessageCircle],
] as const;

interface ChatMsg { role: 'you' | 'vsb'; text: string; served_by?: string; is_external?: boolean; attached?: boolean; image_understood?: boolean; image_served_by?: string | null; image_is_external?: boolean }

export const VSBCockpit: React.FC = () => {
  const [vsbs, setVsbs] = useState<VSBRow[]>([]);
  const [vsbFilter, setVsbFilter] = useState('');
  const [selected, setSelected] = useState<string>('');
  const [detail, setDetail] = useState<Dict | null>(null);
  const [plan, setPlan] = useState<Dict | null>(null);
  const [objOrch, setObjOrch] = useState('');                 // objective id being delivered by the Chief
  const [objOrchResult, setObjOrchResult] = useState<Dict>({}); // tree result per objective id
  const [deliverables, setDeliverables] = useState<Dict[]>([]); // this VSB's living outputs (§13)
  const [delivType, setDelivType] = useState('report');
  const [delivBrief, setDelivBrief] = useState('');
  const [delivProducing, setDelivProducing] = useState(false);
  const [delivFormat, setDelivFormat] = useState('md');
  const [delivFormats, setDelivFormats] = useState<{ id: string; label: string }[]>([{ id: 'md', label: 'Markdown (.md)' }]);
  const [standards, setStandards] = useState<Dict[]>([]);
  const [tab, setTab] = useState<string>('org');
  const [loading, setLoading] = useState(false);
  const [tx, setTx] = useState<Dict | null>(null);
  const [txRunning, setTxRunning] = useState(false);
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [chatting, setChatting] = useState(false);
  const [pendingImage, setPendingImage] = useState<{ b64: string; name: string } | null>(null);
  const [chatLang, setChatLang] = useState('');   // '' = English; otherwise respond in this language
  const [ledger, setLedger] = useState<Dict | null>(null);
  const [lastCycle, setLastCycle] = useState<Dict | null>(null);
  const [cycling, setCycling] = useState(false);
  const [btoComponents, setBtoComponents] = useState<Dict[]>([]);
  const [btoSel, setBtoSel] = useState<string[]>(['vsb', 'csuite', 'coe', 'domains']);
  const [btoBlueprint, setBtoBlueprint] = useState<Dict | null>(null);
  const [btoBusy, setBtoBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const [speakReplies, setSpeakReplies] = useState(false);
  const recognitionRef = React.useRef<any>(null);
  // Browser-native multimodal — speech-to-text in / text-to-speech out, fully in-house (no external API).
  const SpeechRec: any = typeof window !== 'undefined' ? ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition) : null;
  const canSpeak = typeof window !== 'undefined' && 'speechSynthesis' in window;

  useEffect(() => {
    axios.get('/api/v1/vsb').then(r => {
      const ents: VSBRow[] = r.data.entities || [];
      setVsbs(ents);
      // Honour a ?vsb=<id> deep-link (e.g. "Open in Cockpit" from the Spawn Studio); else prefer an established VSB.
      const want = new URLSearchParams(window.location.search).get('vsb');
      const chosen = (want && ents.find(e => e.vsb_id === want)) || ents.find(e => e.has_board) || ents[0];
      if (chosen) setSelected(chosen.vsb_id);
    }).catch(() => {});
    axios.get('/api/v1/mgmt/standards').then(r => setStandards(r.data.standards || [])).catch(() => {});
    axios.get('/api/v1/bto/components').then(r => setBtoComponents(r.data.components || [])).catch(() => {});
    axios.get('/api/v1/deliverables/output-formats').then(r => {
      if (Array.isArray(r.data?.live) && r.data.live.length) setDelivFormats(r.data.live.map((f: any) => ({ id: f.id, label: f.label })));
    }).catch(() => {});
  }, []);

  // §13 (W338) — drift honesty reaches the USER: the shipped-body manifest (stale flag + reason)
  // is read on selection and after every ship — previously no UI ever read the stale flag, so a
  // drifted shipped body was invisible end-to-end.
  const [shipState, setShipState] = useState<Dict | null>(null);
  const loadShipState = (vid: string) =>
    axios.get(`/api/v1/vsb/${vid}/repo/ship`).then(r => setShipState(r.data))
      .catch(() => setShipState(null));   // 404 = never shipped — honestly nothing to show

  useEffect(() => {
    if (!selected) return;
    setLoading(true); setTx(null); setMessages([]); setLastCycle(null);
    Promise.all([
      axios.get(`/api/v1/vsb/${selected}`).then(r => r.data).catch(() => null),
      axios.get('/api/v1/business-plan', { params: { scope: selected } }).then(r => r.data).catch(() => null),
      axios.get(`/api/v1/economy/ledger/${selected}`).then(r => r.data).catch(() => null),
    ]).then(([d, p, l]) => { setDetail(d); setPlan(p); setLedger(l); setLoading(false); });
    loadDeliverables(selected);
    loadShipState(selected);
  }, [selected]);

  // W299 — the §13 GROWTH machinery reaches the user for THEIR entity (repo ship · repo cascade ·
  // evolve had zero UI callers); W300 — instruct THEIR Chief (apex delegation scoped to this VSB).
  const [growthBusy, setGrowthBusy] = useState('');
  const [actErr, setActErr] = useState('');   // W344 — actions never fail silently
  const [growthResult, setGrowthResult] = useState<Dict | null>(null);
  const [chiefText, setChiefText] = useState('');
  const [chiefBusy, setChiefBusy] = useState(false);
  const [chiefResult, setChiefResult] = useState<Dict | null>(null);

  const runGrowth = async (kind: 'ship' | 'cascade' | 'evolve') => {
    if (!selected) return;
    setGrowthBusy(kind); setGrowthResult(null);
    try {
      const url = kind === 'ship' ? `/api/v1/vsb/${selected}/repo/ship`
        : kind === 'cascade' ? `/api/v1/vsb/${selected}/repo/cascade`
        : `/api/v1/vsb/${selected}/evolve`;
      const body = kind === 'evolve' ? { trigger: 'cockpit' } : {};
      const r = await axios.post(url, body);
      setGrowthResult({ kind, ...r.data });
      loadShipState(selected);   // W338 — the staleness banner reflects the ship immediately
    } catch (e: any) {
      setGrowthResult({ kind, error: e?.response?.data?.detail ?? e?.message ?? 'failed' });
    }
    setGrowthBusy('');
  };

  const instructChief = async () => {
    if (!selected || !chiefText.trim()) return;
    setChiefBusy(true); setChiefResult(null);
    try {
      const r = await axios.post('/api/v1/board/chief/instruct', {
        instruction: chiefText, owner: detail?.owner_id || 'the founder',
        scope: selected, cascade_to_ceo: true,
      });
      setChiefResult(r.data);
      setChiefText('');
    } catch (e: any) {
      setChiefResult({ error: e?.response?.data?.detail ?? e?.message ?? 'failed' });
    }
    setChiefBusy(false);
  };

  const runTransformation = async () => {
    if (!selected) return;
    setTxRunning(true); setTx(null);
    try {
      const objective = plan?.mission || detail?.challenge || `Advance ${detail?.name || 'the venture'}`;
      const r = await axios.post('/api/v1/transformation/orchestrate',
        { objective, scope: selected, owner_id: detail?.owner_id || 'Owner', deep: false });
      setTx(r.data);
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setTxRunning(false);
  };

  // The Chief delivers a single objective via the autonomous in-house workflow TREE — grounded in THIS
  // VSB (scope=selected), governed + sealed into the UEG chain. Mirrors the Business Plan page action.
  const orchestrateObjective = async (oid: string) => {
    if (!selected) return;
    setObjOrch(oid);
    try {
      const r = await axios.post(`/api/v1/business-plan/objective/${oid}/orchestrate`, { scope: selected });
      if (r.data?.tree) setObjOrchResult(m => ({ ...m, [oid]: r.data.tree }));
      else setActErr('Orchestration ran but returned no delivery tree.');
    } catch (e: any) { setActErr(`Orchestration failed: ${e?.response?.data?.detail ?? 'backend unreachable'}`); }
    setObjOrch('');
  };

  // This VSB's living deliverables (§13) — its actual outputs, produced on the native fabric and
  // exportable in any of the in-house formats.
  const loadDeliverables = (vid: string) =>
    axios.get('/api/v1/deliverables', { params: { vsb_id: vid } })
      .then(r => setDeliverables(r.data.deliverables || [])).catch(() => setDeliverables([]));

  const produceDeliverable = async () => {
    if (!selected || !delivBrief.trim()) return;
    setDelivProducing(true);
    try {
      await axios.post('/api/v1/deliverables/produce', { type: delivType, brief: delivBrief, vsb_id: selected });
      setDelivBrief('');
      await loadDeliverables(selected);
    } catch (e: any) { setActErr(`Produce failed: ${e?.response?.data?.detail ?? 'backend unreachable'}`); }
    setDelivProducing(false);
  };

  const speak = (text: string) => {
    if (!speakReplies || !canSpeak || !text) return;
    try { window.speechSynthesis.cancel(); window.speechSynthesis.speak(new SpeechSynthesisUtterance(text.slice(0, 600))); } catch { /* ignore */ }
  };

  const sendChat = async (override?: string) => {
    const msg = (override ?? chatInput).trim();
    if ((!msg && !pendingImage) || chatting || !selected) return;
    const img = pendingImage;
    setMessages(m => [...m, { role: 'you', text: msg || '(image)', attached: !!img }]);
    setChatInput(''); setPendingImage(null); setChatting(true);
    try {
      const body: Record<string, any> = { message: msg || 'What is in this image?', context: 'vsb', vsb_id: selected };
      if (img) body.image_base64 = img.b64;
      if (chatLang) body.language = chatLang;
      const r = await axios.post('/api/v1/avatar/chat', body);
      const reply = r.data.response || '(no response)';
      setMessages(m => [...m, { role: 'vsb', text: reply, served_by: r.data.served_by, is_external: r.data.is_external,
                               image_understood: r.data.image_understood, image_served_by: r.data.image_served_by, image_is_external: r.data.image_is_external }]);
      speak(reply);
    } catch {
      setMessages(m => [...m, { role: 'vsb', text: 'The enterprise avatar is unavailable right now.', is_external: false }]);
    }
    setChatting(false);
  };

  const attachImage = (file?: File) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = String(reader.result || '');
      const b64 = dataUrl.includes(',') ? dataUrl.split(',')[1] : dataUrl;   // strip data: prefix
      if (b64) setPendingImage({ b64, name: file.name });
    };
    reader.readAsDataURL(file);
  };

  const listenVoice = () => {
    if (!SpeechRec) return;
    if (listening) { try { recognitionRef.current?.stop(); } catch { /* ignore */ } return; }
    const rec = new SpeechRec();
    recognitionRef.current = rec;
    rec.lang = 'en-GB'; rec.interimResults = false; rec.maxAlternatives = 1;
    rec.onresult = (e: any) => {
      const transcript = e.results?.[0]?.[0]?.transcript || '';
      if (transcript) { setChatInput(transcript); sendChat(transcript); }   // speak → transcribe → send
    };
    rec.onend = () => setListening(false);
    rec.onerror = () => setListening(false);
    try { rec.start(); setListening(true); } catch { setListening(false); }
  };

  const runCycle = async () => {
    if (!selected || cycling) return;
    setCycling(true);
    try {
      const r = await axios.post('/api/v1/economy/cycle', { vsb_id: selected });
      setLastCycle(r.data.cycle || null);
      const l = await axios.get(`/api/v1/economy/ledger/${selected}`).then(x => x.data).catch(() => null);
      if (l) setLedger(l);
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setCycling(false);
  };

  const configureBto = async () => {
    if (btoBusy) return;
    setBtoBusy(true);
    try {
      const r = await axios.post('/api/v1/bto/configure',
        { entity_name: detail?.name || 'Enterprise', components: btoSel, product_resources: [] });
      setBtoBlueprint(r.data);
    } catch { setActErr('Action failed — backend unreachable; nothing changed.'); }   // W344
    setBtoBusy(false);
  };

  const board = detail?.board || {};
  const economy = detail?.economy || {};
  const waterfall: Dict = economy.waterfall || {};
  const chief = board.chief || {};
  const directors: Dict[] = board.directors || [];
  const swarm = detail?.native_swarm || {};

  return (
    <div className="space-y-8 pb-24">
      {actErr && <p className="text-vital text-xs font-bold">{actErr}</p>}
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">IDBO · Living VSB Enterprise</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">VSB Cockpit</h1>
        <p className="text-slate-500 font-bold mt-2 max-w-2xl leading-relaxed">
          Interact with a generated living VSB IDBO Enterprise — its organisational structure, the Chief's
          digital twin &amp; Board, the living business plan, the management systems (BMS · QMS · DCS · EMS),
          and an end-to-end transformation run. All live from Workstation's <span className="text-highlight">own</span> in-house systems.
        </p>
      </header>

      {/* VSB selector — searchable (the established-VSB list can grow large) */}
      {(() => {
        const q = vsbFilter.trim().toLowerCase();
        // W394 — this store holds 1,552 entities across only 45 distinct names, so the list was
        // rendered in raw API order and the entity you just created sat hundreds of rows down a
        // 1,552-option <select>. Newest first, and only a capped window is rendered: a dropdown with
        // fifteen hundred children is not a chooser, it is a wall.
        const recent = [...vsbs].sort((a, b) => {
          const ts = (v: VSBRow) => {
            const c: unknown = (v as unknown as { created_at?: unknown }).created_at;
            if (typeof c === 'number') return c;
            const parsed = Date.parse(String(c ?? ''));
            return Number.isNaN(parsed) ? 0 : parsed;
          };
          return ts(b) - ts(a);
        });
        const filtered = q
          ? recent.filter(v => `${v.name || ''} ${v.domain || ''} ${v.entity_type || ''} ${v.vsb_id}`.toLowerCase().includes(q))
          : recent;
        const OPTION_CAP = 50;
        const capped = filtered.slice(0, OPTION_CAP);
        const hiddenCount = filtered.length - capped.length;
        // keep the current selection selectable even if filtered or capped out
        const options = (selected && !capped.some(v => v.vsb_id === selected))
          ? [...capped, ...vsbs.filter(v => v.vsb_id === selected)]
          : capped;
        // W393 — with no established VSB the whole page is inert: `detail` is null, so nothing below
        // renders, and the only guidance used to be an UNSELECTABLE <option> inside a dropdown —
        // text that tells you to go somewhere and does nothing when you click it. Give the dead end
        // a real way out instead.
        if (!loading && vsbs.length === 0) {
          return (
            <Card className="p-8 text-center border-dashed border-slate-800">
              <Building2 size={26} className="mx-auto text-slate-700 mb-3" />
              <p className="text-slate-300 font-black uppercase tracking-widest text-xs mb-2">
                No established VSB enterprises yet
              </p>
              <p className="text-slate-500 text-xs font-semibold max-w-md mx-auto leading-relaxed mb-5">
                The cockpit operates a living VSB IDBO enterprise — its Board, business plan and
                management systems. Establish one first and it will appear here.
              </p>
              <div className="flex gap-2 justify-center flex-wrap">
                <Button type="button" onClick={() => { window.location.href = '/vsb-spawn'; }}>
                  Open VSB Spawn Studio
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => { window.location.href = '/genesis'; }}
                  className="border-slate-800 text-slate-400"
                >
                  Start a Genesis journey
                </Button>
              </div>
            </Card>
          );
        }
        return (
          <Card className="p-5 flex items-center gap-3 flex-wrap">
            <Building2 size={18} className="text-highlight shrink-0" />
            {vsbs.length > 8 && (
              <input aria-label="Filter VSBs" value={vsbFilter} onChange={e => setVsbFilter(e.target.value)}
                placeholder="Filter by name, domain, type, id…"
                className="min-w-[180px] bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-300" />
            )}
            <select aria-label="Select VSB" value={selected} onChange={e => setSelected(e.target.value)}
              className="flex-1 min-w-[240px] bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white">
              {vsbs.length === 0 && <option value="">No established VSBs yet — spawn one in the VSB Spawn Studio</option>}
              {vsbs.length > 0 && options.length === 0 && <option value="">No VSB matches “{vsbFilter}”</option>}
              {options.map(v => <option key={v.vsb_id} value={v.vsb_id}>{v.name || v.vsb_id}{v.domain ? ` · ${v.domain}` : ''}{v.has_board ? ' ✓' : ''}</option>)}
            </select>
            {vsbs.length > 8 && (
              // Never truncate silently: a capped list that looks complete is worse than a long one.
              <span className="text-[10px] font-black uppercase text-slate-500 shrink-0">
                {hiddenCount > 0
                  ? `newest ${capped.length} of ${filtered.length}${q ? '' : ` · ${vsbs.length} total`} — filter to narrow`
                  : q ? `${filtered.length} of ${vsbs.length}` : `${vsbs.length} VSBs`}
              </span>
            )}
            {loading && <Loader2 size={16} className="animate-spin text-highlight" />}
          </Card>
        );
      })()}

      {detail && (
        <>
          <div className="flex gap-2 flex-wrap p-1 rounded-2xl bg-slate-900 border border-slate-800 w-fit">
            {TABS.map(([id, label, Icon]) => (
              <button key={id} type="button" onClick={() => setTab(id)}
                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all flex items-center gap-2 ${tab === id ? 'bg-slate-800 text-highlight shadow-lg' : 'text-slate-500 hover:text-white'}`}>
                <Icon size={13} /> {label}
              </button>
            ))}
          </div>

          {/* Organisation */}
          {tab === 'org' && (
            <div className="space-y-4">
              <Card className="p-6 space-y-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h3 className="text-lg font-black text-white">{detail.name}</h3>
                  <div className="flex gap-2">
                    {detail.domain && <Badge color="highlight">{detail.domain}</Badge>}
                    {detail.status && <Badge color="emerald-500">{detail.status}</Badge>}
                    {detail.stage && <Badge color="aura">{detail.stage}</Badge>}
                  </div>
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed">{detail.challenge}</p>
                <p className="text-[9px] font-mono text-slate-600">{detail.vsb_id} · realm: {detail.realm} · owner: {detail.owner_id}</p>
              </Card>
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2"><Workflow size={14} /> Organisational hierarchy (apex → operational delivery)</h4>
                <div className="flex flex-wrap items-center gap-2 text-[10px] font-black uppercase tracking-wider">
                  {['Chief of Board', 'Board of Directors', 'AI CEO', 'C-Suite', 'Centres of Excellence', 'Business Transformation Office', 'Build-to-Order'].map((t, i, a) => (
                    <React.Fragment key={t}>
                      <span className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">{t}</span>
                      {i < a.length - 1 && <span className="text-highlight">→</span>}
                    </React.Fragment>
                  ))}
                </div>
                {swarm.org && (
                  <p className="text-[10px] text-slate-500 mt-4">Native delivery swarm: <span className="text-aura font-bold">{swarm.name || swarm.cascade_id}</span> · {(swarm.stages || []).length} stages · posture {swarm.posture || 'in-house'}</p>
                )}
              </Card>
            </div>
          )}

          {/* Chief & Board */}
          {tab === 'chief' && (
            <div className="space-y-4">
              {/* W300 — instruct THIS entity's Chief: apex delegation scoped to the VSB's own plan */}
              <Card className="p-6 space-y-3 border-highlight/30 bg-highlight/5">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight flex items-center gap-2"><Crown size={14} /> Instruct this entity's Chief</h4>
                <textarea value={chiefText} onChange={e => setChiefText(e.target.value)} rows={2}
                  placeholder="Give the Chief an instruction — it lands as objectives on THIS entity's living plan and cascades to its AI CEO."
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50 resize-none" />
                <Button type="button" onClick={instructChief} disabled={chiefBusy || !chiefText.trim()}
                  className="bg-highlight text-sovereign text-xs flex items-center gap-2">
                  {chiefBusy ? <Loader2 size={13} className="animate-spin" /> : <Crown size={13} />} Issue instruction
                </Button>
                {chiefResult && (
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-[11px] text-slate-300 space-y-1">
                    {chiefResult.error ? <p className="text-vital">{String(chiefResult.error)}</p> : (
                      <>
                        <p className="text-emerald-400 font-bold">{chiefResult.objectives_added ?? 0} objective(s) landed on this entity's plan · gaas: {chiefResult.governance?.status ?? '—'}</p>
                        <p className="whitespace-pre-wrap line-clamp-6">{chiefResult.chief_directive}</p>
                      </>
                    )}
                  </div>
                )}
              </Card>
              <Card className="p-6 space-y-2 border-aura/30">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-aura flex items-center gap-2"><Crown size={14} /> Chief of the Board (Owner's digital twin)</h4>
                <p className="text-white font-black">{chief.title || chief.name || `Chief — Digital Twin of ${board.owner || detail.owner_id}`}</p>
                {chief.role && <p className="text-[11px] text-slate-500">{chief.role}</p>}
                {board.vision_summary && <p className="text-[11px] text-slate-400 leading-relaxed mt-2">{board.vision_summary}</p>}
                {board.governance && <p className="text-[9px] font-mono text-slate-600 mt-2">{typeof board.governance === 'string' ? board.governance : JSON.stringify(board.governance)}</p>}
              </Card>
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Users size={14} /> Board of Directors ({directors.length})</h4>
                <div className="grid grid-cols-1 @[560px]:grid-cols-2 gap-3">
                  {directors.length === 0 && <p className="text-slate-600 text-xs">No directors recorded.</p>}
                  {directors.map((d, i) => (
                    <div key={i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <p className="font-black text-white text-sm">{d.title || d.name || d.role || `Director ${i + 1}`}</p>
                      {(d.specialism || d.theme || d.focus) && <p className="text-[10px] text-slate-500 mt-1">{d.specialism || d.theme || d.focus}</p>}
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}

          {/* Business Plan */}
          {tab === 'plan' && plan && (
            <div className="space-y-4">
              {/* Chief's Opening (W91/W93) — Executive Summary · Concept · Vision, seeded from the Genesis journey */}
              {(plan.executive_summary || plan.concept || plan.vision) && (
                <Card className="p-6 border-highlight/40 bg-gradient-to-br from-highlight/10 to-transparent">
                  <div className="flex items-center gap-2 mb-3">
                    <Crown size={15} className="text-highlight" />
                    <h4 className="text-[10px] font-black uppercase tracking-widest text-white">Chief’s Opening — Executive Summary · Concept · Vision</h4>
                  </div>
                  {([['Executive Summary', plan.executive_summary], ['Concept', plan.concept], ['Vision', plan.vision]] as [string, string][])
                    .filter(([, v]) => v).map(([label, val]) => (
                    <div key={label} className="mb-3 last:mb-0">
                      <p className="text-[9px] font-black uppercase tracking-widest text-highlight/70 mb-1">{label}</p>
                      <p className="text-sm text-slate-300 leading-relaxed">{val}</p>
                    </div>
                  ))}
                </Card>
              )}
              {[['Mission', plan.mission], ['Strategy', plan.strategy]].map(([label, val]) => (
                <Card key={label as string} className="p-6">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-2">{label}</h4>
                  <p className="text-sm text-slate-300 leading-relaxed">{(val as string) || <span className="text-slate-600">Not set.</span>}</p>
                </Card>
              ))}
              {Array.isArray(plan.aims) && plan.aims.length > 0 && (
                <Card className="p-6">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-2">Aims</h4>
                  <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">{plan.aims.map((a: string, i: number) => <li key={i}>{a}</li>)}</ul>
                </Card>
              )}
              {plan.roadmap && plan.roadmap.phases?.length > 0 && (
                <Card className="p-6 border-highlight/30">
                  <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
                    <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight flex items-center gap-2"><Workflow size={14} /> Living roadmap</h4>
                    <span className="text-[9px] font-black uppercase text-slate-500">overall {plan.roadmap.overall_progress_pct}% · current: {plan.roadmap.current_phase || '—'}</span>
                  </div>
                  <div className="space-y-3">
                    {plan.roadmap.phases.map((ph: Dict, i: number) => (
                      <div key={i} className={`p-3 rounded-xl border ${ph.timeline === plan.roadmap.current_phase ? 'bg-highlight/5 border-highlight/40' : 'bg-slate-900 border-slate-800'}`}>
                        <div className="flex items-center justify-between gap-2">
                          <p className="text-[11px] font-black uppercase tracking-wider text-white">{ph.timeline}</p>
                          <span className="text-[9px] font-black text-highlight">{ph.progress_pct}% · {ph.count} objective{ph.count === 1 ? '' : 's'}{ph.complete ? ' ✓' : ''}</span>
                        </div>
                        <div className="mt-2 h-1.5 rounded-full bg-slate-800 overflow-hidden"><div className="h-full bg-highlight" style={{ width: `${ph.progress_pct}%` }} /></div>
                        <div className="mt-2 flex flex-wrap gap-1.5">
                          {(ph.objectives || []).map((o: Dict, j: number) => <span key={j} className="text-[9px] text-slate-400">· {o.title}</span>)}
                        </div>
                      </div>
                    ))}
                  </div>
                  {plan.roadmap.next_milestone && <p className="text-[10px] text-slate-500 mt-3">Next milestone: <span className="text-white font-bold">{plan.roadmap.next_milestone.title}</span> ({plan.roadmap.next_milestone.phase})</p>}
                  <p className="text-[9px] text-slate-600 italic mt-2">{plan.roadmap.note}</p>
                </Card>
              )}
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-3">Objectives ({(plan.objectives || []).length})</h4>
                <div className="space-y-3">
                  {(plan.objectives || []).map((o: Dict, i: number) => (
                    <div key={o.id || i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="flex items-center justify-between gap-2 flex-wrap">
                        <p className="font-black text-white text-sm">{o.title}</p>
                        <div className="flex items-center gap-2">
                          {o.timeline && <span className="text-[9px] font-black uppercase text-slate-500">{o.timeline}</span>}
                          {o.status && <Badge color={o.status === 'done' ? 'emerald-500' : 'aura'}>{o.status}</Badge>}
                        </div>
                      </div>
                      <div className="mt-2 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div className="h-full bg-highlight" style={{ width: `${Math.max(0, Math.min(100, o.progress_pct || 0))}%` }} />
                      </div>
                      <button type="button" onClick={() => orchestrateObjective(o.id)} disabled={objOrch === o.id}
                        className="mt-2 text-[9px] font-black uppercase tracking-widest text-aura border border-aura/30 px-2 py-1 rounded flex items-center gap-1 disabled:opacity-50">
                        {objOrch === o.id ? <Loader2 size={10} className="animate-spin" /> : <Crown size={10} />} Chief: deliver via tree
                      </button>
                      {objOrchResult[o.id] && (
                        <div className="mt-2 p-2 rounded-lg bg-aura/5 border border-aura/20">
                          <div className="flex items-center flex-wrap gap-1.5">
                            <span className="text-[8px] font-black uppercase tracking-widest text-aura">Chief workflow-tree</span>
                            <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-highlight/15 text-highlight">decision: {objOrchResult[o.id].decision?.recommendation ?? '—'}</span>
                            <span className={`text-[8px] font-black uppercase px-1.5 py-0.5 rounded ${objOrchResult[o.id].consensus?.choice === 'proceed' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>consensus: {objOrchResult[o.id].consensus?.choice ?? 'none'}</span>
                            <span className="text-[8px] font-black uppercase px-1.5 py-0.5 rounded bg-slate-900 text-slate-400">{objOrchResult[o.id].node_count} nodes</span>
                            {objOrchResult[o.id].ueg_hash && <span className="text-[8px] font-mono text-slate-600" title={objOrchResult[o.id].ueg_hash}>UEG {String(objOrchResult[o.id].ueg_hash).slice(0, 12)}…</span>}
                          </div>
                          {objOrchResult[o.id].final && <p className="text-[10px] text-slate-400 whitespace-pre-wrap line-clamp-3 mt-1">{objOrchResult[o.id].final}</p>}
                        </div>
                      )}
                    </div>
                  ))}
                  {(plan.objectives || []).length === 0 && <p className="text-slate-600 text-xs">No objectives yet.</p>}
                </div>
              </Card>
            </div>
          )}

          {/* Deliverables — this VSB's living outputs (§13), exportable in any in-house format */}
          {tab === 'deliverables' && (
            <div className="space-y-4">
              <Card className="p-6">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-3 flex items-center gap-2"><ScrollText size={14} /> Produce a living deliverable for this VSB</h4>
                <div className="grid grid-cols-1 @[560px]:grid-cols-4 gap-2 mb-2">
                  <select value={delivType} onChange={e => setDelivType(e.target.value)} aria-label="Deliverable type" className="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-slate-300">
                    {['report', 'presentation', 'website', 'brief', 'service', 'app_spec'].map(t => <option key={t} value={t}>{t}</option>)}
                  </select>
                  <input value={delivBrief} onChange={e => setDelivBrief(e.target.value)} placeholder="Brief — what should it cover?" className="bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-sm text-white @[560px]:col-span-2" />
                  <Button onClick={produceDeliverable} disabled={delivProducing || !delivBrief.trim()} className="bg-highlight text-sovereign text-xs flex items-center gap-2">
                    {delivProducing ? <Loader2 size={14} className="animate-spin" /> : <ScrollText size={14} />} Produce
                  </Button>
                </div>
                <p className="text-[9px] text-slate-600">Produced on Workstation’s own native AI fabric (honest in-house provenance) and filed under this VSB.</p>
              </Card>
              <Card className="p-6">
                <div className="flex items-center justify-between gap-2 flex-wrap mb-3">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight">Outputs ({deliverables.length})</h4>
                  <select value={delivFormat} onChange={e => setDelivFormat(e.target.value)} aria-label="Export format" className="text-[10px] bg-slate-950 border border-slate-800 rounded-lg p-1.5 text-slate-300">
                    {delivFormats.map(f => <option key={f.id} value={f.id}>{f.label}</option>)}
                  </select>
                </div>
                <div className="space-y-2">
                  {deliverables.map((d: Dict) => (
                    <div key={d.id} className="flex items-center justify-between gap-2 p-3 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="min-w-0">
                        <p className="text-sm font-black text-white truncate">{d.title}</p>
                        <p className="text-[9px] text-slate-500 uppercase tracking-widest">{d.type} · {d.versions} version{d.versions === 1 ? '' : 's'} · {d.served_by || 'native'}</p>
                      </div>
                      {/* W338 — bearer-carrying export (a raw anchor 401s under auth) */}
                      <button type="button" onClick={async () => {
                          try { await downloadExport(`/api/v1/deliverables/${d.id}/export?format=${delivFormat}`, `${d.title || 'deliverable'}.${delivFormat}`); }
                          catch (e: any) { alert(e?.message ?? 'Export failed'); }
                        }}
                        className="shrink-0 text-[10px] font-black uppercase text-sovereign bg-aura px-3 py-1.5 rounded-lg flex items-center gap-1 hover:opacity-90"><Download size={11} /> Export</button>
                    </div>
                  ))}
                  {deliverables.length === 0 && <p className="text-slate-600 text-xs">No deliverables yet — produce one above.</p>}
                </div>
              </Card>
            </div>
          )}

          {/* Living Systems */}
          {tab === 'systems' && (
            <Card className="p-6">
              <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2"><ShieldCheck size={14} /> Living management systems (BMS · QMS · DCS · EMS …)</h4>
              <div className="grid grid-cols-1 @[560px]:grid-cols-2 @[900px]:grid-cols-3 gap-3">
                {standards.map((s, i) => (
                  <div key={s.id || i} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                    <p className="font-black text-white text-sm">{s.name || s.id}</p>
                    {s.standard && <p className="text-[10px] font-mono text-aura/60 mt-1">{s.standard}</p>}
                    {s.description && <p className="text-[10px] text-slate-500 mt-1 leading-relaxed">{s.description}</p>}
                  </div>
                ))}
                {standards.length === 0 && <p className="text-slate-600 text-xs">Management systems unavailable.</p>}
              </div>
            </Card>
          )}

          {/* Economy — the VSB's economic metabolism (virtual WST only; capital-preserving waterfall) */}
          {tab === 'economy' && (
            <div className="space-y-4">
              <Card className="p-6 space-y-3">
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-2"><Coins size={14} /> Economic model — {economy.entity_name || economy.entity_type || 'entity'}</h4>
                  <span className="text-[8px] font-black uppercase px-2 py-1 rounded bg-amber-500/15 text-amber-400">{economy.currency || 'WST (virtual)'}</span>
                </div>
                {economy.capital_preserved && <p className="text-[10px] text-emerald-400 font-bold">Capital-preserving (waqf principle): the endowment base is protected.</p>}
                <div>
                  <p className="text-[9px] font-black uppercase tracking-widest text-slate-500 mb-2">Profit waterfall</p>
                  <div className="space-y-1.5">
                    {Object.entries(waterfall).map(([k, v]) => (
                      <div key={k} className="flex items-center gap-3">
                        <span className="text-[10px] font-bold text-slate-400 w-32 capitalize">{k.replace(/_/g, ' ')}</span>
                        <div className="flex-1 h-2 rounded-full bg-slate-800 overflow-hidden"><div className="h-full bg-highlight" style={{ width: `${Math.round((v as number) * 100)}%` }} /></div>
                        <span className="text-[10px] font-black text-highlight w-10 text-right">{Math.round((v as number) * 100)}%</span>
                      </div>
                    ))}
                    {Object.keys(waterfall).length === 0 && <p className="text-slate-600 text-xs">No waterfall configured.</p>}
                  </div>
                </div>
              </Card>

              <Card className="p-6">
                <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Virtual ledger {ledger?.currency ? `· ${ledger.currency}` : ''}</h4>
                  <Button type="button" onClick={runCycle} disabled={cycling} className="bg-highlight text-sovereign flex items-center gap-2 text-xs">
                    {cycling ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run economic cycle
                  </Button>
                </div>
                {ledger ? (
                  <>
                    <div className="grid grid-cols-2 @[560px]:grid-cols-4 gap-3">
                      {Object.entries(ledger.balances || {}).map(([k, v]) => (
                        <div key={k} className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                          <p className="text-[9px] font-black uppercase tracking-wider text-slate-500 capitalize">{k.replace(/_/g, ' ')}</p>
                          <p className="text-sm font-black text-white mt-0.5">{Number(v).toLocaleString()}</p>
                        </div>
                      ))}
                    </div>
                    <p className="text-[10px] text-slate-500 mt-3">Total revenue: <span className="text-white font-bold">{Number(ledger.total_revenue || 0).toLocaleString()}</span> · distributed: <span className="text-white font-bold">{Number(ledger.total_distributed || 0).toLocaleString()}</span> · entries: {ledger.entry_count ?? 0}</p>
                  </>
                ) : <p className="text-slate-600 text-xs">No ledger yet — run an economic cycle to seed it.</p>}
                {ledger?.disclaimer && <p className="text-[9px] text-slate-600 italic mt-3">{ledger.disclaimer}</p>}
              </Card>

              {lastCycle && (
                <Card className="p-6 border-highlight/30">
                  <h4 className="text-[10px] font-black uppercase tracking-widest text-highlight mb-3">Latest metabolic cycle</h4>
                  <div className="grid grid-cols-2 @[560px]:grid-cols-3 gap-3 text-[11px]">
                    {[['Intake revenue', lastCycle.intake_revenue], ['Homeostasis reserves', lastCycle.homeostasis_reserves], ['Distributable profit', lastCycle.distributable_profit], ['Giving back', lastCycle.giving_back], ['Metabolic energy', lastCycle.metabolic_energy]].map(([label, val]) => val != null && (
                      <div key={label as string}><span className="text-slate-500">{label}: </span><span className="text-white font-bold">{typeof val === 'number' ? Number(val).toLocaleString() : String(val)}</span></div>
                    ))}
                  </div>
                  {lastCycle.disclaimer && <p className="text-[9px] text-slate-600 italic mt-3">{lastCycle.disclaimer}</p>}
                </Card>
              )}
            </div>
          )}

          {/* Transformation */}
          {tab === 'transform' && (
            <div className="space-y-4">
              {/* §13 (W338) — drift honesty: the stale flag is finally VISIBLE, with the re-ship
                  action right beside it. Amber = the shipped body lags the living record. */}
              {shipState?.stale && (
                <Card className="p-4 border-amber-500/40 bg-amber-500/5">
                  <p className="text-[11px] font-black uppercase tracking-widest text-amber-400">Shipped body is STALE</p>
                  <p className="text-[10px] text-slate-400 mt-1">
                    The living record moved since the last ship{shipState?.stale_reason ? <> — {String(shipState.stale_reason)}</> : null}
                    {shipState?.stale_since ? <> (since {String(shipState.stale_since)})</> : null}.
                    Use “Ship the repo” below to regenerate every surface from the current life.
                  </p>
                </Card>
              )}
              {shipState && !shipState.stale && (
                <p className="text-[9px] font-black uppercase tracking-widest text-emerald-500/80">Shipped body is current (shipped {String(shipState.shipped_at ?? '')})</p>
              )}
              {/* W299 — §13 growth machinery, now reachable for THIS entity (previously API-only) */}
              <Card className="p-6 border-emerald-500/30">
                <h4 className="text-[10px] font-black uppercase tracking-widest text-emerald-400 mb-2">Grow the living enterprise (§13)</h4>
                <div className="flex flex-wrap gap-2">
                  <Button type="button" onClick={() => runGrowth('ship')} disabled={!!growthBusy}
                    className="bg-emerald-500/15 text-emerald-300 text-[11px] flex items-center gap-1.5">
                    {growthBusy === 'ship' ? <Loader2 size={13} className="animate-spin" /> : <Play size={13} />} Ship the repo (all surfaces, one whole)
                  </Button>
                  <Button type="button" onClick={() => runGrowth('cascade')} disabled={!!growthBusy}
                    className="bg-emerald-500/15 text-emerald-300 text-[11px] flex items-center gap-1.5">
                    {growthBusy === 'cascade' ? <Loader2 size={13} className="animate-spin" /> : <Play size={13} />} Run the repo's cascade
                  </Button>
                  <Button type="button" onClick={() => runGrowth('evolve')} disabled={!!growthBusy}
                    className="bg-emerald-500/15 text-emerald-300 text-[11px] flex items-center gap-1.5">
                    {growthBusy === 'evolve' ? <Loader2 size={13} className="animate-spin" /> : <Play size={13} />} Evolve (re-ships the repo)
                  </Button>
                </div>
                {growthResult && (
                  <div className="mt-3 p-3 rounded-xl bg-slate-950 border border-slate-800 text-[11px] text-slate-300 space-y-1">
                    {growthResult.error ? (
                      <p className="text-vital">{String(growthResult.error)}</p>
                    ) : growthResult.kind === 'ship' ? (
                      <p>Shipped {Object.keys(growthResult.surfaces || {}).length} surfaces · coherent whole: {String(growthResult.coherent_whole)} · commit {growthResult.version_control?.commit}</p>
                    ) : growthResult.kind === 'cascade' ? (
                      <p>Cascade run {growthResult.repo_run?.run_id} · plan: {growthResult.repo_run?.plan_binding?.result ?? '—'} · committed {growthResult.version_control?.commit}</p>
                    ) : (
                      <p>Generation {growthResult.generation} · {(growthResult.proposals || []).length} proposals · repo: {growthResult.repo_refresh?.action ?? 'no repo yet'}</p>
                    )}
                  </div>
                )}
              </Card>
              <Card className="p-6">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <div>
                    <h4 className="text-sm font-black text-white uppercase tracking-wide">End-to-end Transformation</h4>
                    <p className="text-[11px] text-slate-500 mt-1">Run the whole org cascade for this VSB: Chief of the Board → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order, governed arms-length and simulated on a digital twin — in-house.</p>
                  </div>
                  <Button type="button" onClick={runTransformation} disabled={txRunning} className="bg-highlight text-sovereign flex items-center gap-2 text-xs shrink-0">
                    {txRunning ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run transformation
                  </Button>
                </div>
              </Card>
              {tx && (
                <>
                  <Card className="p-6">
                    <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3">Cascade ({(tx.cascade || []).length} stages · {tx.validation?.validated ? 'validated' : 'partial'})</h4>
                    <div className="space-y-2">
                      {(tx.cascade || []).map((s: Dict, i: number) => (
                        <div key={i} className="flex items-start gap-3 text-[11px]">
                          <span className="text-highlight font-black shrink-0">{s.step}.</span>
                          <div>
                            <span className="text-white font-black uppercase tracking-wide">{s.tier}</span>
                            {s.delegates_to && <span className="text-slate-600"> → {s.delegates_to}</span>}
                            <p className="text-slate-500">{s.action}</p>
                          </div>
                          {s.verified && <ShieldCheck size={12} className="text-emerald-400 ml-auto shrink-0 mt-0.5" />}
                        </div>
                      ))}
                    </div>
                  </Card>
                  <div className="grid grid-cols-1 @[700px]:grid-cols-2 gap-4">
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><Boxes size={14} /> Operational delivery resources</h4>
                      <div className="flex flex-wrap gap-1.5">{(tx.operational_delivery_resources || []).map((r: string, i: number) => <span key={i} className="px-2 py-1 rounded-md bg-slate-800 text-[9px] font-black uppercase text-slate-300">{r}</span>)}</div>
                    </Card>
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-3 flex items-center gap-2"><ScrollText size={14} /> Products / Services catalogue ({(tx.products_services_catalogue || []).length})</h4>
                      <ul className="text-[11px] text-slate-300 space-y-1">{(tx.products_services_catalogue || []).slice(0, 10).map((p: Dict, i: number) => <li key={i}>· {p.name}</li>)}</ul>
                    </Card>
                  </div>
                  {tx.digital_twin?.simulation && (
                    <Card className="p-6">
                      <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2">Digital-twin simulation</h4>
                      <p className="text-[11px] text-slate-400">Projected realisation: <span className="text-highlight font-black">{String(tx.digital_twin.simulation.projected_realisation ?? '—')}</span> · governance: {tx.governance?.status}</p>
                    </Card>
                  )}
                </>
              )}

              {/* Build-to-Order configurator — assemble the entity's components into a build blueprint */}
              <Card className="p-6 space-y-4">
                <h4 className="text-sm font-black text-white uppercase tracking-wide flex items-center gap-2"><Boxes size={15} className="text-aura" /> Build-to-Order configurator</h4>
                <p className="text-[11px] text-slate-500">Select the components to assemble into this entity's build blueprint.</p>
                <div className="flex flex-wrap gap-2">
                  {btoComponents.map(comp => {
                    const on = btoSel.includes(comp.id);
                    return (
                      <button key={comp.id} type="button"
                        onClick={() => setBtoSel(s => on ? s.filter(x => x !== comp.id) : [...s, comp.id])}
                        className={`px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${on ? 'bg-aura/20 text-aura border border-aura/40' : 'bg-slate-900 text-slate-500 border border-slate-800 hover:text-white'}`}>
                        {comp.label || comp.id}
                      </button>
                    );
                  })}
                </div>
                <Button type="button" onClick={configureBto} disabled={btoBusy || btoSel.length === 0} className="bg-aura text-sovereign flex items-center gap-2 text-xs">
                  {btoBusy ? <Loader2 size={14} className="animate-spin" /> : <Boxes size={14} />} Configure build ({btoSel.length})
                </Button>
                {btoBlueprint && (
                  <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                    <p className="text-[11px] text-slate-300"><span className="text-white font-black">{btoBlueprint.entity_name}</span> — {btoBlueprint.component_count} components · {btoBlueprint.resource_count} product resources</p>
                    <div className="flex flex-wrap gap-1.5">
                      {Object.keys(btoBlueprint.components || {}).map(k => <span key={k} className="px-2 py-0.5 rounded-md bg-slate-800 text-[9px] font-black uppercase text-slate-300">{k}</span>)}
                    </div>
                    <p className="text-[8px] font-mono text-slate-600">blueprint {String(btoBlueprint.blueprint_id).slice(0, 8)}</p>
                  </div>
                )}
              </Card>
            </div>
          )}

          {/* Converse — chat with the living VSB's avatar, grounded in this entity, in-house */}
          {tab === 'chat' && (
            <Card className="p-6 space-y-4">
              <h4 className="text-[10px] font-black uppercase tracking-widest text-slate-400 flex items-center gap-2">
                <MessageCircle size={14} /> Converse with {detail.name} <span className="text-slate-600 normal-case font-bold">— grounded in this living VSB, in-house</span>
              </h4>
              <div className="space-y-3 max-h-[440px] overflow-y-auto">
                {messages.length === 0 && (
                  <p className="text-[11px] text-slate-600">Ask the enterprise about its mission, plan, next steps, or risks — its avatar answers grounded in this VSB, on Workstation's own fabric.</p>
                )}
                {messages.map((m, i) => (
                  <div key={i} className={m.role === 'you' ? 'text-right' : ''}>
                    <div className={`inline-block max-w-[85%] text-left p-3 rounded-2xl text-[12px] leading-relaxed ${m.role === 'you' ? 'bg-highlight/15 text-slate-200' : 'bg-slate-900 border border-slate-800 text-slate-300'}`}>
                      {m.attached && <span className="inline-flex items-center gap-1 text-[9px] font-black uppercase text-aura mb-1"><Paperclip size={10} /> image attached</span>}
                      <p className="whitespace-pre-wrap font-sans">{m.text}</p>
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {m.role === 'vsb' && m.served_by && (
                          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${m.is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                            {m.is_external ? `via ${m.served_by}` : `in-house · ${m.served_by}`}
                          </span>
                        )}
                        {m.role === 'vsb' && m.image_served_by && (
                          <span className={`text-[8px] font-black uppercase px-2 py-0.5 rounded ${m.image_is_external ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                            vision: {m.image_served_by}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              {pendingImage && (
                <div className="flex items-center gap-2 text-[10px] text-aura">
                  <Paperclip size={11} /> {pendingImage.name}
                  <button type="button" onClick={() => setPendingImage(null)} className="text-slate-500 hover:text-white">✕</button>
                </div>
              )}
              <div className="flex items-center gap-2">
                <input aria-label="Message the VSB" value={chatInput} onChange={e => setChatInput(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter') sendChat(); }}
                  placeholder={listening ? 'Listening…' : 'Ask the living enterprise…'}
                  className="flex-1 text-xs bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-300" />
                <label aria-label="Attach an image" title="Attach an image (analysed by the in-house vision model)"
                  className="p-3 rounded-xl shrink-0 bg-slate-800 text-slate-400 hover:text-white cursor-pointer transition-all">
                  <Paperclip size={14} />
                  <input type="file" accept="image/*" className="hidden" onChange={e => attachImage(e.target.files?.[0])} />
                </label>
                {SpeechRec && (
                  <button type="button" onClick={listenVoice} aria-label={listening ? 'Stop listening' : 'Speak to the enterprise'}
                    title="Voice input (browser-native, in-house)"
                    className={`p-3 rounded-xl shrink-0 transition-all ${listening ? 'bg-vital/20 text-vital animate-pulse' : 'bg-slate-800 text-slate-400 hover:text-white'}`}>
                    <Mic size={14} />
                  </button>
                )}
                {canSpeak && (
                  <button type="button" onClick={() => setSpeakReplies(s => !s)} aria-label="Toggle spoken replies"
                    title="Speak the enterprise's replies aloud (browser-native)"
                    className={`p-3 rounded-xl shrink-0 transition-all ${speakReplies ? 'bg-aura/20 text-aura' : 'bg-slate-800 text-slate-400 hover:text-white'}`}>
                    <Volume2 size={14} />
                  </button>
                )}
                <select aria-label="Response language" value={chatLang} onChange={e => setChatLang(e.target.value)}
                  title="Respond in this language (in-house)"
                  className="text-[10px] font-black uppercase bg-slate-800 border border-slate-800 rounded-xl text-slate-300 px-2 py-3 shrink-0">
                  {['', 'Arabic', 'Urdu', 'French', 'Spanish', 'Hindi', 'Bengali', 'Mandarin', 'Turkish', 'Malay', 'Swahili'].map(l => (
                    <option key={l || 'en'} value={l}>{l || 'English'}</option>
                  ))}
                </select>
                <Button type="button" onClick={() => sendChat()} disabled={chatting || (!chatInput.trim() && !pendingImage)} className="bg-highlight text-sovereign flex items-center gap-2 text-xs shrink-0">
                  {chatting ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />} Send
                </Button>
              </div>
              <p className="text-[9px] text-slate-600">Voice (browser-native, in-house) + image (analysed in-house by a local Ollama vision model, with honest provenance) — no external service required.</p>
            </Card>
          )}
        </>
      )}
    </div>
  );
};
