"""§3A Care — the published clinical risk tables COMPUTED in-house (W457, delivery-plan P1.9,
ledger 1.9 / R5.3).

The Care domain's "validated risk scoring" had computed nothing: the route forwarded the
observations to the AI and asked it to "show working". NEWS2, MUST and Waterlow are published
lookup tables — deterministic arithmetic — so they are computed here, in-house, and returned as
a `score` block the page renders FIRST; the AI narrates interpretation only. Falls risk (NICE
CG161) has no validated total, so it is a labelled count of the multifactorial risk factors.

Every function is pure, validates its inputs (units, ranges, completeness), never guesses a
missing observation, and names its table. A clinical professional's judgement is required for
every use — the block says so.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

DISCLAIMER = ("computed in-house from the published table — a decision aid, not a diagnosis; clinical "
              "judgement by a qualified professional is required")


# ─────────────────────────────────── parsing ───────────────────────────────────

def _first(obs: Dict[str, Any], *keys: str) -> Tuple[Optional[str], Any]:
    low = {str(k).strip().lower().replace(" ", "_").replace("-", "_"): v for k, v in (obs or {}).items()}
    for k in keys:
        if k in low and str(low[k]).strip() != "":
            return k, low[k]
    return None, None


def _num(value: Any, lo: float, hi: float, name: str, warnings: List[str]) -> Optional[float]:
    """Parse '22', '22 /min', '38.2C', '101.5 F', '95%' → float in range, or None (with a warning)."""
    if value is None:
        return None
    converted = False
    if isinstance(value, (int, float)):
        v = float(value)
    else:
        s = str(value).strip().lower()
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        if not m:
            warnings.append(f"{name}: not a number ({value!r})")
            return None
        v = float(m.group(0))
        # an EXPLICIT Fahrenheit unit only ("101.5 F", "101.5°F", "101.5 fahrenheit") — never a word that
        # happens to start with f ("36.8 forehead", "38 feverish")
        if name == "temperature" and re.search(r"\d\s*°?\s*(f|fahrenheit)\b", s):
            v = round((v - 32) * 5 / 9, 1)
            converted = True
            warnings.append(f"temperature given in °F — converted to {v} °C")
    if name == "temperature" and not converted and 90 <= v <= 110:
        warnings.append(f"temperature: {v} carries no unit and looks like °F — add the unit (e.g. '{v} F'); treated as missing")
        return None
    if not (lo <= v <= hi):
        warnings.append(f"{name}: {v} is outside the plausible range {lo}–{hi} — treated as missing")
        return None
    return v


def _yes(value: Any) -> Optional[bool]:
    if value is None:
        return None
    s = str(value).strip().lower()
    if s in ("y", "yes", "true", "1", "on", "o2", "oxygen", "supplemental"):
        return True
    if s in ("n", "no", "false", "0", "off", "air", "room air", "none"):
        return False
    return None


def _bound_band(complete: bool, band: Optional[str], top: str) -> Optional[str]:
    """A banded verdict on a LOWER-BOUND total is honest only when the band cannot rise further."""
    return band if (complete or band is None or band == top) else None


# ─────────────────────────────────── NEWS2 (RCP 2017) ───────────────────────────────────

def score_news2(obs: Dict[str, Any]) -> Dict[str, Any]:
    """National Early Warning Score 2 (Royal College of Physicians, 2017). Scale 1 SpO2 unless
    `spo2_scale: 2` (hypercapnic respiratory failure, prescribed target 88–92%)."""
    w: List[str] = []
    missing: List[str] = []
    comp: Dict[str, Dict[str, Any]] = {}

    def add(name: str, value: Any, points: Optional[int], note: str = "") -> None:
        comp[name] = {"value": value, "points": points, "note": note}

    _, rr_raw = _first(obs, "resp_rate", "rr", "respiratory_rate", "respirations", "resp")
    rr = _num(rr_raw, 0, 80, "respiratory rate", w)
    if rr is None:
        missing.append("resp_rate")
    else:
        add("respiratory_rate", rr, 3 if rr <= 8 else 1 if rr <= 11 else 0 if rr <= 20 else 2 if rr <= 24 else 3, "/min")

    _, scale_raw = _first(obs, "spo2_scale", "scale")
    scale_s = str(scale_raw or "").strip().lower()
    scale: Optional[int] = 2 if scale_s in ("2", "scale 2", "scale2") else 1 if scale_s in ("", "1", "scale 1", "scale1") else None
    if scale is None:
        w.append(f"spo2_scale: {scale_raw!r} is not 1 or 2 — SpO2 cannot be scored")
    _, o2_raw = _first(obs, "oxygen", "on_oxygen", "supplemental_o2", "supplemental_oxygen", "o2", "air_or_oxygen")
    on_o2 = _yes(o2_raw)
    _, spo2_raw = _first(obs, "spo2", "sats", "oxygen_saturation", "saturation", "sao2")
    spo2 = _num(spo2_raw, 50, 100, "SpO2", w)
    if spo2 is None:
        missing.append("spo2")
    elif scale is None:
        missing.append("spo2 (spo2_scale must be 1 or 2)")
    elif scale == 1:
        add("spo2_scale_1", spo2, 3 if spo2 <= 91 else 2 if spo2 <= 93 else 1 if spo2 <= 95 else 0, "%")
    elif on_o2 is None and spo2 >= 93:
        # scale 2 scores ≥93% differently on air (0) and on oxygen (1–3) — never guess which
        missing.append("spo2 (scale 2 needs air/oxygen to score an SpO2 of 93% or more)")
    else:
        if on_o2:
            pts = 3 if spo2 <= 83 else 2 if spo2 <= 85 else 1 if spo2 <= 87 else 0 if spo2 <= 92 else 1 if spo2 <= 94 else 2 if spo2 <= 96 else 3
        else:
            pts = 3 if spo2 <= 83 else 2 if spo2 <= 85 else 1 if spo2 <= 87 else 0
        add("spo2_scale_2", spo2, pts, "% (scale 2 — prescribed target 88–92%)")
    if on_o2 is None:
        missing.append("oxygen (air or supplemental oxygen)")
    else:
        add("air_or_oxygen", "oxygen" if on_o2 else "air", 2 if on_o2 else 0)

    _, sbp_raw = _first(obs, "systolic_bp", "sbp", "bp_systolic", "systolic", "blood_pressure", "bp")
    sbp = _num(sbp_raw, 40, 300, "systolic BP", w)
    if sbp is None:
        missing.append("systolic_bp")
    else:
        add("systolic_bp", sbp, 3 if sbp <= 90 else 2 if sbp <= 100 else 1 if sbp <= 110 else 0 if sbp <= 219 else 3, "mmHg")

    _, hr_raw = _first(obs, "pulse", "hr", "heart_rate", "pulse_rate")
    hr = _num(hr_raw, 20, 250, "pulse", w)
    if hr is None:
        missing.append("pulse")
    else:
        add("pulse", hr, 3 if hr <= 40 else 1 if hr <= 50 else 0 if hr <= 90 else 1 if hr <= 110 else 2 if hr <= 130 else 3, "/min")

    _, c_raw = _first(obs, "consciousness", "acvpu", "avpu", "alertness", "conscious_level")
    if c_raw is None:
        missing.append("consciousness (ACVPU)")
    else:
        c = str(c_raw).strip().lower()
        alert = c in ("a", "alert", "awake", "0")
        cvpu = c in ("c", "v", "p", "u", "confusion", "confused", "new confusion", "voice", "pain", "unresponsive")
        if alert or cvpu:
            add("consciousness", "alert" if alert else f"CVPU ({c})", 0 if alert else 3)
        else:
            w.append(f"consciousness: {c_raw!r} is not an ACVPU value (alert / confusion / voice / pain / unresponsive)")
            missing.append("consciousness (ACVPU)")

    _, t_raw = _first(obs, "temp", "temperature", "temp_c", "temperature_c")
    temp = _num(t_raw, 25, 45, "temperature", w)
    if temp is None:
        missing.append("temperature")
    else:
        add("temperature", temp, 3 if temp <= 35.0 else 1 if temp <= 36.0 else 0 if temp <= 38.0 else 1 if temp <= 39.0 else 2, "°C")

    points = [c["points"] for c in comp.values() if c["points"] is not None]
    total = sum(points) if points else None
    any3 = any(p == 3 for p in points)
    complete = not missing
    if total is None:
        band, response = None, None
    elif total >= 7:
        band, response = "high", "emergency response — urgent or emergency clinical review by a team with critical-care competencies; continuous monitoring"
    elif not complete:
        # a lower bound can still rise — no banded verdict below the top band (F10); a single 3 is a
        # trigger in its own right and is said so
        band = None
        response = ("a single parameter already scores 3 — the low-medium urgent ward-based response applies now; "
                    "the total is a lower bound until the missing observations are recorded" if any3 else
                    "no band — the total is a lower bound until the missing observations are recorded")
    elif total >= 5:
        band, response = "medium", "key threshold for urgent response — registered nurse to immediately inform the medical team; urgent assessment by a clinician with competencies in acute illness; care in an environment with monitoring facilities; monitoring at least hourly"
    elif any3:
        band, response = "low-medium", "urgent ward-based response — registered nurse to inform the medical team, who will review and decide whether escalation is required; monitoring at least hourly"
    elif total >= 1:
        band, response = "low", "ward-based assessment — inform the registered nurse; minimum 4–6 hourly monitoring"
    else:
        band, response = "low", "routine monitoring — minimum 12 hourly"
    return {
        "tool": "news2", "table": "NEWS2 — Royal College of Physicians, 2017", "spo2_scale": scale,
        "components": comp, "total": total, "band": band, "response": response,
        "single_parameter_3": any3, "complete": complete, "missing": missing, "warnings": w,
        "note": (None if complete else "score computed from the observations given — INCOMPLETE: the total is a lower bound until the missing observations are recorded"),
        "basis": DISCLAIMER,
    }


# ─────────────────────────────────── MUST (BAPEN) ───────────────────────────────────

def score_must(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Malnutrition Universal Screening Tool (BAPEN): BMI step + unplanned weight-loss step + acute
    disease effect. 0 low · 1 medium · ≥2 high."""
    w: List[str] = []
    missing: List[str] = []
    comp: Dict[str, Dict[str, Any]] = {}
    _, bmi_raw = _first(obs, "bmi")
    bmi = _num(bmi_raw, 8, 80, "BMI", w)
    if bmi is None:
        _, wt = _first(obs, "weight_kg", "weight")
        _, ht = _first(obs, "height_m", "height_cm", "height")
        wt_v = _num(wt, 20, 400, "weight", w)
        ht_v = _num(ht, 0.5, 250, "height", w)
        if wt_v is not None and ht_v is not None:
            if ht_v > 3:   # centimetres
                ht_v = ht_v / 100.0
            bmi = round(wt_v / (ht_v * ht_v), 1)
    if bmi is None:
        missing.append("bmi (or weight_kg + height_m)")
    else:
        comp["bmi"] = {"value": bmi, "points": 0 if bmi > 20 else 1 if bmi >= 18.5 else 2, "note": "kg/m²"}
    _, loss_raw = _first(obs, "weight_loss_pct", "weight_loss_percent", "unplanned_weight_loss_pct", "weight_loss")
    loss: Optional[float] = None
    if loss_raw is not None and re.search(r"\d\s*(kg|kilo)", str(loss_raw).lower()):
        # a loss given in kilograms is NOT a percentage — convert against the current weight or refuse
        kg = _num(loss_raw, 0, 200, "weight loss kg", w)
        _, cur = _first(obs, "weight_kg", "weight")
        c_v = _num(cur, 20, 400, "weight", w)
        if kg is not None and c_v:
            loss = round(kg / (c_v + kg) * 100, 1)
            w.append(f"weight loss given as {kg} kg — {loss}% of the previous weight ({c_v + kg} kg)")
        else:
            w.append("weight loss given in kg without a current weight — cannot be converted to %; treated as missing")
    elif loss_raw is not None:
        loss = _num(loss_raw, 0, 100, "weight loss %", w)
    if loss is None:
        _, prev = _first(obs, "previous_weight_kg", "previous_weight")
        _, cur = _first(obs, "weight_kg", "weight")
        p_v = _num(prev, 20, 400, "previous weight", w)
        c_v = _num(cur, 20, 400, "weight", w)
        if p_v and c_v and p_v > 0:
            loss = round(max(0.0, (p_v - c_v) / p_v * 100), 1)
    if loss is None:
        missing.append("weight_loss_pct (unplanned, past 3–6 months)")
    else:
        comp["unplanned_weight_loss"] = {"value": loss, "points": 0 if loss < 5 else 1 if loss <= 10 else 2, "note": "% in 3–6 months"}
    _, acute_raw = _first(obs, "acute_disease", "acutely_ill_no_intake", "no_intake_5_days", "acute_disease_effect")
    acute = _yes(acute_raw)
    if acute is None:
        missing.append("acute_disease (acutely ill and no nutritional intake for >5 days: yes/no)")
    else:
        comp["acute_disease_effect"] = {"value": "yes" if acute else "no", "points": 2 if acute else 0, "note": ""}
    points = [c["points"] for c in comp.values()]
    total = sum(points) if points else None
    complete = not missing
    band = _bound_band(complete, None if total is None else "low" if total == 0 else "medium" if total == 1 else "high", "high")
    response = {None: (None if total is None else "no band — the total is a lower bound until the missing steps are recorded"),
                "low": "routine clinical care — repeat screening (hospital weekly; care home monthly; community annually for special groups)",
                "medium": "observe — document intake for 3 days; if adequate, little concern and repeat screening; if inadequate, follow local policy",
                "high": "treat — refer to a dietitian / nutritional support team; set goals, improve and increase overall intake; monitor and review"}[band]
    return {"tool": "must", "table": "MUST — BAPEN", "components": comp, "total": total, "band": band, "response": response,
            "complete": complete, "missing": missing, "warnings": w,
            "note": None if complete else "INCOMPLETE — the total is a lower bound until the missing steps are recorded", "basis": DISCLAIMER}


