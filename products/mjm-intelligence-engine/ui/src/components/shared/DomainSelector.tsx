import React from 'react';

const DomainSelector = ({ onSelect, selectedDomain }) => {
  const domains = [
    { id: 'patient_safety', name: 'Patient Safety & Long-Term Risk', icon: '🧬' },
    { id: 'uk_employment_tribunal', name: 'UK Employment Tribunal', icon: '⚖️' },
    { id: 'regulatory_submission', name: 'FDA/EMA Regulatory Submission', icon: '📋' },
    { id: 'commercial_strategy', name: 'Commercial Strategy', icon: '📈' },
  ];

  return (
    <div className="mb-8">
      <label className="block text-sm font-semibold text-gray-700 mb-2">Select Domain Genome</label>
      <div className="grid grid-cols-2 gap-4">
        {domains.map((domain) => (
          <button
            key={domain.id}
            onClick={() => onSelect(domain.id)}
            className={`flex items-center p-4 rounded-lg border-2 transition-all ${
              selectedDomain === domain.id
                ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                : 'border-gray-200 hover:border-indigo-300 bg-white'
            }`}
          >
            <span className="text-2xl mr-3">{domain.icon}</span>
            <div className="text-left">
              <div className="font-bold">{domain.name}</div>
              <div className="text-xs text-gray-500 uppercase tracking-tighter">Genome: {domain.id}</div>
            </div>
          </button>
        ))}
        <button className="flex items-center p-4 rounded-lg border-2 border-dashed border-gray-300 hover:border-gray-400 bg-gray-50 text-gray-500">
          <span className="text-2xl mr-3">➕</span>
          <div className="text-left font-bold">Create New Genome</div>
        </button>
      </div>
    </div>
  );
};

export default DomainSelector;
