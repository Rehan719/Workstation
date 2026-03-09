import React from 'react';
import { motion } from 'framer-motion';

const ScholarDashboard = () => (
  <div className="p-8 bg-white rounded-3xl shadow-2xl border border-emerald-100">
    <h2 className="text-3xl font-black text-emerald-900 mb-8 flex items-center gap-3">
      <span className="w-2 h-8 bg-emerald-500 rounded-full"></span>
      Scholar Governance Portal
    </h2>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div className="p-6 bg-emerald-50 rounded-2xl border border-emerald-100">
        <p className="text-[10px] font-black text-emerald-600 uppercase">Pending Review</p>
        <p className="text-4xl font-black text-emerald-900">14</p>
      </div>
      <div className="p-6 bg-amber-50 rounded-2xl border border-amber-100">
        <p className="text-[10px] font-black text-amber-600 uppercase">Active Vetoes</p>
        <p className="text-4xl font-black text-amber-900">3</p>
      </div>
      <div className="p-6 bg-blue-50 rounded-2xl border border-blue-100">
        <p className="text-[10px] font-black text-blue-600 uppercase">Accredited Teachers</p>
        <p className="text-4xl font-black text-blue-900">128</p>
      </div>
    </div>
    <div className="space-y-4">
      <div className="p-4 border-b border-gray-100 flex justify-between items-center">
        <div>
          <p className="font-bold">v99.0 AI Tafsir (Surah An-Nur)</p>
          <span className="text-[8px] font-black bg-slate-100 px-2 py-1 rounded">CONTENT_REVIEW</span>
        </div>
        <button className="px-6 py-2 bg-emerald-600 text-white rounded-lg font-bold text-xs">VET / APPROVE</button>
      </div>
    </div>
  </div>
);

export default ScholarDashboard;
