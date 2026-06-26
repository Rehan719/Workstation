import React, { useEffect, useRef, useState } from 'react';
import { Mic, Loader2 } from 'lucide-react';

// E6 — voice input (§9 multimodal). A mic button that dictates speech into a text field using the browser's
// native Web Speech API (in-house: runs in the browser, no server). FEATURE-DETECTED — if the API is
// unavailable, it renders nothing (honest: no fake mic). On a final transcript it calls onTranscript(text);
// the caller appends it into its field.

type SpeechRecognitionCtor = new () => any;
function getSR(): SpeechRecognitionCtor | null {
  if (typeof window === 'undefined') return null;
  return (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition || null;
}

interface DictateButtonProps {
  onTranscript: (text: string) => void;
  lang?: string;
}

export const DictateButton: React.FC<DictateButtonProps> = ({ onTranscript, lang = 'en-US' }) => {
  const SR = getSR();
  const [listening, setListening] = useState(false);
  const [err, setErr] = useState('');
  const recRef = useRef<any>(null);

  useEffect(() => () => { try { recRef.current?.abort?.(); } catch { /* ignore */ } }, []);

  if (!SR) return null; // honest: no Web Speech support → no button

  const toggle = () => {
    if (listening) { try { recRef.current?.stop?.(); } catch { /* ignore */ } return; }
    setErr('');
    try {
      const rec = new SR();
      rec.lang = lang;
      rec.continuous = false;
      rec.interimResults = false;
      rec.onresult = (e: any) => {
        const text = Array.from(e.results).map((r: any) => r[0]?.transcript ?? '').join(' ').trim();
        if (text) onTranscript(text);
      };
      rec.onend = () => setListening(false);
      rec.onerror = (e: any) => { setListening(false); if (e?.error && e.error !== 'aborted' && e.error !== 'no-speech') setErr('Voice input unavailable (check microphone permission).'); };
      recRef.current = rec;
      rec.start();
      setListening(true);
    } catch { setErr('Could not start voice input.'); setListening(false); }
  };

  return (
    <div className="inline-flex flex-col gap-1">
      <button type="button" onClick={toggle}
        {...({ 'aria-pressed': listening ? 'true' : 'false' } as { 'aria-pressed': 'true' | 'false' })}
        aria-label={listening ? 'Stop dictation' : 'Dictate by voice'} title={listening ? 'Listening — click to stop' : 'Dictate by voice'}
        className={`text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-lg border flex items-center gap-1.5 transition-all ${
          listening ? 'bg-aura/15 border-aura/40 text-aura' : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white'
        }`}>
        {listening ? <Loader2 size={11} className="animate-spin" /> : <Mic size={11} />} {listening ? 'Listening…' : 'Dictate'}
      </button>
      {err && <span className="text-[9px] text-amber-400 font-bold">{err}</span>}
    </div>
  );
};
