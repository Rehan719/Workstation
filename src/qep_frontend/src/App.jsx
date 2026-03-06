import React, { useState, useEffect } from 'react';
import HifzHeatMap from './components/HifzHeatMap';
import CumulativeDashboard from './components/dashboards/CumulativeDashboard';
import ImmersiveBackground from './components/immersive/ImmersiveBackground';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [status, setStatus] = useState('Initializing Digital Sanctuary...');
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [userProfile, setUserProfile] = useState({
    name: 'Abdullah',
    tazkiyah: 84,
    nurPoints: 1240,
    completedJuz: [1, 2, 3, 4, 18, 36, 67, 112, 113, 114]
  });

  const mockData = {
    timeline: [
      { name: 'W1', value: 45 }, { name: 'W2', value: 52 }, { name: 'W3', value: 48 },
      { name: 'W4', value: 61 }, { name: 'W5', value: 75 }, { name: 'W6', value: 84 }
    ],
    distribution: [
      { label: 'Science', level: 85 }, { label: 'Law', level: 40 },
      { label: 'Faith', level: 95 }, { label: 'Career', level: 60 }, { label: 'Edu', level: 75 }
    ]
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setStatus('v99.0 Transcendent Organism: Active');
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  const pageVariants = {
    initial: { opacity: 0, x: -20 },
    in: { opacity: 1, x: 0 },
    out: { opacity: 0, x: 20 }
  };

  return (
    <div className="dashboard-container font-inter relative min-h-screen flex">
      <ImmersiveBackground domain={activeTab === 'Dashboard' ? 'religion' : activeTab.toLowerCase()} />
      <aside className="sidebar bg-slate-900/80 backdrop-blur-xl text-white w-72 p-8 flex flex-col border-r border-white/10 relative z-10">
        <div className="mb-12">
          <motion.h2
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="text-3xl font-black text-amber-500 tracking-tighter"
          >
            JULES AI
          </motion.h2>
          <p className="text-[10px] uppercase tracking-[0.2em] opacity-50 font-bold">Transcendent v99.0</p>
        </div>

        <nav className="flex-1 space-y-2">
          {['Dashboard', 'Education', 'Science', 'Law', 'Employment', 'Scholar'].map((tab) => (
            <NavItem
              key={tab}
              label={tab === 'Dashboard' ? 'Sovereign Core' : `${tab} Reactor`}
              active={activeTab === tab}
              onClick={() => setActiveTab(tab)}
            />
          ))}
        </nav>

        <div className="pt-6 border-t border-white/10">
          <div className="text-[10px] uppercase opacity-50 font-bold mb-1">AI CEO Status</div>
          <div className="text-xs text-amber-500 font-mono">STRATEGIC_ALIGNMENT_OK</div>
        </div>
      </aside>

      <main className="content-area flex-1 p-12 overflow-y-auto relative z-10">
        <header className="flex justify-between items-start mb-12">
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
            <h1 className="text-5xl font-black text-white mb-2">As-salaam Alaykum, {userProfile.name}</h1>
            <p className="text-slate-400 text-lg">Elevating your potential across five transcendent domains.</p>
          </motion.div>
          <div className="bg-emerald-500/10 text-emerald-400 px-6 py-3 rounded-2xl font-bold shadow-sm text-sm border border-emerald-500/30 backdrop-blur-md">
            {status}
          </div>
        </header>

        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            variants={pageVariants}
            initial="initial"
            animate="in"
            exit="out"
            transition={{ type: 'tween', ease: 'anticipate', duration: 0.4 }}
          >
            {activeTab === 'Dashboard' && (
              <div className="space-y-12">
                <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <StatCard label="Tazkiyah" value={userProfile.tazkiyah} sub="+5.2% growth" color="emerald" />
                  <StatCard label="Nur Points" value={userProfile.nurPoints} sub="Top 5% Global" color="amber" />
                  <StatCard label="Active Streak" value="12 Days" sub="Ramadan Ready" color="blue" />
                  <StatCard label="Mastery" value="Level 9" sub="Cross-Domain" color="purple" />
                </section>

                <CumulativeDashboard domain="religion" data={mockData} />

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
                    <h3 className="text-xl font-bold mb-6 text-slate-800">Hifz Progress Matrix</h3>
                    <HifzHeatMap completedJuz={userProfile.completedJuz} />
                  </div>

                  <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
                    <h3 className="text-xl font-bold mb-6 text-slate-800">Business Incubation Pulse</h3>
                    <div className="space-y-4">
                      <div className="p-4 bg-slate-50 rounded-xl flex justify-between items-center">
                        <span className="font-semibold text-slate-600">Sovereign Entity Readiness</span>
                        <span className="text-emerald-600 font-bold">98%</span>
                      </div>
                      <div className="p-4 bg-slate-50 rounded-xl flex justify-between items-center">
                        <span className="font-semibold text-slate-600">Quantum Search Speedup</span>
                        <span className="text-blue-600 font-bold">142x</span>
                      </div>
                      <div className="p-4 bg-slate-50 rounded-xl flex justify-between items-center">
                        <span className="font-semibold text-slate-600">Market Intelligence Score</span>
                        <span className="text-purple-600 font-bold">8.9</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab !== 'Dashboard' && activeTab !== 'Scholar' && (
               <CumulativeDashboard domain={activeTab.toLowerCase()} data={mockData} />
            )}

            {activeTab === 'Scholar' && (
              <div className="bg-white p-12 rounded-3xl shadow-2xl border border-emerald-100">
                <h2 className="text-3xl font-black text-emerald-900 mb-8 flex items-center gap-3">
                  <span className="w-2 h-8 bg-emerald-500 rounded-full"></span>
                  Scholar Governance Portal
                </h2>
                <div className="space-y-6">
                  <ReviewItem title="v99.0 AI Tafsir (Surah An-Nur)" type="CONTENT" status="PENDING" />
                  <ReviewItem title="Educator Accreditation: Dr. Yusuf" type="IDENTITY" status="APPROVED" />
                  <ReviewItem title="Refined Tazkiyah Calculation" type="POLICY" status="PENDING" />
                </div>
                <button className="mt-12 w-full py-4 bg-emerald-900 text-emerald-50 rounded-xl font-bold hover:bg-emerald-800 transition-all shadow-lg">
                  Access Immutable Audit Ledger
                </button>
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        <footer className="mt-20 pt-8 border-t border-gray-200 opacity-40 text-[11px] font-bold uppercase tracking-widest text-center">
          Sovereign Business Entity: SOV_V99 | Powered by Transcendent Workstation | Article 265 Compliant
        </footer>
      </main>
    </div>
  );
}

function NavItem({ label, active, onClick }) {
  return (
    <motion.div
      whileHover={{ x: 5 }}
      className={`px-6 py-4 rounded-xl cursor-pointer transition-all flex items-center gap-4 ${
        active ? 'bg-amber-500 text-slate-900 font-black shadow-lg shadow-amber-500/20' : 'text-slate-400 hover:text-white hover:bg-white/5'
      }`}
      onClick={onClick}
    >
      <div className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-slate-900' : 'bg-transparent'}`}></div>
      {label}
    </motion.div>
  );
}

function StatCard({ label, value, sub, color }) {
  const colors = {
    emerald: 'text-emerald-400 bg-emerald-900/20 border-emerald-500/30 backdrop-blur-md',
    amber: 'text-amber-400 bg-amber-900/20 border-amber-500/30 backdrop-blur-md',
    blue: 'text-blue-400 bg-blue-900/20 border-blue-500/30 backdrop-blur-md',
    purple: 'text-purple-400 bg-purple-900/20 border-purple-500/30 backdrop-blur-md'
  };

  return (
    <motion.div
      whileHover={{ y: -5 }}
      className={`p-6 rounded-2xl border shadow-sm ${colors[color]}`}
    >
      <div className="text-3xl font-black mb-1">{value}</div>
      <div className="text-xs font-bold uppercase opacity-70 tracking-tighter">{label}</div>
      <div className="text-[10px] mt-2 font-medium opacity-60 italic">{sub}</div>
    </motion.div>
  );
}

function ReviewItem({ title, type, status }) {
  return (
    <div className="flex justify-between items-center p-6 border-b border-gray-100 last:border-0 hover:bg-emerald-50/30 transition-colors">
      <div className="space-y-1">
        <h4 className="font-bold text-slate-800">{title}</h4>
        <span className="text-[10px] font-black text-slate-400 bg-slate-100 px-2 py-0.5 rounded">TYPE: {type}</span>
      </div>
      <div className="flex items-center gap-6">
        <span className={`text-xs font-black ${status === 'PENDING' ? 'text-amber-600' : 'text-emerald-600'}`}>
          {status}
        </span>
        <button className="px-4 py-2 border border-gray-200 rounded-lg text-xs font-bold hover:bg-white hover:shadow-md transition-all text-slate-600">
          Review
        </button>
      </div>
    </div>
  );
}

export default App;
