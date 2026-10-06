"""
Legal entity-type templates for a VSB's economic form.

Each template configures the profit-distribution waterfall defaults and bounds,
capital-preservation rules, and governance posture. Users select the form when
they generate their VSB. The waterfall fractions are of *distributable* profit
(after Stage-0 legal/operating reserves) and always sum to 1.0.
Waterfall stages: owner | self_investment | capital_fund | user_projects | charity
"""
from __future__ import annotations

from typing import Any, Dict

# Default waterfall (the Owner-approved proposal): Owner 20 / Self 30 / Cap 20 / Users 15 / Charity 15
_DEFAULT = {"owner": 0.20, "self_investment": 0.30, "capital_fund": 0.20,
            "user_projects": 0.15, "charity": 0.15}


def _norm(w: Dict[str, float]) -> Dict[str, float]:
    total = sum(w.values()) or 1.0
    return {k: round(v / total, 4) for k, v in w.items()}


ENTITY_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "sole": {
        "name": "Sole Holder", "distributes_profit": True, "capital_preserved": False,
        "description": "Individual-owned; owner-centric distribution.",
        "waterfall": _norm({"owner": 0.55, "self_investment": 0.25, "capital_fund": 0.10,
                            "user_projects": 0.05, "charity": 0.05}),
    },
    "ltd": {
        "name": "Private Limited (Ltd)", "distributes_profit": True, "capital_preserved": False,
        "description": "Default commercial company, limited liability.",
        "waterfall": dict(_DEFAULT),
    },
    "plc": {
        "name": "Public Limited (PLC)", "distributes_profit": True, "capital_preserved": False,
        "description": "Public company; shareholder distributions; built for scale.",
        "waterfall": _norm({"owner": 0.30, "self_investment": 0.30, "capital_fund": 0.25,
                            "user_projects": 0.08, "charity": 0.07}),
    },
    "trust": {
        "name": "Trust", "distributes_profit": True, "capital_preserved": True,
        "description": "Assets held by trustee for beneficiaries under a deed.",
        "waterfall": _norm({"owner": 0.20, "self_investment": 0.20, "capital_fund": 0.30,
                            "user_projects": 0.15, "charity": 0.15}),
    },
    "waqf": {
        "name": "Waqf (Endowment)", "distributes_profit": True, "capital_preserved": True,
        "description": "Perpetual endowment; capital preserved; usufruct to causes.",
        "waterfall": _norm({"owner": 0.05, "self_investment": 0.20, "capital_fund": 0.30,
                            "user_projects": 0.15, "charity": 0.30}),
    },
    "multinational": {
        "name": "Multinational Group", "distributes_profit": True, "capital_preserved": False,
        "description": "Cross-jurisdiction group; multi-entity distribution.",
        "waterfall": _norm({"owner": 0.25, "self_investment": 0.35, "capital_fund": 0.20,
                            "user_projects": 0.10, "charity": 0.10}),
    },
    "nonprofit": {
        "name": "Non-profit", "distributes_profit": False, "capital_preserved": True,
        "description": "Mission-first; surplus reinvested or donated, no owner profit.",
        "waterfall": _norm({"owner": 0.00, "self_investment": 0.45, "capital_fund": 0.20,
                            "user_projects": 0.15, "charity": 0.20}),
    },
    "charity": {
        "name": "Charity", "distributes_profit": False, "capital_preserved": True,
        "description": "Registered charitable purpose; maximal charitable allocation.",
        "waterfall": _norm({"owner": 0.00, "self_investment": 0.15, "capital_fund": 0.10,
                            "user_projects": 0.10, "charity": 0.65}),
    },
    #  P3.11 clause (1) — THE QEP INSTANCE A.8 DESCRIBES, which is why it cannot be the generic template:
    #  the default waqf_ltd_hybrid pays the owner 0.20, and A.8 says "100% donation and waqf-backed", so an
    #  owner share contradicts it outright. The clause's own words: "a guard asserts its proportions differ
    #  from the default, because inheriting the template is the defect".
    #  OWNER 0.00 AND SELF_INVESTMENT 0.05 COME FROM A.8 AND ARE NOT CHOICES — no owner profit, and a
    #  surplus cap of <=5% with reinvestment. The other three are a DEFENSIBLE DEFAULT INSIDE those
    #  constraints and are labelled as such below, because A.8 gives constraints rather than five numbers
    #  and presenting my split as the Owner's model would be the fabrication this plan exists to prevent.
    "qep_waqf_trust": {
        "name": "QEP Waqf Endowment + Not-for-Profit Trust (A.8)",
        "distributes_profit": False,     # 100% donation and waqf-backed — the existing owner>0 check defends this
        "capital_preserved": True,       # the Waqf Endowment Board secures PERPETUAL funding
        "description": ("The Quran Education Platform's own economic model (vision A.8): a Waqf Endowment "
                        "Board stewarding gifts alongside a Not-for-Profit Trust running the platform. FROM "
                        "A.8 AND NOT ADJUSTABLE BY A ROUND: no owner profit (100% donation and waqf-backed) "
                        "and a surplus cap of 5% with reinvestment. THE REMAINING THREE PROPORTIONS ARE A "
                        "DEFAULT INSIDE THOSE CONSTRAINTS, not the Owner's stated figures: the endowment "
                        "takes the largest retained share because A.8 charges it with perpetual funding, "
                        "learners are the beneficiaries because the platform is free at the point of use, "
                        "and the charity share is Zakat-eligible. Virtual WST only."),
        "waterfall": _norm({"owner": 0.00, "self_investment": 0.05, "capital_fund": 0.35,
                            "user_projects": 0.40, "charity": 0.20}),
    },
    "waqf_ltd_hybrid": {
        "name": "Waqf-Ltd Hybrid (recommended)", "distributes_profit": True, "capital_preserved": True,
        "description": "Commercial earnings (Ltd) under endowment governance (Waqf) with a charitable waterfall — the recommended default for the Owner's vision.",
        "waterfall": dict(_DEFAULT),
    },
}

DEFAULT_ENTITY = "waqf_ltd_hybrid"


def get_template(entity_type: str) -> Dict[str, Any]:
    return ENTITY_TEMPLATES.get(entity_type, ENTITY_TEMPLATES[DEFAULT_ENTITY])
