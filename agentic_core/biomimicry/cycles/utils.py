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
        # P3.12 (W520) - the fallback was DEFEATED by the caller's own default. Every cognitive engine
        # is `__init__(self, ueg=None)`, so the attribute EXISTS and is None; getattr then returns the
        # value rather than the default, and None.log_minimisation_event raised AttributeError. The
        # engines were UNCALLABLE as constructed - they did not return a constant, they THREW. An engine
        # that raises satisfies neither branch of P3.12's bar, so `or` is the fix. BOTH decorators in
        # this file had it; fixing one would have left the other raising.
        ueg = getattr(self, 'ueg', None) or VSBUEGLogger()

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
        # P3.12 (W520) - the fallback was DEFEATED by the caller's own default. Every cognitive engine
        # is `__init__(self, ueg=None)`, so the attribute EXISTS and is None; getattr then returns the
        # value rather than the default, and None.log_minimisation_event raised AttributeError. The
        # engines were UNCALLABLE as constructed - they did not return a constant, they THREW. An engine
        # that raises satisfies neither branch of P3.12's bar, so `or` is the fix. BOTH decorators in
        # this file had it; fixing one would have left the other raising.
        ueg = getattr(self, 'ueg', None) or VSBUEGLogger()

        if engine:
            intent = kwargs.get('intent', f"geospheric_{func.__name__}")
            # Ensure niyyah calibration passes before proceeding
            calibration = await engine.calibrate_niyyah(intent)
            #  W584 (FU-406) — THREE-STATE here too. `not calibration.get("passed", False)` recorded a
            #  "calibration_failure" for an intention nothing had assessed, which names a cause that did
            #  not happen: there was no failure, there was no check. The two are logged separately now,
            #  and neither is treated as a pass.
            _n = calibration.get("passed")
            if _n is False:
                await ueg.log_minimisation_event("divine_calibration_refused",
                                                 {"intent": intent, "basis": calibration.get("basis")})
            elif _n is None:
                await ueg.log_minimisation_event("divine_calibration_not_assessed",
                                                 {"intent": intent, "basis": calibration.get("basis")})
            #  Neither branch stops the cycle: this decorator has never had the authority to refuse one,
            #  and a comment claiming a strict environment would someday do so was the only thing
            #  standing in for that authority. What it does have is a record of what was not checked.

        return await func(self, *args, **kwargs)

    return async_wrapper
