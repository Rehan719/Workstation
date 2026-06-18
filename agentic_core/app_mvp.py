"""
Workstation MVP — lean FastAPI application.

Mounts only the spine routers needed for the commercial MVP flow:
  AI CEO → Realm/Domain → Project → Product → Deliverable

Run with:
  uvicorn agentic_core.app_mvp:app --reload --port 8000

All 80+ versioned routers in main.py remain untouched.
"""
from __future__ import annotations

import asyncio
import logging
import os

import psutil
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workstation.mvp")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Workstation",
    description="AI-Mediated Workspace — Commercial MVP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MVP spine routers ─────────────────────────────────────────────────────────

# 1. Projects (concept → commercialise lifecycle, SSE streaming, governance)
from agentic_core.projects import api as projects_api
app.include_router(projects_api.router, prefix="/api/v1")

# 2. AI CEO chat (SSE streaming chat)
from agentic_core.api.v138 import ceo as ceo_v138
app.include_router(ceo_v138.router, prefix="/api/v138")

# 3. CEO generate-blueprint (real AI call → deliverable)
from agentic_core.api.v290 import ceo_generate
app.include_router(ceo_generate.router, prefix="/api/v290")

# 4. C-Suite metrics (CFO/CTO — computed from project store)
from agentic_core.api import csuite
app.include_router(csuite.router, prefix="/api")

# 5. Synthesis (upload → AI → download)
from agentic_core.synthesis import api as synthesis_api
app.include_router(synthesis_api.router, prefix="/api/v1")

# 6. Avatars / biometrics / status
from agentic_core.avatars import api as avatar_api
app.include_router(avatar_api.router, prefix="/api/v1")

# 7. Ingestion (file upload pipeline)
from agentic_core.ingestion import api as ingestion_api
app.include_router(ingestion_api.router, prefix="/api/v1")

# 8. Products (Reactor/Factory/Incubator/Intelligence — all real AI execution)
from agentic_core.api import products as products_api
app.include_router(products_api.router)

# 9. Marketplace (real listings + WST purchase)
from agentic_core.api import marketplace as marketplace_api
app.include_router(marketplace_api.router)

# 10. BTO Catalog + Configurator
from agentic_core.catalog import api as catalog_api, bto as bto_api
app.include_router(catalog_api.router, prefix="/api/v1")
app.include_router(bto_api.router, prefix="/api/v1")

# 10. Entrepreneur / Business Plan Wizard (v310)
from agentic_core.api.v310 import business as business_api
app.include_router(business_api.router, prefix="/api/v310")

# 11. Sovereign Realms registry (persist + discover from project store)
from agentic_core.api.v290.realms import router as realms_router
app.include_router(realms_router, prefix="/api")

# 12. Generic AI query (real gateway call — used by Solutions Platform and CEO assistant)
from agentic_core.api import ai_query as ai_query_api
app.include_router(ai_query_api.router, prefix="/api")

# 13. Council Judiciary (in-memory precedent adjudication — real logic)
from agentic_core.api import council_judiciary as judiciary_api
app.include_router(judiciary_api.router, prefix="/api")

# 14. Treaties (in-memory treaty creation/signing — Treaty Studio frontend calls /api/v250/treaties/*)
from agentic_core.api.v250 import treaties as treaties_api
app.include_router(treaties_api.router, prefix="/api/v250")

# 15. Civilization Intelligence (real assistant query via gateway)
from agentic_core.api.v260 import intelligence as civilization_api
app.include_router(civilization_api.router, prefix="/api")

# 16. DAO/Governance — v310 (proposals, voting, treasury) — called by DAODashboard
from agentic_core.api.v310 import governance as governance_v310
app.include_router(governance_v310.router, prefix="/api/v310")

# 17. Payments / WST wallet — v310 — called by Wallet and Commerce flows
from agentic_core.api.v310 import payments as payments_v310
app.include_router(payments_v310.router, prefix="/api/v310")

# 18. Creator Fund — v310 — epoch synthesis + grants
from agentic_core.api.v310 import fund as fund_v310
app.include_router(fund_v310.router, prefix="/api/v310")

