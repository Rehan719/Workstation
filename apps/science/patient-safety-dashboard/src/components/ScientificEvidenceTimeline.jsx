import React from 'react';
import { ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ScientificEvidenceTimeline = () => {
  const data = [
    { name: '2021', impact: 20, studies: 5 },
    { name: '2023', impact: 45, studies: 12 },
    { name: '2025', impact: 98, studies: 25 },
    { name: '2026', impact: 92, studies: 30 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Scientific Evidence Evolution Timeline</h3>
      <ResponsiveContainer>
        <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid stroke="#f5f5f5" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="impact" fill="#8884d8" stroke="#8884d8" name="Evidence Impact (%)" />
          <Bar dataKey="studies" barSize={20} fill="#413ea0" name="Study Count" />
        </ComposedChart>
      </ResponsiveContainer>
      <p style={{ fontSize: '0.8em' }}>Key Breakthroughs: Wu et al. (2025), Chazarin et al. (2026)</p>
    </div>
  );
};

export default ScientificEvidenceTimeline;
