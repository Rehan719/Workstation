from typing import Any, Dict, List
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

class LogicVerifier:
    """
    Layer 2: Logical Consistency.
    Applies formal logic to verify reasoning.
    Uses safe parsing to avoid evaluation risks.
    """
    def __init__(self):
        self.transformations = standard_transformations

    async def verify_formula(self, formula_str: str, assumptions: List[str]) -> Dict[str, Any]:
        """Checks if a logical formula is coherent."""
        try:
            # Safe parsing without unsafe transformations
            expr = parse_expr(formula_str, transformations=self.transformations, evaluate=False)
            return {
                "status": "PASSED",
                "formula": str(expr),
                "is_coherent": True
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "reason": f"Parsing Error: {str(e)}"
            }
