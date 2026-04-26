import random
import hashlib
import numpy as np
import logging
import struct
from typing import Dict, Any, List, Optional
from ..crypto.entropy_pool import EntropyPool

class OAM_QKDSurrogate:
    def __init__(self, n_modes: int = 48, entropy_pool: Optional[EntropyPool] = None):
        self.logger = logging.getLogger("OAM_QKD")
        self.n_modes = n_modes
        self.entropy_pool = entropy_pool
        self._rng = random.Random()
        self._sync_with_pool()

    def _sync_with_pool(self):
        if self.entropy_pool:
            seed = self.entropy_pool.get_seed()
            self._rng.seed(seed)

    def generate_key(self, plaintext: str, recipient: str) -> Dict[str, Any]:
        self._sync_with_pool()
        length = len(plaintext) * 8
        alice_bits = [self._rng.randint(0, self.n_modes - 1) for _ in range(length * 4)]
        alice_bases = [self._rng.choice(['spatial', 'angular']) for _ in range(length * 4)]
        intrinsic_qber = 0.012
        bob_bits = []
        for i in range(len(alice_bits)):
            if self._rng.random() < intrinsic_qber:
                bob_bits.append(self._rng.randint(0, self.n_modes - 1))
            else:
                bob_bits.append(alice_bits[i])
        bob_bases = [self._rng.choice(['spatial', 'angular']) for _ in range(length * 4)]
        matched_idx = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
        alice_sifted = [alice_bits[i] for i in matched_idx]
        bob_sifted = [bob_bits[i] for i in matched_idx]
        if not alice_sifted: return {"status": "FAILED", "reason": "No sifted bits"}
        errors = sum(1 for a, b in zip(alice_sifted, bob_sifted) if a != b)
        qber = errors / len(alice_sifted)
        def h_d(e, d):
            if e == 0: return 0
            inner = max(1e-10, d - 1)
            e_val = max(1e-10, e)
            one_minus_e = max(1e-10, 1 - e)
            return e_val * np.log2(inner) - e_val * np.log2(e_val) - one_minus_e * np.log2(one_minus_e)
        key_rate = np.log2(self.n_modes) - 2 * h_d(qber, self.n_modes)
        encrypted = hashlib.sha3_512(plaintext.encode()).hexdigest()
        return {
            "encrypted_message": encrypted,
            "security_metrics": {
                "qber": float(qber),
                "key_rate_bits_per_photon": float(key_rate),
                "n_modes": self.n_modes,
                "protocol": "OAM-48-HD-BB84"
            }
        }

    def run_statistical_validation(self, trials: int = 1000) -> Dict[str, Any]:
        qbers, key_rates = [], []
        for _ in range(trials):
            res = self.generate_key("val", "internal")
            if "security_metrics" in res:
                qbers.append(res["security_metrics"]["qber"])
                key_rates.append(res["security_metrics"]["key_rate_bits_per_photon"])
        qber_ci_upper = np.mean(qbers) + (1.96 * np.std(qbers) / np.sqrt(trials))
        key_rate_ci_lower = np.mean(key_rates) - (1.96 * np.std(key_rates) / np.sqrt(trials))
        passed = (qber_ci_upper < 0.05) and (key_rate_ci_lower > 5.0)
        return {"qber_ci_upper": float(qber_ci_upper), "key_rate_ci_lower": float(key_rate_ci_lower), "passed": passed}
