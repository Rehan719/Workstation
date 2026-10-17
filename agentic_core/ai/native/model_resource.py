"""
Model Resource Registry — the native AI fabric's catalogue of usable model resources.

Honest, in-house-first enumeration:
  - native  (always)         : Workstation's own structured engine (the floor).
  - ollama  (local/self-hosted): used when a local Ollama server is reachable — OWNED capability.
  - anthropic / openai (external): OPTIONAL accelerants, available ONLY when a key is present AND
                                   AI_ALLOW_EXTERNAL=true. Never a dependency.

The registry never makes Workstation depend on an external provider: with no key / flag off and no
local model, the `native` resource still serves. `select()` returns resources in-house-first.
"""
from __future__ import annotations

import os
import time
from typing import Dict, List, Optional

_OLLAMA_CACHE = {"at": 0.0, "up": False}
_OLLAMA_TTL = 30.0


def external_allowed() -> bool:
    """External providers are opt-in accelerants only."""
    return os.getenv("AI_ALLOW_EXTERNAL", "false").lower() == "true"


def _ollama_base() -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    return url.rsplit("/api/", 1)[0] if "/api/" in url else url


def ollama_up() -> bool:
    """Probe the local Ollama server (cached). Owned/self-hosted, no external dependency.

    Set AI_DISABLE_LOCAL=1 to skip the local model entirely and resolve straight to the native
    floor — used under the test suite so it doesn't wait on real local inference (and available
    to any deployment that wants the deterministic native path)."""
    if os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes"):
        return False
    now = time.monotonic()
    if now - _OLLAMA_CACHE["at"] < _OLLAMA_TTL:
        return _OLLAMA_CACHE["up"]
    up = False
    try:
        import httpx
        r = httpx.get(f"{_ollama_base()}/api/tags", timeout=1.0)
        # A server that merely responds is not enough — it must have a model pulled, or it
        # cannot serve a completion. Requiring a model avoids burning the per-call read
        # timeout on a server that will only fail, keeping the in-house path snappy.
        up = r.status_code == 200 and bool(r.json().get("models"))
    except Exception:
        up = False
    _OLLAMA_CACHE.update(at=now, up=up)
    return up


_MODELS_CACHE = {"at": 0.0, "models": []}


def local_models() -> List[str]:
    """Discover the local models actually pulled into the Ollama server (cached). Each is an OWNED, composable
    model resource the user can route to by name. Empty under AI_DISABLE_LOCAL or when Ollama is unreachable."""
    if os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes"):
        return []
    now = time.monotonic()
    if now - _MODELS_CACHE["at"] < _OLLAMA_TTL:
        return list(_MODELS_CACHE["models"])
    models: List[str] = []
    try:
        import httpx
        r = httpx.get(f"{_ollama_base()}/api/tags", timeout=1.0)
        if r.status_code == 200:
            models = [m.get("name", "").split(":")[0] if ":latest" in m.get("name", "") else m.get("name", "")
                      for m in (r.json().get("models") or [])]
            models = sorted({m for m in models if m})
    except Exception:
        models = []
    _MODELS_CACHE.update(at=now, models=models)
    return models


# ── Owned-model LIFECYCLE (W276) — the registry is a managed estate, not a static enumeration:
# the Owner can EVALUATE a discovered local model, PROMOTE one to be the serving default (persisted,
# not env-only), and RETIRE/REINSTATE models. State is a small persisted document; every transition
# is UEG-logged at the API layer. Honest: promotion requires the model to be genuinely discovered.
def _lifecycle_path():
    from agentic_core.config import data_path
    return data_path("model_lifecycle.json")


#  FU-894 (W745) - THE CAP ON KEPT EVALUATIONS HAS A NAME, SO A READER CAN STATE IT. `save_lifecycle` keeps the
#  newest this many and drops older ones; GET /api/v1/native-ai/lifecycle says how many the record holds against
#  it. (The baseline store keeps every run: a baseline is the evidence record; an evaluation is a smoke check.)
#  Read at each call, so the figure in a basis is this constant and never a number typed beside it.
EVALUATIONS_KEPT = 50


