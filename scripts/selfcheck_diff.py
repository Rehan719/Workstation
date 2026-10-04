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


def deleted_files(rev: str) -> set:
    """Paths this diff DELETES.

    W575 — A DELETED FILE IS NOT A RENAME, and the screens have to know the difference. Retiring
    `ontology_engine.py` on the Owner's ruling made the [renames] screen report seven of its keys as
    "removed and still referenced", naming 135 files for `basis`, 85 for `domain`, 47 for `query` —
    every unrelated dict in the repository that happens to use a common key name. Eight leads, none
    of them real, in a round whose only genuine lead would have been lost among them. The [routes]
    screen then tried to AST-parse a path that no longer exists and reported the OSError as a
    finding. A screen that cries wolf on every deletion is how a true lead gets skimmed past.
    """
    out = sh("git", "diff", "--name-only", "--diff-filter=D", rev or "HEAD")
    return {f.strip() for f in out.splitlines() if f.strip()}


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
        # W542 — `--untracked`, because without it this searched only files git already knows about, and a
        # SURFACE ADDED IN THE SAME ROUND AS ITS KEY IS UNTRACKED. The keys screen therefore printed "NO
        # page reads it" for fourteen keys that the page committed beside them read perfectly well, and the
        # screen whose whole purpose is to find a field that reaches no surface was blind to the one case
        # where the surface is new. A false absence from an instrument is worse than no instrument: it sends
        # a round looking for a defect that is not there, and it would pass silently on the day it matters.
        out = sh("git", "grep", "-n", "--untracked", "--fixed-strings", needle, "--", d)
        hits += [h for h in out.splitlines() if h.strip()]
    _grep_cache[needle] = hits
    return hits


_WORD_TAIL = re.compile(r"[A-Za-z0-9_]")


def reads_key(line: str, key: str) -> bool:
    """Does this line reference THIS key, rather than one that merely starts with it?

    W494 - `renames` reported `arms_length` as an orphaned key because a page mentions
    `charter.arms_length_agency`: a key that is a PREFIX of another key matched it. The same trap the
    blind harness hits with a twice-occurring anchor. A reference must not continue into another
    identifier character."""
    for form in (f'"{key}"', f"'{key}'", f".{key}"):
        start = 0
        while True:
            i = line.find(form, start)
            if i < 0:
                break
            end = i + len(form)
            # a quoted form is already delimited; a dotted one must not run on into a longer name
            if form.startswith(".") and end < len(line) and _WORD_TAIL.match(line[end]):
                start = i + 1
                continue
            return True
    return False


# ── keys / renames ─────────────────────────────────────────────────────────────────────────────────
KEY_RE = re.compile(r'"([a-z_][a-z0-9_]{2,})"\s*:')
# W493 — a key is also introduced and removed by SUBSCRIPT ASSIGNMENT (`vsb["last_evolved"] = now`),
# which the first version did not match at all. A real break slipped through that gap in this round:
# renaming such a key left two readers, one of which would have starved a round-robin.
# W534 (FU-319) — the `=` here used to match the FIRST CHARACTER OF `==`, so a dict READ being compared was
# counted as a key PRODUCED. The lookahead requires a real assignment. `!=`, `>=` and `<=` never matched,
# because each puts another character between the bracket and the equals sign.
ASSIGN_KEY_RE = re.compile(r'\[\s*"([a-z_][a-z0-9_]{2,})"\s*\]\s*=(?!=)')

# W534 (FU-319) — a line opening with one of these ENDS in a statement colon, so a quoted word immediately
# before that final colon belongs to a comparison or a label, not to a dict.
_BLOCK_KW = frozenset(("if", "elif", "while", "for", "case", "match", "with", "else", "try", "except",
                       "finally", "def", "class", "async"))


def keys_in(line: str) -> set[str]:
    """Every dict key this line introduces, as a literal pair OR a subscript assignment.

    W534 (FU-319) — this reported any `if x == "name":` as a produced key, because the regex sees a quoted
    word followed by a colon and every dispatcher in this repository is built from those lines. The screen
    then asked which page shows a CLI subcommand name. No page shows one and none should.

    The test is POSITIONAL, because the distinction is: on a line that opens a block, the FINAL colon
    terminates the statement, so a match ending at it used that colon and is not a key. A dict key whose
    value sits on the next line still ends its line with a colon, but its line does not open a block, so it
    is still reported — the exclusion is kept as narrow as the defect.
    """
    body = line.split(" #")[0].rstrip()
    head = body.lstrip().split("(")[0].split(":")[0].split()
    opens_block = bool(head) and head[0] in _BLOCK_KW
    out = set()
    for m in KEY_RE.finditer(body):
        if opens_block and m.end() == len(body):
            continue
        out.add(m.group(1))
    return out | set(ASSIGN_KEY_RE.findall(body))


