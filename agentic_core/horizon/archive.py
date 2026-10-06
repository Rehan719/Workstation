"""The asset index over an EXPLICIT INBOX — three-state per file, with its own bounds stated (P2.13).

TWO OWNER RULINGS SHAPE THIS AND BOTH NARROW IT.

  FU-268 — AN EXPLICIT INBOX ONLY. The brief wanted four of the Owner's own folders scanned. They are
  not scanned. This indexes one directory the Owner puts files INTO, so indexing is something they do
  rather than something that happens to them. Measured on 2026-09-27, two of those four folders held
  nothing this platform could read anyway, and the brief's ingestor would have reported ASSIMILATED over
  them regardless — which is the defect this module is built against.

  FU-269 — BOTH EXTRACTORS INTO REQUIREMENTS. python-docx was declared and pypdf was not, so the ruling
  was half-executed until W552 added it. NEITHER IS INSTALLED IN THIS DEPLOYMENT, so the honest state for
  a .docx or .pdf file here is NOT_READ with the missing extractor NAMED. The item's own words: "until it
  lands NOT_EXTRACTED remains the honest answer for a file this platform cannot read. It must never be
  replaced by an optimistic one."

THREE STATES PER FILE, AND NO FOURTH:
  INDEXED   the text was read and is in the lexical index.
  NOT_READ  no extractor for this extension in this deployment, NAMED. The file is listed and its text
            is not in the index — nothing unread enters the knowledge base (the FU-124 rule).
  EXCLUDED  a rule excluded it, and THE RULE IS RECORDED. An exclusion nobody can see looks exactly like
            a file that was never there, which is why every exclusion is listed with the rule that made
            it.

SECRETS ARE EXCLUDED BY RULE, BEFORE ANYTHING IS READ — not filtered out of the text afterwards. The
order matters: a rule applied after reading has already loaded the secret into memory and into whatever
the reader did next.

SEARCH IS THIS PLATFORM'S OWN LEXICAL INDEX. There is no embedding backend installed and the surface says
so, because "search" over a token index is a different promise from semantic recall, and a user who
expects the second from a surface offering the first will conclude their file was not indexed.

THE INDEX IS LOCAL DATA: it lives under the data directory, it is never committed, and nothing in this
module sends it anywhere.
"""
from __future__ import annotations

import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

INDEXED = "INDEXED"
NOT_READ = "NOT_READ"
EXCLUDED = "EXCLUDED"

#  THE BOUNDS, STATED. A scan that does not publish its own limits invites a reader to treat its
#  manifest as the whole of what exists.
MAX_FILES = 2000
#  P3.22 — the passage cap. Per-line tokens over MAX_FILES documents of MAX_BYTES each will not sit in a
#  JSON store, so a document contributes at most this many located passages. IT IS PUBLISHED in `bounds`
#  with its own sentence: a cap nobody is told about is a silent top-N, and a retrieval that quietly stops
#  at a line answers a question about a document nobody has.
MAX_PASSAGES_PER_FILE = 400
MAX_BYTES = 2 * 1024 * 1024          # 2 MiB per file
BOUNDS_BASIS = (f"at most {MAX_FILES} files are listed and at most {MAX_BYTES} bytes are read from any "
                f"one of them. A file beyond the size cap is listed as NOT_READ with the cap named, not "
                f"silently truncated, because a half-read file in a search index answers questions about "
                f"a document nobody has")

#  Excluded BY RULE and BY NAME, before any byte is read. Each pattern is paired with the rule text that
#  is recorded against every file it excludes.
_SECRET_RULES: Tuple[Tuple[str, str], ...] = (
    (r"(?:^|[/\\])\.env(?:\.|$)", "a .env file holds configuration secrets"),
    (r"(?:^|[/\\])\.env$", "a .env file holds configuration secrets"),
    (r"key", "the name contains 'key'"),
    (r"secret", "the name contains 'secret'"),
    (r"^credentials", "the name begins 'credentials'"),
    (r"^id_rsa", "the name begins 'id_rsa' (a private key)"),
    (r"\.pem$", "a .pem file is a certificate or private key"),
)

#  Extensions this deployment can read as text with no extractor at all.
_TEXT_EXT = (".txt", ".md", ".json", ".csv", ".yaml", ".yml", ".log", ".ini", ".cfg", ".tsv")

