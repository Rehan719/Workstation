import json
import logging
import os

logger = logging.getLogger(__name__)

class UltraFineMapper:
    """
    ARTICLE 5.2: Ultra-Fine-Resolution Mapping.
    Synthesizes granular entity evolution from commits, URLs, and text artifacts.
    """
    def __init__(self):
        self.master_data = "docs/knowledge/forensic_master/civilization_master.json"
        self.commit_data = "docs/knowledge/commit_analysis_exhaustive.json"
        self.text_data = "docs/knowledge/background_text_extracts.json"

    def generate_ultra_map(self):
        logger.info("UltraMapper: Reconstructing bit-perfect entity evolution...")

        with open(self.master_data, "r") as f:
            master = json.load(f)
        with open(self.commit_data, "r") as f:
            commits = json.load(f)
        with open(self.text_data, "r") as f:
            text_artifacts = json.load(f)

        content = "# WORKSTATION ULTRA-FINE-RESOLUTION FEATURE MAP\n\n"

        entities = {
            "Identity & Orchestration": ["Entity IDBO", "VSB (BMS, QMS, DCS, EMS)"],
            "AI Governance & C-Suite": ["AI CEO Autonomy", "C-Suite Roles", "Tool Registry", "Memory Arch"],
            "Realms & Domains": ["Learning Realm", "Developer Forge", "Genome Realm", "Religion Domain", "Law Domain"],
            "Infrastructure & Tools": ["GSE Quad Engine", "UVAID/UVIAP", "Homeostatic Mesh", "libp2p Stack"],
            "Cognitive Pipelines": ["Ingestion", "Assimilation", "Introspection", "Retrospection"]
        }

        for category, items in entities.items():
            content += f"## {category}\n"
            for item in items:
                content += f"### {item}\n"
                content += "| Ver/Commit | Internal Component | Capability | Provenance | Status |\n"
                content += "|------------|-------------------|------------|------------|--------|\n"

                # 1. Map from Forensic Master
                for ver, data in master["versions"].items():
                    if any(item.lower().split()[0] in f.lower() for f in data["features"]):
                        content += f"| {ver} | System Core | Evolution | External URL | INTEGRATED |\n"

                # 2. Map from Commits
                for c in commits:
                    if item.lower().split()[0] in c["message"].lower():
                        content += f"| {c['hash'][:8]} | Fix/Module | {c['intent']} | {c['branches'][0] if c['branches'] else 'Git'} | ACTIVE |\n"

                # 3. Map from Text Artifacts
                for path, data in text_artifacts.items():
                    if any(item.lower().split()[0] in f.lower() for f in data["features"]):
                        file_name = os.path.basename(path)
                        content += f"| vDesign | Plan Feature | Implementation | {file_name} | PLANNED |\n"

                content += "\n"

        with open("FINE_RESOLUTION_FEATURE_MAP.md", "w") as f:
            f.write(content)

        logger.info("UltraMapper: FINE_RESOLUTION_FEATURE_MAP.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mapper = UltraFineMapper()
    mapper.generate_ultra_map()
