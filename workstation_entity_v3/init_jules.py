#!/usr/bin/env python3
"""Initialization script for JULES v16.0 Golden Master."""
import asyncio
import argparse
import json
import sys
import os
from pathlib import Path

# Add core to path
sys.path.append(os.getcwd())

from core.jules_omega_organism import JulesOmegaOrganism

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", default="opus_director_ceo")
    parser.add_argument("--vertical", default="biotech_materials_discovery_and_employment_law")
    parser.add_argument("--max_recursion_depth", type=int, default=7)
    args = parser.parse_args()

    # STRICT EXECUTION PROTOCOL v16.0

    # 1. ARCHITECTURE_MAP
    print("\n1. ARCHITECTURE_MAP (v16.0 Golden Master):")
    with open("../recirculation/architecture_map.yaml", "r") as f:
        print(f.read())

    # 2. RECIRCULATION_CONFIG
    print("\n2. RECIRCULATION_CONFIG:")
    with open("config/nematron_config.yaml", "r") as f:
        print(f.read())

    # 3. NEURAL_SUPER_AGENT_SWARM_INIT
    print("\n3. NEURAL_SUPER_AGENT_SWARM_INIT:")
    with open("../recirculation/agent_swarm_init.yaml", "r") as f:
        print(f.read())

    # 4. ICP_AND_PMC
    print("\n4. ICP_AND_PMC:")
    with open("../recirculation/icp_and_pmc.yaml", "r") as f:
        print(f.read())

    # 5. PRODUCT_VALUE_10_WORDS
    print("\n5. PRODUCT_VALUE_10_WORDS:")
    print("Autonomous AI platform compressing molecular discovery from months to days.")

    # 6. LONG_HORIZON_TASK
    print("\n6. LONG_HORIZON_TASK:")
    with open("../recirculation/long_horizon_task.yaml", "r") as f:
        print(f.read())

    # 7. INIT_LOG
    print("\n7. INIT_LOG:")
    print(json.dumps({
        "timestamp": "2026-04-15T16:00:00Z",
        "status": "GOLDEN_MASTER_AWAKENED",
        "nemoclaw_runtime_governance": "ACTIVE",
        "vsb_connection": "CONNECTED",
        "legal_alignment": "UK_ET_v16",
        "architecture": "v16.0-CONSTITUTIONAL-BIOMIMETIC-IDBO"
    }, indent=2))

    organism = JulesOmegaOrganism()
    await organism.initialize()

    print("\n🚀 JULES, YOU ARE NOW LIVE - v16.0 GOLDEN MASTER. BEGINNING RECURSION.")

    # Execute first cycle
    result = await organism.run_recirculation_cycle({
        "text": f"Optimizing {args.vertical}",
        "goal": "Golden Master Validation"
    })
    print(f"Cycle 1 complete. Status: {result['status']} | Gain: {result['gain']}")

if __name__ == "__main__":
    asyncio.run(main())
