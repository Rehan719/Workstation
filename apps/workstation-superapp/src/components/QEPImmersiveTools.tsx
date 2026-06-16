import React, { useState } from 'react';
import { Card, Button, Badge, notImplemented} from '@workstation/ui';
import { Video, Share, Shield, CheckCircle, Microscope, Landmark, Briefcase, HeartPulse, GraduationCap, Zap } from 'lucide-react';

interface QEPImmersiveProps {
  domain?: 'religion' | 'science' | 'law' | 'employment' | 'education' | 'care';
}

export const QEPImmersiveTools: React.FC<QEPImmersiveProps> = ({ domain = 'religion' }) => {
  const domainConfig = {
    religion: { icon: Zap, label: 'Sovereign VC', sub: 'Interfaith Breakout Rooms', action: 'Join Mosque' },
    science: { icon: Microscope, label: 'Bio-Reactor VR', sub: '3D Molecular Visualization', action: 'Enter Lab' },
    law: { icon: Landmark, label: 'Legal Sandbox', sub: 'Constitutional Simulation', action: 'Review Treaty' },
    employment: { icon: Briefcase, label: 'Workforce Mesh', sub: 'Virtual Skill Garden', action: 'Start Collab' },
    education: { icon: GraduationCap, label: 'Universal Aula', sub: 'Immersive Learning Hub', action: 'Enter Aula' },
    care: { icon: HeartPulse, label: 'Patient Twin', sub: 'Bio-Digital Diagnostics', action: 'Start Scan' }
  };

  const config = domainConfig[domain];

  return (
    <div className="space-y-10">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
        <Card className="p-10 border-aura/20 bg-aura/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl">
               <config.icon size={32} />
            </div>
            <div>
               <h3 className="text-2xl font-black text-white uppercase">{config.label}</h3>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{config.sub}</p>
            </div>
          </div>
          <div className="space-y-4">
             <Button onClick={() => notImplemented('This action')} className="w-full bg-slate-900 text-aura border border-aura/20 py-4 flex items-center justify-center gap-3">
                <Video size={18} />
                {config.action}
             </Button>
             <div className="p-6 rounded-2xl bg-slate-950 border border-slate-900 flex justify-between items-center">
                <span className="text-xs font-bold text-slate-400 italic">Domain Sync Active (v1.0)</span>
                <Badge color="aura">LIVE</Badge>
             </div>
          </div>
        </Card>

        <Card className="p-10 border-highlight/20 bg-highlight/5">
          <div className="flex items-center gap-6 mb-8">
            <div className="w-16 h-16 rounded-2xl bg-highlight flex items-center justify-center text-sovereign shadow-xl">
               <Shield size={32} />
            </div>
            <div>
               <h3 className="text-2xl font-black text-white uppercase">Sovereign Governance</h3>
               <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Article-Driven Compliance</p>
            </div>
          </div>
          <div className="space-y-6">
             <div className="flex items-center gap-4 text-xs font-bold text-slate-300">
                <CheckCircle size={16} className="text-emerald-500" />
                Data Sovereignty Verified
             </div>
             <div className="flex items-center gap-4 text-xs font-bold text-slate-300">
                <CheckCircle size={16} className="text-emerald-500" />
                Context: {domain.toUpperCase()} Domain Profile
             </div>
             <Button onClick={() => notImplemented('Audit Framework')} variant="outline" className="w-full text-[10px] py-4 uppercase font-black">Audit Framework</Button>
          </div>
        </Card>
      </div>
    </div>
  );
};
