"""
IDBO Reconfiguration Engine — runtime adaptation of the organism's behaviour.

The config store drives LIVE behaviour for exactly four wired levers (rate limiting, metabolic
throttle, immune quarantine, evolution auto-apply); every other key is stored-only, and the API
says which is which instead of presenting a settings file as a control panel.

W438 honesty + governance pass:
  · Writes go through store_lock + atomic_write_json (heartbeat and the CCA's immune reconfigurator
    race API handlers on this store — the bare write_text here was the documented corruption class).
  · _load_config/reset deep-copy the defaults: the old shallow dict() aliased the nested sections,
    so an update MUTATED the module-level default template and "reset to defaults" restored the
    mutated values while labelling them defaults (proven before the fix).
  · Values are type-coerced against the default schema: the old value:Any stored the AI-suggest
    string 'false' for immune_quarantine, and bool('false') is True — applying the suggestion to
    DISABLE quarantine ENGAGED it.
  · The four live levers are GOVERNED: direct POSTs are refused with a pointer to the Change
    Control Agency, which owns organism changes (submit → review → implement applies it here).
  · Every applied change is UEG-logged and the history records the REAL prior value (reset used to
    fabricate old_value: "custom").

  GET  /api/v1/organism/config             — current configuration + per-key wiring truth
  POST /api/v1/organism/config/update      — apply a change (governed keys → 409 → CCA)
  GET  /api/v1/organism/config/history     — change history
  POST /api/v1/organism/config/reset       — governed (409 → CCA)
  POST /api/v1/organism/config/ai-suggest  — AI suggests changes (with provenance)
"""
from __future__ import annotations

import copy
import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path, atomic_write_json, store_lock
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.auth.core import get_current_user
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])

_CONFIG_STORE = data_path("organism_config.json")
_CONFIG_HISTORY = data_path("organism_config_history.json")

_DEFAULT_CONFIG: dict[str, Any] = {
    "version": "1.0.0",
    "gateway": {
        "rpm_limit": 20,
        "preferred_provider": "auto",   # auto | claude | openai | ollama
        "max_tokens": 4096,
        "temperature_bias": "neutral",  # creative | neutral | precise
    },
    "domains": {
        "religion": {"enabled": True, "priority": "high"},
        "science":  {"enabled": True, "priority": "high"},
        "education":{"enabled": True, "priority": "high"},
        "law":      {"enabled": True, "priority": "high"},
        "care":     {"enabled": True, "priority": "high"},
        "career":   {"enabled": True, "priority": "high"},
    },
    "features": {
        "immune_system":      True,
        "self_healing":       True,
        "nervous_system":     True,
        "genome_encoding":    True,
        "evolution_engine":   True,
        "digital_twin":       True,
        "swarm_orchestration":True,
        "synthesis_studio":   True,
        "capital_fund":       True,
    },
    "organism": {
        "circadian_adaptation": True,    # stored-only (no consumer reads it)
        "metabolic_throttle":   False,   # throttle when resource flow < 20%
        "immune_quarantine":    False,   # containment: no half-open probes while set
        "evolution_auto_apply": False,   # auto-apply approved evolution proposals
    },
    "last_updated": None,
    "updated_by": "system",
}

# THE TRUTH about which keys anything actually reads back — verified by grep, kept accurate on
# pain of the W318 rule (a lever may claim 'implemented' only when a real consumer is wired).
_CONSUMERS: dict[tuple[str, str], str] = {
    ("gateway", "rpm_limit"): "ai.gateway rate limiter (re-synced ~30s via _sync_reconfig)",
    ("organism", "metabolic_throttle"): "organism.heartbeat — evolve tick suppressed at low ATP (W310)",
    ("organism", "immune_quarantine"): "self_healing — OPEN circuits contained, no half-open probes (W318)",
    ("organism", "evolution_auto_apply"): "organism.heartbeat — post-approval auto-apply (W310/W346)",
}

