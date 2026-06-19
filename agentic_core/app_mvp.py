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

from agentic_core.config import settings

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Workstation",
    description="AI-Mediated Workspace — Commercial MVP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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

# 22. Career / Employment domain (Application Studio, job search, doc generation)
from agentic_core.api import career as career_api
app.include_router(career_api.router)

# 23. Law domain (contract analysis, legal document factory)
from agentic_core.api import law as law_api
app.include_router(law_api.router)

# 24. Science domain (research synthesis, hypothesis generation, literature review)
from agentic_core.api import science as science_api
app.include_router(science_api.router)

# 25. Education domain (curriculum design, lesson plans, assessments)
from agentic_core.api import education as education_api
app.include_router(education_api.router)

# 26. Care domain (care plans, risk assessment, clinical handover)
from agentic_core.api import care as care_api
app.include_router(care_api.router)

# ── Agent Collaboration Hub + additional routers ──────────────────────────────

# 27. Agent Collaboration Hub (SSE message bus, handoffs, agent registry)
#     data/agent_messages/, data/handoffs/, data/agent_registry/ must exist
from agentic_core.api import agent_hub
app.include_router(agent_hub.router, prefix="/api/v1")

# 28. AI Orchestration (multi-agent CEO delegation)
from agentic_core.api import ai_orchestration
app.include_router(ai_orchestration.router, prefix="/api")

# 29. Partnerships / Diplomatic Corps
from agentic_core.api import partnerships
app.include_router(partnerships.router, prefix="/api")

# 30. QEP Analytics (Quran Education Platform analytics)
from agentic_core.api import qep_analytics
app.include_router(qep_analytics.router, prefix="/api")

# 31. Tool Ecosystem (tool discovery and invocation)
from agentic_core.api import tools as tools_api
app.include_router(tools_api.router, prefix="/api")

# 32. Cross-Platform Bridge (wearable, voice, AR — Phase 3 scaffolding)
#     Refactored from FastAPI() sub-app to APIRouter (2026-06-18)
from agentic_core.api import cross_platform
app.include_router(cross_platform.api, prefix="/api")

# 33. Religion domain (fiqh research, Quran tafsir, halal review, interfaith)
from agentic_core.api import religion as religion_api
app.include_router(religion_api.router)

# 34. Human Synthesis Studio + VSB entity spawning (concept → commercialisation cascade)
from agentic_core.api import synthesis_studio
app.include_router(synthesis_studio.router)

# 35. AI Agent Swarm Orchestration (CEO → C-Suite → CoE delegation)
from agentic_core.api import swarm as swarm_api
app.include_router(swarm_api.router)

# 36. Digital Twin & Simulation (AI model generation + scenario simulation)
from agentic_core.api import digital_twin as twin_api
app.include_router(twin_api.router)

# 37. IDBO Self-Healing (circuit breaker status + healing log)
from agentic_core.organism import self_healing as self_healing_api
app.include_router(self_healing_api.router)

# 38. Management Systems (QMS/BMS/DCS/Audit/Risk Register — ISO 9001-aligned)
from agentic_core.api import management_systems as mgmt_api
app.include_router(mgmt_api.router)

# 39. Sovereign Capital Fund + VSB Marketplace
from agentic_core.api import capital_fund as fund_api
app.include_router(fund_api.router)

# 40. VSB Full Spawn Pipeline (Cascade → MJM → Genomic Registry → Agent Swarm)
from agentic_core.api import vsb as vsb_api
app.include_router(vsb_api.router)

# 41. Nine Cognitive Engines + MJM HTTP surface
from agentic_core.api import cognitive as cognitive_api
app.include_router(cognitive_api.router)

# 42. Business Development Process + Scientific Process Intelligence Engines
from agentic_core.api import intelligence as intelligence_api
app.include_router(intelligence_api.router)

# 43. Auth (JWT + API key — single-user by default, multi-user with AUTH_ENABLED=true)
from agentic_core.auth import core as auth_api
app.include_router(auth_api.router)

# 44. QEP — Quran Education Platform (Hifz SM-2 + Tajweed + Gamification)
from agentic_core.religious_domain import api as qep_api
app.include_router(qep_api.router)

# 45. IDBO Nervous System (signal routing, reflex arcs, arousal state)
from agentic_core.organism import nervous as nervous_api
app.include_router(nervous_api.router)

