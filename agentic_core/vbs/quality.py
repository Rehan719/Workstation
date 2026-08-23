"""
Living-QMS Quality Assurance — the single, reusable capability that subjects EVERY operational delivery
to the OWNED Quality Management System (continual operational delivery within the living QMS), holds it to
the §10 Solution-Quality Bar, and records it within the §8 biomimetic living-organism.

Honest by construction: the QMS gate runs on REAL metrics computed from the actual delivery content
(coverage = required sections present; stub = placeholder / empty content); the QMS is stateful, so
defects accumulate and a non-conformance rate is tracked across deliveries (this is what makes it
*continual*); the organism snapshot is the live immune health + circadian phase (no fabricated numbers).

Used by the org cascade (`/api/v1/swarm/cascade`), the living deliverables pipeline
(`/api/v1/deliverables/*`), and any other operational-delivery surface — so the whole platform delivers
within one living QMS, to one quality bar, inside one organism.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

# §10 — the Solution-Quality Bar every operational delivery is held to.
SOLUTION_QUALITY_BAR: List[str] = [
    "specifically designed", "modelled", "simulated", "optimised", "categorised", "ranked",
    "best-in-class", "innovative", "effective", "safe", "efficient", "commercially viable",
    "compliant", "verified", "tested", "validated",
]

# §8 — the biomimetic living-organism the delivery happens within.
BIOMIMETIC_LAYERS: List[str] = ["Genome", "Nervous", "Immune", "Cardiovascular", "Respiratory",
                                "Musculoskeletal", "Endocrine"]

_STUB_RE = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|placeholder|coming soon|as an ai)\b", re.I)
_MIN_SUBSTANTIVE = 200  # chars — below this a "delivery" is treated as an empty / stub shell.


def _measure_bar(coverage: float, stub: bool, qms_passed: Optional[bool], min_coverage: float,
                 compliance: Dict[str, Any], evidence: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """§10 (W307) — the Solution-Quality Bar measured PER-CRITERION, honestly. Each of the 16
    criteria is either genuinely measured here (a real proxy with a named basis), attested by the
    CALLER's own real process evidence (e.g. Genesis stage-5 modelling/simulation — the basis is
    recorded), or explicitly NOT MEASURED. The sealed record no longer implies a 16-criterion
    measurement when only two proxies ran."""
    ev = evidence or {}
    verdicts = {v.get("framework"): v.get("status") for v in (compliance.get("verdicts") or [])}
    crit: Dict[str, Dict[str, Any]] = {}

    def measured(name: str, met: bool, basis: str) -> None:
        crit[name] = {"met": bool(met), "basis": basis, "measured": True}

    def unmeasured(name: str) -> None:
        crit[name] = {"met": None, "basis": "not measured by this gate", "measured": False}

    measured("specifically designed", coverage >= min_coverage and not stub,
             f"delivery coverage {coverage} against the declared structure (min {min_coverage}), "
             f"stub_found={stub}")
    if qms_passed is not None:
        measured("verified", bool(qms_passed), "QMS gate on real coverage/stub metrics")
    else:
        unmeasured("verified")
    if verdicts:
        measured("compliant", compliance.get("overall") != "fail", f"§11 screen verdicts: {verdicts}")
        _safety = [f for f in ("ethical", "ehs", "sharia_halal") if f in verdicts]
        if _safety:
            measured("safe", all(verdicts[f] != "fail" for f in _safety),
                     f"§11 safety-bearing frameworks: {({f: verdicts[f] for f in _safety})}")
        else:
            unmeasured("safe")
    else:
        unmeasured("compliant")
        unmeasured("safe")
    for name in SOLUTION_QUALITY_BAR:
        if name in crit:
            continue
        if ev.get(name):   # the caller attests a criterion its own REAL process earned — basis kept
            crit[name] = {"met": True, "basis": f"caller evidence: {str(ev[name])[:200]}",
                          "measured": True}
        else:
            unmeasured(name)
    _m = [c for c in crit.values() if c["measured"]]
    return {"criteria": crit, "measured": len(_m), "met": sum(1 for c in _m if c["met"]),
            "not_measured": len(crit) - len(_m)}


def _delivery_coverage(content: str, required_sections: Optional[List[str]]) -> float:
    """Fraction of the required sections that actually appear in the delivered content (case-insensitive).
    With no declared structure, coverage is binary on whether there is substantive content."""
    text = (content or "").lower()
    if not required_sections:
        return 1.0 if len(text.strip()) >= _MIN_SUBSTANTIVE else 0.0
    present = sum(1 for s in required_sections if str(s).lower() in text)
    return round(present / len(required_sections), 3)


async def assure_delivery(content: str, required_sections: Optional[List[str]] = None,
                          label: str = "delivery",
                          evidence: Optional[Dict[str, Any]] = None,
                          owner_id: Optional[str] = None) -> Dict[str, Any]:
    """Subject an operational delivery to the living QMS + §10 bar + §8 organism.

    Returns ``{"quality": {...}, "biomimetic": {...}}`` — honest and real (no fabricated numbers).
    Never raises: a QMS / organism hiccup is captured as an ``*_error`` field so a delivery is never
    lost to a quality-system fault.
    """
    coverage = _delivery_coverage(content, required_sections)
    stub = bool(_STUB_RE.search(content or "")) or len((content or "").strip()) < _MIN_SUBSTANTIVE
    quality: Dict[str, Any] = {
        "bar": list(SOLUTION_QUALITY_BAR),
        "delivery_coverage": coverage,
        "stub_found": stub,
    }

    # §11 (W287) — the compliance screen runs BEFORE the QMS seal (it used to run after, so the
    # tamper-evident quality record — and every board pack's DCS registration — omitted §11
    # verdicts entirely). Deterministic + explainable; flags, never silently blocks. W286 threads
    # the PRECOMPUTED QMS figures into the Ethical engine (no circular call back into this gate).
    try:
        from agentic_core.api.compliance import screen_compliance
        screen = screen_compliance(content or "", delivery_metrics={
            "delivery_coverage": coverage, "stub_found": stub})
        quality["compliance"] = {"overall": screen["overall"], "compliant": screen["compliant"],
                                 "verdicts": screen["verdicts"]}
    except Exception as exc:
        quality["compliance_error"] = str(exc)
    _comp = quality.get("compliance") or {}

    try:
        from agentic_core.vbs.registry import qms
        # Real, stateful gate: failures open PERSISTENT, traceable defects (W307) and move the real
        # non-conformance rate (gate failures / gates run — no normalised constants).
        # §10 (W316) — a failure's defect carries the REAL delivery reference (content hash +
        # the sections it was measured against) so the close leg can RE-MEASURE, not self-attest.
        import hashlib as _hashlib
        _ref = {"content_sha3": _hashlib.sha3_256((content or "").encode("utf-8")).hexdigest()[:24],
                "required_sections": [str(s) for s in (required_sections or [])], "label": label}
        quality["qms_gate_passed"] = bool(await qms.run_quality_gates(
            {"coverage": coverage, "stubs_found": stub}, label=label, owner_id=owner_id,
            delivery_ref=_ref))
        quality["qms_min_coverage"] = qms.min_coverage
        quality["qms_non_conformance_rate"] = qms.get_non_conformance_rate()
        quality["qms_defects"] = qms.defect_summary()
        # §10 (W307) — the bar measured PER-CRITERION (measured / caller-attested / honestly
        # not-measured), replacing the bare 16-name list that implied a measurement that never ran.
        quality["bar_measured"] = _measure_bar(coverage, stub, quality["qms_gate_passed"],
                                               qms.min_coverage, _comp, evidence)
        # The QMS document-controls the quality record through its OWNED DCMS (QMS ⊃ DCMS, ISO 9001 §7.5):
        # the gate verdict becomes a versioned, SHA3-512-sealed controlled document — W287: the §11
        # verdicts are IN the sealed payload now (the §13 repo's 'compliance + quality record').
        quality["quality_record_hash"] = await qms.control_document(
            f"qms_record:{label}",
            {"label": label, "delivery_coverage": coverage, "stub_found": stub,
             "qms_gate_passed": quality["qms_gate_passed"], "bar": SOLUTION_QUALITY_BAR,
             "bar_measured": quality["bar_measured"],
             "compliance": {"overall": _comp.get("overall"),
                            "verdicts": _comp.get("verdicts")}},
            actor="QMS")
        quality["document_controlled"] = True
    except Exception as exc:  # never break a delivery on a QMS hiccup
        quality["qms_error"] = str(exc)

    # §11×§6 (W287) — every screen SEALS to the tamper-evident UEG ledger (there were ZERO
    # compliance UEG events repo-wide), and a FAIL registers with the living organism's immune
    # system — compliance is a sensed condition, not just a response field.
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "compliance.screen", "label": label,
                         "overall": _comp.get("overall"),
                         "verdicts": {v["framework"]: v["status"] for v in (_comp.get("verdicts") or [])}})
    except Exception:
        pass
    if _comp.get("overall") == "fail":
        try:
            from agentic_core.organism.immune import immune
            immune.record(f"compliance:{label}", "compliance_fail")
        except Exception:
            pass
        # §11 (W287) — a genuine VIOLATION on a MATERIAL delivery routes to the arms-length Change
        # Control Agency at MEDIUM tier (above LOW auto-approve → a real human decision), instead of
        # dying as a response field. Calibrated: only FAIL routes (post-W286 'review' is common and
        # is already surfaced in the response + UEG — routing reviews would proliferate ceremony).
        _MATERIAL = ("cascade", "vsb_repo", "board_pack")
        if label in _MATERIAL or label.startswith("economy"):
            try:
                from agentic_core.api.change_control import SubmitChangeRequest, submit_change
                _fails = "; ".join(f"{v['framework']}: {v['reason'][:120]}"
                                   for v in (_comp.get("verdicts") or []) if v["status"] == "fail")
                await submit_change(SubmitChangeRequest(
                    title=f"Compliance FAIL on {label} delivery",
                    change_type="config_major",   # MEDIUM tier — never auto-approved
                    description=f"§11 screen failed on a material '{label}' delivery. {_fails}",
                    rationale="Automatic routing of a compliance violation to arms-length review (W287).",
                    affected_systems=["compliance", label], submitted_by="compliance_screen"))
                quality["compliance_routed_to_cca"] = True
            except Exception:
                pass

    biomimetic: Dict[str, Any] = {"layers": list(BIOMIMETIC_LAYERS),
                                  "self": "self-managing · improving · healing"}
    try:
        from agentic_core.organism.immune import immune
        from agentic_core.organism.biobus import _circadian_cycle, biobus
        biomimetic["immune"] = immune.status()
        biomimetic["circadian"] = _circadian_cycle()
        # The organism senses every quality outcome (homeostatic feedback).
        biobus.fire_signal("cognitive", f"qms.{label}",
                           f"QMS gate {'PASS' if quality.get('qms_gate_passed') else 'FAIL'} (cov={coverage})", 0.6)
    except Exception as exc:
        biomimetic["error"] = str(exc)

    return {"quality": quality, "biomimetic": biomimetic}
