"""Host and process resources, read in ONE place, over a window that is stated (W746).

WHAT IT REPLACES. Nine call sites read psutil themselves - seven with cpu_percent(interval=None), two with
cpu_percent(interval=0.1). The non-blocking form measures the time since the PREVIOUS call ON THE SAME THREAD,
and every one of those sites ran on the server's one event-loop thread, so each figure covered whatever time
had passed since some other reader last asked, and none of them said how long that was. Two readers inside one
clock tick get psutil's divide-by-zero 0.0, which reads as an idle host. The two blocking sites held the event
loop for a tenth of a second per call. (The claim that a FIRST call returns a meaningless 0.0 on the served app
was refuted: psutil seeds the importing thread at import. The undisclosed, shared window was the defect.)

WHAT IT DOES. Every CPU sample is taken on ONE dedicated sampler thread, so psutil's per-thread baseline is this
module's own: no request thread and no other caller can shorten a window. A percentage is never computed over
less than MIN_WINDOW_S - psutil's own stated minimum - and a reader who asks sooner is handed the last reading
WITH its window and its age, not a new one. While no reading exists - the first call of a process or of a forked
child, and the first call after a failed sample - the caller waits out what is left of one window (at most
MIN_WINDOW_S) on its own thread, which in the served app is the event loop. No other call waits for a window.

HOST AND PROCESS ARE KEPT APART. `host` is the whole machine - every program on it. `process` is this Python
process alone. No reader is handed one under the other's name.

UNKNOWN IS NEVER 0. A figure that could not be read is None with its reason. observe() does not raise.

THESE ARE READINGS. This module caps, defers and refuses nothing, and it sets no operating-system limit.

RAM TOTAL AND CUDA are not read here. tiers.machine() already measures both, and observe(include_machine=True)
returns its answer, so the two can never disagree.
"""
from __future__ import annotations

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional

#  psutil's documented minimum between two non-blocking calls for an accurate percentage
MIN_WINDOW_S = 0.1
#  how long a reader waits on the sampler thread before reporting the CPU figure as not measured
_SAMPLE_TIMEOUT_S = 2.0

HOST_SCOPE = "the whole machine - every program running on it, not this platform alone"
PROCESS_SCOPE = "this Python process alone - the platform's own server, not the machine"

_LOCK = threading.Lock()
_STATE: Dict[str, Any] = {"pid": None, "sampler": None, "proc": None,
                          "sampled_at": None, "reading": None, "error": None}


def _sampler() -> ThreadPoolExecutor:
    """The ONE sampler thread - reopened in a forked child, where the parent's thread does not exist. Under _LOCK."""
    if _STATE["sampler"] is None or _STATE["pid"] != os.getpid():
        _STATE.update(pid=os.getpid(), proc=None, sampled_at=None, reading=None, error=None,
                      sampler=ThreadPoolExecutor(max_workers=1, thread_name_prefix="host-observation"))
    return _STATE["sampler"]


def _sample() -> Dict[str, Any]:
    """Runs ON THE SAMPLER THREAD and nowhere else, so both percentages measure from this module's last sample."""
    import psutil
    if _STATE["proc"] is None:
        _STATE["proc"] = psutil.Process()
    host = psutil.cpu_percent(interval=None)
    proc = _STATE["proc"].cpu_percent(interval=None)
    #  perf_counter, not monotonic: on Windows before Python 3.13 monotonic() ticks in ~15.6 ms steps, which is
    #  coarser than the window this module guarantees
    return {"t": time.perf_counter(), "host": host, "process": proc}


def _take() -> None:
    """One sample. It becomes THE reading only when a window ends with it. Under _LOCK, after _sampler()."""
    last = _STATE["sampled_at"]
    try:
        s = _STATE["sampler"].submit(_sample).result(timeout=_SAMPLE_TIMEOUT_S)
    except Exception as e:                                   # noqa: BLE001 - reported as unmeasured, never as 0
        _STATE.update(sampled_at=None, reading=None, error=f"{e.__class__.__name__}: {str(e)[:120]}")
        return
    #  a sample with no earlier one behind it has no window: psutil's figure for it is meaningless, so it seeds
    _STATE.update(sampled_at=s["t"], error=None,
                  reading=None if last is None else {"host": s["host"], "process": s["process"],
                                                     "window": s["t"] - last, "ended_at": s["t"]})


