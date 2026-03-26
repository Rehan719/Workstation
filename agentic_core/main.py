from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
import os
import random
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from agentic_core.reactor.religion.quranic_studies import QuranicStudiesReactor
from agentic_core.reactor.ecosystem.factory import ReactorFactory
from agentic_core.enterprise.policy import PolicyCoE
from agentic_core.commercial.token_ledger import TokenLedger, UserTier
from agentic_core.synthesis.dual_mode_scraper import DualModeScraper
from agentic_core.synthesis.uviap import UVIAP
from agentic_core.api import qep_analytics, tools, partnerships
from agentic_core.api.v180 import products, user
from agentic_core.api.v190 import introspection as introspection_v190
from agentic_core.api.v190 import extrospection, evolution
from agentic_core.api.v191 import modes, learning, evolution as evolution_v191
from agentic_core.api.v200 import resonance, contribute
from agentic_core.api.v210 import epigenetic, homeostasis, improvement, governance, federation
from agentic_core.api.v220 import federation as federation_v220, economic, twin
from agentic_core.api.v250 import treaties, search
from agentic_core.api.v260 import intelligence
from agentic_core.api.v230 import evolution as evolution_v230, pqc, marketplace
from agentic_core.api.v240 import evolution as evolution_v240
from agentic_core.api.v270 import infrastructure as infra_v270
from agentic_core.api import ai_orchestration, csuite
from agentic_core.api.v280 import csuite_enhanced, gamification
from agentic_core.api.v290 import realms as realms_v290, ceo_generate, marketplace as marketplace_v290, iot
from agentic_core.api.v310 import payments, governance as gov_v310, business, commerce, fund
from agentic_core.api.v320 import intelligence as intel_v320, governance_autonomous, treasury_intelligent, markets
from agentic_core.api.v340 import consciousness, soul_record
from agentic_core.api.v138 import ceo as ceo_v138
from agentic_core.api import v154_unified, v200_unified
from prometheus_client import make_asgi_app, Counter, Histogram
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global CoEs and Reactors
policy = PolicyCoE()
reactor_factory = ReactorFactory()
token_ledger = TokenLedger()
scraper = DualModeScraper(token_ledger=token_ledger)
uviap = UVIAP()

# Default user for demo
token_ledger.initialize_user("demo_user", UserTier.PRO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ARTICLE 541: Passive sensory layer as continuous background process
    logger.info("Apotheosis: Passive Sensory Monitoring Awakening...")

    # Start the scraper's passive mode
    task = asyncio.create_task(scraper.passive.monitor_environment())
    # Start WebSocket broadcast task
    ws_task = asyncio.create_task(broadcast_vitals_background())

    yield
    task.cancel()
    ws_task.cancel()
    logger.info("Apotheosis: System Hibernating.")

app = FastAPI(
    title="Workstation v1.0 Global Launch - Sovereign AI Core",
    lifespan=lifespan
)

# Prometheus Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP Request Latency', ['endpoint'])

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    response = await call_next(request)

    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

    return response

# WebSocket Connections Management
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket Client Connected. Active: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket Client Disconnected. Active: {len(self.active_connections)}")

    async def broadcast_vitals(self):
        vitals = {
            "type": "SYSTEM_VITALS",
            "payload": {
                "cpu": random.uniform(10, 30),
                "memory": random.uniform(5, 15),
                "activeAgents": 42,
                "swarmHealth": 0.98,
                "latency_ms": 18
            }
        }
        for connection in self.active_connections:
            try:
                await connection.send_json(vitals)
            except Exception:
                pass

ws_manager = ConnectionManager()

async def broadcast_vitals_background():
    """Background task to broadcast vitals once per interval."""
    while True:
        await ws_manager.broadcast_vitals()
        await asyncio.sleep(5)

@app.websocket("/api/v154/ws/streams")
async def websocket_streams(websocket: WebSocket):
    """v138.0 Sovereign Stream: Direct WebSocket connection."""
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection open and wait for messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
        ws_manager.disconnect(websocket)

@app.websocket("/ws/test")
async def websocket_test(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"status": "connected", "msg": "Sovereign Test Socket Active"})
    await websocket.close()

