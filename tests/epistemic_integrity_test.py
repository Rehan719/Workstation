import asyncio
import unittest
import os
import json
import hashlib
from agentic_core.ueg.ledger import UnifiedEvidenceGraph, BlockchainLedger
from agentic_core.verification.layer3 import NumericalValidator
from agentic_core.verification.layer5 import AdversarialHypothesisTestingEngine

class TestEpistemicIntegrity(unittest.IsolatedAsyncioTestCase):

    async def test_blockchain_merkle_ledger(self):
        """Verifies Merkle-tree anchoring and blockchain chaining."""
        if os.path.exists("meta/ledger.json"):
            os.remove("meta/ledger.json")

        ueg = UnifiedEvidenceGraph(persistence_path="meta/ueg_test.json")
        ueg.add_node("H1", "Hypothesis", {"claim": "Quantum speedup is real"})
        ueg.add_node("E1", "Evidence", {"data": "Shor's algorithm"})
        ueg.supports("E1", "H1")

        # Add block (anchoring)
        block = ueg.commit()

        self.assertEqual(block['index'], 2) # Genesis is index 1
        self.assertTrue(ueg.ledger.verify_integrity())

        # Tamper check: Tamper with a hash to trigger Merkle failure
        with open("meta/ledger.json", "r") as f:
            data = json.load(f)
        data[1]['transactions'][0]['hash'] = "TAMPERED_HASH"
        with open("meta/ledger.json", "w") as f:
            json.dump(data, f)

        tampered_ledger = BlockchainLedger(persistence_path="meta/ledger.json")
        self.assertFalse(tampered_ledger.verify_integrity())

    async def test_five_layer_verification(self):
        """Verifies Layer 3 (Numerical) and Layer 5 (CEGAR) logic."""
        # Layer 3: Numerical
        validator = NumericalValidator()
        report = await validator.validate_with_analysis(1.000000001, 1.0, {"op_complexity": 50})
        self.assertTrue(report['passed'])
        self.assertEqual(report['error_analysis']['stability_rating'], "STABLE")

        # Layer 5: CEGAR Adversarial
        ueg = UnifiedEvidenceGraph(persistence_path="meta/ueg_test_adversarial.json")
        engine = AdversarialHypothesisTestingEngine(ueg)

        # Make it more vulnerable to fail the 0.6 threshold
        hypothesis = {
            "logic_model": "heuristic_based",
            "metrics": {"variance": 0.9} # This makes it unstable
        }

        report = await engine.run_refutation_suite("H2", hypothesis)
        # Vulnerable if score < 0.6.
        # Attacks: UEG_Counter(fail), CEGAR(success), Sensitivity(success).
        # failed_attacks = 1. score = 1/3 = 0.33. Status = VULNERABLE.
        self.assertEqual(report['status'], "VULNERABLE")

if __name__ == "__main__":
    unittest.main()
