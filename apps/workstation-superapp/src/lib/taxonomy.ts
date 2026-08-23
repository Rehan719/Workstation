// §17.1 (W321) — the frontend's ONE Realm × Domain source, mirroring agentic_core/taxonomy.py
// (the canonical §2 taxonomy: 4 Realms × 6 Domains). The Round-6 audit found drifted per-page
// literals (five-realm lists, domains listed as realms, invented domains) — every routed surface
// now imports from here instead of re-declaring its own variant.
export const REALMS = ['enterprise', 'learning', 'developing', 'scholarship'] as const;
export const DOMAINS = ['religion', 'science', 'education', 'law', 'employment', 'care'] as const;

export const REALM_LABELS: Record<string, string> = {
  enterprise: 'Enterprise', learning: 'Learning', developing: 'Developing', scholarship: 'Scholarship',
};
export const DOMAIN_LABELS: Record<string, string> = {
  religion: 'Religion', science: 'Science', education: 'Education',
  law: 'Law', employment: 'Employment', care: 'Care',
};

// General-purpose workspace domains the backend tolerates as free text (normalise_domain passes
// them through) — for facility tools that operate outside the six named Domains.
export const WORKSPACE_DOMAINS = ['general', 'enterprise', 'technology', ...DOMAINS] as const;
