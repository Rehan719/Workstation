from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jules AI v99.0 Transcendent Master Backend")

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
    return {"message": "Jules AI v99.0 Transcendent Master Backend is operational."}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "99.0.0", "era": "TRANSCENDENT"}

@app.get("/api/v1/status")
async def get_status():
    return {
        "organism_id": "JULES-v99-MASTER",
        "fidelity": 0.992,
        "articles": 297,
        "mode": "OMNI-CONVERGENCE"
    }
