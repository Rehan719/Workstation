export type RealmType = 'LEARNER' | 'DEVELOPER' | 'ENTERPRISE' | 'SCHOLAR' | 'GENOME' | 'UNIFIED';
export type ModeType = 'ACTIVE' | 'REST' | 'EVOLUTION' | 'EMERGENCY';

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
  node_count?: number;
}

export interface UserProfile {
  id: string;
  did?: string;
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

export interface GaaSValidationResult {
  valid: boolean;
  allowed?: boolean; // Legacy support
  article_id?: number | string; // Legacy support
  score: number;
  articles: number[];
  remediation?: string;
  explanation?: string;
}
