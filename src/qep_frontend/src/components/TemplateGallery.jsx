import React, { useState } from 'react';
import { motion } from 'framer-motion';

const TemplateGallery = ({ onSelect }) => {
  const templates = [
    { id: 'qep-std', title: 'Quranic Hub', category: 'Religion', icon: '📖' },
    { id: 'hifz-track', title: 'Hifz Tracker', category: 'Religion', icon: '🕋' },
    { id: 'tajwid-coach', title: 'Tajwid Coach', category: 'Religion', icon: '🗣️' },
    { id: 'revert-support', title: 'Revert Path', category: 'Religion', icon: '🌱' },
    { id: 'study-circle', title: 'Halaqa Manager', category: 'Religion', icon: '👥' },
    { id: 'business-sov', title: 'Sovereign Biz', category: 'Business', icon: '🏢' },
    { id: 'zakat-calc', title: 'Zakat Portal', category: 'Business', icon: '💰' },
    { id: 'waqf-endow', title: 'Waqf Manager', category: 'Business', icon: '📜' },
    { id: 'finops-core', title: 'FinOps Suite', category: 'Business', icon: '📈' },
    { id: 'legal-advisor', title: 'Legal Counsel', category: 'Law', icon: '⚖️' },
    { id: 'compliance-aud', title: 'Compliance Audit', category: 'Law', icon: '📋' },
    { id: 'contract-gen', title: 'Contract Smith', category: 'Law', icon: '🖋️' },
    { id: 'research-hub', title: 'Research Reactor', category: 'Science', icon: '🧪' },
    { id: 'bio-forge', title: 'Bio Forge', category: 'Science', icon: '🧬' },
    { id: 'quantum-sim', title: 'Quantum Lab', category: 'Science', icon: '⚛️' },
    { id: 'career-kit', title: 'Career Launch', category: 'Employment', icon: '🚀' },
    { id: 'job-readiness', title: 'Job Ready AI', category: 'Employment', icon: '👔' },
    { id: 'skill-mapper', title: 'Skill Map', category: 'Employment', icon: '🗺️' },
    { id: 'edu-portal', title: 'Education Portal', category: 'Education', icon: '🎓' },
    { id: 'curriculum-gen', title: 'Curriculum AI', category: 'Education', icon: '📚' },
    { id: 'student-dash', title: 'Student Insight', category: 'Education', icon: '📊' },
    { id: 'community-forum', title: 'Community Hub', category: 'Social', icon: '🌐' },
    { id: 'dawah-outreach', title: 'Dawah Mission', category: 'Social', icon: '📣' },
    { id: 'vga-explorer', title: 'Governance Viz', category: 'Governance', icon: '🛡️' },
    { id: 'ceo-dashboard', title: 'AI CEO Ops', category: 'Executive', icon: '👑' }
  ];

  return (
    <div className="p-8 bg-white/50 backdrop-blur-xl rounded-3xl border border-white/20 shadow-xl">
      <h3 className="text-2xl font-black text-slate-900 mb-6 flex items-center gap-3">
        <span className="w-2 h-6 bg-amber-500 rounded-full"></span>
        Professional Template Gallery (25+ Starters)
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {templates.map(tpl => (
          <motion.div
            key={tpl.id}
            whileHover={{ scale: 1.05 }}
            className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 hover:border-amber-500/50 cursor-pointer group text-center"
            onClick={() => onSelect(tpl)}
          >
            <div className="text-3xl mb-2">{tpl.icon}</div>
            <div className="text-[8px] font-black text-amber-600 uppercase mb-1">{tpl.category}</div>
            <h4 className="text-xs font-bold text-slate-800 truncate">{tpl.title}</h4>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default TemplateGallery;
