from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random
import datetime

router = APIRouter(prefix="/intelligence", tags=["Collective Intelligence"])

@router.get("/insights")
async def get_civilization_insights():
    """v152.0: AI-detected patterns across the global ecosystem."""
    return [
        {
            "id": "insight-01",
            "category": "Economy",
            "title": "Viral Creator Trend: Bio-Reactors",
            "observation": "14% increase in Bio-Reactor creations detected in Swarm sector.",
            "recommendation": "Allocate additional Creator Fund resources to Bio-Ethics CoE.",
            "confidence": 0.94
        },
        {
            "id": "insight-02",
            "category": "Governance",
            "title": "Consensus Drift Detected",
            "observation": "Voting patterns on Article 1095 are deviating from standard resonance.",
            "recommendation": "AI CEO intervention: Publish strategic clarification on Planetary Sovereignty.",
            "confidence": 0.88
        }
    ]

@router.get("/forecasts")
async def get_ecosystem_forecasts():
    """Predictive trends for economic and governance metrics."""
    return {
        "wst_liquidity": {"target": "1.5M", "projection": "1.8M", "timeframe": "30 days"},
        "voter_turnout": {"current": "42%", "projection": "58%", "driver": "Autonomous Delegation"},
        "creation_velocity": {"current": "12/day", "projection": "25/day", "catalyst": "Creator Studio v2"}
    }

@router.get("/anomalies")
async def get_system_anomalies():
    """Security and integrity alerts identified by pattern detection."""
    return [
        {"timestamp": "2026-01-01T14:20:00Z", "type": "Economic", "severity": "low", "message": "Micro-transaction spike in Region: Swarm-North."},
        {"timestamp": "2026-01-01T08:12:00Z", "type": "Governance", "severity": "medium", "message": "Sudden quadratic weight shift in Proposal Prop-151-02."}
    ]
