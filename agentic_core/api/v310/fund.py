from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/fund", tags=["Creator Fund"])

@router.get("/epoch-synthesis")
async def get_epoch_summary():
    """No epoch report exists, and this says so.

    W666 (ledger v16 R6.1) - this returned a fixed dict as an AI CEO report: an economic volume, a
    creator-earnings growth percentage, two fund allocation proposals with reasons and a narrative.
    Nothing was read from any ledger. The sibling route below was corrected the same way in W408.
    """
    return {
        "report": None,
        "detail": ("No epoch report is produced on this deployment: nothing reads the economy's ledgers "
                   "into one. A fixed set of figures was previously returned here. The economy's own "
                   "figures are at /api/v1/economy/status."),
    }

@router.get("/grants/active")
async def list_active_grants():
    """No grants have been awarded, and this says so.

    W408 - this returned two invented grants: {"id": "g-001", "title": "Bio-Reactor Optimization",
    "recipient": "@NatureBuild", "amount": 5000, "status": "funded"} and a second at 2,500 in
    "voting". An endpoint named grants/active returning a FUNDED grant to a named recipient asserts
    that money was awarded to someone. No grant store is read, no recipient exists, and the sibling
    endpoint on this same router does call a real engine - so a consumer had every reason to read
    this list as equally real.
    """
    return {
        "grants": [],
        "detail": ("No grant register exists on this deployment, so no grants are listed. Two "
                   "invented grants were previously returned here."),
    }
