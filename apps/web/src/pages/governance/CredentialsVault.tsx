import React, { useState } from 'react';
import { Card, Badge, Button } from '@workstation/ui';
import { Lock, Key, Shield, RefreshCw, Eye, EyeOff, MoreVertical, Copy } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const CredentialsVault: React.FC = () => {
  const [secrets, setSecrets] = useState([
    { id: 1, name: 'Main-Sovereign-PQC-Key', type: 'DILITHIUM-5', status: 'ROTATED', lastSync: '2h ago' },
    { id: 2, name: 'L11-Orbital-Auth-Token', type: 'JWT-RSA4096', status: 'ACTIVE', lastSync: '5m ago' },
    { id: 3, name: 'GaaS-Verification-Master', type: 'KYBER-1024', status: 'ACTIVE', lastSync: '1d ago' },
  ]);

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black text-white tracking-tighter uppercase italic">Sovereign Vault</h1>
          <p className="text-vital font-black uppercase text-[10px] tracking-[0.3em]">Quantum-Resistant Credential Orchestration • Article 1107</p>
        </div>
        <div className="flex gap-4">
           <Button variant="outline" className="bg-vital/10 border-vital/30 text-vital"><RefreshCw size={18} /> Rotate All</Button>
           <Button className="bg-white text-sovereign shadow-xl shadow-white/10"><Key size={18} /> Add Secret</Button>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         {secrets.map((s, i) => (
           <motion.div key={s.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
             <Card className="group hover:border-vital/30 transition-all border-white/5 bg-slate-950/40">
                <div className="flex justify-between items-start mb-6">
                   <div className="p-3 rounded-xl bg-vital/20 text-vital"><Lock size={20} /></div>
                   <Badge color={s.status === 'ACTIVE' ? 'emerald-500' : 'highlight'}>{s.status}</Badge>
                </div>
                <h3 className="text-lg font-black text-white mb-2 uppercase tracking-widest">{s.name}</h3>
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-6">Type: {s.type}</p>
                <div className="flex justify-between items-center pt-6 border-t border-white/5">
                   <span className="text-[10px] font-mono text-slate-600">Sync: {s.lastSync}</span>
                   <div className="flex gap-2">
                      <button className="p-2 text-slate-500 hover:text-white transition-colors"><Eye size={16} /></button>
                      <button className="p-2 text-slate-500 hover:text-white transition-colors"><Copy size={16} /></button>
                   </div>
                </div>
             </Card>
           </motion.div>
         ))}
      </div>

      <Card className="p-10 bg-vital/5 border-vital/10">
         <div className="flex items-center gap-8">
            <div className="w-20 h-20 rounded-3xl bg-vital flex items-center justify-center text-sovereign shadow-2xl shadow-vital/20">
               <Shield size={40} />
            </div>
            <div className="flex-1">
               <h3 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Post-Quantum Integrity</h3>
               <p className="text-sm text-slate-400 font-bold leading-relaxed max-w-2xl">
                  Vault access is governed by multi-sig council approval (Article 1112). Any attempt to rotate master PQC keys triggers a 10-minute system-wide veto window.
               </p>
            </div>
            <Button variant="outline" className="border-vital/30 text-vital hover:bg-vital hover:text-white transition-all px-10">Audit Logs</Button>
         </div>
      </Card>
    </div>
  );
};
