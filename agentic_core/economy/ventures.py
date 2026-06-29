"""
User-Project Investment Intelligence (§6) — the "seeding offspring" stage of the economic metabolism.

Competitively selects user projects/ventures for investment, not arbitrarily: candidates are scored on
outcome-success × value × benefit × feasibility × strategic-fit, ranked, and the §4 `user_projects` budget is
distributed to the top ventures — then tracked as **portfolio positions** so returns can recycle into the
waterfall (a compounding ecosystem).

Candidate ventures can be injected (the real user projects); a small curated DEMO set is the honest fallback
until real user-project ingestion is wired. All allocations are virtual/simulated WST.
"""
from __future__ import annotations

import json
import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import data_path

_PORTFOLIO_STORE = data_path("economy_ventures_portfolio.json")

# Sample candidate ventures (DEMO — replaced by real user projects when injected). Metrics are 0..1.
_DEMO_VENTURES: List[Dict[str, Any]] = [
    {"id": "v_health_triage", "name": "Community health-triage assistant", "domain": "care",
     "outcome": 0.85, "value": 0.80, "benefit": 0.90, "feasibility": 0.78, "strategic_fit": 0.82},
    {"id": "v_legal_aid", "name": "Free legal-aid document drafter", "domain": "law",
     "outcome": 0.80, "value": 0.75, "benefit": 0.88, "feasibility": 0.82, "strategic_fit": 0.80},
    {"id": "v_edu_tutor", "name": "Adaptive tutor for under-resourced schools", "domain": "education",
     "outcome": 0.82, "value": 0.78, "benefit": 0.92, "feasibility": 0.75, "strategic_fit": 0.85},
    {"id": "v_halal_supply", "name": "Halal supply-chain verification", "domain": "religion",
     "outcome": 0.78, "value": 0.85, "benefit": 0.75, "feasibility": 0.80, "strategic_fit": 0.83},
    {"id": "v_green_logistics", "name": "Zero-waste last-mile logistics", "domain": "enterprise",
     "outcome": 0.76, "value": 0.82, "benefit": 0.80, "feasibility": 0.72, "strategic_fit": 0.78},
]

_METRICS = ("outcome", "value", "benefit", "feasibility", "strategic_fit")


class VentureIntelligence:
    """Scores, ranks, and allocates the user-project investment budget for maximal outcome/value/benefit."""

    def __init__(self, candidates: Optional[List[Dict[str, Any]]] = None):
        # accept real user projects; fall back to the curated demo set (honest: sample candidates)
        self.candidates = candidates if candidates else _DEMO_VENTURES
        self.using_demo = not bool(candidates)

    @staticmethod
    def _g(v: Dict[str, Any], k: str) -> float:
        try:
            return max(0.0, min(1.0, float(v.get(k, 0.5))))
        except (TypeError, ValueError):
            return 0.5

    def score(self, v: Dict[str, Any]) -> float:
        return round(self._g(v, "outcome") * 0.30 + self._g(v, "value") * 0.25
                     + self._g(v, "benefit") * 0.20 + self._g(v, "feasibility") * 0.15
                     + self._g(v, "strategic_fit") * 0.10, 4)

    def ranked(self, top: int = 5) -> List[Dict[str, Any]]:
        scored = [{**v, "score": self.score(v)} for v in self.candidates]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top]

    def allocate(self, budget: float, top: int = 5) -> Dict[str, Any]:
        """Distribute ``budget`` (WST, virtual) across the top ventures, weighted by score."""
        winners = self.ranked(top)
        weight_sum = sum(w["score"] for w in winners) or 1.0
        positions = []
        for w in winners:
            amount = round(max(0.0, budget) * (w["score"] / weight_sum), 2)
            positions.append({"id": w["id"], "name": w.get("name", w["id"]), "domain": w.get("domain", ""),
                              "score": w["score"], "amount_wst": amount})
        return {
            "budget_wst": round(max(0.0, budget), 2),
            "method": "outcome × value × benefit × feasibility × strategic-fit",
            "using_demo_candidates": self.using_demo,
            "positions": positions,
            "disclaimer": "Virtual/simulated investment — no real funds moved.",
        }


# ── Portfolio persistence (§6: tracked as portfolio positions; returns recycle into the waterfall) ─────────

def _load_portfolio() -> Dict[str, Any]:
    try:
        return json.loads(_PORTFOLIO_STORE.read_text()) if _PORTFOLIO_STORE.exists() else {}
    except Exception:
        return {}


def _save_portfolio(d: Dict[str, Any]) -> None:
    _PORTFOLIO_STORE.parent.mkdir(parents=True, exist_ok=True)
    _PORTFOLIO_STORE.write_text(json.dumps(d, indent=2))


def record_positions(vsb_id: str, allocation: Dict[str, Any]) -> None:
    """Track an allocation's positions in the VSB's venture portfolio (virtual; best-effort)."""
    positions = (allocation or {}).get("positions") or []
    if not positions:
        return
    d = _load_portfolio()
    pf = d.get(vsb_id) or {"vsb_id": vsb_id, "currency": "WST", "invested_total": 0.0, "holdings": {}}
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for p in positions:
        if p.get("amount_wst", 0) <= 0:
            continue
        h = pf["holdings"].get(p["id"]) or {"id": p["id"], "name": p["name"], "domain": p.get("domain", ""),
                                            "invested_wst": 0.0, "rounds": 0}
        h["invested_wst"] = round(h["invested_wst"] + p["amount_wst"], 2)
        h["rounds"] += 1
        h["last_round_at"] = at
        h["last_score"] = p.get("score")
        pf["holdings"][p["id"]] = h
        pf["invested_total"] = round(pf["invested_total"] + p["amount_wst"], 2)
    pf["positions_count"] = len(pf["holdings"])
    pf["updated_at"] = at
    d[vsb_id] = pf
    _save_portfolio(d)


def portfolio(vsb_id: str) -> Dict[str, Any]:
    pf = _load_portfolio().get(vsb_id)
    if not pf:
        return {"vsb_id": vsb_id, "currency": "WST", "invested_total": 0.0,
                "positions_count": 0, "holdings": [], "note": "No venture investments yet (virtual)."}
    holdings = sorted(pf["holdings"].values(), key=lambda h: h["invested_wst"], reverse=True)
    return {"vsb_id": vsb_id, "currency": "WST", "invested_total": pf["invested_total"],
            "positions_count": pf.get("positions_count", len(holdings)), "holdings": holdings,
            "updated_at": pf.get("updated_at"),
            "note": "Virtual/simulated venture portfolio — no real funds moved."}
