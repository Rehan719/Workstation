import React, { useEffect, useState } from 'react';

// W737 (cluster F: FU-1020, 1013, 967, 739) — WHAT THIS MACHINE CAN SERVE, SAID BEFORE A FORM IS FILLED.
// Pages promised "builds", "marks", "best-in-class capability on demand" above forms that, with no model
// installed, return the floor's frame and say so only inside the answer. This reads the server's own status
// (GET /api/v1/native-ai/status: is_real_model, mode, active_model_label) once per page load and says, in one
// sentence, which it is NOW. It never guesses: an unread status is said as not known.

export type Status = { is_real_model?: boolean; mode?: string; active_model_label?: string; floor_active?: boolean };

let cached: Promise<Status | null> | null = null;
//  W959 (FU-1181) - a status that cannot be read is null, and every reader says null as "could not be read"
const statusNotKnown = (): null => null;
const readStatus = (): Promise<Status | null> => {
  if (!cached) {
    cached = fetch('/api/v1/native-ai/status')
      .then(r => (r.ok ? r.json() : null))
      .catch(statusNotKnown);
  }
  return cached;
};

// W866 (FU-1013) - the floor verdict, named once, so a page that says more than the sentence reads the same verdict
export const servingIsFloor = (s: Status): boolean =>
  s.floor_active === true || s.is_real_model === false || s.mode === 'deterministic_floor';

export const servingSentence = (s: Status | null | undefined): string => {
  if (!s) return 'What is serving on this deployment could not be read just now, so nothing is claimed about it.';
  if (servingIsFloor(s)) {
    return 'On this deployment right now no owned model is serving: a form here returns a structured frame built '
      + 'from what you type, not model-written work.';
  }
  return `On this deployment right now an owned model is serving (${s.active_model_label || 'a local model'}): a form `
    + 'here returns that model\'s draft, which is not reviewed by a person unless the result says so.';
};

// W866 (FU-1013) - the same one read, for a page that says more than the sentence: undefined while it is read,
// null when it could not be
export const useServingStatus = (): Status | null | undefined => {
  const [status, setStatus] = useState<Status | null | undefined>(undefined);
  useEffect(() => { let live = true; readStatus().then(s => { if (live) setStatus(s); }); return () => { live = false; }; }, []);
  return status;
};

export const ServingNow: React.FC<{ className?: string }> = ({ className }) => {
  const status = useServingStatus();
  if (status === undefined) return null;
  return (
    <p data-testid="serving-now" className={className ?? 'text-[10px] text-amber-400/80 mt-1 max-w-2xl leading-relaxed'}>
      {servingSentence(status)}
    </p>
  );
};
