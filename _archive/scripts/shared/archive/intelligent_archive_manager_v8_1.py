import json
import os
import hashlib
from datetime import datetime, timezone

class IntelligentArchiveManagerV81:
    """
    Reusable archive system for VSB signature products with pipeline awareness.
    Handles versioning, diffing, rollback, compliance tracking, and pipeline metadata.
    Domain: SHARED::ARCHIVE
    """

    def __init__(self, archive_base="archive/qep-v8.1-sovereign-signature"):
        self.archive_base = archive_base
        os.makedirs(self.archive_base, exist_ok=True)

    def archive_version_with_pipelines(self, product_id: str, version: str, artifacts: dict, pipeline_metadata: dict):
        """Archive a product version with full metadata and pipeline tracing."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(self.archive_base, "superseded", "curriculum", f"v{version}_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)

        # Save artifacts (simulated)
        with open(os.path.join(target_dir, "manifest.json"), "w") as f:
            json.dump({
                "product_id": product_id,
                "version": version,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "artifacts": artifacts,
                "pipeline_metadata": pipeline_metadata
            }, f, indent=2)

        print(f"Signature Archive Created: {product_id} v{version} at {target_dir}")
        return target_dir

    def create_vsb_snapshot(self, modules, reason):
        """Standard VSB snapshot for content changes."""
        print(f"Creating VSB Snapshot for {len(modules)} modules. Reason: {reason}")
        return f"SNAP-{hashlib.md5(reason.encode()).hexdigest()[:8]}"
