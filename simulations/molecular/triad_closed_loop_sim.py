import time
import numpy as np
from agentic_core.molecular.triad_integration import MolecularTriad

def simulate_triad():
    print("--- Simulation: Molecular Triad (Layer 1) ---")
    triad = MolecularTriad()

    # 5 steps of simulation
    for i in range(5):
        # healthy vs stressed input
        load = 0.2 if i < 3 else 0.9
        state = triad.run_step(substrate_availability=0.8, demand=load)
        print(f"Step {i}: p53={state['p53_level']:.2f}, ROS={state['ros_level']:.2f}, Energy={state['atp_adp_ratio']:.2f}")
        time.sleep(0.1)

if __name__ == "__main__":
    simulate_triad()
