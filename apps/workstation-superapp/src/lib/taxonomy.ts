// §17.1 (W321) — the frontend's ONE Realm × Domain source, mirroring agentic_core/taxonomy.py
// (the canonical §2 taxonomy: 4 Realms × 6 Domains). The Round-6 audit found drifted per-page
// literals (five-realm lists, domains listed as realms, invented domains) — every routed surface
// now imports from here instead of re-declaring its own variant.
export const REALMS = ['enterprise', 'learning', 'developing', 'scholarship'] as const;
export const DOMAINS = ['religion', 'science', 'education', 'law', 'employment', 'care'] as const;
// W619 (FU-502) — §17.1's third axis, mirroring agentic_core/taxonomy.py PRODUCTS. It had no frontend source,
// so no surface could choose a product and every journey recorded the backend's default.
export const PRODUCTS = ['reactor', 'incubator', 'factory', 'laboratory'] as const;
export const PRODUCT_LABELS: Record<string, string> = {
  reactor: 'Reactor — rapid AI generation', incubator: 'Incubator — iterative development',
  factory: 'Factory — production-grade delivery', laboratory: 'Laboratory — experimental and research',
};

export const REALM_LABELS: Record<string, string> = {
  enterprise: 'Enterprise', learning: 'Learning', developing: 'Developing', scholarship: 'Scholarship',
};
// W654 (FU-656, Owner ruling 2026-10-10) - what choosing a realm changes, in one line each. The realm sets the
// depth and register of what is written (agentic_core/taxonomy.py REALM_REGISTER holds the full instruction).
export const REALM_MEANS: Record<string, string> = {
  enterprise: 'Written for a commercial operator who has to act: decisions, costs, numbers, owners.',
  learning: 'Written for someone building understanding: terms defined, reasoning shown, worked examples.',
  developing: 'Written for building something new with limited means: innovation and technical work, in a resource-constrained setting.',
  scholarship: 'Written for a scholarly reader: precise claims, the limits of the evidence, competing readings.',
};
export const DOMAIN_LABELS: Record<string, string> = {
  religion: 'Religion', science: 'Science', education: 'Education',
  law: 'Law', employment: 'Employment', care: 'Care',
};

// P3.30 (ledger v16 R5.7) — how a domain VALUE is shown, mirroring agentic_core/taxonomy.py domain_label. The
// backend lets a free-text value through, so an entity can carry `enterprise` where one of the six domains is
// expected; a page printed it as if it were one. A member shows its label; anything else is named as outside.
export const domainLabel = (value: unknown): string => {
  const v = String(value ?? '').trim().toLowerCase();
  if (!v) return 'no domain recorded';
  return (DOMAINS as readonly string[]).includes(v) ? DOMAIN_LABELS[v] : `${v} — general (outside the six domains)`;
};

// General-purpose workspace domains the backend tolerates as free text (normalise_domain passes
// them through) — for facility tools that operate outside the six named Domains.
export const WORKSPACE_DOMAINS = ['general', 'enterprise', 'technology', ...DOMAINS] as const;
