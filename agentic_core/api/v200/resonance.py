from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import random
import json

router = APIRouter(prefix="/resonance", tags=["Real-Time Resonance"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/vitals")
async def websocket_vitals(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            vitals = {
                "oxytocin": 0.95 + random.uniform(-0.02, 0.02),
                "serotonin": 0.92 + random.uniform(-0.03, 0.03),
                "dopamine": 0.98 + random.uniform(-0.01, 0.01),
                "system_health": 0.9998
            }
            await websocket.send_text(json.dumps(vitals))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