# ─────────────────────────────────── Waterlow ───────────────────────────────────

_WATERLOW = {
    "build": {"average": 0, "above_average": 1, "obese": 2, "below_average": 3},
    "skin": {"healthy": 0, "tissue_paper": 1, "dry": 1, "oedematous": 1, "clammy": 1, "discoloured": 2, "broken": 3},
    "continence": {"complete": 0, "catheterised": 0, "urinary_incontinence": 1, "faecal_incontinence": 2, "doubly_incontinent": 3},
    "mobility": {"fully": 0, "restless": 1, "apathetic": 2, "restricted": 3, "bedbound": 4, "chairbound": 5},
    "appetite": {"average": 0, "poor": 1, "ng_tube": 2, "fluids_only": 2, "nbm": 3, "anorexic": 3},
    "tissue_malnutrition": {"none": 0, "terminal_cachexia": 8, "multiple_organ_failure": 8, "single_organ_failure": 5,
                            "peripheral_vascular_disease": 5, "anaemia": 2, "smoking": 1},
    "neurological_deficit": {"none": 0, "diabetes": 4, "ms": 4, "cva": 4, "motor_sensory": 4, "paraplegia": 6},
    "major_surgery_trauma": {"none": 0, "orthopaedic_spinal": 5, "on_table_over_2h": 5, "on_table_over_6h": 8},
    "medication": {"none": 0, "cytotoxics": 4, "high_dose_steroids": 4, "anti_inflammatory": 4},
}