# Wired live levers are GOVERNED: they change runtime behaviour, so they route through the CCA
# (arms-length governance for organism changes) — never a raw UI write.
_GOVERNED_KEYS = frozenset(_CONSUMERS.keys())

_CCA_POINTER = ("this key changes LIVE organism behaviour and is governed by the Change Control "
                "Agency — submit it via POST /api/v1/cca/submit with a config_change payload "
                "(review → approve → implement applies it here, audited)")


def wiring_for(section: str, key: str) -> dict[str, Any]:
    consumer = _CONSUMERS.get((section, key))
    return {"wired": consumer is not None,
            "consumer": consumer or "stored-only — nothing reads this key back",
            "governed": (section, key) in _GOVERNED_KEYS}


def _load_config() -> dict:
    if _CONFIG_STORE.exists():
        try:
            saved = json.loads(_CONFIG_STORE.read_text())
            # Merge with a DEEP copy of defaults (aliasing the default sections let updates mutate
            # the module-level template — the reset bug)
            merged = copy.deepcopy(_DEFAULT_CONFIG)
            for k, v in saved.items():
                if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
                    merged[k] = {**merged[k], **v}
                else:
                    merged[k] = v
            return merged
        except Exception:
            pass
    return copy.deepcopy(_DEFAULT_CONFIG)


def _save_config(config: dict) -> None:
    atomic_write_json(_CONFIG_STORE, config)


def _load_history() -> list[dict]:
    if _CONFIG_HISTORY.exists():
        try:
            return json.loads(_CONFIG_HISTORY.read_text())[-100:]
        except Exception:
            pass
    return []


def _append_history(change: dict) -> None:
    with store_lock(_CONFIG_HISTORY):
        history = _load_history()
        history.append(change)
        atomic_write_json(_CONFIG_HISTORY, history[-100:])


def _ueg_log(event: dict) -> None:
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log(event)
    except Exception:
        pass


def coerce_value(section: str, key: str, value: Any) -> Any:
    """Coerce a proposed value to the type the default schema holds at (section, key).

    Raises ValueError with a plain reason when the value cannot honestly become that type —
    bool('false') is True in Python, and that exact coercion gap ENGAGED quarantine from a
    suggestion meant to disable it."""
    template = _DEFAULT_CONFIG.get(section, {})
    if key not in template:
        return value   # unknown key — stored as-is, disclosed as stored-only by wiring_for
    want = template[key]
    if isinstance(want, bool):
        if isinstance(value, bool):
            return value
        if isinstance(value, str) and value.strip().lower() in ("true", "false"):
            return value.strip().lower() == "true"
        raise ValueError(f"{section}.{key} is a boolean — got {value!r} "
                         f"(only true/false accepted; note bool('false') is True in Python)")
    if isinstance(want, int) and not isinstance(want, bool):
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{section}.{key} is an integer — got {value!r}")
    if isinstance(want, float):
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValueError(f"{section}.{key} is a number — got {value!r}")
    return value


