import React from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';

const PentaVeritasRadar = ({ scores }) => {
  const data = [
    { subject: 'Truth I: Objective', A: scores.I * 100, fullMark: 100 },
    { subject: 'Truth II: Subjective', A: scores.II * 100, fullMark: 100 },
    { subject: 'Truth III: Procedural', A: scores.III * 100, fullMark: 100 },
    { subject: 'Truth IV: Temporal', A: scores.IV * 100, fullMark: 100 },
    { subject: 'Truth V: Predictive', A: scores.V * 100, fullMark: 100 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Penta-Veritas Convergence Matrix (5D)</h3>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Penta Convergence" dataKey="A" stroke="#ff7300" fill="#ff7300" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
      <div style={{ marginTop: 20 }}>
        <strong>Overall Penta Score: {(scores.overall * 100).toFixed(2)}%</strong>
        <p>Regulatory Sovereignty: Adaptive Inevitability (0.935+ threshold)</p>
      </div>
    </div>
  );
};

export default PentaVeritasRadar;
