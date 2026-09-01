import React, { useEffect, useState } from 'react';
import { REALMS as CANON_REALMS, DOMAINS as CANON_DOMAINS } from '../lib/taxonomy';
import { Card, Button } from '@workstation/ui';
import { Check, Trash2, User, Settings as SettingsIcon } from 'lucide-react';
import { getPrefs, setPrefs, clearPrefs, LANGUAGES, type UserPrefs } from '../lib/userPrefs';
import { coverageFor, applyDocumentDirection } from '../lib/i18n';
import { clearWorkspaceEverywhere } from '../lib/outputHistory';
import {
  PROFILE_FIELDS, MAX_FIELD_CHARS, EMPTY_PROFILE,
  getProfile, putProfile, clearProfile, type UserProfile,
} from '../lib/userProfile';

// §17.1 canonical realms × domains — kept consistent with Genesis.
const REALMS = [...CANON_REALMS];   // §17.1 (W321)
const DOMAINS = [...CANON_DOMAINS];

// §9 — System Settings: real preferences (display name, defaults, adaptive UI) that personalise the
// experience. Signed in, they are saved to the user's own server-side workspace and follow them
// across devices; in auth-off single-user mode they live in this browser only.
export const Settings: React.FC = () => {
  const [prefs, setLocal] = useState<UserPrefs>(() => getPrefs());
  const [saved, setSaved] = useState(false);

  // §4.2 (W428) — the explicit profile. Server-stored under the caller's owner id, so unlike the
  // browser-local prefs above it follows the person rather than the machine.
  const [profile, setProfile] = useState<UserProfile>(EMPTY_PROFILE);
  const [preamble, setPreamble] = useState('');
  const [profBusy, setProfBusy] = useState(false);
  const [profSaved, setProfSaved] = useState(false);
  const [profErr, setProfErr] = useState('');

  useEffect(() => {
    getProfile().then(r => {
      if (!r) return;                       // unreachable store: leave the form empty, say nothing false
      setProfile({ ...EMPTY_PROFILE, ...r.profile });
      setPreamble(r.preamble_preview || '');
    });
  }, []);

  const saveProfile = async () => {
    setProfBusy(true); setProfErr('');
    try {
      const r = await putProfile(profile);
      // Show the preamble the SERVER built, not one recomputed here — the server trims and
      // neutralises, so a locally-rendered preview could differ from what is actually sent.
      setPreamble(r?.preamble_preview || '');
      setProfSaved(true); setTimeout(() => setProfSaved(false), 1800);
    } catch (e) {
      setProfErr(String((e as Error).message));   // a failed save never renders as saved
    } finally {
      setProfBusy(false);
    }
  };

  const update = (patch: Partial<UserPrefs>) => { setLocal(p => ({ ...p, ...patch })); setSaved(false); };
  const save = () => { setPrefs(prefs); applyDocumentDirection(prefs.language); setSaved(true); setTimeout(() => setSaved(false), 1800); };

  return (
    <div className="space-y-8 pb-16 max-w-2xl">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2 flex items-center gap-2"><SettingsIcon size={12} /> Workstation IDBO</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">System Settings</h1>
        <p className="text-slate-500 font-bold mt-2 leading-relaxed">
          Personalise your experience. Signed in, these preferences are saved to your account and follow you
          across devices; in single-user mode they are saved in this browser.
        </p>
      </header>

      <Card className="p-8 space-y-6">
        <h3 className="text-sm font-black text-white uppercase tracking-wide flex items-center gap-2"><User size={16} className="text-aura" /> Profile & defaults</h3>

        <div>
          <label htmlFor="pref-name" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Display name</label>
          <input id="pref-name" value={prefs.displayName ?? ''} onChange={e => update({ displayName: e.target.value })}
            placeholder="How should we greet you? (e.g. your name)"
            className="block w-full mt-1.5 text-sm bg-slate-950 border border-slate-900 rounded-xl p-3 text-slate-200" />
          <p className="text-[10px] text-slate-600 mt-1">Used to greet you on the Command Center.</p>
        </div>

        <div className="grid grid-cols-1 @[440px]:grid-cols-2 gap-5">
          <div>
            <label htmlFor="pref-realm" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Default realm</label>
            <select id="pref-realm" value={prefs.defaultRealm ?? ''} onChange={e => update({ defaultRealm: e.target.value || undefined })}
              className="block w-full mt-1.5 text-xs font-black uppercase bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
              <option value="">No default</option>
              {REALMS.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label htmlFor="pref-domain" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Default domain</label>
            <select id="pref-domain" value={prefs.defaultDomain ?? ''} onChange={e => update({ defaultDomain: e.target.value || undefined })}
              className="block w-full mt-1.5 text-xs font-black uppercase bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
              <option value="">No default</option>
              {DOMAINS.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>
        </div>
        <p className="text-[10px] text-slate-600">Defaults pre-seed a new Genesis journey (you can always change them there).</p>

        <div>
          <label htmlFor="pref-lang" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Language</label>
          <select id="pref-lang" value={prefs.language ?? 'en-US'} onChange={e => update({ language: e.target.value })}
            className="block w-full @[440px]:w-72 mt-1.5 text-xs font-black bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
            {LANGUAGES.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
          </select>
          {/* §14 (W370) — state coverage from the REAL dictionaries, not a blanket claim. The old
              text said interface translation "depends on the external AI accelerant", which was
              inaccurate: Arabic, French, Spanish and Urdu are translated in-house today. */}
          <p className="text-[10px] text-slate-600 mt-1.5 leading-relaxed">
            <span className="text-emerald-400 font-bold">Voice dictation works in your language.</span>{' '}
            {(() => {
              const cov = coverageFor(prefs.language);
              if (cov.hasDict) return (
                <span className="text-emerald-400 font-bold">
                  The interface is translated ({cov.keys} strings){cov.rtl ? ', and the layout switches to right-to-left' : ''}.{' '}
                </span>
              );
              return (
                <span className="text-amber-400 font-bold">
                  The interface is not translated into this language yet — it stays in English.{' '}
                </span>
              );
            })()}
            Translation covers interface chrome, not every screen, and AI-generated content is still produced
            in English — the in-house engine reasons in English.
          </p>
        </div>

        {/* §9 (W357) — REAL adaptive-UI controls: these genuinely change the interface (font
            scale enlarges rendering; guided mode + tone drive the affordances the hubs show). */}
        <div className="grid grid-cols-1 @[440px]:grid-cols-3 gap-4 pt-2 border-t border-slate-800/60">
          <div>
            <label htmlFor="pref-font" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Text size</label>
            <select id="pref-font" value={prefs.fontScale ?? 'standard'} onChange={e => update({ fontScale: e.target.value as any })}
              className="block w-full mt-1.5 text-xs font-black bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
              <option value="standard">Standard</option>
              <option value="large">Large (accessible)</option>
            </select>
          </div>
          <div>
            <label htmlFor="pref-guided" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Guidance</label>
            <select id="pref-guided" value={(prefs.guidedMode !== false) ? 'on' : 'off'} onChange={e => update({ guidedMode: e.target.value === 'on' })}
              className="block w-full mt-1.5 text-xs font-black bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
              <option value="on">Guided mode</option>
              <option value="off">Advanced (less hand-holding)</option>
            </select>
          </div>
          <div>
            <label htmlFor="pref-tone" className="text-[9px] font-black uppercase tracking-widest text-slate-500">Tone</label>
            <select id="pref-tone" value={prefs.tone ?? 'encouraging'} onChange={e => update({ tone: e.target.value as any })}
              className="block w-full mt-1.5 text-xs font-black bg-slate-900 border border-slate-800 rounded-lg text-slate-300 px-3 py-2.5">
              <option value="encouraging">Encouraging</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>
        </div>
        <p className="text-[10px] text-slate-600">On save, text size takes effect across the whole app; guidance and tone drive the affordances shown on the domain hubs.</p>

        <div className="flex items-center gap-3 flex-wrap">
          <Button type="button" onClick={save} className="bg-aura text-sovereign flex items-center gap-2 text-xs">
            {saved ? <><Check size={14} /> Saved</> : 'Save preferences'}
          </Button>
          {/* W-tour — re-run the onboarding tour on demand (it auto-runs once for new visitors) */}
          <Button type="button" onClick={() => window.dispatchEvent(new CustomEvent('ws:start-tour'))}
            className="bg-slate-900 text-slate-300 text-xs">Take the tour</Button>
        </div>
      </Card>

      {/* §4.2 (W428) — "understand the person". Nothing about the user reached any prompt, and
          there was no field to enter anything. This is that field, and it is deliberately explicit:
          the platform never infers a profile from your activity. */}
      <Card className="p-8 space-y-4">
        <div>
          <h3 className="text-sm font-black text-white uppercase tracking-wide">About you</h3>
          <p className="text-[11px] text-slate-500 leading-relaxed mt-1 max-w-3xl">
            Used to shape what the platform generates for you. Only what you type here is used —
            nothing is inferred from your activity, and it is never drawn from anyone else's.
            You can see exactly what it sends below, and delete it at any time.
          </p>
        </div>
        {PROFILE_FIELDS.map(f => (
          <label key={f.key} className="flex flex-col gap-1">
            <span className="text-[10px] font-black uppercase tracking-widest text-slate-500">{f.label}</span>
            <textarea
              value={profile[f.key]} rows={2} maxLength={MAX_FIELD_CHARS}
              aria-label={f.label}
              onChange={e => { setProfile({ ...profile, [f.key]: e.target.value }); setProfSaved(false); }}
              placeholder={f.hint}
              className="bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-white resize-y" />
          </label>
        ))}
        {profErr && <p role="alert" className="text-[11px] font-bold text-vital">{profErr}</p>}
        {preamble
          ? (
            <div>
              <p className="text-[10px] font-black uppercase tracking-widest text-slate-600 mb-1">
                Exactly what is added to your prompts
              </p>
              <pre className="text-[10px] text-slate-400 bg-slate-950 border border-slate-900 rounded-xl p-3 whitespace-pre-wrap">{preamble}</pre>
            </div>
          )
          : <p className="text-[10px] text-slate-600 font-semibold">Nothing saved — no profile is added to your prompts.</p>}
        <div className="flex flex-wrap gap-3">
          <Button type="button" onClick={saveProfile} disabled={profBusy}>
            {profSaved ? <><Check size={14} /> Saved</> : 'Save profile'}
          </Button>
          <Button type="button" variant="outline" disabled={profBusy || !preamble}
            onClick={async () => {
              setProfBusy(true); setProfErr('');
              try { await clearProfile(); setProfile(EMPTY_PROFILE); setPreamble(''); }
              catch (e) { setProfErr(String((e as Error).message)); }
              finally { setProfBusy(false); }
            }}
            className="text-[10px] border-slate-800 text-slate-400">
            <Trash2 size={14} /> Delete profile
          </Button>
        </div>
      </Card>

      <Card className="p-8 space-y-4 border-slate-900">
        <h3 className="text-sm font-black text-white uppercase tracking-wide">Your data</h3>
        <p className="text-[11px] text-slate-500 leading-relaxed">
          Signed in, your preferences and <span className="text-slate-300">My Work</span> history are saved to
          your own account and follow you across devices; in single-user mode they live only in this browser.
          Clearing removes both copies.
        </p>
        <Button type="button" onClick={() => { clearPrefs(); clearWorkspaceEverywhere(); setLocal({}); }}
          variant="outline" className="text-[10px] border-slate-800 text-slate-400 w-fit">
          <Trash2 size={14} /> Clear preferences & history
        </Button>
      </Card>
    </div>
  );
};
