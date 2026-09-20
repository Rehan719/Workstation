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
# W475 (ledger v4 R1.0) — a haram term inside a NEGATING phrase ('avoids riba', 'no alcohol', 'free of interest')
# is not an offer of it. The screen cannot tell offered from avoided, so such a subject is REVIEW with the phrase
# quoted — never FAIL, and never 'Prohibited element' (a fact the screen cannot know).
# W475 (refutation) — the negator must GOVERN the term: bare 'free' / 'non' / 'zero' are adjectives ('a free casino
# app', 'non-stop gambling', 'zero-fee betting' are offers), a double negation is an offer ('does not avoid alcohol'),
# 'not only riba' is an offer, and punctuation ends the phrase ('no, we charge riba'). The suffix form is a negation
# ('riba-free', 'pork free menu'), and so is a hyphen-attached 'non-' ('non-alcoholic').
_NEGATOR_WORD = re.compile(r"^(?:avoid\w*|without|no|never|not|prohibit\w*|exclud\w*|forbid\w*|reject\w*|refus\w*)$",
                           re.IGNORECASE)
_NOT_WORDS = ("not", "never", "no", "cannot")
_SCOPE_BREAKERS = ("but", "except", "yet", "instead", "rather", "however", "only", "just", "merely")


def _negated(text: str, m) -> bool:
    """True when the haram term matched at `m` is governed by a negation — the subject says it AVOIDS it."""
    if re.match(r"[\s\-]free\b", text[m.end():m.end() + 8], re.IGNORECASE):
        return True                                           # 'riba-free financing', 'our pork free menu'
    if text[max(0, m.start() - 4):m.start()].lower() == "non-":
        return True                                           # 'non-alcoholic'
    tail = re.search(r"[A-Za-z'\s\-]*$", text[max(0, m.start() - 80):m.start()]).group(0)   # stops at punctuation
    if re.search(r"\bfree\s+(?:of|from)\s+(?:[A-Za-z'\-]+\s+){0,2}$", tail, re.IGNORECASE):
        return True                                           # 'free of alcohol', 'free from interest-bearing debt'
    toks = re.findall(r"([A-Za-z']+)(-?)", tail)                      # (word, '-' when hyphen-attached)
    words = [w for w, _ in toks]
    for i in range(len(words) - 1, max(-1, len(words) - 5), -1):   # the nearest negator, at most 3 words away
        if words[i].lower() in _SCOPE_BREAKERS:
            return False                                      # 'no alcohol but beer', 'not just coffee but alcohol'
        if _NEGATOR_WORD.match(words[i]) and toks[i][1] == "-":
            continue                                          # 'no-deposit casino', 'no-fee betting': an adjective
        if _NEGATOR_WORD.match(words[i]):
            prev = words[i - 1].lower() if i > 0 else ""
            nxt = words[i + 1].lower() if i + 1 < len(words) else ""
            if prev in _NOT_WORDS or prev.endswith("n't"):
                return False                                  # double negation: 'does not avoid alcohol'
            if words[i].lower() == "not" and nxt in ("only", "just", "merely"):
                return False                                  # 'not only riba'
            return True
    return False
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
     "engine": "haram-term screen (riba, alcohol, gambling, pork, …) + a three-term officer check; a "
               "matched term refuses the subject, and a subject that merely calls itself halal is "
               "reviewed, never passed — not a certification; a halal verdict comes from a "
               "certifying body, not from here"},
    {"id": "uk_legal", "name": "UK Legal (London)",
     "engine": "keyword screen (fraud, laundering, bribery, …) fails; employment-statute vocabulary "
               "(Equality Act 2010 / ERA 1996 / ACAS Code) flags for review; SHA3-512 audit over the subject — not legal advice"},
    {"id": "regulatory", "name": "Regulatory",
     "engine": "keyword screen for regulated-activity triggers (financial advice, medical, personal data, "
               "weapons, …) — flags for review; matching nothing is 'not assessed', never a clearance"},
    {"id": "ehs", "name": "Environment / Health / Safety",
     "engine": "keyword screen for hazard terms (toxic, emission, waste, …) — flags for review; matching "
               "nothing is 'not assessed', never a clearance"},
    {"id": "ethical", "name": "Ethical (beneficence, honesty, no-harm)",
     "engine": "four dimensions (human · environment · quality · value); three are word-list indicators "
               "that escalate for a human and never clear a subject, and quality is measured from the "
               "delivery's own QMS figures when they are supplied"},
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


