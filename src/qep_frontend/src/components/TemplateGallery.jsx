import React, { useState } from 'react';
import { motion } from 'framer-motion';

const TemplateGallery = ({ onSelect }) => {
  const templates = [
    {
      id: 'qep-standard',
      title: 'Quranic Education Hub',
      category: 'Religion',
      description: 'Standard setup with Tajwid Coach, Hifz tracking, and study circles.',
      icon: '📖'
    },
    {
      id: 'business-sov',
      title: 'Sovereign Business',
      category: 'Business',
      description: 'E-commerce and FinOps ready. Sharia-compliant billing.',
      icon: '🏢'
    },
    {
      id: 'scholar-audit',
      title: 'Governance Portal',
      category: 'Law/Religion',
      description: 'Content review workflows and immutable audit logs.',
      icon: '⚖️'
    }
  ];

  return (
    <div className="p-8 bg-white/50 backdrop-blur-xl rounded-3xl border border-white/20 shadow-xl">
      <h3 className="text-2xl font-black text-slate-900 mb-6 flex items-center gap-3">
        <span className="w-2 h-6 bg-amber-500 rounded-full"></span>
        No-Code Template Gallery
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {templates.map(tpl => (
          <motion.div
            key={tpl.id}
            whileHover={{ y: -5 }}
            className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:border-amber-500/50 cursor-pointer group"
            onClick={() => onSelect(tpl)}
          >
            <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">{tpl.icon}</div>
            <div className="text-[10px] font-black text-amber-600 uppercase mb-1">{tpl.category}</div>
            <h4 className="text-lg font-bold text-slate-800 mb-2">{tpl.title}</h4>
            <p className="text-xs text-slate-500 leading-relaxed mb-6">{tpl.description}</p>
            <button className="w-full py-3 bg-slate-900 text-white text-xs font-black rounded-xl group-hover:bg-amber-500 transition-colors">
              Deploy Template
            </button>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default TemplateGallery;
