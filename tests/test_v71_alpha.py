import unittest
import numpy as np
from agentic_core.molecular.triad_integration import TriadIntegrator
from agentic_core.consciousness.meta_cognitive_executive import MetaCognitiveExecutive

class TestV71AlphaFeatures(unittest.TestCase):
    def setUp(self):
        self.triad = TriadIntegrator()
        self.mce = MetaCognitiveExecutive()

    def test_redox_gated_hsp_increase(self):
        """Test DA-I: ATPase turnover increases with oxidative stress."""
        # Basal potential approx -225mV
        basal_state = self.triad.run_cycle(ros_level=0.8, nadh_ratio=0.5)
        basal_hsp = basal_state["hsp_atp_turnover"]

        # Stress potential (should be more negative for HSP activation in this model)
        # Lower nadh_ratio means more NADH, making potential more negative
        stress_state = self.triad.run_cycle(ros_level=0.8, nadh_ratio=0.01)
        stress_hsp = stress_state["hsp_atp_turnover"]

        print(f"DEBUG: Basal Pot={basal_state['redox_potential_mv']:.1f}mV, Basal HSP={basal_hsp:.2f}")
        print(f"DEBUG: Stress Pot={stress_state['redox_potential_mv']:.1f}mV, Stress HSP={stress_hsp:.2f}")
        self.assertGreater(stress_hsp, basal_hsp)

    def test_keap1_activation(self):
        """Test DA-III: KEAP1/NRF2 release at threshold."""
        # Threshold is -235mV
        basal_state = self.triad.run_cycle(ros_level=0.8, nadh_ratio=0.5)
        self.assertFalse(basal_state["keap1_active"])

        # Lower nadh_ratio means more NADH, making potential more negative
        stress_state = self.triad.run_cycle(ros_level=0.8, nadh_ratio=0.1)
        print(f"DEBUG: Stress Potential={stress_state['redox_potential_mv']:.1f}mV, KEAP1={stress_state['keap1_active']}")
        self.assertTrue(stress_state["keap1_active"])

    def test_mce_proactivity(self):
        """Test Phase 1 Objective: Predictive proactivity."""
        # v71.0 MCE triggers RESOURCE_CONSERVATION at atp < 2.5 (v70 was < 2.0)
        workspace = np.zeros(16)
        workspace[1] = 2.3 # ATP level

        decision = self.mce.make_strategic_decision(workspace)
        self.assertEqual(decision["action"], "RESOURCE_CONSERVATION")
        self.assertIn("Predictive", decision["reason"])

if __name__ == "__main__":
    unittest.main()
