"""
QEP Intelligence API — explainability, translation, and cross-domain adaptation.

Backs the QEP frontier pages that previously had no backend. Distinct paths under
the existing /api/v1/qep prefix (no collision with hifz/tajweed/gamification):

  Explainability (XAI)
    GET  /api/v1/qep/xai/explanations        — feature-attributed rationale for SM-2 scheduling
    POST /api/v1/qep/recommendation/update   — retune the recommendation model weights

  Translation
    GET  /api/v1/qep/translation/status      — pipeline health + supported languages
    POST /api/v1/qep/translation/translate   — AI translation of educational content

  Cross-Domain Adaptation
    GET  /api/v1/qep/adaptation/registry     — registry of adapted plugins/patterns
    POST /api/v1/qep/adaptation/execute      — adapt a pattern into a new domain

  Compliance
    GET  /api/v1/qep/compliance/audit        — governance/compliance audit summary
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/qep", tags=["qep-intelligence"])

_STORE = data_path("qep_intel")
_STORE.mkdir(parents=True, exist_ok=True)
_REGISTRY = _STORE / "adaptation_registry.json"
_MODEL = _STORE / "recommendation_model.json"

_SUPPORTED_LANGUAGES = ["Arabic", "English", "Urdu", "Turkish", "Indonesian", "French", "Malay", "Bengali"]

# W409 — these two seeds carried fidelity 0.94 and 0.89, and the compliance audit graded adaptation
# fidelity against them. Both numbers were literals, so the control could only ever pass: the audit
# was marking its own homework with answers it had written itself. The patterns are real examples
# and are kept; the invented scores are not, so fidelity is null until something measures it.
_DEFAULT_ADAPTATIONS = [
    {"id": "ADP-hifz-science", "pattern": "SM-2 spaced repetition", "from": "religion",
     "to": "science", "status": "pattern_seed", "fidelity": None},
    {"id": "ADP-tajweed-care", "pattern": "phoneme feedback loop", "from": "religion",
     "to": "care", "status": "pattern_seed", "fidelity": None},
]


def _migrate_registry(registry: list) -> list:
    """W439 refuter catch (HIGH): the LIVE store still held the W409 code-literal fidelities
    (0.94/0.89, status 'active') — and the audit relabelled them "model-self-declared", a wording
    false about its own data. Any legacy entry that predates provenance (no served_by) cannot
    prove where its figure came from: the figure is nulled with the reason, and legacy 'active'
    statuses become what they are. Self-correcting on every read, in every deployment."""
    for a in registry:
        if "served_by" not in a:
            if isinstance(a.get("fidelity"), (int, float)):
                a["fidelity"] = None
                a["fidelity_note"] = ("legacy figure removed (W439) — it predates provenance "
                                      "tracking and traces to a W409 code literal, not a model")
            if a.get("status") == "active":
                a["status"] = "pattern_seed"
    return registry


def _load(path: Path, default: Any) -> Any:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return default
    return default


from agentic_core.config import store_lock


def _save(path: Path, data: Any) -> None:
    from agentic_core.config import atomic_write_json
    atomic_write_json(path, data)   # W439: store convention — no torn reads


# ── Explainability (XAI) ──────────────────────────────────────────────────────

class RecommendationUpdate(BaseModel):
    ease_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    interval_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    quality_weight: float = Field(default=0.25, ge=0.0, le=1.0)


@router.get("/xai/explanations")
async def xai_explanations(ease_factor: float = 2.5, interval_days: int = 6,
                           repetition: int = 3, last_quality: int = 4):
    """
    Feature-attributed explanation of *why* the SM-2 engine scheduled a hifz
    review as it did. Real XAI over the actual scheduling inputs QEP uses.
    """
    model = _load(_MODEL, {"ease_weight": 0.4, "interval_weight": 0.35, "quality_weight": 0.25})
    # W439 — the "why the engine scheduled it" answer must come from THE ENGINE: the old
    # next_interval_days here was a parallel approximation (interval x ease) that disagreed with
    # the real SM-2 (which updates the efactor first and branches on repetition count) while
    # presenting itself as the engine's rationale.
    from agentic_core.religious_domain.memorization.engine import MemorizationEngine
    real_interval, real_efactor = MemorizationEngine().calculate_next_review(
        quality=last_quality, repetitions=repetition,
        previous_interval=interval_days, previous_efactor=ease_factor)
    decision = "advance" if last_quality >= 3 else "reset"
    contributions = [
        {"feature": "ease_factor", "value": ease_factor,
         "contribution": round(model["ease_weight"] * (ease_factor / 2.5), 3),
         "rationale": "Higher ease ⇒ longer interval; the learner retains this ayah well."},
        {"feature": "interval_days", "value": interval_days,
         "contribution": round(model["interval_weight"] * (interval_days / 6), 3),
         "rationale": "Prior interval anchors the next spacing step."},
        {"feature": "repetition", "value": repetition,
         "contribution": round(0.1 * repetition, 3),
         "rationale": "Each successful repetition compounds the interval growth."},
        {"feature": "last_quality", "value": last_quality,
         "contribution": round(model["quality_weight"] * (last_quality / 5), 3),
         "rationale": "Recall quality <3 resets the schedule; ≥3 advances it."},
    ]
    return {
        "decision": decision,
        "next_interval_days": real_interval,
        "new_efactor": round(real_efactor, 3),
        "interval_basis": "computed by the REAL MemorizationEngine (SM-2), not an approximation",
        "explanations": contributions,
        "explanations_basis": ("display-weight attribution over the scheduling inputs — an aid to "
                               "reading the decision, not the engine's internal arithmetic; the "
                               "repetition entry uses a fixed display constant of 0.1 that is not "
                               "part of the tunable model weights"),
        "model_weights": model,
        "method": "real SM-2 next-review + display-weight feature attribution",
    }


@router.post("/recommendation/update")
async def recommendation_update(req: RecommendationUpdate):
    """Retune the recommendation model weights (persisted). W439: the compliance audit's own
    check requires the weights to sum to ~1.0 — accepting weights that fail it would let this
    route silently break the contract the audit grades."""
    total = req.ease_weight + req.interval_weight + req.quality_weight
    if abs(total - 1.0) >= 0.05:
        from fastapi import HTTPException
        raise HTTPException(status_code=422,
                            detail=f"weights must sum to ~1.0 (got {round(total, 3)}) — the "
                                   f"compliance audit grades exactly this")
    model = {
        "ease_weight": req.ease_weight,
        "interval_weight": req.interval_weight,
        "quality_weight": req.quality_weight,
        "updated_at": time.time(),
    }
    _save(_MODEL, model)
    return {"status": "updated", "model_weights": model}


# ── Translation ───────────────────────────────────────────────────────────────

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "English"
    source_language: str = "Arabic"
    preserve_tajweed: bool = True


@router.get("/translation/status")
async def translation_status():
    """W439 — every field here was a constant: pipeline "online" (probed nothing), an engine
    string describing a routing order that no longer exists (the gateway is in-house-first:
    owned local model → native floor; external is opt-in), and tajweed_preservation True as a
    capability claim nothing checks. The status is now computed: translation is AVAILABLE only
    when a model resource exists, because the deterministic floor cannot translate."""
    try:
        from agentic_core.ai.native.model_resource import local_models, external_allowed
        models = local_models()
        ext = external_allowed()
    except Exception:
        models, ext = [], False
    available = bool(models) or ext
    return {
        "translation_available": available,
        "availability_basis": (f"{len(models)} local model(s) discovered"
                               + (" + external accelerants enabled" if ext else "")
                               if available else
                               "no model resource is available — the deterministic native floor "
                               "cannot translate, so /translate refuses rather than fabricating"),
        "supported_languages": _SUPPORTED_LANGUAGES,
        "engine": "in-house-first gateway (owned local model; external accelerants opt-in via AI_ALLOW_EXTERNAL)",
        "tajweed_note": ("recitation-note annotation is REQUESTED from the model when "
                         "preserve_tajweed is set — it is a prompt instruction, not a verified "
                         "capability"),
    }


@router.post("/translation/translate")
async def translation_translate(req: TranslateRequest):
    prompt = (
        f"Translate the following from {req.source_language} to {req.target_language}. "
        "Preserve meaning and scholarly register"
        + (" and annotate tajweed/recitation notes where relevant" if req.preserve_tajweed else "")
        + f".\n\nText:\n{req.text}\n\nReturn only the translation."
    )
    # W439 — a translation must come from a MODEL. The deterministic native floor composes
    # structured output from the prompt itself; on faith content, presenting that scaffold as a
    # "translation" with status "translated" would be fabrication of the worst kind.
    # Refuter catch, round 2: the first version called the gateway BEFORE refusing, so the floor
    # scaffold was already written to the interaction log and AI memory by the time the 503 fired.
    # Availability is now checked FIRST — a refusal has no side effects at all.
    try:
        from agentic_core.ai.native.model_resource import local_models, external_allowed
        _available = bool(local_models()) or external_allowed()
    except Exception:
        _available = False
    if not _available:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=(
            "no model resource is available to translate — the deterministic native floor cannot "
            "translate and its output will not be presented as a translation. Start a local model "
            "(Ollama) or enable an external accelerant."))
    meta = await gateway.query_meta(prompt, agent="qep_translator", augment=False)
    served_by = meta.get("served_by", "native")
    if served_by == "native":
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail=(
            "the model resource failed to serve and the deterministic floor answered instead — "
            "its output will not be presented as a translation."))
    return {
        "source_language": req.source_language,
        "target_language": req.target_language,
        "original": req.text,
        "translation": meta.get("output") or "",
        "served_by": served_by,
        "is_external": bool(meta.get("is_external")),
        "status": "translated",
        "label": "AI-assisted translation — not authoritative; scholarly translations differ and matter",
    }


# ── Cross-Domain Adaptation ───────────────────────────────────────────────────

class AdaptationRequest(BaseModel):
    pattern: str
    source_domain: str = "religion"
    target_domain: str = "science"


@router.get("/adaptation/registry")
async def adaptation_registry():
    with store_lock(_REGISTRY):
        registry = _load(_REGISTRY, None)
        if registry is None:
            registry = list(_DEFAULT_ADAPTATIONS)
        registry = _migrate_registry(registry)
        _save(_REGISTRY, registry)
    return {"adaptations": registry, "count": len(registry)}


def _parse_fidelity(blueprint: str):
    """Pull the model's own "Expected Fidelity" figure out of its reply, or return None.

    Took three attempts, each caught by testing rather than reasoning:
      1. allowing a bare 0 or 1 matched the "0" inside the prompt's own range hint "(0-1)" and
         returned 0.0 for a reply that said 0.72 — a worse lie than the constant it replaced;
      2. requiring a decimal then failed on that same reply, because the digits inside "(0-1)"
         break any non-digit gap between the word and the number.
    Parenthetical hints are therefore removed before matching, and only a decimal counts.
    """
    import re as _re
    if not isinstance(blueprint, str):
        return None
    cleaned = _re.sub(r"\([^)]*\)", " ", blueprint)
    m = _re.search(r"fidelity\D{0,40}(0?\.\d+|1\.0+)", cleaned, _re.I)
    if not m:
        return None
    try:
        val = float(m.group(1))
    except ValueError:
        return None
    return val if 0.0 <= val <= 1.0 else None

@router.post("/adaptation/execute")
async def adaptation_execute(req: AdaptationRequest):
    """Adapt a learning pattern from one domain into another via the AI gateway."""
    prompt = (
        f"You are the QEP Cross-Domain Adaptation engine. Adapt the pedagogical pattern "
        f"'{req.pattern}' from the '{req.source_domain}' domain into the '{req.target_domain}' "
        "domain.\n\n## Adapted Mechanism\n## Key Adjustments\n## Expected Fidelity (0-1)"
    )
    # W439 audit catch: gateway.query dropped served_by (a floor scaffold was indistinguishable
    # from a model blueprint), the entry claimed status "active" and the response "executed" when
    # nothing was adapted, activated, or installed anywhere.
    try:
        _meta = await gateway.query_meta(prompt, agent="qep_adapter", augment=False)
        blueprint = _meta.get("output") or ""
        _served_by = _meta.get("served_by", "native")
        _bp_status = "blueprint_generated"
    except Exception as e:
        blueprint = f"[adaptation blueprint unavailable: {e}]"
        _served_by, _bp_status = None, "error"

    with store_lock(_REGISTRY):
        registry = _migrate_registry(_load(_REGISTRY, list(_DEFAULT_ADAPTATIONS)))
        entry = {
        "id": f"ADP-{uuid.uuid4().hex[:8]}",
        "pattern": req.pattern,
        "from": req.source_domain,
        "to": req.target_domain,
        "status": _bp_status,
        "served_by": _served_by,
        # W409 — this was the literal 0.9. The prompt above explicitly asks the model for
        # "## Expected Fidelity (0-1)", and the reply was stored only as free text in `blueprint`
        # while the number was thrown away and replaced by a constant. The model was asked for the
        # exact value that was then invented over the top of it. The reply is now parsed, and when
        # it carries no usable figure the fidelity is null rather than a flattering default.
        "fidelity": _parse_fidelity(blueprint),
        "ts": time.time(),
        }
        registry.append(entry)
        _save(_REGISTRY, registry)
    return {"adaptation": entry, "blueprint": blueprint, "status": _bp_status,
            "status_note": ("a blueprint was generated and recorded — nothing was installed or "
                            "activated anywhere; 'executed'/'active' were the old overclaims")}


# ── Compliance ────────────────────────────────────────────────────────────────

@router.get("/compliance/audit")
async def compliance_audit():
    """Compliance summary derived from checks that can actually fail.

    W409 - this returned "compliant": True as a LITERAL that no branch could change, with two of its
    four controls hardcoded to "pass" ("Explainability (XAI) available", "Translation
    tajweed-preservation") without testing anything. A third graded adaptation fidelity against the
    constant 0.9 that the same module stamped on every adaptation, so it could only ever pass. Only
    the weight-normalisation check was real. An audit that cannot fail is not an audit, and it
    carried an audited_at timestamp and a count to make it look like one.

    The two untestable controls now report not_checked, and the verdict is computed from the
    results: any failure makes it false, and unchecked controls make it null rather than true.
    """
    registry = _migrate_registry(_load(_REGISTRY, list(_DEFAULT_ADAPTATIONS)))
    model = _load(_MODEL, {"ease_weight": 0.4, "interval_weight": 0.35, "quality_weight": 0.25})

    # only figures with provenance count — a legacy number nobody declared grades nothing
    graded = [a.get("fidelity") for a in registry
              if isinstance(a.get("fidelity"), (int, float)) and "served_by" in a]
    weights_ok = abs(sum(v for k, v in model.items() if k.endswith("_weight")) - 1.0) < 0.05

    checks = [
        {"control": "Explainability (XAI) available", "status": "not_checked",
         "reason": "No explainability check exists to run; a pass was previously asserted."},
        {"control": "Translation tajweed-preservation", "status": "not_checked",
         "reason": "No tajweed-preservation check exists to run; a pass was previously asserted."},
        {"control": "Adaptation fidelity (model self-declared) >= 0.85",
         # W439 audit catch: the graded figure is the model's OWN "Expected Fidelity" reply —
         # self-assessment, not measurement; it can satisfy the threshold but never PASS the audit
         "status": ("self_declared" if graded and all(f >= 0.85 for f in graded)
                    else "review" if graded else "not_checked"),
         "reason": (f"{len(graded)} of {len(registry)} adaptation(s) carry a model-self-declared "
                    f"expected fidelity (not independently measured)."
                    if registry else "No adaptations recorded.")},
        {"control": "Recommendation weights normalised",
         "status": "pass" if weights_ok else "review"},
    ]
    statuses = {c["status"] for c in checks}
    compliant = (False if "review" in statuses
                 else None if ("not_checked" in statuses or "self_declared" in statuses) else True)
    return {
        "compliant": compliant,
        "checks": checks,
        "audited_at": time.time(),
        "adaptations_audited": len(registry),
        "note": ("compliant is null when a control could not be checked. It is never asserted "
                 "true on the strength of controls that do not run."),
    }
