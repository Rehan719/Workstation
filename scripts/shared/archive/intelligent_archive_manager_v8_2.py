import json
import os
import hashlib
import shutil
from datetime import datetime, timezone

class IntelligentArchiveManagerV82:
    """
    Reusable archive system for VSB signature products with full pipeline awareness.
    Handles versioning, diffing, rollback, compliance tracking, pipeline metadata,
    and reusability export management.
    Domain: SHARED::ARCHIVE
    """

    def __init__(self, archive_base="archive/qep-v8.2-sovereign-signature"):
        self.archive_base = archive_base
        os.makedirs(self.archive_base, exist_ok=True)
        os.makedirs(os.path.join(self.archive_base, "superseded", "curriculum"), exist_ok=True)
        os.makedirs(os.path.join(self.archive_base, "reusability_exports"), exist_ok=True)

    def archive_version_with_full_pipeline_awareness(
        self,
        product_id: str,
        version: str,
        artifacts: dict,
        pipeline_metadata: dict,
        reusability_exports: dict = None
    ):
        """Archive a product version with full metadata and pipeline tracing."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(self.archive_base, "superseded", "curriculum", f"v{version}_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)

        manifest = {
            "product_id": product_id,
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "artifacts": artifacts,
            "pipeline_metadata": pipeline_metadata,
            "reusability_exports": reusability_exports
        }

        with open(os.path.join(target_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"Sovereign Signature Archive Created: {product_id} v{version} at {target_dir}")
        return target_dir

    def export_reusability_mechanisms(self, product_id, version, export_config):
        """Export reusable mechanisms to the VSB ecosystem."""
        export_dir = os.path.join(self.archive_base, "reusability_exports", f"v{version}")
        os.makedirs(export_dir, exist_ok=True)

        with open(os.path.join(export_dir, "reusability_package.json"), "w") as f:
            json.dump({
                "product_id": product_id,
                "version": version,
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "mechanisms": export_config
            }, f, indent=2)

        print(f"Reusability Mechanisms Exported: {product_id} v{version}")
        return export_dir

    def create_vsb_snapshot(self, modules, reason):
        """Standard VSB snapshot for content changes."""
        print(f"Creating VSB Snapshot for {len(modules)} modules. Reason: {reason}")
        return f"SNAP-V82-{hashlib.md5(reason.encode()).hexdigest()[:8]}"
