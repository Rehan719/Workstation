import asyncio
import logging
import json
from src.orchestrator.orchestrator import Orchestrator
from src.triad.quantum.hybrid_optimizer import HybridQuantumClassicalOptimizer
from src.triad.quantum.qnlp import QNLPProcessor
from src.orchestrator.collaboration import CollaborativeIntelligenceProtocol

logging.basicConfig(level=logging.INFO)

async def run_mastery_demo():
    orchestrator = Orchestrator()
    ueg = orchestrator.ueg

    print("\n=== JULES AI v53.0 MASTERY DISCOVERY DEMO ===")

    # 1. Quantum-AI Synergy: Protein Folding & QNLP
    print("\n[1] Quantum-AI Synergy:")
    vqe = HybridQuantumClassicalOptimizer()
    vqe_res = await vqe.solve_folding_stub({"seq": "MET-ALA-VAL"})
    print(f"VQE Folding Energy: {vqe_res['ground_state_energy']:.4f}")

    qnlp = QNLPProcessor()
    semantic = await qnlp.analyze_sentiment("Primary Sclerosing Cholangitis is a chronic liver disease.")
    print(f"QNLP Semantic Stability: {semantic['epistemic_stability']:.4f}")

    # 2. Advanced Scholarship: Grant Proposal
    print("\n[2] Mastered Scholarship:")
    from src.scholarship.grant_generator import GrantProposalGenerator
    grant_gen = GrantProposalGenerator(ueg)
    proposal = await grant_gen.generate_proposal("Liver Fibrosis Reversal", ["Dr. Alice", "Jules AI"])
    print(f"Generated Proposal Title: {proposal['title']}")

    # 3. Collaborative Intelligence: BFT Consensus
    print("\n[3] Collaborative Intelligence:")
    collab = CollaborativeIntelligenceProtocol(ueg)
    proposal_data = {"action": "commit_discovery_v53"}
    votes = {"agent_alpha": True, "agent_beta": True, "agent_gamma": True, "user_admin": True}
    decision = await collab.process_collaborative_decision("user_master", proposal_data, votes)
    print(f"BFT Consensus Result: {decision['consensus']['status']}")
    print(f"Contribution Signature: {decision['attribution']['signature']}")

    # 4. End-to-End Simulation
    print("\n[4] End-to-End Simulation:")
    result = await orchestrator.psc_discovery_simulation("test_master")
    print(f"Workstation Status: {result['status']}")
    print(f"Verified via: {result['verification_report']}")

    # 5. Epistemic Integrity Check
    print("\n[5] Epistemic Integrity Check:")
    integrity = ueg.ledger.verify_integrity()
    print(f"Blockchain & Merkle Chain Integrity: {'PASSED' if integrity else 'FAILED'}")

if __name__ == "__main__":
    asyncio.run(run_mastery_demo())
