import hashlib
import zipfile
import json
import os
from pathlib import Path
from datetime import datetime

class TribunalBundleGenerator:
    """
    Creates an immutable ZIP package for tribunal submission.
    Includes full cryptographic manifest and audit trails.
    """
    def generate(self, case_id: str, documents: list, audit_trail: list, output_dir: str = "data/organism/bundles"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TRIBUNAL_BUNDLE_{case_id}_{timestamp}.zip"
        os.makedirs(output_dir, exist_ok=True)
        output_path = Path(output_dir) / filename

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as bundle:
            # 1. Add Legal Documents
            for doc in documents:
                bundle.writestr(f"documents/{doc['name']}", doc['content'])

            # 2. Add AI Audit Trail
            audit_json = "\n".join([json.dumps(e) for e in audit_trail])
            bundle.writestr("audit/sovereign_audit.jsonl", audit_json)

            # 3. Generate SHA-256 Manifest
            manifest = []
            for name in bundle.namelist():
                # Read content from the zip to hash it correctly
                with bundle.open(name) as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                manifest.append(f"{file_hash}  {name}")

            bundle.writestr("MANIFEST.sha256", "\n".join(manifest))

            # 4. Add Verification README
            readme = (
                f"Sovereign Digital Organism - Evidence Package\n"
                f"Case: {case_id}\n"
                f"Timestamp: {timestamp}\n\n"
                "To verify the integrity of this bundle, run:\n"
                "sha256sum -c MANIFEST.sha256"
            )
            bundle.writestr("README.txt", readme)

        print(f"Bundle successfully packaged: {output_path}")
        return str(output_path)
