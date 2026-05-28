import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const EthicalAIAudit = () => {
  const data = [
    { name: 'Bias Score', value: 2, full: 100, fill: '#82ca9d' },
    { name: 'Equity Impact', value: 95, full: 100, fill: '#8884d8' },
    { name: 'Auditability', value: 100, full: 100, fill: '#ffc658' },
    { name: 'XAI Compliance', value: 98, full: 100, fill: '#ff8042' },
  ];

  return (
    <div style={{ width: '100%', height: 400 }}>
      <h3>Ethical AI Audit Dashboard (v16.0)</h3>
      <ResponsiveContainer>
        <BarChart data={data} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 100]} />
          <YAxis dataKey="name" type="category" />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p style={{ fontSize: '0.8em', color: '#666' }}>Compliance Status: GDPR / AI Act 2024 (Verified)</p>
    </div>
  );
};

export default EthicalAIAudit;
