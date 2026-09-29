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

from agentic_core.config import StoreUnavailable, data_path, read_json_strict, store_lock

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
    """Scores and allocates the user-project investment budget from POLICY CONSTANTS, not measurements.

    W489 (sweep S2.12, C3) — this said "scores, ranks … for maximal outcome/value/benefit", and the
    surfaces called the result a ranking. The five inputs are eligibility constants keyed on a
    handful of booleans — whether a board exists, whether a cycle has run, which domain bucket the
    entity is in — so every governed, once-cycled VSB in the same bucket scores IDENTICALLY (0.6925),
    and the only continuous term moves the total by 0.0025 per operating cycle, capped at 0.0375.
    A figure that cannot distinguish two entities is not a ranking of them. The scoring is unchanged
    (it is a reasonable eligibility policy); what changes is that it is named for what it is, ties are
    reported rather than hidden by a stable sort, and the method string no longer says "×" for what
    is a weighted SUM."""

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
        """Candidates by POLICY SCORE, descending. Each row says how many others share its score, so a
        reader can see that an order between equals is arbitrary (a stable sort keeps harvest order)."""
        scored = [{**v, "score": self.score(v)} for v in self.candidates]
        scored.sort(key=lambda x: x["score"], reverse=True)
        counts: Dict[float, int] = {}
        for s in scored:
            counts[s["score"]] = counts.get(s["score"], 0) + 1
        for s in scored:
            s["score_basis"] = "policy constants (stage/operating/governance/domain) — not a measurement"
            s["tied_with"] = counts[s["score"]] - 1
        return scored[:top]

    def allocate(self, budget: float, top: int = 5) -> Dict[str, Any]:
        """Distribute ``budget`` (WST, virtual) across the top ventures, weighted by score."""
        winners = self.ranked(top)
        weight_sum = sum(w["score"] for w in winners) or 1.0
        positions = []
        for w in winners:
            amount = round(max(0.0, budget) * (w["score"] / weight_sum), 2)
            positions.append({"id": w["id"], "name": w.get("name", w["id"]), "domain": w.get("domain", ""),
                              "score": w["score"], "amount_wst": amount,
                              # W506 (P2.7(7)) - carried on EVERY position, because a position travels
                              # away from this response and the statement has to travel with it
                              "funding_state": "recorded_unfunded",
                              "funding_basis": _UNFUNDED_BASIS})
        # W506 (P2.7(7)) - the RESIDUAL. Each share was rounded to 2dp independently, so the positions did
        # not sum to the budget: measured 100.0 -> 100.01 and 33.33 -> 33.32, a cent created and a cent
        # destroyed. Harmless while nothing is funded and real money the moment anything is, so it is fixed
        # now rather than left for whoever takes the funding arm. The residual lands on the largest position.
        _budget = round(max(0.0, budget), 2)
        _sum = round(sum(p["amount_wst"] for p in positions), 2)
        _residual = round(_budget - _sum, 2)
        if positions and _residual:
            _biggest = max(positions, key=lambda p: p["amount_wst"])
            _biggest["amount_wst"] = round(_biggest["amount_wst"] + _residual, 2)
            _biggest["absorbed_rounding_wst"] = _residual
        assert round(sum(p["amount_wst"] for p in positions), 2) == _budget or not positions, (
            "the positions do not sum to the budget after the residual correction")
        return {
            "budget_wst": round(max(0.0, budget), 2),
            # W489 — it is a weighted SUM of policy constants, and it was described as a product of
            # measurements. Both halves of that were wrong.
            "method": ("policy score: weighted sum of eligibility constants "
                       "(outcome .30 + value .25 + benefit .20 + feasibility .15 + strategic_fit .10)"),
            "method_basis": ("the five inputs are constants keyed on stage, whether a cycle has run, "
                             "whether the entity is governed, and its domain bucket — nothing is measured; "
                             "entities in the same bucket tie, and tied positions split the budget evenly"),
            "using_demo_candidates": self.using_demo,
            "positions": positions,
            # W506 (P2.7(7)) - "no real funds moved" was true and was not the thing a reader needed to
            # know: no VIRTUAL funds reach the investee either. The board pack rendered these positions with
            # named investees as if capital had been deployed.
            "disclaimer": "Virtual/simulated investment \u2014 no real funds moved.",
            "funding_state": "recorded_unfunded",
            "funding_basis": _UNFUNDED_BASIS,
        }


