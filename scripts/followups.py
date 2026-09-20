"""Follow-up register CLI — see agentic_core/plan_followups.py for the rules.

  python scripts/followups.py add --title T --why W --source W462 [--slot P2.6|auto|OWNER] [--files a,b] [--severity high|medium|low] [--owner-gated]
                                              # no --slot (or auto): routed to the plan item that owns its area
  python scripts/followups.py list [--all]
  python scripts/followups.py close FU-007 --by W463
  python scripts/followups.py drop FU-007 --note "why it is not worth doing"
  python scripts/followups.py reslot FU-007 --slot P2.1|auto [--ungate]   # --ungate once the Owner has ruled
  python scripts/followups.py reslot FU-007 --gate                        # it waits on the Owner after all
  python scripts/followups.py routes          # which plan item owns which area (in precedence order)
  python scripts/followups.py route --slot P2.9 [--files a/,b.py] [--words "cannot be read,ueg"] [--note N] [--position 1]
  python scripts/followups.py route --slot P2.9 --remove
  python scripts/followups.py route --from P2.8 --slot P2.7       # hand a DONE item's area on: its routes become handed routes of P2.7
  python scripts/followups.py done P1.13 --by W470 [--reroute] [--hand-to P1.14]
                                              # mark an item ✅ DONE; move its open rows along the routes; hand its routes on
  python scripts/followups.py schedule        # PLAN NOW and the ordered schedule, as the plan will show them
  python scripts/followups.py render          # rewrite both generated blocks in both plan docs
  python scripts/followups.py check           # exit 1 on any problem (the suite's guards run the same check)

W469 — NEXT is retired: every row rides the plan item that owns its area (see agentic_core/plan_followups.py).

Every mutating command holds the register's lock, validates the change AND both docs, then writes the two docs
and the register last (each atomically), so the register and the plans move together. A file named on a row
must be in the working tree and tracked by git (git add a new file first). Owner-gated work is slotted OWNER.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentic_core import plan_followups as fu  # noqa: E402

LOCK_WAIT_S = float(os.environ.get("FOLLOWUPS_LOCK_WAIT_S") or 30)   # the guard shortens it


def _os_lock(fd: int) -> None:
    if os.name == "nt":
        import msvcrt
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _os_unlock(fd: int) -> None:
    try:
        if os.name == "nt":
            import msvcrt
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass


@contextmanager
def register_lock():
    """One writer at a time: parallel sessions recording follow-ups used to hand out the same id and lose rows.
    An OS lock on a byte of a persistent (gitignored) lock file — the OS releases it when the holder exits or
    is killed, so there is no stale lock to take over, nothing to delete, and no race over who deleted it."""
    lock = fu.REGISTER.with_name(fu.REGISTER.name + ".lock")
    fd = os.open(str(lock), os.O_CREAT | os.O_RDWR)
    deadline = time.time() + LOCK_WAIT_S
    try:
        while True:
            try:
                _os_lock(fd)
                break
            except OSError:
                if time.time() > deadline:
                    sys.exit(f"REFUSED — another followups.py is writing the register (waited {LOCK_WAIT_S}s)")
                time.sleep(0.05)
        try:
            yield
        finally:
            _os_unlock(fd)
    finally:
        os.close(fd)


def _one_line(value: str) -> str:
    return " ".join(value.split())


def _find(reg, fid):
    matches = [r for r in fu.raw_items(reg) if isinstance(r, dict) and r.get("id") == fid]
    if len(matches) != 1:
        sys.exit(f"REFUSED — {len(matches)} rows have id {fid}; repair the register by hand first")
    return matches[0]


def _set_priority_parts(r, args):
    """W478 — the priority parts named on the command line; an unknown area is refused, never silently unmapped."""
    from agentic_core import plan_priority as pp
    if args.tier is not None:
        r["tier"] = args.tier
    if args.area.strip():
        cfg, _ = pp.load_config(fu.ROOT)
        ids = [a["id"] for a in cfg["areas"]]
        if args.area.strip() not in ids:
            sys.exit(f"REFUSED — {args.area.strip()!r} is not a priority area; one of: {', '.join(ids)}")
        r["area"] = args.area.strip()
    if args.reach is not None:
        r["reach"] = args.reach


def _texts():
    try:
        return fu.load(), fu.read_doc(fu.PROMPT), fu.read_doc(fu.LIVING)
    except ValueError as exc:
        sys.exit(f"REFUSED — the register or a plan doc cannot be read: {exc}")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):       # the register is prose: '→', '≠', '✅' must never crash a pipe
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    if os.environ.get("WORKSTATION_FOLLOWUPS_ROOT"):
        print(f"note: WORKSTATION_FOLLOWUPS_ROOT is set — working on {fu.ROOT}, not this repository", file=sys.stderr)
    ap = argparse.ArgumentParser(description="the follow-up register")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--why", required=True)
    a.add_argument("--source", required=True, help="the round / refuter that found it, e.g. 'W460 refuter'")
    a.add_argument("--slot", default="auto", help="a plan item (P2.6), auto (route it; the default) or OWNER")
    a.add_argument("--files", default="")
    a.add_argument("--severity", default="medium", choices=fu.SEVERITIES)
    a.add_argument("--owner-gated", action="store_true")
    # W478 — the priority parts a finder knows (otherwise derived: see agentic_core/plan_priority.py)
    a.add_argument("--tier", type=int, choices=(1, 2, 3), help="1 a truth defect on a reached surface · 2 an invisible shortfall · 3 disclosed/unreached")
    a.add_argument("--area", default="", help="a priority area id from docs/PRIORITY.json (default: derived from the files)")
    a.add_argument("--reach", choices=("core", "secondary", "internal"), help="default: derived from the files")
    rp = sub.add_parser("reprioritise", help="set a row's priority parts (tier / area / reach)")
    rp.add_argument("id")
    rp.add_argument("--tier", type=int, choices=(1, 2, 3))
    rp.add_argument("--area", default="")
    rp.add_argument("--reach", choices=("core", "secondary", "internal"))
    rp.add_argument("--clear", action="append", default=[], choices=("tier", "area", "reach"),
                    help="remove a part set on the row, so it is derived again (repeatable)")
    pr = sub.add_parser("priority", help="the open rows ranked by priority, each score's parts shown")
    pr.add_argument("--item", default="", help="only the rows riding this plan item")
    pr.add_argument("--top", type=int, default=20)
    ls = sub.add_parser("list")
    ls.add_argument("--all", action="store_true")
    c = sub.add_parser("close")
    c.add_argument("id")
    c.add_argument("--by", required=True)
    d = sub.add_parser("drop")
    d.add_argument("id")
    d.add_argument("--note", required=True)
    rs = sub.add_parser("reslot")
    rs.add_argument("id")
    rs.add_argument("--slot", help="a plan item, or auto to route it")
    g = rs.add_mutually_exclusive_group()
    g.add_argument("--ungate", action="store_true", help="the Owner has ruled: schedule it into --slot")
    g.add_argument("--gate", action="store_true", help="it waits on the Owner: slot OWNER")
    sub.add_parser("routes")
    ro = sub.add_parser("route")
    ro.add_argument("--slot", required=True)
    ro.add_argument("--files", default="", help="comma-separated file paths or directory prefixes ending in /")
    ro.add_argument("--words", default="", help="comma-separated whole words matched in a row's title (lower case)")
    ro.add_argument("--note", default="")
    ro.add_argument("--position", type=int, default=0, help="1-based precedence for a new route (default: last)")
    ro.add_argument("--remove", action="store_true")
    ro.add_argument("--handed", action="store_true", help="with --remove: also remove the routes handed to this item")
    ro.add_argument("--from", dest="from_slot", default="", help="hand every route of this DONE item to --slot (each becomes a handed route of it, in its own place)")
    dn = sub.add_parser("done")
    dn.add_argument("slot")
    dn.add_argument("--by", required=True)
    dn.add_argument("--reroute", action="store_true", help="move the item's open rows along the routes")
    dn.add_argument("--hand-to", dest="hand_to", default="", help="the open item the finished item's routes now send to")
    sub.add_parser("schedule")
    sub.add_parser("render")
    sub.add_parser("check")
    fc = sub.add_parser("forecast", help="the pace the plan is moving at, and what it projects")
    fc.add_argument("--window", type=int, default=6, help="build rounds to measure the rate over")
    args = ap.parse_args()

    if args.cmd in ("check", "list", "schedule", "routes", "priority", "forecast"):
        with register_lock():                      # never read the register and the docs from different moments
            reg, prompt, living = _texts()
        if args.cmd == "priority":
            s = fu.schedule(reg, prompt)
            pr_ = s["priority"]
            rows = [r for slot in s["schedule"] for r in slot["items"] if not args.item or r["slot"] == args.item]
            rows.sort(key=lambda r: -r["priority"]["score"])
            print(f"priority weights: {pr_['config']}; current gate: {pr_['gate_phase']}")
            for p_ in pr_["config_problems"]:
                print("PROBLEM", p_)
            for r in rows[: max(1, args.top)]:
                q = r["priority"]
                parts = " × ".join(f"{k} {v}" for k, v in q["parts"].items())
                print(f"{q['score']:6.1f}  {r['id']} {r['slot']:5} {r['title'][:90]}")
                print(f"        = 100 × {parts}")
                print("        " + " · ".join(f"{k}: {v}" for k, v in q["basis"].items()))
            comp = pr_["completion"]
            print("completion weighted by priority: " + " · ".join(
                f"{ph} {d['weighted_pct']}% ({d['rows_closed']}/{d['rows_closed'] + d['rows_open']} rows)"
                for ph, d in comp["by_phase"].items()) + f" · all {comp['overall_weighted_pct']}%")
            print("open items by total open priority (a suggestion beside the plan's order): " + " · ".join(pr_["suggested_order"]))
            return 1 if pr_["config_problems"] else 0
        if args.cmd == "forecast":
            print(fu.render_forecast(reg, prompt))
            # The register cannot know how long a round TAKES — git can, so the wall-clock is
            # measured separately and labelled as a different measurement, never blended in.
            import subprocess as _sp, datetime as _dt, re as _re
            try:
                _log = _sp.run(["git", "log", "--format=%ct %s", "-40"], capture_output=True,
                               text=True, encoding="utf-8", errors="replace").stdout.splitlines()
                _pts = [(int(l.split(" ", 1)[0]), _re.search(r"\(W(\d{3})\)", l))
                        for l in _log if l.strip() and l.split(" ", 1)[0].isdigit()]
                _b = [(t, "W" + m.group(1)) for t, m in _pts if m]
                _gaps = [round((_b[i - 1][0] - _b[i][0]) / 3600.0, 1) for i in range(1, len(_b))]
                _gaps = [g for g in _gaps if 0.2 <= g <= 48]
                if len(_gaps) >= 3:
                    _gaps_sorted = sorted(_gaps)
                    _med = _gaps_sorted[len(_gaps_sorted) // 2]
                    print(f"  WALL CLOCK (git, a separate measurement): {len(_gaps)} commit-to-commit gaps, "
                          f"median {_med} h per round, range {min(_gaps)}–{max(_gaps)} h.")
                else:
                    print("  WALL CLOCK: not assessable — too few round commits on record.")
            except Exception as _e:
                print(f"  WALL CLOCK: not assessable — git could not be read ({str(_e)[:80]}).")
            return 0
        if args.cmd == "check":
            problems = fu.check(reg, prompt, living)
            for p in problems:
                print("PROBLEM", p)
            print("ok" if not problems else f"{len(problems)} problem(s)")
            return 1 if problems else 0
        if args.cmd == "list":
            for r in fu.raw_items(reg):
                if not isinstance(r, dict):
                    continue
                if args.all or r.get("status") == "open":
                    gate = " OWNER-GATED" if r.get("owner_gated") is True else ""
                    print(f"{r.get('id')} {str(r.get('status')):7} {str(r.get('slot')):6} [{r.get('severity')}]{gate} {r.get('title')}")
            return 0
        if args.cmd == "routes":
            items = {i["slot"]: i for i in fu.plan_items(prompt)}
            for n, rt in enumerate(fu.raw_routes(reg), 1):
                if not isinstance(rt, dict):
                    print(f"{n}. (malformed)")
                    continue
                it = items.get(rt.get("slot"))
                state = "not a plan item" if it is None else (f"DONE {it['done_by']}" if it["done"] else "open")
                print(f"{n}. {rt.get('slot')} [{state}] files={rt.get('files', [])} words={rt.get('words', [])}"
                      + (f" — {rt['note']}" if rt.get("note") else ""))
            return 0
        print(fu.render_plan_now(reg, prompt))
        print()
        print(fu.render(reg, prompt))
        return 0

    with register_lock():
        reg, prompt, living = _texts()            # read INSIDE the lock — never a stale copy
        before = set(fu.check(copy.deepcopy(reg), prompt, living))
        if not isinstance(reg, dict) or not isinstance(reg.get("items"), list):
            sys.exit("REFUSED — the register must be an object with an items list")

        new_prompt_src = prompt                    # `done` edits the plan itself; every other command keeps it
        said = []
        if args.cmd == "add":
            nums = [fu.id_number(r.get("id")) for r in reg["items"] if isinstance(r, dict)]
            n = max([x for x in nums if x is not None] or [0]) + 1
            slot = args.slot.strip()
            title = _one_line(args.title)
            files = [fu.normalise_path(f) for f in args.files.split(",") if f.strip()]
            if slot.upper() in fu.RETIRED_SLOTS:
                sys.exit(f"REFUSED — slot {slot} is retired (W469): a row rides the plan item that owns its area "
                         "(leave --slot out to route it, or name the item)")
            if args.owner_gated and slot != "OWNER":
                if slot != "auto":                 # only a slot the caller named is worth a note
                    print(f"note: owner-gated work is slotted OWNER (not {slot})")
                slot = "OWNER"
            elif slot == "auto":
                routed = fu.route_row(reg, prompt, title, files, args.severity)
                if not routed["slot"]:
                    sys.exit(f"REFUSED — {routed['reason']}")
                slot = routed["slot"]
                said.append(f"routed to {slot} — {routed['by']}")
            reg["items"].append({
                "id": f"FU-{n:03d}", "title": title, "why": _one_line(args.why),
                "source": _one_line(args.source), "found": time.strftime("%Y-%m-%d"),
                "files": files,
                "severity": args.severity, "owner_gated": bool(args.owner_gated),
                "slot": slot, "status": "open", "closed_by": None, "note": "",
            })
            _set_priority_parts(reg["items"][-1], args)
            added_id = f"FU-{n:03d}"
        elif args.cmd == "reprioritise":
            r = _find(reg, args.id)
            if r.get("status") != "open":
                sys.exit(f"REFUSED — {args.id} is {r.get('status')}; only an open row is reprioritised")
            if args.tier is None and not args.area and args.reach is None and not args.clear:
                sys.exit("REFUSED — name what to set: --tier, --area, --reach and/or --clear tier|area|reach")
            given = {"tier": args.tier is not None, "area": bool(args.area.strip()), "reach": args.reach is not None}
            both = [p_ for p_ in args.clear if given.get(p_)]
            if both:                                  # (refutation 2) never a report of an action not taken
                sys.exit(f"REFUSED — {', '.join(both)}: --clear and a value for the same part; pass one or the other")
            if args.area and not args.area.strip():
                sys.exit("REFUSED — a blank --area names no area; use --clear area to remove one")
            cleared = [p_ for p_ in args.clear if p_ in r]
            for p_ in cleared:                        # (refutation) a stale part can be removed, not only overwritten
                r.pop(p_, None)
            _set_priority_parts(r, args)
            said.append(f"{args.id} priority parts set" + (f"; cleared {', '.join(cleared)}" if cleared else "")
                        + (f"; not set, so nothing to clear: {', '.join(p_ for p_ in args.clear if p_ not in cleared)}"
                           if any(p_ not in cleared for p_ in args.clear) else ""))
        elif args.cmd == "close":
            r = _find(reg, args.id)
            if r.get("status") != "open":            # W473 (FU-067) — a closed row's round is history, never rewritten
                sys.exit(f"REFUSED — {args.id} is {r.get('status')} (closed by {r.get('closed_by') or 'a note'}); only an open row closes")
            r["status"], r["closed_by"] = "done", args.by.strip()
        elif args.cmd == "drop":
            r = _find(reg, args.id)
            if r.get("status") != "open":            # W473 (FU-067)
                sys.exit(f"REFUSED — {args.id} is {r.get('status')}; only an open row is dropped")
            r["status"], r["note"] = "dropped", _one_line(args.note)
        elif args.cmd == "reslot":
            r = _find(reg, args.id)
            if r.get("status") != "open":            # W473 (FU-067, refutation) — the same rule as close and drop
                sys.exit(f"REFUSED — {args.id} is {r.get('status')}; only an open row is re-slotted")
            if args.gate:
                if args.slot:                        # W473 (FU-068) — never silently ignored
                    sys.exit("REFUSED — --gate slots the row OWNER; do not pass --slot with it")
                r["owner_gated"], r["slot"] = True, "OWNER"
            else:
                if not args.slot:
                    sys.exit("REFUSED — reslot needs --slot (or --gate)")
                if r.get("owner_gated") is True and not args.ungate:
                    sys.exit(f"REFUSED — {args.id} is owner-gated; pass --ungate once the Owner has ruled")
                if args.ungate:
                    r["owner_gated"] = False
                slot = args.slot.strip()
                if slot.upper() in fu.RETIRED_SLOTS:
                    sys.exit(f"REFUSED — slot {slot} is retired (W469): use --slot auto or name the plan item")
                if slot == "auto":
                    routed = fu.route_row(reg, prompt, str(r.get("title") or ""), list(r.get("files") or []),
                                          str(r.get("severity") or ""))
                    if not routed["slot"]:
                        sys.exit(f"REFUSED — {args.id}: {routed['reason']}")
                    slot = routed["slot"]
                    said.append(f"{args.id} routed to {slot} — {routed['by']}")
                r["slot"] = slot
        elif args.cmd == "route":
            routes = reg.setdefault("routes", [])
            if not isinstance(routes, list):
                sys.exit("REFUSED — the register's routes are not a list; repair it by hand first")
            target = args.slot.strip()
            open_items = {i["slot"] for i in fu.plan_items(prompt) if not i["done"]}
            # (refutation 2) a flag this branch would not read is refused, never ignored — the FU-068 class
            given = {k for k, v in (("--files", args.files.strip()), ("--words", args.words.strip()),
                                    ("--note", args.note.strip()), ("--position", args.position),
                                    ("--from", args.from_slot.strip()), ("--handed", args.handed),
                                    ("--remove", args.remove)) if v}
            branch = "remove" if args.remove else ("from" if args.from_slot.strip() else "add")
            reads = {"remove": {"--remove", "--handed"}, "from": {"--from"},
                     "add": {"--files", "--words", "--note", "--position"}}[branch]
            stray = sorted(given - reads)
            if stray:
                sys.exit(f"REFUSED — {', '.join(stray)} means nothing with "
                         + {"remove": "--remove", "from": "--from", "add": "a route's matchers"}[branch]
                         + " (--handed goes with --remove; --from hands a DONE item's routes on and takes no matchers)")
            if args.remove:
                # (refutation) the item's OWN route goes; a route handed to it stays unless --handed says so
                kept = [rt for rt in routes if not (isinstance(rt, dict) and rt.get("slot") == target
                                                    and (args.handed or not rt.get("handed_from")))]
                if len(kept) == len(routes):
                    sys.exit(f"REFUSED — no route of {target}'s own sends rows to it"
                             + (" (routes handed to it exist: pass --handed to remove those too)"
                                if any(isinstance(rt, dict) and rt.get("slot") == target for rt in routes) else ""))
                routes[:] = kept
                said.append(f"removed the route(s) to {target}" + (" including the handed ones" if args.handed else ""))
            elif target not in open_items:
                sys.exit(f"REFUSED — {target} is not an open delivery-plan item; a route sends new rows only to one")
            elif args.from_slot.strip():
                src = args.from_slot.strip()
                if src == target:
                    sys.exit("REFUSED — --from and --slot name the same item")
                if src in open_items:                    # (refutation) an open item does not hand its area away
                    sys.exit(f"REFUSED — {src} is still open; an area is handed on when its item is done")
                try:
                    n = fu.merge_routes(reg, src, target)
                except ValueError as exc:
                    sys.exit(f"REFUSED — {exc}")
                if not n:
                    sys.exit(f"REFUSED — no route sends rows to {src}")
                said.append(f"{n} route(s) to {src} handed to {target} (each in its own place, marked handed_from)")
            else:
                new_route = {"slot": args.slot.strip(),
                             "files": [fu.normalise_path(f) for f in args.files.split(",") if f.strip()],
                             "words": [" ".join(w.split()).lower() for w in args.words.split(",") if w.strip()]}
                if args.note.strip():
                    new_route["note"] = _one_line(args.note)
                same = [i for i, rt in enumerate(routes) if isinstance(rt, dict) and rt.get("slot") == new_route["slot"]
                        and not rt.get("handed_from")]        # (refutation) only the item's OWN route is replaced
                if same:
                    routes[same[0]] = new_route
                    said.append(f"route {same[0] + 1} to {new_route['slot']} replaced")
                else:
                    at = len(routes) if args.position <= 0 else min(args.position - 1, len(routes))
                    routes.insert(at, new_route)
                    said.append(f"route to {new_route['slot']} added at position {at + 1}")
        elif args.cmd == "done":
            slot = args.slot.strip()
            by = args.by.strip()
            same = [i for i in fu.plan_items(prompt) if i["slot"] == slot and i["done"] and i["done_by"] == by]
            try:
                # done by THIS round already (a done whose other writes did not land): finish it, do not refuse it
                new_prompt_src = prompt if same else fu.mark_done(prompt, slot, by)
            except ValueError as exc:
                sys.exit(f"REFUSED — {exc}")
            open_after = {i["slot"] for i in fu.plan_items(new_prompt_src) if not i["done"]}
            riders = [r for r in fu.raw_items(reg) if isinstance(r, dict) and r.get("status") == "open"
                      and r.get("slot") == slot and r.get("owner_gated") is not True]
            if riders and not args.reroute:       # unfinished work is named first
                sys.exit(f"REFUSED — {len(riders)} open row(s) ride {slot}: "
                         + ", ".join(str(r.get("id")) for r in riders)
                         + " — close each one it did, or pass --reroute to move the rest along the routes")
            hand = args.hand_to.strip()
            if hand and hand not in open_after:   # checked whenever it is given, never silently ignored
                sys.exit(f"REFUSED — --hand-to {hand} is not an open delivery-plan item")
            routes = fu.raw_routes(reg)
            to_finished = [rt for rt in routes if isinstance(rt, dict) and rt.get("slot") == slot]
            if to_finished and not hand:
                sys.exit(f"REFUSED — {len(to_finished)} route(s) still send new rows to {slot}: pass --hand-to "
                         "<the open item that owns that area now> (its routes become handed routes of that item)")
            if same and not to_finished and not riders:
                sys.exit(f"REFUSED — {slot} is already DONE {by}, with no rows riding it and no route to it: nothing left to do")
            if hand:
                try:
                    n = fu.merge_routes(reg, slot, hand)
                except ValueError as exc:
                    sys.exit(f"REFUSED — {exc}")
                said.append(f"{n} route(s) handed from {slot} to {hand}" if n else
                            f"note: no route sent rows to {slot}; --hand-to {hand} had nothing to hand")
            for r in riders:
                routed = fu.route_row(reg, new_prompt_src, str(r.get("title") or ""), list(r.get("files") or []),
                                      str(r.get("severity") or ""))
                if not routed["slot"]:
                    sys.exit(f"REFUSED — {r.get('id')} cannot be moved along the routes: re-slot it first "
                             f"(python scripts/followups.py reslot {r.get('id')} --slot P…) or add a route that owns it")
                said.append(f"{r.get('id')} moved from {slot} to {routed['slot']} — {routed['by']}")
                r["slot"] = routed["slot"]
            said.insert(0, f"{slot} already ✅ DONE {by} — finished what was left" if same else f"{slot} marked ✅ DONE {by}")

        # validate EVERYTHING before writing ANYTHING: both docs must splice, and the change must not ADD a
        # problem (one already there does not block the command that fixes it; lockstep is what render fixes)
        if not fu.plan_items(new_prompt_src):     # never render a plan it could not read, never write past it
            sys.exit("REFUSED — the delivery plan's <delivery_plan> section has no items this code can read; repair "
                     "it first (python scripts/followups.py check names the problem)")
        try:
            new_prompt = fu.splice_all(new_prompt_src, reg, new_prompt_src)
            new_living = fu.splice_all(living, reg, new_prompt_src)
        except ValueError as exc:
            sys.exit(f"REFUSED — {exc}; repair the doc's markers first")
        if args.cmd != "render":
            added = [p for p in fu.check(reg, new_prompt, new_living) if p not in before and p not in fu.LOCKSTEP]
            if added:
                for p in added:
                    print("REFUSED", p)
                return 1
        writes = [(fu.PROMPT, prompt.encode("utf-8"), new_prompt.encode("utf-8")),
                  (fu.LIVING, living.encode("utf-8"), new_living.encode("utf-8"))]
        if args.cmd not in ("render",):
            reg_write = (fu.REGISTER, fu.REGISTER.read_bytes(),
                         (json.dumps(reg, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
            if args.cmd == "done":
                # the register FIRST; whatever lands, running the same done again finishes it (a done item marked
                # by the same round is completed, not refused)
                writes.insert(0, reg_write)
            else:
                writes.append(reg_write)           # last: the register never moves unless both docs did
        try:
            fu.write_all(writes)
        except fu.PartialWrite as exc:
            if args.cmd == "done":
                sys.exit(f"REFUSED — {exc.cause}; these files carry the change and could not be put back: "
                         f"{', '.join(str(p) for p in exc.unrestored)} (every other file is as it was). Run the same "
                         "done command again once the files are free — it finishes whatever did not land")
            sys.exit(f"REFUSED — {exc.cause}; these files still carry the change and could not be put back: "
                     f"{', '.join(str(p) for p in exc.unrestored)} — run python scripts/followups.py render once "
                     "they are free (the register was not changed)")
        except OSError as exc:
            sys.exit(f"REFUSED — could not write {getattr(exc, 'filename', None) or 'a file'} ({exc.strerror or exc}); "
                     "nothing was changed (files already written were put back)")
        if args.cmd == "add":
            print(f"added {added_id}")
        for line in said:
            print(line)
    print("rendered into", fu.PROMPT.name, "and", fu.LIVING.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