# 19. Gamification (XP / quests / levels) — called by gamificationStore.ts
from agentic_core.api.v280 import gamification as gamification_api
app.include_router(gamification_api.router, prefix="/api/v280")

# 20. Evolution proposals (v191) — called by Proposals + EvolutionDashboard pages
from agentic_core.api.v191 import evolution as evolution_v191
app.include_router(evolution_v191.router, prefix="/api/v191")

# 21. Contribute / voting (v200) — called by Proposals page vote action
from agentic_core.api.v200 import contribute as contribute_v200
app.include_router(contribute_v200.router, prefix="/api/v200")

# ── Health ────────────────────────────────────────────────────────────────────

import datetime


def _circadian_cycle() -> str:
    hour = datetime.datetime.now().hour
    if 6 <= hour < 9 or 17 <= hour < 20:
        return "ACTIVE_REST"
    if 9 <= hour < 17:
        return "ACTIVE_FOCUS"
    if 20 <= hour < 23:
        return "MAINTENANCE_FOCUS"
    return "MAINTENANCE_REST"


@app.get("/api/v1/biometrics/status")
async def biometrics_status():
    """Organism vitals derived from real system state — psutil + project store."""
    from agentic_core.projects.api import _all_projects
    try:
        projects = _all_projects()
        active = sum(1 for p in projects if p.status == "running")
    except Exception:
        projects = []
        active = 0

    cpu  = psutil.cpu_percent(interval=None)
    mem  = psutil.virtual_memory()
    ws   = len(_ws.connections)

    resource_flow = max(0.0, 100.0 - cpu)
    peristaltic_delay = round(max(1, mem.percent / 20), 1)

    if active > 2 or cpu > 70:
        cognition_state = "FLOURISHING"
        primary_drive   = "SYNTHESIS"
    elif cpu > 40 or len(projects) > 0:
        cognition_state = "STABLE"
        primary_drive   = "ACHIEVEMENT"
    else:
        cognition_state = "STABLE"
        primary_drive   = "DISCOVERY"

    if ws > 0:
        neurotransmitter = "Dopamine"
    elif active > 0:
        neurotransmitter = "Serotonin"
    else:
        neurotransmitter = "Oxytocin"

    return {
        "circadian":      {"cycle": _circadian_cycle()},
        "cardiovascular": {"resource_flow": round(resource_flow, 1), "peristaltic_delay": peristaltic_delay},
        "cognition":      {"state": cognition_state, "primary_drive": primary_drive},
        "communication":  {"active_channels": ["WS"] if ws > 0 else [], "neurotransmitter": neurotransmitter, "is_active": ws > 0},
    }


@app.get("/health")
@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "1.0.0", "app": "workstation-mvp"}


@app.get("/api/v1/claude/status")
async def claude_status():
    return {"authenticated": bool(os.getenv("ANTHROPIC_API_KEY"))}


# ── Real-time vitals WebSocket ────────────────────────────────────────────────

class _VSManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws) if hasattr(self.connections, 'discard') else None
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, payload: dict):
        dead = []
        for ws in list(self.connections):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

_ws = _VSManager()


@app.websocket("/api/v154/ws/streams")
async def ws_stream(websocket: WebSocket):
    await _ws.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        _ws.disconnect(websocket)


async def _vitals_loop():
    from agentic_core.projects.api import _all_projects
    while True:
        try:
            projects = _all_projects()
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            active = sum(1 for p in projects if p.status == "running")
            await _ws.broadcast({
                "type": "SYSTEM_VITALS",
                "payload": {
                    "cpu": cpu,
                    "memory": mem,
                    "activeAgents": active,
                    "totalProjects": len(projects),
                    "connections": len(_ws.connections),
                    "swarmHealth": min(1.0, 0.7 + (len(projects) * 0.01)),
                    "latency_ms": 12,
                },
            })
        except Exception as exc:
            logger.debug("vitals loop error: %s", exc)
        await asyncio.sleep(5)


@app.on_event("startup")
async def _startup():
    asyncio.create_task(_vitals_loop())
    logger.info("Workstation MVP started — spine routers only.")
