import asyncio
from typing import List, Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.cognitive.inkashaf_engine import InkashafEngine
from agentic_core.cognitive.aqal_engine import AqalEngine
from agentic_core.cognitive.samajh_engine import SamajhEngine
from agentic_core.cognitive.hoshiyari_engine import HoshiyariEngine
from agentic_core.cognitive.soch_engine import SochEngine
from agentic_core.cognitive.iman_engine import ImanEngine

class UltimateCognitiveCascade:
    """
    Recursive Cognitive Cascade Engine.
    Executes all six Urdu cognitive engines in a systems-biology inspired sequence.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.inkashaf = InkashafEngine(self.ueg)
        self.aqal = AqalEngine(self.ueg)
        self.samajh = SamajhEngine(self.ueg)
        self.hoshiyari = HoshiyariEngine(self.ueg)
        self.soch = SochEngine(self.ueg)
        self.iman = ImanEngine(self.ueg)

    async def execute_cascade(self, problem: Any) -> Dict[str, Any]:
        # Sequence: Reveal -> Comprehend -> Reflect -> Reason -> Detect -> Align
        # W531 (FU-322) — each engine is RECORDED as it completes, so the count downstream is computed
        # from what happened rather than written as a literal. Before this the report said nothing about
        # which engines ran, so /cascade had nothing to count and reported a hard 6 with a basis sentence
        # beside it. A basis beside a literal does not make the literal a measurement.
        engines_ran: list = []

        patterns = await self.inkashaf.unveil_patterns(problem)
        engines_ran.append("inkashaf")
        understanding = await self.samajh.comprehend(patterns)
        engines_ran.append("samajh")
        hypotheses = await self.soch.reflect(str(understanding))
        engines_ran.append("soch")
        plan = await self.aqal.reason({"goals": hypotheses}, {})
        engines_ran.append("aqal")
        alerts = await self.hoshiyari.detect_anomalies(plan)
        engines_ran.append("hoshiyari")
        final_alignment = await self.iman.validate_values(plan)
        engines_ran.append("iman")

        cascade_report = {
            "patterns": patterns,
            "understanding": understanding,
            "plan": plan,
            "alignment": final_alignment,
            "alerts": alerts,
            # W531 — `engines_ran` is the list; anything reporting a count derives it from here.
            "engines_ran": engines_ran,
            "engines_ran_count": len(engines_ran),
            # W531 — this said "fully_integrated", a superlative over six engines that each return a fixed
            # marker. What happened is that six calls completed; integration is not something this measured.
            "status": "completed",
            "status_basis": (f"{len(engines_ran)} engine call(s) completed in sequence. Each returns a fixed "
                            "marker rather than computing (P3.12), so this reports completion and not "
                            "analysis, and nothing here measures integration"),
        }

        await self.ueg.log_minimisation_event("cognitive_cascade_completed", {"problem": str(problem)})
        return cascade_report