#  Extensions that NEED an extractor, with the package that provides it. Reported as NOT_READ naming the
#  package when it is absent — never as an empty document, and never as indexed.
_NEEDS_EXTRACTOR = {".pdf": "pypdf", ".docx": "python-docx", ".pptx": "python-pptx"}


def _inbox() -> str:
    return str(data_path("horizon/inbox"))


def _store():
    return data_path("horizon/asset_index.json")


def _read_index() -> Dict[str, Any]:
    return read_json_strict(_store(), missing={"files": [], "tokens": {}}, expect=dict)


def extractor_available(package: str) -> bool:
    """Whether the extractor is importable HERE. Declared in requirements is not installed."""
    import importlib.util
    _mod = {"python-docx": "docx", "python-pptx": "pptx", "pypdf": "pypdf"}.get(package, package)
    return importlib.util.find_spec(_mod) is not None


def _excluded_by(name: str, rel: str) -> Optional[str]:
    """The RULE that excludes this file, or None. Checked on the name before anything is read."""
    low = name.lower()
    for pat, rule in _SECRET_RULES:
        if re.search(pat, low) or re.search(pat, rel.lower().replace(os.sep, "/")):
            return rule
    return None


def _tokens(text: str) -> List[str]:
    """The platform's own lexical tokens. No embedding, no stemming, no synonyms."""
    return sorted({t for t in re.findall(r"[a-z0-9_]{3,}", text.lower())})


