import datetime
import uuid
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.catalog.api import list_products

router = APIRouter(prefix="/bto", tags=["BTO Configurator"])

COMPONENT_ROUTES: Dict[str, str] = {
    "vsb": "/ceo",
    "csuite": "/debate",
    "coe": "/audit",
    "realms": "/realm-editor",
    "products": "/products",
    "services": "/marketplace",
}


class BTOConfigureRequest(BaseModel):
    entity_name: str = "Unnamed Entity"
    components: List[str] = []


def _build_component(kind: str) -> Dict[str, Any]:
    if kind == "entity":
        return {"type": "Sovereign Digital Entity", "status": "Provisioned", "identity_layer": "L1 Core Identity"}
    if kind == "organism":
        return {"type": "Sovereign Digital Organism", "layers": [f"L{n}" for n in range(1, 13)], "status": "Bootstrapped"}
    if kind == "vsb":
        return {"name": "Virtual Sovereign Business", "ai_ceo": "VSB AI CEO", "status": "Active", "route": COMPONENT_ROUTES["vsb"]}
    if kind == "csuite":
        return {
            "members": [
                {"role": "CFO", "status": "ACTIVE"},
                {"role": "CTO", "status": "ACTIVE"},
                {"role": "CMO", "status": "ACTIVE"},
                {"role": "COO", "status": "ACTIVE"},
            ],
            "route": COMPONENT_ROUTES["csuite"],
        }
    if kind == "coe":
        return {"centers": ["Security", "AI Ethics", "Constitutional Compliance", "Quality Assurance"], "route": COMPONENT_ROUTES["coe"]}
    if kind == "domains":
        return {
            "available": ["Religion", "Science", "Law", "Care", "Employment", "Education"],
            "routes": {"Religion": "/qep-religion", "Science": "/science", "Law": "/law", "Care": "/care", "Employment": "/employment", "Education": "/education"},
        }
    if kind == "realms":
        return {"available": ["LEARNER", "DEVELOPER", "ENTERPRISE", "SCHOLAR", "GENOME"], "route": COMPONENT_ROUTES["realms"]}
    if kind == "products":
        return {"catalog": list_products(), "route": COMPONENT_ROUTES["products"]}
    if kind == "services":
        return {"available": ["Synthesis Studio", "Capital Fund", "Living Marketplace"], "route": COMPONENT_ROUTES["services"]}
    return {"status": "Unknown component"}


@router.get("/components")
async def list_components():
    return {
        "components": [
            {"id": "entity", "label": "Entity"},
            {"id": "organism", "label": "Organism"},
            {"id": "vsb", "label": "Virtual Sovereign Business"},
            {"id": "csuite", "label": "C-Suite"},
            {"id": "coe", "label": "Centers of Excellence"},
            {"id": "domains", "label": "Domains"},
            {"id": "realms", "label": "Realms"},
            {"id": "products", "label": "Products"},
            {"id": "services", "label": "Services"},
        ]
    }


@router.post("/configure")
async def configure_bto(request: BTOConfigureRequest):
    blueprint = {
        "blueprint_id": str(uuid.uuid4()),
        "entity_name": request.entity_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "components": {kind: _build_component(kind) for kind in request.components},
    }
    return blueprint
