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
import math
import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import data_path, load_json_tolerant, store_lock

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

# Deterministic stage → progression score (how far the venture has REALLY progressed).
_STAGE_SCORE = {"concept": 0.45, "prototype": 0.62, "build": 0.70, "development": 0.70,
                "commercialise": 0.85, "operational": 0.85}
# Beneficence-weighted domains (the Owner's §2 values: care for people first) — a documented POLICY
# weight over the real domain field, not an estimate.
_BENEFIT_DOMAINS = ("care", "education", "religion", "law", "charity", "health")


def real_candidates(exclude_vsb: str = "", cap: int = 40,
                    user: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Harvest REAL investment candidates from the platform's own stores — the user's projects and
    the living VSB offspring — with metrics derived DETERMINISTICALLY from observable state (stage,
    operational status, governance completeness, beneficence-weighted domain). No metric is invented:
    each is a documented policy function of live fields; `metrics_source` says so on every candidate."""
    out: List[Dict[str, Any]] = []
    src = "derived deterministically from live stage/status/governance (documented policy weights, not estimates)"
    # W442 — under auth this list leaked EVERY tenant's project titles and living enterprises to
    # any caller (contradicting the W320 scoping one endpoint over); scope to what the requesting
    # user can access. No user (the cycle's internal path) keeps the federation view by design.
    def _visible(owner_id) -> bool:
        if user is None:
            return True
        try:
            from agentic_core.auth.core import auth_enabled, user_can_access
            return (not auth_enabled()) or user_can_access(user, owner_id)
        except Exception:
            return False
    try:
        from agentic_core.projects.api import _all_projects
        for p in _all_projects()[:cap]:
            if not _visible(getattr(p, "owner_id", None) or getattr(p, "owner", None)):
                continue
            stage = str(getattr(p, "stage", "") or "").lower()
            s = _STAGE_SCORE.get(stage, 0.5)
            domain = str(getattr(p, "domain", "") or getattr(p, "realm", "") or "").lower()
            has_outputs = bool(getattr(p, "outputs", None))
            out.append({
                "id": f"proj:{p.id}", "name": p.title, "domain": domain, "kind": "user_project",
                "outcome": s,
                "value": round(min(1.0, s + (0.10 if has_outputs else 0.0)), 2),
                "benefit": 0.70 if domain in _BENEFIT_DOMAINS else 0.55,
                "feasibility": round(min(1.0, s + (0.10 if has_outputs else 0.0)), 2),
                "strategic_fit": 0.55,
                "metrics_source": src,
            })
    except Exception:
        pass
    try:
        from agentic_core.economy.living_vsbs import _load as _living
        from agentic_core.api.vsb import _load_vsb
        for vid, rec in list(_living().items())[:cap]:
            if vid == exclude_vsb:
                continue
            ent = _load_vsb(vid) or {}
            if not _visible(ent.get("owner_id") or rec.get("owner")):
                continue
            governed = bool(ent.get("board")) and bool(ent.get("economy"))
            cycles = int(rec.get("operating_cycles", 0) or 0)
            domain = str(rec.get("domain", "") or "").lower()
            base = 0.70 if cycles > 0 else 0.60   # genuinely operating vs newly living
            out.append({
                "id": f"vsb:{vid}", "name": rec.get("name") or vid, "domain": domain,
                "kind": "living_vsb_offspring",
                "outcome": base,
                "value": round(min(1.0, base + min(0.15, cycles * 0.01)), 2),
                "benefit": 0.70 if domain in _BENEFIT_DOMAINS else 0.55,
                "feasibility": round(min(1.0, base + (0.10 if governed else 0.0)), 2),
                "strategic_fit": round(0.65 + (0.10 if governed else 0.0), 2),
                "metrics_source": src,
            })
    except Exception:
        pass
    return out


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
    # W442 — tolerant load: a corrupt file used to read as {} and the next save erased every
    # holding (the shared-store concurrency class' silent-wipe half).
    d = load_json_tolerant(_PORTFOLIO_STORE, {}) if _PORTFOLIO_STORE.exists() else {}
    return d if isinstance(d, dict) else {}


def _save_portfolio(d: Dict[str, Any]) -> None:
    from agentic_core.config import atomic_write_json
    atomic_write_json(_PORTFOLIO_STORE, d)


def record_return(vsb_id: str, holding_id: str, amount: float, memo: str = "") -> Dict[str, Any]:
    """§6 'returns recycle into the waterfall': record a virtual RETURN on a real holding. The amount
    is tracked on the holding + queued as a PENDING return that the next metabolic cycle consumes as
    intake revenue — so returns genuinely re-enter the waterfall. Virtual WST only."""
    # W442 — the amount was caller-asserted and UNBOUNDED: inf survived max/round and a
    # 10^12-WST "return" on a 5-WST holding was accepted — money credited that was never
    # invested and never earned, entering the next cycle's waterfall (and, before the gate fix,
    # distributing ungated). Finite, positive, and capped at 10× the holding's invested capital.
    if not math.isfinite(float(amount)):
        raise ValueError("Return amount must be a finite number.")
    amount = round(float(amount), 2)
    if amount <= 0:
        raise ValueError("Return amount must be positive.")
    with store_lock(_PORTFOLIO_STORE):
        d = _load_portfolio()
        pf = d.get(vsb_id)
        if not pf or holding_id not in (pf.get("holdings") or {}):
            raise KeyError(f"No holding '{holding_id}' in {vsb_id}'s venture portfolio.")
        h = pf["holdings"][holding_id]
        invested = round(float(h.get("invested_wst", 0.0) or 0.0), 2)
        cap = round(10 * invested, 2)
        # W442 refuter catch: the cap was PER-CALL, so N calls of ≤10× each accumulated without
        # limit (10 × 500 WST on a 50-WST holding = 100× invested minted). CUMULATIVE now.
        already_returned = round(float(h.get("returned_wst", 0.0) or 0.0), 2)
        if invested <= 0 or (already_returned + amount) > cap:
            raise ValueError(
                f"Return {amount} WST refused: holding '{holding_id}' has {invested} WST invested "
                f"and {already_returned} WST already returned — cumulative caller-asserted returns "
                f"above 10× invested capital (cap {cap} WST) are money from nothing. Nothing "
                "measures venture returns; the bound is the honesty floor.")
        at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        h["returned_wst"] = round(h.get("returned_wst", 0.0) + amount, 2)
        h["last_return_at"] = at
        pf["returns_total"] = round(pf.get("returns_total", 0.0) + amount, 2)
        pf["pending_returns_wst"] = round(pf.get("pending_returns_wst", 0.0) + amount, 2)
        pf["updated_at"] = at
        d[vsb_id] = pf
        _save_portfolio(d)
    return {"vsb_id": vsb_id, "holding_id": holding_id, "returned_wst": amount,
            "holding_returned_total_wst": h["returned_wst"],
            "pending_returns_wst": pf["pending_returns_wst"],
            "amount_source": "caller_asserted (cumulative returns bounded at 10× invested; nothing measures returns)",
            "recycles": "consumed as intake revenue by the next metabolic cycle (virtual WST)",
            "memo": memo}


def peek_pending_returns(vsb_id: str) -> float:
    """W442 — READ-ONLY view of the queued returns, for the §3 materiality estimate (the gate
    must see what the cycle will consume, or stuffing this queue bypasses Change Control)."""
    pf = _load_portfolio().get(vsb_id) or {}
    return round(pf.get("pending_returns_wst", 0.0), 2)


def consume_pending_returns(vsb_id: str) -> float:
    """Drain the queued venture returns for a VSB — called by the metabolic cycle at intake so the
    returns enter THIS cycle's waterfall. Returns the consumed amount (0.0 when none pending)."""
    with store_lock(_PORTFOLIO_STORE):
        d = _load_portfolio()
        pf = d.get(vsb_id)
        if not pf:
            return 0.0
        pending = round(pf.get("pending_returns_wst", 0.0), 2)
        if pending <= 0:
            return 0.0
        pf["pending_returns_wst"] = 0.0
        pf["recycled_total_wst"] = round(pf.get("recycled_total_wst", 0.0) + pending, 2)
        d[vsb_id] = pf
        _save_portfolio(d)
    return pending


def record_positions(vsb_id: str, allocation: Dict[str, Any]) -> None:
    """Track an allocation's positions in the VSB's venture portfolio (virtual; best-effort).

    W442 refuter catch: this was the THIRD writer on the portfolio store and the only unlocked
    one — every metabolic cycle calls it, so a heartbeat cycle racing a locked record_return
    still clobbered the just-written figures. Locking two of three writers serialises nothing."""
    positions = (allocation or {}).get("positions") or []
    if not positions:
        return
    with store_lock(_PORTFOLIO_STORE):
        _record_positions_locked(vsb_id, positions)


def _record_positions_locked(vsb_id: str, positions) -> None:
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
    # W442 refuter catch: pending_returns_wst lived in the store but never in this response, so
    # the panel's headline badge read 0 forever — the exact invisibility W442 claimed to fix.
    pf = _load_portfolio().get(vsb_id)
    if not pf:
        return {"vsb_id": vsb_id, "currency": "WST", "invested_total": 0.0,
                "positions_count": 0, "holdings": [], "pending_returns_wst": 0.0,
                "returns_total": 0.0, "recycled_total_wst": 0.0,
                "note": "No venture investments yet (virtual)."}
    holdings = sorted(pf["holdings"].values(), key=lambda h: h["invested_wst"], reverse=True)
    return {"vsb_id": vsb_id, "currency": "WST", "invested_total": pf["invested_total"],
            "positions_count": pf.get("positions_count", len(holdings)), "holdings": holdings,
            "pending_returns_wst": round(pf.get("pending_returns_wst", 0.0), 2),
            "returns_total": round(pf.get("returns_total", 0.0), 2),
            "recycled_total_wst": round(pf.get("recycled_total_wst", 0.0), 2),
            "updated_at": pf.get("updated_at"),
            "note": "Virtual/simulated venture portfolio — no real funds moved."}
