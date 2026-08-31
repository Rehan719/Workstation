#!/usr/bin/env python3
"""Report (and, only if you insist, remove) VSB entities created by test runs.

WHY THIS EXISTS
    integration_tests/conftest.py promised "isolated test data directories so tests don't pollute
    real data" but never set DATA_DIR — where VSB entities actually live. Every suite run therefore
    wrote entities into the real store. By 2026-08-31 that store held 1,552 entities across only 45
    distinct names, 1,526 of them sharing a name with another: "pytest VSB business-plan seed check"
    x185, "pytest per-vsb swarm" x184, "list-flags test" x184, "avatar grounding test" x183.

    conftest now isolates DATA_DIR, so no NEW pollution accumulates. This script deals with what is
    already there — and it is deliberately not run for you.

SAFETY
    Dry run by default: it prints what it would remove and removes nothing. `--apply` is required to
    delete, and even then an entity is SKIPPED when it shows signs of being real work:
      * it is referenced by any service contract, marketplace listing, or ledger entry
    Board/plan/swarm state is REPORTED but is not a veto — test runs exercise real flows, so their
    entities carry that state too, and vetoing on it protected all 1,037 matches and made the script
    useless. The name is the signal; nobody names an enterprise "pytest per-vsb swarm".
    Deleting a record that something else points at is how you get dangling references, which is
    worse than clutter.

USAGE
    python scripts/prune_test_entities.py                 # report only
    python scripts/prune_test_entities.py --apply         # actually delete the safe ones
    python scripts/prune_test_entities.py --pattern foo   # add your own name pattern (repeatable)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from agentic_core.config import data_path  # noqa: E402

# Names that only a test run produces. Matched case-insensitively against the entity name.
TEST_NAME_PATTERNS = [
    r"\bpytest\b",
    r"\blist-flags test\b",
    r"\bavatar grounding test\b",
    r"\bper-vsb deliverable\b",
    r"\bledger lock-in\b",
    r"\bsmoke test\b",
    r"\btest VSB\b",
    r"\bseed check\b",
]

# These fields are reported, NOT used as a veto. A first draft treated them as "this entity carries
# real work, never touch it" and consequently protected all 1,037 matches, making the script useless:
# the tests exercise genuine flows, so of course their entities have boards, plans and swarms. The
# unambiguous signal is the NAME — nobody names their enterprise "pytest per-vsb swarm".
INFO_FIELDS = ("has_board", "business_plan_scope", "has_native_swarm",
               "operating_cycles", "last_distributable")


def read_json(path: pathlib.Path):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return json.loads(path.read_text(encoding=enc))
        except UnicodeDecodeError:
            continue
        except (OSError, ValueError):
            return None
    return None


# Only these carry CROSS-entity references — a vsb_id here would dangle if the entity vanished.
# Everything else under data/ that mentions a vsb_id (its board pack, its repo, its business plan,
# its deliverables) is the entity's OWN footprint, created by the same run that created it. A first
# draft scanned all of data/ and therefore reported every one of the 1,037 candidates as
# "referenced", which is true and useless: a record pointing only at itself is not a reference.
CROSS_REFERENCE_FILES = (
    "vsb_contracts.json",          # §15 contracts name a client and a provider
    "living_vsbs.json",            # the autonomous economy roster
    "economy_ventures_portfolio.json",
    "economy_owner_payments.json",
)
CROSS_REFERENCE_DIRS = ("marketplace", "economy")


def referenced_ids() -> set[str]:
    """vsb_ids named by something OTHER than the entity's own derived artifacts."""
    ids: set[str] = set()
    root = pathlib.Path(str(data_path("."))).resolve()
    targets: list[pathlib.Path] = [root / f for f in CROSS_REFERENCE_FILES]
    for d in CROSS_REFERENCE_DIRS:
        targets += list((root / d).rglob("*.json")) if (root / d).exists() else []
    for path in targets:
        if not path.exists() or not path.is_file():
            continue
        doc = read_json(path)
        if doc is None:
            continue
        for m in re.findall(r"vsb-[0-9a-f]{6,}", json.dumps(doc)):
            ids.add(m)
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually delete (default: report only)")
    ap.add_argument("--pattern", action="append", default=[], help="extra name pattern (regex)")
    args = ap.parse_args()

    store = pathlib.Path(str(data_path("vsb_entities")))
    if not store.exists():
        print(f"no entity store at {store}")
        return 0

    patterns = [re.compile(p, re.I) for p in TEST_NAME_PATTERNS + args.pattern]
    linked = referenced_ids()

    total = removable = kept_real = kept_linked = 0
    by_name: dict[str, int] = {}
    to_remove: list[pathlib.Path] = []

    for path in sorted(store.glob("*.json")):
        doc = read_json(path)
        if doc is None:
            continue
        total += 1
        name = str(doc.get("name") or "")
        if not any(p.search(name) for p in patterns):
            continue
        # The reference check is the HARD guard and must run first: deleting a record something
        # else points at creates a dangling reference, which is worse than clutter. (In the first
        # draft the real-work veto ran first and swallowed every candidate, so this never reported.)
        if doc.get("vsb_id") in linked:
            kept_linked += 1
            continue
        if any(doc.get(f) for f in INFO_FIELDS):
            kept_real += 1          # counted for visibility only — not a veto
        removable += 1
        by_name[name] = by_name.get(name, 0) + 1
        to_remove.append(path)

    print(f"entities in store            : {total}")
    print(f"test-named and safe to remove: {removable}")
    print(f"  ...of those, carrying board/plan/swarm state : {kept_real}  (reported, not a veto)")
    print(f"test-named but KEPT (referenced elsewhere)    : {kept_linked}")
    if by_name:
        print("\nwould remove, by name:")
        for n, c in sorted(by_name.items(), key=lambda kv: -kv[1]):
            print(f"  {c:>5}x  {n[:70]}")

    if not args.apply:
        print("\nDRY RUN — nothing was deleted. Re-run with --apply to remove the entries above.")
        return 0

    deleted = 0
    for path in to_remove:
        try:
            path.unlink()
            deleted += 1
        except OSError as exc:
            print(f"  could not delete {path.name}: {exc}")
    print(f"\ndeleted {deleted} entity file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
