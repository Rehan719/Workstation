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
// W505 (P2.3 / FU-168) — the SAME expression DictateButton uses to decide whether it can run at all.
// Read here rather than assumed, so Settings cannot promise a capability the browser does not have.
const dictationAvailable = typeof window !== 'undefined'
  && !!((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition);

export const Settings: React.FC = () => {
  const [prefs, setLocal] = useState<UserPrefs>(() => getPrefs());
  const [saved, setSaved] = useState(false);

  // §4.2 (W428) — the explicit profile. Server-stored under the caller's owner id, so unlike the
  // browser-local prefs above it follows the person rather than the machine.
  const [profile, setProfile] = useState<UserProfile>(EMPTY_PROFILE);
  // W577 (FU-298) — a blank form is what this page shows whether the person never filled one in or
  // their stored profile could NOT BE READ. Saving over the second is how the first becomes true,
  // and the save button sits right below the sentence that says nothing is saved.
  const [profIncomplete, setProfIncomplete] = useState<string | null>(null);
  const [preamble, setPreamble] = useState('');
  const [profBusy, setProfBusy] = useState(false);
  const [profSaved, setProfSaved] = useState(false);
  const [profErr, setProfErr] = useState('');

  useEffect(() => {
    getProfile().then(r => {
      if (!r) return;                       // unreachable store: leave the form empty, say nothing false
      setProfile({ ...EMPTY_PROFILE, ...r.profile });
      setProfIncomplete(r.profile_is_incomplete ? (r.store_incomplete ?? '') : null);
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
            {/* W505 (P2.3 deliverable 5 / FU-168) — this said, in emerald, "Voice dictation works in your
                language." unconditionally, for every language. The platform sets `rec.lang` on the
                BROWSER's Web Speech API and nothing more; whether recognition exists at all is a property
                of the browser (see dictationAvailable above, which reads the same constructor
                DictateButton needs), and which languages it supports is the browser and OS's business —
                not measured here, and not ours to promise. The identifier is deliberately not repeated in
                this comment: a guard requiring a token can be satisfied by a comment naming it. */}
            {dictationAvailable ? (
              <span className="text-slate-400">
                Voice dictation is <span className="font-bold">sent to your browser</span> in your chosen
                language. Whether your browser recognises it is its own capability, which this platform
                cannot check.{' '}
              </span>
            ) : (
              <span className="text-amber-400 font-bold">
                Your browser does not provide speech recognition, so voice dictation is unavailable here.{' '}
              </span>
            )}
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
            scale enlarges rendering; guided mode + tone are SAVED and displayed but drive nothing yet
            — W493/FU-154). */}
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
        {/* W493 (FU-154, sweep S10.5, C4) - "drive the affordances shown on the domain hubs" was not
            true: only the hub badges read guidance and tone. Text size genuinely applies app-wide. */}
        <p className="text-[10px] text-slate-600" data-testid="prefs-effect-basis">On save, text size takes effect across the whole app. Guidance and tone are saved and shown on the domain hubs, but nothing yet changes with them — no affordance is gated on guidance and no request carries the tone.</p>

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
          {/* W490 (sweep S6.4, C7) — THE PRIVACY CLAIM MUST BE TRUE OF THE WHOLE PLATFORM, not just
              of this card. "Nothing is inferred from your activity" was written about the profile and
              read as a statement about everything: two surfaces DO use recall of your prior
              interactions — the AI-CEO chat and the avatar — and every interaction is written to a
              tenant-scoped memory store this page's delete button does not clear. Generation itself
              stopped using recall in W489; saying so is only honest if the exceptions are named. */}
          <p className="text-[11px] text-slate-500 leading-relaxed mt-1 max-w-3xl">
            Used to shape what the platform generates for you. This profile is only what you type here,
            it is never drawn from anyone else's, and you can see exactly what it sends below and
            delete it at any time.
          </p>
          {/* (refutation) The first cut of this replaced one false claim with another: it said every
              interaction is "stored under your account", but a call only lands in your namespace when
              it threads your id, and most do not — they land in the SHARED platform namespace, which
              recall reads for every tenant. Saying less, and saying it truly. */}
          <p className="text-[11px] text-slate-500 leading-relaxed mt-1 max-w-3xl" data-testid="recall-disclosure">
            What the platform generates for you — documents, plans, blueprints, deliverables — does not
            draw on earlier conversations. Two conversational surfaces do: the
            <span className="text-slate-400"> AI CEO chat</span> and the
            <span className="text-slate-400"> avatar</span> recall earlier interactions to keep a thread.
          </p>
          {/* W496 (FU-258) — the leak this caveat warned about is closed at the mechanism: a completion
              written with no account id now lands in an UNATTRIBUTED namespace that recall never reads,
              for any account, so a call site that forgets to thread an id cannot leak. Most call sites
              still do not thread one, which is why the recall those two surfaces get is thinner than it
              could be — an enhancement, not a leak. The caveat says what is now true. */}
          <p className="text-[11px] text-slate-500 leading-relaxed mt-1 max-w-3xl" data-testid="recall-scope-caveat">
            Interactions are written to a memory store. A call that carries your account id is stored
            under your account and only you can recall it; a call that carries none is stored
            unattributed, and <span className="text-slate-400">nothing unattributed is ever recalled</span> —
            not by you, not by anyone else on this installation. Most internal calls carry no id, so the
            two surfaces above recall less than everything you have typed. Deleting this profile does not
            clear that store.
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
          : profIncomplete !== null
            ? <p data-testid="profile-store-incomplete" title={profIncomplete || undefined}
                 className="text-[10px] font-bold px-2 py-1 rounded bg-amber-500/20 text-amber-400">
                Your stored profile could not be read in full, so this form may not show what you
                saved. Saving now would replace it — reload before you edit.
              </p>
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