_LOG_METHODS = {"info", "warning", "warn", "error", "debug", "exception", "critical", "log"}


def _emitting_calls(path: str) -> list[str]:
    """The SOURCE of every call in `path` that puts text in front of someone: print, or a logger method.

    ON THE AST, NOT ON THE TEXT, and that distinction is the whole point of this fix. FU-348 records
    that its own screen family has produced four precision defects with one shape — "a textual proxy
    standing in for a structural question" — so "a line in scripts/ mentions the key near the word
    print" would be a fifth. The structural question is whether the key is read INSIDE an emitting
    call, and a Call node answers it.

    Returns source segments rather than nodes so the caller can ask whether a key appears in one. A
    file that will not parse yields nothing: a screen cannot claim a surface it could not read.
    """
    #  `Path.read_text`, because this module does not import `io` — and the first version of this
    #  helper used it and died with NameError on its first call. A helper added to an existing file
    #  inherits that file's imports and nothing else.
    try:
        src = Path(path).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except (OSError, SyntaxError, ValueError):
        return []
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        emits = (isinstance(f, ast.Name) and f.id == "print") or (
            isinstance(f, ast.Attribute) and f.attr in _LOG_METHODS)
        if not emits:
            continue
        seg = ast.get_source_segment(src, n)
        if seg:
            out.append(seg)
    return out


def _mentions(seg: str, key: str) -> bool:
    """Does this source segment read `key` directly — as a literal, an attribute or a subscript?"""
    return (f'"{key}"' in seg or f"'{key}'" in seg or f".{key}" in seg)


def _aliases_of(path: str, key: str) -> set[str]:
    """Local names bound from an expression that reads `key`, in `path`.

    ONE LEVEL. `_nc = _out.get("not_considered_row_count")` binds `_nc`, so emitting `_nc` emits the
    key's value. Two levels (`a = d["k"]; b = a; print(b)`) are NOT followed, and a helper that returns
    it is not followed either: this is a diff screen, not an analyser, and the honest boundary is stated
    rather than discovered later.
    """
    try:
        src = Path(path).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except (OSError, SyntaxError, ValueError):
        return set()
    out: set[str] = set()
    for n in ast.walk(tree):
        if not isinstance(n, (ast.Assign, ast.AnnAssign)):
            continue
        val = n.value
        if val is None:
            continue
        seg = ast.get_source_segment(src, val) or ""
        if not _mentions(seg, key):
            continue
        targets = n.targets if isinstance(n, ast.Assign) else [n.target]
        for t in targets:
            if isinstance(t, ast.Name):
                out.add(t.id)
    #  A ONE-CHARACTER ALIAS WOULD MATCH ALMOST ANY SEGMENT, so it is refused rather than trusted: a
    #  false surface is worse here than a missed one, because it makes the screen CLEAR something.
    return {a for a in out if len(a) >= 2}


def _cli_surfaces(candidates: set[str], key: str) -> set[str]:
    """Which candidate files EMIT this key's value — a surface for a round rather than for a page.

    A key whose consumer is a round is surfaced by a CLI, and FU-345's subject was exactly that: the
    round-start step states its own width by printing it. Counting only pages made such a key read as
    unsurfaced by construction.

    IT IS NARROW ON PURPOSE. Only .py files, only calls that actually emit, and the key must appear in
    the emitting call's own source. A mention anywhere else in the file does not count — the W493
    refutation already narrowed this screen once for exactly that reason, when "any other file mentions
    it" made the printed label false.
    """
    found = set()
    for c in sorted(candidates):
        if not c.endswith(".py") or "test_" in Path(c).name:
            continue
        #  ONE LEVEL OF INDIRECTION, AND MEASURED ON THE REAL CASE. followups.py does
        #  `_nc = _out.get("not_considered_row_count")` and then prints `_nc`, so the key's literal is
        #  never inside the print — asking only "is the key in an emitting call" answered NONE for the
        #  exact case FU-348 was filed about. That would have been a fix that did not fix it.
        #  ONE level, not full dataflow: a key passed through two bindings or into a helper is NOT seen,
        #  and a screen claiming more reach than it has is this family's own defect. The finding stays
        #  a LEAD either way.
        aliases = _aliases_of(c, key)
        for seg in _emitting_calls(c):
            if _mentions(seg, key) or any(re.search(rf"\b{re.escape(a)}\b", seg) for a in aliases):
                found.add(c)
                break
    return found


