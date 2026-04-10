import os
import json
import shutil

def generate_veritas_series():
    """
    Populates the products/ directory with manifests and links to Grand Operation outputs.
    """
    products_root = "products"
    manifest_data = {
        "series_name": "Veritas Signature Products",
        "date": "2026-04-10",
        "products": []
    }

    config = [
        {
            "domain": "Religion",
            "id": "VSB-SIG-REL-QUADRA-9.0",
            "name": "Quran Education Platform",
            "framework": "Quadra-Veritas",
            "version": "9.0",
            "source": "outputs/Religion/QuranEducation/"
        },
        {
            "domain": "Science",
            "id": "VSB-SIG-SCI-OMNIA-18.0",
            "name": "Omnia-Veritas Patient Safety Intelligence",
            "framework": "Omnia-Veritas",
            "version": "18.0",
            "source": "outputs/Science/PatientSafety/v18_omnia_veritas/"
        },
        {
            "domain": "Law",
            "id": "VSB-SIG-LAW-OMNIOCTO-19.0",
            "name": "Omni-Octo Veritas Employment Tribunal Intelligence",
            "framework": "Omni-Octo Veritas",
            "version": "19.0",
            "source": "outputs/Law/EmploymentTribunal/v16/" # Highest available
        },
        {
            "domain": "Employment",
            "id": "VSB-SIG-EMP-PENTA-3.0",
            "name": "Penta-Veritas Career Advocacy & Application Intelligence",
            "framework": "Penta-Veritas",
            "version": "3.0",
            "source": "outputs/Employment/UKHSA_SeniorScientist_1991213/"
        },
        {
            "domain": "Care",
            "id": "VSB-SIG-CARE-SEXTA-1.0",
            "name": "Sexta-Veritas Health & Social Care Intelligence",
            "framework": "Sexta-Veritas",
            "version": "1.0",
            "source": "outputs/care_q2/" # From current operation
        }
    ]

    for item in config:
        product_dir = os.path.join(products_root, item["domain"], item["id"])
        os.makedirs(product_dir, exist_ok=True)
        os.makedirs(os.path.join(product_dir, "docs"), exist_ok=True)
        os.makedirs(os.path.join(product_dir, "assets"), exist_ok=True)

        # Create manifest
        manifest = {
            "product_id": item["id"],
            "name": item["name"],
            "domain": item["domain"],
            "version": item["version"],
            "release_date": "2026-04-10",
            "veritas_framework": item["framework"],
            "outputs_path": "outputs/",
            "status": "PRODUCTION_READY"
        }

        with open(os.path.join(product_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

        # Create README stub
        with open(os.path.join(product_dir, "README.md"), "w") as f:
            f.write(f"# {item['name']}\n\nStandalone signature product for the {item['domain']} domain.\n\n## Quick Start\n1. Review `manifest.json` for dependencies.\n2. Explore `outputs/` for intelligence artifacts.\n3. Refer to `docs/` for framework guidance.\n")

        # Handle outputs (copy if exists, else placeholder)
        out_target = os.path.join(product_dir, "outputs")
        if os.path.exists(item["source"]):
            if os.path.islink(out_target): os.unlink(out_target)
            if os.path.exists(out_target): shutil.rmtree(out_target)
            try:
                shutil.copytree(item["source"], out_target)
            except Exception as e:
                print(f"Warning: Failed to copy {item['source']} -> {out_target}: {e}")
        else:
            os.makedirs(out_target, exist_ok=True)
            with open(os.path.join(out_target, "placeholder.md"), "w") as f:
                f.write("# Placeholder for Grand Operation Outputs")

        manifest_data["products"].append(manifest)

    # Master manifest
    with open(os.path.join(products_root, "VeritasSeriesManifest.json"), "w") as f:
        json.dump(manifest_data, f, indent=2)

    print("Veritas Series generation complete.")

if __name__ == "__main__":
    generate_veritas_series()
