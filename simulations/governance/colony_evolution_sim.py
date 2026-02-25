import time
from agentic_core.governance.quorum_sensing import QuorumSensing

def simulate_governance():
    print("--- Simulation: Symbiotic Governance (Layer 4) ---")
    quorum = QuorumSensing(min_colony_size=3)

    # Broadcast healthy signals from 4 agents
    agents = ["org-01", "org-02", "org-03", "org-04"]
    for aid in agents:
         quorum.broadcast_health_signal(aid, intensity=0.9)

    # Check quorum
    quorum.update_colony_state()
    has_q = quorum.has_ecosystem_quorum()
    print(f"Colony size 4. Has Quorum (Threshold 3): {has_q}")

if __name__ == "__main__":
    simulate_governance()
