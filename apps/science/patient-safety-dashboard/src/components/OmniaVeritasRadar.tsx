import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts';

const OmniaVeritasRadar = ({ scores }: { scores: any }) => {
  const data = [
    { subject: 'Objective', A: scores.Truth_I_Objective, fullMark: 1.0 },
    { subject: 'Subjective', A: scores.Truth_II_Subjective, fullMark: 1.0 },
    { subject: 'Procedural', A: scores.Truth_III_Procedural, fullMark: 1.0 },
    { subject: 'Temporal', A: scores.Truth_IV_Temporal, fullMark: 1.0 },
    { subject: 'Predictive', A: scores.Truth_V_Predictive, fullMark: 1.0 },
    { subject: 'Ethical', A: scores.Truth_VI_Ethical, fullMark: 1.0 },
    { subject: 'Convergent', A: scores.Truth_VII_Convergent, fullMark: 1.0 },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="subject" />
          <PolarRadiusAxis angle={30} domain={[0, 1.0]} />
          <Radar
            name="Omnia-Veritas v18.0"
            dataKey="A"
            stroke="#8884d8"
            fill="#8884d8"
            fillOpacity={0.6}
          />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default OmniaVeritasRadar;
