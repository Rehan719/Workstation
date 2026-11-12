"""W874 (FU-1082, plan item P5.20, clause 7) - THE REGULATOR'S FIVE EXPECTATIONS, AS ROWS.

Research the Legal Services Board published on 10 June 2026 names five things people expect of an AI legal tool: a
minimum level of accuracy, no consequential action without informed consent, some human oversight, access to redress,
and protection of personal data. The Owner's ruling of 2026-10-13 (P5.20, clause 7) asked for this platform's own
self-assessment against them, as rows. Each row says whether the platform meets the expectation, partly meets it or
does not, how, and the code that makes the statement true, named as module:symbol and resolved when the rows are read:
a symbol that has been renamed or removed is reported, and its row cannot claim more than "not met".

The five come from the register of sources (lsb-ai-consumer-expectations-2026), which records the publisher's page as
read through a fetch that summarises it and not re-read by a second reader; the two reports themselves were not read.
This is a self-assessment, not a regulator's finding, and the platform is not a regulated provider.
"""
from __future__ import annotations

import importlib
from typing import Any, Dict, List

SOURCE_ID = "lsb-ai-consumer-expectations-2026"
SOURCE_BASIS = ("the five expectations as the register of sources records them from the Legal Services Board's page "
                "(published 10 June 2026), read through a fetch that summarises the page and not re-read by a second "
                "reader; the two reports themselves were not read")

EXPECTATIONS: tuple = (
    {"id": "accuracy", "expectation": "a minimum level of accuracy", "state": "partly",
     "how": ("Enacted law is shown word for word from its publisher, with a fidelity check that can fail, and text "
             "that does not match its own record is not shown. A composed answer's accuracy is not measured; with no "
             "model serving nothing is researched at all, and each answer says which it was."),
     "made_true_by": ["agentic_core.legal.statute:fidelity", "agentic_core.api.law:_FLOOR_LAW"]},
    {"id": "consent", "expectation": "no consequential action without informed consent", "state": "met",
     "how": ("Nothing is filed, sent or signed. A filing-shaped document is assembled as a draft and stays one until "
             "the Owner approves it."),
     "made_true_by": ["agentic_core.legal.specialist:approve", "agentic_core.api.law:matter_approve"]},
    {"id": "oversight", "expectation": "some human oversight", "state": "not met",
     "how": ("No qualified person reviews an answer before it is shown. Each answer says its tier of review, which is "
             "unreviewed until a record says otherwise, and a question about a person's own case is routed to people "
             "instead of being answered."),
     "made_true_by": ["agentic_core.api._review_tier:review_statement", "agentic_core.legal.own_case:own_case_route"]},
    {"id": "redress", "expectation": "access to redress", "state": "partly",
     "how": ("The help list says how to complain to the Owner of this platform, and that no ombudsman or regulator "
             "handles complaints about it, because it is not a regulated provider."),
     "made_true_by": ["agentic_core.api.law:help_from_a_person"]},
    {"id": "personal_data", "expectation": "protection of personal data", "state": "partly",
     "how": ("While the external switch is off, no question leaves this machine; a person's words reach the model "
             "marked as data, and the matter folder is never sent anywhere. What is asked is kept on this machine: "
             "a person's workspace history can be cleared by them, and the record of interactions and the memory "
             "layer keep what was asked and are not cleared on request."),
     "made_true_by": ["agentic_core.api._ai_provenance:MATERIAL_SLOT", "agentic_core.legal.bundle:status"]},
)


def _resolves(ref: str) -> bool:
    mod, _, sym = ref.partition(":")
    try:
        return hasattr(importlib.import_module(mod), sym)
    except Exception:                      # noqa: BLE001 - a module that cannot be imported resolves nothing
        return False


def assessment() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for e in EXPECTATIONS:
        missing = [r for r in e["made_true_by"] if not _resolves(r)]
        row = {**e, "made_true_by_missing": missing}
        if missing:
            row["state"] = "not met"
            row["how"] = (f"{e['how']} NOT SHOWN TO HOLD: {', '.join(missing)} no longer resolves, so this row "
                          f"claims nothing more than not met.")
        rows.append(row)
    return {"rows": rows, "source": SOURCE_ID, "source_basis": SOURCE_BASIS,
            "basis": ("a self-assessment by this platform against the five expectations, each row naming the code "
                      "that makes it true; not a regulator's finding"),
            "composed": False}
