import React from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip } from 'recharts';

/**
 * Sexta-Veritas Convergence Dashboard (v17.0)
 * Visualization of six truth dimensions for Sovereign Patient Safety.
 */
const SextaVeritasRadar = ({ data, jurisdiction }) => {
  const chartData = [
    { subject: 'Truth I: Objective', A: data.dimension_scores.truth_i * 100 },
    { subject: 'Truth II: Subjective', A: data.dimension_scores.truth_ii * 100 },
    { subject: 'Truth III: Procedural', A: data.dimension_scores.truth_iii * 100 },
    { subject: 'Truth IV: Temporal', A: data.dimension_scores.truth_iv * 100 },
    { subject: 'Truth V: Ethical', A: data.dimension_scores.truth_v * 100 },
    { subject: 'Truth VI: Sovereign', A: data.dimension_scores.truth_vi * 100 },
  ];

  return (
    <div className="sexta-radar">
      <h4>Convergence Matrix ({jurisdiction})</h4>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Sovereign Convergence" dataKey="A" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
      <div className="convergence-meta">
        <strong>Score: {data.overall_score}</strong>
        <p>Status: {data.status}</p>
      </div>
    </div>
  );
};

export default SextaVeritasRadar;