# ── route responses: the THIRD kind of surface ──────────────────────────────────────────────────────
# W578 (FU-396) — a key produced by a route NO PAGE FETCHES still reaches a reader: through the route's
# own JSON. The screen knew two kinds, a page and a printed line, so it reported nine such keys as
# reaching NO SURFACE AT ALL. Each of those nine was a true statement about where no page is and a false
# conclusion about whether anybody can read the key.
#
# STATIC resolution, deliberately. reach_audit.py imports the app to walk `app.routes`, which is exact
# and touches the stores; this runs before every commit and must mutate nothing. A suite guard
# cross-checks what is composed here against the real route table, so the exactness is proven elsewhere.
_MOUNTS: dict | None = None


def _route_mounts() -> dict:
    """{module stem: mount prefix} from app_mvp.py's include_router calls, plus each router's own."""
    global _MOUNTS
    if _MOUNTS is not None:
        return _MOUNTS
    mounts: dict = {}
    app_src = ""
    try:
        app_src = (Path("agentic_core/app_mvp.py")).read_text(encoding="utf-8", errors="replace")
    except OSError:
        _MOUNTS = mounts
        return mounts
    #  `from agentic_core.api.v310 import payments as payments_v310` → alias to module stem
    alias: dict = {}
    for m in re.finditer(r"from\s+agentic_core\.api[\w.]*\s+import\s+(\w+)(?:\s+as\s+(\w+))?", app_src):
        alias[m.group(2) or m.group(1)] = m.group(1)
    #  `app.include_router(x.router, prefix="/api/v310")`
    for m in re.finditer(r"include_router\(\s*(\w+)\.router\s*(?:,\s*prefix\s*=\s*[\"']([^\"']*)[\"'])?", app_src):
        stem = alias.get(m.group(1), m.group(1))
        mounts.setdefault(stem, m.group(2) or "")
    _MOUNTS = mounts
    return mounts


def _router_prefix(path: str) -> str:
    """The `APIRouter(prefix=...)` declared in this module, or ""."""
    try:
        src = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r"APIRouter\((?:[^)]*?)prefix\s*=\s*[\"']([^\"']*)[\"']", src, re.S)
    return m.group(1) if m else ""


def _route_of(path: str, line_no: int) -> str | None:
    """The full route path of the handler CONTAINING line_no, or None when that line is not in one.

    Composed as mount + router prefix + the decorator's own path. A decorator path that already starts
    with the mount (several routes in this repo declare the whole path on the decorator) is not
    double-prefixed.
    """
    try:
        src = Path(path).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return None
    stem = Path(path).stem
    mount = _route_mounts().get(stem, "")
    rp = _router_prefix(path)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not (node.lineno <= line_no <= (node.end_lineno or node.lineno)):
            continue
        for d in node.decorator_list:
            seg = ast.get_source_segment(src, d) or ""
            m = re.search(r"router\.(get|post|put|delete|patch)\(\s*[\"']([^\"']*)[\"']", seg)
            if not m:
                continue
            own = m.group(2)
            if own.startswith("/api/"):           # the decorator carries the whole path already
                return own
            return (mount + rp + own) or None
    return None


