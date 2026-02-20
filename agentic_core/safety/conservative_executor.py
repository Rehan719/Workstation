from typing import Dict, Any, List, Callable, Awaitable
import asyncio
import traceback
from datetime import datetime

class ConservativeExecutor:
    """
    Article Q: Conservative Execution Mandate.
    Prioritizes correctness, reliability, and verifiability over aggressive optimization.
    Wraps high-risk actions with fallback procedures and strict monitoring.
    """
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.anomaly_log = []

    async def execute_safely(self, action_fn: Callable[..., Awaitable[Any]], *args, **kwargs) -> Dict[str, Any]:
        """
        Executes an action with retries, fallback, and anomaly reporting.
        """
        retries = 0
        last_error = None

        while retries < self.max_retries:
            try:
                print(f"🛡️ [Article Q] Executing high-risk action (Attempt {retries + 1})...")
                result = await action_fn(*args, **kwargs)
                return {"status": "success", "result": result}
            except Exception as e:
                retries += 1
                last_error = str(e)
                self._report_anomaly(e, action_fn.__name__)
                await asyncio.sleep(2 ** retries) # Exponential backoff

        # Final Fallback logic
        return self._handle_failure(last_error)

    def _report_anomaly(self, error: Exception, context: str):
        """Article Q: Real-time anomaly reporting."""
        anomaly = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "error": str(error),
            "traceback": traceback.format_exc(),
            "severity": "CRITICAL"
        }
        self.anomaly_log.append(anomaly)
        print(f"🚨 [ANOMALY DETECTED] in {context}: {error}")

    def _handle_failure(self, last_error: str) -> Dict[str, Any]:
        """Article Q: Default to safe/conservative fallback state."""
        return {
            "status": "fallback",
            "message": "Max retries reached. Defaulting to conservative safety state.",
            "error": last_error
        }