# ── Portfolio persistence (§6: tracked as portfolio positions; returns recycle into the waterfall) ─────────

# W506 (P2.7(7)) \u2014 ONE statement, so the API, the portfolio and the board pack cannot each word it
# differently (the W475 second-writer lesson applied to a disclosure).
_UNFUNDED_BASIS = (
    "recorded, unfunded — the investee is NOT credited. The position is the investor's own record of an allocation; no intake is queued for the named entity and its waterfall never receives this amount. Virtual WST throughout.")


def _load_portfolio() -> Dict[str, Any]:
    """W472 (register FU-052) — whole or StoreUnavailable. W442's tolerant load still read a corrupt file as {} when
    no prefix parsed, and record_positions then kept only the new position (holdings and pending returns lost)."""
    return read_json_strict(_PORTFOLIO_STORE, dict, expect=dict)


def _recycle_fields() -> dict:
    """W502 (FU-163) — what happens to a returned amount, from whether a cycle is coming."""
    try:
        from agentic_core.economy.living_vsbs import intake_note
        n = intake_note("this return")
        return {"recycles": n["note"], "autonomous_cycles": n["autonomous_cycles"]}
    except Exception:
        return {"recycles": ("this return is queued as intake revenue; whether a next metabolic cycle is "
                             "scheduled could not be determined here"),
                "autonomous_cycles": None}


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
            # W502 (FU-163) — computed, not promised: autonomous cycles are OFF by default
            **_recycle_fields(),
            "memo": memo}


def peek_pending_returns(vsb_id: str) -> float:
    """W442 — READ-ONLY view of the queued returns, for the §3 materiality estimate (the gate
    must see what the cycle will consume, or stuffing this queue bypasses Change Control)."""
    try:
        pf = _load_portfolio().get(vsb_id) or {}
    except StoreUnavailable:
        return 0.0            # a READ-ONLY estimate; the drain itself (a writer) refuses on the same file
    return round(pf.get("pending_returns_wst", 0.0), 2)


def consume_pending_returns(vsb_id: str, max_amount: Optional[float] = None) -> float:
    """Drain the queued venture returns for a VSB — called by the metabolic cycle at intake so the
    returns enter THIS cycle's waterfall. Returns the consumed amount (0.0 when none pending).
    W463 — `max_amount` caps the drain at what the materiality gate measured; the remainder stays
    pending for the next cycle."""
    with store_lock(_PORTFOLIO_STORE):
        d = _load_portfolio()
        pf = d.get(vsb_id)
        if not pf:
            return 0.0
        pending = round(pf.get("pending_returns_wst", 0.0), 2)
        take = pending if max_amount is None else round(min(pending, max(0.0, float(max_amount))), 2)
        if take <= 0:
            return 0.0
        pf["pending_returns_wst"] = round(pending - take, 2)
        pf["recycled_total_wst"] = round(pf.get("recycled_total_wst", 0.0) + take, 2)
        d[vsb_id] = pf
        _save_portfolio(d)
    return take


def return_pending_returns(vsb_id: str, amount: float) -> None:
    """W467 (register FU-044) — give back venture returns a cycle drained (consume_pending_returns) when that cycle then
    wrote nothing to the ledger: they reached no books, so they wait for the next cycle."""
    amount = round(float(amount), 2)
    if amount <= 0:
        return
    with store_lock(_PORTFOLIO_STORE):
        d = _load_portfolio()
        pf = d.get(vsb_id)
        if not isinstance(pf, dict):
            raise KeyError(f"no venture portfolio for {vsb_id} to give {amount} WST of drained returns back to")
        pf["pending_returns_wst"] = round(pf.get("pending_returns_wst", 0.0) + amount, 2)
        pf["recycled_total_wst"] = round(max(0.0, pf.get("recycled_total_wst", 0.0) - amount), 2)
        d[vsb_id] = pf
        _save_portfolio(d)



# ── §12 THE REINVESTMENT SHARE (OWNER RULING 2026-09-29, FU-300) ───────────────────────────────────────────
#
# What fraction of the user_projects allocation actually reaches the investee. The Owner ruled this a SETTING
# whose default is the proportion already described: `user_projects` is a §4 waterfall stage with a
# per-template share (0.05-0.15), already adjustable per VSB, so THAT share is the Owner's proportion and
# this is only the question of whether it arrives. Default 1.0 - all of it does, which is what §6/§12 state.
#
# At 0.0 the behaviour is exactly what it was before this ruling: positions recorded, no investee credited,
# and the "recorded, unfunded" label W506 put on every figure is then the truthful one.
_FUNDING_SHARE_STORE_NAME = "economy_venture_funding_share.json"
_DEFAULT_FUNDING_SHARE = 1.0


