// W1237 - the session as the server answers it, for a panel that stays on screen across a sign-in or a sign-out.
// Read on mount and again on every 'ws:identity', which setToken and clearToken dispatch, and on every change another
// tab makes to the stored token. The sidebar read it once on mount, so after a sign-in made in the page (the sign-in
// form calls nav('/') and nothing reloads) it still offered "Sign in". The listeners are removed on unmount, and an
// answer to an earlier read never replaces a later one.
import { useEffect, useState } from 'react';
import { whoami, type WhoAmI } from './auth';

//  the key auth.ts stores the token under (its KEY)
const TOKEN_KEY = 'workstation_token';

export function useIdentity(): WhoAmI | null {
  const [identity, setIdentity] = useState<WhoAmI | null>(null);
  useEffect(() => {
    let mounted = true;
    let asked = 0;
    const read = () => {
      const n = ++asked;
      const answered = (w: WhoAmI) => { if (mounted && n === asked) setIdentity(w); };
      //  W930 - whoami says an unknown session itself; a throw it never makes is said the same way, not dropped
      whoami().then(answered).catch(e => answered({ mode: 'unknown', basis: String(e) }));
    };
    //  setToken dispatches 'ws:identity' before it stores the new token (it clears the last person's data first), so
    //  the read waits until setToken has returned: asked at once, the server would be asked without the token
    const onIdentity = () => {
      setIdentity(null);
      queueMicrotask(read);
    };
    //  a sign-in or a sign-out in another tab stores or removes the token this tab sends too, and dispatches
    //  'ws:identity' in its own tab only: here it is a 'storage' event (a clear of the whole store has no key)
    const onStorage = (e: StorageEvent) => {
      if (e.key === TOKEN_KEY || e.key === null) onIdentity();
    };
    read();
    window.addEventListener('ws:identity', onIdentity);
    window.addEventListener('storage', onStorage);
    return () => {
      mounted = false;
      window.removeEventListener('ws:identity', onIdentity);
      window.removeEventListener('storage', onStorage);
    };
  }, []);
  return identity;
}
