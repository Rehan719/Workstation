from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/realms", tags=["User Realms"])

class RealmComponent(BaseModel):
    type: str
    config: Dict[str, Any]

class CustomRealm(BaseModel):
    name: str
    creator: str
    template_type: str # DAO, StudyGroup, Project, Community
    components: List[RealmComponent]
    monetization_enabled: bool = False
    access_fee_wst: float = 0.0

@router.post("/create")
async def create_custom_realm(realm: CustomRealm):
    """v147.0 Realm Builder backend."""
    # Simulation: Store the custom realm configuration
    return {"status": "realm_published", "realm_id": f"realm-gen-{realm.name.lower().replace(' ', '-')}"}

@router.get("/discover")
async def discover_realms(category: str = "all"):
    """Global discovery for user-generated realms."""
    return [
        {"id": "realm-1", "name": "AI Ethics Swarm", "creator": "Guardian-Alpha", "users": 1240, "template": "DAO"},
        {"id": "realm-2", "name": "Quantum Math Study", "creator": "Scholar-Beta", "users": 850, "template": "StudyGroup"}
    ]
