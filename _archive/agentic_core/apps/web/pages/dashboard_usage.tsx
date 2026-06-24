import { useEffect, useState } from 'react';
export default function DashboardUsage() {
  const [usage, setUsage] = useState({ used: 0, limit: 50 });
  useEffect(() => {
    fetch('/api/usage/status').then(r => r.json()).then(setUsage);
  }, []);
  return (
    <div className="p-4 border rounded bg-white shadow-sm">
      <h4 className="font-bold mb-2">Usage Monitor</h4>
      <p className="text-sm text-gray-600">Executions: {usage.used} / {usage.limit}</p>
      <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
        <div
          className="bg-blue-600 h-2.5 rounded-full"
          style={{ width: `${Math.min((usage.used / usage.limit) * 100, 100)}%` }}
        ></div>
      </div>
      {usage.used / usage.limit > 0.8 && (
        <p className="text-xs text-orange-600 mt-2 font-semibold">
          ⚠️ Approaching limit. <a href="/pricing" className="underline">Upgrade</a>
        </p>
      )}
    </div>
  );
}
