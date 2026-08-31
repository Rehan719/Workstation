from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/qep/analytics", tags=["QEP Analytics"])

from agentic_core.ueg.ueg_manager import UEGManager

ueg = UEGManager()

@router.get("/overview")
async def qep_analytics_overview():
    """QEP analytics are NOT measured, and this says so instead of inventing them.

    W400 - this endpoint called ueg.get_summary(), which has never existed: UEGManager exposes only
    write operations (add_claim, add_insight, ...) and no read API at all, so a plain GET raised
    AttributeError. It could never have worked.

    Repairing the crash would have been worse than the crash, because the body was almost entirely
    invented: accuracy_score 0.999, morphology_coverage "99.9%", quiz_accuracy "98.2%",
    study_groups_active 42, a scholar trust network with avg_oxytocin 0.992, and a real count with
    "+ 1024  # v128 scaling" added to it. No measurement produced any of it.

    Until there is a source to compute them from, this reports that plainly.
    """
    return {
        "measured": False,
        "metrics": {},
        "detail": (
            "QEP analytics are not implemented. The UEG manager exposes only write operations, so "
            "there is no source to compute active students, verified scholars or annotation counts "
            "from. This endpoint previously returned hardcoded figures that no measurement produced."
        ),
    }