def _share_store():
    from agentic_core.config import data_path
    return data_path(_FUNDING_SHARE_STORE_NAME)


def venture_funding_share(vsb_id: str) -> tuple:
    """(share, source) for this investor. Never raises: an unreadable store falls back to the DEFAULT and
    says so, because refusing to fund is a decision and this function is not where it should be taken."""
    from agentic_core.config import StoreUnavailable, read_json_strict
    try:
        d = read_json_strict(_share_store(), dict, expect=dict) if _share_store().exists() else {}
    except (StoreUnavailable, Exception):                       # noqa: B014 - any read problem, same answer
        return _DEFAULT_FUNDING_SHARE, ("the share store could not be read, so the default "
                                        f"{_DEFAULT_FUNDING_SHARE} applies")
    raw = d.get(vsb_id)
    if raw is None:
        return _DEFAULT_FUNDING_SHARE, f"the default ({_DEFAULT_FUNDING_SHARE}) - no override is set"
    try:
        v = max(0.0, min(1.0, float(raw)))
    except (TypeError, ValueError):
        return _DEFAULT_FUNDING_SHARE, f"the stored override {raw!r} is not a number, so the default applies"
    return v, "an Owner override for this entity"


def set_venture_funding_share(vsb_id: str, share: float) -> dict:
    """Persist the Owner's share for one entity, bounded to 0.0-1.0, under the store's own lock."""
    from agentic_core.config import StoreUnavailable, atomic_write_json, read_json_strict, store_lock
    v = max(0.0, min(1.0, float(share)))
    with store_lock(_share_store()):
        try:
            d = read_json_strict(_share_store(), dict, expect=dict) if _share_store().exists() else {}
        except StoreUnavailable as e:
            raise                                               # refuse rather than replace an unreadable store
        d[vsb_id] = v
        _share_store().parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(_share_store(), d)
    return {"vsb_id": vsb_id, "venture_funding_share": v,
            "basis": ("the fraction of this entity's user_projects allocation that reaches the investees. "
                      "The SIZE of that allocation is the user_projects waterfall stage, which is set "
                      "separately; this is only whether it arrives. 0.0 records positions and funds nobody.")}


def _is_live_vsb(candidate_id: str) -> bool:
    """Whether this position names a LIVE entity. A position can name a DEMO candidate, which is not an
    entity and must never be credited - crediting one would put WST into a namespace nothing tends."""
    try:
        from agentic_core.economy.living_vsbs import list_living
        rows = (list_living() or {}).get("living_vsbs") or []
        ids = {str(r.get("vsb_id")) for r in rows if isinstance(r, dict)}
    except Exception:
        return False                                            # cannot establish liveness -> do not credit
    cid = str(candidate_id or "")
    return cid in ids or cid.replace("vsb:", "") in ids

