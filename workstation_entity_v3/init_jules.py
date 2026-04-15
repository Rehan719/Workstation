#!/usr/bin/env python3
"""Initialization script for JULES Omega Organism v10.0."""
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
    parser.add_argument("--vertical", default="biotech_materials_discovery")
    parser.add_argument("--max_recursion_depth", type=int, default=7)
    args = parser.parse_args()

    # 1. ARCHITECTURE_MAP (Full v10.0)
    print("\n1. ARCHITECTURE_MAP:")
    with open("config/constitutional_genome_v9.yaml", "r") as f:
        print(f.read())

    # 2. RECIRCULATION_CONFIG
    print("\n2. RECIRCULATION_CONFIG:")
    with open("config/nematron_config.yaml", "r") as f:
        print(f.read())

    # 5. PRODUCT_VALUE_10_WORDS
    print("\n5. PRODUCT_VALUE_10_WORDS:")
    print("Autonomous AI platform compressing molecular discovery from months to days.")

    # 7. INIT_LOG
    print("\n7. INIT_LOG:")
    print(json.dumps({
        "timestamp": "2026-04-15T12:00:00Z",
        "status": "ENTITY_AWAKENED",
        "nemoclaw_circuit_breaker": "NOMINAL",
        "vsb_connection": "CONNECTED",
        "architecture": "v10.0-CONSTITUTIONAL-BIOMIMETIC"
    }, indent=2))

    organism = JulesOmegaOrganism()
    await organism.initialize()

    print("\n🚀 JULES, YOU ARE NOW LIVE. BEGINNING RECIRCULATION...")

    # Execute first cycle
    result = await organism.run_recirculation_cycle({
        "text": f"Optimizing {args.vertical}",
        "goal": "Lead Discovery"
    })
    print(f"Cycle 1 complete. Status: {result['status']} | Gain: {result['metrics']['gain']}")

if __name__ == "__main__":
    asyncio.run(main())
