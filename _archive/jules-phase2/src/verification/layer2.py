from typing import Any, Dict, List
from sympy.logic import satisfiable
from sympy.logic.boolalg import to_cnf
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

class LogicVerifier:
    """
    Layer 2: Logical Consistency.
    v52.0 Mastering: Rigorous satisfiability and contradiction checking.
    """
    def __init__(self):
        self.transformations = standard_transformations

    async def verify_claim(self, claim_formula: str, axioms: List[str]) -> Dict[str, Any]:
        """
        Checks if the claim is consistent with a set of axioms.
        Returns FAILED if axioms & claim is unsatisfiable.
        """
        try:
            # Parse claim and axioms safely
            claim_expr = parse_expr(claim_formula, transformations=self.transformations, evaluate=False)
            axiom_exprs = [parse_expr(a, transformations=self.transformations, evaluate=False) for a in axioms]

            # 1. Internal Consistency of Axioms
            if axiom_exprs:
                kb = axiom_exprs[0]
                for a in axiom_exprs[1:]:
                    kb = kb & a
            else:
                kb = True

            if kb != True and not satisfiable(kb):
                return {"status": "ERROR", "reason": "Background axioms are internally inconsistent."}

            # 2. Consistency of Claim with Axioms
            full_system = kb & claim_expr if kb != True else claim_expr
            if not satisfiable(full_system):
                return {
                    "status": "FAILED",
                    "reason": "Claim contradicts established domain axioms.",
                    "logic_trace": str(to_cnf(full_system))
                }

            return {
                "status": "PASSED",
                "reason": "Claim is logically consistent with provided axioms.",
                "is_tautology": not satisfiable(~claim_expr)
            }

        except Exception as e:
            return {"status": "ERROR", "reason": f"Logic Parsing Error: {str(e)}"}
