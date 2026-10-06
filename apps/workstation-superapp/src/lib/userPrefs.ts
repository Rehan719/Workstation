// E5 — personalisation (§9 "personalised to each user's instructions, history, preferences"). Stored
// locally in this browser (honest: no server profile). Used to greet the user and pre-seed defaults.

export interface UserPrefs {
  displayName?: string;
  defaultRealm?: string;   // §17.1 realm (enterprise · learning · developing · scholarship)
  defaultDomain?: string;  // §17.1 domain (religion · science · education · law · employment · care)
  language?: string;       // E7 — BCP-47 code; the INTERFACE language (translated in-house, see i18n DICTS)
  //  P3.6 clause (3) + OWNER RULING 2026-10-05 — DICTATION IS ITS OWN CONTROL, deliberately wider than
  //  the interface. One field used to serve both, so trimming the interface list to the languages with
  //  dictionaries would have removed voice dictation in the other seven. Falls back to `language`, then
  //  to en-US, so a user who never touches it keeps the behaviour they had.
  dictationLanguage?: string;
  pinned?: string[];       // §9 — user-customisable interface: nav item ids the user pinned for quick access
  // §9 (W357) — REAL adaptive-UI preferences (were fabricated constants): fontScale genuinely
  // enlarges the interface; guidedMode/tone are the user's own stored choice, honestly reflected.
  fontScale?: 'standard' | 'large';
  guidedMode?: boolean;    // show the guided affordances (default on)
  tone?: 'encouraging' | 'neutral';
}

// E7 — supported languages (§9 "accessible to all — all languages"). BCP-47 codes are used by the
// browser Web Speech API so a user can DICTATE in their own language today.
//
// P3.6 clause (3) + OWNER RULING 2026-10-05: THIS IS THE DICTATION LIST, DELIBERATELY WIDER THAN THE
// INTERFACE LIST. The item asks for the twelve to be trimmed to what has a dictionary, and trimming this
// list would also have narrowed voice dictation, because `prefs.language` drives the Web Speech API and
// the RTL direction. The Owner's approved shape was to trim the INTERFACE list and keep a wider set for
// DICTATION as a separate control — so nothing here is deleted, and the interface picker instead calls
// `interfaceLanguages()` from lib/i18n, which derives its options from the dictionaries that exist.
// Dictation in a language the interface cannot be translated into is a real capability, not a gap.
export const LANGUAGES: { code: string; label: string }[] = [
  { code: 'en-US', label: 'English' },
  { code: 'ar-SA', label: 'Arabic (العربية)' },
  { code: 'ur-PK', label: 'Urdu (اردو)' },
  { code: 'fr-FR', label: 'French (Français)' },
  { code: 'es-ES', label: 'Spanish (Español)' },
  { code: 'de-DE', label: 'German (Deutsch)' },
  { code: 'hi-IN', label: 'Hindi (हिन्दी)' },
  { code: 'bn-BD', label: 'Bengali (বাংলা)' },
  { code: 'zh-CN', label: 'Mandarin (中文)' },
  { code: 'id-ID', label: 'Indonesian' },
  { code: 'tr-TR', label: 'Turkish (Türkçe)' },
  { code: 'ms-MY', label: 'Malay' },
];

const KEY = 'ws_user_prefs_v1';

export function getPrefs(): UserPrefs {
  try { const p = JSON.parse(localStorage.getItem(KEY) || '{}'); return p && typeof p === 'object' ? p : {}; }
  catch { return {}; }
}

export function setPrefs(next: UserPrefs) {
  try {
    localStorage.setItem(KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent('ws:user-prefs'));
  } catch { /* quota — ignore */ }
}

export function clearPrefs() {
  try { localStorage.removeItem(KEY); window.dispatchEvent(new CustomEvent('ws:user-prefs')); } catch { /* ignore */ }
}

// §9 — user-customisable interface: pin/unpin nav items for a personal quick-access section.
export function getPinned(): string[] {
  const p = getPrefs().pinned;
  return Array.isArray(p) ? p : [];
}

export function togglePinned(id: string) {
  const prefs = getPrefs();
  const pinned = Array.isArray(prefs.pinned) ? prefs.pinned : [];
  const next = pinned.includes(id) ? pinned.filter(x => x !== id) : [...pinned, id];
  setPrefs({ ...prefs, pinned: next });
}
