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

def _computed(res: Any) -> Dict[str, Any]:
    """An engine's COMPUTED answer: the registry nests it under `result`; a top-level answer is still read.

    P3.28 — gates 2 to 4 read only the top level, while nine_engine_registry.get_engine_response puts what the
    engine computed under `result`, so Niyyah's `ratified` sat one level below where its gate looked. The nested
    answer wins where both exist, because it is what the engine computed rather than what wrapped it.
    """
    if not isinstance(res, dict):
        return {}
    nested = res.get("result") if isinstance(res.get("result"), dict) else {}
    return {**res, **nested}


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
        #  registration here was correct and NOT yet load-bearing (corrected below: W555 made it so),
        #  which was said plainly rather than left for a reader to infer from a registry attribute that
        #  looks like enforcement.
        from agentic_core.validation.constitutional_validators import register_all as _register
        self.enforcement_registry = _register(self.enforcement)
        #
        #  W555 (FU-364) — AND IT IS CONSULTED NOW, as gate 6. The paragraph above said this
        #  registration was "correct and NOT yet load-bearing"; it is load-bearing from this round, so
        #  that sentence is corrected rather than left standing.
        #
        #  THE CONSEQUENCE, STATED HERE BECAUSE A READER WILL MEET IT AS A BUG OTHERWISE: this chain
        #  CANNOT REACH A CLEARED VERDICT on this deployment. The pattern cannot clear while fifteen of
        #  the nineteen declared constraints have no instrument in this repository, and a constraint
        #  nobody can check is neither a pass nor a breach — so gate 6 blocks, every time, for a reason
        #  it states in full. That is the honest state and not a defect: reading "could not check" as
        #  "checked and fine" at the top of the stack is the certifies-an-absence defect this programme
        #  has spent rounds removing from the screens below. Nothing the platform does changes, because
        #  the live recirculation loop already withholds every emission at gate 1. The cleared verdict
        #  becomes reachable when the constraints become assessable, and a guard drives it today by
        #  registering validators that all assess and pass — because a chain that can never clear under
        #  ANY circumstance would be as useless as one that always does.

    #  The gates in order, with the FIELD each one reads and the placeholder attestation key.
    #  Named as data so the chain cannot silently grow a gate that nothing records — and W555 grew one,
    #  which is what that sentence was written for. gates_declared and gates_passed are both COUNTED
    #  from this tuple, so the figures move with it.
    _GATES = (
        ("mushawara", "Mushāwara", "deliberative consensus across cognitive perspectives"),
        ("niyyah", "Niyyah", "intent ratification"),
        ("tawazun", "Tawazun", "balance between depth and cognitive load"),
        ("tafakkur", "Tafakkur", "reflection on downstream effects"),
        ("tahqeeq", "Tahqeeq", "output verification against hard constraints"),
        #  W555 (FU-364) — THE SIXTH, and it is why this chain holds an enforcement pattern at all.
        #  Until this round the chain constructed one, registered nineteen validators onto it and NEVER
        #  called validate: a constitutional clearance chain that never consulted the constitutional
        #  constraints, with a populated `enforcement_registry` attribute that read exactly like
        #  enforcement to anyone who found it. It consults them now, last, over the emission's own text.
        ("enforcement", "Constitutional constraints",
         "the nineteen declared constraints, each assessed or refusing by name"),
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
        """Run the clearance chain, gate by gate. A gate with no input BLOCKS.

        P3.14. THREE of the five gates that existed then read their field with a default that meant APPROVAL, so an engine
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
        #  P3.28 clause (2) — DECIDE BY COVERAGE, NOT STATUS. This required APPROVED, which a screen cannot
        #  issue, so it could only ever block. It clears on "screened, nothing refused" and refuses on a
        #  refusal; NOT ASSESSED still blocks, because clearing on an absence of flags would be worse than
        #  today's honest abstention.
        if _status not in ("APPROVED", "SCREENED_NO_REFUSAL"):
            _basis = (_missing("status", mushawara_res) if _status is None else
                      f"deliberation returned status {_status!r}, which is neither APPROVED nor screened with "
                      f"no refusal")
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked", _basis)],
                attestations, 0,
                # the engine's own reason when it gave one, otherwise the basis computed above. Falling
                # straight through to `.get('reason')` printed "Block: None", which tells a caller nothing
                # while a precise reason had already been worked out one line earlier.
                f"Gate 1 ({name}) Block: "
                f"{(mushawara_res.get('reason') if isinstance(mushawara_res, dict) else None) or _basis}")
        if _status == "SCREENED_NO_REFUSAL":
            _cov = (mushawara_res.get("coverage") or {}) if isinstance(mushawara_res, dict) else {}
            _rec = self._record(key, name, subject, "cleared",
                                f"cleared BY COVERAGE, not approved: screened by "
                                f"{', '.join(_cov.get('screened_by') or []) or 'an unnamed screen'} and nothing "
                                f"refused. Stated limit: {_cov.get('coverage_limit') or 'not stated'}")
            _rec["coverage"] = _cov
        else:
            _rec = self._record(key, name, subject, "cleared", "deliberation returned status APPROVED")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 2: Niyyah — intent ratification ───────────────────────────────────────────────
        #  This gate was ALREADY correct before P3.14: its default was negative, so a missing field
        #  blocked. Its behaviour is unchanged, and that is recorded here because a round claiming to have
        #  fixed all the gates would be reporting work it did not do.
        key, name, subject = self._GATES[1]
        niyyah_res = await self.orchestrator.process_engine("niyyah", emission, context)
        #  P3.28 — the engine's computed answer is under `result` (nine_engine_registry nests the engine's
        #  metadata there), so reading only the top level made this gate unclearable by construction. The
        #  nested answer is read first; a top-level one is still honoured.
        _rat = _computed(niyyah_res).get("ratified")
        if _rat is not True:
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked",
                                      _missing("ratified", niyyah_res) if _rat is None else
                                      "intent was not ratified: the quorum of signatures was not met")],
                attestations, 1,
                #  P3.28 — say WHICH: an intent that was not assessable (no signatures, no quorum stated) is a
                #  different fact from one that was counted and fell short, and the engine says which
                f"Gate 2 ({name}) Block: "
                + ("Intent failed ratification" if _rat is False else
                   f"intent was not assessable - {_computed(niyyah_res).get('basis') or 'the engine gave no basis'}"))
        _rec = self._record(key, name, subject, "cleared", "intent ratified against a stated quorum")
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 3: Tawazun — balance between depth and cognitive load ─────────────────────────
        key, name, subject = self._GATES[2]
        tawazun_res = await self.orchestrator.process_engine("tawazun", emission, context)
        #  FU-471 (Owner ruling 2026-10-06, option 3) — Tawazun returns a FRONTIER, never a `balanced` key, so
        #  this gate could not clear on the real engine. BALANCED MEANS THE EMITTED DRAFT IS NON-DOMINATED among
        #  the drafts the caller held, under the Owner's recorded objectives. The emitted draft's id travels in
        #  the context; with no id, or an engine that could not assess, the gate blocks and says which.
        _tc3 = _computed(tawazun_res)
        _basis3 = "balance affirmed by the engine"
        if "frontier" in _tc3 or _tc3.get("assessable") is False:
            _emitted = (context or {}).get("emitted_candidate") if isinstance(context, dict) else None
            _front = _tc3.get("frontier") or []
            _n = len((context or {}).get("candidates") or []) if isinstance(context, dict) else 0
            if _tc3.get("assessable") is False:
                _bal, _why3 = None, f"balance was not assessable: {_tc3.get('basis') or 'no basis given'}"
            elif not _emitted:
                _bal, _why3 = None, "no emitted draft was named, so nothing can be placed on the frontier"
            else:
                _bal = _emitted in _front
                _why3 = (f"the emitted draft {_emitted!r} is dominated: the frontier over {_n} draft(s) is "
                         f"{', '.join(_front)}")
            _basis3 = (f"the emitted draft {_emitted!r} is on the frontier over {_n} draft(s) under the Owner's "
                       f"recorded objectives" + (" - EVERY draft held is on it (they are identical, or each "
                                                 "trades off against the others), so this placed nothing below "
                                                 "another" if _n and len(_front) == _n else ""))
        else:
            _bal = _tc3.get("balanced")
            _why3 = (_missing("balanced", tawazun_res) if _bal is None else
                     "the emission was assessed as unbalanced for its audience")
        if _bal is not True:                              # the old default here approved on absence
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked", _why3)],
                attestations, 2, f"Gate 3 ({name}) Block: {_why3}")
        _rec = self._record(key, name, subject, "cleared", _basis3)
        attestations[key] = self._attest_gate(emission, _rec)
        gates.append(_rec)

        # ── GATE 4: Tafakkur — reflection on downstream effects ────────────────────────────────
        key, name, subject = self._GATES[3]
        tafakkur_res = await self.orchestrator.process_engine("tafakkur", emission, context)
        #  P3.28 — Tafakkur reports DRIFT and its own `stable` verdict against a stated threshold; it never
        #  produced a `risk_score`, so this gate could not clear on the real engine. Its own verdict is used
        #  when present, and the legacy risk_score path below is kept for a caller that supplies one.
        _tc = _computed(tafakkur_res)
        if "stable" in _tc or "assessable" in _tc:
            if _tc.get("stable") is not True:
                _why4 = (f"drift {_tc.get('drift')} against threshold {_tc.get('threshold')} is not stable"
                         if _tc.get("stable") is False else
                         f"drift was not measured: {_tc.get('basis') or 'no basis given'}")
                return self._blocked(
                    gates + [self._record(key, name, subject, "blocked", _why4)],
                    attestations, 3, f"Gate 4 ({name}) Block: {_why4}")
            _rec = self._record(key, name, subject, "cleared",
                                f"drift {_tc.get('drift')} is within threshold {_tc.get('threshold')}"
                                + (", which is a DEFAULT this repository has not tuned against its own history"
                                   if _tc.get("threshold_is_a_default") else ""))
        else:
            _risk = _tc.get("risk_score")
            if _risk is None:                             # the old default read absence as NO RISK
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

        # ── GATE 6: the declared constitutional constraints (W555, FU-364) ─────────────────────
        #  THE PATTERN THIS CHAIN HAS ALWAYS HELD, finally consulted. Three outcomes, not two, because
        #  the pattern itself has three: a BREACH blocks with the violated constraint named, and a
        #  NOT-CLEARED blocks too — a constraint with no instrument is neither a pass nor a breach, and
        #  a chain that read "could not check" as "checked and fine" would be the certifies-an-absence
        #  defect at the top of the stack. The pattern's own sentence is carried verbatim into the
        #  reason rather than paraphrased, so the count it reports cannot drift from the count it made.
        key, name, subject = self._GATES[5]
        _subject_text = emission.get("text") or emission.get("content") or ""
        _enf = self.enforcement.validate(_subject_text)
        _verdict = getattr(_enf, "passed", None)
        _enf_basis = (getattr(_enf, "basis", "") or "").strip()
        #  OWNER RULING 2026-10-06 (FU-472, choice 1) — DECIDE BY COVERAGE, the rule gate 1 follows. A
        #  VIOLATION still blocks, and so does a run that checked NOTHING; when every constraint that CAN be
        #  checked passed and none was violated, the gate clears and the record names every constraint that
        #  was NOT checked, so the reader is told exactly what this clearance does not cover. Which declared
        #  constraints apply to a reply at all is the Owner's later review (choice 3).
        _det = getattr(_enf, "details", None) or {}
        _assessed = list(_det.get("assessed") or []) if isinstance(_det, dict) else []
        _unchecked = list(_det.get("unassessable") or []) if isinstance(_det, dict) else []
        _cov6 = None
        if _verdict is None and _assessed and not getattr(_enf, "violation", None):
            _cov6 = {"assessed": _assessed, "not_checked": _unchecked,
                     "no_instrument": list(_det.get("no_instrument") or []),
                     "input_absent": list(_det.get("input_absent") or [])}
            _verdict = "coverage"
        if _verdict not in (True, "coverage"):
            _why = (f"a declared constraint was VIOLATED: {getattr(_enf, 'violation', None)!r}. {_enf_basis}"
                    if _verdict is False else
                    f"the constraints could not all be assessed, so the chain did not clear. {_enf_basis}"
                    if _enf_basis else
                    "the enforcement pattern returned no verdict and no basis, which is itself unassessed")
            return self._blocked(
                gates + [self._record(key, name, subject, "blocked", _why)],
                attestations, 5, f"Gate 6 ({name}) Block: {_why}")
        if _cov6 is not None:
            _rec = self._record(key, name, subject, "cleared", (
                f"cleared BY COVERAGE, not a pass of every declared constraint: {len(_assessed)} assessed and "
                f"passed ({', '.join(_assessed)}); {len(_unchecked)} NOT CHECKED ({', '.join(_unchecked)}) - "
                f"{len(_cov6['no_instrument'])} have no instrument and {len(_cov6['input_absent'])} were not "
                f"given their input"))
            _rec["coverage"] = _cov6
        else:
            _rec = self._record(key, name, subject, "cleared", _enf_basis or (
                "every declared constraint was assessed and passed"))
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