def _passages(text: str) -> List[Dict[str, Any]]:
    """Split a document into LOCATED passages — one per non-empty line, numbered from 1.

    P3.22 clause (1): "a passage without a resolvable location cannot be cited." A line number is the
    location that can actually be resolved: a reader opens the file, goes to the line and sees the text, and
    the verifier's check_quote_at_location does exactly that mechanically. A paragraph index or a character
    offset would not survive a reader checking it by hand, and P3.23's clause asks for "the document and
    LINE it came from" in as many words.

    BLANK LINES ARE SKIPPED AND THE NUMBERING STILL COUNTS THEM, so line 42 here is line 42 in the file.
    Getting that wrong would produce citations that resolve to the WRONG TEXT, which is worse than no
    citation at all — a precise-looking reference to something the document does not say.
    """
    out: List[Dict[str, Any]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if len(out) >= MAX_PASSAGES_PER_FILE:
            break
        out.append({"line": i, "text": line[:400], "tokens": _tokens(line)})
    return out


def scan() -> Dict[str, Any]:
    """Index the inbox. Every file gets exactly one of the three states, and the counts are published."""
    inbox = _inbox()
    os.makedirs(inbox, exist_ok=True)
    files: List[Dict[str, Any]] = []
    tokens: Dict[str, List[str]] = {}
    passages: Dict[str, List[Dict[str, Any]]] = {}      # P3.22 — located passages, per file
    _capped = False

    for root, _dirs, names in os.walk(inbox):
        for name in sorted(names):
            if len(files) >= MAX_FILES:
                _capped = True
                break
            full = os.path.join(root, name)
            rel = os.path.relpath(full, inbox).replace(os.sep, "/")
            ext = os.path.splitext(name)[1].lower()

            #  EXCLUSION FIRST, BEFORE ANY READ. A rule applied after reading has already loaded the
            #  secret, and nothing downstream can undo that.
            rule = _excluded_by(name, rel)
            if rule:
                files.append({"path": rel, "state": EXCLUDED, "rule": rule, "ext": ext,
                              "basis": (f"EXCLUDED by rule: {rule}. The file is LISTED so the exclusion "
                                        f"is visible — an exclusion nobody can see looks exactly like a "
                                        f"file that was never there — and its content was never read")})
                continue

            try:
                size = os.path.getsize(full)
            except OSError as e:
                files.append({"path": rel, "state": NOT_READ, "ext": ext,
                              "basis": f"NOT_READ: the file could not be sized ({e.__class__.__name__})"})
                continue

            if size > MAX_BYTES:
                files.append({"path": rel, "state": NOT_READ, "ext": ext, "bytes": size,
                              "basis": (f"NOT_READ: {size} bytes exceeds the {MAX_BYTES}-byte cap. It is "
                                        f"listed rather than truncated, because a half-read file in a "
                                        f"search index answers questions about a document nobody has")})
                continue

            if ext in _NEEDS_EXTRACTOR:
                pkg = _NEEDS_EXTRACTOR[ext]
                if not extractor_available(pkg):
                    files.append({"path": rel, "state": NOT_READ, "ext": ext, "needs": pkg,
                                  "basis": (f"NOT_READ: no extractor for {ext} in this deployment — "
                                            f"{pkg} is not installed. The file is listed and its text is "
                                            f"NOT in the index, so nothing unread is in the knowledge "
                                            f"base")})
                    continue
                #  The extractor exists. Reading it is the work of the round that installs it; until
                #  then this branch is unreachable here and says so rather than pretending to read.
                files.append({"path": rel, "state": NOT_READ, "ext": ext, "needs": pkg,
                              "basis": (f"NOT_READ: {pkg} is installed but this module does not yet call "
                                        f"it. Reporting INDEXED here would claim a read that did not "
                                        f"happen")})
                continue

            if ext not in _TEXT_EXT:
                files.append({"path": rel, "state": NOT_READ, "ext": ext,
                              "basis": (f"NOT_READ: {ext or '(no extension)'} is not a format this "
                                        f"deployment reads as text and no extractor is named for it")})
                continue

            try:
                with open(full, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read(MAX_BYTES)
            except OSError as e:
                files.append({"path": rel, "state": NOT_READ, "ext": ext,
                              "basis": f"NOT_READ: the file could not be opened ({e.__class__.__name__})"})
                continue

            tokens[rel] = _tokens(text)
            #  P3.22 — LOCATED passages beside the file-level token set. `tokens[rel]` is left exactly as
            #  it was: `files[].tokens` counts it and readers depend on that count.
            passages[rel] = _passages(text)
            _capped_p = len(passages[rel]) >= MAX_PASSAGES_PER_FILE
            files.append({"path": rel, "state": INDEXED, "ext": ext, "bytes": size,
                          "tokens": len(tokens[rel]),
                          "passages": len(passages[rel]),
                          "passages_capped": _capped_p,
                          "basis": (f"INDEXED: read as UTF-8 text and reduced to {len(tokens[rel])} "
                                    f"lexical token(s) and {len(passages[rel])} located passage(s), each "
                                    f"carrying its line number so a claim can be traced to a place in the "
                                    f"document and not merely to the document. No embedding was computed"
                                    + (f". ONLY THE FIRST {MAX_PASSAGES_PER_FILE} passages were indexed - "
                                       f"later lines of this file are NOT searchable, which is a cap and "
                                       f"not an absence of content" if _capped_p else ""))})
        if _capped:
            break

    counts = {s: sum(1 for f in files if f["state"] == s) for s in (INDEXED, NOT_READ, EXCLUDED)}
    manifest = {
        "scanned_at": time.time(),
        "inbox": inbox,
        "files": files,
        "counts": counts,
        "total": len(files),
        "file_cap_reached": _capped,
        "bounds": {"max_files": MAX_FILES, "max_bytes": MAX_BYTES,
                   "max_passages_per_file": MAX_PASSAGES_PER_FILE,
                   "passage_basis": (f"a document contributes at most {MAX_PASSAGES_PER_FILE} located "
                                     f"passages; a file longer than that is indexed to that line and the "
                                     f"file's own entry says so, because a cap nobody is told about reads "
                                     f"as a complete index"),
                   "exclusion_rules": [r for _, r in _SECRET_RULES],
                   "text_extensions": list(_TEXT_EXT),
                   "extractor_extensions": dict(_NEEDS_EXTRACTOR),
                   "basis": BOUNDS_BASIS},
        "extractors": {pkg: extractor_available(pkg) for pkg in sorted(set(_NEEDS_EXTRACTOR.values()))},
        "embedding_backend": None,
        "search_basis": ("search is this platform's OWN LEXICAL index — exact token matching, no "
                         "embedding, no stemming and no synonyms. There is no embedding backend "
                         "installed, so this is not semantic recall and must not be read as it"),
        "counts_basis": (f"{counts[INDEXED]} indexed, {counts[NOT_READ]} not read, {counts[EXCLUDED]} "
                         f"excluded, {len(files)} listed in total. Every listed file carries exactly one "
                         f"state and the three counts sum to the total — a file in no state would be a "
                         f"file this manifest had lost"),
        "locality_basis": ("this index is LOCAL DATA under the data directory. It is never committed and "
                           "nothing in this module sends it anywhere"),
    }
    with store_lock(_store()):
        atomic_write_json(_store(), {"manifest": manifest, "tokens": tokens, "passages": passages})
    return manifest


def recount() -> Dict[str, Any]:
    """Re-count the stored manifest from its own file list, so the published counts can be CHECKED.

    The bar's words are "the manifest's counts match a re-count". A count written beside the thing it
    counts is a claim; a count derived again from the list is a check.
    """
    data = _read_index()
    man = data.get("manifest") or {}
    files = man.get("files") or []
    fresh = {s: sum(1 for f in files if f.get("state") == s) for s in (INDEXED, NOT_READ, EXCLUDED)}
    stated = man.get("counts") or {}
    agrees = all(fresh.get(k) == stated.get(k) for k in fresh) and len(files) == man.get("total")
    return {"stated": stated, "recounted": fresh, "total_stated": man.get("total"),
            "total_recounted": len(files), "agrees": agrees,
            "basis": ("the published counts were derived again from the file list and agree"
                      if agrees else
                      "THE PUBLISHED COUNTS DISAGREE with a re-count of the same list, so at least one "
                      "file is in a state the counts do not reflect")}


def search(term: str, limit: int = 20) -> Dict[str, Any]:
    """Exact lexical match over the indexed files only. An unread file cannot match."""
    data = _read_index()
    man = data.get("manifest") or {}
    toks = data.get("tokens") or {}
    needle = (term or "").strip().lower()
    #  P3.22 — THE CAP IS REPORTED. This was `[...][:limit]` with nothing saying so, so a caller seeing
    #  twenty hits could not tell whether there were two hundred: `searched_files` counts indexed FILES,
    #  not matches. Same defect class as a basis sentence denying the truncation its own code applies.
    _all_hits = [p for p, ts in sorted(toks.items()) if needle and needle in ts]
    hits = _all_hits[:limit]
    #  P3.22 clause (1) — LOCATED passages, ADDED beside `hits`. `hits` keeps holding PATHS because its
    #  readers expect paths; a field's meaning belongs to them. A passage whose line does not resolve is
    #  reported as NOT CITABLE rather than returned without one, which is the clause word for word.
    _passage_hits: List[Dict[str, Any]] = []
    _not_citable: List[Dict[str, Any]] = []
    for _rel, _plist in sorted((data.get("passages") or {}).items()):
        for _p in _plist or []:
            if not needle or needle not in (_p.get("tokens") or []):
                continue
            if not isinstance(_p.get("line"), int) or _p["line"] < 1:
                _not_citable.append({"path": _rel, "why": (
                    "this passage carries no resolvable line, so it CANNOT be cited - a claim traced to a "
                    "document but not to a place in it is not traceable")})
                continue
            _passage_hits.append({"path": _rel, "line": _p["line"], "text": _p.get("text") or ""})
    _passage_hits.sort(key=lambda h: (h["path"], h["line"]))
    _unread = [f["path"] for f in (man.get("files") or []) if f.get("state") != INDEXED]
    return {
        "term": term,
        "hits": hits,
        "matched_files": len(_all_hits),
        "shown_files": len(hits),
        "truncated": len(hits) < len(_all_hits),
        "passages": _passage_hits[:limit],
        "passages_matched": len(_passage_hits),
        "not_citable": _not_citable,
        "citation_basis": (
            f"{len(_passage_hits)} passage(s) matched, each carrying its document and LINE so the claim can "
            f"be checked at the source. A passage with no resolvable line is listed under not_citable "
            f"rather than returned without one: a claim traced to a document but not to a place in it is "
            f"not traceable."
            + (f" {len(_not_citable)} passage(s) could not be cited." if _not_citable else "")),
        "file_hits_basis": (
            f"{len(_all_hits)} file(s) matched and {len(hits)} are shown"
            + (f", so THIS IS A TOP-{len(hits)} of a larger set - raise `limit` to see the rest"
               if len(hits) < len(_all_hits) else ", none omitted")),
        "searched_files": len(toks),
        #  THE FU-124 RULE, MADE VISIBLE: what the search could not look inside, named.
        "not_searched": _unread,
        "basis": (f"exact lexical match over {len(toks)} indexed file(s). {len(_unread)} listed file(s) "
                  f"were NOT searched because their text is not in the index — they are unread or "
                  f"excluded, and nothing unread is in the knowledge base. This is token matching, not "
                  f"semantic recall: a document about the subject that never uses the word does not "
                  f"match"),
        "embedding_backend": None,
    }
