import React, { useState, useEffect } from 'react';
import {
  Settings,
  ShieldAlert,
  Zap,
  Lightbulb,
  TestTube,
  FlaskConical,
  Factory,
  CheckCircle,
  AlertTriangle,
  Cpu,
  Download,
  Smartphone,
  Globe
} from 'lucide-react';

const FacilityCard = ({ id, name, icon: Icon, status, metrics, onOpen }) => (
  <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/50 transition-all cursor-pointer group" onClick={onOpen}>
    <div className="flex justify-between items-start mb-4">
      <div className="p-3 bg-cyan-500/10 rounded-lg text-cyan-400 group-hover:scale-110 transition-transform">
        <Icon size={24} />
      </div>
      <span className={`px-2 py-1 rounded text-xs font-bold ${
        status === 'online' ? 'bg-green-500/10 text-green-400' : 'bg-yellow-500/10 text-yellow-400'
      }`}>
        {status.toUpperCase()}
      </span>
    </div>
    <h3 className="text-xl font-bold text-white mb-2">{name}</h3>
    <div className="space-y-2">
      {Object.entries(metrics).map(([key, val]) => (
        <div key={key} className="flex justify-between text-sm">
          <span className="text-slate-400 capitalize">{key.replace('_', ' ')}:</span>
          <span className="text-cyan-300 font-mono">{val}</span>
        </div>
      ))}
    </div>
  </div>
);

