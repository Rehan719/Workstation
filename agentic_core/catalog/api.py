import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/catalog", tags=["Product Catalog"])

PRODUCTS_DIR = Path(__file__).resolve().parent.parent.parent / "products"

# Live route within the SuperApp for products that already have a dedicated page.
ROUTE_OVERRIDES: Dict[str, str] = {
    "capital_fund": "/capital",
    "digital_reactor": "/reactor",
    "enterprise-file-hub": "/text-index",
    "OctoVeritasEngine": "/constitution",
    "qep-sdk": "/qep-religion",
}

# W470 (P1.13, ledger R5.6) — the six 'Domain Signature Product' directories are legacy archives: a manifest
# that self-declares PRODUCTION_READY / WCAG 2.2 AAA / nine injection formats, served by no route. They
# used to route to the domain hubs, which presented the hub as the product. They are listed as what they
# are (status 'legacy'), never counted as live, and open nothing.
LEGACY_ARCHIVES = frozenset({"Care", "Education", "Employment", "Law", "Religion", "Science"})

# status — the one word the marketplace counts by:
#   live    a served surface in the SuperApp (route set);
#   source  a registered directory whose substance is a source pointer or metadata only — nothing served;
#   legacy  an archived signature-product directory (see LEGACY_ARCHIVES).
STATUS_LIVE, STATUS_SOURCE, STATUS_LEGACY = "live", "source", "legacy"


def _status(slug: str, route: Any) -> str:
    if slug in LEGACY_ARCHIVES:
        return STATUS_LEGACY
    return STATUS_LIVE if route else STATUS_SOURCE

# Descriptive metadata for product directories that don't ship a metadata.json
# (platform-level products and domain signature-product directories).
CATALOG_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "capital_fund": {
        "name": "Sovereign Capital Fund",
        "tier": "Enterprise",
        "category": "Platform",
        "features": ["Autonomous Rebalancing", "On-Chain Gateway", "Constitutional Evolution Voting"],
    },
    "enterprise-file-hub": {
        "name": "Enterprise File Hub",
        "tier": "Enterprise",
        "category": "Platform",
        "features": ["Agentic Document Pipelines", "CLI Ingestion", "Federated Storage"],
    },
    "mjm-intelligence-engine": {
        "name": "MJM Intelligence Engine",
        "tier": "Enterprise+",
        "category": "Platform",
        "features": ["Mushahida / Jaiza / Muaina Learning Loop", "Genomic Domain Configuration", "Governed Self-Evolution"],
    },
    "OctoVeritasEngine": {
        "name": "OctoVeritas Engine",
        "tier": "Enterprise+",
        "category": "Platform",
        "features": ["Constitutional Compliance Checking", "C-Suite Coordination", "Quad-Engine Bridge"],
    },
    "qep-sdk": {
        "name": "QEP-as-a-Service SDK",
        "tier": "Standard/Pro/Enterprise",
        "category": "Domain (Quran Education Platform)",
        "features": ["Arabic Morphology Analysis", "AI Quiz Generation", "Scholarly Annotation Trust Scoring"],
    },
    "signature-product-suite": {
        "name": "Signature Product Suite",
        "tier": "Enterprise",
        "category": "Platform",
        "features": ["Zero-Placeholder Certification Pipeline", "Cross-Domain Packaging", "Constitutional Validation Gates"],
    },
    "Care": {
        "name": "Care Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-CARE directory — not a served product"],
    },
    "Education": {
        "name": "Education Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-EDU directory — not a served product"],
    },
    "Employment": {
        "name": "Employment Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-EMP directory — not a served product"],
    },
    "Law": {
        "name": "Law Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-LAW directory — not a served product"],
    },
    "Religion": {
        "name": "Religion Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-REL directory — not a served product"],
    },
    "Science": {
        "name": "Science Domain Signature Product",
        "tier": "Legacy",
        "category": "Legacy archive",
        "features": ["Archived VSB-SIG-SCI directory — not a served product"],
    },
}


def _load_product(slug: str, path: Path) -> Dict[str, Any]:
    metadata_file = path / "metadata.json"
    if metadata_file.exists():
        try:
            data = json.loads(metadata_file.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Failed to parse metadata.json for %s: %s", slug, e)
            data = {}
        route = ROUTE_OVERRIDES.get(slug)
        return {
            "slug": slug,
            "name": data.get("name", slug),
            "tier": data.get("tier", "Standard"),
            "category": "SDK",
            "features": data.get("features", []),
            "source": data.get("source"),
            "route": route,
            "status": _status(slug, route),
            "live": bool(route) and slug not in LEGACY_ARCHIVES,
        }

    override = CATALOG_OVERRIDES.get(slug, {})
    route = None if slug in LEGACY_ARCHIVES else ROUTE_OVERRIDES.get(slug)
    return {
        "slug": slug,
        "name": override.get("name", slug),
        "tier": override.get("tier", "Standard"),
        "category": override.get("category", "Platform"),   # the six legacy overrides say "Legacy archive"
        "features": override.get("features", []),
        "source": None,
        "route": route,
        "status": _status(slug, route),
        "live": bool(route),
    }


def list_products() -> List[Dict[str, Any]]:
    if not PRODUCTS_DIR.exists():
        return []
    return [
        _load_product(entry.name, entry)
        for entry in sorted(PRODUCTS_DIR.iterdir())
        if entry.is_dir() and not entry.name.startswith((".", "_"))  # skip __pycache__/dotdirs (not products)
    ]


def catalogue_counts(products: List[Dict[str, Any]]) -> Dict[str, int]:
    """W470 — the honest header numbers: live is only what a route serves."""
    return {
        "registered": len(products),
        "live": sum(1 for p in products if p.get("status") == STATUS_LIVE),
        "source": sum(1 for p in products if p.get("status") == STATUS_SOURCE),
        "legacy": sum(1 for p in products if p.get("status") == STATUS_LEGACY),
    }


def served_products() -> List[Dict[str, Any]]:
    """W470 (refutation) — the ONLY list a consumer may seed, build, rank or deliver from: the entries a route
    serves. The catalogue lists a legacy archive or a source pointer as what it is; it never hands one on as
    a product (Build-to-Order used to report a legacy archive BUILT, the marketplace seeded it as a tradeable
    listing, the resource fabric ranked it)."""
    return [p for p in list_products() if p.get("live")]


def not_served_reason(product: Dict[str, Any]) -> str:
    return {STATUS_LEGACY: "legacy archive — not a served product",
            STATUS_SOURCE: "source pointer — nothing served yet"}.get(str(product.get("status")), "not a served product")


@router.get("/products")
async def get_catalog():
    products = list_products()
    # W470 — `count` is registered directories; `counts` says how many a route actually serves
    return {"products": products, "count": len(products), "counts": catalogue_counts(products)}
