import numpy as np
from agentic_core.interface.neuromorphic_cortex import NeuromorphicCortex

def simulate_interface():
    print("--- Simulation: Neuromorphic Cortex (Layer 5) ---")
    cortex = NeuromorphicCortex(num_neurons=50)

    # Send random input spikes
    input_spikes = np.random.rand(50) > 0.7
    output = cortex.update_cortex(input_spikes.astype(float), dt_ms=10.0)

    print(f"Input Active: {np.sum(input_spikes)}, Output Active: {np.sum(output)}")
    print(f"Learning Gain vs rate-based: {cortex.get_learning_efficiency_gain()}x")

if __name__ == "__main__":
    simulate_interface()