def _route_response_surface(f: str, key: str, line_no: int) -> str | None:
    """The route whose own response is this key's surface, or None.

    Returns a path ONLY when no frontend file fetches it. When a page DOES fetch the route and still
    does not read the key, that is the real defect and this must stay silent so the screen reports it —
    a false surface here is worse than a missed one, because it makes the screen CLEAR something.
    """
    route = _route_of(f, line_no)
    if not route:
        return None
    #  a path parameter matches whatever the page interpolates, so compare on the literal prefix
    stem = route.split("{")[0].rstrip("/")
    if not stem:
        return None
    for hit in grep_repo(stem):
        p = hit.split(":", 1)[0]
        if p.endswith((".tsx", ".mjs")) or (p.endswith(".ts") and not p.endswith(".d.ts")):
            return None                      # a page fetches it: the page is the surface, or nothing is
    return route


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
                # W578 — THIS SCREEN'S OWN DISPATCH TABLE. Registering a new screen adds a dict entry
                # whose key is the screen's name, and the keys screen read that as a produced field
                # reaching no surface. It is not a response: it maps a name to a function. A blind spot
                # this screen always had for its own registry, invisible until a round added to it.
                # Derived from SCREENS rather than a hardcoded list, so it cannot go stale.
                if f.endswith("selfcheck_diff.py") and key in CHECKS:
                    continue
                hits = [h for h in (grep_repo(f'"{key}"') + grep_repo("'" + key + "'")
                                    + grep_repo("." + key)) if reads_key(h, key)]
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
                # W570 (FU-348) - A KEY WHOSE CONSUMER IS A ROUND IS SURFACED BY A CLI. This counted
                # only pages, so such a key reached "no surface" BY CONSTRUCTION: FU-345's whole
                # subject was that the round-start step states its own width, and that step prints it.
                # Asked on the AST - is the key read inside a print or a log call - because this screen
                # family has produced four precision defects with one shape, a textual proxy standing
                # in for a structural question, and "a line mentions the key near print" is a fifth.
                cli = _cli_surfaces(others, key)
                if cli:
                    continue
                # W578 (FU-396) — THE THIRD KIND. A key produced by a route no page fetches reaches a
                # reader through that route's own JSON, and this screen used to call that no surface at
                # all. The label says which case it took, because "no page reads it" and "no page EXISTS
                # to read it" are different findings and a round acts on them differently.
                _resp = _route_response_surface(f, key, ln)
                if _resp:
                    out.append(f"{f}:{ln}  key '{key}' reaches no page, and NO PAGE IN THIS APP FETCHES "
                               f"{_resp} - so that route's own response is the surface a person reads. "
                               f"Confirm a guard asserts the key is IN that response; if a page is later "
                               f"written for this route, it must render it.")
                    continue
                internal = {o for o in others if o.endswith(".py") and "test_" not in Path(o).name}
                # AND THE TWO FINDINGS ARE NOW DIFFERENT. "No page reads it" was printed whether a CLI
                # showed the value or nothing did, so a round could not tell NO PAGE from NOBODY.
                where = (f"only {len(internal)} backend module(s) read it, and none of them PRINTS it"
                         if internal else "nothing outside this file reads it")
                out.append(f"{f}:{ln}  key '{key}' is produced here and reaches NO SURFACE AT ALL - no "
                           f"page renders it and no print or log statement emits it - {where}"
                           f"{' (a guard or a register row is not a surface)' if others and not internal else ''}"
                           f". If it qualifies a claim, which surface shows it?")
    return out


# ── plan pins: a guard that fails when the plan ADVANCES ────────────────────────────────────────────
# W578 (FU-365). An assertion whose truth requires an item to be INCOMPLETE goes red on success, and the
# bill arrives after the full suite. This screens a round's OWN added lines, because a sweep over the
# existing ones finds nothing: W577 ran it and all four candidates were false positives, so acting on
# them would have broken four correct assertions. The exemptions below ARE those four, plus the one that
# bit W577 for real.
_SLOT = re.compile(r"""[\"']P[1-5]\.\d+[\"']""")
#  shapes whose truth needs an item to be INCOMPLETE, or that pin an ordinal
_PIN_OPEN = re.compile(r"not\s+in\b|\bnot\s+done\b|is\s+False\b|\bblocked\b|==\s*[\"']open[\"']")
_PIN_SETEQ = re.compile(r"\}\s*==|==\s*\{")
_PIN_ORDINAL = re.compile(r"\[\s*0\s*\]")
#  a COUNT over a collection filtered to the OPEN rows — exactly what went red in W577
_PIN_OPENCOUNT = re.compile(r"len\(.*?[\"']open[\"'].*?\)\s*(>=|==|>|<=)\s*\d+")
#  EXEMPT, each one a measured false positive
_EX_ORDER = re.compile(r"\.index\(")                 # plan ORDER: closing an item does not change it
_EX_SUBSET = re.compile(r"<=")                        # a SUBSET of done, and done never reverts
_EX_PROVENANCE = re.compile(r"handed_from|delivered_by|closed_by|slot_source")   # historical, immutable
_EX_FIXTURE = re.compile(r"[\{\[]\s*[\"']id[\"']\s*:|[\"']status[\"']\s*:\s*[\"']open[\"']\s*,")


