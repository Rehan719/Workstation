import React, { useState } from 'react';
import { REALMS as CANON_REALMS, DOMAINS as CANON_DOMAINS } from '../lib/taxonomy';
import { Card, Button } from '@workstation/ui';
import { Check, Trash2, User, Settings as SettingsIcon } from 'lucide-react';
import { getPrefs, setPrefs, clearPrefs, LANGUAGES, type UserPrefs } from '../lib/userPrefs';
import { clearOutputs } from '../lib/outputHistory';

// §17.1 canonical realms × domains — kept consistent with Genesis.
const REALMS = [...CANON_REALMS];   // §17.1 (W321)
const DOMAINS = [...CANON_DOMAINS];

// E5 — System Settings: real, honest, local preferences (display name + defaults) that personalise the
// experience. Replaces the former stub. All values are stored in this browser only (no server profile).
export const Settings: React.FC = () => {
  const [prefs, setLocal] = useState<UserPrefs>(() => getPrefs());
  const [saved, setSaved] = useState(false);

  const update = (patch: Partial<UserPrefs>) => { setLocal(p => ({ ...p, ...patch })); setSaved(false); };
  const save = () => { setPrefs(prefs); setSaved(true); setTimeout(() => setSaved(false), 1800); };

  return (
    <div className="space-y-8 pb-16 max-w-2xl">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-aura mb-2 flex items-center gap-2"><SettingsIcon size={12} /> Workstation IDBO</p>
        <h1 className="text-4xl @[640px]:text-5xl font-black tracking-tight text-white uppercase italic">System Settings</h1>
        <p className="text-slate-500 font-bold mt-2 leading-relaxed">
          Personalise your experience. These preferences are saved locally in this browser (no server profile).
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
          <p className="text-[10px] text-slate-600 mt-1.5 leading-relaxed">
            <span className="text-emerald-400 font-bold">Voice dictation works in your language now.</span>{' '}
            AI text responses in your language and full interface translation depend on the external AI accelerant
            (Owner-gated) — the in-house engine currently reasons in English.
          </p>
        </div>

        <Button type="button" onClick={save} className="bg-aura text-sovereign flex items-center gap-2 text-xs">
          {saved ? <><Check size={14} /> Saved</> : 'Save preferences'}
        </Button>
      </Card>

      <Card className="p-8 space-y-4 border-slate-900">
        <h3 className="text-sm font-black text-white uppercase tracking-wide">Your data</h3>
        <p className="text-[11px] text-slate-500 leading-relaxed">
          Everything here lives only in this browser. Clear it any time — this removes your saved preferences
          and your <span className="text-slate-300">My Work</span> output history.
        </p>
        <Button type="button" onClick={() => { clearPrefs(); clearOutputs(); setLocal({}); }}
          variant="outline" className="text-[10px] border-slate-800 text-slate-400 w-fit">
          <Trash2 size={14} /> Clear preferences & history
        </Button>
      </Card>
    </div>
  );
};
