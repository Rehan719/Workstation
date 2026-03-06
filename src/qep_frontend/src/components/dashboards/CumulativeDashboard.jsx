import React from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const CumulativeDashboard = ({ domain, data }) => {
  const themes = {
    religion: { primary: '#064e3b', secondary: '#f59e0b', label: 'Spiritual Mastery' },
    education: { primary: '#1e3a8a', secondary: '#10b981', label: 'Academic Proficiency' },
    business: { primary: '#111827', secondary: '#ec4899', label: 'Commercial Growth' },
    science: { primary: '#4c1d95', secondary: '#06b6d4', label: 'Research Impact' },
    law: { primary: '#7c2d12', secondary: '#facc15', label: 'Compliance Index' }
  };

  const theme = themes[domain] || themes.religion;

  const narrative = {
    religion: "Your spiritual path is blooming through consistent Quranic practice.",
    education: "Academic mastery is reaching peak performance in core standards.",
    science: "Research impact is surging with high-centrality citation links.",
    law: "Transborder compliance thresholds are being successfully maintained.",
    business: "Venture incubation cycle is approaching OCI deployment readiness."
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 rounded-xl shadow-2xl bg-white/10 backdrop-blur-xl border border-white/20 border-t-4"
      style={{ borderColor: theme.primary }}
    >
      <div className="flex justify-between items-center mb-8">
        <div>
          <h3 className="text-2xl font-bold text-white uppercase tracking-tighter">
            {theme.label} Dashboard
          </h3>
          <p className="text-xs text-white/60 mt-1 italic font-medium">{narrative[domain] || "Evolving..."}</p>
        </div>
        <div className="px-3 py-1 rounded-full text-xs font-semibold text-white shadow-inner" style={{ backgroundColor: theme.secondary }}>
          v99.0 TRANSCENDENT
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-64 mt-6">
        <div className="bg-black/20 backdrop-blur-sm p-4 rounded-lg border border-white/10">
          <p className="text-xs font-bold text-gray-400 mb-2 uppercase">Progress Timeline</p>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data.timeline}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" hide />
              <YAxis domain={[0, 100]} hide />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderRadius: '8px', border: 'none' }} />
              <Line
                type="monotone"
                dataKey="value"
                stroke={theme.secondary}
                strokeWidth={3}
                dot={{ fill: theme.secondary }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-black/20 backdrop-blur-sm p-4 rounded-lg border border-white/10">
          <p className="text-xs font-bold text-gray-400 mb-2 uppercase">Domain Distribution</p>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.distribution}>
              <XAxis dataKey="label" fontSize={10} tick={{ fill: 'rgba(255,255,255,0.5)' }} />
              <YAxis hide />
              <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ backgroundColor: '#1e293b', borderRadius: '8px', border: 'none' }} />
              <Bar dataKey="level" fill={theme.primary} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-8 flex gap-4 overflow-x-auto pb-2">
        {['Real-time Audit', 'Evolution Logs', 'Quantum Projection'].map((btn) => (
          <motion.button
            key={btn}
            whileHover={{ scale: 1.05, backgroundColor: 'rgba(255,255,255,0.2)' }}
            whileTap={{ scale: 0.95 }}
            className="whitespace-nowrap px-4 py-2 bg-white/10 text-white rounded-md text-sm font-medium transition-colors border border-white/10"
          >
            {btn}
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
};

export default CumulativeDashboard;
