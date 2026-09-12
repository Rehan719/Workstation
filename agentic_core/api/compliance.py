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

import json
import re
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])

# Built-in deterministic rule patterns (explainable fallbacks; engines layered on top).
# §11 (W342) — vocabulary hardened after an adversarial sweep: a 'fine wine subscription club'
# survived 8 continuous re-screens because wine/beer/liquor/casino/lottery/betting were absent.
# Word-boundary-safe; deliberately NOT matching bare 'spirit' (spiritual) or 'bet' (better) —
# 'betting/bets on' and 'spirits' (plural, the drink) are the safe forms.
_HARAM = re.compile(
    r"\b(riba|interest[- ]bearing|usury|alcohol|wine|beer|liquor|whisk(?:y|ey)|vodka|spirits\b|"
    r"brewer|distiller|gambling|gambl\w*|casino|lottery|lotteries|betting|wager|"
    r"pork|lard|bacon|haram|pornograph|exploitat)\w*",
    re.IGNORECASE)
_ILLEGAL = re.compile(
    r"\b(fraud|launder|illegal|counterfeit|insider[- ]trad|bribe|narcotic|trafficking|smuggl)\w*",
    re.IGNORECASE)
_REGULATED = re.compile(
    r"\b(financial advice|securities|medical|health claim|personal data|gdpr|kyc|aml|"
    r"pharmaceutical|firearm|weapon)\w*",
    re.IGNORECASE)
_EHS = re.compile(r"\b(toxic|hazardous|pollut|unsafe|emission|waste|carcinogen|flammable)\w*",
                  re.IGNORECASE)

# W285 — the registry names ONLY what genuinely runs: the Halal and UK-Legal ENGINES are actually
# invoked (below), regulatory/EHS are built-in deterministic rules (there is no
# 'RegulatoryComplianceMonitor' class in this repo — the old entry named a phantom).
# W455 (P1.7, ledger 1.7 / R1.6) — each entry names WHAT THE CHECK ACTUALLY DOES. The old labels
# ("UKLegalPrecisionEngine (invoked, statute vocabularies + SHA3-512 audit)") presented eight
# employment-law terms and a three-word substring loop as engine-grade coverage.
_FRAMEWORKS = [
    {"id": "sharia_halal", "name": "Sharia / Halal",
     "engine": "haram-term screen (riba, alcohol, gambling, pork, …) + a three-term officer check; "
               "a subject with halal vocabulary and no haram term passes the screen — not a certification"},
    {"id": "uk_legal", "name": "UK Legal (London)",
     "engine": "keyword screen (fraud, laundering, bribery, …) fails; employment-statute vocabulary "
               "(Equality Act 2010 / ERA 1996 / ACAS Code) flags for review; SHA3-512 audit over the subject — not legal advice"},
    {"id": "regulatory", "name": "Regulatory",
     "engine": "keyword screen for regulated-activity triggers (financial advice, medical, personal data, "
               "weapons, …) — flags for review; not a regulatory assessment"},
    {"id": "ehs", "name": "Environment / Health / Safety",
     "engine": "keyword screen for hazard terms (toxic, emission, waste, …) — flags for review; not an EHS assessment"},
    {"id": "ethical", "name": "Ethical (beneficence, honesty, no-harm)",
     "engine": "four explainable dimensions (human · environment · quality · value) over the text and the "
               "delivery's own QMS figures; a dimension it cannot assess says so"},
    {"id": "constitutional", "name": "Constitutional (gaas.v5)",
     "engine": "an ACTION gate over nine prohibited agent intents (delete_all, wire_funds, …) plus an output "
               "screen for unsafe shell / SQL / private-key patterns; it does not read content for policy — "
               "content is 'not checked' here"},
]

# W455 — positive vocabularies: coverage is claimed only where a vocabulary was actually present.
_HALAL_VOCAB = re.compile(r"\b(halal|islamic|sharia|shariah|zakat|waqf|muslim|sunnah|tayyib|qard)\w*", re.IGNORECASE)
NO_COVERAGE = "no engine covers this area"

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


