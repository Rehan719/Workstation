"""The constitutional validators: FOUR that assess, FIFTEEN that refuse by name (FU-358).

WHY NOT NINETEEN. OmniEnforcementPatternSupreme declares nineteen constraint names across five phases
and not one had an implementation, so every enforcement check refused and the recirculation loop's normal
outcome was WITHHELD. The fix is NOT nineteen validators. Three of those names — `statistical_rigor`,
`first_principles_grounding` and `sincerity_integrity_loyalty` — have no instrument anywhere in this
repository, and A VALIDATOR THAT RETURNS A NUMBER IT INVENTED IS WORSE THAN A MISSING ONE, because the
missing one refuses. They are registered as permanently NOT ASSESSABLE and marked so that a later round
cannot quietly turn them into scores.

THE FOUR THAT ASSESS EACH REUSE AN EXISTING HONEST CHECK rather than inventing a second screen:

  zero_placeholder            the rule this programme enforces by hand every round, made executable.
  thermodynamic_accountability  the TFEL's metered bits, which became real measurements in W546 when six
                              invented constants were replaced by the measured size of each payload.
  constitutional_compliance   delegates to ConstitutionalPolicyGate.validate_output — the screen that
                              already exists, so there is no second list of forbidden patterns to drift.
  hallucination_containment   delegates to HallucinationSandbox, which W415 already made honest. ITS
                              LIMIT TRAVELS WITH IT: a pass means two heuristics flagged nothing, never
                              that an output was verified. Nothing in this repository measures fidelity.

AND THE OTHER TWELVE REFUSE WITH A NAMED REASON. An unassessable constraint is not a failure and not a
pass: it is a constraint with no instrument, and saying which is the whole point. The chain reads these
three states and cannot CLEAR while any of them is unassessable — so it still withholds, but now for a
reason a reader can act on rather than for want of any validator at all.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

from agentic_core.validation.enforcement_pattern import ValidationResult

#  The three names that must never become a score. Checked by a guard, because the temptation to supply
#  a plausible number for "statistical rigor" is exactly what this list exists to resist.
NEVER_A_SCORE: Tuple[str, ...] = (
    "statistical_rigor", "first_principles_grounding", "sincerity_integrity_loyalty",
)

#  Why each unassessable constraint has no instrument. A reason is required: "not implemented" tells a
#  reader nothing about what would change it.
NO_INSTRUMENT: Dict[str, str] = {
    "edge_first_sovereignty": (
        "nothing here measures where a computation ran. There is no execution-locality record to read, so "
        "an edge-first claim would be a claim about infrastructure this process cannot observe"),
    "causal_sovereignty": (
        "a causal claim needs an intervention or a model to test it against. agentic_core/simverse holds "
        "an emulator that schedules nothing, so there is no causal apparatus to consult"),
    "biomimetic_fidelity": (
        "fidelity to a biological analogue is not a measurable property of an output. W543 found the six "
        "biogeochemical cycles bound to nothing and three outside briefs describing them as a running "
        "control layer; a fidelity figure here would be that same claim in one number"),
    "genetic_immune_topology_integrity": (
        "the immune system scores a SAMPLE a caller supplies and holds no standing topology figure, which "
        "is the same reason W543 declined to bind the nitrogen cycle to it"),
    "legal_precision_hard": (
        "no verified law corpus exists in this repository. The archived one held 342 rows of simulated "
        "content stamped EXTRACTED, so a legal-precision verdict would rest on text nobody checked"),
    "adversarial_co_evolution": (
        "this names a process over time, not a property of one output. There is no adversarial history to "
        "read, and a per-output verdict would describe something the constraint does not mean"),
    "trillion_token_provenance": (
        "provenance per output EXISTS and is enforced elsewhere (the W479 rule, carried on every answer "
        "this platform serves), but nothing counts tokens across a corpus, so the quantity this "
        "constraint names is not measured"),
    "human_ai_constitutional_co_sovereignty": (
        "co-sovereignty is a governance arrangement, evidenced by the Change Control Agency and the "
        "Board's ratification path rather than by inspecting an output. There is nothing in a text to "
        "measure it against"),
    "oam_qkd_software_only": (
        "no optical or quantum-key hardware is present and none is claimed. The constraint is satisfied "
        "trivially and therefore measures nothing — reporting it as a pass would read as a hardware "
        "attestation"),
    "federated_consensus": (
        "no federation runs. The archived KademliaDHT was a local dict with a DHT's vocabulary (recorded "
        "W544), so there are no peers to reach consensus among"),
    "commercial_integrity": (
        "money here is virtual WST and no real-money rail is enabled, so there is no commercial "
        "transaction whose integrity could be assessed"),
    "lob_fixpoint": (
        "a Löb fixpoint is a property of a proof system this repository does not implement. The "
        "clearance chain's own stability constraint is a separate, driven check"),
    #  the three that must never become scores
    "statistical_rigor": (
        "NO INSTRUMENT, AND THIS ONE MUST NEVER BECOME A SCORE. Rigour is not a quantity an output "
        "carries; a number here would be the most believable fabrication on the page because it would "
        "look like a measurement of method"),
    "first_principles_grounding": (
        "NO INSTRUMENT, AND THIS ONE MUST NEVER BECOME A SCORE. Whether reasoning rests on first "
        "principles is a judgement about an argument, and a figure asserting it would be exactly the "
        "'computed over fabricated inputs' shape this programme keeps removing"),
    "sincerity_integrity_loyalty": (
        "NO INSTRUMENT, AND THIS ONE MUST NEVER BECOME A SCORE — and it is the most important of the "
        "three to refuse. These are qualities OF A PERSON OR AN INTENTION, and Ruling A.9.5 forbids an "
        "AI verdict on anyone's inner state. A number here would breach the ruling, not merely overclaim"),
}


class NotAssessable:
    """A constraint with no instrument. Returns None with its reason — never True, never a number."""

    def __init__(self, name: str, reason: str):
        self.name = name
        self.reason = reason
        self.never_a_score = name in NEVER_A_SCORE

    def validate(self, target: Any, context: Any = None) -> ValidationResult:
        return ValidationResult(
            #  `no_instrument` distinguishes THIS from a real validator that simply lacked its input.
            #  The chain reports the two separately, because "nothing can check this" and "nothing handed
            #  this check its input" are different facts with different fixes.
            passed=None, violation=None,
            details={"constraint": self.name, "no_instrument": True},
            basis=(f"NOT ASSESSABLE ({self.name}): {self.reason}. This is neither a pass nor a breach — "
                   f"it is a constraint with no instrument, and the chain cannot clear while it stands"))


class ZeroPlaceholder:
    """No placeholder stands in for work. The rule this programme enforces by hand, made executable."""

    #  Markers that mean "this is not the real thing". Each has cost this programme a round.
    _MARKERS: Tuple[str, ...] = (
        r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\bXXX\b",
        r"\blorem ipsum\b", r"\bplaceholder\b", r"\bcoming soon\b",
        r"\bnot (?:yet )?implemented\b", r"\bstub(?:bed)?\b",
        r"\bsimulated (?:resolution|result|value|score|output)\b",
        r"\bfor (?:now|demo) purposes\b", r"\bdummy (?:data|value)\b",
    )

    def validate(self, target: Any, context: Any = None) -> ValidationResult:
        if not isinstance(target, str) or not target.strip():
            #  FAIL CLOSED on something it cannot read, rather than passing it.
            return ValidationResult(
                passed=None, violation=None, basis=(
                    "NOT ASSESSABLE (zero_placeholder): the subject is not readable text, so no screen "
                    "ran over it. A screen that did not run is not a screen that passed"))
        hits = [m for p in self._MARKERS for m in re.findall(p, target, re.I)]
        if hits:
            return ValidationResult(
                passed=False, violation="zero_placeholder", details={"markers": sorted(set(hits))[:8]},
                basis=(f"BREACH (zero_placeholder): {len(hits)} placeholder marker(s) in the output — "
                       f"{sorted(set(hits))[:5]}. A placeholder shipped as an answer is work claimed and "
                       f"not done"))
        return ValidationResult(
            passed=True, violation=None,
            basis=("zero_placeholder: no placeholder marker found. THE LIMIT: this screens a fixed list "
                   "of markers, so an unlabelled stub — a plausible sentence over no work — passes it. "
                   "It catches the declared placeholder, not the undeclared one"))


class ThermodynamicAccountability:
    """The information cost must be METERED, read from the ledger's own record."""

    def validate(self, target: Any, context: Any = None) -> ValidationResult:
        rec = (context or {}).get("metering") if isinstance(context, dict) else None
        if not isinstance(rec, dict):
            return ValidationResult(
                passed=None, violation=None, basis=(
                    "NOT ASSESSABLE (thermodynamic_accountability): no metering record was supplied with "
                    "this action, so its information cost is unknown. The ledger exists and is honest "
                    "(core/transcendent_subsystems/tfel.py); nothing handed its record to this check"))
        if rec.get("metered") is not True:
            return ValidationResult(
                passed=False, violation="thermodynamic_accountability",
                details={"basis": rec.get("basis")},
                basis=(f"BREACH: a metering record was supplied and it reports metered={rec.get('metered')!r} "
                       f"— the action ran without its information cost being recorded. "
                       f"{rec.get('basis') or ''}"))
        bits = rec.get("entropy_bits")
        if not isinstance(bits, (int, float)) or bits <= 0:
            return ValidationResult(
                passed=False, violation="thermodynamic_accountability",
                basis=(f"BREACH: the metering record claims metered=True with entropy_bits={bits!r}. A "
                       f"metered operation of zero or absent bits is a record of nothing"))
        return ValidationResult(
            passed=True, violation=None,
            basis=(f"thermodynamic_accountability: {bits} bit(s) metered, from a MEASURED payload size "
                   f"(W546 replaced six invented constants with the real size of what each stage "
                   f"handled). THE LIMIT: payload size is not the number of bits ERASED, which is what "
                   f"Landauer's bound concerns, so the ledger's figure is a floor over a measured "
                   f"quantity and not an energy this platform drew"))