def evaluations_held_basis(held: int, incomplete: Optional[str] = None) -> str:
    """How many evaluations the record holds against the cap, in one sentence computed from the two numbers. A
    record that could not be read whole says so first: its count is only what was read (W577)."""
    cap = EVALUATIONS_KEPT
    if incomplete:
        return (f"the lifecycle record could not be read whole ({str(incomplete)[:120]}), so {held} evaluation(s) "
                f"were read and others may be missing; the store keeps at most {cap}")
    if held >= cap:
        return (f"the record holds {held} evaluation(s), which reaches the cap of {cap}: the store keeps the newest "
                f"{cap} and drops the oldest when one is added, so older evaluations may have been dropped. A "
                f"dropped evaluation is not in this record and is not counted here")
    return (f"every evaluation recorded is held: {held}, under the cap of {cap} beyond which the oldest are "
            f"dropped")


def lifecycle_state(strict: bool = False) -> Dict:
    """The model lifecycle record. `strict=True` REFUSES an unreadable store, for a writer.

    W577 (FU-395) — the four lifecycle writers (evaluate · promote · retire · reinstate) each took
    this value and handed it to `save_lifecycle`. A tolerant read recovers the store's first complete
    JSON value and discards the rest, so any of them could persist a prefix and silently drop the
    retired list and the evaluation history — on the very record whose purpose is to say which models
    were retired and why. A writer reads strictly and refuses; readers stay tolerant.
    """
    from agentic_core.config import StoreUnavailable, read_json_reported, read_json_strict
    if strict:
        st = read_json_strict(_lifecycle_path(), {}, expect=dict) or {}
        _why = None
    else:
        st, _why = read_json_reported(_lifecycle_path(), {})
        st = st if isinstance(st, dict) else {}
    st.setdefault("default_local", None)     # promoted default (None → the OLLAMA_MODEL env default)
    st.setdefault("retired", [])
    st.setdefault("evaluations", [])
    # W577 (FU-298) — a reader that prints "no models retired" must be able to tell that from
    # "the record of retirements could not be read". The reason rides on the record itself.
    st["store_incomplete"] = _why
    return st


def save_lifecycle(st: Dict) -> None:
    from agentic_core.config import atomic_write_json
    st["evaluations"] = (st.get("evaluations") or [])[-EVALUATIONS_KEPT:]
    # W577 — `store_incomplete` describes THIS READ, not the record. Persisting it would store a
    # transient fact about one request as if it were part of the lifecycle, and the next reader would
    # take a stale reason for a live one. Popped here, at the single write point, so none of the four
    # writers has to remember to.
    st.pop("store_incomplete", None)
    atomic_write_json(_lifecycle_path(), st)


def effective_default_local() -> Optional[str]:
    """The local model the 'ollama' resource would serve with: the PROMOTED default when set (and not
    retired), else the OLLAMA_MODEL env name IF that model is actually present.

    W492 (FU-183) — this returned the env fallback string unconditionally, so with no model installed
    at all it answered 'llama3.2' and /lifecycle published that as `effective_default`. The Native-AI
    page then said "Serving default: llama3.2 (env default)" beside its own "Deterministic floor
    active" — a name for something serving nothing. A default that is not present is not a default:
    None means the floor serves, and the caller must say so. `configured_default_local()` below still
    exposes the env NAME for surfaces that want to show what is configured but absent."""
    # W492 (refutation) - the round's first fix presence-checked only the ENV branch, so a PROMOTED
    # model that had since been uninstalled was still returned as what serves, and /lifecycle asserted
    # "<model> is installed and serves local calls" about a model that is gone. Presence is the same
    # requirement for both branches.
    st = lifecycle_state()
    _present = set(active_local_models())
    promoted = st.get("default_local")
    if promoted and promoted not in set(st.get("retired") or []) and promoted in _present:
        return promoted
    env_name = configured_default_local()
    return env_name if env_name and env_name in _present else None


def configured_default_local() -> Optional[str]:
    """The model NAME configured by OLLAMA_MODEL, whether or not it is installed. Naming what is
    configured is honest; presenting it as what serves is not."""
    return os.getenv("OLLAMA_MODEL", "llama3.2") or None


def active_local_models() -> List[str]:
    """Discovered local models MINUS retired ones — what default orchestration may draw on.
    (Explicit ollama:<name> routing remains the user's explicit choice, retired or not.)"""
    retired = set(lifecycle_state().get("retired") or [])
    return [m for m in local_models() if m not in retired]


