import os
import shutil
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def package_products():
    """
    ARTICLE 536-540: Packaging UVIAP, GSE, and Scraping Suite as commercial products.
    Focus on technical isolation, enterprise documentation, and feature toggles.
    """
    products = {
        "uviap": {
            "name": "Unified Version Ingestion & Assimilation Pipeline",
            "source": "agentic_core/synthesis/uviap.py",
            "tier": "Enterprise",
            "features": ["GitHub Deep Analysis", "Biomimetic Pattern Recognition", "Self-Evolution Logic"]
        },
        "gse": {
            "name": "Grand Synthesis Engine",
            "source": "agentic_core/synthesis/grand_synthesis_engine.py",
            "tier": "Enterprise+",
            "features": ["Cross-Version Synthesis", "Constitutional Generation", "Audit Automation"]
        },
        "scraping_suite": {
            "name": "Dual-Mode Sensory Scraper",
            "source": "agentic_core/synthesis/dual_mode_scraper.py",
            "tier": "Standard/Pro",
            "features": ["Passive Sensory Mode", "Active Swarm Missions", "Reasoning Gate (WST)"]
        },
        "business_incubator": {
            "name": "Co-Evolutionary Business Incubator",
            "source": "agentic_core/incubation/business_incubator.py",
            "tier": "Enterprise",
            "features": ["Strategic Foresight", "Constitutional Vetting", "Co-Evolutionary Simulation"]
        },
        "digital_reactor": {
            "name": "Digital Reactor (Simulation-as-a-Service)",
            "source": "agentic_core/simulation/engine.py",
            "tier": "Standard/Pro/Enterprise",
            "features": ["High-Fidelity Twinning", "ABM/Physics Simulation", "Synthetic Data Generation"]
        },
        "molecular_sdk": {
            "name": "Molecular Communication SDK",
            "source": "agentic_core/biochemical/molecular_comm.py",
            "tier": "Enterprise",
            "features": ["Neurotransmitter Signaling", "Emotional Interfacing", "Trust Modulation"]
        },
        "nanophotonic_navigation": {
            "name": "Neuromorphic Nanophotonic Navigator",
            "source": "agentic_core/simulation/nanophotonics.py",
            "tier": "Enterprise+",
            "features": ["Polarised-Light Sensing", "Ultra-Low Power Navigation", "Insect-Inspired AI"]
        },
        "cognitive_scraper": {
            "name": "Cognitive Computing Scraper SDK",
            "source": "agentic_core/synthesis/cognitive_scraper.py",
            "tier": "Enterprise",
            "features": ["Frontier AI Ingestion", "Concept Graph Mapping", "Temporal Trend Analysis"]
        },
        "asymmetric_drive": {
            "name": "Asymmetric-Drive Rectification SDK",
            "source": "agentic_core/biochemical/rectification_engine.py",
            "tier": "Enterprise+",
            "features": ["Topological Ratchets", "Residual Cost Accounting", "Structural Memory"]
        },
        "synaptic_circuits": {
            "name": "Synaptic Circuit SDK",
            "source": "agentic_core/simulation/synaptic_circuits.py",
            "tier": "Enterprise+",
            "features": ["Near-Sensor Computing", "Memristor Simulation", "Low-Latency Perception"]
        }
    }

    base_dir = "products"
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs("docs/commercial", exist_ok=True)

    # Shared dependencies to copy
    shared_deps = [
        "agentic_core/ueg/ueg_manager.py",
        "agentic_core/genetics/genomic_registry.py",
        "agentic_core/governance/runtime_framework.py"
    ]

    # Explicit adjacent dependencies for standalone reactors/simulators
    adjacent_deps = {
        "digital_reactor": [
            "agentic_core/simulation/registry.py",
            "agentic_core/simulation/physics.py",
            "agentic_core/simulation/abm.py",
            "agentic_core/simulation/lifecycle.py",
            "agentic_core/simulation/fidelity.py"
        ],
        "scraping_suite": [
            "agentic_core/synthesis/agentic_orchestrator.py",
            "agentic_core/synthesis/insight_extractor.py",
            "agentic_core/synthesis/knowledge_synthesis.py",
            "agentic_core/simulation/nanophotonics.py",
            "agentic_core/biochemical/molecular_comm.py",
            "agentic_core/synthesis/cognitive_scraper.py"
        ],
        "molecular_sdk": [
            "agentic_core/biochemical/rectification_engine.py"
        ],
        "synaptic_circuits": [
            "agentic_core/biochemical/molecular_comm.py"
        ]
    }

    for name, config in products.items():
        product_dir = os.path.join(base_dir, name)
        os.makedirs(product_dir, exist_ok=True)

        # 1. Technical Isolation (Source & Toggles)
        sdk_dir = os.path.join(product_dir, "sdk")
        os.makedirs(sdk_dir, exist_ok=True)

        # Copy main source
        dest_src = os.path.join(sdk_dir, os.path.basename(config["source"]))
        if os.path.exists(config["source"]):
            shutil.copy(config["source"], dest_src)
            logger.info(f"Packaged {name} source: {config['source']} -> {dest_src}")

        # Copy dependencies for standalone functionality
        for dep in shared_deps:
            if os.path.exists(dep):
                dep_dest = os.path.join(sdk_dir, os.path.basename(dep))
                shutil.copy(dep, dep_dest)

        # Copy adjacent dependencies
        if name in adjacent_deps:
            for dep in adjacent_deps[name]:
                if os.path.exists(dep):
                    dep_dest = os.path.join(sdk_dir, os.path.basename(dep))
                    shutil.copy(dep, dep_dest)

        # 2. Dockerization
        with open(os.path.join(product_dir, "Dockerfile"), "w") as f:
            f.write(f"""FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install
ENV APP_MODE=COMMERCIAL
ENV FEATURE_TOGGLE_ENTERPRISE=true
CMD ["python", "sdk/{os.path.basename(config['source'])}"]
""")

        # 3. Enterprise Documentation
        doc_path = f"docs/commercial/{name}_enterprise_guide.md"
        with open(doc_path, "w") as f:
            f.write(f"# {config['name']} - Enterprise Guide\n\n")
            f.write(f"**Tier:** {config['tier']}\n\n")
            f.write("## Features\n")
            for feat in config["features"]:
                f.write(f"- {feat}\n")
            f.write("\n## Enterprise Configuration\n")
            f.write("Enable high-scale features by setting `FEATURE_TOGGLE_ENTERPRISE=true`.\n")
            f.write("\n## Deployment\nUse the provided Dockerfile for isolated deployment.")

        # 4. Product Metadata (Catalog)
        with open(os.path.join(product_dir, "metadata.json"), "w") as f:
            json.dump(config, f, indent=4)

    # Master Catalog
    with open("docs/commercial/product_catalog.md", "w") as f:
        f.write("# Jules AI Commercial Product Catalog\n\n")
        f.write("| Product | Tier | Features |\n|---|---|---|\n")
        for name, config in products.items():
            f.write(f"| {config['name']} | {config['tier']} | {', '.join(config['features'])} |\n")

    logger.info("All commercial products packaged and documented successfully.")

if __name__ == "__main__":
    package_products()