def record_positions(vsb_id: str, allocation: Dict[str, Any], round_id: str | None = None) -> None:
    """Track an allocation's positions in the VSB's venture portfolio (virtual; best-effort).

    W442 refuter catch: this was the THIRD writer on the portfolio store and the only unlocked
    one — every metabolic cycle calls it, so a heartbeat cycle racing a locked record_return
    still clobbered the just-written figures. Locking two of three writers serialises nothing."""
    positions = (allocation or {}).get("positions") or []
    if not positions:
        return
    with store_lock(_PORTFOLIO_STORE):
        _record_positions_locked(vsb_id, positions)

    # §12 (OWNER RULING 2026-09-29, FU-300) - THE INVESTEE IS CREDITED. Until this ruling the investor's
    # holdings were the only thing written and the named entity received nothing, so a position was a record
    # of an allocation that arrived nowhere. Credit-only: the investor's debit already happened as the
    # user_projects distribution, and a second one would be the W504 defect.
    #
    # OUTSIDE the portfolio lock on purpose - the credit takes the pending-transfers store's lock, and
    # holding both would fix a portfolio->pending order another path could deadlock against.
    share, share_source = venture_funding_share(vsb_id)
    # W507 (FU-300) - THE REF IDENTIFIES THE ALLOCATION, NOT THE CLOCK. A wall-clock stamp was wrong in
    # both directions, and driving it showed both: two allocations in the SAME second produced the same
    # ref and the second was skipped as a duplicate (measured - a 0.25 share credited 0.0), while a
    # retry a second later produced a new ref and would have credited twice. A caller that wants a
    # retry to be idempotent passes its own `round_id`; without one each call is a distinct investment,
    # which is what an unidentified allocation actually is.
    round_at = str(round_id) if round_id else uuid.uuid4().hex[:12]
    funded, unfunded = [], []
    for p in positions:
        amount = round(float(p.get("amount_wst") or 0.0) * share, 2)
        pid = str(p.get("id") or "")
        if share <= 0:
            unfunded.append({"id": pid, "why": f"the funding share is {share} ({share_source})"})
            continue
        if amount <= 0:
            unfunded.append({"id": pid, "why": "the share leaves nothing to credit at this position's size"})
            continue
        if not _is_live_vsb(pid):
            unfunded.append({"id": pid, "why": "this position does not name a live entity (a demo candidate "
                                               "is not an entity, and crediting one would put WST where "
                                               "nothing tends it)"})
            continue
        try:
            from agentic_core.economy.transfers import credit_venture_intake
            res = credit_venture_intake(pid.replace("vsb:", ""), amount,
                                        ref=f"venture:{vsb_id}:{pid}:{round_at}",
                                        memo=f"\u00a712 reinvestment from {vsb_id}")
            (funded if res.get("credited") else unfunded).append(
                {"id": pid, "amount_wst": amount, **({} if res.get("credited") else {"why": res.get("reason")})})
        except Exception as exc:                                # noqa: BLE001 - recorded, never swallowed
            unfunded.append({"id": pid, "why": f"the credit failed: {exc.__class__.__name__}: {exc}"})
    _record_funding_outcome(vsb_id, share, share_source, funded, unfunded)


def _record_funding_outcome(vsb_id: str, share: float, share_source: str, funded, unfunded) -> None:
    """Persist WHAT REACHED the investees beside what was allocated. FU-300.

    Two different facts, and before this ruling only the first existed: `invested_wst` is what the investor
    set aside, `funded_wst` is what arrived. They differ whenever the share is below 1.0 or a position names
    something that is not a live entity, and a reader who cannot see both cannot tell those cases apart.
    """
    from agentic_core.config import StoreUnavailable
    try:
        with store_lock(_PORTFOLIO_STORE):
            d = _load_portfolio()
            pf = d.get(vsb_id)
            if not isinstance(pf, dict):
                return
            pf["funding_share"] = share
            pf["funding_share_source"] = share_source
            pf["funded_total_wst"] = round(pf.get("funded_total_wst", 0.0)
                                           + sum(f.get("amount_wst", 0.0) for f in funded), 2)
            for f in funded:
                h = pf.get("holdings", {}).get(f["id"])
                if isinstance(h, dict):
                    h["funded_wst"] = round(h.get("funded_wst", 0.0) + f.get("amount_wst", 0.0), 2)
            pf["last_funding"] = {"funded": funded, "unfunded": unfunded, "share": share,
                                  "share_source": share_source}
            d[vsb_id] = pf
            _save_portfolio(d)
    except (StoreUnavailable, TimeoutError):
        # the credits ALREADY LANDED in the investees' queues; failing to record the summary must not
        # pretend they did not. The investee-side queue is the authority either way.
        import logging
        logging.getLogger("economy.ventures").warning(
            "venture funding summary not recorded for %s (the credits themselves landed in the investees' "
            "queues, which are the authority either way)", vsb_id)


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


def _funding_disclosure(pf: Dict[str, Any]) -> Dict[str, Any]:
    """The funding_state/basis pair, COMPUTED from what the last round actually funded. W507 (FU-300).

    W506 hard-coded "recorded_unfunded" because nothing could ever be funded. Now that the Owner has ruled
    the loop closed, asserting it would be false for a funded position - and deleting it would be false at
    share 0.0, which is still a supported setting. So it is derived.
    """
    share = pf.get("funding_share")
    funded_total = round(pf.get("funded_total_wst", 0.0) or 0.0, 2)
    last = pf.get("last_funding") or {}
    unfunded = last.get("unfunded") or []
    if funded_total <= 0:
        return {"funding_state": "recorded_unfunded",
                "funding_basis": (_UNFUNDED_BASIS if share in (None, 0, 0.0) else
                                  "recorded, unfunded - the share is above zero and nothing was credited; "
                                  "see last_funding.unfunded for the reason against each position")}
    if unfunded:
        return {"funding_state": "partly_funded",
                "funding_basis": (f"{funded_total} WST reached live investees; {len(unfunded)} position(s) "
                                  f"were not funded (see last_funding.unfunded). A position that names a demo "
                                  f"candidate is never credited, because it is not an entity.")}
    return {"funding_state": "funded",
            "funding_basis": (f"{funded_total} WST was queued as the named investees' intake at a funding "
                              f"share of {share}. It enters each investee's §4 waterfall when that entity's "
                              f"next metabolic cycle runs, which is not automatic unless it is being tended.")}


