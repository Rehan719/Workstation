"""PRIVACY EXPOSURE - what the public repository must never hold, found by path and kind and never by value.

W732, on the Owner's word of 2026-10-14 ("put in safeguards to prevent these exposures happening again ... get
diagnosed and resolve if they do"). Two exposures were found in this public repository that day: credentials
pasted into archived text (W729) and 1,264 files of the Owner's own legal and career papers (W731). This module
is the one screen every door uses: the commit hook (`scripts/privacy_check.py --staged`), the suite's guard, the
platform's own diagnosis route, and the move that resolves a finding (`scripts/move_to_private_store.py`).

FIVE KINDS are looked for:
  credential         a key-shaped value (the W729 shapes)
  case_number        an employment-tribunal case number shape (seven digits / a year)
  personal_document  a document file (pdf, Word, image...) whose NAME says it is a personal paper
  private_folder     a file under a folder kept private on the Owner's word (W731)
  private_marker     a word or name from the Owner's PRIVATE marker list, which lives OUTSIDE the repository
                     (WORKSTATION_PRIVATE_MARKERS, default ~/.workstation/private_markers.txt) so the screen
                     never publishes what it protects

A SCREEN MAY REFUSE, NEVER CLEAR (W483). A scan that read no marker list says the marker kind was NOT CHECKED;
it never reports the tree clear of the Owner's names because it had none to look for. Findings carry the path,
the line and the kind - never the matched text.

HISTORY IS READ, NEVER REWRITTEN (W1208, FU-1864). scan() reads the files as they are now. scan_history() reads
every blob reachable from the refs once, for the credential kind only, and names the commit that introduced each
finding. It only reads. Its report says history was scanned only when the clone is not shallow and the walk
read something; on a shallow clone it names the boundary commits the walk stopped at, which is never a pass.
"""
from __future__ import annotations

import os
import pathlib
import re
import subprocess
from typing import Dict, Iterable, List, Optional, Tuple

