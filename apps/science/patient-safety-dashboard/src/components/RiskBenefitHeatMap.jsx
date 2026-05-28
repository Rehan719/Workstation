import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RiskBenefitHeatMap = () => {
  const data = [
    { x: 10, y: 90, z: 200, name: 'Status Quo', risk: 'Critical', benefit: 'Low' },
    { x: 50, y: 40, z: 300, name: 'Defensive Data', risk: 'Moderate', benefit: 'Moderate' },
    { x: 90, y: 10, z: 400, name: 'Proactive Leadership', risk: 'Low', benefit: 'High' },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Strategic Risk-Benefit Heat Map</h3>
      <ResponsiveContainer>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <XAxis type="number" dataKey="x" name="Commercial Opportunity" unit="%" />
          <YAxis type="number" dataKey="y" name="Patient Risk" unit="%" />
          <ZAxis type="number" dataKey="z" range={[100, 1000]} name="Investment" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Legend />
          <Scatter name="Strategic Options" data={data} fill="#8884d8" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskBenefitHeatMap;
