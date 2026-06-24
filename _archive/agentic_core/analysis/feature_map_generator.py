import json
import logging
import os

logger = logging.getLogger(__name__)

class FeatureMapGenerator:
    """
    ARTICLE 5.2: Fine-Resolution Mapping Pipeline.
    Synthesizes entity evolution from forensic JSON records.
    """
    def __init__(self):
        self.master_data = "docs/knowledge/forensic_master/civilization_master.json"
        self.commit_data = "docs/knowledge/commit_analysis_raw.json"

    def generate_map(self):
        logger.info("FeatureMapper: Reconstructing granular entity evolution...")

        with open(self.master_data, "r") as f:
            master = json.load(f)
        with open(self.commit_data, "r") as f:
            commits = json.load(f)

        content = "# WORKSTATION FINE-RESOLUTION FEATURE MAP\n\n"

        entities = {
            "Identity & Orchestration": ["Entity IDBO", "VSB (BMS, QMS, DCS, EMS)"],
            "AI Governance & C-Suite": ["AI CEO Autonomy", "C-Suite Roles", "Tool Registry"],
            "Realms & Domains": ["Learning Realm", "Developer Forge", "Genome Realm", "Religion Domain"],
            "Infrastructure & Tools": ["GSE Quad Engine", "UVAID/UVIAP", "Homeostatic Mesh"]
        }

        for category, items in entities.items():
            content += f"## {category}\n"
            for item in items:
                content += f"### {item}\n"
                content += "| Version/Commit | Sub-component | Capability | Provenance | Status |\n"
                content += "|----------------|---------------|------------|------------|--------|\n"

                # Sample entries derived from forensic master
                for ver, data in master["versions"].items():
                    if any(item.lower() in f.lower() for f in data["features"]):
                        content += f"| {ver} | Core Module | System Execution | External URL | INTEGRATED |\n"

                # Check commits for the entity
                for c in commits:
                    if item.lower().split()[0] in c["message"].lower():
                        content += f"| {c['hash'][:8]} | Fix/Patch | {c['inferred_intent']} | Git Commit | ACTIVE |\n"

                content += "\n"

        with open("FINE_RESOLUTION_FEATURE_MAP.md", "w") as f:
            f.write(content)

        logger.info("FeatureMapper: FINE_RESOLUTION_FEATURE_MAP.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mapper = FeatureMapGenerator()
    mapper.generate_map()
