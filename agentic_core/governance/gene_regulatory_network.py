import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class GeneRegulatoryNetwork:
    """
    ARTICLE 161: Gene Regulatory Network Governance.
    Decentralized governance where modules interact through defined regulatory rules.
    """

    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.regulatory_rules: List[Dict[str, Any]] = []
        self.signaling_protocols: Dict[str, List[str]] = {}

    def register_module(self, name: str, module: Any, receptors: List[str], signals: Optional[List[str]] = None):
        """Register module with signal receptors and emitted signals."""
        self.modules[name] = {
            "instance": module,
            "receptors": receptors,
            "signals": signals or [],
            "health": 1.0
        }
        for sig in receptors:
            if sig not in self.signaling_protocols:
                self.signaling_protocols[sig] = []
            self.signaling_protocols[sig].append(name)

    def emit_signal(self, signal: str, data: Any, source: str):
        """Broadcast signal and evaluate regulatory rules (Article 187)."""
        if signal not in self.signaling_protocols:
            return
        for module_name in self.signaling_protocols[signal]:
            if module_name == source:
                continue
            module_info = self.modules[module_name]
            try:
                # Actual signal processing logic
                if hasattr(module_info["instance"], "receive_signal"):
                    module_info["instance"].receive_signal(signal, data, source)
                logger.info(f"GRN: {module_name} processed {signal} from {source}")

                # Evaluate regulatory rules
                self._evaluate_rules(signal, data)
            except Exception as e:
                logger.error(f"GRN: Signal {signal} failed for {module_name}: {e}")

    def _evaluate_rules(self, signal: str, data: Any):
        """Condition-action pairs for system-wide adaptation."""
        for rule in self.regulatory_rules:
            if rule["condition"](signal, data):
                logger.info(f"GRN: Executing regulatory action for rule {rule['name']}")
                rule["action"]()

    def add_rule(self, name: str, condition: Any, action: Any):
        self.regulatory_rules.append({"name": name, "condition": condition, "action": action})
