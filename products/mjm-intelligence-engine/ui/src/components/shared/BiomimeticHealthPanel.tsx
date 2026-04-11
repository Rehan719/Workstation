import React from 'react';

const HealthGauge = ({ title, value, threshold, trend }) => {
  const isHealthy = value >= threshold;
  const color = isHealthy ? 'text-green-600' : 'text-red-600';

  return (
    <div className="p-4 border rounded shadow-sm bg-gray-50">
      <h4 className="text-sm font-bold text-gray-500 uppercase">{title}</h4>
      <div className={`text-2xl font-mono ${color}`}>
        {(value * 100).toFixed(1)}%
      </div>
      <div className="text-xs text-gray-400">
        Threshold: {threshold * 100}% | Trend: {trend}
      </div>
    </div>
  );
};

const BiomimeticHealthPanel = ({ metrics }) => {
  if (!metrics) return <div>Loading vital signs...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6 bg-white rounded-lg shadow-inner">
      <HealthGauge
        title="🏠 Homeostasis"
        value={metrics.homeostasis.quality_score}
        threshold={0.95}
        trend={metrics.homeostasis.stability_trend}
      />
      <HealthGauge
        title="🧠 Adaptation"
        value={metrics.adaptation.learning_velocity}
        threshold={0.05}
        trend="improving"
      />
      <HealthGauge
        title="🛡️ Integrity"
        value={metrics.security.attestation_score}
        threshold={1.0}
        trend="stable"
      />
    </div>
  );
};

export default BiomimeticHealthPanel;
