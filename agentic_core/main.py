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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global CoEs and Reactors
policy = PolicyCoE()
reactor_factory = ReactorFactory()
token_ledger = TokenLedger()
scraper = DualModeScraper(token_ledger=token_ledger)

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
        "organism_id": "JULES-v120-MASTER",
        "fidelity": 0.998,
        "articles": 600,
        "mode": "APOTHEOSIS-OF-SENSORY-CONVERGENCE",
        "governance": policy.bms.generate_performance_report()
    }

# TOKEN LEDGER ENDPOINTS
@app.get("/api/v1/tokens/ledger/{user_id}")
async def get_token_ledger(user_id: str):
    report = token_ledger.get_ledger_report(user_id)
    if "error" in report:
        raise HTTPException(status_code=404, detail="User not found")
    return report

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

@app.post("/api/v1/governance/blueprints/{blueprint_id}/approve")
async def approve_blueprint(blueprint_id: str):
    success = policy.approve_blueprint(blueprint_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blueprint not found or already approved")
    return {"status": "SUCCESS", "message": f"Blueprint {blueprint_id} approved."}

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "version": "120.0.0"}
