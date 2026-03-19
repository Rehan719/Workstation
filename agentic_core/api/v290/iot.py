from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio

router = APIRouter(prefix="/iot", tags=["Physical-Digital Symbiosis"])

class Device(BaseModel):
    id: str
    name: str
    type: str # sensor, actuator, hybrid
    protocol: str # mqtt, coap, simulation
    status: str = "connected"
    last_pulse: float = 0.0

DEVICES = [
    {"id": "dev-001", "name": "Node-Alpha Environment", "type": "sensor", "protocol": "mqtt", "status": "online"},
    {"id": "dev-002", "name": "Bio-Reactor Vent", "type": "actuator", "protocol": "coap", "status": "idle"}
]

@router.get("/devices", response_model=List[Device])
async def list_devices():
    """v150.0 Device Registry."""
    return DEVICES

@router.post("/bridge/mqtt/publish")
async def mqtt_publish(topic: str, payload: str):
    """Real MQTT connectivity stub."""
    # Simulation: Talk to local Mosquitto if configured
    print(f"MQTT Publish [Stub]: {topic} -> {payload}")
    return {"status": "dispatched", "broker": "localhost:1883"}

@router.get("/bridge/coap/get")
async def coap_get(resource: str):
    """Real CoAP connectivity stub."""
    print(f"CoAP GET [Stub]: {resource}")
    return {"resource": resource, "value": 24.5, "unit": "celsius"}

@router.get("/telemetry/{device_id}")
async def get_telemetry(device_id: str):
    """Simulated real-time data for visualization widgets."""
    import random
    return {
        "timestamp": "2026-01-01T00:00:00Z",
        "values": [
            {"label": "Temperature", "value": 22 + random.random() * 5, "unit": "C"},
            {"label": "Resonance", "value": 0.85 + random.random() * 0.1, "unit": "Fr"}
        ]
    }
