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

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 rounded-xl shadow-2xl bg-white border-t-4"
      style={{ borderColor: theme.primary }}
    >
      <div className="flex justify-between items-center mb-8">
        <h3 className="text-2xl font-bold text-gray-800 uppercase tracking-tighter">
          {theme.label} Dashboard
        </h3>
        <div className="px-3 py-1 rounded-full text-xs font-semibold text-white shadow-inner" style={{ backgroundColor: theme.secondary }}>
          v99.0 TRANSCENDENT
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 h-64">
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-xs font-bold text-gray-400 mb-2 uppercase">Progress Timeline</p>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data.timeline}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" hide />
              <YAxis domain={[0, 100]} hide />
              <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Line
                type="monotone"
                dataKey="value"
                stroke={theme.primary}
                strokeWidth={3}
                dot={{ fill: theme.primary }}
                activeDot={{ r: 8, stroke: theme.secondary, strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-xs font-bold text-gray-400 mb-2 uppercase">Domain Distribution</p>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.distribution}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="label" fontSize={10} />
              <YAxis hide />
              <Tooltip />
              <Bar dataKey="level" fill={theme.secondary} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-8 flex gap-4 overflow-x-auto pb-2">
        {['Real-time Audit', 'Evolution Logs', 'Quantum Projection'].map((btn) => (
          <motion.button
            key={btn}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="whitespace-nowrap px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-md text-sm font-medium transition-colors"
          >
            {btn}
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
};

export default CumulativeDashboard;
