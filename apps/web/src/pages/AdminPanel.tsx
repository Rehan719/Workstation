import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, Settings, Users, Activity, Lock } from 'lucide-react';

export const AdminPanel: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-12 max-w-6xl mx-auto"
    >
      <header className="flex flex-col gap-4 border-b border-white/5 pb-8">
        <div className="flex items-center gap-4">
          <div className="p-4 bg-vital/20 rounded-2xl text-vital shadow-[0_0_20px_rgba(255,82,82,0.2)]">
            <Lock size={32} />
          </div>
          <div>
            <h1 className="text-5xl font-black tracking-tight neon-text !text-vital drop-shadow-[0_0_12px_rgba(255,82,82,0.6)]">
              Sovereign Command Console
            </h1>
            <p className="text-slate-500 font-bold text-lg mt-2">
              System-level governance and administrative protocols.
            </p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <AdminCard
          title="User Management"
          description="Provision identities and manage realm permissions."
          icon={Users}
          status="Restricted"
        />
        <AdminCard
          title="System Config"
          description="Adjust core reactor setpoints and PID parameters."
          icon={Settings}
          status="Restricted"
        />
        <AdminCard
          title="Security Audits"
          description="View PQC handshake logs and node defense vitals."
          icon={ShieldAlert}
          status="Restricted"
        />
      </div>

      <section className="p-12 glass-card border-vital/20 bg-vital/5 text-center flex flex-col items-center justify-center gap-6 min-h-[400px]">
        <div className="w-20 h-20 rounded-full bg-vital/10 flex items-center justify-center text-vital animate-pulse">
           <Activity size={40} />
        </div>
        <div className="space-y-2">
          <h2 className="text-3xl font-black text-white">Console Under Synchronization</h2>
          <p className="text-slate-400 font-bold max-w-md mx-auto leading-relaxed">
            The Sovereign Command Console is currently undergoing v148.0 protocol integration. Functional admin tools will be available upon full planetary synchronization.
          </p>
        </div>
        <div className="flex gap-4 mt-4">
           <button className="px-8 py-3 bg-slate-800 text-slate-400 font-bold rounded-xl cursor-not-allowed border border-slate-700">
             Authorize Override
           </button>
           <button className="px-8 py-3 bg-vital/20 text-vital font-bold rounded-xl border border-vital/30 hover:bg-vital/30 transition-all">
             View Audit Logs
           </button>
        </div>
      </section>
    </motion.div>
  );
};

const AdminCard = ({ title, description, icon: Icon, status }: any) => (
  <div className="p-8 glass-card group border-white/5 hover:border-vital/30">
    <div className="flex justify-between items-start mb-6">
      <div className="p-4 bg-surface rounded-2xl text-slate-500 group-hover:text-vital transition-colors">
        <Icon size={24} />
      </div>
      <span className="text-[10px] font-black px-3 py-1.5 rounded-full bg-vital/10 text-vital border border-vital/20 uppercase tracking-widest">
        {status}
      </span>
    </div>
    <h3 className="text-xl font-bold mb-2">{title}</h3>
    <p className="text-xs text-slate-500 font-bold leading-relaxed">{description}</p>
  </div>
);
