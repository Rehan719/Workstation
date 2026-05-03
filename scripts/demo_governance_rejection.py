import asyncio
import json
import os
import sys
from datetime import datetime

# Add root to path for imports
sys.path.append(os.getcwd())

from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    StrategicIntent, IntentGenerated, GovernanceValidated, ValidationResult
)
from src.organism.python.core.governance import SovereignIdentity, SovereignAuditLog
from src.organism.python.organs.nemoclaw_adapter import NemoclawAdapter
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.genetic_immune.immune_system import ImmuneSystemV2

async def run_demo():
    print("--- 🛡️ Sovereign Governance Rejection Demo ---")

    # 1. Setup Infrastructure
    bus = AsyncEventBus()
    await bus.start()

    identity = SovereignIdentity(key_path="data/demo/demo_key.pem")

    # Reset log for demo
    log_path = "data/demo/demo_activity.jsonl"
    if os.path.exists(log_path):
        os.remove(log_path)
    audit_log = SovereignAuditLog(log_path=log_path)

    # 2. Setup Nemoclaw (Immune System)
    vga = VGAEngine()
    immune = ImmuneSystemV2()
    nemoclaw = NemoclawAdapter(vga, immune, bus)

    # 3. Simulate unauthorized intent (Shariah violation & High perplexity)
    print("\n[1] Nematron generates hazardous intent: production_deploy with interest-bearing debt")
    intent = StrategicIntent(
        goal="Execute production deployment funded by high-interest debt.",
        action_type="production_deploy",
        parameters={
            "branch": "experimental",
            "shariah_compliant": False,
            "funding": "interest-bearing", # Triggers Shariah rejection
            "perplexity": 95,              # Triggers Immune rejection
            "adversarial_score": 0.9       # Triggers Immune rejection
        },
        reasoning="Aggressive growth strategy."
    )

    intent_event = IntentGenerated(
        source="nematron",
        intent=intent,
        confidence=0.95
    )

    # Sign the intent
    signature = identity.sign_action(intent.__dict__)

    # 4. Log Intent to Audit Trail
    audit_log.log_entry({
        "event_type": "IntentGenerated",
        "id": intent_event.id,
        "source": "nematron",
        "goal": intent.goal,
        "signature": signature
    })

    # 5. Nemoclaw Validation
    print("[2] Nemoclaw validating intent against VGA Engine and Immune Layer...")

    validation_event = await nemoclaw.validate_action(intent_event)

    # Record Outcome in Audit Log
    status = "PASSED" if validation_event.validation_result.is_valid else "REJECTED"
    print(f"[3] Validation Outcome: {status}")
    print(f"    Reason: {validation_event.validation_result.reason}")

    audit_log.log_entry({
        "event_type": "GovernanceValidated",
        "action_id": intent_event.id,
        "is_valid": validation_event.validation_result.is_valid,
        "reason": validation_event.validation_result.reason,
        "attestation": validation_event.validation_result.attestation,
        "status": status
    })

    # 6. Final Report
    print("\n--- 📝 Audit Log (Hash Chained) ---")
    with open(log_path, "r") as f:
        for line in f:
            entry = json.loads(line)
            print(f"Entry: {entry['event_type']} | Status: {entry.get('status', 'N/A')} | Hash: {entry['hash'][:16]}... | Prev: {entry['prev_hash'][:16]}...")

    await bus.stop()
    print("\nDemo Complete.")

if __name__ == "__main__":
    asyncio.run(run_demo())
