from fastapi import APIRouter
import random

router = APIRouter(prefix="/introspection", tags=["Cognitive Introspection"])

@router.get("/vitals")
async def get_vitals():
    return {
        "oxytocin": 0.95 + random.uniform(-0.02, 0.02),
        "serotonin": 0.92 + random.uniform(-0.03, 0.03),
        "dopamine": 0.98 + random.uniform(-0.01, 0.01),
        "system_health": 0.9998,
        "mode": "STRATEGIC-SYNTHESIS"
    }

@router.get("/telemetry")
async def get_telemetry():
    return {
        "cpu_usage": "14.2%",
        "memory_resonance": "92%",
        "active_swarms": 42,
        "anomalies": []
    }
