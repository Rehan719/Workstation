"""Recovery audit — find work this repository ALREADY has before building it again.

W482. Three rounds in a row (W480, W481, W482) an outside proposal offered to build something this
repository already contained: the nine-engine registry and the five-gate clearance chain (W480), the
transformation cascade's own verdict (W481), and the Biomimetic Minimisation Engine — whose Schrödinger
bridge and diffusion engine had been DELETED but are recoverable from git, and whose Landauer meter still
exists as `core/transcendent_subsystems/tfel.py` (W482). Rebuilding these would have produced a second
implementation of each, and the new one would have been the weaker.

This script finds those cases mechanically, and prints the command that recovers each one. It reads; it
changes nothing.

    python scripts/recovery_audit.py                 # human summary
    python scripts/recovery_audit.py --json out.json # machine-readable
    python scripts/recovery_audit.py --only orphans,deleted

Findings (each with the evidence and the next command):
  orphans   — a compiled .pyc with no source beside it: the source was deleted, the work may be recoverable
  deleted   — each of those, classified from git history WITH RENAMES: moved_to_archive (the sweep moved it;
              read the destination), recoverable (deleted outright; git holds it), name_elsewhere (a file of
              that name is under _archive/ — compare first) or unknown. Biggest work first
  archived  — modules under _archive/ whose name nothing live references
  optional  — `try: import X` guards whose module is NOT installed, so that code path is silently off
  unwired   — APIRouter modules the app never includes
  unfilled  — registries/collections with a register/add API that nothing ever calls
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE_DIRS = ["agentic_core", "core", "apps/workstation-superapp/src", "scripts", "integration_tests"]
PKG_PREFIXES = ["agentic_core/", "core/"]


def _run(args: list[str]) -> str:
    try:
        # utf-8 explicitly: git output carries non-cp1252 characters (commit subjects, paths) and the
        # platform default decoder raises on them
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=300,
                              encoding="utf-8", errors="replace").stdout
    except Exception as e:                                    # a missing git is a finding, not a crash
        return f"__ERROR__ {e}"


def _py_files() -> list[Path]:
    out = []
    for d in PKG_PREFIXES:
        base = ROOT / d.rstrip("/")
        if base.exists():
            out += [p for p in base.rglob("*.py") if "__pycache__" not in p.parts]
    return out


def find_orphan_pycache() -> list[dict]:
    """A .pyc whose .py is gone: something was deleted and its compiled form was left behind."""
    found = []
    for d in PKG_PREFIXES:
        base = ROOT / d.rstrip("/")
        if not base.exists():
            continue
        for pyc in base.rglob("__pycache__/*.pyc"):
            stem = pyc.name.split(".")[0]
            src = pyc.parent.parent / f"{stem}.py"
            if not src.exists():
                found.append({"pyc": str(pyc.relative_to(ROOT)).replace("\\", "/"),
                              "missing_source": str(src.relative_to(ROOT)).replace("\\", "/")})
    return found


def _history_map() -> dict:
    """path -> {"how": "deleted"|"moved", "sha", "subject", "to"} for every tracked file that left its place.

    W482 accuracy fix: a file MOVED into `_archive/` is recorded by git as a RENAME, not a deletion, so a
    `--diff-filter=D` scan misses exactly the cases most worth recovering (the W159/W382 archive sweeps).
    This reads D and R together with `--name-status -M`.
    """
    log = _run(["git", "log", "--diff-filter=DR", "-M", "--pretty=format:__C__%H|%s", "--name-status"])
    out: dict = {}
    sha = subject = None
    for line in log.splitlines():
        if line.startswith("__C__"):
            sha, subject = line[5:].split("|", 1)
            continue
        if not line.strip() or not sha:
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("D") and len(parts) >= 2:
            out.setdefault(parts[1], {"how": "deleted", "sha": sha, "subject": subject})
        elif status.startswith("R") and len(parts) >= 3:
            out.setdefault(parts[1], {"how": "moved", "sha": sha, "subject": subject, "to": parts[2]})
    return out


def _archive_index() -> dict:
    """basename -> [paths] under _archive/ (a fallback when history does not name the destination)."""
    idx: dict = {}
    arch = ROOT / "_archive"
    if arch.exists():
        for p in arch.rglob("*.py"):
            idx.setdefault(p.name, []).append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return idx


def find_deleted_sources(paths: list[str]) -> list[dict]:
    """Classify each missing source, with the command that recovers it, biggest work first.

    moved_to_archive — git recorded the move; read the destination (it is the same bytes unless edited since)
    recoverable      — deleted outright; git holds the last version
    name_elsewhere   — no history entry, but a file of that name exists under _archive/ (verify before trusting)
    unknown          — nothing to recover
    """
    hist, arch = _history_map(), _archive_index()
    out = []
    for rel in paths:
        h = hist.get(rel)
        row: dict = {"path": rel}
        blob_ref = None
        if h and h["how"] == "moved":
            row.update(kind="moved_to_archive", moved_to=h["to"], moved_in=h["sha"][:8],
                       commit_subject=h["subject"][:100], read_with=f"cat {h['to']}")
            blob_ref = f"{h['sha']}:{h['to']}"
        elif h:
            row.update(kind="recoverable", deleted_in=h["sha"][:8], commit_subject=h["subject"][:100],
                       recover_with=f"git show {h['sha'][:8]}^:{rel} > {rel}")
            blob_ref = f"{h['sha']}^:{rel}"
        else:
            copies = [c for c in arch.get(Path(rel).name, [])]
            if copies:
                row.update(kind="name_elsewhere", candidates=copies[:3],
                           note="same file name under _archive/; compare before trusting it")
            else:
                row.update(kind="unknown", note="no history entry and no archive copy")
        if blob_ref:
            blob = _run(["git", "show", blob_ref])
            row["lines"] = len(blob.splitlines()) if blob and not blob.startswith("__ERROR__") else None
        else:
            row["lines"] = None
        out.append(row)
    order = {"recoverable": 0, "moved_to_archive": 1, "name_elsewhere": 2, "unknown": 3}
    return sorted(out, key=lambda r: (order[r["kind"]], -(r["lines"] or 0)))


def _live_text() -> str:
    parts = []
    for d in CODE_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.suffix in (".py", ".ts", ".tsx", ".json", ".yml", ".yaml", ".toml", ".cfg") \
                    and "__pycache__" not in p.parts and "node_modules" not in p.parts:
                try:
                    parts.append(p.read_text(encoding="utf-8", errors="ignore"))
                except Exception:
                    pass
    return "\n".join(parts)


def find_archived_unreferenced(live: str) -> list[dict]:
    """Modules under _archive/ whose module name nothing live mentions — recoverable work, or settled history."""
    arch = ROOT / "_archive"
    if not arch.exists():
        return []
    out = []
    for p in sorted(arch.rglob("*.py")):
        name = p.stem
        if name in ("__init__", "setup", "conftest"):
            continue
        if not re.search(rf"\b{re.escape(name)}\b", live):
            out.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "module": name})
    return out


def find_optional_imports_missing() -> list[dict]:
    """`try: import X` guards whose module is not installed — that code path is silently off."""
    out, seen = [], set()
    for p in _py_files():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Try):
                continue
            handled = any(isinstance(h.type, ast.Name) and h.type.id in ("ImportError", "Exception")
                          or h.type is None for h in node.handlers)
            if not handled:
                continue
            for stmt in node.body:
                mods = []
                if isinstance(stmt, ast.Import):
                    mods = [a.name.split(".")[0] for a in stmt.names]
                elif isinstance(stmt, ast.ImportFrom) and stmt.module and stmt.level == 0:
                    mods = [stmt.module.split(".")[0]]
                for m in mods:
                    if m in seen or m in ("agentic_core", "core", "apps"):
                        continue
                    seen.add(m)
                    probe = subprocess.run([sys.executable, "-c", f"import {m}"],
                                           cwd=ROOT, capture_output=True, text=True)
                    if probe.returncode != 0:
                        out.append({"module": m, "guarded_in": str(p.relative_to(ROOT)).replace("\\", "/"),
                                    "effect": "the guarded code path is off in this environment"})
    return out


def find_unwired_routers(live: str) -> list[dict]:
    """Modules that define an APIRouter the app never includes."""
    app = (ROOT / "agentic_core" / "app_mvp.py")
    app_text = app.read_text(encoding="utf-8", errors="ignore") if app.exists() else ""
    out = []
    for p in _py_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "APIRouter(" not in text:
            continue
        mod = str(p.relative_to(ROOT)).replace("\\", "/")[:-3].replace("/", ".")
        leaf = mod.split(".")[-1]
        if mod in app_text:
            continue
        # an aggregator may include it instead of app_mvp — look for the dotted path anywhere live
        if re.search(rf"{re.escape(mod)}\b", live) or re.search(rf"include_router\([^)]*\b{re.escape(leaf)}\b", live):
            continue
        out.append({"module": mod, "path": str(p.relative_to(ROOT)).replace("\\", "/")})
    return out


def find_unfilled_registries() -> list[dict]:
    """A class with a register/add API that nothing ever calls: declared capacity, never populated."""
    out = []
    for p in _py_files():
        text = p.read_text(encoding="utf-8", errors="ignore")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            meths = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            reg = [m for m in meths if m in ("register", "register_validator", "register_engine", "add_engine")]
            if not reg:
                continue
            for m in reg:
                calls = _run(["git", "grep", "-n", f".{m}(", "--", "agentic_core", "core", "scripts",
                              "integration_tests"])
                sites = [ln for ln in calls.splitlines()
                         if f".{m}(" in ln and f"def {m}(" not in ln
                         and not ln.startswith(str(p.relative_to(ROOT)).replace("\\", "/") + ":")]
                if not sites:
                    out.append({"class": node.name, "method": m,
                                "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                                "effect": "nothing ever registers: lookups raise or return empty"})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", dest="json_out", help="write the findings to this file")
    ap.add_argument("--only", help="comma-separated: orphans,deleted,archived,optional,unwired,unfilled")
    args = ap.parse_args()
    want = set((args.only or "orphans,deleted,archived,optional,unwired,unfilled").split(","))

    report: dict = {}
    if "orphans" in want or "deleted" in want:
        orphans = find_orphan_pycache()
        if "orphans" in want:
            report["orphans"] = orphans
        if "deleted" in want:
            report["deleted"] = find_deleted_sources(sorted({o["missing_source"] for o in orphans}))
    live = _live_text() if ({"archived", "unwired"} & want) else ""
    if "archived" in want:
        report["archived"] = find_archived_unreferenced(live)
    if "optional" in want:
        report["optional"] = find_optional_imports_missing()
    if "unwired" in want:
        report["unwired"] = find_unwired_routers(live)
    if "unfilled" in want:
        report["unfilled"] = find_unfilled_registries()

    for kind, rows in report.items():
        print(f"\n== {kind}: {len(rows)}")
        for r in rows[:25]:
            print("  " + json.dumps(r, ensure_ascii=False))
        if len(rows) > 25:
            print(f"  … and {len(rows) - 25} more (use --json for all)")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwritten: {args.json_out}")
    print("\nThis audit REPORTS candidates with their evidence. It never decides that something is dead: "
          "[[feedback-reachability-blind-spots]] — imports and a green suite do not prove a file is unused.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