def _assert_subject(line: str) -> str:
    """The asserted EXPRESSION, without its message. A slot id in an assertion's MESSAGE is not pinned
    by the assertion — one of the four false positives was exactly that."""
    s = line.strip()
    if not s.startswith("assert "):
        return s
    s = s[len("assert "):]
    #  the message begins at the first top-level comma; track bracket depth so a comma inside a
    #  literal or a call does not end the subject early
    depth = 0
    for i, ch in enumerate(s):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            return s[:i]
    return s


def check_plan_pins(rev: str, files: list[str]) -> list[str]:
    """An ADDED assertion that pins plan state, so it goes red when the plan advances."""
    out = []
    for f in files:
        if not f.endswith(".py") or ("test_" not in Path(f).name and "integration_tests" not in f):
            continue
        added, _ = added_removed(rev, f)
        #  a preceding `len(x) == 1` makes an ordinal unambiguous — there is no tie-break to lose
        sized = {ln for ln, line in added if re.search(r"len\(\s*\w+\s*\)\s*==\s*1", line)}
        #  W578 — A FIXTURE THE TEST BUILDS ITSELF. The plan moving cannot touch a slot id the test
        #  wrote into its own input, and `_two[0]["items_advanced"] == ["P2.4", "P2.9"]` is exactly that
        #  shape in this suite. Fixture-ness is established where the variable is ASSIGNED, not on the
        #  asserting line, so it is collected over the whole added set — a single-line screen cannot see
        #  it and would push a round to rewrite a correct assertion.
        fixture_vars = set()
        for _, line in added:
            m = re.match(r"\s*(\w+)\s*=\s*.*[\[{]", line)
            if m and (_SLOT.search(line) or re.search(r"[\"']id[\"']\s*:|[\"']slot[\"']\s*:", line)):
                fixture_vars.add(m.group(1))
        for ln, line in added:
            code = line.split("#", 1)[0]
            # W578 — the line must BE an assertion, not merely contain the word. The screen's own guard
            # carries each flagged shape as a STRING in a list of examples, and `"assert" in code` read
            # those as assertions and flagged five of them: a screen cannot tell its own test data from
            # its subject unless it looks at the syntax. A real assertion starts with the keyword.
            if not code.strip().startswith("assert "):
                continue
            subject = _assert_subject(code)
            if _EX_ORDER.search(subject) or _EX_SUBSET.search(subject):
                continue
            if _EX_PROVENANCE.search(subject) or _EX_FIXTURE.search(subject):
                continue
            if any(re.search(r"\b" + re.escape(v) + r"\b", subject) for v in fixture_vars):
                continue
            why = None
            if _SLOT.search(subject):
                if _PIN_OPEN.search(subject):
                    why = ("it asserts a plan slot is ABSENT, OPEN or BLOCKED, which is true only while "
                           "that item is incomplete")
                elif _PIN_SETEQ.search(subject):
                    why = ("it compares a SET of plan slots by equality, so closing or adding one breaks "
                           "it")
                elif _PIN_ORDINAL.search(subject) and not any(abs(ln - s) <= 3 for s in sized):
                    why = ("it indexes a collection at [0] and asserts a plan slot of that element, so a "
                           "TIE-BREAK in the ordering breaks it (a preceding `len(x) == 1` would settle it)")
            if why is None and _PIN_OPENCOUNT.search(subject):
                why = ("it asserts a COUNT over rows filtered to `open`, so every row the item CLOSES "
                       "pushes it toward the bound - count over every status instead, because closing a "
                       "row does not un-move it")
            if why:
                out.append(f"{f}:{ln}  this assertion pins plan state and will go RED WHEN THE PLAN "
                           f"ADVANCES - {why}. Derive it from state, or assert the relation.")
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
                       if not h.startswith(f + ":") and reads_key(h, key)]
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


