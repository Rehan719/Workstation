import json
import os
import shutil
import hashlib
from datetime import datetime, timezone

class ArchiveManager:
    """
    Superseded Run and Retention Management System for Quran Education Platform
    Domain: RELIGION::QEP::GOVERNANCE
    """
    def __init__(self, archive_base="archive/Religion/QuranEducation/superseded"):
        self.archive_base = archive_base
        self.retention_period = 90  # days
        os.makedirs(self.archive_base, exist_ok=True)

    def supersede_curriculum(self, version, source_dir):
        """Archives a curriculum version and marks it as superseded"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        target_dir = os.path.join(self.archive_base, "curriculum", f"v{version}_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)

        # Copy source contents to archive
        if os.path.exists(source_dir):
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(target_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

        # Create metadata
        metadata = {
            "version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reason": "PLATFORM_UPGRADE_v8.0",
            "retention_expires": (datetime.now(timezone.utc).timestamp() + (self.retention_period * 86400)),
            "hash_verification": self._generate_dir_hash(target_dir)
        }
        with open(os.path.join(target_dir, "archive_metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Archived Curriculum v{version} to {target_dir}")
        return target_dir

    def _generate_dir_hash(self, directory):
        """Generates a SHA-256 hash for all files in a directory"""
        hashes = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                with open(filepath, "rb") as f:
                    hashes.append(hashlib.sha256(f.read()).hexdigest())
        return hashlib.sha256("".join(sorted(hashes)).encode()).hexdigest()

if __name__ == "__main__":
    manager = ArchiveManager()
    manager.supersede_curriculum("7.0", "outputs/Religion/release_v7.0")
