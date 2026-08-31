"""
C-Suite API — real metrics computed from the project store and token ledger.

GET /api/csuite/cfo/metrics
GET /api/csuite/cto/infrastructure
"""
from __future__ import annotations

import time

import psutil
from fastapi import APIRouter

router = APIRouter(prefix="/csuite", tags=["C-Suite"])


def _project_stats() -> dict:
    """Load portfolio stats from the projects store. Fails gracefully."""
    try:
        from agentic_core.projects.api import _all_projects
        projects = _all_projects()
        total = len(projects)
        by_stage = {"concept": 0, "prototype": 0, "commercialise": 0}
        total_outputs = 0
        active = 0
        for p in projects:
            by_stage[p.stage] = by_stage.get(p.stage, 0) + 1
            total_outputs += len(p.outputs)
            if p.status == "running":
                active += 1
        return {
            "total": total,
            "by_stage": by_stage,
            "total_outputs": total_outputs,
            "active": active,
            "complete": by_stage.get("commercialise", 0),
        }
    except Exception:
        return {"total": 0, "by_stage": {}, "total_outputs": 0, "active": 0, "complete": 0}


def _token_stats() -> dict:
    """Pull usage stats from the token ledger. Fails gracefully."""
    try:
        from agentic_core.commercial.token_ledger import ledger
        user_data = ledger.get_balance("demo_user")
        return {
            "balance":    user_data.get("balance", 0),
            "tier":       user_data.get("tier", "FREE"),
            "spend_24h":  user_data.get("spend_24h", 0),
        }
    except Exception:
        return {"balance": 0, "tier": "FREE", "spend_24h": 0}


@router.get("/cfo/metrics")
async def get_cfo_metrics() -> dict:
    """Real portfolio and ledger figures. No monetary valuation is synthesised.

    W410 - the docstring here used to read "All values are calculated from real data - no hardcoded
    literals", directly above a body that was nothing but hardcoded literals:
        stage_values  = {"concept": 1_000, "prototype": 5_000, "commercialise": 15_000}
        output_value  = total_outputs * 250        # "each deliverable = $250 value unit"
        cost_per_project = 120                     # "AI inference + infra per project"
        unrealised    = prototype * 500 + concept * 100
        realised      = complete * 2_500
        growth        = f"+{min(total * 4.2, 99.9):.1f}%"
    The COUNTS are real; every multiplier was invented, so "revenue", "growth", "liquidity" and
    "ROI" were invented too. A docstring asserting the opposite is worse than silence: it forecloses
    the question for anyone reading the code.

    Counts and the real token ledger are reported. Valuation is not, because nothing values a
    project.
    """
    s = _project_stats()
    t = _token_stats()
    return {
        "portfolio": {
            "total_projects": s["total"],
            "by_stage": s["by_stage"],
            "complete": s["complete"],
            "active": s["active"],
            "total_outputs": s["total_outputs"],
        },
        "token_balance": t["balance"],
        "token_tier": t["tier"],
        "token_spend_24h": t["spend_24h"],
        "currency": "WST (virtual)",
        "valuation": None,
        "kpis": [
            {"label": "Projects", "value": str(s["total"])},
            {"label": "Deliverables", "value": str(s["total_outputs"])},
            {"label": "Commercialised", "value": str(s["complete"])},
            {"label": "Active", "value": str(s["active"])},
        ],
        "note": ("Revenue, growth, liquidity and ROI are not reported. They were previously derived "
                 "from project counts multiplied by invented constants."),
        "computed_at": time.time(),
    }

@router.get("/cto/infrastructure")
async def get_cto_infra() -> dict:
    """
    Infrastructure metrics from psutil (real) + project activity (real).
    """
    s = _project_stats()
    cpu    = psutil.cpu_percent(interval=0.1)
    mem    = psutil.virtual_memory()
    disk   = psutil.disk_usage("/")

    return {
        "cpu_percent":    cpu,
        "memory_percent": mem.percent,
        "memory_used_gb": round(mem.used / 1e9, 2),
        "disk_percent":   disk.percent,
        "active_projects": s["active"],
        "total_projects":  s["total"],
        "total_outputs":   s["total_outputs"],
        # W410 — "uptime": "99.9%" and "pqc_status": "Enforced" used to sit here, in a payload
        # whose docstring frames it as real instrumentation and whose neighbours genuinely are
        # psutil readings. That framing is what made them dangerous: a consumer reads 99.9% as
        # measured availability and "Enforced" as a verified post-quantum posture. Nothing tracks
        # uptime and nothing checks or enforces PQC. Reported as unmeasured rather than removed,
        # so the absence is visible.
        "uptime":          None,
        "pqc_status":      "not_checked",
        "ai_provider":     "Anthropic Claude" if __import__("os").getenv("ANTHROPIC_API_KEY") else "Ollama (local)",
        "computed_at":     time.time(),
    }