# -- P3.32 (W745) - THE INSTALLED MODELS, DESCRIBED BY THE RUNTIME THAT HOLDS THEM ------------------------------
#  Name, digest, size, parameter size, quantisation, family and format come from the runtime's list (GET
#  /api/tags); the licence text, the parameter count and the capabilities from its description of each model
#  (POST /api/show). NOTHING HERE IS TYPED: a field the runtime does not report is None and is named under
#  `not_reported`, never filled in from what a model of that name usually is. Read at each call and cached
#  nowhere, because a tag can be pulled again to a different build. The runtime is asked to list and to describe;
#  nothing here asks it to pull, push, copy, create or delete a model.
#  Timeouts: 10 s to list and 20 s per description. Measured live on the Owner's machine while this was prepared,
#  a cold list took 4.9 s and a cold description 9.2 s; at 2 s and 5 s the first read came back NOT READ.
_LISTED_FIELDS = ("digest", "size_bytes", "parameter_size", "quantization_level", "family", "format")
_DESCRIBED_FIELDS = ("parameter_count", "capabilities", "licence")


def describe_installed(show: bool = True) -> Dict:
    """The local models as the local runtime describes them, read now. Three outcomes, never folded together:
    READ (each model with the runtime's own fields; an empty list means the runtime holds none), NOT READ because
    the local runtime is disabled here, and NOT READ because it did not answer. Not read is not nothing installed.
    `show=False` lists without describing each model (the candidate register needs only the names)."""
    import hashlib
    at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    base = _ollama_base()
    if os.getenv("AI_DISABLE_LOCAL", "").lower() in ("1", "true", "yes"):
        return {"read": False, "read_at": at, "read_from": None, "models": [],
                "basis": ("NOT READ: AI_DISABLE_LOCAL is set, so the local runtime is not asked. This says "
                          "nothing about what is installed on this machine")}
    try:
        import httpx
        r = httpx.get(f"{base}/api/tags", timeout=10.0)
        if r.status_code != 200:
            raise ValueError(f"HTTP {r.status_code}")
        listed = (r.json() or {}).get("models")
        if not isinstance(listed, list):
            raise ValueError("the answer holds no model list")
    except Exception as e:                                   # noqa: BLE001 - said, never read as an empty list
        return {"read": False, "read_at": at, "read_from": f"{base}/api/tags", "models": [],
                "basis": (f"NOT READ: the local runtime at {base} did not give its model list "
                          f"({e.__class__.__name__}: {str(e)[:80]}). This says nothing about what is installed")}
    models: List[Dict] = []
    for m in listed:
        if not isinstance(m, dict) or not str(m.get("name") or m.get("model") or ""):
            continue
        name = str(m.get("name") or m.get("model"))
        det = m.get("details") if isinstance(m.get("details"), dict) else {}
        size = m.get("size")
        row = {"name": name,
               #  the name this platform routes by: `local_models()` drops a ":latest" tag the same way
               "routing_name": name.split(":")[0] if ":latest" in name else name,
               "digest": m.get("digest") or None,
               "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) else None,
               "parameter_size": det.get("parameter_size") or None,
               "quantization_level": det.get("quantization_level") or None,
               "family": det.get("family") or None,
               "format": det.get("format") or None,
               "modified_at": m.get("modified_at") or None,
               "parameter_count": None, "capabilities": None, "licence": None,
               "show_read": False,
               "show_basis": None if show else "not asked: this read lists the models and describes none of them"}
        if show:
            try:
                s = httpx.post(f"{base}/api/show", json={"model": name}, timeout=20.0)
                if s.status_code != 200:
                    raise ValueError(f"HTTP {s.status_code}")
                sj = s.json() or {}
                info = sj.get("model_info") if isinstance(sj.get("model_info"), dict) else {}
                pc = info.get("general.parameter_count")
                row["parameter_count"] = pc if isinstance(pc, int) and not isinstance(pc, bool) else None
                caps = sj.get("capabilities")
                row["capabilities"] = [str(c) for c in caps] if isinstance(caps, list) and caps else None
                lic = sj.get("license")
                if isinstance(lic, list):
                    lic = "\n".join(str(x) for x in lic)
                if isinstance(lic, str) and lic.strip():
                    row["licence"] = {
                        "first_line": next(ln.strip() for ln in lic.splitlines() if ln.strip())[:200],
                        "chars": len(lic), "sha256": hashlib.sha256(lic.encode("utf-8")).hexdigest(),
                        "basis": ("the licence text the runtime holds for this model: its first line, its length "
                                  "and its hash. It is not a reading of what the licence permits")}
                row["show_read"] = True
            except Exception as e:                           # noqa: BLE001 - said on the row
                row["show_basis"] = (f"the runtime's description of {name} could not be read "
                                     f"({e.__class__.__name__}: {str(e)[:80]}), so its licence, parameter count "
                                     f"and capabilities are not known")
        _asked = _LISTED_FIELDS + _DESCRIBED_FIELDS if row["show_read"] else _LISTED_FIELDS
        row["not_reported"] = [f for f in _asked if row.get(f) is None]
        models.append(row)
    return {"read": True, "read_at": at,
            "read_from": f"{base}/api/tags" + (f" and {base}/api/show for each model" if show else ""),
            "models": models,
            "basis": (f"{len(models)} model(s), as the local runtime at {base} "
                      f"{'listed and described' if show else 'listed'} them at {at}. Every field is the runtime's "
                      f"own; a field it did not report is null and named under not_reported, never filled in"
                      + ("" if models else ". The runtime answered and lists no model"))}


