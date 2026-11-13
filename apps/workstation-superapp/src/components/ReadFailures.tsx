// W928 — A READ THAT FAILS IS SAID. Since W927 every read checks its status, so a refusal reaches the read's catch; a
// catch that does nothing then leaves the page empty or loading with no sentence, and a reader cannot tell "there is
// nothing" from "this could not be read". A page notes each failed read here by what it was reading, and shows the
// list where its content starts, each with the server's own reason (the status and the detail it sent) or the fact
// that the server could not be reached.
import React, { useCallback, useState } from 'react';
import { axiosDetail, errorMessage } from '../lib/api';

/** The sentence for a failed read: an axios refusal carries its status and the server's detail; anything else is
 *  said by the shared helper (an ApiError's status and detail, an abort, or an unreachable server). */
export function describeReadFailure(e: unknown): string {
  const ax = e as { isAxiosError?: boolean; response?: { status?: number } };
  if (ax?.isAxiosError && typeof ax.response?.status === 'number') {
    return `Failed (HTTP ${ax.response.status}): ${axiosDetail(e, 'no reason given')}`;
  }
  return errorMessage(e);
}

export function useReadFailures() {
  const [failures, setFailures] = useState<Record<string, string>>({});
  /** `.catch(note('the entity types'))`: records what could not be read and why */
  const note = useCallback((what: string) => (e: unknown) => {
    setFailures(f => ({ ...f, [what]: describeReadFailure(e) }));
  }, []);
  /** a later read of the same thing that succeeds takes its failure off the list */
  const clear = useCallback((what: string) => {
    setFailures(f => {
      if (!(what in f)) return f;
      const rest = { ...f };
      delete rest[what];
      return rest;
    });
  }, []);
  return { failures, note, clear };
}

export const ReadFailures: React.FC<{ failures: Record<string, string> }> = ({ failures }) => {
  const items = Object.entries(failures);
  if (!items.length) return null;
  return (
    <div role="alert" data-testid="read-failures" className="space-y-1 rounded-xl border border-amber-500/30 bg-amber-500/5 p-3">
      {items.map(([what, why]) => (
        <p key={what} data-testid="read-failure" className="text-[11px] font-bold text-amber-400 leading-relaxed">
          Could not read {what} — {why}
        </p>
      ))}
    </div>
  );
};
