"""
Constitutional Clearance Chain (vΩ∞-AVATAR-OMNISYNTHESIS).
Five-gate validation for every avatar instructional emission.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time
import logging
from agentic_core.cognitive.registry import EngineType
from agentic_core.attestation import attest as _attest
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

logger = logging.getLogger(__name__)

@dataclass
class ClearanceResult:
    """P3.14 — a verdict that says what every gate decided, not only whether the chain cleared.

    `gates` carries one record per gate: cleared, blocked, or NOT_EVALUATED. The chain returns on the first
    block, so without that third state a reader could not tell a gate that approved from one that never ran,
    and a blocked result used to discard the gates that had already cleared.
    """
    passed: bool
    reason: Optional[str] = None
    #  P3.15 — records, not literals. Each value is an attestation record from agentic_core.attestation:
    #  either a real HMAC-SHA3-512 signature over the gate's canonical verdict, or a stated refusal naming
    #  the missing key. The type widened from Dict[str, str] and its only reader is updated with it.
    attestations: Dict[str, Any] = None
    gates: Optional[List[Dict[str, Any]]] = None
    #  P3.15 — replaces `attestations_are_placeholders`. Nothing writes a placeholder now, so a field whose
    #  name asserted that they were placeholders would itself be the untrue claim this item removes. False
    #  here means the platform has no attestation key configured, NOT that a placeholder was written.
    attestations_signed: bool = False
    attestations_basis: Optional[str] = None

class ConstitutionalClearanceChain:
    """
    ARTICLE 1134: Five-gate constitutional clearance chain.
    Mushāwara → Niyyah → Tawazun → Tafakkur → Tahqeeq.
    Ensures absolute pedagogical safety and legal precision.
    """
    def __init__(self, ueg_logger: Any, cognitive_orchestrator: Any):
        self.ueg = ueg_logger
        self.orchestrator = cognitive_orchestrator
        self.enforcement = OmniEnforcementPatternSupreme(
            {"fail_on_missing_validator": False},
            {"task": "avatar_clearance_omega"}
        )
        #  W553 (FU-358) — REGISTERED HERE, at construction. A validator nobody registers is a validator
        #  that is not on the path, which is the reach failure this plan keeps finding; leaving it to a
        #  caller to remember is how nineteen declared constraints came to have no implementation between
        #  them. Four assess, fifteen return NOT ASSESSABLE with a named reason, and the pattern therefore
        #  cannot CLEAR — which is the honest state and a different statement from a constraint having
        #  been violated.
        #
        #  AND THIS CHAIN DOES NOT YET CONSULT IT (FU-364, measured in W553 by grepping its own body):
        #  `self.enforcement` is constructed and registered here and `validate` is never called on it.
        #  The pattern that IS consulted is the recirculation orchestrator's, which it hands to the VRPR
        #  pipeline and the cognitive orchestrator; that verdict and its basis reach a surface. So the
        #  registration here is correct and NOT yet load-bearing, which is said plainly rather than left
        #  for a reader to infer from a registry attribute that looks like enforcement.
        from agentic_core.validation.constitutional_validators import register_all as _register
        self.enforcement_registry = _register(self.enforcement)

    #  The five gates in order, with the FIELD each one reads and the placeholder attestation key.
    #  Named as data so the chain cannot silently grow a sixth gate that nothing records.
    _GATES = (
        ("mushawara", "Mushāwara", "deliberative consensus across cognitive perspectives"),
        ("niyyah", "Niyyah", "intent ratification"),
        ("tawazun", "Tawazun", "balance between depth and cognitive load"),
        ("tafakkur", "Tafakkur", "reflection on downstream effects"),
        ("tahqeeq", "Tahqeeq", "output verification against hard constraints"),
    )

    @staticmethod
    def _record(key: str, name: str, subject: str, verdict: str, basis: str) -> Dict[str, Any]:
        return {"gate": key, "name": name, "subject": subject, "verdict": verdict, "basis": basis}

    @staticmethod
    def _attest_gate(emission: Dict[str, Any], record: Dict[str, Any]) -> Dict[str, Any]:
        """Attest a gate's OWN verdict, rather than passing through whatever string the engine offered.

        The five literals this replaces were DEFAULTS on the engine's own field, so an engine that returned
        nothing produced an attestation indistinguishable from one that had signed — which is what made them
        decoration rather than evidence. What is signed here is the verdict this chain itself reached. The
        replaced expressions are in the commit message, not here, because a guard forbids them in source.
        """
        return _attest({"gate": record["gate"],
                        "emission_id": emission.get("id"),
                        "verdict": record["verdict"],
                        "basis": record["basis"]})

    @staticmethod
    def _attestation_state(attestations: Dict[str, Any]) -> tuple:
        """Whether EVERY attestation is signed, and a basis a reader can act on."""
        if not attestations:
            return False, "no gate was attested, because no gate cleared"
        unsigned = sorted(k for k, v in attestations.items()
                          if not (isinstance(v, dict) and v.get("signed")))
        if unsigned:
            return False, (f"{len(unsigned)} of {len(attestations)} gate attestation(s) are NOT SIGNED "
                           f"({', '.join(unsigned)}): no attestation key is configured, so the chain "
                           "recorded a stated refusal rather than a placeholder signature")
        return True, (f"all {len(attestations)} gate attestation(s) carry an HMAC-SHA3-512 signature over "
                      "the gate's canonical verdict, under the configured key")

    def _blocked(self, gates: List[Dict[str, Any]], attestations: Dict[str, str],
                 idx: int, reason: str) -> ClearanceResult:
        """Return a block that keeps what the earlier gates decided and says the rest never ran."""
        for key, name, subject in self._GATES[idx + 1:]:
            gates.append(self._record(key, name, subject, "not_evaluated",
                                      "the chain returned at an earlier gate, so this gate never ran - "
                                      "which is not the same as approving"))
        _signed, _basis = self._attestation_state(attestations)
        return ClearanceResult(False, reason, attestations=dict(attestations), gates=gates,
                               attestations_signed=_signed, attestations_basis=_basis)

    async def validate_emission(self, emission: Dict[str, Any], context: Dict[str, Any]) -> ClearanceResult:
        """Run the five-gate clearance chain. A gate with no input BLOCKS.

        P3.14. THREE of the five gates read their field with a default that meant APPROVAL, so an engine
        returning an empty dict cleared them. Gate 1 indexed its field directly and RAISED instead, which is
        not clearing but is not a refusal either. Gate 2 was already correct. Every gate now requires its
        field to be PRESENT and affirmative, and says so when it is not. The replaced expressions are
        recorded in the commit message rather than quoted here, where a guard reads.
        """
        attestations: Dict[str, str] = {}
        gates: List[Dict[str, Any]] = []

        def _missing(field: str, res: Any) -> str:
            return (f"the engine returned no '{field}' field, so nothing affirms this gate. A missing "
                    f"answer is not approval - it is an engine that did not answer "
                    f"(received: {type(res).__name__} with "
                    f"{sorted(res)[:6] if isinstance(res, dict) else 'no fields'})")

        # ── GATE 1: Mushāwara — deliberative consensus (≥3 engines) ─────────────────────────────
        key, name, subject = self._GATES[0]
        try:
            mushawara_res = await self.orchestrator.consult(emission, ["inkashaf", "aqal", "samajh"])
        except Exception as exc:                          # noqa: BLE001 — a crash is a BLOCK with a reason
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      f"the deliberation call itself failed: "
                                      f"{exc.__class__.__name__}: {exc}")],
                attestations, 0, f"Gate 1 ({name}) Block: the deliberation call failed")
        # This gate raised KeyError before P3.14 — a crash rather than a verdict.
        _status = mushawara_res.get("status") if isinstance(mushawara_res, dict) else None
        if _status != "APPROVED":
            _basis = (_missing("status", mushawara_res) if _status is None else
                      f"deliberation returned status {_status!r}, not APPROVED")
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked", _basis)],
                attestations, 0,
                # the engine's own reason when it gave one, otherwise the basis computed above. Falling
                # straight through to `.get('reason')` printed "Block: None", which tells a caller nothing
                # while a precise reason had already been worked out one line earlier.
                f"Gate 1 ({name}) Block: "
                f"{(mushawara_res.get('reason') if isinstance(mushawara_res, dict) else None) or _basis}")
        _rec = self._record(key, name, subject, "cleared", "deliberation returned status APPROVED")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 2: Niyyah — intent ratification ───────────────────────────────────────────────
        #  This gate was ALREADY correct before P3.14: its default was negative, so a missing field
        #  blocked. Its behaviour is unchanged, and that is recorded here because a round claiming to have
        #  fixed all five gates would be reporting work it did not do.
        key, name, subject = self._GATES[1]
        niyyah_res = await self.orchestrator.process_engine("niyyah", emission, context)
        _rat = niyyah_res.get("ratified") if isinstance(niyyah_res, dict) else None
        if _rat is not True:
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      _missing("ratified", niyyah_res) if _rat is None else
                                      "intent was not ratified: the quorum of signatures was not met")],
                attestations, 1, f"Gate 2 ({name}) Block: Intent failed ratification")
        _rec = self._record(key, name, subject, "cleared", "intent ratified against a stated quorum")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 3: Tawazun — balance between depth and cognitive load ─────────────────────────
        key, name, subject = self._GATES[2]
        tawazun_res = await self.orchestrator.process_engine("tawazun", emission, context)
        _bal = tawazun_res.get("balanced") if isinstance(tawazun_res, dict) else None
        if _bal is not True:                              # the old default here approved on absence
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      _missing("balanced", tawazun_res) if _bal is None else
                                      "the emission was assessed as unbalanced for its audience")],
                attestations, 2, f"Gate 3 ({name}) Block: Cognitive load imbalance")
        _rec = self._record(key, name, subject, "cleared", "balance affirmed by the engine")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 4: Tafakkur — reflection on downstream effects ────────────────────────────────
        key, name, subject = self._GATES[3]
        tafakkur_res = await self.orchestrator.process_engine("tafakkur", emission, context)
        _risk = tafakkur_res.get("risk_score") if isinstance(tafakkur_res, dict) else None
        if _risk is None:                                 # the old default read absence as NO RISK
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      "the engine reported no 'risk_score', and an unmeasured risk is not "
                                      "a zero risk. This gate previously read a missing score as 0.0, "
                                      "which is the strongest possible pass")],
                attestations, 3, f"Gate 4 ({name}) Block: downstream risk not assessed")
        if not isinstance(_risk, (int, float)) or isinstance(_risk, bool):
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      f"'risk_score' is not a number but a {type(_risk).__name__}, so it "
                                      f"cannot be compared with the threshold")],
                attestations, 3, f"Gate 4 ({name}) Block: risk score is not a number")
        if _risk > 0.15:
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      f"downstream risk {_risk} exceeds the threshold 0.15")],
                attestations, 3, f"Gate 4 ({name}) Block: Downstream risk threshold exceeded")
        _rec = self._record(key, name, subject, "cleared",
                            f"downstream risk {_risk} is within the threshold 0.15, which is a "
                            f"DEFAULT this repository has not tuned against its own history")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 5: Tahqeeq — output verification ──────────────────────────────────────────────
        key, name, subject = self._GATES[4]
        tahqeeq_res = await self.orchestrator.verify_output(emission)
        _ver = tahqeeq_res.get("verified") if isinstance(tahqeeq_res, dict) else None
        if _ver is not True:                              # the old default here approved on absence
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      _missing("verified", tahqeeq_res) if _ver is None else
                                      f"verification failed: "
                                      f"{tahqeeq_res.get('reason') if isinstance(tahqeeq_res, dict) else 'no reason given'}")],
                attestations, 4,
                f"Gate 5 ({name}) Block: "
                f"{(tahqeeq_res.get('reason') if isinstance(tahqeeq_res, dict) else None) or _missing('verified', tahqeeq_res)}")
        _rec = self._record(key, name, subject, "cleared", "output verified against hard constraints")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # Log completion of the clearance cycle to UEG. `gates_passed` is COUNTED from the records rather
        # than written as 5, so a chain that grows a gate cannot keep reporting the old number.
        _signed, _basis = self._attestation_state(attestations)
        await self.ueg.log_event("CONSTITUTIONAL_CLEARANCE_CONVERGED", {
            "emission_id": emission.get("id"),
            "gates_passed": sum(1 for g in gates if g["verdict"] == "cleared"),
            "gates_declared": len(self._GATES),
            "attestations": attestations,
            "attestations_signed": _signed,
            "attestations_basis": _basis,
        })

        return ClearanceResult(True, attestations=attestations, gates=gates,
                               attestations_signed=_signed, attestations_basis=_basis)
