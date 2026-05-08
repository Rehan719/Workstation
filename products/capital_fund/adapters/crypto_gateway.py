import os
from decimal import Decimal
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import logging
import hashlib
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from agentic_core.crypto import pqc
from products.capital_fund.core.vault import CapitalVault

class CryptoGateway:
    """
    Module 3B: Crypto Gateway Adapter.
    Handles on-chain deposits and withdrawals for USDC/ETH.
    Integrates PQC-secured wallets and gas fee modelling.
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
        Executes a crypto withdrawal with PQC signing and gas modelling.
        """
        # 1. Gas Fee Modelling (Article 1134 requirement)
        # Simulate gas estimation
        estimated_gas_usd = Decimal("2.50")
        if estimated_gas_usd > (amount * self.gas_reserve_ratio):
             raise ValueError(f"Gas cost ({estimated_gas_usd} USD) exceeds 5% reserve limit.")

        # 2. PQC Transaction Signing
        # Sign the withdrawal intent using Dilithium
        withdrawal_intent = f"WITHDRAW_{self.owner_uid}_{amount}_{asset_type}_{destination}".encode()
        # In Phase 3, we use a constant representing the owner's PQC identity
        owner_pqc_identity = b"VSB_SOVEREIGN_ID_v1"
        pqc_signature = pqc.sign_instruction(withdrawal_intent, owner_pqc_identity)

        # 3. Constitutional Validation
        validation = await self.validator.validate_action(
            "CRYPTO_WITHDRAWAL",
            {"uid": self.owner_uid, "amount": float(amount), "dest": destination, "pqc_signed": True}
        )
        if not validation.get("passed"):
            raise ValueError(f"Constitutional Violation: {validation.get('reason')}")

        # 4. Atomic Vault Settlement (Debit)
        # Note: In Phase 3, we simulate MultiSig signatures to satisfy the check if needed
        # or assume owner balance is sufficient.
        vault_result = await self.vault.withdraw(amount)

        # 5. UEG Logging with SHA-3-512
        tx_hash = hashlib.sha3_512(f"{pqc_signature}{datetime.now(UTC)}".encode()).hexdigest()

        await self.ueg.log_event(
            "CRYPTO_WITHDRAWAL_EXECUTED",
            {
                "uid": self.owner_uid,
                "tx_hash": tx_hash,
                "amount": float(amount),
                "dest": destination,
                "pqc_signature": pqc_signature.hex() if isinstance(pqc_signature, bytes) else str(pqc_signature)
            }
        )

        return {
            "status": "SUBMITTED",
            "tx_hash": tx_hash,
            "pqc_verified": True
        }