# 45. IDBO Reconfiguration Engine (runtime feature flags, provider config)
from agentic_core.organism import reconfiguration as reconfig_api
app.include_router(reconfig_api.router)

# 46. IDBO Genome System (project trait encoding, crossover, mutation)
from agentic_core.organism import genome as genome_api
app.include_router(genome_api.router)

# 47. Master Organism Status + Homeostasis
from agentic_core.api import organism_status as organism_status_api
app.include_router(organism_status_api.router)

# 48. Change Control Agency (arms-length governance for organism changes)
from agentic_core.api import change_control as cca_api
app.include_router(cca_api.router)

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
    """Organism vitals: psutil + project store + immune system + ATPSimulator + NervousSystem."""
    from agentic_core.projects.api import _all_projects
    from agentic_core.organism.immune import immune
    from agentic_core.organism.nervous import nervous

    try:
        projects = _all_projects()
        active = sum(1 for p in projects if p.status == "running")
    except Exception:
        projects = []
        active = 0

    cpu  = psutil.cpu_percent(interval=None)
    mem  = psutil.virtual_memory()
    ws   = len(_ws.connections)
    imm  = immune.status()
    nervous_status = nervous.status()

    resource_flow = max(0.0, 100.0 - cpu)
    peristaltic_delay = round(max(1, mem.percent / 20), 1)

    # ATP Simulator — molecular energy model (real biomimetic calculation)
    try:
        from agentic_core.molecular.atp_simulator import ATPSimulator
        if not hasattr(biometrics_status, "_atp"):
            biometrics_status._atp = ATPSimulator()
        circadian_efficiency = 1.0 if _circadian_cycle() == "ACTIVE_FOCUS" else 0.8
        metabolic_load = cpu / 100.0
        biometrics_status._atp.update(dt=1.0, metabolic_load=metabolic_load, circadian_efficiency=circadian_efficiency)
        atp_ratio = round(max(0.0, min(1.0, biometrics_status._atp.ratio)), 3)
    except Exception:
        atp_ratio = round(resource_flow / 100.0, 3)

    # Cognition degrades under immune stress
    immune_health = imm["health"]
    if active > 2 or cpu > 70:
        cognition_state = "FLOURISHING" if immune_health > 0.5 else "STRESSED"
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

    # Metabolic: ATP ratio + project stage ratio combined
    total_projects = len(projects)
    concept_count = sum(1 for p in projects if p.stage == "concept")
    stage_efficiency = round(
        1.0 - (concept_count / total_projects) if total_projects > 0 else 1.0, 3
    )
    metabolic_efficiency = round((atp_ratio + stage_efficiency) / 2, 3)

    return {
        "circadian":      {"cycle": _circadian_cycle()},
        "cardiovascular": {"resource_flow": round(resource_flow, 1), "peristaltic_delay": peristaltic_delay},
        "cognition":      {"state": cognition_state, "primary_drive": primary_drive},
        "communication":  {"active_channels": ["WS"] if ws > 0 else [], "neurotransmitter": neurotransmitter, "is_active": ws > 0},
        "immune":         imm,
        "metabolic":      {"efficiency": metabolic_efficiency, "atp_ratio": atp_ratio, "concept_projects": concept_count, "total_projects": total_projects},
        "nervous":        {"arousal_state": nervous_status["arousal_state"], "signal_rate": nervous_status["signal_rate_per_second"]},
    }


@app.get("/health")
@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "1.0.0", "app": "workstation-mvp"}


@app.get("/api/v1/system/info")
async def system_info():
    """Non-sensitive system configuration summary for ops/monitoring."""
    return {
        "environment": settings.environment,
        "auth_enabled": settings.auth_enabled,
        "has_ai_provider": settings.has_ai_provider,
        "gateway_rpm": settings.gateway_rpm,
        "default_model": settings.default_model,
        "cors_origins_count": len(settings.cors_origins),
        "cors_wildcard": "*" in settings.cors_origins,
        "config_warnings": settings.validate(),
    }


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


@app.on_event("startup")  # noqa: deprecated — lifespan refactor is Phase 1
async def _startup():
    asyncio.create_task(_vitals_loop())
    logger.info("Workstation MVP started — spine routers only.")
