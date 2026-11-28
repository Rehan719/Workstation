"""The two registers a reader can check for themselves (Owner rulings 2026-10-12).

  GET /api/v1/registers/sources    every authority this platform names: its page, the date read, who read it, its
                                   status and what replaced it - with the check's own result beside the rows
  GET /api/v1/registers/coverage   what a person can do here today, subject by subject, for each domain

Nothing here is composed. Each route returns the rows of a file in docs/ and the result of running that file's
check NOW, so the answer cannot say "all current" over a row whose date has passed. A register that cannot be
read answers 503 and says so - never an empty list, which would read as "nothing is named" or "nothing is built".
"""
from __future__ import annotations

import importlib.util
import logging
import os
import pathlib
import sys
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/api/v1/registers", tags=["registers"])

_ROOT = pathlib.Path(__file__).resolve().parents[2]


_log = logging.getLogger(__name__)

#  W1251 - WHAT A ROUTE MAY READ THAT THE IMAGE DOES NOT HOLD, ON PURPOSE, each with what the route says in its place.
#  The live image answered GET /api/v1/care/tools with 503 "(FileNotFoundError)": _script loads scripts/<name>.py by
#  path and the Dockerfile copied no scripts/. The image now copies the three checks the routes run; anything else a
#  route reads by path and the image leaves out is named here. test_w1251 reads every _script call in agentic_core,
#  every file a copied check reads and every COPY line of the image, so a load added without a copy, or a copy taken
#  out, fails it.
NOT_IN_THE_IMAGE = {
    "scripts/session_forecast.py": ("it measures how long past rounds took from git's commit history, which the "
                                    "image does not hold; a change submitted with a commitment records the "
                                    "capacity as NOT MEASURED in its place"),
    "integration_tests/test_mvp_spine.py": ("the test suite is not shipped; GET /api/v1/registers/coverage says the "
                                            "tests its rows name were not checked here"),
    "apps/workstation-superapp/src": ("the image holds the built pages, not their source; GET "
                                      "/api/v1/registers/sources names it among the places it did not read"),
}

#  what a person who meets a refusal here can do (W1251)
NEXT_STEP = "Tell whoever runs this platform what this says, so they can put it right, then try again."
TESTS_NOT_CHECKED = ("This installation does not hold the test suite, so whether each test a row names is in it "
                     "was not checked here. Wherever the suite is run, the check reads it.")


class NotHeld(LookupError):
    """W1251 - a script a route runs is not in this installation. Its text is a sentence a person reads."""


