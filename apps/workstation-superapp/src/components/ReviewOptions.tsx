// W925 (P5.15, RELEASE — the Owner's ruling of 2026-10-12): BOTH OPTIONS, shown where a tool is offered and before
// anything is typed into it — the tier of review the tool has reached, the option of a qualified person with when
// one is warranted, and what release would leave with a person. Every sentence is the server's
// (GET /api/v1/review-options, which reads the tool the route declares and the one tier function every answer
// passes through); this component types none of them. An endpoint that declares no tool shows the server's own
// sentence saying so. A failure to read is said, never hidden and never shown as a tier.
import React, { useEffect, useState } from 'react';
import { ApiError, apiJson, errorMessage } from '../lib/api';

interface ReviewOptionsAnswer {
  tool: string;
  discipline: string | null;
  review: { label: string; basis: string; known?: boolean };
  person: { option: string; warranted_when: string | null; release: string; basis: string };
}

export const ReviewOptions: React.FC<{ endpoint: string }> = ({ endpoint }) => {
  const [said, setSaid] = useState<ReviewOptionsAnswer | null>(null);
  const [none, setNone] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    let live = true;
    setSaid(null);
    setNone('');
    setError('');
    apiJson<ReviewOptionsAnswer>(`/api/v1/review-options?endpoint=${encodeURIComponent(endpoint)}`)
      .then(a => {
        if (!live) return;
        //  an answer without a tier and a person's option is not shown as one
        if (a?.review?.label && a?.person?.option) setSaid(a);
        else setError('the answer carried no tier of review and no option of a person');
      })
      .catch(e => {
        if (!live) return;
        if (e instanceof ApiError && e.status === 404) setNone(e.detail);
        else setError(errorMessage(e));
      });
    return () => { live = false; };
  }, [endpoint]);

  return (
    <div data-testid="review-options" className="mt-2 max-w-2xl space-y-1 border border-slate-800 rounded-lg p-2">
      {none ? (
        <p data-testid="review-options-none" className="text-[10px] text-slate-500 leading-relaxed">{none}</p>
      ) : error ? (
        <p data-testid="review-options-error" className="text-[10px] text-amber-400 leading-relaxed">
          The review this tool has reached could not be read, so none is shown. {error}
        </p>
      ) : !said ? (
        <p className="text-[10px] text-slate-600">Reading the review this tool has reached…</p>
      ) : (
        <>
          <p data-testid="review-option-tier" className="text-[10px] text-slate-400 leading-relaxed">
            <span className="font-black uppercase tracking-widest text-[9px] text-slate-300">Review reached: {said.review.label}</span>
            {' — '}{said.review.basis}.
          </p>
          <p data-testid="review-option-person" title={said.person.basis} className="text-[10px] text-slate-400 leading-relaxed">
            <span className="font-black uppercase tracking-widest text-[9px] text-slate-300">A qualified person</span>
            {' — '}{said.person.option}
            {said.person.warranted_when
              ? <span data-testid="review-option-warranted"> {said.person.warranted_when}</span>
              : <span data-testid="review-option-not-stated"> {said.person.basis}</span>}
          </p>
          <p data-testid="review-option-release" className="text-[10px] text-slate-500 leading-relaxed">{said.person.release}</p>
        </>
      )}
    </div>
  );
};
