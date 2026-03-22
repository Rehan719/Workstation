export type RealmType = 'LEARNER' | 'DEVELOPER' | 'ENTERPRISE' | 'SCHOLAR' | 'UNIFIED' | 'SOVEREIGN';
export type AppMode = 'REST' | 'WORK' | 'PLAY';

export interface AgentVitals {
  id: string;
  name: string;
  role: 'MODEL' | 'EDITOR' | 'WATCHER';
  status: 'IDLE' | 'ACTIVE' | 'THINKING' | 'ERROR';
  fitness: number;
  did?: string;
  lineage?: string[];
  article_ref?: string;
}

export interface SystemVitals {
  cpu: number;
  memory: number;
  activeAgents: number;
  swarmHealth: number;
  cl1_efficiency?: number;
  latency_ms?: number;
  node_count?: number;
}

export interface UserProfile {
  id: string;
  email: string;
  displayName: string;
  role: 'ADMIN' | 'USER' | 'GUEST';
  persona?: RealmType;
  did?: string;
  mode?: AppMode;
}

export interface CommunicationChannel {
  id: string;
  name: string;
  icon: string;
  description: string;
}

export interface GenomicMetadata {
  root_hash: string;
  integrity_status: 'VERIFIED' | 'TAMPERED';
  regulon_count: number;
  active_transcription_factors: number;
  methylation_markers: string[];
}

export interface GaaSValidationResult {
  allowed: boolean;
  article_id: string;
  explanation: string;
  trust_score: number;
}
