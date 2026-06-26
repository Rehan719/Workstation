from agentic_core.domains.religion.product_v3 import ReligionProductV3
from agentic_core.domains.science.product_v4 import ScienceProductV4
from agentic_core.domains.law.product_v4 import LawProductV4
from agentic_core.domains.employment.product_v3 import EmploymentProductV3
from agentic_core.domains.education.product_v3 import EducationProductV3
from agentic_core.domains.care.product_v3 import CareProductV3
import json
import os

# For v4, we wrap existing v3 products to make them v4 compatible if they don't have a v4 yet
# but for MVP we focus on Law and Science as pilot v4 domains

def generate_v4_series():
    manifest = {
        "series": "Veritas Signature Products v4.0",
        "release_date": "2026-04-11",
        "engine": "OctoVeritasEngine v4.0",
        "workstation_integrated": true,
        "biomimetic_enabled": true,
        "constitutional_enforcement": "P0",
        "products": []
    }

    # Pilot V4 Domains
    v4_products = [
        ScienceProductV4(),
        LawProductV4()
    ]

    for p in v4_products:
        print(f"Generating sovereign v4 package for {p.domain}...")
        res_files = p.produce_package({"claimant": "Sovereign Entity"}, bto_config={"default_mode": "synthesis"})
        manifest["products"].append({
            "domain": p.domain,
            "version": "4.0",
            "status": "SUCCESS",
            "files": res_files
        })

    with open("products/VeritasSeriesManifest_v4.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("Veritas Series v4.0 generation complete.")

if __name__ == "__main__":
    generate_v4_series()