class ConstitutionalCompliance:
    """Delegates to the policy gate that already screens output — one screen, not a second list."""

    def validate(self, target: Any, context: Any = None) -> ValidationResult:
        try:
            from agentic_core.gaas.v5.policy_gate import ConstitutionalPolicyGate
        except Exception as e:                   # noqa: BLE001
            return ValidationResult(
                passed=None, violation=None, basis=(
                    f"NOT ASSESSABLE (constitutional_compliance): the policy gate could not be imported "
                    f"({e.__class__.__name__}), so nothing screened this output"))
        res = ConstitutionalPolicyGate().validate_output(target)
        if not res.get("compliant", True):
            return ValidationResult(
                passed=False, violation="constitutional_compliance",
                details={"violations": res.get("violations")},
                basis=(f"BREACH: the constitutional policy gate found {res.get('violations')}. This is "
                       f"the SAME screen the interceptor runs — there is no second list here to drift "
                       f"from it"))
        return ValidationResult(
            passed=True, violation=None,
            basis=("constitutional_compliance: the policy gate's output screen found nothing. THE LIMIT: "
                   "that screen matches a fixed set of unsafe payload patterns, so it establishes the "
                   "absence of those patterns and not compliance with the constitution as a whole"))


class HallucinationContainment:
    """Delegates to the sandbox W415 made honest. A pass means two heuristics flagged nothing."""

    def validate(self, target: Any, context: Any = None) -> ValidationResult:
        try:
            from agentic_core.governance.gaas.v5.hallucination_sandbox import HallucinationSandbox
        except Exception as e:                   # noqa: BLE001
            return ValidationResult(
                passed=None, violation=None, basis=(
                    f"NOT ASSESSABLE (hallucination_containment): the sandbox could not be imported "
                    f"({e.__class__.__name__})"))
        if not isinstance(target, str) or not target.strip():
            return ValidationResult(
                passed=None, violation=None, basis=(
                    "NOT ASSESSABLE (hallucination_containment): the subject is not readable text"))
        #  W555 (FU-363) — THE SYNC SCREEN, so this assesses on the path that matters. Until this round
        #  the validator called asyncio.run on the sandbox's async validate_output, which raises whenever
        #  an event loop is already running — and the live path always is, because VRPR's process() is
        #  async and the recirculation loop drives it. So the one constraint here that HAS an instrument
        #  could only ever assess from synchronous test code. The sandbox is async because it awaits a
        #  UEG write, not because the screening needs to be: screen() is that same screening, extracted,
        #  and it is the SAME implementation rather than a second copy of two heuristics that would drift.
        #  WHAT IS LOST, and it is stated rather than quietly dropped: this path does not write the
        #  "hallucination_scan_completed" UEG event, because writing it is the async half. The screen's
        #  verdict travels in the chain's result instead.
        try:
            res = HallucinationSandbox().screen(target)
        except Exception as e:                   # noqa: BLE001
            return ValidationResult(
                passed=None, violation=None,
                basis=f"NOT ASSESSABLE (hallucination_containment): the sandbox raised {e.__class__.__name__}")
        #  A PARTIAL SCREEN IS NOT A PASS. screen() reports passed=None with the check NAMED when one of
        #  its two heuristics could not run, and that None must travel rather than being read as a pass.
        if res.get("passed") is None:
            return ValidationResult(
                passed=None, violation=None, details={"checks_not_run": res.get("checks_not_run")},
                basis=(f"NOT ASSESSABLE (hallucination_containment): the screen could not run every "
                       f"heuristic — {res.get('checks_not_run')}. A check that did not run is not a "
                       f"check that passed"))
        if not res.get("passed", True):
            return ValidationResult(
                passed=False, violation="hallucination_containment",
                details={"flags": res.get("hallucinations")},
                basis=f"BREACH: the sandbox's heuristics flagged {res.get('hallucinations')}")
        return ValidationResult(
            passed=True, violation=None, details={"checks_run": res.get("checks_run")},
            #  The checks are NAMED FROM THE SCREEN'S OWN REPORT rather than described from memory: a
            #  sentence listing two heuristics is a claim about what ran, and only the screen knows.
            basis=(f"hallucination_containment: {len(res.get('checks_run') or [])} heuristic(s) ran and "
                   f"flagged nothing — {', '.join(res.get('checks_run') or []) or 'none'}. THE LIMIT, "
                   f"carried from W415 which removed this module's fabricated fidelity score: NOTHING IN "
                   f"THIS REPOSITORY MEASURES FIDELITY. This means those heuristics found nothing, never "
                   f"that the output was verified. It is also the SAME screen the sandbox runs, not a "
                   f"copy of it — the async wrapper adds the UEG write and nothing else"))


