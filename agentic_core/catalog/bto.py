import datetime
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.catalog.api import catalogue_counts, list_products, not_served_reason, served_products

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
    # W415 — these read "Provisioned" / "Bootstrapped" / "Active" / "ACTIVE", and BTOCatalog.tsx
    # renders the `status` string verbatim as each component's summary line. They are past-tense
    # state assertions, but configure_bto provisions, bootstraps and activates nothing — it
    # dict-builds a design blueprint. Nothing here is running when the user reads "Active".
    # The honest label is what this actually is: a specification. POST /bto/build is the sibling
    # that really produces (via the §13 deliverables engine) and honestly reports BUILT/FAILED.
    _SPEC = "SPECIFIED (blueprint only)"
    if kind == "entity":
        return {"type": "Sovereign Digital Entity", "status": _SPEC, "provisioned": False,
                "identity_layer": "L1 Core Identity"}
    if kind == "organism":
        return {"type": "Sovereign Digital Organism", "layers": [f"L{n}" for n in range(1, 13)],
                "status": _SPEC, "bootstrapped": False}
    if kind == "vsb":
        return {"name": "Virtual Sovereign Business", "ai_ceo": "VSB AI CEO", "status": _SPEC,
                "activated": False, "route": COMPONENT_ROUTES["vsb"]}
    if kind == "csuite":
        return {
            "members": [
                {"role": "CFO", "status": _SPEC, "instantiated": False},
                {"role": "CTO", "status": _SPEC, "instantiated": False},
                {"role": "CMO", "status": _SPEC, "instantiated": False},
                {"role": "COO", "status": _SPEC, "instantiated": False},
            ],
            "route": COMPONENT_ROUTES["csuite"],
        }
    if kind == "coe":
        return {"centers": ["Security", "AI Ethics", "Constitutional Compliance", "Quality Assurance"], "route": COMPONENT_ROUTES["coe"]}
    if kind == "domains":
        # §17.1 (W311) — the CANONICAL taxonomy, not a local variant
        from agentic_core.taxonomy import DOMAIN_LABELS
        return {
            "available": list(DOMAIN_LABELS.values()),
            "routes": {
                "Religion": "/qep-religion", "Science": "/science", "Law": "/law",
                "Care": "/care", "Employment": "/employment", "Education": "/education",
            },
        }
    if kind == "realms":
        # §17.1 (W311) — was a drifted five-item list (LEARNER/DEVELOPER/ENTERPRISE/SCHOLAR/GENOME);
        # the canon is the Whole Vision's 4 Realms.
        from agentic_core.taxonomy import REALM_LABELS
        return {"available": list(REALM_LABELS.values()), "route": COMPONENT_ROUTES["realms"]}
    if kind == "products":
        # W470 — the blueprint's catalogue is what a route serves; the rest is named, never built from
        every = list_products()
        return {"catalog": served_products(), "counts": catalogue_counts(every),
                "not_served": [{"slug": p["slug"], "name": p["name"], "status": p["status"], "reason": not_served_reason(p)}
                               for p in every if not p.get("live")],
                "route": COMPONENT_ROUTES["products"]}
    if kind == "services":
        return {"available": ["Synthesis Studio", "Capital Fund", "Living Marketplace"], "route": COMPONENT_ROUTES["services"]}
    return {"status": "Unknown component"}


