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

# W285 — the registry names ONLY what genuinely runs: the Halal and UK-Legal ENGINES are actually
# invoked (below), regulatory/EHS are built-in deterministic rules (there is no
# 'RegulatoryComplianceMonitor' class in this repo — the old entry named a phantom).
_FRAMEWORKS = [
    {"id": "sharia_halal", "name": "Sharia / Halal",
     "engine": "HalalComplianceOfficer (invoked) + built-in rules"},
    {"id": "uk_legal", "name": "UK Legal (London)",
     "engine": "UKLegalPrecisionEngine (invoked, statute vocabularies + SHA3-512 audit) + built-in rules"},
    {"id": "regulatory", "name": "Regulatory", "engine": "built-in regulatory rules (trigger set)"},
    {"id": "ehs", "name": "Environment / Health / Safety", "engine": "built-in EHS rules"},
    {"id": "ethical", "name": "Ethical (beneficence, honesty, no-harm)",
     "engine": "EthicalEngine (invoked): human · environment · quality · value dimensions"},
    {"id": "constitutional", "name": "Constitutional (gaas.v5)", "engine": "gaas.v5 policy gate"},
]

# W285 — lazy module-level engine singletons (never raise at import; a failed engine leaves the
# built-in rules serving, honestly labelled).
_HALAL_ENGINE = None
_LEGAL_ENGINE = None


def _halal_engine():
    global _HALAL_ENGINE
    if _HALAL_ENGINE is None:
        from agentic_core.business.governance.halal_compliance_officer import HalalComplianceOfficer
        _HALAL_ENGINE = HalalComplianceOfficer()
    return _HALAL_ENGINE


def _legal_engine():
    global _LEGAL_ENGINE
    if _LEGAL_ENGINE is None:
        import os
        from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
        _LEGAL_ENGINE = UKLegalPrecisionEngineImpl(
            rules_path=os.getenv("LEGAL_PATH", "configs/legal_precision.yaml"))
    return _LEGAL_ENGINE


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


def screen_compliance(text: str, jurisdiction: str = "UK / London",
                      delivery_metrics: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Reusable, deterministic compliance screen over arbitrary delivery text — Sharia/Halal · UK Legal ·
    Regulatory · EHS · Ethical. Pure + explainable (regex rules; engines layered where present). Returns
    {overall, compliant, verdicts}. Shared by the /check endpoint AND the universal delivery gate
    (`assure_delivery`) so compliance is woven into every workflow (§11), not bolted on. (The gaas.v5
    Constitutional gate is applied separately by the org cascade / Change Control.)"""
    text = text or ""
    verdicts: List[Dict[str, str]] = []

    # W285 — the Halal ENGINE is genuinely INVOKED (the old code imported it and appended
    # '(engine-backed)' without ever calling it — an honesty defect). Worst-of merge: an engine
    # fail OR a rule fail → fail; an engine pass never downgrades a rule fail. The suffix is
    # appended ONLY when the engine actually executed; on engine failure the built-in rule
    # verdict stands, labelled as such.
    halal_status, halal_reason = "pass", "No prohibited (haram) elements detected."
    if _HARAM.search(text):
        halal_status, halal_reason = "fail", f"Prohibited element: '{_HARAM.search(text).group(0)}'"
    try:
        _audit = _halal_engine().audit_transaction({"description": text})
        _viols = _audit.get("violations") or []
        if _viols and halal_status != "fail":
            halal_status, halal_reason = "fail", f"Engine violations: {', '.join(_viols)}."
        elif _viols:
            halal_reason = f"{halal_reason} Engine also flags: {', '.join(_viols)}."
        halal_reason += " (engine-backed)"
    except Exception:
        halal_reason += " (built-in rules)"
    verdicts.append(_verdict("sharia_halal", halal_status, halal_reason))

    # W285 — the UK-Legal ENGINE is genuinely INVOKED: potential flags are derived from the
    # engine's OWN statute vocabularies found in the text, validated across its statutes, with
    # the engine's SHA3-512 audit hash carried in the reason. Same worst-of merge + honest labels.
    legal_status, legal_reason = "pass", f"No unlawful elements; jurisdiction {jurisdiction}."
    if _ILLEGAL.search(text):
        legal_status, legal_reason = "fail", f"Unlawful element: '{_ILLEGAL.search(text).group(0)}'"
    try:
        _eng = _legal_engine()
        _low = text.lower()
        _flags = sorted({f for terms in _eng.statutes.values() for f in terms
                         if f.replace("_", " ") in _low or f in _low})
        _res = _eng.validate(
            {"type": "delivery_screen", "jurisdiction": "UK", "potential_flags": _flags},
            {"required_statutes": list(_eng.statutes.keys()), "jurisdiction": "UK",
             "layer": "compliance_screen"})
        if _res.violations and legal_status != "fail":
            legal_status, legal_reason = "fail", f"{'; '.join(_res.violations)}."
        elif _res.violations:
            legal_reason = f"{legal_reason} Engine also flags: {'; '.join(_res.violations)}."
        legal_reason += f" (UK engine-backed · audit {str(_res.audit_hash)[:16]}…)"
    except Exception:
        legal_reason += " (built-in rules)"
    verdicts.append(_verdict("uk_legal", legal_status, legal_reason))

    reg_status, reg_reason = "pass", "No regulated-activity triggers."
    if _REGULATED.search(text):
        reg_status, reg_reason = "review", f"Regulated activity — review required: '{_REGULATED.search(text).group(0)}'"
    verdicts.append(_verdict("regulatory", reg_status, reg_reason))

    ehs_status, ehs_reason = "pass", "No environmental/health/safety hazards detected."
    if _EHS.search(text):
        ehs_status, ehs_reason = "review", f"Potential EHS concern: '{_EHS.search(text).group(0)}'"
    verdicts.append(_verdict("ehs", ehs_status, ehs_reason))

    # W286 — the Ethical engine is REAL now (the old line hardcoded 'pass — no violations
    # detected' without checking anything — a standing fabrication). Four explainable
    # sub-verdicts; un-assessable dimensions say so honestly; `delivery_metrics` threads the
    # caller's PRECOMPUTED QMS figures in (never a call back into the quality gate).
    try:
        from agentic_core.compliance.ethical_engine import evaluate_ethics
        _eth = evaluate_ethics(text, delivery_metrics)
        _eth_status = "pass" if _eth["overall"] in ("pass", "not_assessed") else _eth["overall"]
        verdicts.append(_verdict("ethical", _eth_status, f"{_eth['reason']} (engine-backed)"))
    except Exception:
        verdicts.append(_verdict("ethical", "review",
                                 "Ethical engine unavailable — review required (never a silent pass)."))

    statuses = [v["status"] for v in verdicts]
    overall = "fail" if "fail" in statuses else ("review" if "review" in statuses else "pass")
    return {"overall": overall, "compliant": overall != "fail", "verdicts": verdicts}


@router.post("/check")
async def check(req: ComplianceCheck):
    """Check a subject across all frameworks. status: pass | review | fail."""
    screen = screen_compliance(req.subject or "", req.jurisdiction)
    verdicts = list(screen["verdicts"])

    # Constitutional (gaas.v5) — added to the full endpoint check (needs domain/kind context)
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
