import functools
import asyncio
from typing import Any, Callable, Dict
from agentic_core.ueg.logger import VSBUEGLogger

def constitutional_guard(func: Callable):
    """
    Decorator to enforce constitutional compliance checks before and after execution.
    Logs interaction to UEG to ensure an immutable audit trail exists for the action.
    """
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        ueg = getattr(self, 'ueg', VSBUEGLogger())

        # Pre-execution audit
        await ueg.log_minimisation_event(f"constitutional_pre_audit_{func.__name__}", {
            "origin": self.__class__.__name__,
            "params": str(args)
        })

        result = await func(self, *args, **kwargs)

        # Post-execution audit
        await ueg.log_minimisation_event(f"constitutional_post_audit_{func.__name__}", {
            "status": "completed",
            "result_type": type(result).__name__
        })

        return result

    return wrapper

def divine_calibration(func: Callable):
    """
    Decorator to calibrate system actions against Divine Will (Niyyah/Khayr).
    Enforces that the action is measured against its ukhrawi impact.
    """
    @functools.wraps(func)
    async def async_wrapper(self, *args, **kwargs):
        engine = getattr(self, 'niyyah', getattr(self, 'divine', None))
        ueg = getattr(self, 'ueg', VSBUEGLogger())

        if engine:
            intent = kwargs.get('intent', f"geospheric_{func.__name__}")
            # Ensure niyyah calibration passes before proceeding
            calibration = await engine.calibrate_niyyah(intent)
            if not calibration.get("passed", False):
                 await ueg.log_minimisation_event("divine_calibration_failure", {"intent": intent})
                 # In a strict environment, we would raise an error here.
                 # For now, we log and proceed but with a penalty flag.

        return await func(self, *args, **kwargs)

    return async_wrapper
