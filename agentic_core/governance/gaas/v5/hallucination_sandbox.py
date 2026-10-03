import asyncio
import hashlib
from typing import Dict, Any, List, Optional
from agentic_core.ueg.logger import VSBUEGLogger

class HallucinationSandbox:
    """
    Validation Sandbox for LLM Outputs.
    Prevents unverified or hallucinated claims from entering the UEG.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.knowledge_base = {
            "v-infinity": "Master converged biogeospheric architecture",
            "mjm-v5": "12,000-dimensional hyperdimensional meta-learning",
            "gaas-v4": "Constitutional governance middleware"
        }

    def screen(self, output: str) -> Dict[str, Any]:
        """The two heuristics, SYNCHRONOUSLY. No logging, no awaiting, no side effect.

        W555 (FU-363) — THIS EXISTS SO THERE IS ONE SCREEN AND NOT TWO. validate_output was async only
        because it awaits a UEG write, and the constitutional validator interface is synchronous, so
        hallucination_containment could never assess on the live path — the recirculation loop is always
        inside an event loop. The alternative was to copy these two heuristics into the validator, which
        would have created a second screen over the same subject and the two copies would have drifted.
        The screening is extracted instead; validate_output keeps its signature, its arithmetic and its
        threshold, and adds the log.

        WHICH CHECKS RAN IS REPORTED, not assumed. The diversity check divides by the word count, so on
        an output with no words it CANNOT RUN — and it previously raised ZeroDivisionError there, which
        the interceptor did not guard. A check that did not run is not a check that passed, so it is
        named in `checks_not_run` and `passed` is None rather than a verdict.
        """
        score = 1.0
        hallucinations: List[str] = []
        ran: List[str] = []
        not_run: Dict[str, str] = {}

        # Simple keyword-based verification
        for key, fact in self.knowledge_base.items():
            if key in output.lower() and fact.lower() not in output.lower():
                score -= 0.2
                hallucinations.append(f"Possible contradiction for {key}")
        ran.append("knowledge_base_contradiction (3-term vocabulary)")

        # Entropy check: overly repetitive or gibberish detection
        words = str(output or "").split()
        if words:
            if len(set(words)) / len(words) < 0.3:
                score -= 0.5
                hallucinations.append("Low diversity/Entropy violation")
            ran.append("lexical_diversity")
        else:
            not_run["lexical_diversity"] = (
                "the subject has no words, so there is no diversity to measure. This previously raised "
                "ZeroDivisionError here and the interceptor did not guard it")

        return {
            # None when a check could not run: a partial screen is not a pass. The arithmetic and the
            # 0.7 threshold are unchanged for the case where both ran (uci_interceptor.py:91 branches
            # on this field, and the recirculation loop reaches that branch).
            "passed": (score > 0.7) if not not_run else None,
            "heuristic_score": round(score, 2),
            "hallucinations": hallucinations,
            "checks_run": ran,
            "checks_not_run": not_run,
        }

    async def validate_output(self, output: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check for consistency with established knowledge and context, and LOG the scan.

        The screening itself is sync and lives in screen(); this wrapper is async because it writes to
        the UEG. Keeping the two apart is what lets the constitutional validator call the same screen on
        the live path without a second copy of it (FU-363).
        """
        _s = self.screen(output)
        score = _s["heuristic_score"]
        hallucinations = _s["hallucinations"]

        # W415 — this returned {"passed": score > 0.7, "fidelity_score": score, ...} and score
        # starts at 1.0, decrementing only against the three literal keys in self.knowledge_base
        # ("v-infinity", "mjm-v5", "gaas-v4") plus a lexical-diversity check. Any ordinary text
        # therefore returned fidelity_score 1.0 — a perfect measured hallucination score — and
        # that figure was then sealed into the tamper-evident UEG as "hallucination_scan_completed",
        # asserting a fidelity measurement that for almost all inputs consisted of nothing. There
        # is no source registry or fact-check backend in this repo, so nothing measures fidelity:
        # it is reported as absent, and the two heuristics that DO run are named alongside their
        # raw deduction total so a reader can see the actual coverage. `passed` keeps the same
        # arithmetic and threshold (uci_interceptor.py:91 branches on it) but it means "these two
        # heuristics flagged nothing", not "this output was verified".
        res = {
            "passed": _s["passed"],
            "fidelity_score": None,
            "heuristic_score": round(score, 2),
            "hallucinations": hallucinations,
            #  W555 — the checks that RAN, read from the screen rather than listed as a constant. The
            #  constant said both always ran, which was untrue of an output with no words: that case
            #  raised before reaching this dict, so the list described a run that never completed.
            "checks_run": _s["checks_run"],
            "checks_not_run": _s["checks_not_run"],
            "verified_against_source": False,
            "note": ("Detection-only heuristic. No source registry or fact-check backend is "
                     "implemented, so nothing measures fidelity; 'passed' means these two checks "
                     "found nothing, NOT that the output was verified."),
        }
        await self.ueg.log_minimisation_event("hallucination_scan_completed", res)
        return res

    async def regenerate_with_citations(self, output: str) -> str:
        """No-op marker. NOTE: this method adds no citations and regenerates nothing — there is no
        RAG or source-verification backend in this repo. It only labels the output as unverified."""
        # W415 — this returned f"{output}\n\n[VERIFIED: JULES v∞ Registry]". No registry is
        # consulted anywhere in this class, no citation is added, and no regeneration happens —
        # a reader of the returned string saw "VERIFIED" against a named registry and believed
        # the content had been checked against it. Worse, uci_interceptor.py:92 calls this ONLY
        # when validate_output has just FAILED the text, so the single path that stamped content
        # "VERIFIED" was the path handling content the sandbox had just flagged. The method name
        # still overpromises, but it is another module's call site (uci_interceptor.py:92) and
        # renaming it is out of scope for this fix; the marker now states what actually happened.
        return (f"{output}\n\n[UNVERIFIED: flagged by the hallucination sandbox. No citation "
                f"registry or source-verification backend is implemented, so this output was "
                f"NOT corrected, cited or verified.]")