def _selfvars_by_scope(src: str, f: str) -> tuple:
    """Which locals hold THIS file's own text, per enclosing function.

    Returns (module_level, by_function) where by_function maps a function's (start, end) line range to the
    names assigned inside it. W527 — previously one set was computed over the whole file and applied to every
    added line in it, so a function reading ANOTHER file into a common name like `src` inherited the self-read
    of a different function entirely. The code carried that as a known-open limitation; this closes it.
    """
    import ast as _ast

    own = (r"(\w+)\s*=\s*\(?root\s*/\s*['\"]" + re.escape(f) + r"['\"]\)?\.read_text")

    def _names(text: str) -> set:
        found = set(re.findall(own, text))
        for _m in re.finditer(r"(\w+)\s*=\s*([^\n]*__file__[^\n]*read_text[^\n]*)", text):
            rhs = _m.group(2)
            if re.search(r"__file__.*?/\s*[\"']", rhs):
                continue                 # a path JOIN after __file__ means ANOTHER file
            # W527 — `Path(other.__file__)` is another MODULE's file. Only a BARE __file__ is this one.
            if re.search(r"[\w\]\)]\s*\.\s*__file__", rhs):
                continue
            found.add(_m.group(1))
        return found

    try:
        tree = _ast.parse(src)
    except SyntaxError:
        # a file that does not parse: fall back to the whole-file set rather than screening nothing
        return _names(src), {}

    lines = src.splitlines()
    by_func = {}
    covered = set()
    for node in tree.body:
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            start, end = node.lineno, getattr(node, "end_lineno", node.lineno)
            by_func[(start, end)] = _names(chr(10).join(lines[start - 1:end]))
            covered.update(range(start, end + 1))
    module_level = _names(chr(10).join(
        ln for i, ln in enumerate(lines, 1) if i not in covered))
    return module_level, by_func


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
        # FU-303 (W518) - a path JOIN after `__file__` means the variable holds ANOTHER file. Every
        # page-reading guard in the suite is written that way, and so is
        #     d = json.loads((Path(__file__).resolve().parents[1] / "docs/...").read_text())
        # which poisoned the name `d` FILE-WIDE: every later assertion using a local of that name was
        # reported as matching its own text. W517 reverted this fix after measuring 0 leads before and
        # after - but this check only reports ADDED lines, so it reproduces only when a round adds an
        # assertion using a poisoned name. W518 added one and it fired at once.
        #
        # STILL OPEN, registered: selfvars is computed over the WHOLE file and applied to added lines
        # anywhere in it, so two functions sharing a local name still collide. Scoping the variable to
        # its enclosing function is the complete fix.
        for _m in re.finditer(r"(\w+)\s*=\s*([^\n]*__file__[^\n]*read_text[^\n]*)", src):
            _rhs = _m.group(2)
            if re.search(r"__file__.*?/\s*[\"']", _rhs):
                continue                 # reads a DIFFERENT file, so a literal in it is a real claim
            # W527 (FU-303's class, different trigger) — `Path(ge.__file__).read_text()` reads the GENOME
            # ENGINE's file, not this one. Only a BARE __file__ names the file doing the reading, so an
            # attribute access on another object is a read of a different file. Missing this registered the
            # name `src` file-wide from one line and reported five sound assertions in a later function as
            # self-matching. A screen right about a class and wrong about its triggers teaches a reader to
            # stop reading it.
            if re.search(r"[\w\]\)]\s*\.\s*__file__", _rhs):
                continue
            selfvars.add(_m.group(1))
        # W527 — the variables are scoped to the function containing the added line. A module-level read
        # of this file is in scope everywhere, so those names stay global.
        _module_vars, _by_func = _selfvars_by_scope(src, f)
        for ln, line in added_removed(rev, f)[0]:
            m = ASSERT_IN_RE.search(line)
            _scope = set(_module_vars)
            for (_a, _b), _names_in in _by_func.items():
                if _a <= ln <= _b:
                    _scope |= _names_in
            if m and m.group("var") in _scope:
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


# ── claims ─────────────────────────────────────────────────────────────────────────────────────────
# W534 (FU-262) — the markers that turn a report into an ASSERTION. Each must co-occur with a typed digit
# in the same literal, which is what separates "0.6 is the floor" (a claim nothing checked) from
# f"the floor is {floor}" (a report of state).
_CLAIM_MARKERS = ("cannot", "can never", "never ", "always", "must not", "must be", "at least", "at most",
                  "no less", "no more", "no fewer", "below", "above", "exceed", "minimum", "maximum",
                  "guarantee", "ensures", "ensure that", "every ", "all ", "none of", "impossible")

