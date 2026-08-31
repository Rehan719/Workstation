import hashlib
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class IndustryAdapter:
    """Base class for industry-specific adapters."""
    def audit_trail(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generates an industry-specific audit trail."""
        return {"status": "generic"}

class FinancialServicesAdapter(IndustryAdapter):
    """ARTICLE 184: Financial Services compliance."""
    def audit_trail(self, data: Dict[str, Any]):
        """Digest the payload for real; never hand back an attestation nothing issued.

        W409 — this logged "Generating SOX-compliant audit trail" and returned
        {"type": "SOX", "attestation": "ZkP_Hash"} for every input, without reading `data` at
        all. The literal string "ZkP_Hash" was presented as a zero-knowledge attestation, so a
        consumer reads it as cryptographic evidence that a SOX control test passed. No control
        test runs here, no proof is generated, and this deployment has no attestation authority.
        The only fact this function can honestly state about `data` is a digest of it.
        """
        payload = json.dumps(data, sort_keys=True, default=str) if data else ""
        logger.info("IAGF: Digesting the payload for the SOX audit trail (no attestation issued).")
        return {
            "type": "SOX",
            "attestation": None,
            "payload_sha3_512": hashlib.sha3_512(payload.encode("utf-8")).hexdigest(),
            "note": ("No SOX attestation was produced — no control test ran and there is no "
                     "attestation authority on this deployment. Only the payload digest is real."),
        }

class HealthcareHIPAAAdapter(IndustryAdapter):
    """ARTICLE 184: Healthcare compliance."""
    def audit_trail(self, data: Dict[str, Any]):
        """Say that no redaction ran, rather than claiming the payload was sanitised.

        W409 — this logged "Triggering PHI redaction for HIPAA compliance" and returned
        {"type": "HIPAA", "sanitized": True} for every input, without reading `data`. Executed on
        {"patient_ssn": "123-45-6789", "notes": "HIV positive"} it reported sanitized=True with
        the SSN entirely untouched: the caller is told the PHI is gone while still holding it,
        which is the shape that gets unredacted PHI forwarded. No PHI redactor exists anywhere in
        this repo, so the honest answer is that nothing was redacted.
        """
        logger.info("IAGF: No PHI redactor is implemented — reporting the payload as unsanitised.")
        return {
            "type": "HIPAA",
            "sanitized": False,
            "redaction": "NOT_IMPLEMENTED",
            "note": ("No PHI redaction ran. The payload is unchanged and must not be treated as "
                     "de-identified."),
        }

class IslamicFinanceAdapter(IndustryAdapter):
    """ARTICLE 184: Islamic Finance compliance."""
    def audit_trail(self, data: Dict[str, Any]):
        """Run the REAL §11 Sharia/Halal screen instead of certifying halal by literal.

        W409 — this logged "Verifying Riba-free status and Zakat allocation" and returned
        {"type": "Shariah", "halal": True} for every input, without reading `data`. Executed on
        {"product": "interest-bearing payday loan at 400% APR", "riba": True} it returned
        halal=True — a machine-issued religious certification for a transaction that is riba on
        its face — and no Zakat allocation was ever inspected. The real screen already exists:
        api/compliance.screen_compliance invokes HalalComplianceOfficer plus the §11 haram
        vocabulary and gates deliveries elsewhere in the platform.
        """
        subject = json.dumps(data, sort_keys=True, default=str) if data else ""
        try:
            from agentic_core.api.compliance import screen_compliance
            verdict = next((v for v in screen_compliance(subject).get("verdicts", [])
                            if v.get("framework") == "sharia_halal"), None)
            if verdict is None:
                raise RuntimeError("the screen returned no sharia_halal verdict")
            logger.info(f"IAGF: Sharia screen → {verdict['status']}: {verdict['reason']}")
            return {
                "type": "Shariah",
                "halal": verdict["status"] == "pass",
                "status": verdict["status"],
                "reason": verdict["reason"],
                "zakat": "NOT_CHECKED",
                "zakat_note": ("No Zakat allocation was inspected — this screen reads the payload "
                               "text only. HalalComplianceOfficer.calculate_zakat computes Zakat "
                               "when assets and the nisab threshold are supplied."),
                "screened_by": "agentic_core.api.compliance.screen_compliance",
            }
        except Exception as exc:
            logger.warning(f"IAGF: Sharia screen unavailable: {exc}")
            return {
                "type": "Shariah",
                "halal": None,
                "status": "not_checked",
                "detail": ("The Sharia/Halal screen could not run, so no halal verdict is given: "
                           + str(exc)[:160]),
            }

class IndustryType:
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    HEALTH = "healthcare" # Alias for compatibility
    RELIGION = "religion"

class IndustryAdaptiveGovernance:
    def __init__(self):
        self.adapters = {
            IndustryType.FINANCE: FinancialServicesAdapter(),
            IndustryType.HEALTHCARE: HealthcareHIPAAAdapter(),
            IndustryType.RELIGION: IslamicFinanceAdapter()
        }

    def apply_profile(self, industry: str) -> Dict[str, Any]:
        """Article 184: Apply industry-specific governance profile."""
        logger.info(f"IAG: Applying profile for {industry}")
        if industry == IndustryType.HEALTHCARE or industry == IndustryType.HEALTH:
            return {"phi_protection": True, "compliance": "HIPAA"}
        elif industry == IndustryType.FINANCE:
            # W409 — this returned {"compliance": "SOX", "riba_free": True}: a Shariah verdict
            # issued by the SOX profile, from no transaction and no screen. Unlike the other keys
            # here, riba_free is not a profile REQUIREMENT — it is a finding — so asserting it
            # true told the caller a riba screen had passed when none had run. Selecting a profile
            # audits nothing; IslamicFinanceAdapter.audit_trail(data) above runs the real screen.
            return {"compliance": "SOX", "riba_free": None,
                    "riba_note": ("Not screened — apply_profile selects a profile, it audits "
                                  "nothing. Use IslamicFinanceAdapter.audit_trail(data) for a "
                                  "real riba screen.")}
        return {"compliance": "GENERIC"}
