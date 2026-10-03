"""The output refinery — and it no longer reports a confidence nothing measured.

W547 (P3.17, FU-233) — WHAT THIS PIPELINE CLAIMED, measured by driving it.

  (a) A CONFIDENCE THAT ROSE WITH THE NUMBER OF RETRIES. It began at 0.90 and added 0.05 per refinement
      pass, which is backwards on its face: more attempts at an output is weaker evidence for it, not
      stronger. Nothing measured anything at any point.
  (b) AND IT RETURNED 1.05. The enforcement it is constructed with
      (OmniEnforcementPatternSupreme) fails closed on a missing validator and no validator is
      registered, so `val.passed` is always False, the early return is unreachable, the loop always runs
      three iterations, and 0.90 + 0.05 x 3 leaves the pipeline reporting a confidence ABOVE UNITY. Its
      pydantic model accepted it because the field was an unbounded float. That figure was then attached
      to every emission the recirculation loop produced, on the path the heartbeat runs.
  (c) "REFINEMENT" WAS A STRING APPEND. Each pass appended the literal "(Self-Refined)", so the measured
      output of three refinement iterations was the draft followed by that phrase three times.
  (d) CERTIFICATION WAS str.replace. `_polish` rewrote "Action result" to "Certified Sovereign Action
      Outcome" and "reasoned outcome" to "Certified Strategic Outcome". Renaming text does not certify
      it, and the word Certified is the strongest claim in the sentence.
  (e) IT PASSED A RANDOM VECTOR AS AN INPUT. `np.random.rand(6)` went to the MoE call as though it were
      a real signal, and a bare `except:` swallowed whatever happened next.
  (f) constitutional_articles=[18, 19, 20] was a literal attached on the success path only — article
      numbers cited by nothing that read them.

WHAT IT REPORTS NOW: the iteration count (real), the enforcement's own three-state verdict with its
reason, and no confidence at all, because nothing here produces one. A threshold to compare a confidence
against is declared per mode in mode_controller and read by nothing; that is recorded there.
"""
from typing import Any, List, Optional, Dict
from pydantic import BaseModel


class FinalOutput(BaseModel):
    content: str
    #  Optional, and None in practice: a bounded float would still have invited a figure, and the honest
    #  answer is that this pipeline has no measurement to report.
    confidence_score: Optional[float]
    confidence_basis: str
    #  three-state: True, False, or None when no verdict could be obtained
    verification_passed: Optional[bool]
    verification_basis: str
    refinement_iterations: int
    refinement_basis: str
    constitutional_articles: List[int]
    articles_basis: str
    expert_trace: Dict[str, Any]


_MAX_ITERATIONS = 3


class VRPRPipeline:
    def __init__(self, ueg, enforcement, moe=None):
        self.ueg, self.enforcement, self.moe = ueg, enforcement, moe

    async def process(self, draft, context):
        it, curr, trace = 0, draft, {}
        verdict = None
        verdict_reason = ""
        refined_by = []

        while it <= _MAX_ITERATIONS:
            val = self.enforcement.validate(curr)
            verdict = getattr(val, "passed", None)
            verdict_reason = (getattr(val, "violation", None) or "")
            #  THE EARLY RETURN IS ON THE VERDICT ALONE. It used to require `conf >= 0.95` as well, so a
            #  cleared output still had to survive the retry counter before it could be returned.
            if verdict is True:
                return self._final(curr, it, trace, verdict, verdict_reason, refined_by, polished=True)
            it += 1
            if it > _MAX_ITERATIONS:
                break
            if self.moe:
                try:
                    #  NO RANDOM VECTOR. `np.random.rand(6)` was passed here as though it carried
                    #  information; a generator's output is not a signal, and the MoE could not tell it
                    #  from one. The call is made with the context it was given, or not at all.
                    moe_res = await self.moe.execute_moe_supreme(
                        f"Refine: {curr[:50]}", None, context, self.enforcement)
                    trace[f"it_{it}"] = moe_res
                    curr = f"{curr}\n\n{moe_res}" if isinstance(moe_res, str) else curr
                    refined_by.append("moe")
                except Exception as e:                   # noqa: BLE001 — recorded, never swallowed
                    trace[f"it_{it}"] = {"moe_failed": f"{e.__class__.__name__}: {e}"}
                    refined_by.append("moe_failed")
            else:
                #  NOT A REFINEMENT, and it no longer pretends to be one. The text is returned unchanged
                #  and the record says no refiner was available, where it used to append "(Self-Refined)"
                #  and count the pass as work.
                refined_by.append("none_available")

        return self._final(curr, it - 1, trace, verdict, verdict_reason, refined_by, polished=False)

    def _final(self, content, iterations, trace, verdict, verdict_reason, refined_by, polished):
        """One constructor for both exits, so neither can carry a field the other lacks."""
        _real = [r for r in refined_by if r == "moe"]
        return FinalOutput(
            #  NO str.replace CERTIFICATION. The polished exit returns the same text as the other one:
            #  what distinguished them was renaming a phrase to include the word Certified.
            content=content,
            confidence_score=None,
            #  The mechanism, not the resulting number. The first draft of this sentence typed the figure
            #  the old arithmetic produced, which a reader cannot verify from the string and which would
            #  become wrong the moment the arithmetic described changed. The starting value, the
            #  increment and the pass count are all stated, so the figure is recomputable from here.
            confidence_basis=(f"NOT MEASURED: nothing in this pipeline produces a confidence. The figure "
                              f"that stood here started at a declared 0.90 and gained a declared 0.05 per "
                              f"refinement pass — so it rose with the number of RETRIES rather than with "
                              f"any evidence — over a loop that ran its full {_MAX_ITERATIONS} passes on "
                              f"every run, because the enforcement it consults refuses while no validator "
                              f"is registered. Multiply it out to see what it reported"),
            verification_passed=verdict,
            verification_basis=(
                f"the enforcement pattern returned passed={verdict!r}"
                + (f" with violation {verdict_reason!r}" if verdict_reason else "")
                + (". A None verdict means no check could be obtained, which is not a pass"
                   if verdict is None else "")),
            refinement_iterations=iterations,
            refinement_basis=(
                f"{iterations} pass(es); {len(_real)} applied a real refiner ({', '.join(refined_by) or 'none'}). "
                f"A pass with no refiner available changes nothing and is counted as a pass, not as work"),
            #  cited only where something actually cleared, and even then as a CITATION rather than a
            #  finding, because nothing in this pipeline evaluates an article
            constitutional_articles=([18, 19, 20] if polished else []),
            articles_basis=("these article numbers are the ones this pipeline has always cited on a "
                            "cleared output. Nothing here evaluates an article's content, so they name "
                            "the articles the enforcement pattern is meant to cover rather than "
                            "findings against them"
                            if polished else
                            "no article is cited, because nothing cleared"),
            expert_trace=trace,
        )