#  each pattern is written so that it does not match its own source text
CREDENTIAL_SHAPES = [
    ("an AI provider key", re.compile(r"sk-(?:proj-|ant-)?[A-Za-z0-9_\-]{32,}")),
    ("a payment provider key", re.compile(r"(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}")),
    ("a webhook signing secret", re.compile(r"whsec_[A-Za-z0-9]{24,}")),
    ("a Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("a Google sign-in client secret", re.compile(r"GOCSPX-[A-Za-z0-9_\-]{20,}")),
    ("a database address with a password", re.compile(r"mongodb(?:\+srv)?://[^\s:/@<]+:[^\s@/<]{4,}@")),
    ("a source-host token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("a cloud access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("a private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("a service-account file", re.compile(r'"type"\s*:\s*"service_account"')),
]
#  W732 - GitHub's generic-secret detection is not offered on this repository, so the screen carries a strict
#  one: a value ASSIGNED to a password/secret/token/key name that is long, mixes cases and digits, is highly
#  random and is not an address. Measured on the tree before adding it: the loose form hit 23 test fixtures,
#  placeholders and URLs; this form hits none.
GENERIC_ASSIGN = re.compile(r"""(?i)\b(?:password|passwd|pwd|secret|client_secret|api_?key|access_?key|token|auth_?token)\b["']?\s*[:=]\s*["']([^"'\s<>${}()]{20,})["']""")


def _looks_random(v: str) -> bool:
    import math
    from collections import Counter
    if "://" in v or v.startswith(("/", "http")) or not (re.search(r"[a-z]", v) and re.search(r"[A-Z]", v) and re.search(r"\d", v)):
        return False
    c = Counter(v)
    return -sum(n / len(v) * math.log2(n / len(v)) for n in c.values()) >= 4.0


CASE_NUMBER = re.compile(r"(?<![\d/])\d{7}/20\d{2}(?![\d/])")
DOCUMENT_EXT = {".pdf", ".doc", ".docx", ".odt", ".rtf", ".pages", ".xls", ".xlsx", ".jpg", ".jpeg", ".heic", ".png", ".msg", ".eml"}
PERSONAL_NAME = re.compile(
    r"(?i)(^|[^a-z])(cv|resume|curriculum[ _-]?vitae|grievance|settlement[ _-]?agreement|payslip|p60|p45|passport|"
    r"driving[ _-]?licen[cs]e|bank[ _-]?statement|fit[ _-]?note|sick[ _-]?note|probation|dismissal|termination|"
    r"appeal[ _-]?hearing|interview[ _-]?prep|witness[ _-]?statement|contemporaneous[ _-]?log|tenancy|"
    r"medical[ _-]?record|occupational[ _-]?health)([^a-z]|$)")
#  W740 - a child's school or care paper is a personal paper too (the Owner, 2026-10-14)
CHILD_DOCUMENT = re.compile(
    r"(?i)(^|[^a-z])(sats|school[ _-]?report|report[ _-]?card|ehcp|birth[ _-]?certificate|child[ _-]?benefit|"
    r"safeguarding[ _-]?referral|pupil[ _-]?(record|profile|premium))([^a-z]|$)")
#  W731 - the folders moved to the Owner's private store; the .gitignore carries the same list
PRIVATE_FOLDERS = (
    "inputs/Law/", "inputs/Employment/", "knowledge/Employment/", "knowledge/Science/RM_CV_Science_Versions/",
    "knowledge/Law/EmploymentTribunal/evidence/", "products/Law/VSB-SIG-LAW-OMNIOCTO-19.0/",
    "products/Employment/VSB-SIG-EMP-PENTA-3.0/", "products/Science/VSB-SIG-SCI-OMNIA-18.0/",
    "_archive/outputs/Law/", "_archive/outputs/Employment/", "_archive/outputs/Science/PatientSafety/",
    "_archive/outputs/interview_prep/", "_archive/scripts/Law/", "_archive/scripts/Employment/",
    "_archive/scripts/Science/PatientSafety/", "_archive/docs/Law/", "_archive/ingest/Employment/",
    "_archive/legacy-archive/Employment/", "_archive/agentic_core/domains/law/", "_archive/legacy-archive/law-grand-operation",
    # W740 - the Owner's child's school material, moved to the Owner's private Education folder
    "_archive/outputs/education/sats_2026/", "outputs/education/sats_2026/",
    "_archive/agentic_core/identity/sats_persona.py")
KINDS = ("credential", "case_number", "personal_document", "private_folder", "private_marker")
MAX_BYTES = 32_000_000          # a larger file is LISTED as not read, never skipped silently


def marker_file() -> pathlib.Path:
    return pathlib.Path(os.environ.get("WORKSTATION_PRIVATE_MARKERS")
                        or (pathlib.Path.home() / ".workstation" / "private_markers.txt"))


def load_markers(path: Optional[pathlib.Path] = None) -> Optional[List[str]]:
    """The Owner's private markers, or None when there is no list to read (then that kind is NOT CHECKED).
    One marker per line; blank lines and lines starting with # are skipped; a marker shorter than 4
    characters is refused as too likely to match ordinary words."""
    p = path or marker_file()
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    return [s.strip() for s in lines if s.strip() and not s.strip().startswith("#") and len(s.strip()) >= 4]


def load_allowed(root: pathlib.Path) -> List[Tuple[str, str]]:
    """Allowed false positives, by EXACT path and kind, each with a reason (config/privacy_allow.json). An entry
    without a reason is not honoured: an allowance nobody can explain is a hole."""
    import json
    try:
        rows = json.loads((root / "config" / "privacy_allow.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [(r["path"], r["kind"]) for r in rows
            if isinstance(r, dict) and r.get("path") and r.get("kind") in KINDS and str(r.get("reason") or "").strip()]


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def scan_one(rel: str, data: bytes, markers: Optional[List[str]] = None,
             allowed: Iterable[Tuple[str, str]] = ()) -> List[Dict]:
    """Findings for ONE file: [{path, kind, line, what}] - `what` names the shape, never the matched text."""
    allow = set(allowed)
    out: List[Dict] = []
    rel = rel.replace("\\", "/")
    name = rel.rsplit("/", 1)[-1]
    if rel.startswith(PRIVATE_FOLDERS):
        out.append({"path": rel, "kind": "private_folder", "line": None, "what": "a file under a folder kept private"})
    if pathlib.PurePosixPath(rel).suffix.lower() in DOCUMENT_EXT and PERSONAL_NAME.search(name):
        out.append({"path": rel, "kind": "personal_document", "line": None,
                    "what": "a document whose name says it is a personal paper"})
    elif pathlib.PurePosixPath(rel).suffix.lower() in DOCUMENT_EXT and CHILD_DOCUMENT.search(name):
        out.append({"path": rel, "kind": "personal_document", "line": None,
                    "what": "a document whose name says it is a child's school or care paper"})
    text = data[:MAX_BYTES].decode("utf-8", "ignore")
    for what, rx in CREDENTIAL_SHAPES:
        for m in rx.finditer(text):
            out.append({"path": rel, "kind": "credential", "line": _line(text, m.start()), "what": what})
    for m in GENERIC_ASSIGN.finditer(text):
        if _looks_random(m.group(1)):
            out.append({"path": rel, "kind": "credential", "line": _line(text, m.start()),
                        "what": "a random-looking value assigned to a secret's name"})
    for m in CASE_NUMBER.finditer(text):
        out.append({"path": rel, "kind": "case_number", "line": _line(text, m.start()),
                    "what": "a tribunal case number shape"})
    for i, mk in enumerate(markers or []):
        low = mk.lower()
        if low in name.lower():
            out.append({"path": rel, "kind": "private_marker", "line": None, "what": f"private marker #{i + 1} in the file name"})
        pos = text.lower().find(low)
        if pos >= 0:
            out.append({"path": rel, "kind": "private_marker", "line": _line(text, pos), "what": f"private marker #{i + 1}"})
    return [f for f in out if (f["path"], f["kind"]) not in allow]


def tracked(root: pathlib.Path) -> List[str]:
    r = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("the tracked files could not be listed, so nothing was scanned")
    return [x for x in r.stdout.decode("utf-8", "replace").split("\0") if x]


def staged(root: pathlib.Path) -> List[Tuple[str, bytes]]:
    """The files a commit is about to record, with the STAGED content (what would be committed)."""
    r = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR"],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("the staged files could not be listed, so nothing was scanned")
    out = []
    for rel in [x for x in r.stdout.decode("utf-8", "replace").split("\0") if x]:
        b = subprocess.run(["git", "-C", str(root), "show", f":{rel}"], capture_output=True)
        out.append((rel, b.stdout if b.returncode == 0 else b""))
    return out


def scan(root: pathlib.Path, files: Optional[List[Tuple[str, bytes]]] = None,
         markers: Optional[List[str]] = None, allowed: Iterable[Tuple[str, str]] = ()) -> Dict:
    """Scan the given (path, bytes) pairs, or every tracked file. The report says what was checked and what was
    NOT, so a clean result is never more than its coverage."""
    allowed = list(allowed)
    whole_tree = files is None
    not_read: List[str] = []
    if files is None:
        files = []
        for rel in tracked(root):
            p = root / rel
            try:
                if p.is_file() and p.stat().st_size > MAX_BYTES:
                    not_read.append(rel)
                files.append((rel, p.read_bytes()[:MAX_BYTES] if p.is_file() else b""))
            except OSError:
                not_read.append(rel)
                files.append((rel, b""))
    findings: List[Dict] = []
    for rel, data in files:
        findings += scan_one(rel, data, markers, allowed)
    checked = [k for k in KINDS if k != "private_marker" or markers]
    return {
        "files_read": len(files),
        "checked": checked,
        "not_checked": [] if markers else ["private_marker"],
        "not_checked_basis": ("" if markers else
                              f"no private marker list was read ({marker_file()}), so the Owner's own names and "
                              "markers were NOT looked for - this is not a finding that none are present"),
        #  W732 - WHAT THIS REPORT IS ABOUT. It reads files as they are now. A file removed from the tree is still
        #  in the repository's history, which this scan does not read (scan_history does, W1208), so the report
        #  says so: a zero is never more than its coverage (a screen may refuse, never clear).
        "scope": ("every file tracked in the working tree, as it is now" if whole_tree
                  else "only the files handed to the scan (the commit hook hands it the staged content)"),
        "history_scanned": False,
        "history_basis": ("git history was NOT scanned: a file removed from the tree in an earlier round is still "
                          "in earlier commits, so this report is about the current files only; rewriting history "
                          "is the Owner's decision"),
        "markers_read": len(markers or []),
        "not_read_in_full": not_read,
        "findings": findings,
        "count": len(findings),
        "by_kind": {k: sum(1 for f in findings if f["kind"] == k) for k in KINDS},
        "basis": (f"{len(findings)} finding(s) over {len(files)} file(s); each is reported by path, line and kind, "
                  "never by the matched text"),
    }


#  W1208 (FU-1864, P4.5) - THE HISTORY MODE. scan() reads the files as they are now; a credential removed from the
#  tree in an earlier round is still in earlier commits. scan_history() reads them, and only reads: it runs git
#  rev-parse, config, rev-list, cat-file and log, and changes no commit, ref, object or file. Rewriting history is the
#  Owner's decision (OWNER RULING 2026-10-14) and is never done here; a read is not a rewrite. Revoking a credential
#  it finds is the Owner's, at the provider (runbook step 3; the values W729 redacted are FU-1837's).
HISTORY_ALLOW = "config/privacy_history_allow.json"
HISTORY_KINDS = ("credential",)
_COMMIT_ID = re.compile(r"[0-9a-f]{7,64}")
_OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_REF_SETS = ("--all", "--branches", "--tags", "--remotes")
#  every blob is read whole, in windows that overlap by more than the longest shape the screen looks for
HISTORY_WINDOW = 1 << 20
HISTORY_OVERLAP = 8192
HISTORY_TIMEOUT = 3600          # seconds for any one git command; one that runs longer is said as not completed
#  no prompt for a password, no fetch of a missing object, and no replace ref standing in for a commit
_GIT_ENV = {"GIT_TERMINAL_PROMPT": "0", "GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1"}
HISTORY_READ_ONLY = ("this mode only reads: it runs git rev-parse, config, rev-list, cat-file and log, with no "
                     "lazy fetch, no replace refs and no prompt, and changes no commit, ref, object or file; history "
                     "is never rewritten here, which is the Owner's decision")


def load_history_allowed(root: pathlib.Path) -> List[Tuple[str, str, str, int]]:
    """Allowed history findings, by (commit, path, kind, line), each with a reason, from
    config/privacy_history_allow.json (its "allowed" list; the file's "about" says the format). The commit is the one
    a finding names (a full id or an abbreviation of at least seven hex digits) and the path the one it names there.
    Each entry allows that one finding only. An entry without a reason or a line is not honoured. load_allowed never
    reads this file, so an allowance here clears nothing in the tree, and one in config/privacy_allow.json clears
    nothing in history."""
    import json
    try:
        doc = json.loads((root / HISTORY_ALLOW).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    rows = doc.get("allowed") if isinstance(doc, dict) else doc
    out: List[Tuple[str, str, str, int]] = []
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict):
            continue
        commit = str(r.get("commit") or "").strip().lower()
        line = r.get("line")
        if (_COMMIT_ID.fullmatch(commit) and r.get("path") and r.get("kind") in KINDS
                and isinstance(line, int) and not isinstance(line, bool) and line >= 1
                and str(r.get("reason") or "").strip()):
            out.append((commit, str(r["path"]), str(r["kind"]), line))
    return out


def _git_env() -> Dict[str, str]:
    return dict(os.environ, **_GIT_ENV)


def _git_read(root: pathlib.Path, *args: str, data: Optional[bytes] = None) -> subprocess.CompletedProcess:
    """One read-only git command in ROOT; no optional lock is taken, and any failure to run is a RuntimeError."""
    try:
        return subprocess.run(["git", "--no-optional-locks", "--no-replace-objects", "-C", str(root), *args],
                              capture_output=True, input=data, stdin=None if data is not None else subprocess.DEVNULL,
                              env=_git_env(), timeout=HISTORY_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"git {args[0]} ran longer than {HISTORY_TIMEOUT} seconds, so the walk did not complete")
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"git could not be run ({type(exc).__name__}), so no history was read")


def _scan_blob(path: str, stream, size: int) -> List[Tuple[int, str]]:
    """(line, what) for each credential in one blob of SIZE bytes read from STREAM, read whole in windows of
    HISTORY_WINDOW bytes that overlap by HISTORY_OVERLAP, so a value across a window's edge is still found."""
    hits = set()
    tail, nl_seen, left = b"", 0, size
    while True:
        chunk = stream.read(min(left, HISTORY_WINDOW)) if left else b""
        if left and not chunk:
            raise RuntimeError("git stopped while reading a blob, so the walk did not complete")
        left -= len(chunk)
        window = tail + chunk
        before = nl_seen - tail.count(b"\n")
        for f in scan_one(path, window):
            if f["kind"] in HISTORY_KINDS:
                hits.add((before + f["line"], f["what"]))
        nl_seen += chunk.count(b"\n")
        tail = window[-HISTORY_OVERLAP:] if HISTORY_OVERLAP else b""
        if not left:
            return sorted(hits)


def _blobs_scanned(root: pathlib.Path, blobs: List[str]):
    """Each distinct blob once, through one `git cat-file --batch`: (blob, [(line, what)])."""
    try:
        proc = subprocess.Popen(["git", "--no-optional-locks", "--no-replace-objects", "-C", str(root), "cat-file",
                                 "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL, env=_git_env())
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"git could not be run ({type(exc).__name__}), so no history was read")
    try:
        for sha in blobs:
            proc.stdin.write(sha.encode("ascii") + b"\n")
            proc.stdin.flush()
            head = proc.stdout.readline().split()
            if len(head) != 3 or head[1] != b"blob" or head[0] != sha.encode("ascii"):
                raise RuntimeError(f"git could not read blob {sha[:12]}, so the walk did not complete")
            hits = _scan_blob("", proc.stdout, int(head[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"git's reading of blob {sha[:12]} ended out of step, so the walk did not complete")
            yield sha, hits
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"git's reading of the blobs failed ({type(exc).__name__}), so the walk did not complete")
    finally:
        for pipe in (proc.stdin, proc.stdout):
            try:
                pipe.close()
            except OSError:
                pass
        proc.wait()


def _attributed(root: pathlib.Path, ref_args: List[str], targets) -> Dict[str, Dict]:
    """For each blob in TARGETS: the first commit, oldest first by ancestry, whose change adds it at any path (the
    commit that introduced it, a rename or copy counted where the value first came in), the path it has there, and
    every path it is ever added at. One `git log --raw -z` pass over the walk, read NUL by NUL, so a path is never
    split or quoted."""
    want = set(targets)
    out: Dict[str, Dict] = {}
    if not want:
        return out
    lg = _git_read(root, "log", *ref_args, "--topo-order", "--reverse", "-m", "--no-renames", "--raw",
                   "--no-abbrev", "-z", "--format=COMMIT %H", "--")
    if lg.returncode != 0:
        raise RuntimeError("git could not list the history's changes, so the findings could not be dated")
    commit, meta = None, None
    for tok in lg.stdout.split(b"\0"):
        if meta is not None:        # a path always follows its change line, whatever it holds
            new, status = meta
            if status in (b"A", b"M", b"T") and new in want:
                path = tok.decode("utf-8", "surrogateescape")
                row = out.setdefault(new, {"commit": commit, "path": path, "paths": []})
                if path not in row["paths"]:
                    row["paths"].append(path)
            meta = None
            continue
        tok = tok.lstrip(b"\n")
        if tok.startswith(b"COMMIT "):
            commit = tok[7:].decode("ascii", "replace")
        elif tok.startswith(b":"):
            part = tok.split()
            meta = (part[3].decode("ascii", "replace"), part[4][:1]) if len(part) >= 5 else (None, b"")
    return out


def _config_set(root: pathlib.Path, *args: str) -> bool:
    r = _git_read(root, "config", *args)
    return r.returncode == 0 and bool(r.stdout.strip())


def scan_history(root: pathlib.Path, refs="--all", allowed: Iterable[Tuple[str, str, str, int]] = ()) -> Dict:
    """Read every blob reachable from REFS (default every local ref) ONCE and WHOLE, for the credential kind only.
    Each finding names the commit that introduced the blob, the path it has there, every path it is added at, the
    kind and the line - never the matched text. history_scanned is True only when the walk read at least one commit
    and one blob and is whole: not a shallow clone, no grafts file, no single-branch fetch. Otherwise it stays False
    and the report says why, naming the boundary commits of a shallow clone. A partial clone is refused, since
    reading it would fetch. Allowances are by (commit, path, kind, line) with a reason (load_history_allowed), each
    for one finding. Raises RuntimeError when git cannot read the repository or the walk does not complete."""
    ref_args = [refs] if isinstance(refs, str) else list(refs)
    for a in ref_args:
        if not a or (a.startswith("-") and a not in _REF_SETS):
            raise RuntimeError(f"{a!r} is not a set of refs the history mode walks, so nothing was read")
    allow = [(c.lower(), p, k, n) for c, p, k, n in allowed]
    top = _git_read(root, "rev-parse", "--is-shallow-repository")
    if top.returncode != 0:
        raise RuntimeError("git could not read this repository, so no history was read")
    #  a partial clone fetches each blob it lacks when it is read: refused, so the mode never writes or calls out
    pack = _git_read(root, "rev-parse", "--git-path", "objects/pack")
    pdir = pathlib.Path(pack.stdout.decode("utf-8", "replace").strip())
    pdir = pdir if pdir.is_absolute() else root / pdir
    if (_config_set(root, "--get", "extensions.partialclone")
            or _config_set(root, "--get-regexp", r"^remote\..*\.promisor$")
            or (pdir.is_dir() and any(p.suffix == ".promisor" for p in pdir.iterdir()))):
        raise RuntimeError("this is a partial clone: blobs it does not hold would be fetched when read, so no history "
                           "was read; make a full clone, or a mirror clone, and run it there")
    shallow = top.stdout.decode("utf-8", "replace").strip() == "true"

    def git_path(name):
        p = pathlib.Path(_git_read(root, "rev-parse", "--git-path", name).stdout.decode("utf-8", "replace").strip())
        return p if p.is_absolute() else root / p
    boundary: List[str] = []
    if shallow:
        try:
            boundary = sorted(x.strip() for x in git_path("shallow").read_text(encoding="utf-8").splitlines()
                              if x.strip())
        except OSError:
            raise RuntimeError("this clone is shallow and its boundary could not be read, so no history was read")
    grafted = git_path("info/grafts").is_file()
    fetch = _git_read(root, "config", "--get-regexp", r"^remote\..*\.fetch$").stdout.decode("utf-8", "replace")
    single = sorted({ln.split(None, 1)[0].split(".")[1] for ln in fetch.splitlines()
                     if ln.strip() and "*" not in ln and ln.count(".") >= 2})
    replaced = _git_read(root, "for-each-ref", "--format=%(refname)", "refs/replace/").stdout.split()
    commits = _git_read(root, "rev-list", *ref_args, "--")
    objects = _git_read(root, "rev-list", "--objects", "--no-object-names", *ref_args, "--")
    if commits.returncode != 0 or objects.returncode != 0:
        raise RuntimeError(f"git could not walk {' '.join(ref_args)}, so no history was read")
    n_commits = len([x for x in commits.stdout.split(b"\n") if x.strip()])
    kinds = _git_read(root, "cat-file", "--batch-check=%(objectname) %(objecttype)", data=objects.stdout)
    if kinds.returncode != 0:
        raise RuntimeError("git could not list the objects it walked, so no history was read")
    blobs: List[str] = []
    for ln in kinds.stdout.decode("ascii", "replace").split("\n"):
        part = ln.split()
        if len(part) == 2 and part[1] == "blob" and _OBJECT_ID.fullmatch(part[0]):
            blobs.append(part[0])
    hits: List[Tuple[str, int, str]] = []
    n_read = 0
    for sha, found in _blobs_scanned(root, blobs):
        n_read += 1
        hits += [(sha, line, what) for line, what in found]
    where = _attributed(root, ref_args, {sha for sha, _l, _w in hits})
    findings: List[Dict] = []
    suppressed = 0
    used = set()
    for sha, line, what in hits:
        at = where.get(sha) or {"commit": None, "path": "", "paths": []}
        commit = at["commit"]
        found = {"commit": commit, "path": at["path"], "paths": at["paths"], "kind": "credential", "line": line,
                 "what": what, "blob": sha, "at_boundary": bool(commit and commit in boundary)}
        match = [e for e in allow if e not in used and commit and commit.startswith(e[0]) and e[1] == found["path"]
                 and e[2] == found["kind"] and e[3] == line]
        if match:
            used.add(match[0])
            suppressed += 1
            continue
        findings.append(found)
    walked = n_commits > 0 and n_read > 0
    said = " ".join(ref_args)
    why_partial = ([f"this clone is shallow, so the walk stopped at {len(boundary)} boundary commit(s) "
                    f"({', '.join(b[:12] for b in boundary)})"] if shallow else [])
    why_partial += (["a grafts file (info/grafts) cuts commits off from their parents, so the walk did not reach "
                     "them"] if grafted else [])
    why_partial += ([f"{len(single)} remote(s) fetch one branch only ({', '.join(single)}), so other branches were "
                     "not fetched"] if single else [])
    scope = ("the refs this clone holds; a commit only on the host, such as a pull request's head or one orphaned "
             "there, is not read: a mirror clone fetches the host's pull request heads, and an orphaned commit is the "
             "host's own secret scanning's")
    if not walked:
        basis = (f"git history was NOT scanned: the walk of {said} found {n_commits} commit(s) and {n_read} file(s) to "
                 "read, so it examined nothing")
    elif why_partial:
        basis = (f"git history was NOT scanned in full: {'; '.join(why_partial)}, after {n_commits} commit(s) and "
                 f"{n_read} distinct blob(s); what lies beyond was not read, so this is a partial reading and never a "
                 f"pass, and the full walk is for a full clone. It covers {scope}")
    else:
        basis = (f"git history was scanned for credentials: every blob reachable from {said} was read once and whole "
                 f"({n_commits} commit(s), {n_read} distinct blob(s)); the other kinds are read in the tree only. It "
                 f"covers {scope}")
    return {
        "refs": ref_args,
        "shallow": shallow,
        "boundary_commits": boundary,
        "grafted": grafted,
        "single_branch_remotes": single,
        "replace_refs_ignored": len(replaced),
        "commits_walked": n_commits,
        "blobs_read": n_read,
        "checked": list(HISTORY_KINDS),
        "not_checked": [k for k in KINDS if k not in HISTORY_KINDS],
        "scope": f"every blob reachable from {said}, each read once and whole, for the credential kind only; {scope}",
        "history_scanned": walked and not why_partial,
        "history_basis": basis,
        "read_only": HISTORY_READ_ONLY,
        "findings": findings,
        "count": len(findings),
        "allowed_count": suppressed,
        "basis": (f"{len(findings)} finding(s) over {n_read} blob(s); each is reported by commit, path, line and kind, "
                  "never by the matched text"),
    }


RUNBOOK = "docs/PRIVACY_EXPOSURE_RUNBOOK.md"
