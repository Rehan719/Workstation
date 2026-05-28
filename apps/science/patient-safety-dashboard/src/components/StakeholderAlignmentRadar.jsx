import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

const StakeholderAlignmentRadar = () => {
  const data = [
    { subject: 'Patients', A: 95, fullMark: 100 },
    { subject: 'Regulators', A: 85, fullMark: 100 },
    { subject: 'Organization', A: 90, fullMark: 100 },
    { subject: 'Clients', A: 80, fullMark: 100 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Stakeholder Alignment Radar</h3>
      <ResponsiveContainer>
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 100]} />
          <Radar name="Alignment Score" dataKey="A" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default StakeholderAlignmentRadar;
