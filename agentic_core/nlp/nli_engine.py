import logging
from typing import Dict, Any, List, Optional
import re

logger = logging.getLogger(__name__)

class NLIEngine:
    """
    ARTICLE 145: Natural language inference for intent verification.
    Supports semantic validation in the conversational app builder.
    """
    def __init__(self, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold
        # Rule-based fallback for intent verification
        self.intent_patterns = {
            "BUILD_APP": [r"build", r"create", r"app", r"generate"],
            "DEPLOY_APP": [r"deploy", r"release", r"push", r"cloud"],
            "SYNC_DATA": [r"sync", r"synchronize", r"collaboration"],
            "RESEARCH": [r"research", r"paper", r"qa", r"scientific"]
        }

    def infer_intent(self, text: str) -> Dict[str, Any]:
        """
        Infers the user's intent from the provided text using keyword matching and pattern analysis.
        """
        text = text.lower()
        intent_scores = {}

        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for p in patterns if re.search(p, text))
            intent_scores[intent] = score / len(patterns)

        # §4.5-class defect (W430): `max()` over equal scores returns the FIRST key by dict order, so
        # text matching NOTHING was reported as the first intent in the pattern table — "BUILD_APP",
        # confidence 0.0, every score 0.0. `is_verified` said False, but the field named `intent`
        # reads as a determination and a caller rendering it shows a category nothing supports.
        # Absence beats invention: when nothing scored, there is no intent, and a tie at the top is
        # DISCLOSED rather than resolved silently by dict order.
        best_score = max(intent_scores.values()) if intent_scores else 0.0
        top = sorted(k for k, v in intent_scores.items() if v == best_score)
        no_signal = best_score <= 0.0
        tied = len(top) > 1 and not no_signal
        best_intent = None if (no_signal or tied) else top[0]
        is_verified = (not no_signal) and (not tied) and best_score >= self.confidence_threshold

        logger.info("NLIEngine: intent=%s score=%.2f verified=%s no_signal=%s tied=%s",
                    best_intent, best_score, is_verified, no_signal, tied)
        return {
            "intent": best_intent,
            "confidence": best_score,
            "is_verified": is_verified,
            "all_scores": intent_scores,
            # Why there is no intent, when there is none — a bare null invites the reader to guess.
            "no_signal": no_signal,
            "tied": tied,
            "tied_intents": top if tied else [],
            "basis": ("no pattern matched this text" if no_signal else
                      f"{len(top)} intents tied at {best_score} - not resolved by pattern score" if tied
                      else f"highest pattern score {best_score} of {len(intent_scores)} intents"),
        }

    # W431 — words that INVERT a claim. Token overlap is blind to them: "the sky is not blue" shares
    # every token of "the sky is blue" except the one that reverses its meaning, so the old code
    # scored 4/4 and returned ENTAILED for a premise that REFUTES the hypothesis.
    _NEGATORS = frozenset({"not", "no", "never", "cannot", "cant", "isnt", "arent", "wasnt",
                           "werent", "wont", "dont", "doesnt", "didnt", "none", "neither", "nor",
                           "without", "fails", "failed", "denies", "denied", "refuses", "refused"})

    def verify_premise_entailment(self, premise: str, hypothesis: str) -> str:
        """Label only. Prefer `entailment_detail` — this returns the bare verdict for legacy callers."""
        return self.entailment_detail(premise, hypothesis)["label"]

    def entailment_detail(self, premise: str, hypothesis: str) -> Dict[str, Any]:
        """Word-overlap NLI, with the number it decided on and the limits of what it can know.

        W431 — three §4.5-class defects fixed here:
          · NEGATION WAS INVISIBLE. Overlap counts hypothesis tokens found in the premise, and a
            negator appears in the PREMISE only — so it never entered the ratio. "The sky is not
            blue" -> "The sky is blue" returned ENTAILED. Asymmetric negation now yields
            CONTRADICTION, which the docstring had always promised and the code never returned.
          · THE DECIDING NUMBER WAS WITHHELD. `overlap_ratio` and its cut-points were computed and
            discarded, so a caller got a verdict with no way to see a 4/4 token match produced it.
          · AN EMPTY HYPOTHESIS SCORED 0.0 AND READ AS NEUTRAL — indistinguishable from a genuinely
            unrelated one. It is now reported as undecidable, with the reason.

        What this still CANNOT do, stated because the label is a logical claim: it does not read word
        order ("blue is sky the" matches), quantifiers, or role inversion beyond negation ("Alice paid
        Bob" vs "Bob paid Alice" shares every token). Callers must treat the label as lexical
        evidence, not proof — which is what `basis` and `method` are for.
        """
        p_raw, h_raw = (premise or "").lower(), (hypothesis or "").lower()
        premise_words = set(p_raw.split())
        hypothesis_words = set(h_raw.split())

        if not hypothesis_words:
            return {"label": "UNDECIDABLE", "overlap_ratio": None, "negation_conflict": False,
                    "method": "word-overlap NLI (owned nlp)",
                    "basis": "the hypothesis is empty - there is nothing to decide"}

        intersection = premise_words & hypothesis_words
        overlap_ratio = round(len(intersection) / len(hypothesis_words), 3)

        # A negator on exactly ONE side reverses the claim, whatever the tokens agree on.
        p_neg = bool(premise_words & self._NEGATORS)
        h_neg = bool(hypothesis_words & self._NEGATORS)
        negation_conflict = (p_neg != h_neg)

        if negation_conflict and overlap_ratio >= 0.5:
            label = "CONTRADICTION"
            basis = (f"token overlap {overlap_ratio} but negation appears on one side only "
                     f"({'premise' if p_neg else 'hypothesis'}) - the claim is reversed")
        elif overlap_ratio >= 0.9:
            label, basis = "ENTAILED", f"token overlap {overlap_ratio} >= 0.9"
        elif overlap_ratio < 0.2:
            label, basis = "NEUTRAL", f"token overlap {overlap_ratio} < 0.2"
        else:
            label, basis = "PARTIAL_ENTAILMENT", f"token overlap {overlap_ratio} between 0.2 and 0.9"

        return {"label": label, "overlap_ratio": overlap_ratio,
                "negation_conflict": negation_conflict,
                "method": "word-overlap NLI (owned nlp)",
                "basis": basis,
                "limits": "lexical only - does not read word order, quantifiers or role inversion"}

    def get_intent_confidence(self, intent_id: str) -> float:
        """
        Returns the confidence score for a specific intent ID based on historical results.
        """
        return 0.85 # Placeholder for historical confidence tracking
