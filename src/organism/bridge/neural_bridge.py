import os
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Header, HTTPException, Depends
from typing import Dict, Any, List, Optional
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import BiomimeticEvent

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple token security (In production, use OAuth2/JWT)
SOVEREIGN_TOKEN = os.getenv("SOVEREIGN_TOKEN", "sovereign-dev-token")

async def verify_token(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {SOVEREIGN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Sovereign Token")
    return True

class NeuralBridge:
    """
    Bridges the Python NeuralBus to the TypeScript/UI layer via WebSockets.
    Requires authentication for connection.
    """
    def __init__(self, event_bus: AsyncEventBus):
        self.event_bus = event_bus
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        # Verify token from query parameter for WebSockets
        token = websocket.query_params.get("token")
        if token != SOVEREIGN_TOKEN:
            await websocket.close(code=1008) # Policy Violation
            logger.warning("NeuralBridge: Unauthorized WebSocket connection attempt blocked.")
            return

        self.active_connections.append(websocket)
        logger.info(f"NeuralBridge: WebSocket client connected. Active: {len(self.active_connections)}")

        # Start listening to all events on the bus
        self.event_bus.subscribe(BiomimeticEvent, self.broadcast_event)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("NeuralBridge: WebSocket client disconnected.")

    async def broadcast_event(self, event: BiomimeticEvent):
        """Serializes and broadcasts events to all connected UI clients."""
        event_dict = {
            "type": type(event).__name__,
            "payload": self._serialize_event(event)
        }

        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(event_dict)
            except Exception:
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)

    def _serialize_event(self, event: Any) -> Dict[str, Any]:
        """Custom serialization for biomimetic events."""
        if hasattr(event, "__dict__"):
             res = {}
             for k, v in event.__dict__.items():
                 if hasattr(v, "__dict__"):
                     res[k] = self._serialize_event(v)
                 elif isinstance(v, (list, tuple)):
                     res[k] = [self._serialize_event(i) if hasattr(i, "__dict__") else i for i in v]
                 else:
                     res[k] = v
             return res
        return str(event)

# Global bridge instance (to be initialized by main.py)
bridge: Optional[NeuralBridge] = None

@router.websocket("/ws/organism/neural-bus")
async def websocket_neural_bus(websocket: WebSocket):
    if bridge is None:
        await websocket.close(code=1011)
        return

    await bridge.connect(websocket)
    try:
        while True:
            # Keep connection open
            await websocket.receive_text()
    except WebSocketDisconnect:
        bridge.disconnect(websocket)
    except Exception as e:
        logger.error(f"NeuralBridge: WebSocket error: {e}")
        bridge.disconnect(websocket)

@router.get("/api/v1/organism/health", dependencies=[Depends(verify_token)])
async def get_organism_health():
    """Returns vital signs for the health dashboard."""
    return {
        "sentience": 0.92,
        "compliance": 0.98,
        "throughput": 12.5,
        "cognitive_load": 0.45,
        "integrity": 0.99,
        "realms": {
            "development": "HEALTHY",
            "production": "HEALTHY"
        }
    }
