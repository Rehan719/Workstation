import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '@workstation/ui';
import { KeyRound, Loader2, LogIn, ShieldCheck, UserPlus } from 'lucide-react';
import { clearToken, setToken, whoami, WhoAmI } from '../lib/auth';

// §14 (W296) — the FRONT DOOR: the multi-user journey can begin. Honest at every edge:
//  - auth-off single-user mode says so (no fake login theatre);
//  - registration is Owner-curated (admin-only backend) — the admin gets an in-page add-user
//    form; everyone else is told to ask the Owner, never shown a fake signup.
export const Login: React.FC = () => {
  const nav = useNavigate();
  const [who, setWho] = useState<WhoAmI | null>(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [nu, setNu] = useState({ username: '', password: '', role: 'user' });
  const [nuMsg, setNuMsg] = useState('');

  useEffect(() => { whoami().then(setWho); }, []);

  const login = async () => {
    if (!username.trim() || !password) return;
    setBusy(true); setError('');
    try {
      const body = new URLSearchParams({ username, password });
      const r = await fetch('/api/v1/auth/token', {
        method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body,
      });
      if (!r.ok) { setError(r.status === 401 ? 'Invalid username or password.' : `HTTP ${r.status}`); setBusy(false); return; }
      const d = await r.json();
      setToken(d.access_token);
      setWho(await whoami());
      nav('/');
    } catch (e: any) { setError(e?.message ?? String(e)); }
    setBusy(false);
  };

  const logout = async () => { clearToken(); setWho(await whoami()); };

  const addUser = async () => {
    if (!nu.username.trim() || !nu.password) return;
    setNuMsg('');
    const r = await fetch('/api/v1/auth/register', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(nu),
    });
    const d = await r.json().catch(() => ({}));
    setNuMsg(r.ok ? `Created '${nu.username}' (${d.role}).` : `Failed: ${d?.detail ?? r.status}`);
    if (r.ok) setNu({ username: '', password: '', role: 'user' });
  };

  return (
    <div className="max-w-lg mx-auto space-y-8 pb-24 pt-10">
      <header>
        <p className="text-[10px] font-black uppercase tracking-[0.3em] text-highlight mb-2">Workstation IDBO · Access</p>
        <h1 className="text-4xl font-black tracking-tight text-white uppercase italic">Sign in</h1>
      </header>

      {who?.mode === 'auth-off' && (
        <Card className="p-5 border-amber-500/30 bg-amber-500/5">
          <p className="text-[11px] text-amber-300 font-bold flex items-center gap-2"><ShieldCheck size={14} />
            Single-user mode — authentication is currently OFF (AUTH_ENABLED=false), so the whole
            platform is open without a sign-in. Multi-user isolation activates when the Owner enables auth.</p>
        </Card>
      )}

      {who?.mode === 'authenticated' ? (
        <Card className="p-6 space-y-3">
          <p className="text-sm text-white font-black">Signed in as {who.username} <span className="text-[9px] font-black uppercase px-1.5 py-0.5 rounded bg-highlight/15 text-highlight ml-1">{who.role}</span></p>
          <Button onClick={logout} className="bg-slate-800 text-white text-xs">Sign out</Button>
        </Card>
      ) : (
        <Card className="p-6 space-y-4">
          <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" autoComplete="username"
            className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
          <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" autoComplete="current-password"
            onKeyDown={e => e.key === 'Enter' && login()}
            className="w-full bg-slate-900 border border-slate-800 rounded-xl p-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-highlight/50" />
          <div className="flex items-center gap-3">
            <Button onClick={login} disabled={busy || !username.trim() || !password} className="flex items-center gap-2 bg-highlight text-sovereign text-sm">
              {busy ? <Loader2 size={15} className="animate-spin" /> : <LogIn size={15} />} Sign in
            </Button>
            {error && <p className="text-vital text-xs font-bold">{error}</p>}
          </div>
          <p className="text-[10px] text-slate-500 flex items-center gap-1.5"><KeyRound size={12} />
            Accounts are Owner-curated — ask the Owner for access. There is no self-serve signup (by design).</p>
        </Card>
      )}

      {who?.mode === 'authenticated' && who.role === 'admin' && (
        <Card className="p-6 space-y-3 border-sky-500/30">
          <p className="text-[10px] font-black uppercase tracking-widest text-sky-300 flex items-center gap-2"><UserPlus size={13} /> Add a user (Owner-curated registration)</p>
          <div className="grid grid-cols-1 @[480px]:grid-cols-3 gap-2">
            <input value={nu.username} onChange={e => setNu({ ...nu, username: e.target.value })} placeholder="Username"
              className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white" />
            <input value={nu.password} onChange={e => setNu({ ...nu, password: e.target.value })} placeholder="Password" type="password"
              className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white" />
            <select value={nu.role} onChange={e => setNu({ ...nu, role: e.target.value })}
              className="bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-sm text-white">
              <option value="user">user</option><option value="viewer">viewer</option><option value="admin">admin</option>
            </select>
          </div>
          <div className="flex items-center gap-3">
            <Button onClick={addUser} className="bg-sky-500/20 text-sky-300 text-xs">Create user</Button>
            {nuMsg && <p className="text-[11px] text-slate-400">{nuMsg}</p>}
          </div>
        </Card>
      )}
    </div>
  );
};
