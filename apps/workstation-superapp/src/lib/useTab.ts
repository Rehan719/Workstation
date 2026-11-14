import { useSearchParams } from 'react-router-dom';

// W1027 - a page's tab is in its address. Six domain hubs and the entity cockpit read ?tab= once, when they mounted,
// and never wrote it, and the Quran platform's hub did not read it at all: a tool chosen on a hub was lost on a
// reload, a link could not name it, and an address that changed while the hub was open was not followed. The four tab
// hubs W1017 rendered already read and wrote it. This reads the tab from the address on every render, writes the one
// chosen (the first tab is the address with no ?tab=), keeps every other parameter the address carries, and opens the
// first tab for one the page does not have.
export function useTab(ids: readonly string[], first: string): [string, (id: string) => void] {
  const [sp, setSp] = useSearchParams();
  const asked = sp.get('tab');
  const active = asked !== null && ids.includes(asked) ? asked : first;
  const choose = (id: string) => setSp(prev => {
    const next = new URLSearchParams(prev);
    if (id === first) next.delete('tab');
    else next.set('tab', id);
    return next;
  }, { replace: true });
  return [active, choose];
}
