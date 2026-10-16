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
    # W740 - the Owner's child's school material, moved to his private Education folder
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
        "markers_read": len(markers or []),
        "not_read_in_full": not_read,
        "findings": findings,
        "count": len(findings),
        "by_kind": {k: sum(1 for f in findings if f["kind"] == k) for k in KINDS},
        "basis": (f"{len(findings)} finding(s) over {len(files)} file(s); each is reported by path, line and kind, "
                  "never by the matched text"),
    }


RUNBOOK = "docs/PRIVACY_EXPOSURE_RUNBOOK.md"
