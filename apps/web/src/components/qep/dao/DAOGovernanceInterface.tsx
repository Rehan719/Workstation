import React, { useState } from 'react';
import { Vote, FileText, CheckCircle2, XCircle, Users, LayoutDashboard } from 'lucide-react';

export const DAOGovernanceInterface: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'source' | 'moderation' | 'ledger'>('source');

  const sourceProposals = [
    { id: 'prop-a1', proposer: 'scholar_01', description: 'Primary Quranic Text (Quran.com)', status: 'Approved', votes: { yes: 120, no: 5 } },
    { id: 'prop-b2', proposer: 'contributor_02', description: 'Tafsir Ibn Kathir (English Translation)', status: 'Pending', votes: { yes: 45, no: 12 } },
    { id: 'prop-c3', proposer: 'scholar_04', description: 'Sahih Muslim (Integrated API)', status: 'Pending', votes: { yes: 88, no: 3 } }
  ];

  const moderationProposals = [
    { id: 'mod-x1', moderator: 'mod_01', content: 'Lesson 10: Advanced Tajweed', status: 'Approved', votes: { yes: 50, no: 2 } },
    { id: 'mod-y2', moderator: 'mod_03', content: 'Tafsir Module: Al-Kahf', status: 'Pending', votes: { yes: 12, no: 8 } }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tighter flex items-center gap-2">
          <Vote className="w-8 h-8 text-rose-600" />
          Decentralized Governance
        </h2>
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('source')}
            className={`px-4 py-2 rounded-xl text-xs font-black uppercase transition-all ${activeTab === 'source' ? 'bg-rose-600 text-white shadow-lg' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
          >
            Source Proposals
          </button>
          <button
            onClick={() => setActiveTab('moderation')}
            className={`px-4 py-2 rounded-xl text-xs font-black uppercase transition-all ${activeTab === 'moderation' ? 'bg-rose-600 text-white shadow-lg' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
          >
            Moderation
          </button>
          <button
            onClick={() => setActiveTab('ledger')}
            className={`px-4 py-2 rounded-xl text-xs font-black uppercase transition-all ${activeTab === 'ledger' ? 'bg-rose-600 text-white shadow-lg' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
          >
            Sovereign Ledger
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          {activeTab === 'source' && (
            sourceProposals.map((prop) => (
              <div key={prop.id} className="p-5 bg-white border-2 border-slate-100 rounded-2xl hover:border-rose-200 transition-colors group">
                 <div className="flex justify-between items-start mb-3">
                   <div>
                     <div className="text-xs font-bold text-slate-400 uppercase mb-1">{prop.id} • Proposer: {prop.proposer}</div>
                     <div className="text-base font-black text-slate-800">{prop.description}</div>
                   </div>
                   <div className={`px-2 py-1 rounded text-[10px] font-black uppercase ${prop.status === 'Approved' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                     {prop.status}
                   </div>
                 </div>
                 <div className="flex items-center gap-4">
                   <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden flex">
                      <div className="bg-emerald-500 h-full" style={{ width: `${(prop.votes.yes / (prop.votes.yes + prop.votes.no)) * 100}%` }}></div>
                      <div className="bg-rose-500 h-full" style={{ width: `${(prop.votes.no / (prop.votes.yes + prop.votes.no)) * 100}%` }}></div>
                   </div>
                   <div className="text-xs font-black text-slate-500 uppercase">{prop.votes.yes + prop.votes.no} Votes</div>
                   <button className="px-4 py-2 bg-slate-900 text-white text-[10px] font-black uppercase rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                     Vote
                   </button>
                 </div>
              </div>
            ))
          )}

          {activeTab === 'moderation' && (
            moderationProposals.map((prop) => (
              <div key={prop.id} className="p-5 bg-white border-2 border-slate-100 rounded-2xl hover:border-rose-200 transition-colors group">
                 <div className="flex justify-between items-start mb-3">
                   <div>
                     <div className="text-xs font-bold text-slate-400 uppercase mb-1">{prop.id} • Moderator: {prop.moderator}</div>
                     <div className="text-base font-black text-slate-800">{prop.content}</div>
                   </div>
                   <div className={`px-2 py-1 rounded text-[10px] font-black uppercase ${prop.status === 'Approved' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                     {prop.status}
                   </div>
                 </div>
                 <div className="flex gap-4">
                   <div className="flex items-center gap-1 text-[10px] font-black text-emerald-600 uppercase bg-emerald-50 px-2 py-1 rounded">
                     <CheckCircle2 className="w-3 h-3" /> Approve: {prop.votes.yes}
                   </div>
                   <div className="flex items-center gap-1 text-[10px] font-black text-rose-600 uppercase bg-rose-50 px-2 py-1 rounded">
                     <XCircle className="w-3 h-3" /> Reject: {prop.votes.no}
                   </div>
                 </div>
              </div>
            ))
          )}

          {activeTab === 'ledger' && (
             <div className="p-8 bg-slate-900 rounded-3xl border-2 border-slate-800 text-center space-y-4">
                <Users className="w-12 h-12 text-rose-500 mx-auto" />
                <h3 className="text-xl font-black text-white uppercase tracking-widest">Sovereign Governance Ledger</h3>
                <p className="text-slate-400 text-xs font-bold max-w-md mx-auto leading-relaxed uppercase">
                  Proof of reputation, voting power, and contribution rewards. All ledger entries are cryptographically signed and immutable.
                </p>
                <div className="grid grid-cols-2 gap-4 mt-8">
                   <div className="p-4 bg-slate-800 rounded-xl border border-slate-700">
                      <div className="text-[10px] font-black text-slate-500 uppercase mb-1 tracking-tighter">Total Governance Tokens</div>
                      <div className="text-2xl font-black text-white">45,820</div>
                   </div>
                   <div className="p-4 bg-slate-800 rounded-xl border border-slate-700">
                      <div className="text-[10px] font-black text-slate-500 uppercase mb-1 tracking-tighter">Verified Contributors</div>
                      <div className="text-2xl font-black text-white">1,245</div>
                   </div>
                </div>
             </div>
          )}
        </div>

        <div className="space-y-6">
          <div className="p-6 bg-slate-50 border-2 border-slate-200 rounded-2xl space-y-4">
            <h3 className="text-xs font-black text-slate-800 uppercase flex items-center gap-2">
               <LayoutDashboard className="w-4 h-4 text-rose-600" />
               DAO Statistics
            </h3>
            <div className="space-y-3">
               {[
                 { label: 'Avg Consensus Delay', value: '4.2 hrs', icon: '⏱️' },
                 { label: 'Participation Rate', value: '78.5%', icon: '📈' },
                 { label: 'Theological Approval', value: '99.8%', icon: '📖' }
               ].map((stat) => (
                 <div key={stat.label} className="flex justify-between items-center p-2 bg-white rounded-lg border border-slate-100 shadow-sm">
                    <div className="text-[10px] font-bold text-slate-500 uppercase flex items-center gap-1">
                      <span>{stat.icon}</span> {stat.label}
                    </div>
                    <div className="text-xs font-black text-slate-800">{stat.value}</div>
                 </div>
               ))}
            </div>
          </div>

          <div className="p-6 bg-indigo-900 rounded-2xl text-white space-y-3 relative overflow-hidden">
             <div className="relative z-10">
               <h4 className="text-xs font-black uppercase mb-1">Your Voting Power</h4>
               <div className="text-3xl font-black tracking-tighter">1,245 QEP</div>
               <div className="text-[10px] font-bold text-indigo-300 uppercase mt-2">Active Multiplier: 1.2x (Senior Scholar)</div>
             </div>
             <FileText className="absolute bottom-[-10px] right-[-10px] w-24 h-24 text-indigo-800 rotate-12" />
          </div>
        </div>
      </div>
    </div>
  );
};
