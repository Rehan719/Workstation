import datetime
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.catalog.api import list_products

router = APIRouter(prefix="/bto", tags=["BTO Configurator"])

COMPONENT_ROUTES: Dict[str, str] = {
    "vsb": "/ceo",
    "csuite": "/debate",
    "coe": "/audit",
    "realms": "/realm-editor",
    "products": "/bto",
    "services": "/marketplace",
}


class BTOConfigureRequest(BaseModel):
    entity_name: str = "Unnamed Entity"
    components: List[str] = []
    product_resources: List[str] = []   # slugs of catalog products to integrate


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
            "routes": {
                "Religion": "/qep-religion", "Science": "/science", "Law": "/law",
                "Care": "/care", "Employment": "/employment", "Education": "/education",
            },
        }
    if kind == "realms":
        return {"available": ["LEARNER", "DEVELOPER", "ENTERPRISE", "SCHOLAR", "GENOME"], "route": COMPONENT_ROUTES["realms"]}
    if kind == "products":
        return {"catalog": list_products(), "route": COMPONENT_ROUTES["products"]}
    if kind == "services":
        return {"available": ["Synthesis Studio", "Capital Fund", "Living Marketplace"], "route": COMPONENT_ROUTES["services"]}
    return {"status": "Unknown component"}


def _integrate_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Wraps a catalog product entry as an integrated BTO resource record."""
    return {
        "slug": product["slug"],
        "name": product["name"],
        "tier": product["tier"],
        "category": product["category"],
        "features": product.get("features", []),
        "route": product.get("route"),
        "status": "INTEGRATED",
        "integration_mode": "Plug-in resource — accessible via Sovereign Mesh",
    }


@router.get("/components")
async def list_components():
    return {
        "components": [
            {"id": "entity",   "label": "Entity"},
            {"id": "organism", "label": "Organism"},
            {"id": "vsb",      "label": "Virtual Sovereign Business"},
            {"id": "csuite",   "label": "C-Suite"},
            {"id": "coe",      "label": "Centers of Excellence"},
            {"id": "domains",  "label": "Domains"},
            {"id": "realms",   "label": "Realms"},
            {"id": "products", "label": "Products"},
            {"id": "services", "label": "Services"},
        ]
    }


@router.post("/configure")
async def configure_bto(request: BTOConfigureRequest):
    # Resolve requested product resources from the catalog
    all_products: List[Dict[str, Any]] = list_products()
    slug_index: Dict[str, Dict[str, Any]] = {p["slug"]: p for p in all_products}
    integrated = [
        _integrate_product(slug_index[slug])
        for slug in request.product_resources
        if slug in slug_index
    ]

    blueprint = {
        "blueprint_id": str(uuid.uuid4()),
        "entity_name": request.entity_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "components": {kind: _build_component(kind) for kind in request.components},
        "product_resources": integrated,
        "resource_count": len(integrated),
        "component_count": len(request.components),
    }
    return blueprint