_WATERLOW_ADDITIVE = ("tissue_malnutrition", "neurological_deficit", "major_surgery_trauma", "medication")


def score_waterlow(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Waterlow pressure-ulcer risk — the Waterlow card with the appetite row (the 2005 revision replaced
    that row with a Malnutrition Screening Tool block, which this table does NOT implement).
    10+ at risk · 15+ high risk · 20+ very high. The special-risk groups are additive on the card
    ("anaemia, smoking" scores 2 + 1) and a group that is not stated is MISSING — never scored as none."""
    w: List[str] = []
    missing: List[str] = []
    comp: Dict[str, Dict[str, Any]] = {}
    for field, table in _WATERLOW.items():
        _, raw = _first(obs, field)
        if raw is None:
            missing.append(field + " (" + " / ".join(table) + ")")
            continue
        tokens = [x.strip().lower().replace(" ", "_").replace("-", "_")
                  for x in re.split(r"[,+;]|\band\b", str(raw).lower()) if x.strip()]
        unknown = [x for x in tokens if x not in table]
        if not tokens or unknown or (len(tokens) > 1 and field not in _WATERLOW_ADDITIVE):
            w.append(f"{field}: {', '.join(unknown) or raw!r} is not one of {', '.join(table)}"
                     + (" (one value only)" if len(tokens) > 1 and field not in _WATERLOW_ADDITIVE else "")
                     + " — treated as missing")
            missing.append(field)
            continue
        comp[field] = {"value": " + ".join(tokens), "points": sum(table[x] for x in tokens),
                       "note": "additive special risks" if len(tokens) > 1 else ""}
    _, sex_raw = _first(obs, "sex", "gender")
    sex = str(sex_raw or "").strip().lower()
    if sex in ("m", "male"):
        comp["sex"] = {"value": "male", "points": 1, "note": ""}
    elif sex in ("f", "female"):
        comp["sex"] = {"value": "female", "points": 2, "note": ""}
    else:
        missing.append("sex (male/female)")
    _, age_raw = _first(obs, "age", "age_years")
    age = _num(age_raw, 0, 120, "age", w)
    if age is None:
        missing.append("age")
    else:
        comp["age"] = {"value": age, "points": 1 if age <= 49 else 2 if age <= 64 else 3 if age <= 74 else 4 if age <= 80 else 5, "note": "years"}
    points = [c["points"] for c in comp.values()]
    total = sum(points) if points else None
    complete = not missing
    band = _bound_band(complete, None if total is None else "very high risk" if total >= 20 else "high risk" if total >= 15 else "at risk" if total >= 10 else "low", "very high risk")
    return {"tool": "waterlow", "table": "Waterlow pressure ulcer risk (the appetite-row card — not the 2005 MST revision)", "components": comp, "total": total, "band": band,
            "response": {None: (None if total is None else "no band — the total is a lower bound until the missing items are recorded"),
                         "low": "reassess on change of condition", "at risk": "pressure-relieving support and a repositioning plan; reassess regularly",
                         "high risk": "high-specification foam / alternating-pressure support; skin inspection every shift; nutrition review",
                         "very high risk": "alternating-pressure or low-air-loss support; tissue-viability referral; documented repositioning"}[band],
            "complete": complete, "missing": missing, "warnings": w,
            "note": None if complete else "INCOMPLETE — the total is a lower bound until the missing items are recorded", "basis": DISCLAIMER}


# ─────────────────────────────────── Falls (NICE CG161) ───────────────────────────────────

_FALLS_FACTORS = ("falls_history", "gait_balance_mobility_problem", "osteoporosis_risk", "fear_of_falling",
                  "visual_impairment", "cognitive_impairment", "urinary_incontinence", "home_hazards",
                  "polypharmacy_or_psychotropics", "postural_hypotension", "age_65_plus")


def score_falls(obs: Dict[str, Any]) -> Dict[str, Any]:
    """NICE CG161 is a MULTIFACTORIAL assessment with no validated numeric total: this is a labelled
    COUNT of the factors present, not a score. A falls history, or two or more factors, warrants the
    multifactorial assessment; it does not replace it."""
    present, absent, missing = [], [], []
    for f in _FALLS_FACTORS:
        _, raw = _first(obs, f)
        if f == "age_65_plus" and raw is None:
            _, age_raw = _first(obs, "age")
            if age_raw is not None:
                a = _num(age_raw, 0, 120, "age", [])
                raw = None if a is None else ("yes" if a >= 65 else "no")
        v = _yes(raw)
        (present if v else absent if v is False else missing).append(f)
    count = len(present)
    return {"tool": "falls_risk", "table": "NICE CG161 multifactorial falls risk — factor COUNT, not a validated score",
            "components": {f: {"value": "present", "points": 1, "note": ""} for f in present},
            "total": count, "band": ("multifactorial assessment warranted" if ("falls_history" in present or count >= 2) else "no trigger recorded"),
            "response": ("offer a multifactorial falls risk assessment (NICE CG161 1.1.2) — this count is not a score"
                         if ("falls_history" in present or count >= 2) else "no falls history and fewer than two factors recorded — reassess on change"),
            "factors_present": present, "factors_absent": absent, "complete": not missing, "missing": missing, "warnings": [],
            "note": "NICE CG161 defines no numeric falls score — this is a count of factors, not a score; a prompt for the multifactorial assessment, never a substitute",
            "basis": DISCLAIMER}


_SCORERS = {"news2": score_news2, "must": score_must, "waterlow": score_waterlow, "falls_risk": score_falls}


def compute_score(tool: str, obs: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch by tool id. A tool without a published table returns an honest 'not available'."""
    fn = _SCORERS.get((tool or "").strip().lower())
    if fn is None:
        return {"tool": tool, "available": False,
                "note": "no published arithmetic exists for this tool — the narrative below is an AI aid only, not a score",
                "basis": DISCLAIMER}
    out = fn(obs or {})
    out["available"] = True
    return out


def score_summary(score: Dict[str, Any]) -> str:
    """One line for the AI's prompt and the record: 'NEWS2 6 · medium · urgent ward-based response'."""
    if not score or not score.get("available"):
        return "no computed score (no published table for this tool)"
    tool = str(score.get("tool", "")).upper().replace("_", " ")
    total = score.get("total")
    if total is None:
        return f"{tool}: no total — missing {', '.join(score.get('missing') or [])}"
    parts = ", ".join(f"{k} {v['points']}" for k, v in (score.get("components") or {}).items() if v.get("points") is not None)
    head = (f"{tool} factor count {total}" if score.get("tool") == "falls_risk"
            else f"{tool} {total}" if score.get("complete") or score.get("band") else f"{tool} ≥ {total} (lower bound)")
    return (f"{head} · {score.get('band') or 'no band'} · {score.get('response')} ({parts})"
            + ("" if score.get("complete") else f" — INCOMPLETE, missing: {', '.join(score.get('missing') or [])}"))
