"""
Priority — how much a follow-up matters to delivering the vision, and how far delivery has come, weighted by that.

W478 (the Owner's instruction, 2026-09-19): "there needs to be a prioritisation mechanism along with a scheduling
mechanism within the planning system, to correlate significance to vision-delivery importance to completion of
delivery". Before this, the schedule ordered rows by plan position, then high/medium/low, then age: a Tier-1 untruth on
the Genesis journey and a tidy-up in an internal script sorted alike, and PLAN NOW counted rows, not what they are worth.

A row's priority is a PRODUCT of named parts, each shown with the score (never a black box):
  vision       — the weight of the vision area the row serves, decided in this order: an explicit row["area"]; the vision
                 section the row's title CITES ('§8', '§11.2' — the ledgers' own classification; the heaviest if several);
                 its PRIMARY file (a row listing no files uses the one tracked file each name in its text can only mean);
                 a word of its title. All mapped by docs/PRIORITY.json — the Owner's values live in that one file.
  truth        — the defect tier when known (Tier-1 a truth defect on a reached surface · Tier-2 an invisible shortfall ·
                 Tier-3 disclosed or unreached), else the finder's severity.
  reach        — core journey surface · reached/secondary · internal.
  criticality  — the row rides the current phase gate (the phase of the next open plan item) · a later phase ·
                 Owner-gated (0: it cannot be scheduled).
  breadth      — more untruths closed by one fix ranks higher (a sweep row's finding count).
  effort       — files beyond one per finding rank a little lower, so quick wins surface without cancelling breadth.
score = 100 × vision × truth × reach × criticality × breadth × effort, rounded to 0.1.

Follow-up completion is weighted the same way: the share of the ROWS' priority already closed in a phase (closed rows
are scored with the same parts, criticality as if in their own gate), beside the plain row count. It measures the
register's rows, not plan items (an item finished before the register existed carries no rows); the retired pre-plan
NEXT queue is shown apart and left out of the overall figure.

The plan's own order is never changed here: phase gates stand (P1 before P2), and inside an item rows run
highest-priority first. `suggested_order` shows the open items by total open priority for the Owner to consider.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TIER_WEIGHT = {1: 1.0, 2: 0.5, 3: 0.2}
RETIRED = "retired NEXT (pre-plan)"
SEVERITY_WEIGHT = {"high": 0.8, "medium": 0.5, "low": 0.25}
REACH_WEIGHT = {"core": 1.0, "secondary": 0.6, "internal": 0.3}
CRITICALITY = {"gate": 1.0, "later": 0.5, "owner": 0.0}

# The Owner-editable defaults (docs/PRIORITY.json overrides any of these). Areas are matched in order; the first whose
# file prefix or title word matches a row wins.
DEFAULTS: Dict[str, Any] = {
    "areas": [
        {"id": "faith", "name": "§11 faith-content constitution + the Quran Education Platform (Appendix A)", "weight": 1.0,
         "files": ["agentic_core/api/religion.py", "agentic_core/religious_domain/", "agentic_core/api/qep",
                   "agentic_core/reactor/religion/", "apps/workstation-superapp/src/pages/domains/ReligionHub.tsx",
                   "apps/workstation-superapp/src/pages/domains/QEPReligionHub.tsx", "apps/workstation-superapp/src/components/qep/",
                   "apps/workstation-superapp/src/pages/qep/"],
         "words": ["quran", "qur'an", "ayah", "surah", "tafsir", "basmala", "hifz", "recitation"]},
        {"id": "compliance", "name": "§10 the quality bar + §11 live compliance", "weight": 1.0,
         "files": ["agentic_core/api/compliance.py", "agentic_core/compliance/", "agentic_core/vbs/quality.py",
                   "apps/workstation-superapp/src/pages/governance/ComplianceChecker.tsx"],
         "words": ["compliance", "halal", "sharia", "ethical", "qms gate"]},
        {"id": "lifecycle", "name": "§4 the end-to-end lifecycle + §13 what the output is", "weight": 0.9,
         "files": ["agentic_core/api/genesis.py", "agentic_core/api/intelligence.py", "agentic_core/api/vsb.py",
                   "agentic_core/api/deliverables.py", "agentic_core/api/business_plan.py",
                   "apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx",
                   "apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx",
                   "apps/workstation-superapp/src/pages/Deliverables.tsx",
                   "apps/workstation-superapp/src/pages/enterprise/BusinessPlan.tsx"],
         "words": ["genesis", "establish", "deliverable", "board pack", "repository"]},
        {"id": "native_ai", "name": "§6 the native AI mandate (own models · orchestration · swarm)", "weight": 0.9,
         "files": ["agentic_core/ai/", "apps/workstation-superapp/src/pages/developers/NativeAI.tsx"],
         "words": ["native ai", "provenance", "served_by"]},
        {"id": "organisation", "name": "§5 the living organisation (Chief → Board → CEO → C-Suite → CoE → BTO)", "weight": 0.8,
         "files": ["agentic_core/api/board.py", "agentic_core/api/v138/", "agentic_core/api/swarm.py",
                   "agentic_core/api/change_control.py", "agentic_core/api/transformation_orchestration.py",
                   "apps/workstation-superapp/src/pages/enterprise/BoardOfDirectors.tsx",
                   "apps/workstation-superapp/src/components/organism/SwarmIntelligence.tsx"],
         "words": ["chief", "board of directors", "ceo", "c-suite", "org cascade", "change control"]},
        {"id": "economy", "name": "§12 the economic organism (the VSB economy)", "weight": 0.7,
         "files": ["agentic_core/economy/", "agentic_core/api/economy.py", "agentic_core/api/capital_fund.py",
                   "apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx",
                   "apps/workstation-superapp/src/pages/enterprise/CapitalDashboard.tsx",
                   "apps/workstation-superapp/src/pages/enterprise/ServiceContracts.tsx"],
         "words": ["waterfall", "wst", "charity", "virtual ledger", "economy cycle"]},
        {"id": "organism", "name": "§8 the biomimetic living organism", "weight": 0.7,
         "files": ["agentic_core/organism/", "agentic_core/api/organism_status.py", "agentic_core/api/sovereign_evolution.py",
                   "agentic_core/api/transformation.py", "apps/workstation-superapp/src/pages/organism/",
                   "apps/workstation-superapp/src/pages/evolution/", "apps/workstation-superapp/src/pages/TransformationDashboard.tsx"],
         "words": ["heartbeat", "organism", "homeostasis", "immune", "self-healing", "survival instinct"]},
        {"id": "fabric", "name": "§7 the reconfigurable resource fabric + the catalogue", "weight": 0.7,
         "files": ["agentic_core/api/resource_fabric.py", "agentic_core/api/products.py", "agentic_core/catalog/",
                   "apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx",
                   "apps/workstation-superapp/src/pages/marketplace/"],
         "words": ["fabric", "marketplace", "catalogue", "composition"]},
        {"id": "domains_ux", "name": "§3A the domains + §9 the user experience + §14 democratisation", "weight": 0.7,
         "files": ["apps/workstation-superapp/src/pages/", "apps/workstation-superapp/src/components/", "packages/ui/",
                   "agentic_core/api/"],
         "words": []},
        {"id": "tooling", "name": "internal tooling, tests and docs", "weight": 0.3,
         "files": ["scripts/", "integration_tests/", "docs/", "config/", "agentic_core/plan_followups.py",
                   "agentic_core/plan_priority.py"],
         "words": []},
    ],
    "unmapped_weight": 0.5,
    # W478 (refutation 2) — the vision section a row's title CITES (the ledgers file each entry under one or more of
    # them: 'v5 R6.1: §8 survival instinct / §8→§12 …') is the row's own classification, and it decides the area before
    # any file heuristic does; a row citing several takes the heaviest. §15 (the founding principles) binds every area,
    # so it maps to none. A sub-section is looked up exactly first, then by its section number.
    "sections": {"3": "domains_ux", "3A": "domains_ux", "4": "lifecycle", "5": "organisation", "6": "native_ai",
                 "7": "fabric", "8": "organism", "9": "domains_ux", "10": "compliance", "11": "compliance",
                 "11.2": "faith", "12": "economy", "13": "lifecycle", "14": "domains_ux", "17.2": "organism",
                 "17.3": "lifecycle", "17.4": "organisation", "17.5": "organism"},
    # the surfaces a user meets on the core journey: a row touching one of these is 'core' reach
    "core_surfaces": ["agentic_core/api/genesis.py", "agentic_core/api/intelligence.py", "agentic_core/api/vsb.py",
                      "agentic_core/api/deliverables.py", "agentic_core/api/religion.py", "agentic_core/religious_domain/",
                      "agentic_core/api/compliance.py", "agentic_core/compliance/", "agentic_core/vbs/quality.py",
                      "apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx",
                      "apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx",
                      "apps/workstation-superapp/src/pages/Deliverables.tsx",
                      "apps/workstation-superapp/src/pages/domains/", "apps/workstation-superapp/src/components/DomainTool.tsx",
                      "apps/workstation-superapp/src/pages/DashboardNew.tsx", "packages/ui/src/CommandCenter.tsx"],
    "breadth_per_log": 0.25,
    "effort_per_file": 0.1,
}

_TIER_IN_TITLE = re.compile(r"\bTier-([123])\b")
_LEDGER_KEY = re.compile(r"^v[45] R\d+\.\d+:")          # rows registered from the ledgers' standing Tier-1 entries
_FINDINGS = re.compile(r"\b(\d+) Tier-[123] (?:truth defects?|shortfalls?)\b")


def config_path(root: Path) -> Path:
    return root / "docs" / "PRIORITY.json"


def load_config(root: Path) -> Tuple[Dict[str, Any], List[str]]:
    """The weights in force and any problem reading them. A missing file means the defaults; an unreadable or malformed
    one is REPORTED (check() fails on it) and the defaults serve, so nothing that renders can crash on it."""
    p = config_path(root)
    cfg = json.loads(json.dumps(DEFAULTS))
    if not p.exists():
        cfg["_tracked"] = _tracked_files(root)
        return cfg, []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                      # noqa: BLE001 — reported, never raised
        cfg["_tracked"] = _tracked_files(root)
        return cfg, [f"docs/PRIORITY.json cannot be read ({exc.__class__.__name__}): the default weights serve until it is repaired"]
    problems = config_problems(raw)
    if problems:
        cfg["_tracked"] = _tracked_files(root)
        return cfg, problems
    cfg.update(raw)
    cfg["_tracked"] = _tracked_files(root)
    return cfg, []


def _tracked_files(root: Path) -> List[str]:
    """The repository's tracked files, so a short name a row's text cites ('genesis.py:394', 'religious_domain/api.py')
    resolves to the one file it can only mean. Not a git checkout (a scratch root): none — only full paths resolve."""
    import subprocess
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=str(root), capture_output=True, timeout=20)
        if out.returncode != 0:
            return []
        return [f for f in out.stdout.decode("utf-8", "replace").split("\0") if f]
    except Exception:                              # noqa: BLE001 — resolution is a convenience, never a crash
        return []


def config_problems(raw: Any) -> List[str]:
    p: List[str] = []
    if not isinstance(raw, dict):
        return ["docs/PRIORITY.json must be an object"]
    areas = raw.get("areas", DEFAULTS["areas"])
    if not isinstance(areas, list) or not areas:
        p.append("docs/PRIORITY.json: areas must be a non-empty list")
        return p
    seen = set()
    for i, a in enumerate(areas):
        name = f"docs/PRIORITY.json area {i + 1}"
        if not isinstance(a, dict):
            p.append(f"{name}: not an object")
            continue
        if not isinstance(a.get("id"), str) or not a["id"].strip():
            p.append(f"{name}: id must be a non-empty string")
        if not isinstance(a.get("name"), str) or not a["name"].strip():
            p.append(f"{name} ({a.get('id')}): name must be a non-empty string (it is what every score's basis says)")
        elif a["id"] in seen:
            p.append(f"{name}: duplicate id {a['id']!r}")
        else:
            seen.add(a["id"])
        w = a.get("weight")
        if not isinstance(w, (int, float)) or isinstance(w, bool) or not (0.0 <= float(w) <= 1.0):
            p.append(f"{name} ({a.get('id')}): weight must be a number from 0 to 1")
        for key in ("files", "words"):
            v = a.get(key, [])
            if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
                p.append(f"{name} ({a.get('id')}): {key} must be a list of non-empty strings")
        if not a.get("files") and not a.get("words"):
            p.append(f"{name} ({a.get('id')}): needs at least one file prefix or title word")
    for key in ("unmapped_weight", "breadth_per_log", "effort_per_file"):
        if key in raw:
            v = raw[key]
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not (0.0 <= float(v) <= 1.0):
                p.append(f"docs/PRIORITY.json: {key} must be a number from 0 to 1")
    cs = raw.get("core_surfaces", DEFAULTS["core_surfaces"])
    if not isinstance(cs, list) or not all(isinstance(x, str) and x.strip() for x in cs):
        p.append("docs/PRIORITY.json: core_surfaces must be a list of non-empty strings")
    secs = raw.get("sections", DEFAULTS["sections"])
    ids = {a.get("id") for a in areas if isinstance(a, dict)}
    if not isinstance(secs, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in secs.items()):
        p.append("docs/PRIORITY.json: sections must map a section number ('8', '11.2') to an area id")
    else:
        for k, v in secs.items():
            if v not in ids:
                p.append(f"docs/PRIORITY.json: section §{k} maps to {v!r}, which is not an area id")
    return p


def row_field_problems(row: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    """The optional priority fields a row may carry, validated (set with followups.py add/reprioritise). With the
    weights in force, a stored area that names no configured area is a problem (refutation: renaming an area id in
    docs/PRIORITY.json silently unmapped the rows the Owner had placed in it)."""
    p: List[str] = []
    if cfg is not None and isinstance(row.get("area"), str) and row["area"].strip() and _area_by_id(cfg, row["area"]) is None:
        p.append(f"area {row['area']!r} names no area in docs/PRIORITY.json — the row would be silently unmapped "
                 "(python scripts/followups.py reprioritise <id> --area <id> or --clear area)")
    if "tier" in row and not (isinstance(row["tier"], int) and not isinstance(row["tier"], bool) and row["tier"] in TIER_WEIGHT):
        p.append("tier must be 1, 2 or 3")
    if "reach" in row and row["reach"] not in REACH_WEIGHT:
        p.append("reach must be core, secondary or internal")
    if "area" in row and not (isinstance(row["area"], str) and row["area"].strip()):
        p.append("area must name a priority area (docs/PRIORITY.json)")
    if "findings" in row and not (isinstance(row["findings"], int) and not isinstance(row["findings"], bool) and row["findings"] >= 1):
        p.append("findings must be a whole number of at least 1")
    return p


def _file_match(prefix: str, f: str) -> bool:
    """A prefix ending '/' is a directory; any other prefix is a file path or a file-name stem ('agentic_core/api/qep'
    names every qep*.py router) — never a directory by accident."""
    if prefix.endswith("/"):
        return f.startswith(prefix)
    return f == prefix or (f.startswith(prefix) and "/" not in f[len(prefix):])


_NAME_IN_TEXT = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:py|tsx|ts))\b")


def _resolve(name: str, tracked: List[str]) -> Optional[str]:
    """A name a row's text cites, as the ONE tracked file it can mean ('genesis.py' → agentic_core/api/genesis.py); a
    name several files end with ('api.py') resolves to none — never a guess."""
    name = name.lstrip("./")
    if name in tracked:
        return name
    hits = [f for f in tracked if f.endswith("/" + name)]
    return hits[0] if len(hits) == 1 else None


def files_of(row: Dict[str, Any], cfg: Optional[Dict[str, Any]] = None) -> Tuple[List[str], bool]:
    """The row's files, in order (the sweep registers the primary emitting file first). W478 (refutations 1 and 2): a
    row registered with no files — the ledger rows cite theirs in their text as short names ('genesis.py:394',
    'religious_domain/api.py') — uses the tracked files those names can only mean, and says so."""
    files = [str(f) for f in (row.get("files") or []) if str(f).strip()]
    if files:
        return files, False
    tracked = (cfg or {}).get("_tracked") or []
    named: List[str] = []
    for n in _NAME_IN_TEXT.findall(str(row.get("title", "")) + " " + str(row.get("why", ""))):
        f = _resolve(n, tracked) if tracked else (n if "/" in n and n.split("/")[0] in ("agentic_core", "apps", "packages", "scripts", "config") else None)
        if f and f not in named:
            named.append(f)
    return named, bool(named)


_SECTION = re.compile(r"§\s?(\d+(?:\.\d+)?[A-Z]?)")


def _section_area(row: Dict[str, Any], cfg: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    secs = cfg.get("sections") or {}
    best: Optional[Dict[str, Any]] = None
    cited = ""
    title = str(row.get("title", ""))
    if title.startswith("sweep "):               # a sweep row names its emitting file, not a vision section
        return None, ""
    # the whole title: a ledger row's section text can itself hold ' — ' ('§3A Domain Working (Religion — Halal …) / §11')
    for s in _SECTION.findall(title):
        aid = secs.get(s) or secs.get(re.match(r"\d+", s).group(0))
        a = _area_by_id(cfg, aid) if aid else None
        if a is not None and (best is None or float(a["weight"]) > float(best["weight"])):
            best, cited = a, s
    return best, (f"the title cites §{cited}" if best else "")


def _area_by_id(cfg: Dict[str, Any], area_id: str) -> Optional[Dict[str, Any]]:
    return next((a for a in cfg["areas"] if a["id"] == area_id), None)


def area_of(row: Dict[str, Any], cfg: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    """The vision area the row serves. The row's PRIMARY file decides (where the fix lands), never an incidental later
    file (refutation: a cosmetic badge row borrowed the faith weight from a fifth file, ReligionHub.tsx); then the title
    itself (never the '— observed' prose after it); an explicit area on the row wins over both."""
    areas = cfg["areas"]
    explicit = row.get("area")
    if isinstance(explicit, str) and explicit:
        a = _area_by_id(cfg, explicit)
        if a is not None:
            return a, "set on the row"
    sec, why = _section_area(row, cfg)           # (refutation 2) the vision section the row's title cites
    if sec is not None:
        return sec, why
    files, derived = files_of(row, cfg)
    if files:
        primary = files[0]
        for a in areas:
            if any(_file_match(pre, primary) for pre in a.get("files", [])):
                return a, f"{'named in the row' if derived else 'primary file'} {primary}"
    title = str(row.get("title", "")).split(" — ")[0].lower()
    for a in areas:
        for w in a.get("words", []):
            if re.search(rf"(?<![a-z0-9]){re.escape(w.lower())}(?![a-z0-9])", title):
                return a, f"title word '{w}'"
    return None, "no area matches"


def tier_of(row: Dict[str, Any]) -> Optional[int]:
    t = row.get("tier")
    if isinstance(t, int) and not isinstance(t, bool) and t in TIER_WEIGHT:
        return t
    title = str(row.get("title", ""))
    m = _TIER_IN_TITLE.search(title)
    if m:
        return int(m.group(1))
    if _LEDGER_KEY.match(title):
        return 1                                  # the ledgers registered their standing Tier-1 entries only
    return None


def reach_of(row: Dict[str, Any], cfg: Dict[str, Any], tier: Optional[int]) -> Tuple[str, str]:
    """Core when the fix lands on a core surface (the primary file) or the page the user meets it on is one (a listed
    page/component); never because an incidental backend file further down the list is (refutation)."""
    r = row.get("reach")
    if isinstance(r, str) and r in REACH_WEIGHT:
        return r, "set on the row"
    files, derived = files_of(row, cfg)
    candidates = files[:1] + [f for f in files[1:] if f.startswith(("apps/", "packages/ui/"))]
    for f in candidates:
        if any(_file_match(pre, f) for pre in cfg["core_surfaces"]):
            return "core", f"core surface {f}" + (" (named in the row)" if derived else "")
    if tier in (1, 2):
        return "secondary", "a reached surface (the audit or sweep reproduced it there)"
    if any(f.startswith(("apps/", "packages/ui/")) for f in files):
        return "secondary", "a page or component"
    return "internal", "no page named"


def findings_of(row: Dict[str, Any]) -> int:
    n = row.get("findings")
    if isinstance(n, int) and not isinstance(n, bool) and n >= 1:
        return n
    m = _FINDINGS.search(str(row.get("title", "")))
    return int(m.group(1)) if m else 1


def _phase(slot: str) -> str:
    return slot.split(".")[0] if isinstance(slot, str) and "." in slot else slot


def score_row(row: Dict[str, Any], cfg: Dict[str, Any], gate_phase: Optional[str], as_open: bool = True) -> Dict[str, Any]:
    """The row's priority and every part of it. `as_open=False` scores a closed row as if it were open (for completion)."""
    area, area_basis = area_of(row, cfg)
    vision = float(area["weight"]) if area else float(cfg.get("unmapped_weight", 0.5))
    tier = tier_of(row)
    truth = TIER_WEIGHT[tier] if tier else SEVERITY_WEIGHT.get(str(row.get("severity")), 0.5)
    reach, reach_basis = reach_of(row, cfg, tier)
    if row.get("owner_gated") is True or row.get("slot") == "OWNER":
        crit_key = "owner" if as_open else "later"
    elif gate_phase and _phase(str(row.get("slot"))) == gate_phase:
        crit_key = "gate"
    else:
        crit_key = "later"
    n = findings_of(row)
    breadth = 1.0 + float(cfg.get("breadth_per_log", 0.25)) * math.log(n)
    listed, derived = files_of(row, cfg)
    nfiles = len(listed)
    # effort counts only the files BEYOND one per finding (refutation: a sweep row lists every writer of its untruths,
    # so charging each file cancelled its breadth — an 8-finding row scored like a 1-finding row)
    extra = max(0, nfiles - max(1, n))
    effort = 1.0 / (1.0 + float(cfg.get("effort_per_file", 0.1)) * extra)
    score = round(100.0 * vision * truth * REACH_WEIGHT[reach] * CRITICALITY[crit_key] * breadth * effort, 1)
    return {
        "score": score,
        "parts": {"vision": round(vision, 3), "truth": truth, "reach": REACH_WEIGHT[reach],
                  "criticality": CRITICALITY[crit_key], "breadth": round(breadth, 3), "effort": round(effort, 3)},
        "area": area["id"] if area else None,
        "tier": tier,
        "basis": {"area": (str(area.get("name") or area["id"]) if area else "unmapped") + f" ({area_basis})",
                  "truth": f"Tier-{tier}" if tier else f"severity {row.get('severity')} (no tier recorded)",
                  "reach": f"{reach} ({reach_basis})",
                  "criticality": {"gate": f"rides the current gate ({gate_phase})", "later": "a later phase",
                                  "owner": "awaits the Owner — never scheduled"}[crit_key],
                  "breadth": f"{n} finding{'s' if n != 1 else ''}",
                  "effort": ("no files named" if nfiles == 0 else
                             f"{nfiles} file{'s' if nfiles != 1 else ''}" + (" named in the row's text" if derived else "")
                             + (f", {extra} beyond one per finding" if extra else ""))},
    }


