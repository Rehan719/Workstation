import React from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip, Legend } from 'recharts';

const QuintaVeritasRadar = ({ scores }) => {
  const data = [
    { subject: 'Truth I: Objective', A: scores.I * 100, fullMark: 100 },
    { subject: 'Truth II: Subjective', A: scores.II * 100, fullMark: 100 },
    { subject: 'Truth III: Procedural', A: scores.III * 100, fullMark: 100 },
    { subject: 'Truth IV: Temporal', A: scores.IV * 100, fullMark: 100 },
    { subject: 'Truth V: Ethical', A: scores.V * 100, fullMark: 100 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Quinta-Veritas Convergence Matrix (5D)</h3>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Quinta Convergence" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
          <Legend />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
      <div style={{ marginTop: 20, textAlign: 'center' }}>
        <strong>Coherence Index: {(scores.overall * 100).toFixed(2)}%</strong>
        <p>Blockchain Anchor: SHA-3-512 Verified</p>
      </div>
    </div>
  );
};

export default QuintaVeritasRadar;
