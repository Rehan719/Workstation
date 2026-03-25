import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class FeatureMapper:
    """
    ULTIMATE FEATURE MAPPING PIPELINE.
    Builds a unified matrix from Git history and external URLs.
    """
    def __init__(self):
        self.git_data = "docs/knowledge/git_forensic_analysis.json"
        self.url_data = "docs/knowledge/url_forensic_data.json"
        self.output_path = "docs/knowledge/feature_matrix_v0.json"

    def map_features(self):
        logger.info("FeatureMapper: Generating unified feature matrix...")

        with open(self.git_data, "r") as f:
            git_commits = json.load(f)
        with open(self.url_data, "r") as f:
            url_versions = json.load(f)

        matrix = {}

        # 1. Map from Git History
        for commit in git_commits:
            ver = commit["inferred_version"]
            if ver not in matrix: matrix[ver] = []
            # Extract features from commit message and files
            if "web" in str(commit["files_changed"]): matrix[ver].append("Web UI Update")
            if "agentic" in commit["message"].lower(): matrix[ver].append("Agentic Core Enhancement")

        # 2. Map from URL Sources
        for src in url_versions:
            ver = src["version"]
            if ver not in matrix: matrix[ver] = []
            matrix[ver].extend(src["features"])

        # Deduplicate
        for ver in matrix:
            matrix[ver] = list(set(matrix[ver]))

        with open(self.output_path, "w") as f:
            json.dump(matrix, f, indent=2)
        logger.info("FeatureMapper: Matrix generation complete.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mapper = FeatureMapper()
    mapper.map_features()
