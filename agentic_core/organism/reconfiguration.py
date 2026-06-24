"""
IDBO Reconfiguration Engine — runtime adaptation of the organism's behaviour.

The reconfiguration system allows the IDBO to adapt its operating parameters
at runtime without restarts:
  - Agent routing weights (which agents get priority for which domains)
  - Rate limits per endpoint category
  - Feature flags (enable/disable capabilities)
  - Domain specialisation overrides

This is the organism's adaptive response to its environment — like epigenetic
regulation in biology: same genome, different expression based on conditions.

  GET  /api/v1/organism/config             — current running configuration
  POST /api/v1/organism/config/update      — apply a configuration change
  GET  /api/v1/organism/config/history     — change history
  POST /api/v1/organism/config/reset       — reset to defaults
  POST /api/v1/organism/config/ai-suggest  — AI suggests optimal configuration
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any

from fastapi import APIRouter
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
        "circadian_adaptation": True,    # adjust behaviour by time of day
        "metabolic_throttle":   False,   # throttle when resource flow < 20%
        "immune_quarantine":    False,   # auto-disable failing endpoints
        "evolution_auto_apply": False,   # auto-apply approved evolution proposals
    },
    "last_updated": None,
    "updated_by": "system",
}


def _load_config() -> dict:
    if _CONFIG_STORE.exists():
        try:
            saved = json.loads(_CONFIG_STORE.read_text())
            # Merge with defaults to handle new fields
            merged = {**_DEFAULT_CONFIG}
            for k, v in saved.items():
                if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
                    merged[k] = {**merged[k], **v}
                else:
                    merged[k] = v
            return merged
        except Exception:
            pass
    return dict(_DEFAULT_CONFIG)


def _save_config(config: dict) -> None:
    _CONFIG_STORE.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_STORE.write_text(json.dumps(config, indent=2))


def _load_history() -> list[dict]:
    if _CONFIG_HISTORY.exists():
        try:
            return json.loads(_CONFIG_HISTORY.read_text())[-100:]
        except Exception:
            pass
    return []


def _append_history(change: dict) -> None:
    history = _load_history()
    history.append(change)
    _CONFIG_HISTORY.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_HISTORY.write_text(json.dumps(history[-100:], indent=2))


@router.get("/config")
async def get_config():
    """Return current organism configuration."""
    return _load_config()


@router.get("/config/history")
async def config_history():
    """Return configuration change history."""
    return {"history": list(reversed(_load_history())), "total": len(_load_history())}


class ConfigUpdateRequest(BaseModel):
    section: str          # gateway | domains | features | organism
    key: str
    value: Any
    reason: str = ""


@router.post("/config/update")
async def update_config(req: ConfigUpdateRequest):
    """Apply a runtime configuration change."""
    config = _load_config()

    if req.section not in config:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Unknown config section: {req.section}")

    section_data = config[req.section]
    if not isinstance(section_data, dict):
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Section {req.section} is not a dict.")

    old_value = section_data.get(req.key)
    section_data[req.key] = req.value
    config[req.section] = section_data
    config["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    _save_config(config)

    change = {
        "change_id": uuid.uuid4().hex[:8],
        "section": req.section,
        "key": req.key,
        "old_value": old_value,
        "new_value": req.value,
        "reason": req.reason,
        "applied_at": config["last_updated"],
    }
    _append_history(change)

    return {"status": "applied", "change": change}


@router.post("/config/reset")
async def reset_config():
    """Reset configuration to defaults."""
    defaults = dict(_DEFAULT_CONFIG)
    defaults["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _save_config(defaults)
    _append_history({
        "change_id": uuid.uuid4().hex[:8],
        "section": "all",
        "key": "reset",
        "old_value": "custom",
        "new_value": "defaults",
        "reason": "Manual reset to defaults",
        "applied_at": defaults["last_updated"],
    })
    return {"status": "reset", "config": defaults}


class AISuggestRequest(BaseModel):
    context: str = ""


@router.post("/config/ai-suggest")
async def ai_suggest_config(req: AISuggestRequest):
    """
    AI analyses current system state and suggests optimal configuration changes.
    """
    config = _load_config()

    # Gather system state
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

    raw = await gateway.query(prompt, agent="reconfiguration_engine")

    suggestions = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.upper().startswith("CHANGE"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 5:
            suggestions.append({
                "section": parts[1],
                "key": parts[2],
                "suggested_value": parts[3],
                "rationale": parts[4],
            })

    return {
        "suggestions": suggestions,
        "system_context": state_context,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
