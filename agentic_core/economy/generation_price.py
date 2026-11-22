"""THE PRICE OF GENERATING AN ENTITY - one place holds it, and nothing charges it yet.

OWNER RULING 2026-10-13, from comparable prices read at their publishers' pages: ninety-nine pounds, once,
credited against the first profit share; waived for a charitable or non-distributing entity; and NOTHING IS
CHARGED until three things exist - a named reviewer's pass on what is generated, a solicitor's view on whether a
founder buying this is a consumer, and the real-money switch, which is the Owner's and last.

OWNER RULING 2026-11-22 (P5.16, the recommendation accepted): the credit is to carry forward against later fees
until it is used up, with no conversion while money is virtual; the unit it is held in goes to the accountant
(docs/business/FORMATION_WORKPACK.md, question 3 for an accountant). W1204 (FU-1881) says so where the credit is
read: CREDIT_RULE is the one statement of it, which this answer's credit_basis (the sentence the price panel
draws) and the cycle's fee (metabolism.py) each take.

This module states the price and why it is not charged. It posts nothing and calls no payment provider. Every
sentence a page shows about the price is built here, from these constants, so the figure is written once.
"""
from __future__ import annotations

from typing import Any, Dict, List

PRICE_GBP = 99
RULED_ON = "2026-10-13"
CREDITED_AGAINST_FIRST_PROFIT_SHARE = True
#  W1204 (FU-1881) - the flag above and the answer's field credited_against_first_profit_share keep their names,
#  which the price panel and three guards read: each says whether the price is credited at all. CREDIT_RULE says
#  how, as the Owner ruled on 2026-11-22: carried forward against the fees until it is used up.
CREDIT_RULED_ON = "2026-11-22"
CREDIT_RULE = ("credited against the platform's fees as they fall due, from the first, and carried forward until "
               "it is used up, with no conversion while money is virtual")
WAIVED_FOR_NON_DISTRIBUTING = True

#  the three things that must exist before anything is charged; each is read, never assumed
CONDITIONS = ("a named reviewer's pass on what is generated",
              "a solicitor's view on whether a founder buying this is a consumer",
              "the real-money switch, which is the Owner's")


def _real_money_on() -> bool:
    try:
        #  READ ONLY. The switch lives in one module and is the Owner's; nothing here sets it.
        from agentic_core.economy import owner_payments as _op
        return bool(getattr(_op, "REAL_MONEY_ENABLED", False))
    except Exception:                       # noqa: BLE001 - a switch that cannot be read is not on
        return False


def conditions_met() -> List[Dict[str, Any]]:
    """Each condition and whether it holds, with how that is known. The first two have no record anywhere yet,
    and are reported as not met BECAUSE no record exists - not because one was read and found wanting."""
    return [
        {"condition": CONDITIONS[0], "met": False,
         "basis": "no record of a reviewer's pass on a generated entity exists on this platform"},
        {"condition": CONDITIONS[1], "met": False,
         "basis": "no record of a solicitor's view exists on this platform; the Owner arranges it"},
        {"condition": CONDITIONS[2], "met": _real_money_on(),
         "basis": "read from the platform's own setting"},
    ]


def statement(non_distributing: bool = False) -> Dict[str, Any]:
    """What a person is told about the price of generating an entity, and what is charged now: nothing."""
    conds = conditions_met()
    chargeable = all(c["met"] for c in conds)
    waived = bool(non_distributing and WAIVED_FOR_NON_DISTRIBUTING)
    return {
        "price_gbp": 0 if waived else PRICE_GBP,
        "price_basis": (f"set by the Owner on {RULED_ON} from comparable prices read at their publishers' pages: "
                        f"{PRICE_GBP} pounds, once"),
        "credited_against_first_profit_share": CREDITED_AGAINST_FIRST_PROFIT_SHARE and not waived,
        "credit_basis": (f"the price, once charged, is {CREDIT_RULE} (ruled by the Owner on {CREDIT_RULED_ON}); the "
                         f"unit the credit is held in is a question for an accountant"),
        "waived": waived,
        "waived_basis": ("a charitable or non-distributing entity pays no price and no share; a stated gift, "
                         "decided on the fund's written criteria") if waived else None,
        "charged_now": False,
        "charged_now_gbp": 0,
        "chargeable": chargeable,
        "conditions": conds,
        "not_charged_basis": ("nothing is charged for generating an entity. It will not be until each of these "
                              "exists: " + "; ".join(CONDITIONS) + ". "
                              + f"{sum(1 for c in conds if c['met'])} of {len(conds)} exist today"),
        #  even with every condition met THIS MODULE charges nothing: it only states. The charge is other work.
        "this_answer_charges": False,
    }