def completion(rows: List[Dict[str, Any]], cfg: Dict[str, Any], gate_phase: Optional[str]) -> Dict[str, Any]:
    """Priority-weighted delivery completion: per phase, and over all rows. Dropped rows are left out (they were
    decided not to be done); owner-gated rows are left out (they are not the plan's to schedule)."""
    per: Dict[str, Dict[str, float]] = {}
    for r in rows:
        if r.get("status") == "dropped" or r.get("owner_gated") is True or r.get("slot") == "OWNER":
            continue
        slot = str(r.get("slot"))
        # a row closed on the retired NEXT queue (before W469) belongs to no phase: it is labelled as what it was, kept
        # out of the overall figure, and scored like every other row — as if in its own gate (refutation: it was halved)
        ph = _phase(slot) if re.match(r"^P\d+\.\d+$", slot) else RETIRED
        s = score_row(r, cfg, _phase(slot), as_open=False)["score"]
        d = per.setdefault(ph, {"closed": 0.0, "open": 0.0, "rows_closed": 0, "rows_open": 0})
        if r.get("status") == "done":
            d["closed"] += s
            d["rows_closed"] += 1
        else:
            d["open"] += s
            d["rows_open"] += 1
    out = {}
    for ph, d in sorted(per.items()):
        total = d["closed"] + d["open"]
        out[ph] = {"weighted_pct": round(100.0 * d["closed"] / total, 1) if total else None,
                   "rows_closed": int(d["rows_closed"]), "rows_open": int(d["rows_open"]),
                   "closed_priority": round(d["closed"], 1), "open_priority": round(d["open"], 1)}
    tc = sum(d["closed"] for ph, d in per.items() if ph != RETIRED)
    to = sum(d["open"] for ph, d in per.items() if ph != RETIRED)
    return {"by_phase": out, "gate_phase": gate_phase,
            "overall_weighted_pct": round(100.0 * tc / (tc + to), 1) if (tc + to) else None}
