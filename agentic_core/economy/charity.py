"""
Charitable-Giving Intelligence — the "nutrient-return" loop of the economic metabolism.

Allocates the charity budget intelligently, not arbitrarily: candidate causes are
scored on urgency × gravity × reach × marginal-impact-of-funds × trust, ranked,
and the budget is distributed to the top causes for maximal relief.

Owner directives (2026-06-21):
  • Prioritise: WATER · Orphan Sponsorship · Conflict (& natural disaster) · Dawah.
  • EXCLUDE any cause without a 100% donation policy (every WST given reaches the cause).
  • Halal / ethical only (enforced + checked via the unified compliance engine).

`ingest_live_signals()` is the clean seam for approved real-world feeds
(humanitarian/disaster/needs APIs). All allocations are virtual/simulated.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

# Curated candidate causes (categories). 0..1 metrics. `donation_100pct`: only causes
# that pass 100% of donations to the cause are eligible (Owner directive).
_CANDIDATES: List[Dict[str, Any]] = [
    {"id": "clean_water", "cause": "Clean water & wells (WATER)", "region": "global",
     "urgency": 0.85, "gravity": 0.90, "reach": 0.92, "trust": 0.92, "donation_100pct": True},
    {"id": "orphan_sponsorship", "cause": "Orphan sponsorship & welfare", "region": "global",
     "urgency": 0.80, "gravity": 0.92, "reach": 0.85, "trust": 0.92, "donation_100pct": True},
    {"id": "conflict_relief", "cause": "Conflict & natural-disaster relief", "region": "global",
     "urgency": 0.97, "gravity": 0.97, "reach": 0.85, "trust": 0.88, "donation_100pct": True},
    {"id": "dawah", "cause": "Dawah & Islamic education", "region": "global",
     "urgency": 0.55, "gravity": 0.80, "reach": 0.88, "trust": 0.90, "donation_100pct": True},
    {"id": "famine_food", "cause": "Famine & food security", "region": "global",
     "urgency": 0.90, "gravity": 0.95, "reach": 0.80, "trust": 0.85, "donation_100pct": True},
    {"id": "emergency_health", "cause": "Emergency healthcare", "region": "global",
     "urgency": 0.85, "gravity": 0.90, "reach": 0.80, "trust": 0.88, "donation_100pct": True},
    {"id": "refugee_support", "cause": "Refugee & displacement support", "region": "global",
     "urgency": 0.85, "gravity": 0.90, "reach": 0.75, "trust": 0.80, "donation_100pct": True},
]

# Owner-prioritised cause ids (receive a scoring boost).
_PRIORITIES = ["clean_water", "orphan_sponsorship", "conflict_relief", "dawah"]


class CharityIntelligence:
    """Scores, ranks, and allocates the charity budget for maximal outcome impact."""

    def __init__(self, exclusions: Optional[List[str]] = None,
                 priorities: Optional[List[str]] = None, require_100pct: bool = True):
        self.exclusions = set(exclusions or [])
        self.priorities = set(priorities or _PRIORITIES)
        self.require_100pct = require_100pct   # Owner directive: 100%-donation causes only
        self._live: List[Dict[str, Any]] = []

    def ingest_live_signals(self, signals: List[Dict[str, Any]]) -> None:
        """Seam for approved real-world feeds. Each signal mirrors a candidate dict."""
        self._live = signals or []

    def _candidates(self) -> List[Dict[str, Any]]:
        pool = [c for c in (_CANDIDATES + self._live) if c["id"] not in self.exclusions]
        if self.require_100pct:
            pool = [c for c in pool if c.get("donation_100pct", False)]
        return pool

    @staticmethod
    def _marginal_impact(c: Dict[str, Any]) -> float:
        return round((c["urgency"] * 0.5 + c["gravity"] * 0.5), 3)

    def score(self, c: Dict[str, Any]) -> float:
        base = (c["urgency"] * 0.30 + c["gravity"] * 0.30 + c["reach"] * 0.15
                + self._marginal_impact(c) * 0.15 + c["trust"] * 0.10)
        if c["id"] in self.priorities:
            base = min(1.0, base + 0.12)   # Owner-prioritised boost
        return round(base, 4)

    def ranked(self, top: int = 5) -> List[Dict[str, Any]]:
        scored = [{**c, "score": self.score(c), "marginal_impact": self._marginal_impact(c)}
                  for c in self._candidates()]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top]

    def allocate(self, budget: float, top: int = 5) -> Dict[str, Any]:
        """Distribute ``budget`` (WST, virtual) across the top causes, weighted by score."""
        winners = self.ranked(top)
        weight_sum = sum(w["score"] for w in winners) or 1.0
        grants = []
        for w in winners:
            amount = round(budget * (w["score"] / weight_sum), 2)
            grants.append({"id": w["id"], "cause": w["cause"], "region": w["region"],
                           "score": w["score"], "amount_wst": amount, "donation_100pct": True})
        return {
            "budget_wst": round(budget, 2),
            "method": "urgency × gravity × reach × marginal-impact × trust; 100%-donation causes only",
            "priorities": _PRIORITIES,
            "grants": grants,
            "disclaimer": "Virtual/simulated allocation — no real funds moved.",
        }
