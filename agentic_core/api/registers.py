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
import pathlib
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/registers", tags=["registers"])

_ROOT = pathlib.Path(__file__).resolve().parents[2]


def _script(name: str):
    """Load scripts/<name>.py as a module. The check that the suite runs is the check the route runs."""
    path = _ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_register_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@router.get("/sources")
async def sources() -> Dict[str, Any]:
    try:
        sc = _script("sources_check")
        d = sc.load()
        res = sc.check(d)
    except Exception as e:                      # noqa: BLE001 - reported to the reader, never swallowed
        raise HTTPException(status_code=503, detail=(
            f"The register of sources could not be read ({type(e).__name__}), so nothing can be said about "
            f"whether the authorities this platform names still stand."))
    stale = {i for i, _ in res["not_recently_checked"]}
    rows = [{**r, "recently_checked": (None if r.get("status") != "current" else r["id"] not in stale)} for r in d["rows"]]
    return {"about": d.get("about"), "review_days": res["review_days"], "rows": rows, "generated": False,
            "check": {"files_examined": res["files_examined"], "names_found": res["names_found"],
                      "names_with_no_row": [{"file": f, "line": n, "name": nm} for f, n, nm in res["names_with_no_row"]],
                      "readers_of_a_replaced_source": [{"file": f, "line": n, "name": nm, "row": i} for f, n, nm, i in res["readers_of_a_replaced_source"]],
                      "not_recently_checked": [{"row": i, "age_days": a} for i, a in res["not_recently_checked"]],
                      "named_not_read": res["named_not_read"], "row_problems": res["row_problems"]},
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
        res = cr.check(d)
    except Exception as e:                      # noqa: BLE001
        raise HTTPException(status_code=503, detail=(
            f"The coverage register could not be read ({type(e).__name__}), so nothing can be said here about "
            f"what a person can do on this platform."))
    return {"about": d.get("about"), "rows": d["rows"], "by_domain": res["by_domain"], "a_person_can_do": res["a_person_can_do"],
            "problems": res["problems"], "generated": False, "basis": res["basis"]}