const FacilityControlRoom = () => {
  const [selectedFacility, setSelectedFacility] = useState(null);
  const [safetyIncidents, setSafetyIncidents] = useState([
    { id: 1, type: 'Containment', facility: 'Reactors', msg: 'Theological anomaly detected in Surah Al-Baqarah Tafsir module.', time: '10 mins ago' },
    { id: 2, type: 'Isolation', facility: 'Petri Dishes', msg: 'A/B Test 09-B failed validation gate. Auto-rollback triggered.', time: '2 hours ago' }
  ]);

  const facilities = [
    {
      id: 'engines',
      name: 'Digital Engines',
      icon: Cpu,
      status: 'online',
      metrics: { throughput: '1.2k/hr', uptime: '99.99%', load: '42%' }
    },
    {
      id: 'reactors',
      name: 'Reactors',
      icon: Zap,
      status: 'online',
      metrics: { validation: '100%', containment: 'Ready', intensity: 'High' }
    },
    {
      id: 'incubators',
      name: 'Incubators',
      icon: Lightbulb,
      status: 'online',
      metrics: { graduation: '78%', active_concepts: '12', community: 'High' }
    },
    {
      id: 'petri_dishes',
      name: 'Petri Dishes',
      icon: TestTube,
      status: 'online',
      metrics: { isolation: '100%', stability: '99.5%', active_tests: '4' }
    },
    {
      id: 'laboratories',
      name: 'Laboratories',
      icon: FlaskConical,
      status: 'online',
      metrics: { research: '8 publications', ontology: '+12%', audits: 'Pass' }
    },
    {
      id: 'factories',
      name: 'Factories',
      icon: Factory,
      status: 'online',
      metrics: { yield: '99.9%', localization: '100%', backlog: 'Zero' }
    }
  ];

  return (
    <div className="min-h-screen bg-black text-slate-200 p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tighter flex items-center gap-3">
            <Factory className="text-cyan-500" /> INDUSTRIAL FACILITY CONTROL ROOM
          </h1>
          <p className="text-slate-500">QEP v8.8 Sovereign Signature | Production-Scale Management Layer</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-800 text-sm">
            <span className="text-slate-500 mr-2">GLOBAL HEALTH:</span>
            <span className="text-green-400 font-bold">OPTIMAL</span>
          </div>
          <div className="bg-cyan-500 text-black px-4 py-2 rounded-lg font-bold text-sm flex items-center gap-2">
            <ShieldAlert size={16} /> VSB SIGNATURE ACTIVE
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {facilities.map(f => (
          <FacilityCard key={f.id} {...f} onOpen={() => setSelectedFacility(f)} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Safety Incidents */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <ShieldAlert className="text-yellow-500" /> SAFETY & CONTAINMENT LOG
          </h2>
          <div className="space-y-4">
            {safetyIncidents.map(incident => (
              <div key={incident.id} className="p-4 bg-black/50 border-l-4 border-yellow-500 rounded-r-lg">
                <div className="flex justify-between mb-1">
                  <span className="text-xs font-bold text-yellow-500 uppercase">{incident.type}</span>
                  <span className="text-xs text-slate-600 font-mono">{incident.time}</span>
                </div>
                <p className="text-sm text-slate-300 font-medium">{incident.msg}</p>
                <div className="mt-2 text-xs text-slate-500 italic">Facility: {incident.facility}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Delivery & PWA */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Globe className="text-cyan-500" /> STANDALONE DELIVERY (PWA & MOBILE)
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-black/30 border border-slate-800 rounded-lg text-center group hover:bg-cyan-500/10 transition-all cursor-pointer">
              <Globe className="mx-auto mb-2 text-cyan-400" />
              <div className="text-sm font-bold text-white">Progressive Web App</div>
              <div className="text-xs text-slate-500 mb-3">Install on Desktop/Mobile</div>
              <button className="bg-cyan-500/20 text-cyan-300 px-3 py-1 rounded text-xs font-bold border border-cyan-500/30">INSTALL PWA</button>
            </div>
            <div className="p-4 bg-black/30 border border-slate-800 rounded-lg text-center">
              <Smartphone className="mx-auto mb-2 text-slate-500" />
              <div className="text-sm font-bold text-slate-400">Native Mobile Apps</div>
              <div className="text-xs text-slate-600 mb-3">iOS & Android (v8.8)</div>
              <div className="flex gap-2 justify-center">
                <button className="bg-slate-800 text-slate-500 px-2 py-1 rounded text-[10px] font-bold opacity-50 cursor-not-allowed">APP STORE</button>
                <button className="bg-slate-800 text-slate-500 px-2 py-1 rounded text-[10px] font-bold opacity-50 cursor-not-allowed">PLAY STORE</button>
              </div>
            </div>
            <div className="col-span-2 p-4 bg-cyan-500/5 border border-cyan-500/20 rounded-lg flex items-center justify-between">
              <div>
                <div className="text-sm font-bold text-cyan-300 flex items-center gap-2">
                   <Download size={16}/> Industrial Export Package
                </div>
                <div className="text-xs text-slate-500">Offline content factory ZIP (Full Signature)</div>
              </div>
              <button className="bg-cyan-500 text-black px-4 py-2 rounded font-bold text-xs">DOWNLOAD ZIP</button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal / Panel Placeholder */}
      {selectedFacility && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 w-full max-w-2xl rounded-2xl p-8 relative shadow-2xl">
            <button className="absolute top-4 right-4 text-slate-500 hover:text-white" onClick={() => setSelectedFacility(null)}>✕</button>
            <div className="flex items-center gap-4 mb-6">
              <div className="p-4 bg-cyan-500/20 rounded-xl text-cyan-400">
                <selectedFacility.icon size={32} />
              </div>
              <div>
                <h2 className="text-3xl font-black text-white">{selectedFacility.name.toUpperCase()}</h2>
                <p className="text-cyan-500/70 font-mono tracking-widest text-xs">FACILITY ID: {selectedFacility.id.toUpperCase()}-001</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="bg-black/40 p-4 rounded-lg border border-slate-800">
                <div className="text-xs text-slate-500 uppercase mb-1">Operational Protocol</div>
                <div className="text-sm font-bold text-slate-200">Standard Production (v8.8)</div>
              </div>
              <div className="bg-black/40 p-4 rounded-lg border border-slate-800">
                <div className="text-xs text-slate-500 uppercase mb-1">Safety Handler</div>
                <div className="text-sm font-bold text-slate-200">{selectedFacility.id === 'reactors' ? 'Containment (Active)' : 'Auto-Remediation'}</div>
              </div>
            </div>

            <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Live Throughput Data</h4>
            <div className="h-24 bg-black/60 rounded-lg mb-6 flex items-end justify-between p-2 gap-1 border border-slate-800">
              {[...Array(20)].map((_, i) => (
                <div key={i} className="bg-cyan-500/30 w-full rounded-t-sm" style={{ height: `${Math.random() * 100}%` }}></div>
              ))}
            </div>

            <button
              className="w-full py-4 bg-cyan-600 hover:bg-cyan-500 text-black font-black rounded-xl transition-colors uppercase tracking-widest"
              onClick={() => setSelectedFacility(null)}
            >
              Close Facility Monitor
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FacilityControlRoom;
