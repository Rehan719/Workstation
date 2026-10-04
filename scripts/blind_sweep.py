"""The blind harness — W537 draft, for P2.17 bar (b)3 and Article 5.

WHY THIS FILE EXISTS. Article 5 of this platform's constitution is titled AN INSTRUMENT THAT CANNOT FAIL IS NOT
EVIDENCE, and until W536 its *Verified:* line cited this very path as the mechanism that enforces it. The file
had never been committed, so the article against unfalsifiable evidence rested on something nobody could run.
W536 corrected the claim; this file is what makes the claim true again, and the guard added in W536 ties the two
together — it asserts that while this file is absent the article must SAY so, and that once it exists the
article must stop saying it. They cannot drift apart.

WHAT A BLIND IS. A blind is a mutation that SHOULD make a named check fail: restore the defect, run the
selector, and see whether the guard notices. Every round in this programme already does this by hand; this
harness is the same discipline made repeatable and, crucially, made to report the THREE outcomes rather than
two.

THE THREE OUTCOMES, which is the whole point:
  * BLIND(red)  — the mutation applied cleanly and the selected tests FAILED. The guard sees the defect.
  * VACUOUS     — the mutation applied cleanly and the tests PASSED. The guard is blind to the very defect it
                  was written for. This is the finding; four of these were caught by hand in W535-W536 alone.
  * BAD BLIND   — the run did not get as far as a verdict: the selector matched nothing, collection failed, or
                  pytest errored. The blind is wrong, NOT the guard, and conflating the two is how a sweep
                  reports success while measuring nothing.

EXIT CODES ARE THE DISCRIMINATOR, and this encodes a lesson already paid for: pytest exit 5 means NO TESTS
COLLECTED, and a sweep that reads 5 as "nothing failed, so green" reports off an absent test. It is a BAD
BLIND, never a pass.
      0 -> VACUOUS      (ran, nothing failed)
      1 -> BLIND(red)   (ran, something failed)
      5 -> BAD BLIND    (selector matched nothing)
   2,3,4 -> BAD BLIND   (interrupted, internal error, usage error)

RESTORE IS NOT OPTIONAL AND NOT TRUSTED. Every blind is applied to bytes, restored from bytes, and the restore
is verified against a sha256 taken before the mutation. A sweep that corrupts the tree it measures is worse
than no sweep, and this repository has lost work to exactly that (W462), so the restore runs in a finally and
the verification raises rather than warns.

NOT YET DECIDED, and it must be before this lands: whether a blind may be applied to a file ANOTHER blind in
the same sweep also mutates. Serial application makes that safe; sharding across worktrees (FU-253) does not,
and that is why FU-253 is scheduled after this file exists rather than with it.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import io
import json
import os
import subprocess
import sys
import time
from typing import Any, Dict, List

BLIND_RED = "BLIND(red)"
VACUOUS = "VACUOUS"
BAD_BLIND = "BAD BLIND"

_VERDICT_BY_EXIT = {0: VACUOUS, 1: BLIND_RED, 2: BAD_BLIND, 3: BAD_BLIND, 4: BAD_BLIND, 5: BAD_BLIND,
                    -1: BAD_BLIND}        # -1: refused as nested; pytest was never reached


def _sha(path: str) -> str:
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


NESTED_GUARD_ENV = "WORKSTATION_BLIND_SWEEP_ACTIVE"
NESTED_EXIT = -1          # not a pytest code: a nested sweep never reached pytest at all


def _run_selector(selector: str, test_path: str, env: Dict[str, str]) -> int:
    """Run the selector, unless we are already inside a sweep.

    W537 — A SWEEP MAY NOT RUN INSIDE A SWEEP, and this is structural rather than conventional because the
    failure that produced it was not a mistake in a selector. This harness's own guard calls sweep() to prove
    an ambiguous anchor is refused; a blind driven against that guard disabled the refusal, so the inner sweep
    applied the anchor and ran `-k` on the test that had called it. Thirty-eight python processes, killed by
    hand. A marker in the environment cannot be defeated by a badly chosen selector.
    """
    if env.get(NESTED_GUARD_ENV):
        return NESTED_EXIT
    r = subprocess.run([sys.executable, "-m", "pytest", test_path, "-q", "--no-header",
                        "-p", "no:warnings", "-k", selector],
                       capture_output=True, text=True, errors="replace",
                       env=dict(env, **{NESTED_GUARD_ENV: "1"}))
    return r.returncode


def sweep(blinds: List[Dict[str, Any]], test_path: str, store: str) -> Dict[str, Any]:
    """Apply each blind, run its selector, classify, restore. Returns a report; raises on a failed restore."""
    os.makedirs(os.path.join(store, "projects"), exist_ok=True)
    env = dict(os.environ, DATA_DIR=store, WORKSTATION_DATA_DIR=store,
               WORKSTATION_UEG_PATH=os.path.join(store, "ueg.json"),
               PROJECTS_DIR=os.path.join(store, "projects"),
               AI_DISABLE_LOCAL="1", PYTHONIOENCODING="utf-8")
    results: List[Dict[str, Any]] = []
    for b in blinds:
        path, old, new = b["file"], b["old"], b["new"]
        original = io.open(path, "rb").read()
        before = hashlib.sha256(original).hexdigest()
        src = original.decode("utf-8")
        occurrences = src.count(old)
        if occurrences != 1:
            # The blind's anchor is wrong — that is a BAD BLIND and must never read as a guard verdict.
            results.append({"tag": b["tag"], "verdict": BAD_BLIND, "exit": None,
                            "why": (f"the anchor matched {occurrences} times, not once, so the mutation was "
                                    f"not applied and nothing about the guard was measured")})
            continue
        started = time.time()
        # W537 — AN IN-FLIGHT MARKER, because `finally` does not run when the process is killed and one
        # mutation DID survive a taskkill /F during this round. The marker names the file and the sha to
        # restore to; `--recover` puts the tree back from it. A restore that only works on a clean exit is not
        # a restore for a tool whose whole job is to break things.
        marker = os.path.join(store, "IN_FLIGHT.json")
        try:
            with io.open(marker, "w", encoding="utf-8") as fh:
                json.dump({"file": path, "restore_sha256": before, "tag": b["tag"],
                           "bytes_len": len(original)}, fh)
        except OSError:
            pass
        try:
            io.open(path, "wb").write(src.replace(old, new, 1).encode("utf-8"))
            code = _run_selector(b.get("selector") or b["tag"], test_path, env)
        finally:
            io.open(path, "wb").write(original)
            after = _sha(path)
            if after != before:
                raise RuntimeError(f"RESTORE FAILED for {path}: {before} -> {after}")
            try:
                os.remove(marker)
            except OSError:
                pass
        results.append({"tag": b["tag"], "verdict": _VERDICT_BY_EXIT.get(code, BAD_BLIND),
                        "exit": code, "seconds": round(time.time() - started, 1),
                        "why": {BLIND_RED: "the guard failed on the restored defect",
                                VACUOUS: "the guard PASSED with the defect restored",
                                BAD_BLIND: f"pytest exited {code} without reaching a verdict"}
                               .get(_VERDICT_BY_EXIT.get(code, BAD_BLIND))})
    counts = {v: sum(1 for r in results if r["verdict"] == v) for v in (BLIND_RED, VACUOUS, BAD_BLIND)}
    return {
        "blinds": len(blinds),
        "counts": counts,
        "results": results,
        "basis": (f"{counts[BLIND_RED]} of {len(blinds)} blind(s) were SEEN by their guard; "
                  f"{counts[VACUOUS]} were NOT, which is a guard that cannot fail on its own subject; "
                  f"{counts[BAD_BLIND]} did not reach a verdict and say nothing about any guard"),
        "limits": ("Each blind is applied SERIALLY to the real tree and restored under a verified sha. This "
                   "harness measures whether a guard notices a restored defect; it does not measure whether "
                   "the guard asserts the RIGHT property, and a blind nobody wrote is a defect nobody looked "
                   "for — the sweep's coverage is the blind list, not the codebase"),
    }


SHARD_PIN_ENV = "WORKSTATION_BLIND_SHARD_ROOT"


def _tree_files(extra: List[str]) -> List[str]:
    """Every tracked file, plus any file a blind names that git does not track.

    An untracked blind target is normal in this programme — a round's new guard file or blind list may
    not be added yet — and a copy missing it would turn that blind into a BAD BLIND for a reason that
    has nothing to do with the guard.
    """
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    files = [f for f in out.split("\0") if f]
    known = set(files)
    for f in extra:
        n = f.replace("\\", "/")
        if n not in known and os.path.exists(n):
            files.append(n)
            known.add(n)
    return files


def _materialise(dest: str, files: List[str]) -> Dict[str, Any]:
    """Copy the listed files into `dest`, preserving relative paths. Returns what it actually copied."""
    copied, missing = 0, []
    for f in files:
        src = f
        dst = os.path.join(dest, f.replace("/", os.sep))
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with io.open(src, "rb") as a, io.open(dst, "wb") as b:
                b.write(a.read())
            copied += 1
        except OSError:
            missing.append(f)
    return {"copied": copied, "missing": missing}


def _shard(blinds: List[Dict[str, Any]], n: int) -> List[List[Dict[str, Any]]]:
    """Round-robin, so one long blind does not pile its shard up behind the others."""
    buckets: List[List[Dict[str, Any]]] = [[] for _ in range(max(1, n))]
    for i, b in enumerate(blinds):
        buckets[i % len(buckets)].append(b)
    return [b for b in buckets if b]


def sweep_sharded(blinds: List[Dict[str, Any]], test_path: str, store: str,
                  shards: int) -> Dict[str, Any]:
    """The same sweep, N ways, each shard in its own COPY of the working tree.

    THE REAL TREE IS NEVER MUTATED HERE, and its sha is checked before and after to prove it. Every
    verdict is merged BY TAG and the merge asserts that each blind came back with exactly one: a sweep
    that silently dropped a shard would report a smaller, greener list, which is the defect class this
    whole harness exists to catch.
    """
    started = time.time()
    targets = sorted({b["file"] for b in blinds})
    before = {f: _sha(f) for f in targets if os.path.exists(f)}
    files = _tree_files(targets)
    parts = _shard(blinds, shards)
    procs, roots = [], []
    for i, part in enumerate(parts):
        root = os.path.join(store, f"shard{i}")
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(root, exist_ok=True)
        mat = _materialise(root, files)
        if mat["missing"]:
            raise RuntimeError(f"shard {i}: could not copy {len(mat['missing'])} file(s), first: "
                               f"{mat['missing'][:3]}")
        bl = os.path.join(root, "_shard_blinds.json")
        io.open(bl, "w", encoding="utf-8").write(json.dumps(part, ensure_ascii=False))
        rep = os.path.join(store, f"shard{i}.json")
        env = dict(os.environ)
        env.pop(NESTED_GUARD_ENV, None)
        #  PIN THE IMPORT TO THIS SHARD. PYTHONPATH is inserted ahead of the .pth entries, so the copy
        #  wins over the real repo root the stray jules_ai.pth puts on sys.path. The shard asserts it.
        env["PYTHONPATH"] = root + os.pathsep + env.get("PYTHONPATH", "")
        env[SHARD_PIN_ENV] = root
        env["PYTHONIOENCODING"] = "utf-8"
        procs.append(subprocess.Popen(
            [sys.executable, os.path.join(root, "scripts", "blind_sweep.py"),
             "--blinds", bl, "--tests", test_path,
             "--store", os.path.join(root, "_store"), "--json", rep],
            cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
        roots.append((root, rep, len(part)))
    merged: List[Dict[str, Any]] = []
    shard_notes = []
    for (root, rep, n_expected), pr in zip(roots, procs):
        out = (pr.communicate()[0] or b"").decode("utf-8", "replace")
        if not os.path.exists(rep):
            raise RuntimeError(f"shard at {root} wrote no report (exit {pr.returncode}); tail:\n"
                               f"{out[-700:]}")
        r = json.loads(io.open(rep, encoding="utf-8").read())
        if len(r.get("results") or []) != n_expected:
            raise RuntimeError(f"shard at {root} was given {n_expected} blind(s) and reported "
                               f"{len(r.get('results') or [])}; a dropped blind reads as a greener sweep")
        merged.extend(r["results"])
        shard_notes.append({"root": root, "blinds": n_expected, "exit": pr.returncode})
    #  EVERY BLIND CAME BACK, EXACTLY ONCE. A tag reported twice means a shard ran another's work.
    _tags = [b["tag"] for b in blinds]
    _got = [r["tag"] for r in merged]
    if sorted(_tags) != sorted(_got):
        _lost = sorted(set(_tags) - set(_got))
        _dupe = sorted(t for t in set(_got) if _got.count(t) > 1)
        raise RuntimeError(f"the merge does not match the blind list: {len(_lost)} missing "
                           f"{_lost[:3]}, {len(_dupe)} duplicated {_dupe[:3]}")
    #  AND THE REAL TREE IS UNTOUCHED, which is the sharded path's main safety claim.
    for f, sha in before.items():
        now = _sha(f)
        if now != sha:
            raise RuntimeError(f"THE REAL TREE WAS MUTATED by a sharded sweep: {f} {sha} -> {now}")
    counts = {v: sum(1 for r in merged if r["verdict"] == v) for v in (BLIND_RED, VACUOUS, BAD_BLIND)}
    order = {b["tag"]: i for i, b in enumerate(blinds)}
    merged.sort(key=lambda r: order.get(r["tag"], 0))
    return {
        "blinds": len(blinds), "counts": counts, "results": merged,
        "shards": shard_notes, "wall_seconds": round(time.time() - started, 1),
        "basis": (f"{counts[BLIND_RED]} of {len(blinds)} blind(s) were SEEN by their guard; "
                  f"{counts[VACUOUS]} were NOT, which is a guard that cannot fail on its own subject; "
                  f"{counts[BAD_BLIND]} did not reach a verdict and say nothing about any guard"),
        "limits": ("Run in {n} COPIES of the working tree, one per shard, so THE REAL TREE IS NEVER "
                   "MUTATED and its sha is checked before and after to prove it. Each shard pins "
                   "PYTHONPATH to its own copy and asserts the module under test resolves inside it, "
                   "because a stray .pth puts the real repo root on sys.path and a shard importing the "
                   "ORIGINAL would report confident verdicts about the wrong tree. The merge asserts "
                   "every blind came back exactly once. What it still does NOT measure is whether a "
                   "guard asserts the RIGHT property, and a blind nobody wrote is a defect nobody "
                   "looked for — the sweep's coverage is the blind list, not the codebase"
                   ).replace("{n}", str(len(shard_notes))),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blinds", required=True, help="a JSON file: [{file, old, new, tag, selector}]")
    ap.add_argument("--tests", default="integration_tests/test_mvp_spine.py")
    ap.add_argument("--store", default="/c/tmp/blind_sweep")
    ap.add_argument("--json", default="", help="write the report here as well as printing it")
    ap.add_argument("--shards", type=int, default=1,
                    help="run N shards in parallel, each in its own COPY of the working tree (the real "
                         "tree is then never mutated). 1 keeps the serial path, which stays the trusted "
                         "one until a sharded run is proven to give the same verdicts")
    ap.add_argument("--recover", action="store_true",
                    help="report an in-flight marker left by a killed sweep instead of running")
    a = ap.parse_args()
    marker = os.path.join(a.store, "IN_FLIGHT.json")
    if a.recover:
        if not os.path.exists(marker):
            print("no in-flight marker at %s — no sweep was killed mid-mutation, or its store differs"
                  % marker)
            return 0
        m = json.loads(io.open(marker, encoding="utf-8").read())
        now = _sha(m["file"]) if os.path.exists(m["file"]) else None
        print("IN-FLIGHT MARKER: %s was mutated for %r" % (m["file"], m["tag"]))
        print("  restore sha256: %s" % m["restore_sha256"])
        print("  current sha256: %s" % now)
        print("  STATE: %s" % ("already restored — the marker is stale and can be removed"
                               if now == m["restore_sha256"] else
                               "STILL MUTATED — this file does not match the sha the sweep recorded before "
                               "mutating it, so a killed sweep left its change on disk"))
        return 0 if now == m["restore_sha256"] else 1
    if os.path.exists(marker) and a.shards <= 1:
        print("REFUSING: an in-flight marker is present at %s, so a previous sweep was killed mid-mutation. "
              "Run with --recover first." % marker)
        return 1
    blinds = json.loads(io.open(a.blinds, encoding="utf-8").read())
    #  W572 — EVERY ANCHOR IS CHECKED BEFORE ANY OF THEM RUNS. A blind whose `old` does not match its
    #  file exactly once is not applied, so it reaches a verdict of BAD BLIND and says NOTHING about
    #  any guard — and that is only discovered at the end, after the whole sweep has been paid for.
    #  Two came back that way tonight from a double-escaped em dash in a JSON blind file. The check
    #  costs a second against twenty minutes, so it is a REFUSAL rather than a warning: the point is
    #  to fix every bad anchor in one go and then run the sweep once.
    _bad = []
    for _b in blinds:
        try:
            _hits = io.open(_b["file"], encoding="utf-8").read().count(_b["old"])
        except OSError as _e:                    # noqa: BLE001
            _bad.append((_b.get("tag", "?"), _b.get("file", "?"), f"unreadable: {_e}"))
            continue
        if _hits != 1:
            _bad.append((_b.get("tag", "?"), _b["file"],
                         f"anchor matches {_hits} time(s), not once"))
    if _bad:
        print("REFUSING: %d of %d blind(s) could not be applied, so they would reach no verdict and "
              "say nothing about any guard. Fix them all, then run once:" % (len(_bad), len(blinds)))
        for _t, _f, _w in _bad:
            print("  BAD ANCHOR  %-54s %s  (%s)" % (_t[:54], _w, _f))
        return 1
    #  W569 — A SHARD PROVES IT IS READING ITS OWN COPY BEFORE IT MUTATES ANYTHING. A stray .pth puts
    #  the real repo root on sys.path for every local process, so a shard could import the ORIGINAL
    #  `agentic_core` and report confident verdicts about a tree nobody is committing. PYTHONPATH is
    #  measured to win over the .pth — but "should win" is not a measurement, so this asserts it.
    _pin = os.environ.get(SHARD_PIN_ENV)
    if _pin:
        try:
            import agentic_core as _ac
            _where = os.path.realpath(os.path.dirname(os.path.dirname(_ac.__file__ or "")))
        except Exception as _e:                  # noqa: BLE001
            print(f"REFUSING: shard pinned to {_pin} cannot import its own tree ({_e})")
            return 1
        if os.path.realpath(_pin) != _where:
            print(f"REFUSING: this shard is pinned to {_pin} but imports its subject from {_where}. A "
                  f"sweep reading a different tree than it mutates reports verdicts about code nobody "
                  f"is committing.")
            return 1
    if a.shards > 1:
        rep = sweep_sharded(blinds, a.tests, a.store, a.shards)
    else:
        rep = sweep(blinds, a.tests, a.store)
    for r in rep["results"]:
        print("  %-11s %-54s exit=%-4s %s" % (r["verdict"], r["tag"][:54], r.get("exit"), r.get("why") or ""))
    print("\n" + rep["basis"])
    print("LIMITS: " + rep["limits"])
    if a.json:
        io.open(a.json, "w", encoding="utf-8").write(json.dumps(rep, indent=2))
    # A sweep EXITS NON-ZERO when any guard was blind or any blind was bad, so a round cannot read a sweep
    # that found a vacuous guard as a success.
    return 0 if rep["counts"][VACUOUS] == 0 and rep["counts"][BAD_BLIND] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
