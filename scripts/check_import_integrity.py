#!/usr/bin/env python3
"""Fail if any live module imports a first-party module that does not exist.

WHY THIS EXISTS
    On 2026-08-31 an archive pass moved 259 modules out of the live tree. 49 of them were named in
    real import statements by code that was still live, and 4 more were invoked only from CI and
    setup scripts. Nothing caught it: the integration suite does not import those modules, so it
    stayed green. The break surfaced as a red Doc-Sync job with ModuleNotFoundError.

    This check closes that gap. It is static, so it costs no runtime and needs no fixtures, and it
    sees imports that no test happens to exercise.

WHAT COUNTS AS A BREAK
    A module-level import (outside try/except) of a first-party module with no file behind it.
    Guarded imports are deliberate optional dependencies and are ignored.

CORRECTNESS NOTES — both of these produced wrong answers in a first draft:
  * Namespace packages: a directory with no __init__.py IS importable in py3. Requiring
    __init__.py wrongly flagged agentic_core/api/v290, and therefore app_mvp.py, which boots fine.
  * Self-contained products: products/mjm-intelligence-engine ships its own `core/` package and is
    run with its own directory as the path root. Resolving `core.models` against the repo root
    wrongly flagged 21 of its modules. Such roots are resolved against themselves.

BASELINE
    The repo already carries pre-existing dangling imports from earlier work. Failing on those would
    make this check useless noise, so they are recorded in the baseline file and this check fails
    only on NEW breaks. To accept a new one deliberately, add it to the baseline with a reason.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = ROOT / "scripts" / "import_integrity_baseline.txt"

SKIP_DIRS = {"node_modules", "venv", ".venv", "__pycache__", ".git", "build", "dist",
             ".pytest_cache", ".mypy_cache", "_archive"}
FIRST_PARTY = ("agentic_core", "products", "src", "scripts", "config", "integration_tests", "core")

# Directories that are their own import root (run with themselves on sys.path).
SELF_ROOTED = [ROOT / "products" / "mjm-intelligence-engine"]


def _resolves(mod: str, base: pathlib.Path) -> bool:
    rel = mod.replace(".", "/")
    return (base / f"{rel}.py").exists() or (base / rel).is_dir()


def resolves_anywhere(mod: str, origin: pathlib.Path) -> bool:
    if _resolves(mod, ROOT):
        return True
    for root in SELF_ROOTED:                      # a self-rooted product resolves against itself
        if origin.is_relative_to(root) and _resolves(mod, root):
            return True
    return False


def dangling_imports() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for path in ROOT.rglob("*.py"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, OSError):
            continue
        guarded = {id(stmt) for node in ast.walk(tree) if isinstance(node, ast.Try)
                   for stmt in ast.walk(node) if isinstance(stmt, (ast.Import, ast.ImportFrom))}
        bad: list[str] = []
        for node in tree.body:                    # module level only
            if id(node) in guarded:
                continue
            targets: list[str] = []
            if isinstance(node, ast.Import):
                targets = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                targets = [node.module]
            bad += [t for t in targets
                    if t.startswith(FIRST_PARTY) and not resolves_anywhere(t, path)]
        if bad:
            out[rel.as_posix()] = sorted(set(bad))
    return out


def load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    return {ln.split("#", 1)[0].strip() for ln in BASELINE.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")} - {""}


def main() -> int:
    found = dangling_imports()
    baseline = load_baseline()
    new = {f: m for f, m in found.items() if f not in baseline}

    if "--write-baseline" in sys.argv:
        BASELINE.write_text(
            "# Files with pre-existing dangling first-party imports, recorded so that\n"
            "# scripts/check_import_integrity.py fails only on NEW breaks.\n"
            "# Removing a line here is how you assert a file has been fixed.\n"
            + "\n".join(f"{f}  # missing: {', '.join(m)}" for f, m in sorted(found.items())) + "\n",
            encoding="utf-8")
        print(f"baseline written: {len(found)} files")
        return 0

    fixed = sorted(baseline - set(found))
    if fixed:
        print(f"{len(fixed)} baselined file(s) no longer dangle — drop them from the baseline:")
        for f in fixed[:10]:
            print(f"  {f}")
        print()

    if not new:
        print(f"import integrity OK — no new dangling first-party imports "
              f"({len(found)} baselined).")
        return 0

    print(f"IMPORT INTEGRITY FAILED — {len(new)} file(s) import first-party modules that do not exist:")
    for f, mods in sorted(new.items()):
        print(f"  {f}")
        for m in mods:
            print(f"        missing: {m}")
    print("\nEither restore the module, fix the import, or — if this is deliberate — add the file to")
    print(f"{BASELINE.relative_to(ROOT)} with a reason.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
