from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any, List, Optional
from agentic_core.reactor.religion.quranic_studies import QuranicStudiesReactor
from agentic_core.enterprise.policy import PolicyCoE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jules AI v120.0 Apotheosis of Synergy Master Backend")

# Initialize global CoEs and Reactors
policy = PolicyCoE()
quran_reactor = QuranicStudiesReactor()

# Article 284: Unified Product Interface / CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://workstation-pwa.vercel.app",
        "http://localhost:5173",          # for local development
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Jules AI v120.0 Apotheosis of Synergy Master Backend is operational."}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "120.0.0", "era": "APOTHEOSIS_OF_SYNERGY"}

@app.get("/api/v1/status")
async def get_status():
    return {
        "organism_id": "JULES-v120-MASTER",
        "fidelity": 0.995,
        "articles": 540,
        "mode": "APOTHEOSIS-OF-SYNERGY",
        "governance": policy.bms.generate_performance_report()
    }

@app.get("/api/v1/qep/ayah/{reference}")
async def get_ayah(reference: str, edition: Optional[str] = "en.sahih"):
    res = await quran_reactor.incubate(reference, {"task": "get_ayah", "edition": edition})
    if res["status"] == "SUCCESS":
        return res
    raise HTTPException(status_code=404, detail=res.get("message", "Ayah not found"))

@app.get("/api/v1/qep/search")
async def search_quran(q: str):
    res = await quran_reactor.incubate(q, {"task": "search"})
    if res["status"] == "SUCCESS":
        return res
    raise HTTPException(status_code=400, detail=res.get("message", "Search failed"))

@app.get("/api/v1/governance/okrs")
async def get_okrs():
    return policy.bms.generate_performance_report()
