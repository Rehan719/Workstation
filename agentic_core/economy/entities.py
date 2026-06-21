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
    "waqf_ltd_hybrid": {
        "name": "Waqf-Ltd Hybrid (recommended)", "distributes_profit": True, "capital_preserved": True,
        "description": "Commercial earnings (Ltd) under endowment governance (Waqf) with a charitable waterfall — the recommended default for the Owner's vision.",
        "waterfall": dict(_DEFAULT),
    },
}

DEFAULT_ENTITY = "waqf_ltd_hybrid"


def get_template(entity_type: str) -> Dict[str, Any]:
    return ENTITY_TEMPLATES.get(entity_type, ENTITY_TEMPLATES[DEFAULT_ENTITY])
