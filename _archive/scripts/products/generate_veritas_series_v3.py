from agentic_core.domains.religion.product_v3 import ReligionProductV3
from agentic_core.domains.science.product_v3 import ScienceProductV3
from agentic_core.domains.law.product_v3 import LawProductV3
from agentic_core.domains.employment.product_v3 import EmploymentProductV3
from agentic_core.domains.education.product_v3 import EducationProductV3
from agentic_core.domains.care.product_v3 import CareProductV3
import json
import os

def generate_v3_series():
    products = [
        ReligionProductV3(),
        ScienceProductV3(),
        LawProductV3(),
        EmploymentProductV3(),
        EducationProductV3(),
        CareProductV3()
    ]

    manifest = {
        "series": "Veritas Signature Products v3.0",
        "release_date": "2026-04-11",
        "engine": "OctoVeritasEngine v3.0",
        "products": []
    }

    for p in products:
        print(f"Generating v3 package for {p.domain}...")
        res = p.produce_package({"topic": "v3 rollout"})
        manifest["products"].append({
            "domain": p.domain,
            "status": res["status"],
            "mode": res.get("mode"),
            "files": res.get("files", [])
        })

    with open("products/VeritasSeriesManifest_v3.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("Veritas Series v3.0 generation complete.")

if __name__ == "__main__":
    generate_v3_series()