def _verdict(framework: str, status: str, reason: str, coverage: str = "vocabulary") -> Dict[str, str]:
    """coverage: 'vocabulary' (a keyword screen matched or a positive vocabulary was present) ·
    'engine' (an engine produced the verdict) · 'none' (nothing here reads this subject — review)."""
    return {"framework": framework, "status": status, "reason": reason, "coverage": coverage}


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
    # W455 — a subject outside the vocabulary is REVIEW, never a green pass: the screen matched
    # nothing, and nothing here can say the subject is halal. Positive halal vocabulary + no haram
    # term is a pass OF THE SCREEN, labelled as such.
    halal_cov = "vocabulary"
    if _HARAM.search(text):
        halal_status, halal_reason = "fail", f"Prohibited element: '{_HARAM.search(text).group(0)}'"
    elif _HALAL_VOCAB.search(text):
        halal_status, halal_reason = "pass", ("halal vocabulary present and no prohibited (haram) term — "
                                              "a keyword screen, not a certification")
    else:
        halal_status, halal_reason, halal_cov = "review", (f"{NO_COVERAGE} — the haram-term screen matched "
                                                           "nothing and no halal vocabulary is present; not a certification"), "none"
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
    verdicts.append(_verdict("sharia_halal", halal_status, halal_reason, halal_cov))

    # W285 — the UK-Legal ENGINE is genuinely INVOKED: potential flags are derived from the
    # engine's OWN statute vocabularies found in the text, validated across its statutes, with
    # the engine's SHA3-512 audit hash carried in the reason. Same worst-of merge + honest labels.
    legal_cov = "vocabulary"
    _flags: List[str] = []
    if _ILLEGAL.search(text):
        legal_status, legal_reason = "fail", f"Unlawful element: '{_ILLEGAL.search(text).group(0)}'"
    else:
        legal_status, legal_reason = "review", (f"{NO_COVERAGE} — keyword screen + employment-statute "
                                                f"vocabulary matched nothing (jurisdiction {jurisdiction}); not legal advice")
        legal_cov = "none"
    # W455 (R1.6) — the audit hash COVERS THE SUBJECT, computed before the engine runs so an engine
    # raise still leaves a hash on the row (refuter F9). The engine's own hash was over
    # {intent_type, violations, layer} — identical for a halal bakery and a laundering scheme.
    import hashlib as _hl
    _low = text.lower()
    try:
        _eng = _legal_engine()
        _flags = sorted({f for terms in _eng.statutes.values() for f in terms
                         if f.replace("_", " ") in _low or f in _low})
    except Exception:
        _eng, _flags = None, []
    _audit = _hl.sha3_512(json.dumps({"subject": text, "flags": _flags, "status": legal_status},
                                     sort_keys=True).encode("utf-8")).hexdigest()
    try:
        if _eng is None:
            raise RuntimeError("legal engine unavailable")
        _res = _eng.validate(
            {"type": "delivery_screen", "jurisdiction": "UK", "potential_flags": _flags},
            {"required_statutes": list(_eng.statutes.keys()), "jurisdiction": "UK",
             "layer": "compliance_screen"})
        # refuter F2 — the engine records a STATUTORY_BREACH for ANY statute term present (mentioning
        # a grievance procedure is not a breach), so statute vocabulary is REVIEW with the statute
        # named — never a fail on vocabulary alone, never a pass either (the old 'pass' branch was dead)
        if _res.violations and legal_status != "fail":
            legal_status, legal_cov = "review", "vocabulary"
            legal_reason = (f"employment-statute vocabulary present — {'; '.join(_res.violations)} — "
                            "review required; a vocabulary screen, not legal advice")
        elif _res.violations:
            legal_reason = f"{legal_reason} Engine also flags: {'; '.join(_res.violations)}."
        legal_reason += f" (UK engine-backed · audit {_audit[:16]}… over the subject)"
    except Exception:
        legal_reason += f" (built-in rules · audit {_audit[:16]}… over the subject)"
    verdicts.append(_verdict("uk_legal", legal_status, legal_reason, legal_cov))

    reg_status, reg_reason = "pass", "keyword screen found no regulated-activity trigger — not a regulatory assessment"
    if _REGULATED.search(text):
        reg_status, reg_reason = "review", f"Regulated activity — review required: '{_REGULATED.search(text).group(0)}'"
    verdicts.append(_verdict("regulatory", reg_status, reg_reason, "screen"))

    ehs_status, ehs_reason = "pass", "keyword screen found no hazard term — not an EHS assessment"
    if _EHS.search(text):
        ehs_status, ehs_reason = "review", f"Potential EHS concern: '{_EHS.search(text).group(0)}'"
    verdicts.append(_verdict("ehs", ehs_status, ehs_reason, "screen"))

    # W286 — the Ethical engine is REAL now (the old line hardcoded 'pass — no violations
    # detected' without checking anything — a standing fabrication). Four explainable
    # sub-verdicts; un-assessable dimensions say so honestly; `delivery_metrics` threads the
    # caller's PRECOMPUTED QMS figures in (never a call back into the quality gate).
    try:
        from agentic_core.compliance.ethical_engine import evaluate_ethics
        _eth = evaluate_ethics(text, delivery_metrics)
        _eth_status = "pass" if _eth["overall"] in ("pass", "not_assessed") else _eth["overall"]
        verdicts.append(_verdict("ethical", _eth_status, f"{_eth['reason']} (engine-backed)", "engine"))
    except Exception:
        verdicts.append(_verdict("ethical", "review",
                                 "Ethical engine unavailable — review required (never a silent pass).", "none"))

    overall = _overall(verdicts)
    return {"overall": overall, "compliant": overall != "fail", "verdicts": verdicts,
            "coverage_gaps": [v["framework"] for v in verdicts if v.get("coverage") == "none"],
            "basis": ("keyword and vocabulary screens plus the ethical dimensions; the overall is the verdict "
                      "of the rows that could read the subject and `coverage_gaps` names the rows that could "
                      "not ('review — no engine covers this area'); a pass is a pass of the screen, not a certification")}