def _integrate_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Wraps a catalog product entry as a SELECTED BTO resource record (design-time, not wired)."""
    # W415 — this stamped every selected catalog slug "status": "INTEGRATED" with
    # "integration_mode": "Plug-in resource — accessible via Sovereign Mesh". No integration runs
    # here and nothing is made reachable: the function copies catalog fields into a dict. The
    # reachability sentence was the worst of it — it told the user the resource was live.
    return {
        "slug": product["slug"],
        "name": product["name"],
        "tier": product["tier"],
        "category": product["category"],
        "features": product.get("features", []),
        "route": product.get("route"),
        "status": "SELECTED (blueprint only)",
        "integrated": False,
        "integration_mode": "Not integrated by /bto/configure — POST /bto/build produces it for real.",
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


class BTOBuildRequest(BaseModel):
    entity_name: str = "Unnamed Entity"
    product_resources: List[str] = []   # catalog product slugs to build-to-order
    objective: str = ""
    domain: str = "enterprise"


@router.post("/build")
async def build_to_order(request: BTOBuildRequest):
    """Build-to-Order: take the configured catalog products and genuinely PRODUCE a deliverable for each via
    the §13 living-deliverables engine (QMS-gated, §8-metered) — turning a blueprint into REAL build-to-order
    output on Workstation's OWN engines, not just an 'INTEGRATED' descriptor. Closes the
    Catalogue → Build-to-Order → delivery path."""
    slug_index: Dict[str, Dict[str, Any]] = {p["slug"]: p for p in list_products()}
    asked = [slug_index[s] for s in request.product_resources if s in slug_index]
    selected = [p for p in asked if p.get("live")]
    objective = request.objective or f"Build-to-order delivery for {request.entity_name}"
    # W470 — a legacy archive or a source pointer is never built: it is answered as what it is
    built: List[Dict[str, Any]] = [{"slug": p["slug"], "name": p["name"], "status": "NOT_BUILT",
                                    "reason": not_served_reason(p)} for p in asked if not p.get("live")]
    if selected:
        from agentic_core.api.deliverables import produce, ProduceRequest
        for p in selected:
            try:
                brief = (f"Build-to-order the '{p['name']}' product (category {p.get('category', '')}, "
                         f"tier {p.get('tier', '')}) for «{request.entity_name}». Objective: {objective}. "
                         f"Realise these features: {', '.join((p.get('features') or [])[:8]) or 'core capabilities'}.")
                d = await produce(ProduceRequest(type="report", title=f"{p['name']} — Build-to-Order",
                                                 brief=brief, domain=request.domain))
                qms = ((d.get("quality_assurance") or {}).get("quality") or {}).get("qms_gate_passed") if isinstance(d, dict) else None
                # §5 (W494, FU-147) — "BUILT" was set whenever produce() did not raise, so a
                # floor-composed report scaffold with qms_gate_passed None counted as a built product
                # and the page showed a green BUILT chip. "did not raise" is not "was built". The
                # status now names what actually happened, and only a PASSED quality gate is BUILT.
                _status = ("BUILT" if qms is True else
                           "COMPOSED_GATE_FAILED" if qms is False else
                           "COMPOSED_NOT_ASSESSED")
                built.append({"slug": p["slug"], "name": p["name"],
                              "deliverable_id": d.get("id") if isinstance(d, dict) else None,
                              "qms_gate_passed": qms, "status": _status,
                              "status_basis": (
                                  "the living-QMS gate passed on this deliverable" if qms is True else
                                  "the living-QMS gate FAILED on this deliverable" if qms is False else
                                  "a document was composed and the living-QMS gate could not assess it "
                                  "(floor-served: the floor emits the requested headings, so coverage "
                                  "cannot be measured). Composed is not built.")})
            except Exception as e:
                built.append({"slug": p["slug"], "name": p["name"], "status": "FAILED", "error": str(e)[:160]})
    _built_n = sum(1 for b in built if b["status"] == "BUILT")
    # W494 (refutation) - startswith("COMPOSED") also matched COMPOSED_GATE_FAILED, so a product whose
    # quality gate FAILED was counted and printed as "composed, not assessed". A gate that ran and said
    # no is the opposite of a gate that could not say anything. Counted apart.
    _composed_n = sum(1 for b in built if b["status"] == "COMPOSED_NOT_ASSESSED")
    _gate_failed_n = sum(1 for b in built if b["status"] == "COMPOSED_GATE_FAILED")
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("motor", "bto.build",
                           f"Build-to-order: {_built_n} gate-passed, {_composed_n} composed but "
                           f"unassessed → {request.entity_name}", 0.7)
    except Exception:
        pass
    return {"entity_name": request.entity_name, "objective": objective, "domain": request.domain,
            "requested": request.product_resources, "built": built,
            # W494 (FU-147) — this counted every non-raising produce() call and was printed as
            # "Delivered N". It counts gate-passed products only, and the composed-but-unassessed
            # ones are counted separately rather than folded into a delivery figure.
            "delivered_count": _built_n,
            "composed_not_assessed_count": _composed_n,
            "gate_failed_count": _gate_failed_n,
            "delivered_basis": (
                f"{_built_n} product(s) passed the living-QMS gate; {_composed_n} had a document "
                "composed that the gate could not assess (floor-served); "
                f"{_gate_failed_n} had a document composed that the gate FAILED. Neither of the last "
                "two is a delivery, and they are not the same outcome"),
            "posture": "in-house-first",
            "note": ("Build-to-order via the §13 living-deliverables engine. A product counts as BUILT "
                     "only when the living-QMS gate PASSED on its deliverable; a composed document the "
                     "gate could not assess is reported as composed, not delivered.")}


@router.post("/configure")
async def configure_bto(request: BTOConfigureRequest):
    """Assemble a DESIGN blueprint for the requested components and catalog resources.

    W415 — nothing in this handler provisions, bootstraps, activates or integrates anything; it
    resolves catalog slugs and builds a dict. The per-component "Provisioned"/"Active"/"INTEGRATED"
    state assertions it used to return are now honest specification labels, and the response says
    plainly that it is a blueprint so a reader does not take it for a running system.
    """
    # Resolve requested product resources from the catalog
    all_products: List[Dict[str, Any]] = list_products()
    slug_index: Dict[str, Dict[str, Any]] = {p["slug"]: p for p in all_products}
    integrated = [
        _integrate_product(slug_index[slug])
        for slug in request.product_resources
        if slug in slug_index and slug_index[slug].get("live")        # W470 — served entries only
    ]
    not_buildable = [{"slug": slug, "name": slug_index[slug]["name"], "status": slug_index[slug]["status"],
                      "reason": not_served_reason(slug_index[slug])}
                     for slug in request.product_resources if slug in slug_index and not slug_index[slug].get("live")]

    blueprint = {
        "blueprint_id": str(uuid.uuid4()),
        "entity_name": request.entity_name,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "components": {kind: _build_component(kind) for kind in request.components},
        "product_resources": integrated,
        "not_buildable": not_buildable,
        "resource_count": len(integrated),
        "component_count": len(request.components),
        "provisioned": False,
        "note": ("Design blueprint only — this endpoint provisions, activates and integrates "
                 "nothing. POST /bto/build genuinely produces the selected products via the §13 "
                 "living-deliverables engine and reports BUILT/FAILED per item."),
    }
    return blueprint
