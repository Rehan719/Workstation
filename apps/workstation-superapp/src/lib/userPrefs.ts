// E5 — personalisation (§9 "personalised to each user's instructions, history, preferences"). Stored
// locally in this browser (honest: no server profile). Used to greet the user and pre-seed defaults.

export interface UserPrefs {
  displayName?: string;
  defaultRealm?: string;   // §17.1 realm (enterprise · learning · developing · scholarship)
  defaultDomain?: string;  // §17.1 domain (religion · science · education · law · employment · care)
}

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
