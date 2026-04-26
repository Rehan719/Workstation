import hashlib
import time
import struct
from typing import Dict, Any, Optional

class EntropyPool:
    def __init__(self):
        self.pool = b"v-infinity-genesis-seed"
        self.total_bits_harvested = 0
        self._update_hash()

    def _update_hash(self):
        self.pool_hash = hashlib.sha3_512(self.pool).digest()

    def add_entropy(self, metadata: Dict[str, Any]):
        entropy_string = f"{metadata.get('size', 0)}-{metadata.get('timestamp', time.time())}-" \
                         f"{metadata.get('source', 'unknown')}-{metadata.get('content_hash', 'none')}"
        new_entropy = hashlib.sha3_512(entropy_string.encode()).digest()
        mixed = bytearray()
        for i in range(len(self.pool_hash)):
            mixed.append(self.pool_hash[i] ^ new_entropy[i])
        self.pool = bytes(mixed)
        self._update_hash()
        self.total_bits_harvested += 128

    def get_seed(self) -> int:
        seed_bytes = self.pool_hash[:8]
        return struct.unpack("<Q", seed_bytes)[0]

    def get_status(self) -> Dict[str, Any]:
        return {
            "bits_available": self.total_bits_harvested,
            "pool_integrity": hashlib.sha3_512(self.pool).hexdigest()[:16]
        }
