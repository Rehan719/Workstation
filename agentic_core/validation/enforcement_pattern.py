from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    #  W547 (FU-235) — THREE-STATE. None means no check could be obtained, which is not a pass and not a
    #  failure. Every existing reader tests `if not result.passed`, so None routes to the violation
    #  handler — the fail-closed direction, which is the right default for a constitutional check.
    passed: Optional[bool]
    violation: Optional[str] = None
    details: Any = None
    basis: str = ""

class UniversalEnforcementPattern:
    """
    Reusable, reconfigurable enforcement pattern for all constitutional and technical constraints.
    Ensures zero bypasses and consistent action on failure across all components.
    """
    def __init__(self, constraint_config: Dict[str, Any], context: Any):
        self.config = constraint_config
        self.context = context
        self.validators = {} # To be populated by specific validator instances

    def register_validator(self, name: str, validator: Any):
        self.validators[name] = validator

    def validate(self, target: Any) -> ValidationResult:
        """Validate target against all registered constraints — and refuse to answer with none.

        W547 (FU-235) — THIS RETURNED passed=True OVER AN EMPTY VALIDATOR DICT. `self.validators` starts
        as {} and nothing in this repository calls register_validator, so the loop below iterated nothing
        and the method reported a clean constitutional pass. ZERO CHECKS IS NOT A PASS: it is the
        strongest possible claim resting on the least possible evidence, and it was the default state.

        MEASURED CORRECTION TO THE ROW THAT ASKED FOR THIS: the defect is LATENT, not live. Nothing
        instantiates this base class — the clearance chain and the recirculation orchestrator both use
        OmniEnforcementPatternSupreme, whose validate() fails closed on a missing validator. So the live
        consequence was the opposite one (every validation refuses), and this class was a trap waiting
        for the first caller to construct it directly.
        """
        if not self.validators:
            return ValidationResult(
                passed=None, violation=None, details=[],
                basis=("NOT ASSESSED: no validator is registered on this enforcement pattern, so nothing "
                       "was checked. This is not a pass — a constitutional verdict over zero checks is a "
                       "claim with no evidence behind it. Register validators, or read this None as the "
                       "refusal it is"))
        results = []
        for name, validator in self.validators.items():
            # In a concrete implementation, validator would have a .validate method
            try:
                result = validator.validate(target, self.context)
                if not result.passed:
                    return self._handle_violation(name, result)
                results.append(result)
            except Exception as e:
                return self._handle_violation(name, ValidationResult(passed=False, details=str(e)))

        return ValidationResult(passed=True, details=results)

    def _handle_violation(self, name: str, result: ValidationResult) -> ValidationResult:
        """Handle constraint violation based on reconfigurable action policy."""
        action = self.config.get(name, {}).get("action_on_violation", "log")

        # Log to UEG implicitly via the result objects
        # In production, this would trigger specific handlers (Halt, Block, Quarantine, Fallback)
        print(f"!!! CONSTRAINT VIOLATION: {name} | Action: {action} !!!")

        return ValidationResult(passed=False, violation=name, details=result)
