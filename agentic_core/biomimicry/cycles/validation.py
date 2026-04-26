from typing import Dict, Any, Optional

class ClosedLoopValidator:
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger

    async def record(self, process_name: str, recovered: float, total: float):
        waste = total - recovered
        if self.ueg:
            await self.ueg.log_minimisation_event("closed_loop_audit", {
                "process": process_name,
                "recovered": recovered,
                "total": total,
                "waste": waste
            })

class StatisticalValidator:
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger

    async def record(self, metric_name: str, value: float):
        if self.ueg:
            await self.ueg.log_minimisation_event("statistical_rigor", {
                "metric": metric_name,
                "value": value
            })
