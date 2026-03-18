from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter(prefix="/identity/global", tags=["Global Identity Layer"])

class CitizenPassport(BaseModel):
    did: str
    reputation_score: float
    contributions_count: int
    authorized_realms: List[str]
    voting_power: float

@router.get("/passport/{did}")
async def get_citizen_passport(did: str):
    """Retrieves the global, portable identity and reputation of a citizen."""
    return {
        "did": did,
        "handle": "guardian-prime",
        "reputation_score": 0.985,
        "contributions_count": 1420,
        "voting_power": 42.5,
        "authorized_realms": ["Governance", "Scholar", "Physical-World"],
        "constitutional_rights": ["Article 1086-Access", "Article 1095-Verification"]
    }

@router.post("/realm/join")
async def one_click_join(did: str, realm_id: str):
    """Seamlessly transfers identity and reputation to a new realm."""
    return {"status": "authorized", "realm": realm_id, "mode": "resident"}