# -- P3.32 (W745) - CANDIDATES ARE REGISTERED, NOT DOWNLOADED ---------------------------------------------------
#  Research leads, each with the licence the research named. They live HERE, beside the lifecycle record, and
#  not in that record's file: the file is per machine and untracked, and a lead is a fact the code must carry
#  everywhere. What IS per machine - whether a lead is downloaded and whether it was evaluated - is never written
#  on a lead: `candidate_register` reads both from the runtime's list and the stored records each time it is asked,
#  and whether a lead is the configured default from the configured model name. Registering a lead downloads
#  nothing. Downloading one is the Owner's decision.
CANDIDATE_LEADS_RECORDED = "2026-10-16"
CANDIDATE_LEADS = (
    {"id": "qwen3.5-4b", "name": "Qwen3.5-4B", "licence": "Apache-2.0", "runtime_tag": "qwen3.5:4b-q4_K_M",
     "notes": "multimodal; the runtime library lists its 4-bit build (qwen3.5:4b-q4_K_M) at 3.3 GB"},
    {"id": "qwen3.5-2b", "name": "Qwen3.5-2B", "licence": "Apache-2.0", "runtime_tag": None,
     "notes": "multimodal; about 2B parameters by its name; no file size and no runtime tag were recorded for it"},
    {"id": "qwen3.5-0.8b", "name": "Qwen3.5-0.8B", "licence": "Apache-2.0", "runtime_tag": None,
     "notes": "multimodal; about 0.8B parameters by its name; no file size and no runtime tag were recorded for it"},
    {"id": "qwen3-4b-instruct-2507", "name": "Qwen3-4B-Instruct-2507", "licence": "Apache-2.0", "runtime_tag": None,
     "notes": "about 4B parameters by its name; no file size and no runtime tag were recorded for it"},
    {"id": "phi-4-mini-instruct", "name": "Phi-4-mini-instruct", "licence": "MIT", "runtime_tag": None,
     "notes": "its published model code is custom and needs trust_remote_code to load"},
    {"id": "gemma-4-e2b-it", "name": "Gemma-4-E2B-it", "licence": "Apache-2.0", "runtime_tag": None,
     "notes": ("10.2 GB as published, in one file, with 5.1B parameters in total: a file that size may not fit in "
               "a small machine's memory, so compare it with this machine's memory (GET /api/v1/native-ai/inventory "
               "measures it) before any download")},
    {"id": "qwen2.5-coder-3b", "name": "Qwen2.5-Coder-3B", "licence": "a research-only licence", "runtime_tag": None,
     "notes": "NOT for commercial use: its licence is for research only"},
    {"id": "llama-3.2", "name": "Llama 3.2", "licence": "Llama 3.2 Community License", "runtime_tag": "llama3.2",
     "notes": ("the licence carries attribution and naming duties. An installed build's own licence text is read "
               "from the runtime: GET /api/v1/native-ai/lifecycle/installed")},
)


