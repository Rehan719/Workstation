import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Shield, Activity, Target, MessageSquare } from 'lucide-react';

const ConsciousnessPanel = () => {
  const [metrics, setMetrics] = useState({
    health: 'Optimal',
    pas: 98.4,
    uptime: 99.99,
    trust: 95.2
  });

  const [guidance, setGuidance] = useState('');
  const [response, setResponse] = useState('');

  const handleSeek = (e) => {
    e.preventDefault();
    if (guidance.toLowerCase().includes('purpose')) {
      setResponse('ARTICLE 336: The Workstation is founded upon a dual purpose: spiritual-ethical and operational-commercial.');
    } else {
      setResponse('ARTICLE 1: The system operates as a sovereign digital organism under constitutional governance.');
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-indigo-900 flex items-center">
          <Activity className="mr-2" /> Consciousness Center
        </h2>
        <div className="consciousness-orb h-6 w-6 rounded-full bg-green-500"></div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 uppercase tracking-wider">Purpose Alignment</p>
          <p className="text-xl font-bold text-indigo-700">{metrics.pas}%</p>
        </div>
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 uppercase tracking-wider">Uptime</p>
          <p className="text-xl font-bold text-indigo-700">{metrics.uptime}%</p>
        </div>
      </div>

      <div className="mb-6">
        <p className="text-sm italic text-gray-600 mb-2">"Seek the pleasure of the Creator through excellence in service to the creation."</p>
      </div>

      <form onSubmit={handleSeek} className="relative">
        <input
          type="text"
          value={guidance}
          onChange={(e) => setGuidance(e.target.value)}
          placeholder="Seek Constitutional Guidance..."
          className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gold-500 focus:outline-none pr-10"
        />
        <button type="submit" className="absolute right-2 top-2 text-gold-600">
          <Target size={20} />
        </button>
      </form>

      {response && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-indigo-50 text-indigo-900 rounded-lg text-sm font-medium"
        >
          {response}
        </motion.div>
      )}
    </div>
  );
};

export default ConsciousnessPanel;
