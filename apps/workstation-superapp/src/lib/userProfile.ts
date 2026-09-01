// §4.2 (W428) — the EXPLICIT user profile. Server-stored, owner-scoped, and used to shape what the
// platform generates for this person.
//
// Deliberately NOT the same thing as userPrefs.ts. Prefs are browser-local conveniences (display
// name, default realm, font scale). This is content the user writes about themselves that reaches
// generation prompts, so it lives on the server under their owner id — and, unlike the AI gateway's
// recall path, nothing here is inferred from anyone else's traffic. The user writes it, sees exactly
// what it sends, and can delete it.

export interface UserProfile {
  about_you: string;
  context: string;
  goals: string;
  constraints: string;
  success_criteria: string;
}

export const PROFILE_FIELDS: { key: keyof UserProfile; label: string; hint: string }[] = [
  { key: 'about_you', label: 'About you',
    hint: 'Who you are and what you do — background, role, level of expertise.' },
  { key: 'context', label: 'Your situation',
    hint: 'What you are working on and where it sits.' },
  { key: 'goals', label: 'What you are trying to achieve',
    hint: 'The outcome you actually want.' },
  { key: 'constraints', label: 'Constraints you work under',
    hint: 'Budget, time, staffing, regulation, anything that rules options out.' },
  { key: 'success_criteria', label: 'What success looks like',
    hint: 'How you will know this worked.' },
];

// Mirrors the server cap (agentic_core/ai/user_context.py MAX_FIELD_CHARS). The server trims
// regardless — this is a courtesy so the field does not silently lose text on save.
export const MAX_FIELD_CHARS = 600;

export const EMPTY_PROFILE: UserProfile = {
  about_you: '', context: '', goals: '', constraints: '', success_criteria: '',
};

interface ProfileResponse {
  owner_id: string;
  profile: UserProfile;
  preamble_preview: string;
  applied_to?: string;
  is_recall?: boolean;
}

export async function getProfile(): Promise<ProfileResponse | null> {
  try {
    const r = await fetch('/api/v1/user/profile');
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  }
}

export async function putProfile(p: UserProfile): Promise<ProfileResponse | null> {
  const r = await fetch('/api/v1/user/profile', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(p),
  });
  if (!r.ok) throw new Error(`Save failed (${r.status})`);
  return await r.json();
}

export async function clearProfile(): Promise<void> {
  const r = await fetch('/api/v1/user/profile', { method: 'DELETE' });
  if (!r.ok) throw new Error(`Clear failed (${r.status})`);
}
