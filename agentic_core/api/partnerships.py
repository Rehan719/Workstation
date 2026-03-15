from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from agentic_core.commercial.partnership_framework import PartnershipFramework, PartnershipTier

router = APIRouter(prefix="/partnerships", tags=["Diplomatic Corps"])
framework = PartnershipFramework()

@router.get("/registry")
async def get_partnership_registry():
    """ARTICLE 755: Public Partnership Registry."""
    return framework.get_public_registry()

@router.post("/onboard")
async def onboard_partner(entity_name: str, tier: int):
    """
    Tier mapping: 1=Associate, 2=Certified, 3=Strategic
    """
    if tier == 1:
        ptier = PartnershipTier.TIER_1
    elif tier == 2:
        ptier = PartnershipTier.TIER_2
    elif tier == 3:
        ptier = PartnershipTier.TIER_3
    else:
        raise HTTPException(status_code=400, detail="Invalid partnership tier")

    return framework.initiate_onboarding(entity_name, ptier)

@router.get("/status/{partner_id}")
async def get_partner_status(partner_id: str):
    if partner_id in framework.partners:
        return framework.partners[partner_id]
    raise HTTPException(status_code=404, detail="Partner not found")
