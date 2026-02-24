import logging
from typing import Dict, List, Any, Callable

logger = logging.getLogger(__name__)

class GeneCircuit:
    """
    DB: Gene Circuitry.
    Implements complex logic gates for gene regulation.
    """
    def __init__(self, name: str, logic: Callable[[Dict[str, float]], float]):
        self.name = name
        self.logic = logic

    def evaluate(self, inputs: Dict[str, float]) -> float:
        result = self.logic(inputs)
        logger.info(f"CIRCUIT: {self.name} evaluated to {result:.4f}")
        return result

class GeneCircuitryManager:
    """
    DB: Manages a collection of gene circuits.
    """
    def __init__(self):
        self.circuits = {}

    def add_circuit(self, name: str, logic: Callable[[Dict[str, float]], float]):
        self.circuits[name] = GeneCircuit(name, logic)

    def process_signals(self, signals: Dict[str, float]) -> Dict[str, float]:
        outputs = {}
        for name, circuit in self.circuits.items():
            outputs[name] = circuit.evaluate(signals)
        return outputs

# Example logic functions
def and_gate(inputs: Dict[str, float]) -> float:
    return min(inputs.values()) if inputs else 0.0

def or_gate(inputs: Dict[str, float]) -> float:
    return max(inputs.values()) if inputs else 0.0

def feedback_loop(inputs: Dict[str, float]) -> float:
    # Simulates self-reinforcement
    val = inputs.get('primary', 0.0)
    return min(1.0, val * 1.5)
