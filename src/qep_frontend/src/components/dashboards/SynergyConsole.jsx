import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import DigitalTwinVisualizer from '../twins/DigitalTwinVisualizer';
import { motion } from 'framer-motion';

const SynergyConsole = () => {
  const [activeWorkflow, setActiveWorkflow] = useState(null);
  const [telemetry, setTelemetry] = useState({ cpu: 45, memory: 62, api: 88 });

  const workflows = [
    { id: 'startup', name: 'Startup Ecosystem Mega-Twin', reactors: ['Law', 'Religion', 'Career'] },
    { id: 'edu', name: 'Educational Impact Mega-Twin', reactors: ['Education', 'Science'] },
    { id: 'fatwa', name: 'Fatwa Impact Mega-Twin', reactors: ['Fiqh', 'Finance', 'Dawah'] }
  ];

  return (
    <div className="synergy-console bg-slate-900 min-h-screen text-white p-8">
      <h1 className="text-4xl font-bold mb-8">v100.0 Synergy Console</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left: Workflow Selection */}
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
          <h2 className="text-xl font-semibold mb-4">Active Mega-Twin Workflows</h2>
          {workflows.map(wf => (
            <motion.div
              key={wf.id}
              whileHover={{ scale: 1.02 }}
              onClick={() => setActiveWorkflow(wf)}
              className={`p-4 mb-4 cursor-pointer rounded-lg border ${activeWorkflow?.id === wf.id ? 'border-amber-500 bg-amber-500/10' : 'border-slate-600 bg-slate-700'}`}
            >
              <div className="font-bold">{wf.name}</div>
              <div className="text-xs text-slate-400 mt-2">Reactors: {wf.reactors.join(' + ')}</div>
            </motion.div>
          ))}
        </div>

        {/* Center: 3D Twin Visualization */}
        <div className="lg:col-span-2 bg-slate-950 rounded-xl h-[500px] relative overflow-hidden border border-slate-800">
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <Suspense fallback={null}>
              <ambientLight intensity={0.5} />
              <pointLight position={[10, 10, 10]} />
              <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
              <DigitalTwinVisualizer twinData={activeWorkflow} />
              <OrbitControls enableZoom={false} />
            </Suspense>
          </Canvas>

          {/* Overlay: Telemetry HUD */}
          <div className="absolute top-4 right-4 bg-black/60 backdrop-blur-md p-4 rounded-lg border border-white/10 text-xs">
            <div className="mb-2">ARO TELEMETRY: ACTIVE</div>
            <div className="flex justify-between w-32 mb-1">
              <span>CPU Usage:</span>
              <span className="text-emerald-400">{telemetry.cpu}%</span>
            </div>
            <div className="flex justify-between w-32">
              <span>Fabric Load:</span>
              <span className="text-emerald-400">{telemetry.memory}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom: Analysis & RAL Logs */}
      <div className="mt-8 bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h2 className="text-xl font-semibold mb-4">System Event Log (RAL/BTO)</h2>
        <div className="font-mono text-sm text-emerald-400 bg-black p-4 rounded-lg h-32 overflow-y-auto">
          {activeWorkflow ? (
            <>
              <div>[RAL] ASSEMBLE pool_x99: COMPUTE(15), API(300) -> VERIFIED</div>
              <div>[BTO] VTF_{activeWorkflow.id} formed: Negotiating roles...</div>
              <div>[BTO] Leader: PhysicsAgent, Reviewer: TafsirAgent -> READY</div>
              <div>[ESE] Twin_{activeWorkflow.id} initialized. Fidelity: 0.985</div>
            </>
          ) : (
            <div>Waiting for workflow activation...</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SynergyConsole;
