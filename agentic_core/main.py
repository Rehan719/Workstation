from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
import os
from contextlib import asynccontextmanager
from typing import Dict, Any, List, Optional
from agentic_core.reactor.religion.quranic_studies import QuranicStudiesReactor
from agentic_core.reactor.ecosystem.factory import ReactorFactory
from agentic_core.enterprise.policy import PolicyCoE
from agentic_core.commercial.token_ledger import TokenLedger, UserTier
from agentic_core.synthesis.dual_mode_scraper import DualModeScraper
from agentic_core.synthesis.uviap import UVIAP

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

    yield
    task.cancel()
    logger.info("Apotheosis: System Hibernating.")

app = FastAPI(
    title="Jules AI v120.0 Apotheosis of Sensory Convergence Master Backend",
    lifespan=lifespan
)

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
        "organism_id": "JULES-v124-MASTER",
        "fidelity": 0.9992,
        "articles": 690,
        "mode": "GENOMIC-RESONANCE-EVOLUTIONARY-CONVERGENCE",
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
    return {"status": "healthy", "version": "124.0.0"}

@app.get("/health")
async def health_root():
    return {"status": "healthy", "version": "124.0.0"}
