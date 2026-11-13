"""THE SCHOLAR'S APPROVAL PACK - everything a child could ever be shown, seen and decided AS ONE WHOLE.

Owner ruling 2026-10-14 (verbatim): "I want the tools built so that the scholar can see what to approve as a
whole". The children's Education and Quran tools are built and HELD; nothing reaches a child until sign-in is on
AND a named scholar on the roster has approved the CURRENT pack.

WHAT THE PACK IS. Three sections, assembled from the tree and the review store, never typed twice:
  rules            the fixed rules every children's tool keeps (from the Owner's rulings), stated once here
  tools            each children's tool as a child would meet it: who runs it, what the child sees, the exact
                   wording on screen, the steps, and where any Arabic comes from (CHILDREN_TOOLS, below)
  learner_content  every learner-facing item awaiting or holding a scholar's decision in the review store,
                   with its text - the research tools' items (keys "religion-research:") are adult tools and are
                   not in the children's pack

ONE DECISION, BOUND TO THE WHOLE. The pack's hash covers all three sections' substance (the items' text by
their body hashes, not their states). A decision records the hash it was made on. If anything in the pack
changes afterwards - one word of a screen, one rule, one item - the hash moves and the approval no longer
applies: the pack reads "changed since it was approved" and the children's tools are held again.

WHO DECIDES: a scholar on the roster (scholar_review.roster()). With sign-in off the Owner enters the decision on
the named scholar's behalf, recorded as ATTESTED; with sign-in on only the scholar's own account decides. A
decision is "approve" or "return" with notes, overall and per section. Nothing here can approve for a scholar.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Dict, List, Optional

#  the rules, as the Owner ruled them (dates in the rulings record); stated ONCE, shown to the scholar whole
RULES: List[Dict[str, str]] = [
    {"id": "R1", "rule": "Qur'anic Arabic is never written by AI. Every verse a child sees is fetched from a sourced "
                         "edition, with the edition named on the screen."},
    {"id": "R2", "rule": "A child's recitation is never scored, never marked, and nothing appears to correct it. A "
                         "reference recitation may be listened to; it is a published reciter's, never a synthesised voice."},
    {"id": "R3", "rule": "A child's audio never leaves the device and is never sent to an outside service."},
    {"id": "R4", "rule": "No rankings or leaderboards, no awards, no streaks. A challenge is only against the child's "
                         "own past, and a circle sees only its shared total."},
    {"id": "R5", "rule": "No religious ruling and no composed explanation of a verse is shown unless this scholar has "
                         "approved that exact text; anything else is withheld, and the screen says so."},
    {"id": "R6", "rule": "A parent or teacher runs every children's tool. A child does not sign in, and no child's "
                         "name, age or school is recorded."},
    {"id": "R7", "rule": "Nothing about a child's progress is kept as a measure of the child; what is kept is which "
                         "portions were practised and when, for the adult running the tool."},
]

#  every children's tool route is under this one prefix, on agentic_core/api/qep_children.py's router, which asks
#  the gate before any handler runs (W943)
CHILDREN_PREFIX = "/api/v1/qep/children"

#  each children's tool AS A CHILD WOULD MEET IT. A tool is listed here in the same change that builds it, with the
#  routes it serves: test_w943's census fails on a route under CHILDREN_PREFIX that this list does not describe,
#  and on a route it describes that is not mounted.
CHILDREN_TOOLS: List[Dict[str, Any]] = [
    #  W943 - P5.21 clause 4, the first tool
    {"id": "memorisation-practice",
     "name": "Memorisation practice, run by a parent or teacher",
     "run_by": ("a parent or teacher, on their own screen, sitting with the child. The adult chooses the verse; "
                "the child does not sign in and is not named"),
     "what_a_child_sees": ("The first word of one verse, fetched from the named edition, with the edition named "
                           "(more of its first words if the adult chooses). The next word, or the whole verse, "
                           "only when the adult shows it. No mark, no score, no count, and no record of how it "
                           "went."),
     "steps": ["The adult chooses a surah and a verse the child is learning.",
               "The screen shows the verse's first word, as fetched from the named edition, and names the edition.",
               "The child says the rest of the verse from memory to the adult. Nothing listens, and nothing marks it.",
               "If the child pauses, the adult may show the next word.",
               "The adult may show the whole verse, for the child to look at with them.",
               "Nothing is recorded: not the child, not the verse, and not how it went."],
     "wording": ["Say the rest of this verse from memory, to the grown-up with you.",
                 "Nothing here listens to you or marks you.",
                 "Show the next word",
                 "Show the whole verse",
                 "This verse is shown as it was fetched from:"],
     "arabic_from": ("the verse as fetched from alquran.cloud, edition quran-uthmani, with the edition and its "
                     "provenance named beside it. Nothing is generated, and a verse that cannot be fetched is not "
                     "shown."),
     "routes": [f"GET {CHILDREN_PREFIX}/memorisation/{{surah_number}}/{{ayah_number}}",
                f"GET {CHILDREN_PREFIX}/memorisation/{{surah_number}}/{{ayah_number}}/next"]},
    #  W944 - P5.21 clause 4, the second tool
    {"id": "own-past-challenge",
     "name": "A challenge against the child's own past, run by a parent or teacher",
     "run_by": ("a parent or teacher, signed in on their own account. The child is one of the adult's numbered "
                "children, 1 to 9, and is never named"),
     "what_a_child_sees": ("How many portions they have practised this week, beside their own earlier weeks. Never "
                           "another child's number, and no rank, award, streak or score."),
     "steps": ["After a practice, the adult notes the portion the child practised: a surah, and its first and last "
               "verse.",
               "The platform keeps which portion was practised and on which day, for this adult and this numbered "
               "child only.",
               "The adult opens the challenge. It shows this week's count of portions practised beside the child's "
               "own earlier weeks.",
               "Nothing compares the child with any other child, and nothing counts days in a row.",
               "The adult can remove the child's record at any time, and nothing of it is kept afterwards."],
     "wording": ["Portions practised this week: {this_week}.",
                 "Last week: {last_week}.",
                 "Can you practise as many this week as last week?",
                 "This is only about you. Nobody else sees it, and you are not compared with anyone."],
     "arabic_from": "none: this tool shows no Arabic, only the surah and verse numbers the adult noted.",
     "routes": [f"POST {CHILDREN_PREFIX}/challenge/{{child}}/practised",
                f"GET {CHILDREN_PREFIX}/challenge/{{child}}",
                f"DELETE {CHILDREN_PREFIX}/challenge/{{child}}"]},
    #  W945 - P5.21 clause 4, the third tool
    {"id": "teaching-aids",
     "name": "Teaching aids for a teacher",
     "run_by": "a teacher, or a parent teaching, signed in on their own account and preparing a lesson",
     "what_a_child_sees": ("A sheet of one portion, shown or printed: each verse as fetched from the named edition, "
                           "with the edition named, or for recall practice only each verse's first word. No mark, "
                           "score or name is on it."),
     "steps": ["The teacher chooses a surah, and the first and last verse of a portion of at most 40 verses.",
               "The sheet lists each verse of the portion as fetched from the named edition, and names the edition.",
               "For recall practice, the teacher may choose the sheet that shows only each verse's first word.",
               "A verse that cannot be fetched is named as missing, and nothing is put in its place.",
               "Nothing is recorded about the teacher's class or any child."],
     "wording": ["Portion: surah {surah}, verses {from_ayah} to {to_ayah}.",
                 "Each verse is shown as it was fetched from:",
                 "Say the rest of each verse from memory.",
                 "Not available, so not shown:"],
     "arabic_from": ("each verse as fetched from alquran.cloud, edition quran-uthmani, with the edition named on "
                     "the sheet. Nothing is generated, and a verse that cannot be fetched is named as missing and "
                     "not shown."),
     "routes": [f"GET {CHILDREN_PREFIX}/teaching/sheet/{{surah_number}}"]},
]

PACK_STORE = "scholar_pack_decisions.json"
_RESEARCH_PREFIX = "religion-research:"


def _store_path():
    from agentic_core.config import data_path
    return data_path(PACK_STORE)


def _learner_items() -> List[Dict[str, Any]]:
    from agentic_core.api.scholar_review import _load, _review_path
    recs = _load(_review_path())
    return sorted(({"content_key": k, "surface": r.get("surface"), "reference": r.get("reference"),
                    "body": r.get("body"), "body_hash": r.get("body_hash"), "state": r.get("state")}
                   for k, r in recs.items() if not str(k).startswith(_RESEARCH_PREFIX)),
                  key=lambda r: str(r["content_key"]))


def pack_hash(rules: List[Dict[str, str]], tools: List[Dict[str, Any]], items: List[Dict[str, Any]]) -> str:
    """The fingerprint of the WHOLE pack: rules and tools as written, items by their text's hash (not state)."""
    substance = {"rules": rules, "tools": tools,
                 "learner_content": [{"content_key": i["content_key"], "body_hash": i["body_hash"]} for i in items]}
    return hashlib.sha256(json.dumps(substance, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:32]


def _decisions() -> List[Dict[str, Any]]:
    from agentic_core.config import read_json_strict
    p = _store_path()
    if not p.exists():
        return []
    return read_json_strict(p, list, expect=list) or []


def assemble() -> Dict[str, Any]:
    """The whole pack, with what its current state is and why."""
    items = _learner_items()
    h = pack_hash(RULES, CHILDREN_TOOLS, items)
    ds = _decisions()
    on_this = [d for d in ds if d.get("pack_hash") == h]
    latest = on_this[-1] if on_this else None
    earlier = [d for d in ds if d.get("pack_hash") != h and d.get("decision") == "approve"]
    if latest and latest.get("decision") == "approve":
        state, basis = "approved", (f"approved as a whole by {latest['scholar_id']} on {latest['at']} "
                                    f"({latest['attestation']})")
    elif latest:
        state, basis = "returned", f"returned by {latest['scholar_id']} on {latest['at']} with notes"
    elif earlier:
        state, basis = "changed_since_approval", ("an earlier pack was approved, and this pack has changed since: "
                                                  "the approval does not carry over, and review is open again")
    else:
        state, basis = "awaiting_review", "no scholar has decided on this pack"
    return {"pack_hash": h, "state": state, "basis": basis, "decision": latest,
            "sections": {"rules": RULES, "tools": CHILDREN_TOOLS, "learner_content": items},
            "counts": {"rules": len(RULES), "tools": len(CHILDREN_TOOLS), "learner_content": len(items)},
            "whole": ("one decision covers everything in this pack; a change to any part re-opens review")}


def decide(scholar_id: str, decision: str, notes: str = "", section_notes: Optional[Dict[str, str]] = None,
           *, seen_hash: str, entered_by: str, attestation: str) -> Dict[str, Any]:
    """Record a decision on the CURRENT pack. Refused when the scholar is not on the roster, when the decision is
    not approve or return, or when the pack changed after the scholar read it (seen_hash)."""
    from agentic_core.api.scholar_review import roster
    from agentic_core.config import atomic_write_json, store_lock
    if decision not in ("approve", "return"):
        return {"ok": False, "detail": "A decision on the pack is 'approve' or 'return'."}
    if scholar_id not in roster():
        return {"ok": False, "detail": (f"{scholar_id!r} is not on the scholar roster, so no decision on the pack can "
                                        f"be recorded for them.")}
    current = assemble()["pack_hash"]
    if seen_hash != current:
        return {"ok": False, "detail": ("The pack changed after it was read (it is not the pack you saw). Read it "
                                        "again and decide on what it holds now.")}
    rec = {"pack_hash": current, "decision": decision, "scholar_id": scholar_id, "notes": str(notes)[:4000],
           "section_notes": {k: str(v)[:4000] for k, v in (section_notes or {}).items()
                             if k in ("rules", "tools", "learner_content")},
           "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "entered_by": entered_by,
           "attestation": attestation}
    p = _store_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with store_lock(p):
        ds = _decisions()
        ds.append(rec)
        atomic_write_json(p, ds)
    return {"ok": True, "decision": rec}


def children_tools_open() -> Dict[str, Any]:
    """THE GATE every children's tool asks. Open only when sign-in is on AND the current pack is approved."""
    from agentic_core.auth.core import auth_enabled
    st = assemble()
    signed = bool(auth_enabled())
    ok = signed and st["state"] == "approved"
    why = []
    if not signed:
        why.append("sign-in is off, and no children's tool opens before it is on")
    if st["state"] != "approved":
        why.append(f"the scholar's approval pack is {st['state'].replace('_', ' ')}: {st['basis']}")
    return {"open": ok, "pack_hash": st["pack_hash"], "pack_state": st["state"],
            "basis": "open: sign-in is on and the current pack is approved" if ok else "HELD: " + "; and ".join(why)}


def as_document() -> str:
    """The pack as ONE document a scholar can read, print or keep (Markdown)."""
    st = assemble()
    lines = [f"# The approval pack for the children's tools", "",
             f"Pack {st['pack_hash']} - state: {st['state'].replace('_', ' ')}. {st['basis']}.", "",
             "One decision covers everything below. A change to any part re-opens review.", "",
             "## 1. The rules every children's tool keeps", ""]
    lines += [f"- **{r['id']}** {r['rule']}" for r in st["sections"]["rules"]]
    lines += ["", "## 2. The tools, as a child would meet them", ""]
    if not st["sections"]["tools"]:
        lines.append("No children's tool is built yet. Each one is added here in the change that builds it.")
    for t in st["sections"]["tools"]:
        lines += [f"### {t.get('name')}", f"Run by: {t.get('run_by')}", "", f"What the child sees: {t.get('what_a_child_sees')}", ""]
        lines += [f"{i}. {s}" for i, s in enumerate(t.get("steps") or [], 1)]
        lines += ["", "Exact wording on screen:"] + [f"> {w}" for w in (t.get("wording") or [])]
        lines += ["", f"Where any Arabic comes from: {t.get('arabic_from')}", ""]
    lines += ["## 3. Learner-facing text awaiting or holding a decision", ""]
    if not st["sections"]["learner_content"]:
        lines.append("None is in the review store yet.")
    for i in st["sections"]["learner_content"]:
        lines += [f"### {i['content_key']} ({i.get('surface')}) - {i.get('state')}", "", str(i.get("body") or ""), ""]
    return "\n".join(lines) + "\n"
