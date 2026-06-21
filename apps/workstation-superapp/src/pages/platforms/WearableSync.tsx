import React from 'react';
import { Card, Badge, Button, notImplemented, toast } from '@workstation/ui';

const syncVitals = async () => {
  try {
    const r = await fetch('/api/v1/frontier/platform/wearable/sync', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ device: 'Apple Watch Ultra', heart_rate: 72, steps: 4200, focus_score: 0.86 }),
    });
    const d = await r.json();
    toast(`Vitals ${d.status} — biometric signal fired to organism`);
  } catch { toast('Sync failed'); }
};
import { Watch, Smartphone, Bluetooth, Wifi, Activity, ShieldCheck, History, Info, ChevronRight, Zap, Bell, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';

export const WearableSync: React.FC = () => {
  const devices = [
    { id: 'w-1', name: 'Apple Watch Ultra', status: 'Connected', battery: '84%', type: 'WatchOS' },
    { id: 'w-2', name: 'Pixel Watch 2', status: 'Idle', battery: '42%', type: 'Wear OS' },
  ];

  return (
    <div className="space-y-12 pb-24">
      <header className="flex flex-col @[480px]:flex-row @[480px]:justify-between @[480px]:items-end gap-6">
        <div>
          <h1 className="text-3xl @[480px]:text-4xl @[680px]:text-6xl font-black mb-1 text-white tracking-tighter break-words">Wearable Sync</h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Glanceable Notifications • Haptic Alerts • Phase 3</p>
        </div>
        <div className="flex gap-4 flex-wrap shrink-0">
           <Button onClick={() => notImplemented('Pair Device')} variant="outline"><Bluetooth size={18} /> Pair Device</Button>
           <Button onClick={syncVitals} className="bg-aura text-sovereign shadow-xl shadow-aura/20">
              <Watch size={18} /> Sync Vitals
           </Button>
        </div>
      </header>

      <div className="grid grid-cols-1 @[440px]:grid-cols-12 gap-10">
         <main className="@[440px]:col-span-8 space-y-10">
            <Card className="p-10 space-y-10">
               <h3 className="text-2xl font-black text-white flex items-center gap-4 uppercase tracking-tight">
                  <Watch size={24} className="text-aura" />
                  Active Peripherals
               </h3>

               <div className="space-y-4">
                  {devices.map((device, i) => (
                    <motion.div
                      key={device.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="p-8 rounded-[2.5rem] bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all cursor-pointer"
                    >
                       <div className="flex items-center gap-8">
                          <div className="w-14 h-14 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-aura group-hover:bg-aura group-hover:text-sovereign transition-all">
                             <Watch size={24} />
                          </div>
                          <div>
                             <p className="text-lg font-black text-white mb-1 uppercase tracking-widest">{device.name}</p>
                             <div className="flex items-center gap-4 text-[10px] font-black text-slate-500 uppercase">
                                <span>{device.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-800" />
                                <span className="text-emerald-500">{device.battery} Charged</span>
                             </div>
                          </div>
                       </div>
                       <div className="flex items-center gap-6">
                          <Badge color={device.status === 'Connected' ? 'emerald-500' : 'slate-500'}>{device.status}</Badge>
                          <Button onClick={() => notImplemented('Configure')} variant="outline" className="px-6 py-3">Configure</Button>
                       </div>
                    </motion.div>
                  ))}
               </div>
            </Card>

            <Card className="p-10 space-y-10">
               <div className="flex justify-between items-center">
                  <h3 className="text-2xl font-black text-white uppercase tracking-tight flex items-center gap-4">
                     <Bell size={24} className="text-aura" />
                     Glanceable Alerts
                  </h3>
                  <Badge color="aura">Real-time Push</Badge>
               </div>

               <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { title: 'Treaty Ratified', desc: 'Alliance tr-142 ratified by council.', icon: ShieldCheck, time: '2m ago' },
                    { title: 'Care Alert', desc: 'Rest period required for learner agent.', icon: Bell, time: '14m ago' },
                  ].map((alert, i) => (
                    <div key={i} className="p-6 rounded-[2rem] bg-slate-950 border border-slate-900 flex items-start gap-5">
                       <div className="w-10 h-10 rounded-xl bg-slate-900 flex items-center justify-center text-aura flex-shrink-0">
                          <alert.icon size={20} />
                       </div>
                       <div>
                          <p className="text-xs font-black text-white uppercase tracking-widest mb-1">{alert.title}</p>
                          <p className="text-[10px] font-bold text-slate-500 leading-relaxed">{alert.desc}</p>
                          <p className="text-[8px] font-black text-slate-700 uppercase mt-2">{alert.time}</p>
                       </div>
                    </div>
                  ))}
               </div>
            </Card>
         </main>

         <aside className="@[440px]:col-span-4 space-y-10">
            <Card className="p-10 space-y-8 bg-aura/5 border-aura/20">
               <div className="w-16 h-16 rounded-2xl bg-aura flex items-center justify-center text-sovereign shadow-xl shadow-aura/20">
                  <Activity size={32} />
               </div>
               <div>
                  <h4 className="text-2xl font-black text-white mb-2 uppercase tracking-tight">Haptic Feedback</h4>
                  <p className="text-sm text-slate-400 font-bold leading-relaxed">
                     Enable bi-directional vitals sync. Pulse events will trigger subtle haptic markers on your wrist.
                  </p>
               </div>
               <div className="space-y-4 pt-6 border-t border-aura/10">
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Sync Frequency</span>
                     <span className="text-white">Continuous</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-black uppercase text-slate-500">
                     <span>Encryption</span>
                     <span className="text-emerald-500">AES-PQC</span>
                  </div>
               </div>
               <Button onClick={syncVitals} className="w-full bg-aura text-sovereign py-5 rounded-2xl font-black text-[10px] uppercase tracking-widest">Enable Sync</Button>
            </Card>

            <Card className="p-8 border-slate-800">
               <div className="flex items-center gap-4 text-slate-500">
                  <Info size={24} />
                  <p className="text-[10px] font-black uppercase tracking-widest leading-relaxed">
                     Wearable modules support watchOS, Wear OS, and Fitbit integration via the Unified Mobile Bridge.
                  </p>
               </div>
            </Card>
         </aside>
      </div>
    </div>
  );
};
