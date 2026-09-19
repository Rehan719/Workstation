"""W477 sweep inventory: every reached frontend surface (pages + components + the shell's packages/ui) with the /api
paths it calls, grouped into shards of similar weight. Deterministic — the coverage is fixed before any agent runs."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("C:/Users/rehan/Workstation")
SRC = ROOT / "apps/workstation-superapp/src"
UI = ROOT / "packages/ui/src"
API_RE = re.compile(r"""['"`](/api/[A-Za-z0-9_\-/{}$.:?=&]+)""")

files = []
for base in (SRC, UI):
    for p in sorted(base.rglob("*.tsx")) + sorted(base.rglob("*.ts")):
        if any(part in ("__tests__", "node_modules", "_archive") for part in p.parts) or p.name.endswith(".d.ts"):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        apis = sorted(set(m.group(1).split("?")[0] for m in API_RE.finditer(t)))
        rel = p.relative_to(ROOT).as_posix()
        # a surface worth sweeping: it calls the API, or it renders figures/status text a user reads
        renders = bool(re.search(r"%|verified|pass|healthy|live|active|synchron|realis|score|certif|compliant|safe", t))
        if apis or (renders and "/pages/" in rel) or rel.startswith("packages/ui/"):
            files.append({"file": rel, "lines": t.count("\n") + 1, "apis": apis})

# group by the directory a user thinks in (pages/<area>, components/<area>, lib, packages/ui)
groups = defaultdict(list)
for f in files:
    parts = f["file"].split("/")
    if "pages" in parts:
        i = parts.index("pages")
        key = "pages/" + (parts[i + 1] if len(parts) > i + 2 else "(root)")
    elif "components" in parts:
        i = parts.index("components")
        key = "components/" + (parts[i + 1] if len(parts) > i + 2 else "(root)")
    elif f["file"].startswith("packages/ui"):
        key = "packages/ui"
    else:
        key = "lib+other"
    groups[key].append(f)

# pack groups into shards of ~equal line weight (a big group is split by file)
TARGET = sum(f["lines"] for f in files) / 14
shards, cur, w = [], [], 0
for key in sorted(groups, key=lambda k: -sum(f["lines"] for f in groups[k])):
    for f in sorted(groups[key], key=lambda f: -f["lines"]):
        cur.append(f)
        w += f["lines"]
        if w >= TARGET:
            shards.append(cur)
            cur, w = [], 0
if cur:
    shards.append(cur)
out = [{"shard": i + 1, "files": [f["file"] for f in s], "lines": sum(f["lines"] for f in s),
        "apis": sorted({a for f in s for a in f["apis"]})} for i, s in enumerate(shards)]
json.dump(out, open("C:/tmp/w477_inventory.json", "w", encoding="utf-8", newline="\n"), indent=1)
print(f"{len(files)} surfaces, {sum(f['lines'] for f in files)} lines, "
      f"{len({a for f in files for a in f['apis']})} distinct /api paths → {len(out)} shards")
for s in out:
    print(f"  shard {s['shard']:2}: {len(s['files']):3} files {s['lines']:6} lines {len(s['apis']):3} apis  e.g. {s['files'][0]}")