#  name -> the validator instance that assesses it
ASSESSING: Dict[str, Any] = {
    "zero_placeholder": ZeroPlaceholder(),
    "thermodynamic_accountability": ThermodynamicAccountability(),
    "constitutional_compliance": ConstitutionalCompliance(),
    "hallucination_containment": HallucinationContainment(),
}


def register_all(pattern: Any) -> Dict[str, Any]:
    """Register EVERY declared constraint on an enforcement pattern, and report which is which.

    Called at the construction sites rather than left for a caller to remember: a validator nobody
    registers is a validator that is not on the path, which is the reach failure this plan keeps finding.
    """
    assessing, refusing = [], []
    for phase in sorted(getattr(pattern, "phases", {})):
        for name in pattern.phases[phase]:
            if name in ASSESSING:
                pattern.register_validator(name, ASSESSING[name])
                assessing.append(name)
            else:
                reason = NO_INSTRUMENT.get(
                    name, "no instrument, and no reason recorded — which is itself a defect")
                pattern.register_validator(name, NotAssessable(name, reason))
                refusing.append(name)
    return {
        "assessing": assessing,
        "refusing": refusing,
        "never_a_score": [n for n in refusing if n in NEVER_A_SCORE],
        "basis": (f"{len(assessing)} of {len(assessing) + len(refusing)} declared constraints have an "
                  f"instrument. The rest return NOT ASSESSABLE with a named reason, so the chain cannot "
                  f"clear — which is the honest state, and a different statement from 'a constraint was "
                  f"violated'. Three of them must never become scores"),
    }