def apply_config_change(section: str, key: str, value: Any, reason: str = "",
                        updated_by: str = "system") -> dict:
    """The single write path for a config change — used by the CCA's implement/immune arms and by
    the (ungoverned-keys-only) direct route. Coerces, applies under lock, UEG-logs, records the
    real prior value, and reports the key's wiring truth."""
    if section not in _DEFAULT_CONFIG or not isinstance(_DEFAULT_CONFIG.get(section), dict):
        raise ValueError(f"Unknown config section: {section}")
    coerced = coerce_value(section, key, value)

    with store_lock(_CONFIG_STORE):
        config = _load_config()
        section_data = config[section]
        old_value = section_data.get(key)
        section_data[key] = coerced
        config[section] = section_data
        config["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        config["updated_by"] = updated_by
        _save_config(config)

    # W438 refuter catch: the self-healing quarantine cache is TTL-based (2s) — push the lever
    # value the moment it changes so containment engages immediately, not after a stale window
    if (section, key) == ("organism", "immune_quarantine"):
        try:
            from agentic_core.organism.self_healing import self_healer
            self_healer.set_quarantine(bool(coerced))
        except Exception:
            pass

    change = {
        "change_id": uuid.uuid4().hex[:8],
        "section": section,
        "key": key,
        "old_value": old_value,
        "new_value": coerced,
        "reason": reason,
        "updated_by": updated_by,
        "applied_at": config["last_updated"],
        **wiring_for(section, key),
    }
    _append_history(change)
    _ueg_log({"type": "organism.config_update", **{k: change[k] for k in
              ("section", "key", "old_value", "new_value", "reason", "updated_by")}})
    return change


def apply_config_reset(reason: str = "", updated_by: str = "system") -> dict:
    """Reset to TRUE defaults (deep copy), recording the real prior config in history."""
    with store_lock(_CONFIG_STORE):
        prior = _load_config()
        defaults = copy.deepcopy(_DEFAULT_CONFIG)
        defaults["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        defaults["updated_by"] = updated_by
        _save_config(defaults)
    change = {
        "change_id": uuid.uuid4().hex[:8],
        "section": "all",
        "key": "reset",
        "old_value": {k: prior.get(k) for k in ("gateway", "domains", "features", "organism")},
        "new_value": "defaults",
        "reason": reason or "Reset to defaults",
        "updated_by": updated_by,
        "applied_at": defaults["last_updated"],
    }
    _append_history(change)
    _ueg_log({"type": "organism.config_reset", "reason": reason, "updated_by": updated_by})
    return {"status": "reset", "config": defaults, "change": change}


@router.get("/config")
async def get_config():
    """Current organism configuration, with the wiring truth per key: which keys anything actually
    reads back (and what), which are stored-only, and which are CCA-governed live levers."""
    cfg = _load_config()
    key_wiring = []
    for section in ("gateway", "domains", "features", "organism"):
        for key in (cfg.get(section) or {}):
            key_wiring.append({"section": section, "key": key, **wiring_for(section, key)})
    return {"config": cfg,
            "key_wiring": key_wiring,
            "governed_keys": sorted(f"{s}.{k}" for s, k in _GOVERNED_KEYS),
            "note": ("only the wired keys change live behaviour; stored-only keys persist but "
                     "nothing consults them — displayed so a settings panel cannot pass a dead "
                     "switch off as a control")}


@router.get("/config/history")
async def config_history():
    """Return configuration change history."""
    history = _load_history()
    return {"history": list(reversed(history)), "total": len(history),
            "capacity": 100, "note": "history is capped at the last 100 changes"}


class ConfigUpdateRequest(BaseModel):
    section: str          # gateway | domains | features | organism
    key: str
    value: Any
    reason: str = ""


@router.post("/config/update")
async def update_config(req: ConfigUpdateRequest,
                        user: dict | None = Depends(get_current_user)):
    """Apply a configuration change — UNGOVERNED keys only.

    The four wired live levers (rpm_limit, metabolic_throttle, immune_quarantine,
    evolution_auto_apply) are refused here and routed through the Change Control Agency: they
    change live organism behaviour, and a raw settings write was the governance bypass."""
    if (req.section, req.key) in _GOVERNED_KEYS:
        raise HTTPException(status_code=409, detail={
            "refused": f"{req.section}.{req.key}", "why": _CCA_POINTER,
            "submit_via": "POST /api/v1/cca/submit",
            "example": {"title": f"Set {req.section}.{req.key}", "change_type": "config_major",
                        "description": req.reason or "organism lever change",
                        "config_change": {"section": req.section, "key": req.key, "value": req.value}}})
    # W444 — updated_by was hardcoded "owner-ui-direct": an authorship claim nothing verified
    # (any anonymous caller's change carried the Owner's name in the audit trail).
    from agentic_core.auth.core import request_owner_id
    _by = request_owner_id(user, "owner-ui-direct")
    try:
        change = apply_config_change(req.section, req.key, req.value,
                                     reason=req.reason, updated_by=_by)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"status": "applied", "change": change,
            **({"note": "this key is stored-only — nothing reads it back, so the write changes "
                        "no live behaviour"} if not change["wired"] else {})}


@router.post("/config/reset")
async def reset_config():
    """GOVERNED — a reset flips every wired live lever back to defaults at once; that is an
    organism change and belongs to the CCA."""
    raise HTTPException(status_code=409, detail={
        "refused": "config reset", "why": _CCA_POINTER,
        "submit_via": "POST /api/v1/cca/submit",
        "example": {"title": "Reset organism config to defaults", "change_type": "config_major",
                    "description": "reset all organism configuration to defaults",
                    "config_change": {"reset": True}}})


class AISuggestRequest(BaseModel):
    context: str = ""


@router.post("/config/ai-suggest")
async def ai_suggest_config(req: AISuggestRequest):
    """AI analyses REAL gathered system state and suggests configuration changes — with the serving
    provenance disclosed, each suggestion validated against the schema, and its wiring truth
    attached (a suggestion for a stored-only key is labelled as changing nothing)."""
    config = _load_config()

    # Gather system state — real readings, best-effort
    state_context = ""
    try:
        from agentic_core.organism.immune import immune
        imm = immune.status()
        state_context += f"Immune health: {imm['health']} ({imm['threat_level']}), errors: {imm['errors_in_window']}\n"
    except Exception:
        pass

    try:
        from agentic_core.organism.self_healing import self_healer
        sh = self_healer.status()
        state_context += f"Open circuits: {sh['open_circuits']}, overall health: {sh['overall_health']}\n"
    except Exception:
        pass

    try:
        import psutil
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        state_context += f"CPU: {cpu}%, Memory: {mem}%\n"
    except Exception:
        pass

    if req.context:
        state_context += f"User context: {req.context}\n"

    prompt = (
        f"You are the IDBO Reconfiguration Engine. Analyse the system state and suggest "
        f"configuration changes to optimise performance, reliability, and capability.\n\n"
        f"Current system state:\n{state_context}\n"
        f"Current configuration summary:\n"
        f"  RPM limit: {config['gateway']['rpm_limit']}\n"
        f"  Preferred provider: {config['gateway']['preferred_provider']}\n"
        f"  Immune quarantine: {config['organism']['immune_quarantine']}\n"
        f"  Metabolic throttle: {config['organism']['metabolic_throttle']}\n\n"
        "Suggest up to 3 configuration changes. For each, format as:\n"
        "CHANGE | section | key | suggested_value | rationale\n\n"
        "Valid sections: gateway, domains, features, organism\n"
        "Output ONLY the CHANGE lines. No other text."
    )

    meta = await gateway.query_meta(prompt, agent="reconfiguration_engine", augment=False)
    raw = meta.get("output") or ""

    suggestions = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.upper().startswith("CHANGE"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5:
            section, key, value = parts[1], parts[2], parts[3]
            # W438 refuter catch: coerce_value passes unknown sections through, so a suggestion
            # naming a section that does not exist was reported valid:true although every apply
            # path refuses it — validate section membership here too
            if section not in _DEFAULT_CONFIG or not isinstance(_DEFAULT_CONFIG.get(section), dict):
                coerced, valid, invalid_reason = None, False, f"unknown config section: {section}"
            else:
                try:
                    coerced = coerce_value(section, key, value)
                    valid, invalid_reason = True, None
                except ValueError as e:
                    coerced, valid, invalid_reason = None, False, str(e)
            suggestions.append({
                "section": section, "key": key,
                "suggested_value": value, "coerced_value": coerced,
                "valid": valid, **({"invalid_reason": invalid_reason} if invalid_reason else {}),
                "rationale": parts[4],
                **wiring_for(section, key),
            })

    return {
        "suggestions": suggestions,
        "system_context": state_context,
        "served_by": meta.get("served_by", "native"),
        "is_external": bool(meta.get("is_external")),
        "note": ("suggestions are ADVISORY — applying a governed key goes through the CCA; the "
                 "wired/consumer fields say whether a suggestion would change live behaviour at all"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
