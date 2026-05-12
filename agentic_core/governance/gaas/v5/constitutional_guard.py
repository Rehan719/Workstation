from typing import Dict, Any, Optional, List
from functools import wraps
import hashlib
import json
from datetime import datetime

def constitutional_guard(ueg=None, orchestrator=None, mjm_model=None):
    """
    Injected Constitutional Guard Factory.
    Enforces self-reflection principles and logs every action to UEG.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Capture Pre-state
            pre_state = None
            if orchestrator:
                pre_state = await orchestrator.capture_state()

            try:
                # 2. Execute target function
                result = await func(*args, **kwargs)

                # 3. Post-execution Logging
                if ueg:
                    await ueg.log_event("ACTION_COMPLETE", {
                        "action": func.__name__,
                        "result_summary": str(result)[:100],
                        "pre_checksum": pre_state.state_checksum if pre_state else None,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                # 4. Feedback to Learner
                if mjm_model and hasattr(mjm_model, "should_learn"):
                    if await mjm_model.should_learn(result):
                        await mjm_model.update(result)

                return result

            except Exception as e:
                # 5. Error Logging & Self-Heal Trigger
                if ueg:
                    await ueg.log_event("ACTION_ERROR", {
                        "action": func.__name__,
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })

                if orchestrator and hasattr(orchestrator, "self_heal"):
                    await orchestrator.self_heal(trigger=func.__name__, context={"error": str(e)})

                raise
        return wrapper
    return decorator
