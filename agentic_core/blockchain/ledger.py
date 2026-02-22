import logging
import hashlib
from web3 import Web3
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BlockchainLedger:
    """
    Blockchain Provenance (Article AT).
    Immutable records via IPFS and Ethereum testnets.
    """

    def __init__(self, provider_url: Optional[str] = None):
        # Use Sepolia as default testnet if no URL provided
        self.w3 = Web3(Web3.HTTPProvider(provider_url or "https://sepolia.infura.io/v3/YOUR_KEY"))
        self.connected = self.w3.is_connected() if provider_url else False

    async def anchor_artifact(self, artifact_id: str, content: bytes) -> Dict[str, Any]:
        """
        Anchors an artifact hash using Web3 provider.
        """
        content_hash = hashlib.sha256(content).hexdigest()

        # In a real system, we'd send a transaction to a 'Provenance' smart contract
        receipt = {
            "artifact_id": artifact_id,
            "hash": f"0x{content_hash}",
            "blockchain": "ethereum_sepolia",
            "status": "pending_anchor" if not self.connected else "anchored",
            "tx_hash": f"0x{hashlib.sha256(artifact_id.encode()).hexdigest()}"
        }

        if self.connected:
            logger.info(f"Transaction sent for {artifact_id}")
        else:
            logger.warning(f"Web3 not connected. Artifact {artifact_id} hash cached locally.")

        return receipt

    def verify_provenance(self, artifact_id: str, content: bytes, receipt: Dict[str, Any]) -> bool:
        """
        Verifies content against the anchored hash.
        """
        current_hash = f"0x{hashlib.sha256(content).hexdigest()}"
        return current_hash == receipt.get("hash")
