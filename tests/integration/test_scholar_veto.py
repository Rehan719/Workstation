
import pytest
import asyncio
from agentic_core.governance.command_dispatch import AICommander
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.survival.survival_engine import SurvivalEngine
from agentic_core.immune.immune_system import ImmuneSystemV2
from unittest.mock import MagicMock

class MockScholarBoard:
    def __init__(self):
        self.veto_active = False

    def check_sharia_compliance(self, action_data: dict) -> bool:
        if self.veto_active:
            return False
        # Example rule: No interest-bearing transactions
        if "interest" in str(action_data).lower():
            return False
        return True

@pytest.mark.asyncio
async def test_scholar_veto_preemption():
    commander = AICommander()
    vga = VGAEngine()
    survival = SurvivalEngine()
    immune = ImmuneSystemV2()
    scholar_board = MockScholarBoard()

    # Scenario: A donation campaign with a hidden 'interest-bearing' component
    campaign_intent = {
        "scope": "financial:donation",
        "action": "START_CAMPAIGN",
        "data": {
            "name": "Ramadan Relief",
            "terms": "interest-bearing-account" # This should trigger a Sharia violation
        }
    }

    print("\n1. Evaluating intent through VGA Shariah Policy...")
    is_halal = vga.validate_action("shariah", campaign_intent["data"])
    assert is_halal == False
    print("   Result: VGA correctly rejected the interest-bearing intent.")

    print("2. Simulating Scholar Veto triggering Immune Layer preemption...")
    scholar_board.veto_active = True

    # If scholar veto is active, it's a critical threat to spiritual integrity
    if scholar_board.veto_active:
        threat_score = immune.evaluate_threat({"perplexity": 100, "reason": "SCHOLAR_VETO"})
        assert threat_score > 0.8
        print(f"   Immune System detected high threat from Scholar Veto: {threat_score:.2f}")

        # Survival Engine Veto (Immune Layer vs Autonomous Business)
        veto_entry = survival.trigger_veto("IMMUNE", "Scholar Governance Veto: Sharia Non-Compliance")
        assert veto_entry["source"] == "IMMUNE"
        print(f"   Survival Engine Vetoed the action. Source: {veto_entry['source']}, Reason: {veto_entry['reason']}")

    print("3. Verifying Commander rejects the intent due to governance failure...")
    # In a real integration, the VGA rejection would stop this
    success = await commander.execute_intent(campaign_intent)
    # The current dispatch_model in command_dispatch.py only has 'financial' and 'healthcare' resolvers.
    # FinancialResolver checks for 'riba-free' in compliance list.
    assert success == False
    print("   Commander successfully rejected the intent.")

if __name__ == "__main__":
    asyncio.run(test_scholar_veto_preemption())
