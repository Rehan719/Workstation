import { AgentVitals, SystemVitals, UserProfile, RealmType } from './types';

export interface BTOProduct {
  id: string;
  name: string;
  category: 'AGENT' | 'REACTOR' | 'REALM';
  price: string;
  description: string;
  specs: Record<string, string>;
}

export const mockBTOProducts: BTOProduct[] = [
  {
    id: 'bto-001',
    name: 'Sovereign C-Suite Cluster',
    category: 'AGENT',
    price: '2.5 WST',
    description: 'A pre-configured swarm of CFO, CTO, and CMO agents with unified memory.',
    specs: { 'Context Window': '128k', 'Consensus': 'Clownfish V2', 'Edge Ready': 'Yes' }
  },
  {
    id: 'bto-002',
    name: 'Knowledge Garden Node',
    category: 'REALM',
    price: '0.8 WST',
    description: 'Deploy a local instance of the Learner Realm with custom ontologies.',
    specs: { 'Storage': '50GB', 'Sync': 'Mycelial', 'Privacy': 'L5 Diff' }
  },
  {
    id: 'bto-003',
    name: 'PQC Gateway Reactor',
    category: 'REACTOR',
    price: '1.2 WST',
    description: 'Post-Quantum Cryptographic reactor for ultra-secure inter-node comms.',
    specs: { 'Protocol': 'Kyber-768', 'Latency': '<5ms', 'Throughput': '10Gbps' }
  }
];

export const mockAgentVitals: AgentVitals[] = [
  { id: '1', name: 'VSB AI CEO', role: 'EDITOR', status: 'ACTIVE', fitness: 0.98 },
  { id: '2', name: 'CFO Agent', role: 'MODEL', status: 'IDLE', fitness: 0.92 },
  { id: '3', name: 'CTO Agent', role: 'MODEL', status: 'THINKING', fitness: 0.95 },
  { id: '4', name: 'Immune Watcher', role: 'WATCHER', status: 'ACTIVE', fitness: 0.99 },
];

export const mockSystemVitals: SystemVitals = {
  cpu: 45.2,
  memory: 12.8,
  activeAgents: 24,
  swarmHealth: 0.96,
};

export const mockUserProfile: UserProfile = {
  id: 'user_001',
  email: 'guardian@vsb.ai',
  displayName: 'Conscious Guardian',
  role: 'ADMIN',
};

export const generateSimulationData = () => {
  const t = Date.now() / 1000;
  return {
    vitals: {
      cpu: 40 + Math.sin(t) * 10 + Math.random() * 5,
      memory: 12 + Math.cos(t * 0.5) * 2,
      activeAgents: Math.floor(25 + Math.sin(t * 0.2) * 5),
      swarmHealth: 0.95 + Math.sin(t * 0.1) * 0.05,
    },
    signals: [
      { id: 'sig-1', type: 'discovery', strength: Math.random() },
      { id: 'sig-2', type: 'synthesis', strength: Math.random() },
    ],
    timestamp: Date.now(),
  };
};
