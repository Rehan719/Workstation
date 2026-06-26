// E5 — personalisation (§9 "personalised to each user's instructions, history, preferences"). Stored
// locally in this browser (honest: no server profile). Used to greet the user and pre-seed defaults.

export interface UserPrefs {
  displayName?: string;
  defaultRealm?: string;   // §17.1 realm (enterprise · learning · developing · scholarship)
  defaultDomain?: string;  // §17.1 domain (religion · science · education · law · employment · care)
  language?: string;       // E7 — BCP-47 code; drives voice-dictation language (real, today)
}

// E7 — supported languages (§9 "accessible to all — all languages"). BCP-47 codes are used by the
// browser Web Speech API so a user can DICTATE in their own language today. (AI text responses in these
// languages + full interface translation depend on the external AI accelerant — Owner-gated.)
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