# W483 — WHAT EACH COVERAGE IS ALLOWED TO SAY. The asymmetry is deliberate and is the whole rule:
# flagging is safe, clearing is the claim that has to be earned. A word list may refuse (a term
# naming a prohibited thing is present) and may escalate (a term whose meaning depends on its object
# is present), but it may never CLEAR — so only an 'engine' row can carry a pass, and only rows that
# genuinely read the subject colour the overall.
#   'engine'      an engine or a measured figure produced the verdict. May be pass, review or fail.
#   'vocabulary'  a term matched in the text. A fact about the text, not about the venture.
#   'screen'      the screen ran and matched nothing. Establishes nothing; status 'not_assessed'.
#   'none'        nothing here reads this area at all.
ASSESSING_COVERAGE = frozenset({"engine"})
COLOURING_COVERAGE = frozenset({"engine", "vocabulary"})


def assessed(verdict: Dict[str, Any]) -> bool:
    """True when this row could actually assess the subject — the only rows a caller may treat as a
    clearance. A pass with any other coverage is a pass OF A WORD LIST, and means nothing."""
    return (verdict.get("coverage") in ASSESSING_COVERAGE
            and verdict.get("status") not in ("not_assessed", "not_checked", "error"))


def _verdict(framework: str, status: str, reason: str, coverage: str = "vocabulary") -> Dict[str, str]:
    """See ASSESSING_COVERAGE above for what each coverage value is allowed to say."""
    return {"framework": framework, "status": status, "reason": reason, "coverage": coverage}


