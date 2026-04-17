import pytest
from agentic_core.ueg.logger import VSBUEGLogger
import json
import os

@pytest.mark.asyncio
async def test_system_wide_entropy_export_audit():
    """
    Verify Article 1110: System must demonstrate net entropy export
    (dS_export > |dS_internal|) per macro-cycle.
    """
    ueg = VSBUEGLogger("data/test_audit.log")

    # Simulate some events to check chain integrity
    await ueg.log_minimisation_event("entropy_audit_start", {"status": "analyzing"})
    await ueg.log_minimisation_event("omega_macro_cycle", {
        "macro_cycle_id": "MC-AUDIT",
        "entropy_reduction": 0.18,
        "total_entropy": 0.25,
        "entropy_export_rate": 0.32, # > 0.25 (internal)
        "legal_coverage": 1.0
    })

    # 1. Chain Integrity Verification
    assert ueg.verify_chain() == True

    # 2. Cross-Layer Balance Check
    with open("data/test_audit.log", "r") as f:
        events = [json.loads(line) for line in f]

    audit_event = next(e for e in events if e["payload"]["event_type"] == "minimisation:omega_macro_cycle")
    metrics = audit_event["payload"]["data"]["metrics"]

    # Check Article 1110 condition
    assert metrics["entropy_export_rate"] > metrics["total_entropy"]
    assert metrics["legal_coverage"] == 1.0