def portfolio(vsb_id: str) -> Dict[str, Any]:
    # W442 refuter catch: pending_returns_wst lived in the store but never in this response, so
    # the panel's headline badge read 0 forever — the exact invisibility W442 claimed to fix.
    try:
        pf = _load_portfolio().get(vsb_id)
    except StoreUnavailable as e:
        # W472 — never zero holdings for a portfolio that could not be read
        # W506 (pre-flight) - the funding state holds whether or not the store can be read: it is a fact
        # about what a position IS, not about this response. Omitting it here made a reader that always
        # reads it fall through to "not stated" on the one response that shows no figures anyway.
        return {"vsb_id": vsb_id, "currency": "WST", "unavailable": str(e), "holdings": [],
                "funding_state": "recorded_unfunded", "funding_basis": _UNFUNDED_BASIS,
                # W507 - None, not 0.0: this store could not be READ, so what was funded is UNKNOWN. A zero
                # here would be a figure, and the one thing this branch knows is that it has no figures.
                "funding_share": None, "funding_share_source": None,
                "funded_total_wst": None, "last_funding": None,
                "note": "the venture portfolio could not be read whole — no figures are shown and nothing is written "
                        "to it until it can be read (virtual)"}
    if not pf:
        return {"vsb_id": vsb_id, "currency": "WST", "invested_total": 0.0,
                "positions_count": 0, "holdings": [], "pending_returns_wst": 0.0,
                "returns_total": 0.0, "recycled_total_wst": 0.0,
                "funding_state": "recorded_unfunded", "funding_basis": _UNFUNDED_BASIS,
                # W507 (FU-300, pre-flight) - the funding figures are on EVERY branch. A caller that reads
                # funded_total_wst on a portfolio with no holdings got undefined, which reads as "unknown"
                # rather than "nothing has been funded because nothing has been allocated".
                "funding_share": None, "funding_share_source": None,
                "funded_total_wst": 0.0, "last_funding": None,
                "note": "No venture investments yet (virtual)."}
    holdings = sorted(pf["holdings"].values(), key=lambda h: h["invested_wst"], reverse=True)
    return {"vsb_id": vsb_id, "currency": "WST", "invested_total": pf["invested_total"],
            "positions_count": pf.get("positions_count", len(holdings)), "holdings": holdings,
            # W507 (FU-300) - WHAT REACHED the investees, beside what was allocated. Two different facts:
            # `invested_total` is what the investor set aside, `funded_total_wst` is what arrived. They
            # differ whenever the share is below 1.0 or a position names something that is not a live
            # entity, and a reader who sees only the first cannot tell those cases apart. Written by
            # _record_funding_outcome; returned here, because a field the writer stores and the reader
            # drops is a fact rendered nowhere.
            "funding_share": pf.get("funding_share"),
            "funding_share_source": pf.get("funding_share_source"),
            "funded_total_wst": round(pf.get("funded_total_wst", 0.0), 2),
            "last_funding": pf.get("last_funding"),
            # W506 (P2.7(7)) x W507 (FU-300) - the label is now COMPUTED from what actually happened
            # rather than asserted: at share 0.0 nothing is funded and "recorded, unfunded" is the true
            # statement; above it, positions that reached a live entity ARE funded and must not claim
            # otherwise. The per-position detail is in `last_funding`.
            **_funding_disclosure(pf),
            "pending_returns_wst": round(pf.get("pending_returns_wst", 0.0), 2),
            "returns_total": round(pf.get("returns_total", 0.0), 2),
            "recycled_total_wst": round(pf.get("recycled_total_wst", 0.0), 2),
            "updated_at": pf.get("updated_at"),
            "note": "Virtual/simulated venture portfolio — no real funds moved."}
