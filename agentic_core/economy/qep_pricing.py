"""P3.11 clause (2) — A.8's three finance limits, each refusing a breaching figure by name.

DESTINATION: agentic_core/economy/qep_pricing.py (new file, LF). Prepared W599.

A.8 (Owner-authored, read verbatim from docs/WORKSTATION_IDBO_WHOLE_VISION.md:1322) states three limits:
  · **free at the point of use** for individuals
  · institutional partnerships at **cost + 5%**
  · a **surplus cap of ≤ 5%** with reinvestment

MEASURED BEFORE WRITING, and it decided the shape:
  · `api/economy.py:1024` declares a service contract's `price_wst: float = Field(default=100.0, gt=0)` —
    STRICTLY POSITIVE. So "free at the point of use" cannot even be EXPRESSED through the existing contract
    mechanism: a price of 0 is rejected by the field before any rule runs. These limits therefore need their
    own check rather than a flag on contracts.
  · nothing in `agentic_core/api/` computes a surplus at all.

THE SHAPE MIRRORS `metabolism.validate_waterfall`, which is this platform's existing idiom for a bounded
economic form: a (value, violations) pair where violations are SENTENCES, not exceptions. A caller gets every
breach at once rather than the first, and each sentence NAMES THE RULE that refused it — because a refusal
that does not say which limit it hit cannot be corrected by the person who hit it.

VIRTUAL WST THROUGHOUT. No real-money rail is touched by anything here; that is the Owner's standing
constraint and not this module's choice.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

#  A.8's figures. They are the Owner's and a round may not adjust them.
INSTITUTIONAL_MARGIN = 0.05        # "institutional partnerships at cost + 5%"
SURPLUS_CAP = 0.05                 # "a surplus cap of <= 5% with reinvestment"
INDIVIDUAL_PRICE = 0.0             # "free at the point of use" for individuals

A8_BASIS = ("these three limits are vision A.8's own figures (Owner-authored): free at the point of use for "
            "individuals, institutional partnerships at cost + 5%, and a surplus cap of 5% with "
            "reinvestment. A round may not adjust them. Virtual WST throughout - no real-money rail.")


def check_individual_price(price_wst: float) -> Tuple[bool, List[str]]:
    """Free at the point of use. ANY non-zero price to an individual is refused.

    Not "low" and not "subsidised": A.8 says free, so the only permitted figure is 0. A tolerance here would
    be a threshold over a number the Owner stated exactly, which is the gate that cannot refuse.
    """
    v: List[str] = []
    try:
        p = float(price_wst)
    except (TypeError, ValueError):
        return False, [f"the individual price {price_wst!r} is not a number, so it was NOT treated as free"]
    if p != INDIVIDUAL_PRICE:
        v.append(f"REFUSED by the free-at-point-of-use rule (A.8): an individual may be charged "
                 f"{INDIVIDUAL_PRICE} WST and this is {p}. QEP is free at the point of use for "
                 f"individuals; there is no reduced rate, because A.8 states free rather than affordable.")
    return not v, v


def check_institutional_price(price_wst: float, cost_wst: float) -> Tuple[bool, List[str]]:
    """Institutions at cost + 5%. A higher margin is refused, NAMING the computed ceiling.

    The ceiling is computed from the cost the caller supplies, so the refusal can be checked by hand: a
    refusal that states only "too high" cannot be corrected by the person who hit it.
    """
    v: List[str] = []
    try:
        p, c = float(price_wst), float(cost_wst)
    except (TypeError, ValueError):
        return False, [f"the institutional price {price_wst!r} or cost {cost_wst!r} is not a number, so no "
                       f"ceiling could be computed and the price was NOT accepted"]
    if c < 0:
        return False, [f"the stated cost {c} is negative, so no ceiling could be computed"]
    ceiling = round(c * (1.0 + INSTITUTIONAL_MARGIN), 2)
    if p > ceiling:
        v.append(f"REFUSED by the cost-plus-5% rule (A.8): the stated cost is {c} WST, so the ceiling is "
                 f"{ceiling} WST ({c} x 1.05) and this price is {p}. The margin asked for is "
                 f"{round((p / c - 1.0) * 100, 2) if c else 'undefined'}%.")
    return not v, v


def check_surplus(surplus_wst: float, revenue_wst: float) -> Tuple[bool, List[str]]:
    """Surplus <= 5% of revenue, reinvested. A higher surplus is refused, naming both figures.

    THREE STATES, because zero revenue is not a breach: a period with no revenue has no ratio to cap, and
    reporting it as a breach would refuse an entity for having earned nothing.
    """
    v: List[str] = []
    try:
        s, r = float(surplus_wst), float(revenue_wst)
    except (TypeError, ValueError):
        return False, [f"the surplus {surplus_wst!r} or revenue {revenue_wst!r} is not a number, so no ratio "
                       f"could be computed and the surplus was NOT accepted"]
    if r <= 0:
        #  not a breach and not a pass: there is nothing to take a ratio of
        return True, []
    cap = round(r * SURPLUS_CAP, 2)
    if s > cap:
        v.append(f"REFUSED by the surplus cap (A.8): revenue is {r} WST so the cap is {cap} WST (5%) and the "
                 f"surplus is {s}, which is {round(s / r * 100, 2)}% of revenue. A.8 requires the surplus to "
                 f"be capped at 5% WITH REINVESTMENT - the excess is reinvested, not retained.")
    return not v, v


def check_all(individual_price: Any = INDIVIDUAL_PRICE, institutional_price: Any = None,
              institutional_cost: Any = None, surplus: Any = None,
              revenue: Any = None) -> Dict[str, Any]:
    """Every A.8 limit at once, so a caller gets all breaches rather than the first.

    A limit whose inputs were not supplied is reported as NOT ASSESSED, never as passed: "nobody told me the
    institutional cost" and "the institutional price is within its ceiling" are different facts, and
    collapsing them would let an unchecked figure read as a cleared one.
    """
    results: Dict[str, Any] = {}
    violations: List[str] = []
    not_assessed: List[str] = []

    ok, v = check_individual_price(individual_price)
    results["individual"] = {"ok": ok, "violations": v}
    violations += v

    if institutional_price is None or institutional_cost is None:
        results["institutional"] = {"ok": None, "violations": [],
                                    "why": "no institutional price and cost were supplied, so the cost-plus "
                                           "ceiling was NOT computed - this is not a pass"}
        not_assessed.append("institutional")
    else:
        ok, v = check_institutional_price(institutional_price, institutional_cost)
        results["institutional"] = {"ok": ok, "violations": v}
        violations += v

    if surplus is None or revenue is None:
        results["surplus"] = {"ok": None, "violations": [],
                              "why": "no surplus and revenue were supplied, so the cap was NOT computed - "
                                     "this is not a pass"}
        not_assessed.append("surplus")
    else:
        ok, v = check_surplus(surplus, revenue)
        results["surplus"] = {"ok": ok, "violations": v}
        violations += v

    return {
        "permitted": not violations,
        "violations": violations,
        "not_assessed": not_assessed,
        "limits": results,
        "figures": {"individual_price": INDIVIDUAL_PRICE, "institutional_margin": INSTITUTIONAL_MARGIN,
                    "surplus_cap": SURPLUS_CAP},
        "basis": (A8_BASIS
                  + (f" {len(not_assessed)} limit(s) were NOT ASSESSED because their inputs were not "
                     f"supplied ({', '.join(not_assessed)}); an unassessed limit is not a cleared one."
                     if not_assessed else "")),
    }