def _overall(verdicts: List[Dict[str, str]]) -> str:
    """fail if any row fails; else review if any row that READ the subject is review, or an engine
    ERROR; else pass — of the rows that could read the subject (the gaps are listed beside it).
    A row with coverage 'none' or status 'not_checked' cannot colour the overall; if NO row could
    read the subject the overall is review."""
    if any(v["status"] == "fail" for v in verdicts):
        return "fail"
    if any(v["status"] == "error" for v in verdicts):
        return "review"
    read = [v for v in verdicts if v.get("coverage", "vocabulary") != "none" and v["status"] != "not_checked"]
    if not read:
        return "review"
    if any(v["status"] == "review" for v in read):
        return "review"
    return "pass"


@router.post("/check")
async def check(req: ComplianceCheck):
    """Check a subject across all frameworks. status: pass | review | fail."""
    screen = screen_compliance(req.subject or "", req.jurisdiction)
    verdicts = list(screen["verdicts"])

    # W455 (P1.7, ledger 1.7 / R1.1) — the constitutional row SAYS WHAT IT CAN CHECK. gaas.v5's
    # validate() is an ACTION gate (nine prohibited intents matched against the action type; it
    # consumed `kind` first, so the subject was dead input and every content check read green
    # "Constitutional gate clear" — for a laundering scheme too). Now: content → the output screen
    # (the only gaas.v5 method that reads text) runs, and the row is 'not_checked' unless it finds
    # an unsafe pattern; an action kind → the action gate on that kind; an engine raise → 'error',
    # never a pass.
    const_cov = "engine"
    try:
        from agentic_core.gaas.v5 import ConstitutionalPolicyGate
        _gate = ConstitutionalPolicyGate(domain=req.domain)
        _out = _gate.validate_output(req.subject)
        if not _out.get("compliant", True):
            const_status, const_reason = "fail", (f"gaas.v5 output screen: unsafe pattern(s) "
                                                  f"{', '.join(map(str, _out.get('violations') or []))} in the subject")
        elif req.kind == "content":
            const_status, const_reason, const_cov = "not_checked", (
                "not applicable to content — gaas.v5 gates agent actions (nine prohibited intents); "
                "the output screen found no unsafe shell / SQL / private-key pattern in this subject"), "none"
        else:
            # refuter F1 — the gate matches its nine prohibited intents against the STRING it is
            # given; given the kind alone the subject was dead input, so 'wire_funds to X' as an
            # intent passed. It is given the kind AND the subject text now.
            pre = _gate.validate(f"{req.kind}: {req.subject[:200]}", {})
            if not pre["allowed"]:
                const_status, const_reason = "fail", pre["reason"]
            else:
                const_status, const_reason = "pass", (f"gaas.v5 action gate: neither the '{req.kind}' kind nor the subject "
                                                      "names a prohibited intent (nine-intent substring gate — not a policy reading)")
    except Exception as exc:
        const_status, const_reason, const_cov = "error", f"constitutional engine raised: {str(exc)[:120]} — recorded, never a pass", "none"
    verdicts.append(_verdict("constitutional", const_status, const_reason, const_cov))

    overall = _overall(verdicts)
    return {
        "subject": req.subject[:120],
        "jurisdiction": req.jurisdiction,
        "overall": overall,
        "compliant": overall != "fail",
        "verdicts": verdicts,
        "coverage_gaps": [v["framework"] for v in verdicts if v.get("coverage") == "none"],
        "basis": screen.get("basis"),
        "note": ("Federated compliance screen: Sharia/Halal · UK Legal · Regulatory · EHS · Ethical · Constitutional — "
                 "keyword and vocabulary screens plus engines where one exists; 'review — no engine covers this "
                 "area' means nothing here read the subject; a pass is a pass of the screen, not a certification."),
    }
