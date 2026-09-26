"""Mechanical pre-flight over the round's OWN uncommitted diff.

Built from a labelled set: the 98 defects the W491 and W492 refutations confirmed. Classifying them by
cause showed that the two largest groups are deterministic to find — 28 were "a second writer or reader
was missed" and 13 were "a new field no consumer reads" — and two more groups (18 vacuous guards, 2
decorator bindings) are partly mechanical. This runs those checks BEFORE the refuter fleet, so the fleet
spends its budget on judgement rather than on bookkeeping I can do exactly.

It reports; it never edits. Every finding names a file:line and what to look at.

    python scripts/selfcheck_diff.py                 # staged AND unstaged, vs HEAD
    python scripts/selfcheck_diff.py --rev HEAD~1    # a committed round
    python scripts/selfcheck_diff.py --check keys    # one check only

Checks
  keys       a dict key added in a changed .py, and who (if anyone) reads it
  renames    a dict key removed in a changed .py, and who still reads it
  routes     a @router decorator bound to a private helper (the insertion trap)
  returns    one function whose dict-literal returns carry different key sets
  selfmatch  a test assertion searching its own file for a literal it contains
  banned     a changed source comment quoting a literal some guard forbids
  order      a branch inserted ahead of an existing one in the same chain

What it CANNOT see (W493, stated so no one trusts it further than it goes)
  A key whose MEANING changed while its NAME stayed. The W493 break was exactly this: `last_evolved`
  kept its name but came to mean "last APPLIED" instead of "last cycle", and two readers went on using
  it with the old meaning - one of them silently starving a round-robin. `renames` compares key NAMES,
  so it reports ok, correctly and uselessly. A semantic change needs the refuters, or a reader-by-reader
  read by hand. Do not read a clean `renames` as "no reader was left behind".

  It also cannot judge whether a new claim is TRUE - the largest group in the labelled set (30 of 98).
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_GLOBS = ("**/*.py", "**/*.ts", "**/*.tsx", "**/*.mjs", "**/*.js", "**/*.json", "**/*.md")
SEARCH_DIRS = ("agentic_core", "apps/workstation-superapp/src", "packages", "integration_tests",
               "scripts", "docs")
# keys that are structural noise rather than claims a surface reads
BORING_KEYS = {
    "id", "name", "type", "status", "error", "note", "at", "ts", "data", "value", "label", "detail",
    "message", "output", "result", "reason", "total", "count", "items", "rows", "path", "url", "kind",
}


def sh(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def changed_files(rev: str) -> list[str]:
    """W493 (refutation) - this ran bare `git diff`, which shows UNSTAGED changes only, while the
    docstring advertised "the working-tree diff vs HEAD". A pre-flight runs immediately before a
    commit, i.e. after `git add`, so on the normal path it saw nothing and reported clean on exactly
    the diff being committed. Defaulting to HEAD covers staged and unstaged together."""
    out = sh("git", "diff", "--name-only", rev or "HEAD")
    return [f.strip() for f in out.splitlines() if f.strip()]


def diff_text(rev: str, path: str) -> str:
    return sh("git", "diff", "-U0", rev or "HEAD", "--", path)


def added_removed(rev: str, path: str) -> tuple[list[tuple[int, str]], list[str]]:
    """(added lines with their new line numbers, removed lines)."""
    added: list[tuple[int, str]] = []
    removed: list[str] = []
    line_no = 0
    for raw in diff_text(rev, path).splitlines():
        if raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            line_no = int(m.group(1)) if m else 0
            continue
        if raw.startswith("+++") or raw.startswith("---"):
            continue
        if raw.startswith("+"):
            added.append((line_no, raw[1:]))
            line_no += 1
        elif raw.startswith("-"):
            removed.append(raw[1:])
    return added, removed


def touched_ranges(rev: str, path: str) -> set[int]:
    """Every new-file line a hunk touched, DELETIONS INCLUDED.

    The first version of this tool asked only for added lines, so a function changed purely by removing
    keys from a return was treated as unchanged and skipped — which is precisely the defect the `returns`
    check exists to find. Measured against a known W492 defect, that bug made the check miss it."""
    out: set[int] = set()
    for raw in diff_text(rev, path).splitlines():
        if not raw.startswith("@@"):
            continue
        m = re.search(r"\+(\d+)(?:,(\d+))?", raw)
        if not m:
            continue
        start = int(m.group(1))
        length = int(m.group(2) or 1)
        # a pure deletion reports length 0 at the line the removal sat before: widen to a small window
        out.update(range(max(1, start - 2), start + max(length, 1) + 2))
    return out


_grep_cache: dict[str, list[str]] = {}


def grep_repo(needle: str) -> list[str]:
    """Every file:line mentioning this literal, across code, tests, scripts and docs."""
    if needle in _grep_cache:
        return _grep_cache[needle]
    hits: list[str] = []
    for d in SEARCH_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        out = sh("git", "grep", "-n", "--fixed-strings", needle, "--", d)
        hits += [h for h in out.splitlines() if h.strip()]
    _grep_cache[needle] = hits
    return hits


# ── keys / renames ─────────────────────────────────────────────────────────────────────────────────
KEY_RE = re.compile(r'"([a-z_][a-z0-9_]{2,})"\s*:')
# W493 — a key is also introduced and removed by SUBSCRIPT ASSIGNMENT (`vsb["last_evolved"] = now`),
# which the first version did not match at all. A real break slipped through that gap in this round:
# renaming such a key left two readers, one of which would have starved a round-robin.
ASSIGN_KEY_RE = re.compile(r'\[\s*"([a-z_][a-z0-9_]{2,})"\s*\]\s*=')


def keys_in(line: str) -> set[str]:
    """Every dict key this line introduces, as a literal pair OR a subscript assignment."""
    return set(KEY_RE.findall(line)) | set(ASSIGN_KEY_RE.findall(line))


def check_keys(rev: str, files: list[str]) -> list[str]:
    """A dict key added to a .py response, and who reads it. A key only its producer mentions is a
    qualifier that reaches no surface — 13 of the 98 labelled defects were exactly this."""
    out = []
    for f in files:
        # W493 - a TEST file's dict literals are request bodies and expectations, not produced fields;
        # scanning them produced only noise on the first real round.
        if not f.endswith(".py") or "test_" in Path(f).name:
            continue
        added, removed = added_removed(rev, f)
        removed_keys = {k for line in removed for k in keys_in(line)}
        for ln, line in added:
            if line.lstrip().startswith("#"):
                continue
            for key in keys_in(line):
                if key in BORING_KEYS or key in removed_keys:
                    continue
                hits = (grep_repo(f'"{key}"') + grep_repo("'" + key + "'") + grep_repo("." + key))
                others = {h.split(":", 1)[0] for h in hits} - {f}
                # W493 (refutation) - this was narrowed to "skip if ANY other file mentions it", which
                # made the printed label ("read by no surface") false: docs/ and integration_tests are
                # searched, and this process REQUIRES a register row and habitually writes a
                # source-substring guard in the same commit, so almost every new key was exempt. A
                # SURFACE is a page; a guard asserting a literal and a register row are not surfaces.
                surfaces = {o for o in others
                            if o.endswith((".tsx", ".mjs")) or (o.endswith(".ts") and not o.endswith(".d.ts"))}
                if surfaces:
                    continue
                internal = {o for o in others if o.endswith(".py") and "test_" not in Path(o).name}
                where = (f"only {len(internal)} backend module(s) read it"
                         if internal else "nothing outside this file reads it")
                out.append(f"{f}:{ln}  key '{key}' is produced here and NO page reads it — {where}"
                           f"{' (a guard or a register row is not a surface)' if others and not internal else ''}"
                           f". If it qualifies a claim, which surface shows it?")
    return out


def check_renames(rev: str, files: list[str]) -> list[str]:
    """A key removed from a .py, and who still reads it. 28 of the 98 were a surviving second reader."""
    out = []
    for f in files:
        if not f.endswith(".py"):
            continue
        added, removed = added_removed(rev, f)
        added_keys = {k for _, line in added for k in keys_in(line)}
        gone = {k for line in removed for k in keys_in(line)} - added_keys - BORING_KEYS
        for key in sorted(gone):
            readers = [h for h in (grep_repo(f'"{key}"') + grep_repo("'" + key + "'")
                                   + grep_repo("." + key))
                       if not h.startswith(f + ":")]
            # W493 (refutation) - this subtracted EVERY file in the diff, assuming a touched file had
            # been updated for THIS key. Nothing checked that. On the round that added this comment,
            # all three surviving readers of the renamed key were in the diff, so the check printed
            # "ok" for the very break it was written to catch - one of which starved a round-robin.
            # A reader is live if the key is STILL in that file's current content, touched or not.
            live = []
            for other in sorted({h.split(":", 1)[0] for h in readers}):
                try:
                    body = (ROOT / other).read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue
                if key in body:
                    live.append(other + (" (also in this diff)" if other in files else ""))
            if live:
                out.append(f"{f}  key '{key}' was removed here and is STILL referenced in "
                           f"{len(live)} file(s): {', '.join(live[:6])}"
                           + (" …" if len(live) > 6 else "")
                           + " — confirm each one was updated for this rename")
    return out


# ── routes ─────────────────────────────────────────────────────────────────────────────────────────
def check_routes(rev: str, files: list[str]) -> list[str]:
    """A @router decorator bound to a private helper. The W492 live break: a helper inserted between the
    decorator and its handler silently took the route, and the app still booted."""
    out = []
    for f in files:
        if not f.endswith(".py"):
            continue
        try:
            tree = ast.parse((ROOT / f).read_text(encoding="utf-8"))
        except Exception as e:
            out.append(f"{f}  could not parse to check route bindings: {e}")
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            decs = [ast.unparse(d) for d in node.decorator_list]
            if any(re.search(r"\brouter\.(get|post|put|patch|delete)\b", d) for d in decs):
                if node.name.startswith("_"):
                    out.append(f"{f}:{node.lineno}  a route decorator is bound to the private helper "
                               f"'{node.name}' — the handler below it is registered nowhere. "
                               f"Move the helper ABOVE the decorator and CALL the route to verify.")
    return out


# ── returns ────────────────────────────────────────────────────────────────────────────────────────
def _returned_dicts(node: ast.AST) -> list[ast.Dict]:
    """The dict literals a `return <expr>` can actually evaluate TO - not every dict inside it.

    W493 (refutation): walking the whole expression counted a nested sub-object as a sibling return.
    Only the value itself and the operands of a top-level or/and/conditional are alternatives."""
    if isinstance(node, ast.Dict):
        return [node]
    if isinstance(node, ast.BoolOp):
        return [d for v in node.values for d in _returned_dicts(v)]
    if isinstance(node, ast.IfExp):
        return _returned_dicts(node.body) + _returned_dicts(node.orelse)
    return []


def _own_returns(fn: ast.AST) -> list[ast.Return]:
    """The Return nodes belonging to THIS function - not those of functions nested inside it.

    W493: ast.walk() crosses into nested `def`/`lambda` bodies, so an inner helper's returns were
    reported as siblings of the enclosing function's, which is a different contract entirely."""
    out: list[ast.Return] = []

    def walk(node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
                continue                      # its own scope, its own return contract
            if isinstance(child, ast.Return):
                out.append(child)
            walk(child)

    walk(fn)
    return out


def check_returns(rev: str, files: list[str]) -> list[str]:
    """One function whose dict-literal returns carry different key sets. A reader indexing a key that
    only some branch sets gets undefined — and prints it."""
    out = []
    changed_lines = {f: touched_ranges(rev, f) for f in files
                     if f.endswith(".py") and "test_" not in Path(f).name}
    for f, lines in changed_lines.items():
        if not lines:
            continue
        try:
            tree = ast.parse((ROOT / f).read_text(encoding="utf-8"))
        except Exception:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            end = getattr(node, "end_lineno", node.lineno)
            if not any(node.lineno <= ln <= end for ln in lines):
                continue
            sets: list[tuple[int, set[str]]] = []
            # W493 (the round's own second pre-flight pass) - ast.walk descends into NESTED function
            # bodies, so a helper defined inside a function had its returns counted as siblings of the
            # outer function's. That accused three correct returns in this round's own planner change:
            # an inner _item_rate() returning {rate, assessable} is not a sibling of the outer
            # forecast()'s {assessable, window, ...}. A nested def has its own return contract and is
            # visited as its own node by the enclosing walk.
            for sub in _own_returns(node):
                if sub.value is None:
                    continue
                # W493 — the first version required Return.value to BE a dict, so it missed the very
                # common `return helper(x) or {...}` and `return a if c else {...}` shapes.
                # W493 (refutation) — but walking the WHOLE expression then counted dicts NESTED inside
                # a returned dict as extra "sibling returns", diluting the threshold below and falsely
                # accusing a return whose sub-object happens to carry different keys. Only the dicts a
                # return can actually evaluate TO are siblings: the value itself, or the operands of a
                # top-level `or`/`and`/conditional.
                for inner in _returned_dicts(sub.value):
                    keys = {k.value for k in inner.keys
                            if isinstance(k, ast.Constant) and isinstance(k.value, str)}
                    if keys:
                        sets.append((getattr(inner, "lineno", sub.lineno), keys))
            if len(sets) < 2:
                continue
            union = set().union(*(s for _, s in sets))
            for ln, keys in sets:
                missing = union - keys
                # only report keys that at least half the returns carry: a genuinely shared shape
                shared = {k for k in missing if sum(1 for _, s in sets if k in s) >= len(sets) / 2}
                if shared:
                    out.append(f"{f}:{ln}  this return omits {sorted(shared)} which sibling returns in "
                               f"{node.name}() carry — a reader indexing them here gets undefined")
    return out


# ── test-guard shapes ──────────────────────────────────────────────────────────────────────────────
ASSERT_IN_RE = re.compile(r"""assert\s+(?P<neg>not\s+)?['"](?P<lit>[^'"]{6,})['"]\s+(?:not\s+)?in\s+(?P<var>\w+)""")
ASSERT_NOTIN_RE = re.compile(r"""assert\s+['"](?P<lit>[^'"]{6,})['"]\s+not\s+in\s+(?P<var>\w+)""")


def check_selfmatch(rev: str, files: list[str]) -> list[str]:
    """A test assertion searching its OWN file for a literal the assertion itself contains: it matches
    itself and can never fail. Hit twice in W491, in both directions."""
    out = []
    for f in files:
        if "test_" not in Path(f).name or not f.endswith(".py"):
            continue
        src = (ROOT / f).read_text(encoding="utf-8")
        # which locals hold this file's own text?
        selfvars = set(re.findall(r"(\w+)\s*=\s*\(?root\s*/\s*['\"]" + re.escape(f) + r"['\"]\)?\.read_text", src))
        selfvars |= set(re.findall(r"(\w+)\s*=\s*.*__file__.*read_text", src))
        for ln, line in added_removed(rev, f)[0]:
            m = ASSERT_IN_RE.search(line)
            if m and m.group("var") in selfvars:
                out.append(f"{f}:{ln}  this assertion reads its OWN file and searches for a literal the "
                           f"line itself contains — it matches itself and cannot fail. Assert the "
                           f"contract against a live response instead.")
    return out


SRC_READ_RE = re.compile(
    r"""(?P<var>\w+)\s*=\s*\(?\s*(?:root|app|S)\s*/\s*["'](?P<path>[^"']+)["']\s*\)?\s*\.read_text""")


def check_banned(rev: str, files: list[str]) -> list[str]:
    """A changed source comment quoting a literal a guard forbids IN THAT FILE. Cheap, and it cost ~6
    failed guard runs per round.

    The forbidden literal is scoped to the file its assertion actually targets: a guard reading
    `mkt = (app / "pages/.../LivingMarketplace.tsx").read_text()` and asserting `"x" not in mkt`
    forbids "x" in that file only. Applying such literals globally floods the report with generic
    words ("status", "verified") — which is how the first version of this check behaved."""
    forbidden: dict[str, list[tuple[str, str]]] = defaultdict(list)   # target path -> [(lit, test file)]
    for tf in sorted(ROOT.glob("integration_tests/*.py")):
        text = tf.read_text(encoding="utf-8")
        # var -> the source file that variable holds, per test module
        var_path = {m.group("var"): m.group("path") for m in SRC_READ_RE.finditer(text)}
        app_prefix = "apps/workstation-superapp/src/"
        for m in ASSERT_NOTIN_RE.finditer(text):
            lit, var = m.group("lit"), m.group("var")
            if len(lit) < 12:          # a short generic word is not a distinctive claim
                continue
            target = var_path.get(var)
            if not target:
                continue
            for cand in (target, app_prefix + target):
                if (ROOT / cand).exists():
                    forbidden[cand].append((lit, tf.name))
                    break
    out = []
    for f in files:
        if f.endswith(".py") and "test_" in Path(f).name:
            continue
        rules = forbidden.get(f)
        if not rules:
            continue
        for ln, line in added_removed(rev, f)[0]:
            stripped = line.strip()
            is_comment = stripped.startswith(("#", "//", "*", "/*")) or stripped.startswith("{/*")
            if not is_comment:
                continue
            for lit, where in rules:
                if lit in line:
                    out.append(f"{f}:{ln}  a comment added here quotes '{lit[:60]}', which {where} "
                               f"asserts must NOT appear in THIS file — reword the comment")
    return out


def check_order(rev: str, files: list[str]) -> list[str]:
    """A branch inserted ahead of an existing one in the same chain. W492: making a failed screen HOLD
    a listing put `held` first and made the round's own error notice unreachable."""
    out = []
    for f in files:
        if not f.endswith((".tsx", ".ts")):
            continue
        added, _ = added_removed(rev, f)
        for ln, line in added:
            s = line.strip()
            if re.match(r"^[?:]?\s*\w[\w.?\[\]']*\s*===?\s*['\"]", s) and ("?" in s or s.startswith(":")):
                out.append(f"{f}:{ln}  a condition was added into a ternary chain — confirm the arm "
                           f"BELOW it is still reachable (and that this one is)")
    return out


CHECKS = {
    "keys": ("a key produced but read by no surface", check_keys),
    "renames": ("a key removed while other files still read it", check_renames),
    "routes": ("a route decorator bound to a private helper", check_routes),
    "returns": ("sibling returns with different key sets", check_returns),
    "selfmatch": ("a test assertion that matches its own text", check_selfmatch),
    "banned": ("a comment quoting a literal a guard forbids", check_banned),
    "order": ("a branch inserted ahead of an existing one", check_order),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="", help="compare against this rev (default: the working tree)")
    ap.add_argument("--check", action="append", choices=sorted(CHECKS), help="run only these checks")
    args = ap.parse_args()

    files = changed_files(args.rev)
    # W493 (refutation) — the banner used to print only AFTER this early exit, so on a clean tree the
    # tool printed "no changed files" and nothing else. A guard asserting the banner therefore passed
    # only while the author's copy was dirty, and failed in CI the moment the round was committed. The
    # banner always prints, and says plainly when there was nothing to compare.
    print(f"SELF-CHECK over {len(files)} changed file(s)"
          f"{' vs ' + args.rev if args.rev else ' (working tree)'}"
          f"{' — nothing to compare, so no check ran' if not files else ''}\n")
    if not files:
        return 0

    selected = args.check or list(CHECKS)
    findings: dict[str, list[str]] = {}
    # W493 (refutation) - main() returned 0 on every path, including when a check RAISED, so a guard
    # asserting the exit code could not fail even with the tool broken. A check that cannot run is a
    # failure of the tool and now exits non-zero; FINDINGS still exit 0, because they are leads.
    errored: list[str] = []
    for key in selected:
        label, fn = CHECKS[key]
        try:
            findings[key] = fn(args.rev, files)
        except Exception as e:  # a check that breaks must say so, never pass silently
            findings[key] = [f"CHECK ERROR in '{key}': {type(e).__name__}: {e}"]
            errored.append(key)

    total = 0
    for key in selected:
        label = CHECKS[key][0]
        rows = findings[key]
        head = f"[{key}] {label}"
        if not rows:
            print(f"  ok   {head}")
            continue
        total += len(rows)
        print(f"  {len(rows):<4} {head}")
        for r in rows:
            print(f"         - {r}")
    print(f"\n{total} thing(s) to look at. These are LEADS, not verdicts: each one is a place the last "
          f"two rounds' refutations found real defects.")
    if errored:
        print(f"\n{len(errored)} CHECK(S) COULD NOT RUN: {', '.join(errored)} - the tool is broken, "
              f"so a clean report above means nothing for those checks.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
