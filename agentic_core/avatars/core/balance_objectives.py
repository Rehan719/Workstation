"""The Owner's goals for a reply's depth against its load — the honest input clearance gate 3 balances over.

OWNER RULING 2026-10-06 (FU-471, option 3). Gate 3 (Tawazun) takes a Pareto frontier over NAMED objectives, each
with a direction, across candidate drafts that carry a number for every objective. The avatar loop had neither,
so the gate could only withhold. The directions are a judgement about what a good reply is, so they are the
OWNER'S, written once; the numbers are MEASURED from each draft's text and nothing else.

MEASURED, NOT ESTIMATED: words, mean_sentence_words and mean_word_chars are counts over the text. None is a
reading-level score, and none is called one; a lower mean sentence length is a property of the text, not a
verdict that it is easier.
"""
from __future__ import annotations

import re
import time
from typing import Any, Dict, List

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

MEASURED = {
    "words": "the number of words in the draft",
    "mean_sentence_words": "words per sentence, sentences split on . ! ?",
    "mean_word_chars": "letters per word",
}
DIRECTIONS = ("min", "max")


def _path():
    return data_path("avatars/balance_objectives.json")


def measure(text: Any) -> Dict[str, float]:
    t = str(text or "")
    words = re.findall(r"[A-Za-zÀ-￿']+", t)
    sentences = [s for s in re.split(r"[.!?]+", t) if s.strip()]
    return {"words": float(len(words)),
            "mean_sentence_words": (len(words) / len(sentences)) if sentences else 0.0,
            "mean_word_chars": (sum(len(w) for w in words) / len(words)) if words else 0.0}


def get() -> Dict[str, Any]:
    try:
        d = read_json_strict(_path(), missing=None, expect=dict)
    except Exception as exc:  # noqa: BLE001
        return {"objectives": None, "basis": f"the goals record could not be read ({exc.__class__.__name__})"}
    if not d:
        return {"objectives": None,
                "basis": ("no goals are recorded: the Owner has not yet said which way each measured property "
                          "should go, so gate 3 has nothing to balance against and withholds")}
    return {"objectives": d.get("objectives"), "set_by": d.get("set_by"), "set_at": d.get("set_at"),
            "basis": f"recorded by {d.get('set_by')} at {d.get('set_at')}"}


def set_objectives(objectives: List[Dict[str, Any]], by: str) -> Dict[str, Any]:
    by = str(by or "").strip()
    problems: List[str] = [] if by else ["no recorder is named"]
    clean = []
    for o in objectives or []:
        n, dirn = str((o or {}).get("name") or ""), (o or {}).get("direction")
        if n not in MEASURED:
            problems.append(f"{n!r} is not a measured property (one of {', '.join(MEASURED)})")
        elif dirn not in DIRECTIONS:
            problems.append(f"{n!r} has no direction (min or max)")
        else:
            clean.append({"name": n, "direction": dirn})
    if not clean:
        problems.append("no objective was given")
    if problems:
        return {"recorded": False, "refused": "invalid", "basis": "REFUSED: " + "; ".join(problems)}
    rec = {"objectives": clean, "set_by": by, "set_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with store_lock(_path()):
        atomic_write_json(_path(), rec)
    return {"recorded": True, "refused": None, **rec}


def candidates(drafts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Each draft the loop holds, with its measured properties. Ids are the drafts' roles."""
    return [{"id": k, **measure(v)} for k, v in drafts.items()]
