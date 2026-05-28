import React, { useEffect, useState } from 'react';

interface QuotaInfo {
  model: string;
  used: number;
  limit: number;
  remaining: number;
  health: 'healthy' | 'warning';
}

export const AICapabilityDashboard: React.FC = () => {
  const [quotas, setQuotas] = useState<QuotaInfo[]>([]);
  const [activeTasks, setActiveTasks] = useState<number>(0);

  useEffect(() => {
    const fetchQuotas = async () => {
      try {
        const response = await fetch('/api/v1/ai/quotas');
        const data = await response.json();
        setQuotas(data);
      } catch (e) {
        console.error('Failed to fetch AI quotas', e);
      }
    };

    fetchQuotas();
    const interval = setInterval(fetchQuotas, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 bg-slate-900 text-white rounded-2xl shadow-2xl border border-slate-800">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-extrabold flex items-center">
          <span className="mr-3 text-blue-500">🤖</span> AI Engine Evolution
        </h2>
        <div className="px-3 py-1 bg-green-900/30 text-green-400 text-xs rounded-full border border-green-700">
          Sovereign AI v60.1
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {quotas.map((q) => (
          <QuotaCard key={q.model} quota={q} />
        ))}
      </div>

      <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
        <h3 className="text-sm font-semibold mb-3 text-slate-400">Hybrid Orchestration Status</h3>
        <div className="flex space-x-4">
          <StatusBadge label="DeepSeek (Ingestion)" status="ACTIVE" color="bg-blue-500" />
          <StatusBadge label="Qwen (Law)" status="ACTIVE" color="bg-purple-500" />
          <StatusBadge label="Minimax (Code)" status="ACTIVE" color="bg-orange-500" />
        </div>
      </div>
    </div>
  );
};

const QuotaCard: React.FC<{ quota: QuotaInfo }> = ({ quota }) => {
  const percentage = Math.round((quota.used / quota.limit) * 100) || 0;
  const color = quota.health === 'healthy' ? 'bg-blue-500' : 'bg-yellow-500';

  return (
    <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 hover:border-blue-500/50 transition-all">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-bold uppercase tracking-wider">{quota.model}</span>
        <span className={`text-[10px] ${quota.health === 'healthy' ? 'text-blue-400' : 'text-yellow-400'}`}>
          {quota.health.toUpperCase()}
        </span>
      </div>
      <div className="h-2 bg-slate-700 rounded-full overflow-hidden mb-3">
        <div className={`h-full ${color}`} style={{ width: `${percentage}%` }}></div>
      </div>
      <div className="flex justify-between text-xs text-slate-400 font-mono">
        <span>{quota.used.toLocaleString()} / {quota.limit.toLocaleString()}</span>
        <span>{percentage}%</span>
      </div>
    </div>
  );
};

const StatusBadge: React.FC<{ label: string; status: string; color: string }> = ({ label, status, color }) => (
  <div className="flex items-center space-x-2 bg-slate-900/50 px-3 py-2 rounded-lg border border-slate-700">
    <div className={`w-2 h-2 rounded-full ${color} animate-pulse`}></div>
    <div className="flex flex-col">
      <span className="text-[10px] text-slate-500">{label}</span>
      <span className="text-xs font-bold text-slate-200">{status}</span>
    </div>
  </div>
);
