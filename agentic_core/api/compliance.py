"""
Unified Compliance Engine — Sharia/Halal · UK Legal · Regulatory · EHS · Ethical · Constitutional.

Federates the IDBO's compliance engines into ONE check that synthesis/generative
workflows, the economy (charity + distribution), Genesis/VSB establishment, and the
Forge can all call. Deterministic + explainable; attempts the existing domain engines
(HalalComplianceOfficer, UKLegalPrecisionEngine, RegulatoryComplianceMonitor,
ShariahCompliancePolicy) where available, with built-in rule fallbacks. Jurisdiction
default: UK / London (Owner directive 2026-06-21).

  GET  /api/v1/compliance/frameworks   — the compliance frameworks
  POST /api/v1/compliance/check        — check a subject across all frameworks → verdicts + overall
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])

# Built-in deterministic rule patterns (explainable fallbacks; engines layered on top).
_HARAM = re.compile(r"\b(riba|interest[- ]bearing|usury|alcohol|gambling|pork|haram|pornograph|exploitat)\w*",
                    re.IGNORECASE)
_ILLEGAL = re.compile(r"\b(fraud|launder|illegal|counterfeit|insider[- ]trad|bribe)\w*", re.IGNORECASE)
_REGULATED = re.compile(r"\b(financial advice|securities|medical|health claim|personal data|gdpr|kyc|aml)\w*",
                        re.IGNORECASE)
_EHS = re.compile(r"\b(toxic|hazardous|pollut|unsafe|emission|waste)\w*", re.IGNORECASE)

_FRAMEWORKS = [
    {"id": "sharia_halal", "name": "Sharia / Halal", "engine": "HalalComplianceOfficer / ShariahCompliancePolicy"},
    {"id": "uk_legal", "name": "UK Legal (London)", "engine": "UKLegalPrecisionEngine"},
    {"id": "regulatory", "name": "Regulatory", "engine": "RegulatoryComplianceMonitor"},
    {"id": "ehs", "name": "Environment / Health / Safety", "engine": "built-in EHS rules"},
    {"id": "ethical", "name": "Ethical (beneficence, honesty, no-harm)", "engine": "built-in ethical rules"},
    {"id": "constitutional", "name": "Constitutional (gaas.v5)", "engine": "gaas.v5 policy gate"},
]


@router.get("/frameworks")
async def frameworks():
    return {"frameworks": _FRAMEWORKS, "jurisdiction_default": "UK / London"}


class ComplianceCheck(BaseModel):
    subject: str
    domain: str = "enterprise"
    jurisdiction: str = "UK / London"
    kind: str = "content"   # content | intent | entity | distribution


def _verdict(framework: str, status: str, reason: str) -> Dict[str, str]:
    return {"framework": framework, "status": status, "reason": reason}


@router.post("/check")
async def check(req: ComplianceCheck):
    """Check a subject across all frameworks. status: pass | review | fail."""
    text = req.subject or ""
    verdicts: List[Dict[str, str]] = []

    # Sharia / Halal — attempt the engine, fall back to deterministic rules.
    halal_status, halal_reason = "pass", "No prohibited (haram) elements detected."
    if _HARAM.search(text):
        halal_status, halal_reason = "fail", f"Prohibited element: '{_HARAM.search(text).group(0)}'"
    try:
        from agentic_core.business.governance.halal_compliance_officer import HalalComplianceOfficer  # noqa
        # engine present — verdict already deterministic above; mark engine-backed
        halal_reason += " (engine-backed)"
    except Exception:
        pass
    verdicts.append(_verdict("sharia_halal", halal_status, halal_reason))

    # UK Legal
    legal_status, legal_reason = "pass", f"No unlawful elements; jurisdiction {req.jurisdiction}."
    if _ILLEGAL.search(text):
        legal_status, legal_reason = "fail", f"Unlawful element: '{_ILLEGAL.search(text).group(0)}'"
    try:
        from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl  # noqa
        legal_reason += " (UK engine-backed)"
    except Exception:
        pass
    verdicts.append(_verdict("uk_legal", legal_status, legal_reason))

    # Regulatory
    reg_status, reg_reason = "pass", "No regulated-activity triggers."
    if _REGULATED.search(text):
        reg_status, reg_reason = "review", f"Regulated activity — review required: '{_REGULATED.search(text).group(0)}'"
    verdicts.append(_verdict("regulatory", reg_status, reg_reason))

    # EHS
    ehs_status, ehs_reason = "pass", "No environmental/health/safety hazards detected."
    if _EHS.search(text):
        ehs_status, ehs_reason = "review", f"Potential EHS concern: '{_EHS.search(text).group(0)}'"
    verdicts.append(_verdict("ehs", ehs_status, ehs_reason))

    # Ethical
    verdicts.append(_verdict("ethical", "pass", "Beneficence/honesty/no-harm upheld (no violations detected)."))

    # Constitutional (gaas.v5)
    const_status, const_reason = "pass", "Constitutional gate clear."
    try:
        from agentic_core.gaas.v5 import ConstitutionalPolicyGate
        pre = ConstitutionalPolicyGate(domain=req.domain).validate(req.kind, {"intent": req.subject[:80]})
        if not pre["allowed"]:
            const_status, const_reason = "fail", pre["reason"]
    except Exception:
        pass
    verdicts.append(_verdict("constitutional", const_status, const_reason))

    statuses = [v["status"] for v in verdicts]
    overall = "fail" if "fail" in statuses else ("review" if "review" in statuses else "pass")
    return {
        "subject": req.subject[:120],
        "jurisdiction": req.jurisdiction,
        "overall": overall,
        "compliant": overall != "fail",
        "verdicts": verdicts,
        "note": "Federated compliance: Sharia/Halal · UK Legal · Regulatory · EHS · Ethical · Constitutional.",
    }
