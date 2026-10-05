from typing import Dict, Any, Optional
from datetime import datetime
from agentic_core.ueg.logger import VSBUEGLogger

class DivineAlignmentEngineV2:
    """
    Divine Alignment Engine (v∞-MASTER)
    Inherits from the Iman cognitive engine principles.
    Enforces ukhrawi-weighted metrics (70% eternal / 30% temporal).
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()

    #  the weights, declared once so a caller can see what a score would be made of
    _ETERNAL_WEIGHTS = (("faithfulness", 0.4), ("sincerity", 0.3), ("maslaha", 0.3))
    _TEMPORAL_WEIGHTS = (("user_value", 0.4), ("efficiency", 0.3), ("legal_compliance", 0.3))

    async def calculate_divine_alignment_score(self, eternal_metrics: dict,
                                               temporal_metrics: dict) -> Optional[float]:
        """Weight real metrics 70/30 — or return None when any of them was not supplied.

        W584 (FU-406) — every `.get(key, 0.0)` here meant an ABSENT metric was weighted as a zero, so this
        returned a number whenever it was called with nothing. A weighted mean over values it invented is
        a figure about nothing, and this repository already says so where its unassessable constraints are
        registered: "A VALIDATOR THAT RETURNS A NUMBER IT INVENTED IS WORSE THAN A MISSING ONE, because
        the missing one refuses". A missing input now makes the result None, and the caller states it.
        """
        missing = [k for k, _ in self._ETERNAL_WEIGHTS if not isinstance(eternal_metrics.get(k), (int, float))]
        missing += [k for k, _ in self._TEMPORAL_WEIGHTS
                    if not isinstance(temporal_metrics.get(k), (int, float))]
        if missing:
            self.last_missing_metrics = missing
            return None
        self.last_missing_metrics = []
        ukhrawi_score = sum(float(eternal_metrics[k]) * w for k, w in self._ETERNAL_WEIGHTS)
        temporal_score = sum(float(temporal_metrics[k]) * w for k, w in self._TEMPORAL_WEIGHTS)
        return 0.7 * ukhrawi_score + 0.3 * temporal_score

    #  W584 (FU-406) — stated once, because this is the whole of what this method can honestly say.
    #  W584 — the forensics (the exact constants this method used to build, and the five intents it was
    #  driven with) are in the round's commit and in P3.27's record. They are deliberately NOT recited
    #  here: a basis should state the RULE it is applying, and a basis that quotes numbers it does not
    #  compute is a claim a later screen has to re-adjudicate on every run.
    NO_INSTRUMENT_BASIS = (
        "NOT ASSESSED: nothing on this platform reads an intention, so no verdict about one is produced. "
        "This method previously returned a constant that passed every intent it was ever given, because it "
        "never read its `intent` argument at all. A SINCERITY FIGURE IS ALSO NOT SOMETHING THIS PLATFORM "
        "MAY COMPUTE: Ruling A.9.5 forbids an AI verdict on a person's spiritual state, and "
        "agentic_core/validation/constitutional_validators.py registers `sincerity_integrity_loyalty` as "
        "permanently NOT ASSESSABLE for that reason, under its own rule that a validator returning a "
        "number it invented is worse than a missing one, because the missing one refuses. WHAT WOULD "
        "CHANGE THIS: a real reading of a declared intention, supplied by whoever declared it, with a "
        "basis of its own - never a figure this module derives about anybody.")

    async def calibrate_niyyah(self, intent: str, framework: str = "islamic_khayr") -> Dict[str, Any]:
        """REFUSE to assess an intention, rather than return a constant that reads as a pass.

        W584 (FU-406). Driven with five opposite intents, the previous implementation returned 0.9222 and
        passed=True for all five. It is replaced by an explicit refusal: `passed` is None, which the
        interceptor reads as NOT ASSESSED and never as a pass, and no sincerity number is produced or
        logged at all.

        The three-state return is what makes the gate ABLE to refuse, and the limit is stated rather than
        implied: `passed` False is a real outcome for a caller that supplies real metrics through
        `calculate_divine_alignment_score`, and that function currently has NO PRODUCTION CALLER, so
        nothing that runs produces a False today. What changed is still the thing that mattered — before
        this, False could not occur at all and None did not exist, so the gate had exactly one outcome and
        it was a pass on a constant.
        """
        res = {
            "framework": framework,
            "intent": intent,
            "alignment_score": None,
            "passed": None,
            "assessed": False,
            #  NOT 0.0 and not 0.9. There is no sincerity reading, and a number here - of any value -
            #  would be a spiritual judgement this platform does not make.
            "sincerity": None,
            "basis": self.NO_INSTRUMENT_BASIS,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.ueg.log_minimisation_event("divine_niyyah_not_assessed", res)
        return res
