export type RealmType = 'LEARNER' | 'DEVELOPER' | 'ENTERPRISE' | 'SCHOLAR' | 'UNIFIED';

export interface AgentVitals {
  id: string;
  name: string;
  role: 'MODEL' | 'EDITOR' | 'WATCHER';
  status: 'IDLE' | 'ACTIVE' | 'THINKING' | 'ERROR';
  fitness: number;
}

export interface SystemVitals {
  cpu: number;
  memory: number;
  activeAgents: number;
  swarmHealth: number;
}

export interface UserProfile {
  id: string;
  email: string;
  displayName: string;
  role: 'ADMIN' | 'USER' | 'GUEST';
}

export interface CommunicationChannel {
  id: string;
  name: string;
  icon: string;
  description: string;
}