app.include_router(qep_analytics.router, prefix="/api/v1")
app.include_router(tools.router, prefix="/api/v1")
app.include_router(partnerships.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v180")
app.include_router(user.router, prefix="/api/v180")
app.include_router(introspection_v190.router, prefix="/api/v190")
app.include_router(extrospection.router, prefix="/api/v190")
app.include_router(evolution.router, prefix="/api/v190")
app.include_router(modes.router, prefix="/api/v191")
app.include_router(learning.router, prefix="/api/v191")
app.include_router(evolution_v191.router, prefix="/api/v191")
app.include_router(resonance.router, prefix="/api/v200")
app.include_router(contribute.router, prefix="/api/v200")
app.include_router(epigenetic.router, prefix="/api/v210")
app.include_router(homeostasis.router, prefix="/api/v210")
app.include_router(improvement.router, prefix="/api/v210")
app.include_router(governance.router, prefix="/api/v210")
app.include_router(federation.router, prefix="/api/v210")
app.include_router(federation_v220.router, prefix="/api/v220")
app.include_router(economic.router, prefix="/api/v220")
app.include_router(twin.router, prefix="/api/v220")
app.include_router(treaties.router, prefix="/api/v250")
app.include_router(search.router, prefix="/api/v250")
app.include_router(intelligence.router, prefix="/api/v260")
app.include_router(evolution_v230.router, prefix="/api/v230")
app.include_router(pqc.router, prefix="/api/v230")
app.include_router(marketplace.router, prefix="/api/v230")
app.include_router(evolution_v240.router, prefix="/api/v240")
app.include_router(infra_v270.router, prefix="/api/v270")
app.include_router(ai_orchestration.router, prefix="/api")
app.include_router(csuite.router, prefix="/api")
app.include_router(csuite_enhanced.router, prefix="/api/v280")
app.include_router(gamification.router, prefix="/api/v280")
app.include_router(realms_v290.router, prefix="/api/v290")
app.include_router(ceo_generate.router, prefix="/api/v290")
app.include_router(marketplace_v290.router, prefix="/api/v290")
app.include_router(iot.router, prefix="/api/v290")
app.include_router(payments.router, prefix="/api/v310")
app.include_router(gov_v310.router, prefix="/api/v310")
app.include_router(business.router, prefix="/api/v310")
app.include_router(commerce.router, prefix="/api/v310")
app.include_router(fund.router, prefix="/api/v310")
app.include_router(intel_v320.router, prefix="/api/v320")
app.include_router(governance_autonomous.router, prefix="/api/v320")
app.include_router(treasury_intelligent.router, prefix="/api/v320")
app.include_router(markets.router, prefix="/api/v320")
app.include_router(consciousness.router, prefix="/api/v340")
app.include_router(soul_record.router, prefix="/api/v340")
app.include_router(ceo_v138.router, prefix="/api/v138")
app.include_router(v154_unified.router, prefix="/api")
app.include_router(v200_unified.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Jules AI v120.0 Apotheosis of Synergy Master Backend is operational."}

@app.get("/api/v1/status")
async def get_status():
    return {
        "organism_id": "JULES-v128-SOVEREIGN",
        "fidelity": 0.9998,
        "articles": 750,
        "mode": "UNIVERSAL-COMPLETION-INSTITUTIONAL-LEADERSHIP",
        "governance": policy.bms.generate_performance_report()
    }

# KNOWLEDGE ENDPOINTS
@app.get("/api/v1/knowledge/summary")
async def get_knowledge_summary():
    """ARTICLE 396: Unified knowledge summary for dashboards."""
    return {
        "graph_depth": 1420500,
        "nodes": 85000,
        "edges": 320000,
        "last_sync": "JUST_NOW",
        "genomic_operons": 12
    }

# TOKEN LEDGER ENDPOINTS
@app.get("/api/v1/tokens/ledger/{user_id}")
async def get_token_ledger(user_id: str):
    report = token_ledger.get_ledger_report(user_id)
    if "error" in report:
        # Onboarding trigger: Initialize new user with airdrop
        token_ledger.initialize_user(user_id, UserTier.FREE)
        report = token_ledger.get_ledger_report(user_id)
    return report

@app.post("/api/v1/admin/mint")
async def admin_mint(user_id: str, amount: float, reason: str = "Admin Minting"):
    """ARTICLE 591: Admin token minting."""
    success = token_ledger.mint(user_id, amount, reason)
    if not success:
        raise HTTPException(status_code=500, detail="Minting failed")
    return {"status": "SUCCESS", "message": f"Minted {amount} WST for {user_id}"}

# QEP ENDPOINTS
@app.get("/api/v1/qep/ayah/{reference}")
async def get_qep_ayah(reference: str, edition: str = "en.sahih"):
    """P0: Full Quran text, translation, and audio."""
    reactor = reactor_factory.get_reactor("religion", "quranic_studies")
    res = await reactor.incubate(reference, {"task": "get_ayah", "edition": edition})
    return res

# REACTOR ENDPOINTS
@app.get("/api/v1/reactors/{domain}/{sub_domain}")
async def run_reactor(domain: str, sub_domain: str, request: Request):
    params = dict(request.query_params)
    # Extract query 'q' or 'ref' as the primary input data for the reactor
    input_data = params.get("q") or params.get("ref") or "API_REQUEST"
    reactor = reactor_factory.get_reactor(domain, sub_domain)
    res = await reactor.incubate(input_data, params)
    return res

# POLICY & GOVERNANCE ENDPOINTS
@app.get("/api/v1/governance/blueprints")
async def get_blueprints():
    return policy.proposed_blueprints

@app.get("/api/v1/governance/okrs")
async def get_governance_okrs():
    """ARTICLE 346: Real-time OKR and PAS monitoring."""
    return policy.bms.generate_performance_report()

@app.get("/api/v1/cognitive/concepts")
async def get_cognitive_concepts():
    """ARTICLE 691: Access to the cognitive computing concept graph."""
    return scraper.cognitive_agent.perform_temporal_analysis()

@app.post("/api/v1/governance/blueprints/{blueprint_id}/approve")
async def approve_blueprint(blueprint_id: str):
    success = policy.approve_blueprint(blueprint_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blueprint not found or already approved")
    return {"status": "SUCCESS", "message": f"Blueprint {blueprint_id} approved."}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "128.0.0"}

@app.get("/health")
async def health_root():
    return {"status": "healthy", "version": "128.0.0"}