def _script(name: str):
    """Load scripts/<name>.py as a module. The check that the suite runs is the check the route runs.

    W1251 - the one loader of a script by path in agentic_core. A script this installation does not hold is said as
    that, in words, before anything is loaded. Loading one changes nothing in this process: a script sets up its
    own command line when it is imported (auth_perimeter sets AI_DISABLE_LOCAL and WORKSTATION_DRIVE and puts the
    tree on sys.path), and on the serving image that would switch the local model off and mark the platform as
    not the Owner's own running process. So the environment and sys.path are put back as they were."""
    path = _ROOT / "scripts" / f"{name}.py"
    if not path.is_file():
        raise NotHeld(f"this installation does not hold scripts/{name}.py, which this answer runs")
    spec = importlib.util.spec_from_file_location(f"_register_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    env, search = dict(os.environ), list(sys.path)
    try:
        spec.loader.exec_module(mod)
    finally:
        for k in [k for k in os.environ if k not in env]:
            os.environ.pop(k, None)
        for k, v in env.items():
            if os.environ.get(k) != v:
                os.environ[k] = v
        if sys.path != search:
            sys.path[:] = search
    return mod


def unread_said(e: BaseException) -> str:
    """W1251 - why something a route reads could not be read, in plain words and never by an exception's class name
    (the Care page showed "(FileNotFoundError)" to the person reading it). The exception itself goes to the log."""
    _log.warning("a register could not be read: %r", e)
    if isinstance(e, NotHeld):
        return str(e)
    if isinstance(e, FileNotFoundError):
        if not e.filename:
            return "this installation does not hold a file this answer reads"
        p = pathlib.Path(str(e.filename))
        try:
            rel = p.resolve().relative_to(_ROOT.resolve()).as_posix()
        except (ValueError, OSError):
            rel = p.name                        # never a path on the server beyond the file's own name
        return f"this installation does not hold {rel}, which this answer reads"
    if isinstance(e, (ValueError, AssertionError, KeyError, TypeError)):
        return "a file this answer reads is not in the form it expects"
    if isinstance(e, OSError):
        return "a file this answer reads could not be opened"
    return "reading it stopped part-way with an error"


def _tests_named(d) -> set:
    """W1251 - every test the coverage rows name; taken as named where the suite is not held, as the answer says."""
    out = set()
    for r in d.get("rows") or []:
        for k in ("driven_by", "guarded_by"):
            v = r.get(k)
            out.update(t for t in ([v] if isinstance(v, str) else v if isinstance(v, list) else []) if isinstance(t, str))
    return out


@router.get("/sources")
async def sources() -> Dict[str, Any]:
    try:
        sc = _script("sources_check")
        d = sc.load()
        res = sc.check(d)
    except Exception as e:                      # noqa: BLE001 - reported to the reader, never swallowed
        raise HTTPException(status_code=503, detail=(
            f"The register of sources could not be read: {unread_said(e)}. Nothing can be said about whether the "
            f"authorities this platform names still stand. {NEXT_STEP}"))
    #  W1251 - a place the check reads that this installation does not hold (the image holds the built pages, not
    #  their source) is said, so a check over fewer files is not read as a check over all of them
    _base = pathlib.Path(getattr(sc, "ROOT", _ROOT))
    not_held = sorted({str(p.get("dir")) for p in d.get("scan") or [] if p.get("dir") and not (_base / p["dir"]).is_dir()}
                      | {pl for pl, _ in getattr(sc, "REACH_PLACES", ()) if not (_base / pl).is_dir()})
    stale = {i for i, _ in res["not_recently_checked"]}
    rows = [{**r, "recently_checked": (None if r.get("status") != "current" else r["id"] not in stale)} for r in d["rows"]]
    return {"about": d.get("about"), "review_days": res["review_days"], "rows": rows, "generated": False,
            "check": {"files_examined": res["files_examined"], "names_found": res["names_found"],
                      "names_with_no_row": [{"file": f, "line": n, "name": nm} for f, n, nm in res["names_with_no_row"]],
                      "readers_of_a_replaced_source": [{"file": f, "line": n, "name": nm, "row": i} for f, n, nm, i in res["readers_of_a_replaced_source"]],
                      "not_recently_checked": [{"row": i, "age_days": a} for i, a in res["not_recently_checked"]],
                      "named_not_read": res["named_not_read"], "row_problems": res["row_problems"],
                      "places_not_held": not_held,
                      "places_said": (f"This installation does not hold {' and '.join(not_held)}, so no name "
                                      f"written there was read here. Wherever the full source is held, the "
                                      f"check reads it." if not_held else None)},
            "basis": ("rows entered by whoever read each publisher's page, with the date; nothing fetches a page on a "
                      "timer, so a row says when it was read and is shown as not recently checked after "
                      f"{res['review_days']} days")}


@router.get("/coverage")
async def coverage(domain: str = "") -> Dict[str, Any]:
    try:
        cr = _script("coverage_register")
        d = cr.load()
        if domain.strip():
            d = {**d, "rows": [r for r in d["rows"] if str(r.get("domain", "")).lower() == domain.strip().lower()]}
        #  W1251 - the image does not hold the test suite (.dockerignore leaves integration_tests/ out), so where it is
        #  absent each test a row names is taken as named, and the answer says that was not checked here
        suite_held = pathlib.Path(getattr(cr, "SUITE", "")).is_file()
        res = cr.check(d, None if suite_held else _tests_named(d))
    except Exception as e:                      # noqa: BLE001
        raise HTTPException(status_code=503, detail=(
            f"The coverage register could not be read: {unread_said(e)}. Nothing can be said here about what a "
            f"person can do on this platform. {NEXT_STEP}"))
    return {"about": d.get("about"), "rows": d["rows"], "by_domain": res["by_domain"], "a_person_can_do": res["a_person_can_do"],
            "problems": res["problems"], "generated": False, "basis": res["basis"],
            "tests_checked": suite_held, "tests_said": None if suite_held else TESTS_NOT_CHECKED}


@router.get("/perimeter", dependencies=[Depends(get_current_user)])
async def perimeter() -> Dict[str, Any]:
    """WHO MAY CALL WHAT, MEASURED NOW from the mounted application by the same instrument the suite runs.

    The audit's finding was two things: most routes asked for no caller, and NO SURFACE said so. The first was
    closed at the mount; this is the second. It reports counts, never a list of addresses, and it says what the
    measure cannot see - which is the larger half of user isolation: that a route which asks who is calling also
    checks the record is the caller's."""
    try:
        ap = _script("auth_perimeter")
        rows, names, has_list = ap.measure()
    except Exception as e:                      # noqa: BLE001
        raise HTTPException(status_code=503, detail=(
            f"The perimeter could not be measured: {unread_said(e)}. Nothing can be said here about which routes "
            f"ask who is calling. {NEXT_STEP}"))
    #  a route a test adds to the shared application is not the product's; left out by the module that defines it
    rows = [r for r in rows if "test_mvp_spine" not in (r.get("module") or "")]
    by = {s: sum(1 for r in rows if r["state"] == s) for s in ("asks", "public", "OWED", "UNDECIDED")}
    return {
        "route_methods": len(rows), "ask_who_is_calling": by["asks"], "declared_public": by["public"],
        "owed": by["OWED"], "undecided": by["UNDECIDED"],
        "public_that_write": sum(1 for r in rows if r["state"] == "public" and r["writes"]),
        "declared_list_present": bool(has_list), "passes": ap.verdict(rows, has_list) == 0,
        "passes_before_the_switch": ap.verdict(rows, has_list, strict=True) == 0,
        "caller_dependencies_looked_for": names, "measured": True,
        "cannot_see": ("that a handler which asks who is calling USES the answer - that the record it reads or "
                       "changes is the caller's. That is driven separately, group by group, and today only for "
                       "entities and business plans. Nor what a route does with authentication on beyond what the "
                       "suite drives"),
        "basis": ("read from every mounted route's resolved dependencies against docs/PUBLIC_ROUTES.json. A count "
                  "of routes that ASK is not a count of routes that isolate one person's records from another's"),
    }
