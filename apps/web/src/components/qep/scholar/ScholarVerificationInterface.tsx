import React from 'react';

const ScholarVerificationInterface: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState<'Ijazah' | 'Content' | 'Endpoints'>('Ijazah');
  const [isVerifying, setIsVerifying] = React.useState(false);

  return (
    <div className="scholar-verification p-6 bg-slate-900 text-white rounded-xl shadow-2xl border border-slate-700">
      <div className="flex justify-between items-center mb-8 border-b border-slate-700 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-emerald-400">Scholar Governance Portal</h2>
          <p className="text-xs text-slate-500 font-mono mt-1">Sovereign Verification System v8.3</p>
        </div>
        <div className="scholar-badge flex items-center gap-2 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
          <span className="text-lg">📜</span>
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-emerald-400">DR. AL-HUSSARY</span>
            <span className="text-[8px] text-slate-500 font-mono">ID: SCH-001</span>
          </div>
        </div>
      </div>

      <div className="tabs flex gap-6 mb-8">
        {['Ijazah', 'Content', 'Endpoints'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            className={`text-sm font-bold pb-2 transition-all border-b-2 ${activeTab === tab ? 'text-emerald-400 border-emerald-400' : 'text-slate-500 border-transparent hover:text-slate-300'}`}
          >
            {tab} Reviews (2 Pending)
          </button>
        ))}
      </div>

      <div className="verification-item p-4 bg-slate-800/50 rounded-lg border border-slate-700 mb-4 hover:border-emerald-500/30 transition-all">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h3 className="text-lg font-semibold text-emerald-300 mb-1">
              {activeTab === 'Ijazah' ? 'New Ijazah Chain Verification: SC-001' :
               activeTab === 'Content' ? 'New Community Content: CONT-001' :
               'New API Endpoint Registration: quran-mirror-v1'}
            </h3>
            <p className="text-xs text-slate-400">Submitted by: <span className="text-emerald-500/80">Qari-Ahmad-Warsh</span></p>
          </div>
          <span className="text-[10px] bg-slate-700 text-slate-400 px-2 py-1 rounded">PRIORITY: HIGH</span>
        </div>

        {activeTab === 'Ijazah' && (
          <div className="chain-visualization mb-8 bg-slate-900/50 p-4 rounded border border-slate-700/50">
            <div className="flex flex-col items-center gap-3">
              <div className="transmitter p-2 bg-emerald-900/30 border border-emerald-500/40 rounded w-full text-center">
                <span className="text-xs font-bold text-emerald-400">Dr. Mahmoud Al-Hussary</span>
                <span className="block text-[8px] text-slate-500">Scholar ID: SCH-001</span>
              </div>
              <div className="h-4 w-0.5 bg-emerald-500/30"></div>
              <div className="transmitter p-2 bg-slate-800 border border-slate-700 rounded w-full text-center">
                <span className="text-xs font-bold">Sheikh Khalil Al-Husari</span>
                <span className="block text-[8px] text-slate-500">Transmitter ID: TR-005</span>
              </div>
              <div className="h-4 w-0.5 bg-emerald-500/30"></div>
              <div className="transmitter p-2 bg-slate-800 border border-slate-700 rounded w-full text-center">
                <span className="text-xs font-bold">Sheikh Muhammad Salam</span>
                <span className="block text-[8px] text-slate-500">Transmitter ID: TR-022</span>
              </div>
            </div>
          </div>
        )}

        <div className="actions flex gap-4 mt-8">
          <button
            disabled={isVerifying}
            className="flex-1 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded transition-colors text-sm shadow-lg shadow-emerald-900/20"
            onClick={() => {
              setIsVerifying(true);
              setTimeout(() => { setIsVerifying(false); alert('Verified & Logged to Audit Trail (VSB-V83-SIG-001)'); }, 1000);
            }}
          >
            {isVerifying ? 'Signing Transaction...' : 'Verify Chain & Sign'}
          </button>
          <button className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold rounded transition-colors text-sm border border-slate-700">
            Request Clarification
          </button>
          <button className="py-3 px-4 bg-red-900/30 hover:bg-red-900/50 text-red-400 font-bold rounded transition-colors text-sm border border-red-500/20">
            Reject
          </button>
        </div>
      </div>

      <div className="mt-8 p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-lg">
        <h4 className="text-emerald-400 font-bold mb-2 text-sm flex items-center gap-2">
          <span>📜</span> Scholar Protocol Note
        </h4>
        <p className="text-xs text-slate-400 leading-relaxed italic">
          All verification actions utilize a hybrid pattern: automated checks for schema/malicious content, followed by manual scholar signing for theological authenticity. Every signature generates a unique VSB-SIG-HASH.
        </p>
      </div>
    </div>
  );
};

export default ScholarVerificationInterface;
