import os
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import logging
import hashlib
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
# W535 (FU-332) — was an import of a module that does not exist, so this file could not be imported.
from agentic_core import attestation
from products.capital_fund.core.vault import CapitalVault

class CryptoGateway:
    """
    Module 3B: Crypto Gateway Adapter.
    Handles on-chain deposits and withdrawals for USDC/ETH.

    W575 (FU-332) — this line used to claim the wallets were secured by a post-quantum scheme (the
    exact wording is in W575's commit message, not here). NO POST-QUANTUM OPERATION EXISTS IN THIS
    REPOSITORY: `agentic_core/crypto/` holds only an entropy pool, and the primitive this module
    actually reaches for is `agentic_core.attestation`, which states in its own docstring that it
    computes a KEYED MAC and not a post-quantum signature. The wallets are not PQC-secured; nothing
    here is. Real-money rails are owner-gated and off, so no withdrawal executes either way.
    """
    def __init__(self, owner_uid: str, constitutional_validator: GaaSValidator, ueg: UEGLogger):
        self.owner_uid = owner_uid
        self.validator = constitutional_validator
        self.ueg = ueg
        self.vault = CapitalVault(owner_uid)
        self.logger = logging.getLogger("CryptoGateway")
        self.gas_reserve_ratio = Decimal("0.05") # 5% gas reserve mandate

    async def verify_onchain_deposit(self, tx_hash: str, asset_type: str, expected_amount: Decimal) -> Dict[str, Any]:
        """
        Verifies an on-chain transaction and credits the vault atomically.
        In Phase 3, this simulates Web3 receipt verification.
        """
        # 1. Simulate Web3 Receipt Verification
        # In production: receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
        receipt_status = 1 # Success

        if receipt_status != 1:
            raise ValueError(f"On-chain transaction {tx_hash} failed or is pending.")

        # 2. Constitutional AML/KYC Check
        validation = await self.validator.validate_action(
            "CRYPTO_DEPOSIT",
            {"uid": self.owner_uid, "tx_hash": tx_hash, "amount": float(expected_amount), "asset": asset_type}
        )
        if not validation.get("passed"):
            raise ValueError(f"Constitutional Violation: {validation.get('reason')}")

        # 3. Atomic Vault Settlement
        # Credits the balance in Firestore
        vault_result = await self.vault.deposit(expected_amount, f"crypto_{tx_hash}")

        # 4. UEG Logging
        await self.ueg.log_event(
            "CRYPTO_DEPOSIT_VERIFIED",
            {
                "uid": self.owner_uid,
                "tx_hash": tx_hash,
                "asset": asset_type,
                "amount": float(expected_amount),
                "vault_event": vault_result["event_id"]
            }
        )

        return {
            "status": "COMPLETED",
            "tx_hash": tx_hash,
            "new_balance": vault_result["balance"]
        }

    async def execute_onchain_withdrawal(self, amount: Decimal, asset_type: str, destination: str) -> Dict[str, Any]:
        """
        Executes a crypto withdrawal with gas modelling, attested by a KEYED MAC.

        W575 (FU-332) — this line used to name a post-quantum signature scheme (the exact wording is
        in W575's commit message). It never signed anything post-quantum: the
        attestation this path records is a keyed MAC (agentic_core.attestation), which is a different
        and weaker claim; naming a specific lattice signature scheme on a money path is the kind of
        overstatement a reader would act on. (The scheme is not named here: a repo-wide guard forbids
        those names outside the files that record their retirement, and this file is not one of them.
        It is in W575's commit message.) The gate below refuses while real-money rails are off, so
        today this returns REFUSED before any of it runs.
        """
        # 0. THE MONEY GATE, and it goes FIRST. W535 — this path is named an on-chain withdrawal and
        #    consulted NO gate of any kind; it was unreachable only by accident, because the module could not
        #    be imported. Repairing that import without this check would have turned a latent money path into
        #    a reachable ungated one, which is a worse outcome than the broken import. REAL_MONEY_ENABLED is
        #    False in code and only the Owner flips it; while it is False this refuses and says so, and no
        #    virtual-WST ledger is touched here either, because this function is about a real chain.
        from agentic_core.economy.owner_payments import REAL_MONEY_ENABLED
        if not REAL_MONEY_ENABLED:
            return {
                "status": "REFUSED",
                "executed": False,
                "reason": ("real-money rails are disabled in code (REAL_MONEY_ENABLED is False), so no "
                           "on-chain withdrawal is attempted. This platform's money is virtual WST; a real "
                           "transfer needs the Owner's explicit decision, not a caller's request"),
                "tx_hash": None,
                "attested": None,
                # W535 — the three branches of this function must agree on their keys, or a caller indexing
                # the success shape raises on the refusal. This is the branch most likely to be hit.
                "attestation_algorithm": None,
                "verified": None,
                "verified_basis": "nothing was attested, because no withdrawal was attempted",
            }

        # 1. Gas Fee Modelling (Article 1134 requirement)
        # Simulate gas estimation
        estimated_gas_usd = Decimal("2.50")
        if estimated_gas_usd > (amount * self.gas_reserve_ratio):
             raise ValueError(f"Gas cost ({estimated_gas_usd} USD) exceeds 5% reserve limit.")

        # 2. Attestation of the withdrawal intent — COMPUTED, never asserted.
        #    W535 (FU-332) — this claimed to sign the intent with an algorithm this platform does not
        #    implement, by calling a function absent from the package it imported. It then passed
        #    `signed: True` INTO the constitutional validator as an input, so the governance check was being
        #    told the thing it was meant to establish. The attestation is now computed and its real result is
        #    what the validator receives; with no key configured, attest() refuses rather than inventing one.
        withdrawal_intent = {"op": "WITHDRAW", "uid": self.owner_uid, "amount": str(amount),
                             "asset": asset_type, "destination": destination}
        signing = attestation.attest(withdrawal_intent)

        # 3. Constitutional Validation — fed the measured attestation state, not a literal
        validation = await self.validator.validate_action(
            "CRYPTO_WITHDRAWAL",
            {"uid": self.owner_uid, "amount": float(amount), "dest": destination,
             "attested": bool(signing.get("signed")),
             "attestation_algorithm": signing.get("algorithm"),
             "attestation_basis": signing.get("basis")}
        )
        if not validation.get("passed"):
            raise ValueError(f"Constitutional Violation: {validation.get('reason')}")

        # 4. Atomic Vault Settlement (Debit)
        # Note: In Phase 3, we simulate MultiSig signatures to satisfy the check if needed
        # or assume owner balance is sufficient.
        vault_result = await self.vault.withdraw(amount)

        # 5. UEG Logging with SHA-3-512
        tx_hash = hashlib.sha3_512(
            f"{signing.get('signature') or 'NOT ATTESTED'}{datetime.now(UTC)}".encode()).hexdigest()

        await self.ueg.log_event(
            "CRYPTO_WITHDRAWAL_EXECUTED",
            {
                "uid": self.owner_uid,
                "tx_hash": tx_hash,
                "amount": float(amount),
                "dest": destination,
                "attestation": signing,
            }
        )

        # W535 — this returned `verified: True` unconditionally, with nothing verified anywhere in the
        # function. The verification is now RECOMPUTED from the record, and it is three-state: None means it
        # could not be checked, which is not a pass.
        _check = attestation.verify(withdrawal_intent, signing)
        return {
            "status": "SUBMITTED",
            "executed": True,
            "reason": None,
            "tx_hash": tx_hash,
            "attested": bool(signing.get("signed")),
            "attestation_algorithm": signing.get("algorithm"),
            "verified": _check.get("verified"),
            "verified_basis": _check.get("basis"),
        }
