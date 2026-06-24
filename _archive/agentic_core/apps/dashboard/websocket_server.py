import asyncio
import json
import random
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="JULES Ecosystem Dashboard")

class HealthStatus(BaseModel):
    status: str
    timestamp: float

@app.get("/health")
async def health():
    return HealthStatus(status="alive", timestamp=time.time())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate real-time metrics push
            # In production, these would be pulled from the GeosphericHomeostaticOrchestrator
            metrics = {
                "psi_functional": round(random.uniform(0.90, 0.98), 4),
                "lyapunov_exponent": round(random.uniform(-0.5, -0.1), 4),
                "couplings": {
                    "water_carbon": round(random.uniform(0.01, 0.05), 4),
                    "nitrogen_oxygen": round(random.uniform(0.02, 0.06), 4),
                    "phosphorus_sulfur": round(random.uniform(0.01, 0.03), 4)
                },
                "timestamp": time.time()
            }
            await websocket.send_json(metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("Dashboard client disconnected.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
