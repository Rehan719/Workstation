import asyncio
import logging
import unittest
from agentic_core.enterprise.engine import EnterpriseEvolutionEngine
from agentic_core.strategy.engine import StrategicPlanningModule, ResourceManagementModule, PerformanceManagementModule
from agentic_core.entity.ceo_interface import EntityCEOInterface
from agentic_core.self_improvement.strategic_introspection import BusinessAnalystAgent, GovernanceAnalystAgent, StrategicReflector
from agentic_core.governance.verifiable_governance import VGAEngine

class TestV101Components(unittest.TestCase):
    def test_e3_engine(self):
        e3 = EnterpriseEvolutionEngine()
        result = e3.orchestrate_evolution({"kpi_achievement": 0.85})
        self.assertEqual(result["status"], "PROPOSED")
        self.assertTrue(len(result["proposals"]) > 0)

    def test_strategic_planning_module(self):
        spm = StrategicPlanningModule(plan_path="docs/strategy/test_business_plan.md")
        inputs = {"vision": "Test Vision", "objectives": ["Obj 1"]}
        draft = spm.generate_draft_plan(inputs)
        self.assertEqual(draft["vision"], "Test Vision")
        spm.save_plan(draft)
        import os
        self.assertTrue(os.path.exists("docs/strategy/test_business_plan.md"))

    def test_entity_ceo_interface(self):
        interface = EntityCEOInterface()
        ts = interface.send_strategic_guidance("Test Guidance")
        self.assertIsNotNone(ts)
        interface.issue_veto("decision_1", "Test Veto")
        import json
        with open(interface.log_path, 'r') as f:
            log = json.load(f)
            self.assertTrue(any(entry.get("message") == "Test Guidance" for entry in log))
            self.assertTrue(any(entry.get("type") == "VETO" for entry in log))

    def test_strategic_introspection(self):
        ba = BusinessAnalystAgent()
        ga = GovernanceAnalystAgent()
        sr = StrategicReflector()

        b_analysis = ba.analyze_business_metrics({"objective_achievement": 0.7, "resource_roi": 1.0})
        g_assessment = ga.assess_governance([{"type": "VETO"}, {"type": "AUDIT"}])
        reflection = sr.reflect_on_strategy(b_analysis, g_assessment)

        self.assertEqual(b_analysis["status"], "ATTENTION_REQUIRED")
        self.assertEqual(g_assessment["status"], "GOVERNANCE_DRIFT")
        self.assertTrue(len(reflection["strategic_proposals"]) >= 2)

    def test_constitutional_enforcer(self):
        vga = VGAEngine()
        # Test SIH compliance
        valid_action = {"priority_layer": "immune", "security_context": True}
        invalid_action = {"priority_layer": "digestive", "security_context": True}

        self.assertTrue(vga.validate_action("constitutional", valid_action))
        self.assertFalse(vga.validate_action("constitutional", invalid_action))

if __name__ == "__main__":
    unittest.main()
