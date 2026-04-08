import React from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';

/**
 * Quadra-Veritas Convergence Dashboard (D3.js-inspired React Component)
 * Visualization of four truth dimensions for Science Grand Operation v13.0.
 */
const QuadraVeritasRadar = ({ scores }) => {
  const data = [
    { subject: 'Truth I: Objective Record', A: scores.I * 100, fullMark: 100 },
    { subject: 'Truth II: Subjective Narrative', A: scores.II * 100, fullMark: 100 },
    { subject: 'Truth III: Procedural Compliance', A: scores.III * 100, fullMark: 100 },
    { subject: 'Truth IV: Temporal Intelligence', A: scores.IV * 100, fullMark: 100 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Quadra-Veritas Convergence Matrix</h3>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Science Convergence" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
      <div style={{ marginTop: 20 }}>
        <strong>Overall Convergence Score: {(scores.overall * 100).toFixed(2)}%</strong>
        <p>Strategic Sovereignty: Adaptive Inevitability (0.92+ threshold)</p>
      </div>
    </div>
  );
};

export default QuadraVeritasRadar;
