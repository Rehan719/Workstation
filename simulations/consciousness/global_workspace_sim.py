import time
from agentic_core.consciousness.global_workspace import GlobalWorkspace
from agentic_core.consciousness.meta_cognitive_executive import MetaCognitiveExecutive

def simulate_consciousness():
    print("--- Simulation: Global Workspace (Layer 2) ---")
    workspace = GlobalWorkspace()
    mce = MetaCognitiveExecutive(workspace)

    # Publish simulated triad data
    workspace.publish_state("molecular_triad", {"ros_level": 2.1, "atp_adp_ratio": 4.5})

    # Run cognitive cycle
    decision = mce.perform_cognitive_cycle()
    print(f"MCE Decision: {decision['action']} (Reason: {decision['reason']})")

    workspace.trigger_global_ignition()

if __name__ == "__main__":
    simulate_consciousness()