# W534 — a STANDALONE number: not preceded by a letter, digit, dot or hyphen. That one lookbehind is what
# separates a claim from provenance, because every basis in this repository opens with a round or item id
# (W530, P3.16, FU-310) and the first version of this screen read those digits as the subject of the claim.
# 8 of its 9 flags over 25 rounds were that. A trailing unit is allowed, so 100ms still reads as a number.
_STANDALONE_NUM = re.compile(r'(?<![A-Za-z0-9_.\-])\d+(?:\.\d+)?')
_CLAIM_WINDOW = 40


def _numeric_claim(lit: str):
    """(number, marker) when a modal marker sits within _CLAIM_WINDOW characters of a standalone number.

    The window is the whole point: a modal word 300 characters from a round id is not a statement about that
    id, and treating it as one is what made the first version of this screen unusable.
    """
    low = lit.lower()
    for m in _STANDALONE_NUM.finditer(lit):
        lo = max(0, m.start() - _CLAIM_WINDOW)
        hi = min(len(lit), m.end() + _CLAIM_WINDOW)
        near = low[lo:hi]
        for marker in _CLAIM_MARKERS:
            if marker in near:
                return m.group(0), marker
    return None


def _basis_strings(tree: ast.AST):
    """Every string that is used AS A BASIS, with its line and whether any part of it is computed.

    Yields (lineno, literal_parts, is_computed). A basis is recognised three ways, because this repository
    writes them three ways: as a dict entry whose key contains 'basis', as a `basis=` keyword argument, and
    as an assignment to a name containing 'basis'.
    """
    def parts(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return [node.value], False
        if isinstance(node, ast.JoinedStr):
            lit = [v.value for v in node.values
                   if isinstance(v, ast.Constant) and isinstance(v.value, str)]
            return lit, any(isinstance(v, ast.FormattedValue) for v in node.values)
        return None, False

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if (isinstance(k, ast.Constant) and isinstance(k.value, str)
                        and "basis" in k.value.lower()):
                    lit, comp = parts(v)
                    if lit is not None:
                        yield getattr(v, "lineno", node.lineno), lit, comp
        elif isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg and "basis" in kw.arg.lower():
                    lit, comp = parts(kw.value)
                    if lit is not None:
                        yield getattr(kw.value, "lineno", node.lineno), lit, comp
        elif isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            names += [t.attr for t in node.targets if isinstance(t, ast.Attribute)]
            if any("basis" in n.lower() for n in names):
                lit, comp = parts(node.value)
                if lit is not None:
                    yield node.lineno, lit, comp


def check_claims(rev: str, files: list[str]) -> list[str]:
    """A basis that ASSERTS a numeric bound instead of REPORTING one computed from state.

    The largest group in the labelled set (30 of 98) and the one W494 found 32 times in a single round: a
    sentence beside a number, where the sentence states a universal the code never checked. A basis is the
    one place in this repository whose whole job is to say what was measured, so a basis that asserts is
    worse than silence — it answers the question a reader would otherwise ask.
    """
    out = []
    for f in files:
        if not f.endswith(".py") or "test_" in Path(f).name:
            continue
        full = ROOT / f
        if not full.exists():
            continue
        try:
            tree = ast.parse(full.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        added = {ln for ln, _ in added_removed(rev, f)[0]}
        if not added:
            continue
        for lineno, lits, computed in _basis_strings(tree):
            if lineno not in added:
                continue
            for lit in lits:
                hit = _numeric_claim(lit)
                if not hit:
                    continue
                num, marker = hit
                out.append(f"{f}:{lineno}  a basis says '{marker.strip()}' within 40 chars of the TYPED "
                           f"number {num} ({lit[:70]!r}) — is that bound computed from state, or asserted? "
                           + ("the f-string interpolates something, but this number is still a literal"
                              if computed else "nothing in this string is computed"))
    return out


# ── imports ────────────────────────────────────────────────────────────────────────────────────────
# W539 — the modules a patch-written guard reaches for without importing. Six occurrences before this
# screen existed (W527, W530, W531, W535, W536, W539): a patch script imports `ast`, the test it EMITS does
# not, and the test raises NameError on its first run. The imports belong to the writer, not the written.
_MODULE_NAMES = frozenset((
    "ast", "io", "os", "re", "json", "sys", "subprocess", "hashlib", "math", "time", "asyncio",
    "importlib", "pathlib", "shutil", "sqlite3", "random", "textwrap", "datetime", "base64", "uuid",
))


def _bound_names(node: ast.AST) -> set:
    """Every name an import or an assignment binds anywhere inside `node`."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Import):
            out |= {(a.asname or a.name.split(".")[0]) for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            out |= {(a.asname or a.name) for a in n.names}
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.For, ast.With, ast.comprehension)):
            for t in ast.walk(n):
                if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store):
                    out.add(t.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.add(n.name)
            out |= {a.arg for a in n.args.args}
    return out


def check_imports(rev: str, files: list[str]) -> list[str]:
    """A changed test function that USES a module it never imported — the patch-script import gap.

    Cheap and exact: the writer's imports are not the written file's. This screen exists because the same
    NameError was discovered by a selector run six times, and a selector run costs minutes a round."""
    out = []
    for f in files:
        if not f.endswith(".py"):
            continue
        full = ROOT / f
        if not full.exists():
            continue
        try:
            tree = ast.parse(full.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        added = {ln for ln, _ in added_removed(rev, f)[0]}
        if not added:
            continue
        module_scope = _bound_names_top(tree)
        for fn in [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            #  only functions this diff actually touched
            lines = {getattr(fn, "lineno", 0), getattr(fn, "end_lineno", 0)}
            if not any(fn.lineno <= a <= (fn.end_lineno or fn.lineno) for a in added):
                continue
            local = _bound_names(fn)
            seen = set()
            for n in ast.walk(fn):
                if (isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
                        and n.id in _MODULE_NAMES and n.id not in local and n.id not in module_scope
                        and n.id not in seen):
                    seen.add(n.id)
                    out.append(f"{f}:{n.lineno}  {fn.name}() uses `{n.id}` and neither it nor this module "
                               f"imports it — a patch script's imports are not the emitted test's, and "
                               f"this raises NameError on the first run")
    return out


def _bound_names_top(tree: ast.Module) -> set:
    """Names bound at MODULE scope only (an import inside another function does not help this one)."""
    out = set()
    for n in tree.body:
        if isinstance(n, ast.Import):
            out |= {(a.asname or a.name.split(".")[0]) for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            out |= {(a.asname or a.name) for a in n.names}
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out.add(t.id)
    return out


CHECKS = {
    # W570 (FU-348) - the label said "no surface" while the check only looked at PAGES, so a
    # CLI-surfaced key was reported under a label that was false about it. A page and a printed line
    # are both surfaces; a guard asserting a literal and a register row are not.
    "keys": ("a key produced but shown by neither a page nor a printed line", check_keys),
    "imports": ("a changed test uses a module it never imported", check_imports),
    "claims": ("a basis asserting a numeric bound instead of reporting one", check_claims),
    "renames": ("a key removed while other files still read it", check_renames),
    "routes": ("a route decorator bound to a private helper", check_routes),
    "returns": ("sibling returns with different key sets", check_returns),
    "selfmatch": ("a test assertion that matches its own text", check_selfmatch),
    "banned": ("a comment quoting a literal a guard forbids", check_banned),
    "order": ("a branch inserted ahead of an existing one", check_order),
    "planpins": ("an assertion pinned to plan state, which goes red when the plan advances",
                 check_plan_pins),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="", help="compare against this rev (default: the working tree)")
    ap.add_argument("--check", action="append", choices=sorted(CHECKS), help="run only these checks")
    args = ap.parse_args()

    files = changed_files(args.rev)
    #  W575 — DELETIONS ARE REPORTED, NOT SCREENED. Every screen here asks a question about a file's
    #  CONTENT ("is this key still read?", "is this route bound to a helper?"), and a file that is
    #  gone has no content to ask about: the keys were not renamed, the module was retired. Naming
    #  them keeps the deletion visible — the round still has to say why it removed each artefact and
    #  what established its reachability — without manufacturing a finding per common key name.
    _deleted = deleted_files(args.rev)
    if _deleted:
        print(f"  {len(_deleted)} file(s) DELETED by this diff, not screened for content — a deleted "
              f"file has none, and its keys were retired rather than renamed:")
        for _d in sorted(_deleted):
            print(f"      - {_d}")
        print("      (the round states why each was removed, and the check that established its "
              "reachability — the screens below cannot establish either)\n")
    files = [f for f in files if f not in _deleted]
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
