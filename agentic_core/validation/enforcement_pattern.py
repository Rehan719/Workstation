from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    passed: bool
    violation: Optional[str] = None
    details: Any = None

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
        """Validate target against all registered constraints."""
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
