import hashlib
import struct
from typing import Dict, Any


class EntropyPool:
    """Deterministic seed derivation via SHA3-512 + XOR mixing over caller-supplied metadata.

    W437 — what this is and is NOT, stated where a caller can see it:
      · No system, hardware, or physical entropy is ever read. The pool starts from a fixed
        literal and mixes only the metadata strings the caller supplies, so the empty call
        yields the SAME seed forever, in every deployment. That determinism is the feature
        (reproducible in-house seeding) — but the derived seed must never be used as a key,
        nonce, or token.
      · The old `total_bits_harvested` claimed 128 bits "harvested" per source without
        examining a byte of it — five empty dicts reported 640 bits into a 512-bit register.
        Renamed `mixing_rounds`: the count of mixing operations, which is all it ever measured.
      · The old pool-integrity digest was byte-identical to the seed (both were the first
        8 bytes of the same SHA3-512 digest), so it could never disagree with the value it
        claimed to attest. `pool_digest()` now returns a DIFFERENT slice of the pool digest
        (bytes 8..16), so it carries information beyond the seed itself.
    """

    GENESIS = b"v-infinity-genesis-seed"

    def __init__(self):
        self.pool = self.GENESIS
        self.mixing_rounds = 0
        self.timestamps_defaulted = 0
        self._update_hash()

    def _update_hash(self):
        self.pool_hash = hashlib.sha3_512(self.pool).digest()

    def add_entropy(self, metadata: Dict[str, Any]):
        # W437 refuter catch: this used to default a missing timestamp to time.time(), silently
        # injecting wall-clock into a derivation whose response claimed "deterministic" and "no
        # system entropy" CATEGORICALLY — and the one nondeterministic input shape was exactly the
        # one with no disclosure. The default is now the fixed 0 (deterministic by construction),
        # and how many sources needed it is counted so the payload can say so.
        if "timestamp" not in metadata:
            self.timestamps_defaulted += 1
        entropy_string = f"{metadata.get('size', 0)}-{metadata.get('timestamp', 0)}-" \
                         f"{metadata.get('source', 'unknown')}-{metadata.get('content_hash', 'none')}"
        new_entropy = hashlib.sha3_512(entropy_string.encode()).digest()
        mixed = bytearray()
        for i in range(len(self.pool_hash)):
            mixed.append(self.pool_hash[i] ^ new_entropy[i])
        self.pool = bytes(mixed)
        self._update_hash()
        self.mixing_rounds += 1

    def get_seed(self) -> int:
        seed_bytes = self.pool_hash[:8]
        return struct.unpack("<Q", seed_bytes)[0]

    def pool_digest(self) -> str:
        """Bytes 8..16 of the pool digest — disjoint from the seed's bytes 0..8."""
        return self.pool_hash[8:16].hex()

    def get_status(self) -> Dict[str, Any]:
        return {
            "mixing_rounds": self.mixing_rounds,
            "pool_digest": self.pool_digest(),
        }
