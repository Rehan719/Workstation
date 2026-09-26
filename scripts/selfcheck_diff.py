"""Mechanical pre-flight over the round's OWN uncommitted diff.

Built from a labelled set: the 98 defects the W491 and W492 refutations confirmed. Classifying them by
cause showed that the two largest groups are deterministic to find — 28 were "a second writer or reader
was missed" and 13 were "a new field no consumer reads" — and two more groups (18 vacuous guards, 2
decorator bindings) are partly mechanical. This runs those checks BEFORE the refuter fleet, so the fleet
spends its budget on judgement rather than on bookkeeping I can do exactly.

It reports; it never edits. Every finding names a file:line and what to look at.

    python scripts/selfcheck_diff.py                 # the working-tree diff vs HEAD
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
    out = sh("git", "diff", "--name-only", rev) if rev else sh("git", "diff", "--name-only")
    return [f.strip() for f in out.splitlines() if f.strip()]


def diff_text(rev: str, path: str) -> str:
    return sh("git", "diff", "-U0", rev, "--", path) if rev else sh("git", "diff", "-U0", "--", path)


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


def check_keys(rev: str, files: list[str]) -> list[str]:
    """A dict key added to a .py response, and who reads it. A key only its producer mentions is a
    qualifier that reaches no surface — 13 of the 98 labelled defects were exactly this."""
    out = []
    for f in files:
        if not f.endswith(".py"):
            continue
        added, removed = added_removed(rev, f)
        removed_keys = {k for line in removed for k in KEY_RE.findall(line)}
        for ln, line in added:
            if line.lstrip().startswith("#"):
                continue
            for key in KEY_RE.findall(line):
                if key in BORING_KEYS or key in removed_keys:
                    continue
                hits = (grep_repo(f'"{key}"') + grep_repo("'" + key + "'") + grep_repo("." + key))
                others = {h.split(":", 1)[0] for h in hits} - {f}
                surfaces = {o for o in others
                            if o.endswith((".tsx", ".ts", ".mjs")) or "integration_tests" in o}
                if not surfaces:
                    out.append(f"{f}:{ln}  key '{key}' is produced here and read by no page or test "
                               f"({len(others)} other file(s) mention it) — does any surface show it?")
    return out


def check_renames(rev: str, files: list[str]) -> list[str]:
    """A key removed from a .py, and who still reads it. 28 of the 98 were a surviving second reader."""
    out = []
    for f in files:
        if not f.endswith(".py"):
            continue
        added, removed = added_removed(rev, f)
        added_keys = {k for _, line in added for k in KEY_RE.findall(line)}
        gone = {k for line in removed for k in KEY_RE.findall(line)} - added_keys - BORING_KEYS
        for key in sorted(gone):
            readers = [h for h in (grep_repo(f'"{key}"') + grep_repo("'" + key + "'")
                                   + grep_repo("." + key))
                       if not h.startswith(f + ":")]
            live = sorted({h.split(":", 1)[0] for h in readers} - set(files))
            if live:
                out.append(f"{f}  key '{key}' was removed here; still referenced in "
                           f"{len(live)} file(s) NOT in this diff: {', '.join(live[:6])}"
                           + (" …" if len(live) > 6 else ""))
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
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Dict):
                    keys = {k.value for k in sub.value.keys
                            if isinstance(k, ast.Constant) and isinstance(k.value, str)}
                    if keys:
                        sets.append((sub.lineno, keys))
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
    if not files:
        print("no changed files — nothing to check")
        return 0
    print(f"SELF-CHECK over {len(files)} changed file(s)"
          f"{' vs ' + args.rev if args.rev else ' (working tree)'}\n")

    selected = args.check or list(CHECKS)
    findings: dict[str, list[str]] = {}
    for key in selected:
        label, fn = CHECKS[key]
        try:
            findings[key] = fn(args.rev, files)
        except Exception as e:  # a check that breaks must say so, never pass silently
            findings[key] = [f"CHECK ERROR in '{key}': {type(e).__name__}: {e}"]

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
