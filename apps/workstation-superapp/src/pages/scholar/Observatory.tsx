import React, { useState } from 'react';
import { Card, Badge, Button, notImplemented} from '@workstation/ui';
import { Telescope, ShieldCheck, History, Info, ChevronRight, Zap, Globe, AlertCircle, Plus, Microscope, Telescope as TelescopeIcon, Lock } from 'lucide-react';

export const Observatory: React.FC = () => {
  const [orcidConnected, setOrcidConnected] = useState(false);

  const handleOrcidAuth = () => {
     // v0.5: Real OAuth2 Flow Simulation for ORCID
     const clientId = "APP-42SOVEREIGN";
     const redirectUri = encodeURIComponent(window.location.origin + "/scholar/callback");
     const authUrl = `https://orcid.org/oauth/authorize?client_id=${clientId}&response_type=code&scope=/authenticate&redirect_uri=${redirectUri}`;

     alert("Redirecting to ORCID for v0.5 production authentication...");
     window.location.href = authUrl;
  };
  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @lg:flex-row @lg:justify-between @lg:items-end gap-6">
        <div>
          <h1 className="text-3xl @lg:text-4xl @3xl:text-6xl font-black mb-1 text-white tracking-tighter uppercase italic break-words">The Observatory</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Inter-Realm Observation • Meta-Evolutionary Analysis</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button variant="outline" onClick={handleOrcidAuth}>
              {orcidConnected ? <ShieldCheck size={18} /> : <Lock size={18} />}
              {orcidConnected ? "ORCID Verified" : "Connect ORCID"}
           </Button>
           <Button onClick={() => notImplemented('Update Lens')} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <TelescopeIcon size={18} /> Update Lens
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
         <main className="lg:col-span-8 space-y-10">
            <Card className="h-[400px] flex flex-col justify-center items-center relative overflow-hidden bg-aura/5 border-aura/10 group">
               <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(167,139,250,0.05)_0%,transparent_70%)]"></div>
               <div className="absolute top-10 left-10 z-10 space-y-2">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     Omniscient Lens
                     <Badge color="aura">Scholastic Oversight</Badge>
                  </h3>
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Global State & Evolutionary Convergence Tracking</p>
               </div>

               <div className="relative z-10 flex flex-col items-center gap-6">
                  <div className="w-48 h-48 rounded-full border-2 border-aura/20 flex items-center justify-center">
                     <TelescopeIcon size={80} className="text-aura opacity-40 animate-pulse" />
                  </div>
                  <p className="font-mono text-xs text-aura animate-pulse text-center uppercase tracking-widest">... CALIBRATING VECTORS ...<br/>REALMS: 7 | AGENTS: 142K</p>
               </div>
            </Card>
         </main>
      </div>
    </div>
  );
};
