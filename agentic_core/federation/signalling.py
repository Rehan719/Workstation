import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

logger = logging.getLogger(__name__)

app = FastAPI()

class SignallingManager:
    """
    ARTICLE 1040: WebRTC Signalling for Avatar Federation.
    Handles real-time P2P coordination for avatar projection.
    """
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, workstation_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[workstation_id] = websocket
        logger.info(f"Signalling: Workstation {workstation_id} connected.")

    def disconnect(self, workstation_id: str):
        if workstation_id in self.active_connections:
            del self.active_connections[workstation_id]
            logger.info(f"Signalling: Workstation {workstation_id} disconnected.")

    async def send_personal_message(self, message: str, workstation_id: str):
        if workstation_id in self.active_connections:
            await self.active_connections[workstation_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = SignallingManager()

@app.websocket("/ws/signalling/{workstation_id}")
async def websocket_endpoint(websocket: WebSocket, workstation_id: str):
    await manager.connect(workstation_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # In real usage, parse WebRTC Offer/Answer/ICE candidates
            logger.info(f"Signalling: Received data from {workstation_id}: {data}")
            # Broadcast to peers for P2P handshake
            await manager.broadcast(f"Peer {workstation_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(workstation_id)