def _tag_forms(tag) -> set:
    """The names one runtime tag can appear under: a bare name and its ':latest' are the same model."""
    t = str(tag or "").strip()
    if not t:
        return set()
    if t.endswith(":latest"):
        return {t, t[: -len(":latest")]}
    return {t} if ":" in t else {t, f"{t}:latest"}


def candidate_register(installed: Dict, evaluations: List, baselines: List,
                       evaluations_incomplete: Optional[str] = None,
                       baselines_incomplete: Optional[str] = None,
                       configured: Optional[str] = None) -> Dict:
    """Each lead, with DOWNLOADED and EVALUATED read from what is passed in: the runtime's list (from
    `describe_installed`) and the stored evaluation and baseline records; and whether it is the CONFIGURED DEFAULT,
    from the configured model name passed in. Three states each - True, False, or None with the reason it cannot
    be told. A PURE function: the route reads the runtime, the stores and the configuration, and this only
    compares, so every state can be driven."""
    inst = installed if isinstance(installed, dict) else {}
    read = inst.get("read") is True
    present = set()
    for m in inst.get("models") or []:
        if isinstance(m, dict):
            present |= {str(m.get("name") or ""), str(m.get("routing_name") or "")}
    present.discard("")
    evs = [e for e in (evaluations or []) if isinstance(e, dict)]
    bls = [b for b in (baselines or []) if isinstance(b, dict)]
    capped = len(evs) >= EVALUATIONS_KEPT
    cfg_forms = _tag_forms(configured)
    leads = []
    for lead in CANDIDATE_LEADS:
        tag = lead.get("runtime_tag")
        forms = _tag_forms(tag)
        if not forms:
            dl, dl_why = None, ("NOT CHECKED: no runtime tag is recorded for this lead, so the runtime's list "
                                "cannot be matched against it")
        elif not read:
            dl, dl_why = None, f"NOT CHECKED: {inst.get('basis') or 'the local runtime was not read'}"
        elif forms & present:
            dl, dl_why = True, f"{tag} is in the local runtime's list read at {inst.get('read_at')}"
        else:
            dl, dl_why = False, f"{tag} is not in the local runtime's list read at {inst.get('read_at')}"
        if not forms:
            ev, ev_why = None, ("NOT CHECKED: an evaluation names a runtime model, and no runtime tag is recorded "
                                "for this lead")
        else:
            named_e = [e for e in evs if str(e.get("model") or "") in forms]
            named_b = [b for b in bls if str(b.get("tier") or "") in {f"ollama:{f}" for f in forms}]
            served = (sum(1 for e in named_e if e.get("can_serve") is True)
                      + sum(1 for b in named_b if b.get("served_target") is True))
            if served:
                ev, ev_why = True, (f"{len(named_e)} evaluation(s) and {len(named_b)} baseline run(s) name it, "
                                    f"and it served in {served} of them")
            elif evaluations_incomplete or baselines_incomplete:
                ev, ev_why = None, (f"NOT KNOWN: a store of evaluations or baselines could not be read whole "
                                    f"({str(evaluations_incomplete or baselines_incomplete)[:160]}), so a record of "
                                    f"it may be missing")
            elif capped:
                ev, ev_why = None, (f"NOT KNOWN: no record held shows it serving, and the evaluations held reach the "
                                    f"cap of {EVALUATIONS_KEPT}, so an older one may have been dropped")
            elif named_e or named_b:
                ev, ev_why = False, (f"{len(named_e) + len(named_b)} record(s) name it and in none of them did it "
                                     f"serve, so nothing about it was established")
            else:
                ev, ev_why = False, "no evaluation or baseline run recorded here names it"
        if not forms:
            cd, cd_why = None, ("NOT CHECKED: no runtime tag is recorded for this lead, so it cannot be matched "
                                "against the configured default model name")
        elif not cfg_forms:
            cd, cd_why = None, "NOT CHECKED: no configured default model name was read"
        elif forms & cfg_forms:
            cd, cd_why = True, (f"{tag} is the configured default model name ({configured}), read at this call. "
                                f"Configured is not serving: GET /api/v1/native-ai/lifecycle says what serves")
        else:
            cd, cd_why = False, f"the configured default model name is {configured}, not {tag}"
        dl_word = {True: "downloaded", False: "not downloaded", None: "not known whether downloaded"}[dl]
        ev_word = {True: "evaluated", False: "not evaluated", None: "not known whether evaluated"}[ev]
        leads.append({**lead, "downloaded": dl, "downloaded_basis": dl_why, "evaluated": ev,
                      "evaluated_basis": ev_why, "state": f"{dl_word}, {ev_word}",
                      "configured_default": cd, "configured_default_basis": cd_why,
                      "licence_basis": (f"the licence the research named when the lead was recorded "
                                        f"({CANDIDATE_LEADS_RECORDED}); this platform has not read its text")})
    counts = {"downloaded": sum(1 for x in leads if x["downloaded"] is True),
              "not_downloaded": sum(1 for x in leads if x["downloaded"] is False),
              "not_checked": sum(1 for x in leads if x["downloaded"] is None),
              "evaluated": sum(1 for x in leads if x["evaluated"] is True)}
    return {"leads": leads, "counts": counts, "recorded_on": CANDIDATE_LEADS_RECORDED,
            "download_decision": "Registering a lead downloads nothing. Downloading one is the Owner's decision.",
            "basis": (f"{len(leads)} research lead(s) recorded {CANDIDATE_LEADS_RECORDED}, each with the licence the "
                      f"research named: {counts['downloaded']} downloaded, {counts['not_downloaded']} not "
                      f"downloaded, {counts['not_checked']} not checked; {counts['evaluated']} evaluated. Downloaded "
                      f"is read from the local runtime's list, evaluated from the stored records and the configured "
                      f"default from the configured model name at this call; none of them is written on a lead")}


