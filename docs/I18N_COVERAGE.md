# Interface translation coverage — how to check it honestly

The dictionaries live in `lib/i18n.tsx`. `translate()` falls back to English for any missing key, so
**a coverage gap never breaks a screen — it silently shows English.** That is correct behaviour, and
exactly why coverage has to be measured rather than assumed.

Measure it with the survey used in W373 (keys may share a line, so a line-anchored regex undercounts
— that mistake made a fully-populated dictionary look empty):

```bash
python - <<'PY'
import re, pathlib
t = pathlib.Path('apps/workstation-superapp/src/lib/i18n.tsx').read_text(encoding='utf-8')
have = {}
for lang in ('en','ar','fr','es','ur'):
    m = re.search(r'^const ' + lang + r': Dict = \{(.*?)^\};', t, re.S | re.M)
    have[lang] = set(re.findall(r"'([a-zA-Z0-9_.\-]+)'\s*:", m.group(1))) if m else set()
src = pathlib.Path('apps/workstation-superapp/src')
req = set()
for f in src.rglob('*.tsx'):
    x = f.read_text(encoding='utf-8', errors='replace')
    req |= set(re.findall(r"\bt\(\s*'([a-zA-Z0-9_.\-]+)'", x))
    if f.name == 'Sidebar.tsx':                      # nav labels are keyed by item id
        req |= {'nav.' + i for i in re.findall(r"id: '([a-z0-9\-]+)'", x)}
for lang in ('ar','fr','es','ur'):
    missing = sorted(k for k in req if k not in have[lang])
    print(f'{lang}: {len(req)-len(missing)}/{len(req)} covered' + (f' — missing {missing}' if missing else ''))
PY
```

**As of W373: ar/fr/es/ur cover 71/71 requested keys (90 entries each).**

Scope, stated honestly:
- Covered: interface chrome — navigation (every screen), the home surface, the domains hub.
- NOT covered: page bodies beyond those surfaces, and **all AI-generated content** — the in-house
  engine reasons in English. Settings says so to the user rather than implying otherwise.
- Product/proper nouns (VSB, Genesis, CoE, Qur'an Platform, Workstation) are intentionally untranslated.
- RTL: `applyDocumentDirection()` sets `dir`/`lang` on the document for Arabic and Urdu (W370).
