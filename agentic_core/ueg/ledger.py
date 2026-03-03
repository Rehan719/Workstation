import logging
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BlockchainLedger:
    """UEG Blockchain Ledger for immutable trait storage."""

    def __init__(self, storage_path: str = "meta/ledger.json"):
        self.storage_path = storage_path
        self.chain = []

    def add_entry(self, entry: Dict[str, Any]):
        self.chain.append(entry)
        logger.info(f"LEDGER: Added entry to chain. Height: {len(self.chain)}")
        self._persist()

    def _persist(self):
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.chain, f)
        except Exception as e:
            logger.error(f"LEDGER: Failed to persist: {e}")
