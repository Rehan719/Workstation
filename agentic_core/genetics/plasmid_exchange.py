import random
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PlasmidExchanger:
    """
    ARTICLE DC: Horizontal Gene Transfer (Plasmid Exchange).
    Transfer rate: 0.1–10% per hour.
    """
    def __init__(self, exchange_rate: float = 0.05):
        self.exchange_rate = exchange_rate # probability per cycle

    def attempt_exchange(self, local_genome: Dict[str, Any], peer_genome: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transfers a random trait from peer to local.
        """
        if random.random() < self.exchange_rate:
            peer_traits = peer_genome.get("traits", {})
            if peer_traits:
                trait_to_transfer = random.choice(list(peer_traits.keys()))
                local_genome["traits"][trait_to_transfer] = peer_traits[trait_to_transfer]
                logger.info(f"PLASMID: Transferred trait '{trait_to_transfer}' via horizontal exchange.")
        return local_genome
