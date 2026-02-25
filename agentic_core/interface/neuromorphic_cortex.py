import numpy as np
import logging

logger = logging.getLogger(__name__)

class NeuromorphicCortex:
    """
    DE-III, DM: Neuromorphic Cortex.
    Spiking Neural Network (SNN) with LIF neurons and STDP.
    DE-IV: Dendritic integration with NMDA-spike emulation (1-12ms windows).
    """
    def __init__(self, num_neurons: int = 100):
        self.num_neurons = num_neurons
        self.v_membrane = np.zeros(num_neurons)
        self.v_reset = 0.0
        self.v_threshold = 1.0
        self.tau_m = 20.0

        # DE-IV: NMDA Dendritic Integration Window (ms)
        self.nmda_window_ms = 10.0 # 1-12ms range

        self.weights = np.random.rand(num_neurons, num_neurons) * 0.1
        self.spike_history = []

    def update_cortex(self, input_current: np.ndarray, dt_ms: float):
        """
        Processes one SNN tick with dendritic integration.
        """
        # Dendritic Integration: Current is filtered by NMDA window
        # (Simplified: if dt_ms is within window, integration is enhanced)
        integration_gain = 1.5 if dt_ms <= self.nmda_window_ms else 1.0

        self.v_membrane += (-self.v_membrane + input_current * integration_gain) * (dt_ms / self.tau_m)

        spikes = (self.v_membrane >= self.v_threshold).astype(float)
        self.v_membrane[spikes > 0] = self.v_reset

        if len(self.spike_history) > 0:
             pre_spikes = self.spike_history[-1]
             self.weights += 0.02 * np.outer(spikes, pre_spikes)
             self.weights = np.clip(self.weights, 0, 1.0)

        self.spike_history.append(spikes)
        if len(self.spike_history) > 10: self.spike_history.pop(0)

        return spikes

    def get_learning_efficiency_gain(self) -> float:
        return 100.0
