import React from 'react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Tooltip, Legend } from 'recharts';

/**
 * Septima-Veritas Convergence Dashboard (v17.1)
 * Optimized for Scientific Review Excellence.
 */
const SeptimaVeritasRadar = ({ data, jurisdiction }) => {
  const chartData = [
    { subject: 'Truth I: Objective', A: data.dimension_scores.truth_i * 100 },
    { subject: 'Truth II: Subjective', A: data.dimension_scores.truth_ii * 100 },
    { subject: 'Truth III: Procedural', A: data.dimension_scores.truth_iii * 100 },
    { subject: 'Truth IV: Temporal', A: data.dimension_scores.truth_iv * 100 },
    { subject: 'Truth V: Predictive', A: data.dimension_scores.truth_v * 100 },
    { subject: 'Truth VI: Ethical', A: data.dimension_scores.truth_vi * 100 },
    { subject: 'Truth VII: Review', A: data.dimension_scores.truth_vii * 100 },
  ];

  return (
    <div className="septima-radar">
      <h3>Septima-Veritas Scientific Review ({jurisdiction})</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Scientific Convergence" dataKey="A" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.5} />
          <Tooltip />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
      <div className="scientific-meta">
        <strong>GRADE Quality Score: {data.methodological_metrics.grade_score}</strong>
        <p>Uncertainty Quantification: {Math.round(data.methodological_metrics.uncertainty_level * 100)}% (95% CI)</p>
      </div>
    </div>
  );
};

export default SeptimaVeritasRadar;
