"""
QANBridge Simulator – High-fidelity simulator for post-quantum cross-chain settlement.
"""
from typing import Dict, Any, List, Optional
from decimal import Decimal
import hashlib
from datetime import datetime, UTC
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

class QANBridgeSimulator:
    def __init__(self, ueg_logger: Any):
        self.ueg = ueg_logger
        self.local_ledger: Dict[str, Decimal] = {} # target_node -> balance
        # W545 (FU-347) — THE MARKER TRAVELS WITH THE VALUE NOW. This line assigned a standardised
        # algorithm name with a standards citation beside it and carried no simulation marker of its own,
        # while the only disclosure lived in the class docstring and in the UEG payload. The field is
        # returned to callers in the settlement receipt below, so a consumer saw a named post-quantum
        # primitive and nothing to suggest no code implements it. The name is KEPT, because it records
        # which primitive this bridge is specified against, and it is renamed to say what it is.
        self.pqc_algorithm_declared = "ML-DSA-87"   # NIST FIPS 204 — DECLARED, NOT IMPLEMENTED
        self.pqc_implemented = False
        self.pqc_basis = ("DECLARED, NOT IMPLEMENTED: no post-quantum signature, key exchange or "
                          "verification happens anywhere in this module. ML-DSA-87 (NIST FIPS 204) names "
                          "the primitive this bridge is SPECIFIED against, not one it performs")

    async def settle_cross_node(self, amount: Decimal, target_node: str, sender_did: str) -> Dict[str, Any]:
        """
        Simulates post-quantum settlement finality on QANplatform.
        """
        # 1. PQC Key Exchange & Signature Verification (Simulated)
        # In real: use ML-KEM-1024 for shared secret
        handshake_id = hashlib.sha256(f"{sender_did}{target_node}".encode()).hexdigest()

        # 2. lock assets on source (Polygon) and mint on target (QAN)
        self.local_ledger[target_node] = self.local_ledger.get(target_node, Decimal(0)) + amount

        # W545 (FU-347) — THE RECEIPT NOW DISCLOSES ITSELF, which is where the disclosure was missing.
        # The UEG payload below has always carried is_simulated: True, so the LEDGER was honest; the
        # RETURNED RECEIPT said status FINALIZED, named a post-quantum algorithm and reported a 1500ms
        # finality, with nothing to mark any of it simulated. The disclosure sat exactly where no
        # consumer looks and was absent from the only thing a caller receives.
        receipt = {
            "tx_hash": f"pq_0x{hashlib.sha3_512(f'{handshake_id}{amount}'.encode()).hexdigest()[:64]}",
            "simulated": True,
            #  NOT "FINALIZED". Nothing settled, no chain was contacted, and no signature was made or
            #  checked; what happened is a local dict entry.
            "status": "SIMULATED_NOT_SETTLED",
            "pqc_algorithm_declared": self.pqc_algorithm_declared,
            "pqc_implemented": self.pqc_implemented,
            "pqc_basis": self.pqc_basis,
            #  a literal, named as one. 1500 was a plausible sub-2s figure annotated only in a comment.
            "declared_finality_ms": 1500,
            "finality_basis": ("DECLARED, NOT MEASURED: 1500ms is a target this simulator reports, not a "
                              "duration anything timed. No settlement occurred to time"),
            "settlement_basis": ("the amount was added to this process's in-memory ledger. No chain was "
                                 "contacted, nothing was locked on a source chain and nothing was minted "
                                 "on a target chain"),
            "timestamp": datetime.now(UTC).isoformat()
        }

        # 3. Log with SIMULATED flag for Phase 9 release
        await self.ueg.log_event(
            "PQ_CROSS_CHAIN_SETTLEMENT",
            {
                "receipt": receipt,
                "target_node": target_node,
                "amount": float(amount),
                "is_simulated": True
            }
        )

        return receipt

    async def get_pq_balance(self, node_did: str) -> Decimal:
        return self.local_ledger.get(node_did, Decimal(0))
