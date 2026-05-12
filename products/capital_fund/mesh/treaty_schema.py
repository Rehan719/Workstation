from pydantic import BaseModel
class BilateralTreaty(BaseModel):
    treaty_id: str
    node_a: str
    node_b: str
    liquidity_cap_pct: float = 5.0
    profit_share: float = 0.5
    duration_days: int = 30
    status: str = "PROPOSED"
