from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from agentic_core.validation.enforcement_pattern import UniversalEnforcementPattern, ValidationResult

@dataclass
class SupremeValidationResult(ValidationResult):
    phase: int = 0
    timestamp: str = ""

class OmniEnforcementPatternSupreme(UniversalEnforcementPattern):
    def __init__(self, constraint_config: Dict[str, Any], context: Any):
        super().__init__(constraint_config, context)
        self.phases = {1: ["zero_placeholder", "edge_first_sovereignty"], 2: ["causal_sovereignty", "thermodynamic_accountability"], 3: ["constitutional_compliance", "biomimetic_fidelity", "genetic_immune_topology_integrity"], 4: ["statistical_rigor", "legal_precision_hard", "adversarial_co_evolution", "trillion_token_provenance", "human_ai_constitutional_co_sovereignty", "oam_qkd_software_only", "federated_consensus", "commercial_integrity", "hallucination_containment", "first_principles_grounding", "sincerity_integrity_loyalty"], 5: ["lob_fixpoint"]}

    def validate(self, target: Any) -> ValidationResult:
        """Three outcomes, because a constraint with no instrument is neither a pass nor a breach.

        W553 (FU-358) — this returned True or a violation, so the nineteen declared constraints could only
        ever be "fine" or "breached", and with none registered every action was a breach. The third state
        is ADDED, not substituted: a False still stops the chain immediately and all-True still clears, so
        no existing reader changes behaviour (each tests `if not res.passed`, and None is falsy, so a
        not-cleared chain still withholds). What changes is that it now withholds for a NAMED reason —
        "four of nineteen constraints have an instrument" — instead of for want of any validator at all.
        """
        assessed, unassessable, no_instrument, input_absent = [], [], [], []
        for phase_id in sorted(self.phases.keys()):
            for name in self.phases[phase_id]:
                validator = self.validators.get(name)
                if not validator:
                    if self.config.get("fail_on_missing_validator", True):
                        return self._handle_violation(name, ValidationResult(passed=False, details="Missing validator"))
                    continue
                res = validator.validate(target, self.context)
                #  a REAL breach stops the chain here, exactly as before
                if res.passed is False:
                    return self._handle_violation(name, res)
                if res.passed is None:
                    unassessable.append(name)
                    #  WHICH KIND of unassessable: no instrument at all, or an instrument whose input was
                    #  not supplied. A first draft of this basis called all of them "no instrument", which
                    #  was wrong for thermodynamic_accountability — the ledger exists and is honest, and
                    #  nothing had handed it a metering record. Different fact, different fix.
                    if isinstance(getattr(res, "details", None), dict) and res.details.get("no_instrument"):
                        no_instrument.append(name)
                    else:
                        input_absent.append(name)
                else:
                    assessed.append(name)
        _total = len(assessed) + len(unassessable)
        #  ZERO CONSTRAINTS IS NOT A PASS, and this branch is reachable: the clearance chain constructs
        #  this pattern with fail_on_missing_validator False, so before W553 registered anything the loop
        #  skipped all nineteen and returned True — a clearance over no checks at all, which is the very
        #  defect FU-358 names, sitting one level above the screens.
        if _total == 0:
            return ValidationResult(
                passed=None, violation=None, details={"assessed": [], "unassessable": []},
                basis=("NOT CLEARED: not one of the declared constraints was evaluated, because none is "
                       "registered on this pattern. Zero checks is the strongest possible claim resting "
                       "on the least possible evidence, so it is reported as unassessed rather than as a "
                       "pass"))
        if unassessable:
            #  NOT CLEARED. The chain cannot clear on a subset: clearing with fifteen of nineteen
            #  unassessed would be the "certifies an absence" defect one level up from the screens.
            return ValidationResult(
                passed=None, violation=None,
                details={"assessed": assessed, "unassessable": unassessable,
                         "no_instrument": no_instrument, "input_absent": input_absent},
                basis=(f"NOT CLEARED: {len(assessed)} of {_total} declared constraint(s) were assessed "
                       f"and passed. {len(no_instrument)} have NO INSTRUMENT in this repository and each "
                       f"says so by name; {len(input_absent)} {'HAS' if len(input_absent) == 1 else 'HAVE'} an instrument that was not given its "
                       f"input ({', '.join(input_absent) or 'none'}) — a different fact with a different "
                       f"fix. This is not a breach and it is not a pass: the chain withholds because it "
                       f"cannot check itself, which is not the same as a constraint being violated"))
        return ValidationResult(
            passed=True, violation=None, details={"assessed": assessed},
            basis=f"all {_total} declared constraint(s) were assessed and passed")

    def _handle_violation(self, name: str, result: ValidationResult) -> ValidationResult:
        print(f"!!! SUPREME CONSTRAINT VIOLATION: {name} !!!")
        return ValidationResult(passed=False, violation=name, details=result.details)
