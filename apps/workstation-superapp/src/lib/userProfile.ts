// §4.2 (W428) — the EXPLICIT user profile. Server-stored, owner-scoped, and used to shape what the
// platform generates for this person.
//
// Deliberately NOT the same thing as userPrefs.ts. Prefs are browser-local conveniences (display
// name, default realm, font scale). This is content the user writes about themselves that reaches
// generation prompts, so it lives on the server under their owner id — and, unlike the AI gateway's
// recall path, nothing here is inferred from anyone else's traffic. The user writes it, sees exactly
// what it sends, and can delete it.

import { apiJson } from '../lib/api';   // the path W927's census reads every apiJson caller's import by

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
  // W577 (FU-298) — the route reports when the stored document could only be read in part. Without
  // these the page cannot tell an empty profile from an unreadable one, and it offers a Save that
  // would overwrite what it could not show.
  profile_is_incomplete?: boolean;
  store_incomplete?: string | null;
}

// W980 (FU-399 part 13) - EACH OF THESE SAYS A REFUSAL WITH THE SERVER'S REASON. getProfile answered null for a
// refused read and for an unreachable server alike, which the page could only take for a profile never filled in;
// a refused save or clear said its status and dropped the reason (a refused save says nothing stored was lost).
// Each throws apiJson's ApiError now, with the status and the server's detail.
export async function getProfile(): Promise<ProfileResponse> {
  return apiJson<ProfileResponse>('/api/v1/user/profile');
}

export async function putProfile(p: UserProfile): Promise<ProfileResponse> {
  return apiJson<ProfileResponse>('/api/v1/user/profile', { method: 'PUT', body: p });
}

export async function clearProfile(): Promise<void> {
  await apiJson('/api/v1/user/profile', { method: 'DELETE' });
}