class ModelResourceRegistry:
    """Catalogue + in-house-first selection of model resources."""

    def available(self) -> List[Dict]:
        ext = external_allowed()
        discovered = local_models()
        st = lifecycle_state()
        rows = [
            {"name": "native", "kind": "native", "available": True, "is_external": False,
             "note": "Workstation's own structured engine — always available, owned."},
            {"name": "ollama", "kind": "local", "available": ollama_up(), "is_external": False,
             # W492 (FU-183) — `model` is what SERVES (null when nothing is installed);
             # `configured_model` is the name that would be tried. Reporting the second as the first
             # named a model that served nothing while the floor answered every call.
             "model": effective_default_local(), "configured_model": configured_default_local(),
             "local_models": discovered,
             "promoted_default": st.get("default_local"), "retired": st.get("retired") or [],
             "note": "Self-hosted local model(s) — owned capability when running. Route to a specific one "
                     "with model='ollama:<name>'."},
            {"name": "anthropic", "kind": "external", "available": bool(os.getenv("ANTHROPIC_API_KEY")) and ext,
             "is_external": True, "model": os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6"),
             "note": "Optional accelerant — only with a key AND AI_ALLOW_EXTERNAL=true."},
            {"name": "openai", "kind": "external", "available": bool(os.getenv("OPENAI_API_KEY")) and ext,
             "is_external": True, "model": "gpt-4o-mini",
             "note": "Optional accelerant — only with a key AND AI_ALLOW_EXTERNAL=true."},
        ]
        return rows

    def select(self, prefer_external: bool = False) -> List[str]:
        """Return resource names to try, IN-HOUSE FIRST (local owned model → native floor →
        external accelerants only if allowed). External is never tried unless explicitly allowed."""
        avail = {r["name"]: r for r in self.available()}
        order: List[str] = []
        if avail["ollama"]["available"]:
            order.append("ollama")            # owned, self-hosted, real model — preferred
        # external accelerants only if allowed; placed AFTER owned local unless prefer_external
        externals = [n for n in ("anthropic", "openai") if avail[n]["available"]]
        if prefer_external and externals:
            order = externals + order
        order.append("native")                # the always-available owned floor
        if not prefer_external:
            order += externals                # accelerants last (only if allowed)
        # de-dupe, keep order
        seen, final = set(), []
        for n in order:
            if n not in seen:
                seen.add(n); final.append(n)
        return final


registry = ModelResourceRegistry()
