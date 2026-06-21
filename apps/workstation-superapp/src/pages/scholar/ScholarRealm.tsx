import React, { useState } from 'react';
import { Card, Button, notImplemented, toast } from '@workstation/ui';
import { Database, Search, FlaskConical, Share2 } from 'lucide-react';

/**
 * ScholarRealm (v138.0 Phase 6)
 *
 * Target: Researchers.
 * Features: GraphQL query interface, experiment sandbox, reproducibility.
 */
export const ScholarRealm: React.FC = () => {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // Query the live Unified Event Graph (GaaS v5 constitutional audit log).
  const runQuery = async () => {
    setLoading(true);
    try {
      const r = await fetch('/api/v1/gaas/ueg/events?limit=10');
      const d = await r.json();
      const evs = Array.isArray(d?.events) ? [...d.events].reverse() : [];
      setEvents(evs);
      toast(`UEG returned ${evs.length} events`);
    } catch { toast('UEG query failed'); }
    setLoading(false);
  };

  return (
    <div className="space-y-10">
      <header>
        <h1 className="text-5xl font-black text-white uppercase">Observatory of Understanding</h1>
        <p className="text-slate-500 font-bold tracking-widest uppercase text-xs mt-2">Deep Intelligence Research Hub</p>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-4 gap-8">
        <aside className="space-y-6">
           <Card className="p-6">
              <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-4">Research Tools</h4>
              <div className="space-y-2">
                 <Button onClick={runQuery} className="w-full justify-start gap-3" variant="ghost"><Database size={16} /> UEG GraphQL</Button>
                 <Button onClick={() => notImplemented('Sandbox-X')} className="w-full justify-start gap-3" variant="ghost"><FlaskConical size={16} /> Sandbox-X</Button>
                 <Button onClick={() => notImplemented('Export DOI')} className="w-full justify-start gap-3" variant="ghost"><Share2 size={16} /> Export DOI</Button>
              </div>
           </Card>
        </aside>

        <main className="@[440px]:col-span-3 space-y-8">
           <Card className="p-10 border-dashed border-2 border-slate-800 bg-transparent flex flex-col items-center justify-center text-center space-y-6 min-h-[400px]">
              <div className="p-6 bg-slate-900 rounded-full text-slate-500">
                 <Search size={48} />
              </div>
              <div>
                 <h3 className="text-2xl font-black text-white">Execute Raw Query</h3>
                 <p className="text-slate-500 max-w-sm mx-auto mt-2">Query the Unified Event Graph across 50+ federated nodes with differential privacy constraints.</p>
              </div>
              <div className="w-full max-w-lg bg-slate-950 p-4 rounded-xl border border-slate-900 font-mono text-left text-aura text-sm">
                 query {"{"} events(limit: 10) {"{ type, source, timestamp }"} {"}"}
              </div>
              <Button onClick={runQuery} className="bg-aura text-sovereign px-10">{loading ? 'Querying…' : 'Execute Global Discovery'}</Button>
           </Card>

           {events.length > 0 && (
             <Card className="p-6 space-y-2">
               <h4 className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3">UEG Events ({events.length})</h4>
               {events.map((e: any) => (
                 <div key={e.id} className="flex items-center justify-between p-3 bg-slate-950 rounded-lg border border-slate-900 font-mono text-xs gap-3">
                   <span className="text-aura shrink-0">{e.data?.type ?? 'event'}</span>
                   <span className="text-slate-500 truncate">{e.data?.action ?? e.data?.reason ?? e.id}</span>
                 </div>
               ))}
             </Card>
           )}
        </main>
      </div>
    </div>
  );
};
