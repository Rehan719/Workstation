import React from 'react';

const FinOpsDashboard = () => (
  <div className="p-8 bg-white rounded-3xl shadow-2xl border border-blue-100">
    <h2 className="text-3xl font-black text-blue-900 mb-8">Autonomous FinOps Portal</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="p-8 bg-slate-50 rounded-2xl border border-slate-200">
        <h3 className="font-bold mb-4">Zakat Distribution (ARTICLE 245)</h3>
        <div className="space-y-4">
          <div className="flex justify-between text-sm">
            <span>Total Funds Collected:</span>
            <span className="font-bold">$42,500.00</span>
          </div>
          <div className="flex justify-between text-sm text-emerald-600">
            <span>Distributed to Date:</span>
            <span className="font-bold">$38,200.00</span>
          </div>
        </div>
      </div>
      <div className="p-8 bg-slate-50 rounded-2xl border border-slate-200">
        <h3 className="font-bold mb-4">Waqf Performance</h3>
        <p className="text-xs text-slate-500 mb-4">Long-term institutional sustainability tracking.</p>
        <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
          <div className="h-full bg-blue-500" style={{ width: '75%' }}></div>
        </div>
        <p className="text-[10px] mt-2 font-bold text-blue-600">75% OF ANNUAL TARGET MET</p>
      </div>
    </div>
  </div>
);

export default FinOpsDashboard;
