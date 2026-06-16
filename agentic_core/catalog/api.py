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
    "Care": "/care",
    "Education": "/education",
    "Employment": "/employment",
    "Law": "/law",
    "Religion": "/qep-religion",
    "Science": "/science",
}

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
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-CARE Series"],
    },
    "Education": {
        "name": "Education Domain Signature Product",
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-EDU Series"],
    },
    "Employment": {
        "name": "Employment Domain Signature Product",
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-EMP Series"],
    },
    "Law": {
        "name": "Law Domain Signature Product",
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-LAW Series"],
    },
    "Religion": {
        "name": "Religion Domain Signature Product",
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-REL Series"],
    },
    "Science": {
        "name": "Science Domain Signature Product",
        "tier": "Domain",
        "category": "Domain",
        "features": ["VSB-SIG-SCI Series"],
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
        return {
            "slug": slug,
            "name": data.get("name", slug),
            "tier": data.get("tier", "Standard"),
            "category": "SDK",
            "features": data.get("features", []),
            "source": data.get("source"),
            "route": ROUTE_OVERRIDES.get(slug),
        }

    override = CATALOG_OVERRIDES.get(slug, {})
    return {
        "slug": slug,
        "name": override.get("name", slug),
        "tier": override.get("tier", "Standard"),
        "category": override.get("category", "Platform"),
        "features": override.get("features", []),
        "source": None,
        "route": ROUTE_OVERRIDES.get(slug),
    }


def list_products() -> List[Dict[str, Any]]:
    if not PRODUCTS_DIR.exists():
        return []
    return [
        _load_product(entry.name, entry)
        for entry in sorted(PRODUCTS_DIR.iterdir())
        if entry.is_dir()
    ]


@router.get("/products")
async def get_catalog():
    products = list_products()
    return {"products": products, "count": len(products)}
