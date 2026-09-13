"""Follow-up register CLI — see agentic_core/plan_followups.py for the rules.

  python scripts/followups.py add --title T --why W --source W462 --slot P2.6 [--files a,b] [--severity high|medium|low] [--owner-gated]
  python scripts/followups.py list [--all]
  python scripts/followups.py close FU-007 --by W463
  python scripts/followups.py drop FU-007 --note "why it is not worth doing"
  python scripts/followups.py reslot FU-007 --slot P2.1 [--ungate]     # --ungate once the Owner has ruled
  python scripts/followups.py reslot FU-007 --gate                     # it waits on the Owner after all
  python scripts/followups.py schedule        # the ordered schedule as the plan will show it
  python scripts/followups.py render          # rewrite the marker blocks in both plan docs
  python scripts/followups.py check           # exit 1 on any problem (the suite's guard runs the same check)

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
    a.add_argument("--slot", required=True, help="a plan item (P2.6), NEXT, or OWNER")
    a.add_argument("--files", default="")
    a.add_argument("--severity", default="medium", choices=fu.SEVERITIES)
    a.add_argument("--owner-gated", action="store_true")
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
    rs.add_argument("--slot")
    g = rs.add_mutually_exclusive_group()
    g.add_argument("--ungate", action="store_true", help="the Owner has ruled: schedule it into --slot")
    g.add_argument("--gate", action="store_true", help="it waits on the Owner: slot OWNER")
    sub.add_parser("schedule")
    sub.add_parser("render")
    sub.add_parser("check")
    args = ap.parse_args()

    if args.cmd in ("check", "list", "schedule"):
        with register_lock():                      # never read the register and the docs from different moments
            reg, prompt, living = _texts()
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
        print(fu.render(reg, prompt))
        return 0

    with register_lock():
        reg, prompt, living = _texts()            # read INSIDE the lock — never a stale copy
        before = set(fu.check(copy.deepcopy(reg), prompt, living))
        if not isinstance(reg, dict) or not isinstance(reg.get("items"), list):
            sys.exit("REFUSED — the register must be an object with an items list")

        if args.cmd == "add":
            nums = [fu.id_number(r.get("id")) for r in reg["items"] if isinstance(r, dict)]
            n = max([x for x in nums if x is not None] or [0]) + 1
            slot = args.slot.strip()
            if args.owner_gated and slot != "OWNER":
                print(f"note: owner-gated work is slotted OWNER (not {slot})")
                slot = "OWNER"
            reg["items"].append({
                "id": f"FU-{n:03d}", "title": _one_line(args.title), "why": _one_line(args.why),
                "source": _one_line(args.source), "found": time.strftime("%Y-%m-%d"),
                "files": [fu.normalise_path(f) for f in args.files.split(",") if f.strip()],
                "severity": args.severity, "owner_gated": bool(args.owner_gated),
                "slot": slot, "status": "open", "closed_by": None, "note": "",
            })
            added_id = f"FU-{n:03d}"
        elif args.cmd == "close":
            r = _find(reg, args.id)
            r["status"], r["closed_by"] = "done", args.by.strip()
        elif args.cmd == "drop":
            r = _find(reg, args.id)
            r["status"], r["note"] = "dropped", _one_line(args.note)
        elif args.cmd == "reslot":
            r = _find(reg, args.id)
            if args.gate:
                r["owner_gated"], r["slot"] = True, "OWNER"
            else:
                if not args.slot:
                    sys.exit("REFUSED — reslot needs --slot (or --gate)")
                if r.get("owner_gated") is True and not args.ungate:
                    sys.exit(f"REFUSED — {args.id} is owner-gated; pass --ungate once the Owner has ruled")
                if args.ungate:
                    r["owner_gated"] = False
                r["slot"] = args.slot.strip()

        # validate EVERYTHING before writing ANYTHING: both docs must splice, and the change must not ADD a
        # problem (one already there does not block the command that fixes it; lockstep is what render fixes)
        block = fu.render(reg, prompt)
        try:
            new_prompt, new_living = fu.splice(prompt, block), fu.splice(living, block)
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
        if args.cmd != "render":                   # last: the register never moves unless both docs did
            writes.append((fu.REGISTER, fu.REGISTER.read_bytes(),
                           (json.dumps(reg, indent=2, ensure_ascii=False) + "\n").encode("utf-8")))
        try:
            fu.write_all(writes)
        except fu.PartialWrite as exc:
            sys.exit(f"REFUSED — {exc.cause}; these files still carry the change and could not be put back: "
                     f"{', '.join(str(p) for p in exc.unrestored)} — run python scripts/followups.py render once "
                     "they are free (the register was not changed)")
        except OSError as exc:
            sys.exit(f"REFUSED — could not write {getattr(exc, 'filename', None) or 'a file'} ({exc.strerror or exc}); "
                     "nothing was changed (files already written were put back)")
        if args.cmd == "add":
            print(f"added {added_id}")
    print("rendered into", fu.PROMPT.name, "and", fu.LIVING.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
