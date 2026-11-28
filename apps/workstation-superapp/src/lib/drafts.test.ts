// W1253 — what a person was typing is kept in this tab across a sign-in, for that account only, and dropped once used.
//
// lib/drafts.ts keeps a box's text in sessionStorage under the account the stored sign-in was issued to (the token's
// uid, W1198b). These cases drive it with made-up tokens shaped as the server's are (three dot-separated parts, the
// middle one the claims) and made-up text.
import { afterEach, describe, expect, it } from 'vitest';

import { GENESIS_DRAFT, converseDraft, draftOwner, dropDraft, keepDraft, takeDraft } from './drafts';

const tokenFor = (uid: string) => {
  const claims = btoa(JSON.stringify({ sub: 'w1253-made-up-name', uid, type: 'access' }))
    .replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_');
  return `w1253-made-up-head.${claims}.w1253-made-up-signature`;
};
const signIn = (uid: string) => localStorage.setItem('workstation_token', tokenFor(uid));
const IDEA = 'W1253 made up: a tool-lending library for one street';

describe('what a person was typing is kept across a sign-in, for that account only (W1253)', () => {
  afterEach(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  it('keeps a box\'s text for the account signed in, and gives it back to that account only', () => {
    signIn('w1253-made-up-uid-a');
    expect(draftOwner()).toBe('w1253-made-up-uid-a');
    expect(keepDraft(GENESIS_DRAFT, IDEA)).toBe(true);
    localStorage.removeItem('workstation_token');          // the session ended
    signIn('w1253-made-up-uid-a');                          // and the same person signed in again
    expect(takeDraft(GENESIS_DRAFT)).toBe(IDEA);
    expect(takeDraft(GENESIS_DRAFT)).toBe(IDEA);            // reading it leaves it kept until it is used
  });

  it('never shows one account\'s text to another: it is dropped unread', () => {
    signIn('w1253-made-up-uid-a');
    keepDraft(converseDraft('vsb-w1253-made-up'), IDEA);
    signIn('w1253-made-up-uid-b');
    expect(takeDraft(converseDraft('vsb-w1253-made-up'))).toBe('');
    signIn('w1253-made-up-uid-a');
    expect(takeDraft(converseDraft('vsb-w1253-made-up'))).toBe('');
    expect(sessionStorage.length).toBe(0);
  });

  it('keeps text with sign-in off, keeps nothing for a box left empty, and nothing under a sign-in it cannot read', () => {
    expect(draftOwner()).toBe('');
    expect(keepDraft(GENESIS_DRAFT, IDEA)).toBe(true);
    expect(takeDraft(GENESIS_DRAFT)).toBe(IDEA);
    expect(keepDraft(GENESIS_DRAFT, '   ')).toBe(false);
    expect(takeDraft(GENESIS_DRAFT)).toBe('');
    localStorage.setItem('workstation_token', 'w1253-made-up-not-a-token');
    expect(draftOwner()).toBeNull();
    expect(keepDraft(GENESIS_DRAFT, IDEA)).toBe(false);
    expect(sessionStorage.length).toBe(0);
  });

  it('is dropped once used, but not when the box was changed while the work was out', () => {
    signIn('w1253-made-up-uid-a');
    keepDraft(GENESIS_DRAFT, `${IDEA} `);
    expect(dropDraft(GENESIS_DRAFT, IDEA)).toBe(true);
    expect(takeDraft(GENESIS_DRAFT)).toBe('');
    keepDraft(GENESIS_DRAFT, `${IDEA}, and a second thought typed meanwhile`);
    expect(dropDraft(GENESIS_DRAFT, IDEA)).toBe(false);
    expect(takeDraft(GENESIS_DRAFT)).toBe(`${IDEA}, and a second thought typed meanwhile`);
  });
});
