import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const HistoricalTrendOverlay = ({ data }: { data: any }) => {
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h4>Historical Convergence Trend (v13.0 - v18.0)</h4>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="version" />
          <YAxis domain={[0, 1.0]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="score" stroke="#82ca9d" strokeWidth={3} activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default HistoricalTrendOverlay;