def _cpu() -> Dict[str, Any]:
    """The current CPU reading. A new sample is taken only when a full window has passed since the last one."""
    with _LOCK:
        _sampler()
        if _STATE["sampled_at"] is None:
            _take()                                          # the seed: first call, a forked child, or after a failure
        last = _STATE["sampled_at"]
        now = time.perf_counter()
        if last is not None:
            if _STATE["reading"] is None:                    # no reading yet (first call, a forked child, or after
                while now - last < MIN_WINDOW_S:             # a failed sample): wait out the rest of one window
                    time.sleep(MIN_WINDOW_S - (now - last) + 0.001)
                    now = time.perf_counter()
            if now - last >= MIN_WINDOW_S:
                _take()
                now = time.perf_counter()
        #  `now` is the moment of the decision, so a reading served without a new sample is younger than one window
        return {"reading": dict(_STATE["reading"]) if _STATE["reading"] else None,
                "error": _STATE["error"], "now": now, "proc": _STATE["proc"]}


def observe(include_machine: bool = False) -> Dict[str, Any]:
    """Host and process CPU and memory, each saying what it covers and how it was taken. Never raises."""
    c = _cpu()
    r = c["reading"]
    if r:
        window, age = round(r["window"], 3), round(c["now"] - r["ended_at"], 3)
        how = (f"over a {window} s window that ended {age} s ago, sampled on this module's own thread so no other "
               f"reader can shorten it")
    else:
        window = age = None
        how = ("NOT MEASURED: " + (f"the CPU sample failed ({c['error']})" if c["error"] else
                                   "no sampling window has completed") + ", so no percentage is given - and none is 0")
    host: Dict[str, Any] = {
        "cpu_percent": r["host"] if r else None,
        "cpu_window_seconds": window,
        "cpu_reading_age_seconds": age,
        "cpu_basis": f"psutil.cpu_percent {how}; {HOST_SCOPE}" if r else f"{how}; {HOST_SCOPE}",
    }
    process: Dict[str, Any] = {
        "cpu_percent": r["process"] if r else None,
        "cpu_window_seconds": window,
        "cpu_basis": ((f"psutil.Process().cpu_percent {how}, where 100 is one logical CPU fully busy (it can exceed "
                       f"100 across several); {PROCESS_SCOPE}") if r else f"{how}; {PROCESS_SCOPE}"),
    }
    try:
        import psutil
        vm = psutil.virtual_memory()
        host.update(memory_percent=vm.percent, memory_used_bytes=int(vm.used),
                    memory_basis=f"psutil.virtual_memory(), read now; {HOST_SCOPE}")
    except Exception as e:                                   # noqa: BLE001 - reported as unmeasured, never as 0
        host.update(memory_percent=None, memory_used_bytes=None,
                    memory_basis=(f"NOT MEASURED: psutil.virtual_memory() failed ({e.__class__.__name__}), so no "
                                  f"figure is given - and none is 0; {HOST_SCOPE}"))
    try:
        if c["proc"] is None:
            raise RuntimeError("no process handle is open, because no CPU sample has succeeded")
        process.update(rss_mb=round(c["proc"].memory_info().rss / (1024 * 1024), 1),
                       memory_basis=f"resident memory of this process, read now; {PROCESS_SCOPE}")
    except Exception as e:                                   # noqa: BLE001 - reported as unmeasured, never as 0
        process.update(rss_mb=None, memory_basis=(f"NOT MEASURED: {e.__class__.__name__}: {str(e)[:100]} - no "
                                                  f"figure is given, and none is 0; {PROCESS_SCOPE}"))
    out: Dict[str, Any] = {"host": host, "process": process}
    if include_machine:
        try:
            from agentic_core.ai.native import tiers as _tiers
            out["machine"] = _tiers.machine()
        except Exception as e:                               # noqa: BLE001
            out["machine"] = None
            out["machine_basis"] = f"NOT MEASURED: tiers.machine() could not run ({e.__class__.__name__})"
    return out


def prompt_line(obs: Optional[Dict[str, Any]] = None) -> str:
    """One line for a model's prompt that names the machine the figures are of and the window they cover."""
    h = (obs or observe())["host"]
    cpu = (f"CPU {h['cpu_percent']}% over the last {h['cpu_window_seconds']} s"
           if h.get("cpu_percent") is not None else "CPU not measured")
    mem = f"memory {h['memory_percent']}%" if h.get("memory_percent") is not None else "memory not measured"
    return f"Host machine (every program on it, not this platform alone): {cpu}, {mem}"


#  THE FIRST WINDOW OPENS AT IMPORT, so a reader who arrives a tenth of a second later is not kept waiting
try:
    with _LOCK:
        _sampler()
        _take()
except Exception:                                            # noqa: BLE001 - observe() reports it and retries
    pass
