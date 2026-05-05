import pandas as pd
from decimal import Decimal
from typing import Dict, Any
from src.organism.python.evidence.graph_schema import EvidenceGraph

class ScheduleOfLossAgent:
    """
    Deterministic calculation for UK Employment Tribunal Schedule of Loss.
    Uses statutory caps verified for 2026.
    """
    # Statutory Caps as of April 6, 2026
    WEEKLY_PAY_CAP = Decimal("751.00")
    COMPENSATORY_AWARD_CAP = Decimal("123543.00")

    def calculate(self, employee_data: Dict[str, Any], graph: EvidenceGraph) -> pd.DataFrame:
        """
        Generates a Schedule of Loss based on employee data and evidence.
        """
        losses = []

        # 1. Basic Award (Unfair Dismissal)
        # Simplified formula: age factor * tenure * weekly pay
        age = employee_data.get("age", 30)
        tenure = employee_data.get("years_of_service", 2)
        weekly_pay = min(Decimal(str(employee_data.get("gross_weekly_pay", 500))), self.WEEKLY_PAY_CAP)

        # Age factors: <22 = 0.5, 22-40 = 1, >41 = 1.5
        age_factor = 1.0
        if age < 22:
            age_factor = 0.5
        elif age >= 41:
            age_factor = 1.5

        basic_award = Decimal(str(age_factor)) * Decimal(str(tenure)) * weekly_pay
        losses.append({
            "Head of Claim": "Basic Award (Unfair Dismissal)",
            "Statutory Basis": "ERA 1996 s.119",
            "Calculation": f"{age_factor} * {tenure} yrs * £{weekly_pay}",
            "Amount": float(basic_award)
        })

        # 2. Loss of Earnings (Compensatory)
        # In a real scenario, this would be derived from the EvidenceGraph (e.g. dismissal date to tribunal date)
        # Simulation: 26 weeks loss
        lost_weeks = 26
        net_pay = Decimal(str(employee_data.get("net_weekly_pay", 400)))
        comp_loss = min(lost_weeks * net_pay, self.COMPENSATORY_AWARD_CAP)

        losses.append({
            "Head of Claim": "Compensatory Award (Loss of Earnings)",
            "Statutory Basis": "ERA 1996 s.123",
            "Calculation": f"{lost_weeks} weeks * £{net_pay}",
            "Amount": float(comp_loss)
        })

        # 3. Injury to Feelings (Discrimination) - Vento Middle Band 2026
        # Middle band starts at £12,600
        losses.append({
            "Head of Claim": "Injury to Feelings",
            "Statutory Basis": "EqA 2010 s.124 (Vento)",
            "Calculation": "Middle Band (Moderate severity)",
            "Amount": 15000.00
        })

        df = pd.DataFrame(losses)
        return df