def _coverage_report(verdicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """The same coverage statement on every response, so no consumer has to derive it (and no two
    consumers derive it differently — the W475 second-writer lesson)."""
    gaps = [v["framework"] for v in verdicts if v.get("coverage") in ("none", "screen")
            or v.get("status") in ("not_assessed", "not_checked")]
    can = [v["framework"] for v in verdicts if assessed(v)]
    overall = _overall(verdicts)
    return {
        "coverage_gaps": sorted(set(gaps)),
        "assessed_by": sorted(set(can)),
        # W483 — `compliant` was `overall != 'fail'`, so a subject nothing had assessed was reported
        # compliant. Three states: False (a row refused it), True (every area was assessed and
        # passed), None (not established — the ordinary case while the screens are word lists).
        "compliant": (False if overall == "fail" else
                      True if (overall == "pass" and not gaps and can) else None),
        "basis": ("keyword and vocabulary screens plus the ethical dimensions. A screen can refuse and "
                  "can escalate; it cannot clear — so only a row with coverage 'engine' can carry a "
                  "pass, and `coverage_gaps` names every area nothing here assessed"
                  + (f" (assessed here: {', '.join(sorted(set(can)))})" if can else
                     " — NOTHING here assessed this subject, so the overall is 'review' and no part of "
                     "it may be reported as compliant")),
    }


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
    _hits = list(_HARAM.finditer(text))
    _offered = [m for m in _hits if not _negated(text, m)]
    _negated_only = bool(_hits) and not _offered
    if _offered:
        halal_status, halal_reason = "fail", (f"haram term present in the text: '{_offered[0].group(0)}' — a keyword "
                                              "screen, not a certification")
    elif _hits:
        _m = _hits[0]
        _phrase = " ".join(text[max(0, _m.start() - 24):min(len(text), _m.end() + 6)].split())
        halal_status, halal_reason = "review", (f"haram-vocabulary term '{_m.group(0)}' appears only in a negating "
                                                f"phrase ('{_phrase}'); the screen cannot tell offered from avoided — "
                                                "review, not a certification")
    elif _HALAL_VOCAB.search(text):
        # W483 (R1.1) — this was a PASS, and §10 then recorded 'compliant' and 'safe' as MEASURED
        # from it. The only thing established is that the subject calls itself halal. A subject's own
        # vocabulary about itself is not a finding, and certainly not a certification.
        halal_status, halal_reason = "review", (
            f"the subject describes itself with halal vocabulary ('{_HALAL_VOCAB.search(text).group(0)}') "
            "and no prohibited (haram) term matched — that is the subject's own claim, not a "
            "certification and not an assessment; a halal verdict comes from a certifying body")
    else:
        halal_status, halal_reason, halal_cov = "review", (f"{NO_COVERAGE} — the haram-term screen matched "
                                                           "nothing and no halal vocabulary is present; not a certification"), "none"
    try:
        _audit = _halal_engine().audit_transaction({"description": text})
        _viols = _audit.get("violations") or []
        if _viols and halal_status != "fail" and not _negated_only:
            halal_status, halal_reason = "fail", f"Engine violations: {', '.join(_viols)}."
        elif _viols:
            halal_reason = (f"{halal_reason} Engine also flags: {', '.join(_viols)}"
                            + (" (its keyword rule matched the same negated phrase)." if _negated_only else "."))
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

    # W483 (R1.1 / R3.3) — a keyword screen that matches NOTHING used to return 'pass', and the §10
    # bar then recorded 'compliant' and 'safe' as measured. The absence of a word is not a clearance:
    # these rows now say 'not_assessed' and carry no weight in the overall.
    reg_status, reg_reason, reg_cov = "not_assessed", (
        "keyword screen found no regulated-activity trigger — the absence of a trigger word is not a "
        "regulatory clearance; nothing here assessed this subject"), "screen"
    if _REGULATED.search(text):
        reg_status, reg_reason, reg_cov = "review", (
            f"Regulated activity — review required: '{_REGULATED.search(text).group(0)}'"), "vocabulary"
    verdicts.append(_verdict("regulatory", reg_status, reg_reason, reg_cov))

    ehs_status, ehs_reason, ehs_cov = "not_assessed", (
        "keyword screen found no hazard term — the absence of a hazard word is not an EHS clearance; "
        "nothing here assessed this subject"), "screen"
    if _EHS.search(text):
        ehs_status, ehs_reason, ehs_cov = "review", (
            f"Potential EHS concern: '{_EHS.search(text).group(0)}'"), "vocabulary"
    verdicts.append(_verdict("ehs", ehs_status, ehs_reason, ehs_cov))

    # W286 — the Ethical engine is REAL now (the old line hardcoded 'pass — no violations
    # detected' without checking anything — a standing fabrication). Four explainable
    # sub-verdicts; un-assessable dimensions say so honestly; `delivery_metrics` threads the
    # caller's PRECOMPUTED QMS figures in (never a call back into the quality gate).
    # W483 (R1.0 / R2.1) — the row reports the engine's OWN overall. It used to map 'not_assessed'
    # to 'pass', so a subject nothing had assessed came back green; and the engine's lexicon 'fail'
    # (a bare 'kill'/'abuse' match) failed the whole screen. Neither happens now: the engine
    # escalates instead of convicting, and the row's coverage is 'engine' only where a dimension
    # genuinely measured something — otherwise the row cannot colour the overall.
    # W483 (refutation) — the ethical row used to take coverage 'engine' whenever the engine reported
    # `assessed`, and `assessed` was true whenever the QMS supplied delivery figures. But the
    # dimension those figures measure is `quality` — section coverage and a stub regex over the
    # delivered text. Document coverage is not an ethical assessment, and on a clean delivery it was
    # carrying the ENTIRE §11 overall to 'pass' with human, environment and value all not_assessed.
    # The naming invariant: a quantity may carry the name of a thing only when it measured that
    # thing. So the ethical row is never 'engine'; the measured quality figure travels beside it.
    try:
        from agentic_core.compliance.ethical_engine import evaluate_ethics
        _eth = evaluate_ethics(text, delivery_metrics)
        _eth_cov = "vocabulary" if _eth["overall"] == "review" else "none"
        _eth_reason = f"{_eth['reason']} (engine-backed)"
        _row = _verdict("ethical", _eth["overall"], _eth_reason, _eth_cov)
        if _eth.get("escalate"):
            # A severe-harm or extractive term. The flag travels as DATA so a caller can act on it
            # without parsing prose — it is the whole point of downgrading the old 'fail'.
            # W483 (probe) — and the MATCHED TERM travels with it. FU-099 asked for exactly this:
            # the row's reason is a per-dimension summary, so without the term the person the
            # escalation is addressed to cannot see what triggered it.
            _row["escalate"] = list(_eth["escalate"])
            _terms = [t for d in _eth["dimensions"] if d.get("escalate")
                      for t in re.findall(r"'([^']+)'", d.get("reason") or "")]
            _row["escalated_terms"] = _terms
            _row["reason"] += (f" — escalated for a human to assess: {', '.join(_eth['escalate'])}"
                               + (f" (matched: {', '.join(_terms)})" if _terms else ""))
        verdicts.append(_row)
    except Exception:
        verdicts.append(_verdict("ethical", "review",
                                 "Ethical engine unavailable — review required (never a silent pass).", "none"))

    overall = _overall(verdicts)
    return {"overall": overall, "verdicts": verdicts, **_coverage_report(verdicts)}


def _overall(verdicts: List[Dict[str, str]]) -> str:
    """fail if any row fails; else review if any row that READ the subject is review, or an engine
    ERROR; else pass — but ONLY off rows that could assess (coverage 'engine').

    W483: the last clause used to read "pass — of the rows that could read the subject", and a row
    whose keyword screen matched nothing counted as having read it. Three such rows returning 'pass'
    made the overall 'pass', which §10 recorded as MEASURED and the Deliverables page rendered as an
    emerald COMPLIANCE: PASS. A row with coverage 'screen' or 'none', or status 'not_assessed' /
    'not_checked', now colours nothing; with no assessing row left, the overall is 'review'.
    """
    if any(v["status"] == "fail" for v in verdicts):
        return "fail"
    if any(v["status"] == "error" for v in verdicts):
        return "review"
    read = [v for v in verdicts if v.get("coverage", "vocabulary") in COLOURING_COVERAGE
            and v["status"] not in ("not_checked", "not_assessed")]
    if any(v["status"] == "review" for v in read):
        return "review"
    if not [v for v in read if assessed(v)]:
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
    # W483 (refutation) — THE ROUND'S OWN RULE, APPLIED TO THE ROW IT MISSED. This row carried
    # coverage 'engine', and gaas.v5's action gate is a nine-intent SUBSTRING test
    # (gaas/v5/policy_gate.py: `if prohibited in intent`) — a word list. Because 'engine' is the one
    # coverage that can clear, a benign action kind returned 'pass' and, being the only assessing
    # row, carried the whole screen to 'pass' with every other area in coverage_gaps. A match is
    # 'vocabulary' (a fact about the text); matching nothing is 'not_assessed'; only a raise is an
    # engine event. This row can now refuse, and can never clear.
    const_cov = "vocabulary"
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
                const_status, const_reason, const_cov = "not_assessed", (
                    f"gaas.v5 action gate: neither the '{req.kind}' kind nor the subject names one of "
                    "its nine prohibited intents. That is a substring test over a word list, so it "
                    "establishes nothing about this subject — it can refuse, it cannot clear"), "screen"
    except Exception as exc:
        const_status, const_reason, const_cov = "error", f"constitutional engine raised: {str(exc)[:120]} — recorded, never a pass", "none"
    verdicts.append(_verdict("constitutional", const_status, const_reason, const_cov))

    overall = _overall(verdicts)
    return {
        "subject": req.subject[:120],
        "jurisdiction": req.jurisdiction,
        "overall": overall,
        "verdicts": verdicts,
        **_coverage_report(verdicts),
        "note": ("Federated compliance screen: Sharia/Halal · UK Legal · Regulatory · EHS · Ethical · Constitutional — "
                 "keyword and vocabulary screens plus engines where one exists. A screen can refuse a subject and "
                 "can escalate one for a human; it cannot clear one, so an area nothing assessed is named in "
                 "coverage_gaps and is never reported as compliant."),
    }
