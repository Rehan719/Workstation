"""
Realms API v2 — real discovery from the project store.

GET  /api/realms/v2/discover   — list distinct realms from live projects
POST /api/realms/v2/create     — persist a realm config and return its ID
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/realms/v2", tags=["Sovereign Realms 2.0"])

_REALMS_DIR = Path(os.getenv("PROJECTS_DIR", "data/projects")).parent / "realms"
_REALMS_DIR.mkdir(parents=True, exist_ok=True)


class GovernanceRules(BaseModel):
    membership_type: str = "Public"
    posting_rights: str = "Everyone"
    voting_mechanism: str = "SimpleMajority"
    roles: List[str] = ["Admin", "Moderator", "Member"]
    custom_constitution_stub: Optional[str] = None


class RealmV2(BaseModel):
    id: str = ""
    name: str
    creator_id: str = "sovereign"
    description: str = ""
    template: str = "general"
    governance: GovernanceRules = GovernanceRules()
    ai_assistant_id: Optional[str] = "ceo-default"
    member_count: int = 1


@router.post("/create")
async def create_realm_v2(realm: RealmV2) -> dict:
    realm_id = realm.id or uuid.uuid4().hex
    payload = {
        **realm.model_dump(),
        "id": realm_id,
        "created_at": time.time(),
    }
    (_REALMS_DIR / f"{realm_id}.json").write_text(json.dumps(payload, indent=2))
    return {"status": "realm_instantiated", "id": realm_id, "governance_active": True}


@router.get("/discover")
async def discover_realms_v2() -> list:
    """
    Return persisted realms merged with the distinct realms visible
    in the live project store.
    """
    realms: list[dict] = []

    # Load user-created realm configs
    for f in sorted(_REALMS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            realms.append({
                "id":          data["id"],
                "name":        data.get("name", data["id"]),
                "creator":     data.get("creator_id", "sovereign"),
                "description": data.get("description", ""),
                "members":     data.get("member_count", 1),
                "governance":  data.get("governance", {}).get("voting_mechanism", "SimpleMajority"),
            })
        except Exception:
            continue

    # Augment with project-store realms not already listed
    try:
        from agentic_core.projects.api import _all_projects
        seen_names = {r["name"].lower() for r in realms}
        for p in _all_projects():
            key = p.realm.lower()
            if key and key not in seen_names:
                seen_names.add(key)
                realms.append({
                    "id":          f"realm-{key}",
                    "name":        p.realm.title(),
                    "creator":     "system",
                    "description": f"Auto-discovered from {len([x for x in _all_projects() if x.realm.lower() == key])} projects.",
                    "members":     1,
                    "governance":  "Meritocratic",
                })
    except Exception:
        pass

    return realms
