"""
Charitable-Giving Intelligence — the "nutrient-return" loop of the economic metabolism.

Allocates the charity budget intelligently, not arbitrarily: candidate causes are
scored on urgency × gravity × reach × marginal-impact-of-funds × trust, ranked,
and the budget is distributed to the top causes for maximal relief.

PROVENANCE (W415): those five per-cause inputs are CURATED editorial weights encoding the
Owner directive below — they are not measured, sourced or verified needs/impact/trust data.
The ranking arithmetic over them is real; the numbers going in are hand-set. Every emitting
path (`ranked`, `allocate`) now says so, so a reader of a cycle report cannot mistake a
typed 0.92 for a rating something produced.

Owner directives (2026-06-21):
  • Prioritise: WATER · Orphan Sponsorship · Conflict (& natural disaster) · Dawah.
  • EXCLUDE any cause without a 100% donation policy (every WST given reaches the cause).
  • Halal / ethical only (enforced + checked via the unified compliance engine).

`ingest_live_signals()` is the clean seam for approved real-world feeds
(humanitarian/disaster/needs APIs). All allocations are virtual/simulated.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, load_json_tolerant

_DIRECTIVES_STORE = data_path("economy_charity_directives.json")
_SIGNALS_STORE = data_path("economy_charity_signals.json")

# W415 — these 0..1 numbers reached the Owner inside EVERY cycle report's `giving_back` (and the
# VSB cockpit / board pack) reading as per-cause ratings — "trust 0.92", "urgency 0.85" — and
# `donation_100pct: True` read as a verified policy check. Nothing measures or verifies any of
# them: they are editorial priority weights a maintainer typed to encode the 2026-06-21 Owner
# directive. They are KEPT (they are the ranking knobs, and the ranking over them is real
# arithmetic), but every path that emits them now labels their provenance, and the unverified
# 100%-donation claim is reported as not_checked rather than asserted as true.
# Curated candidate causes (categories). `donation_100pct` is a hand-set ELIGIBILITY FLAG, not a
# verification: it records the Owner's rule that only 100%-donation causes may be funded.
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

# Owner-prioritised cause ids (receive a scoring boost) — the 2026-06-21 defaults; the Owner can
# adjust at runtime via the persisted directives (GET/POST /api/v1/economy/charity/directives).
_PRIORITIES = ["clean_water", "orphan_sponsorship", "conflict_relief", "dawah"]


def get_directives() -> Dict[str, Any]:
    """The Owner's persisted charity directives (priorities · exclusions · 100%-donation rule),
    falling back to the 2026-06-21 defaults when never set."""
    d = load_json_tolerant(_DIRECTIVES_STORE, {}) or {}
    return {
        "priorities": list(d.get("priorities") or _PRIORITIES),
        "exclusions": list(d.get("exclusions") or []),
        "require_100pct": bool(d.get("require_100pct", True)),
        "source": "owner_set" if d else "defaults (2026-06-21 Owner directive)",
        "updated_at": d.get("updated_at"),
    }


def set_directives(priorities: Optional[List[str]] = None, exclusions: Optional[List[str]] = None,
                   require_100pct: bool = True) -> Dict[str, Any]:
    """Persist the Owner's charity directives — honoured by EVERY subsequent allocation (the
    metabolic cycle constructs CharityIntelligence with these as its defaults)."""
    d = {
        "priorities": [str(p) for p in (priorities or []) if str(p).strip()] or _PRIORITIES,
        "exclusions": [str(x) for x in (exclusions or []) if str(x).strip()],
        "require_100pct": bool(require_100pct),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    atomic_write_json(_DIRECTIVES_STORE, d)
    return get_directives()


def approved_signals() -> List[Dict[str, Any]]:
    """Owner-approved live signals (the gated ingestion seam) — persisted candidates that mirror the
    curated dict shape. Empty until the Owner enables + supplies sources."""
    rows = load_json_tolerant(_SIGNALS_STORE, []) or []
    return [r for r in rows if isinstance(r, dict) and r.get("id") and r.get("cause")]


class CharityIntelligence:
    """Scores, ranks, and allocates the charity budget for maximal outcome impact."""

    def __init__(self, exclusions: Optional[List[str]] = None,
                 priorities: Optional[List[str]] = None, require_100pct: Optional[bool] = None):
        # No explicit args → the Owner's PERSISTED directives are the defaults, so every call site
        # (the metabolic cycle, the API) honours them with zero call-site changes.
        directives = get_directives()
        self.exclusions = set(exclusions if exclusions is not None else directives["exclusions"])
        self.priorities = set(priorities if priorities is not None else directives["priorities"])
        self.require_100pct = bool(directives["require_100pct"] if require_100pct is None else require_100pct)
        self._live: List[Dict[str, Any]] = approved_signals()   # the gated ingestion seam (empty until enabled)

    def ingest_live_signals(self, signals: List[Dict[str, Any]]) -> None:
        """Seam for approved real-world feeds. Each signal mirrors a candidate dict."""
        self._live = signals or []

    def _candidates(self) -> List[Dict[str, Any]]:
        # W415 — curated rows and Owner-supplied signal rows were indistinguishable once merged, so
        # a consumer could not tell a hand-typed weight from an ingested one. Tag the origin.
        # W442 — "owner_signal" asserted Owner provenance for rows an API caller typed; the label
        # now says what the values actually are.
        pool = ([{**c, "weights_source": "curated"} for c in _CANDIDATES]
                + [{**s, "weights_source": "owner_signal (ingested; caller-asserted values)"}
                   for s in self._live])
        pool = [c for c in pool if c["id"] not in self.exclusions]
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
        # W442 — ranked rows shipped the raw donation_100pct flag unlabelled; on the candidates
        # surface it read as a verified policy check. allocate() already reports it honestly —
        # now the rows do too.
        scored = [{**c, "score": self.score(c), "marginal_impact": self._marginal_impact(c),
                   "donation_100pct_verified": "not_checked"}
                  for c in self._candidates()]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top]

    def allocate(self, budget: float, top: int = 5) -> Dict[str, Any]:
        """Distribute ``budget`` (WST, virtual) across the top causes, weighted by score. EVERY
        grant's cause is screened through the unified compliance engine (Sharia/Halal · UK Legal ·
        Regulatory · EHS · Ethical) BEFORE allocation — a failing cause receives nothing and is
        listed honestly in `excluded_by_compliance`."""
        winners = self.ranked(top)
        # §5 Owner directive: halal/ethical only — the REAL federated screen, not just the static flag
        cleared: List[Dict[str, Any]] = []
        excluded: List[Dict[str, Any]] = []
        for w in winners:
            try:
                from agentic_core.api.compliance import screen_compliance
                screen = screen_compliance(f"charitable grant to: {w['cause']} ({w['region']})")
                statuses = [v.get("status") for v in (screen.get("verdicts") or [])]
                verdict = "fail" if "fail" in statuses else ("review" if "review" in statuses else "pass")
            except Exception:
                verdict = "unscreened (engine unavailable)"
            if verdict == "fail":
                excluded.append({"id": w["id"], "cause": w["cause"], "compliance": verdict})
            else:
                cleared.append({**w, "compliance": verdict})
        weight_sum = sum(w["score"] for w in cleared) or 1.0
        grants = []
        for w in cleared:
            amount = round(budget * (w["score"] / weight_sum), 2)
            # W415 — this carried `donation_100pct: True`, a flat assertion that 100% of the grant
            # reaches the cause. Nothing verifies that; it is a hand-set eligibility flag on a cause
            # CATEGORY, and no delivery organisation is even named yet. State the rule that actually
            # ran, and report the missing check as missing.
            grants.append({"id": w["id"], "cause": w["cause"], "region": w["region"],
                           "score": w["score"], "amount_wst": amount,
                           "donation_100pct_required_by_directive": self.require_100pct,
                           "donation_100pct_verified": "not_checked",
                           "weights_source": w.get("weights_source", "curated"),
                           "compliance": w["compliance"]})
        return {
            "budget_wst": round(budget, 2),
            # W415 — `method` asserted the split was driven by measured urgency/gravity/reach/trust.
            # The weighting arithmetic is real; the inputs are editorial weights nobody measured,
            # and the string never said so — which is what made the ratings credible downstream.
            "method": ("weighted rank over CURATED priority weights (urgency · gravity · reach · "
                       "marginal-impact · trust), budget split pro-rata by score; 100%-donation "
                       "causes only; every grant compliance-screened (halal/ethical)"),
            "weights_provenance": ("curated — the 0..1 cause weights are editorial values encoding the "
                                   "Owner's 2026-06-21 directive; no needs, impact or trust data is "
                                   "measured or sourced. Live feeds pending Owner approval."),
            "priorities": sorted(self.priorities),
            "grants": grants,
            "excluded_by_compliance": excluded,
            "disclaimer": "Virtual/simulated allocation — no real funds moved.",
        }
