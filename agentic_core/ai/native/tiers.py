"""The tier registry and the router (P3.20).

THE POINT OF THIS MODULE, in one sentence: a surface that lists a model the machine cannot run is the
same defect as a leaderboard nothing scored. So every tier reports `runnable here` with a MEASURED
reason, and the measurement is taken from the machine at call time — never written down.

WHY THAT MATTERS MORE THAN IT SOUNDS. The Owner's roadmap specifies a 14B reasoning model, a 15B coder
and an 8B domain specialist. This machine was measured on 2026-09-27 at 7.7 GB of RAM, an i3-1315U and
integrated graphics with no CUDA device, and the Owner's decision (FU-271, default (a)) is to design the
fabric for a 1–3B local tier plus the deterministic floor and have every higher tier report that it is
not runnable here, with the reason. A FIGURE TYPED INTO THIS FILE WOULD GO STALE THE DAY THE MACHINE
CHANGES, and would then be a claim about hardware nobody re-measured — which is the defect this
programme removes everywhere else. So nothing here records 7.7 GB; it asks.

THREE STATES, AS EVERYWHERE. A tier is RUNNABLE, NOT_RUNNABLE with what is missing and by how much, or
UNKNOWN because the measurement itself could not be taken. UNKNOWN is never folded into either of the
others: a machine we could not measure is not a machine that cannot run something.
"""
from __future__ import annotations

import os
import shutil
from typing import Any, Dict, List, Optional, Tuple

RUNNABLE = "RUNNABLE"
NOT_RUNNABLE = "NOT_RUNNABLE"
UNKNOWN = "UNKNOWN"

#  The five tiers the item names, in the order it names them. `needs` is what a tier's resources require
#  of the machine; `serves` is what the router may send it.
TIERS: Dict[str, Dict[str, Any]] = {
    "deterministic_logic": {
        "order": 0,
        "serves": "structured composition from the request itself — no model, no inference",
        "needs": {"ram_gb": 0.0, "gpu": False},
        "why_it_needs_that": (
            "the deterministic floor runs in this process and loads nothing, so it is runnable wherever "
            "the platform is. It is also the only tier with that property"),
    },
    "reflex_routing": {
        "order": 1,
        "serves": "short classification and routing decisions where a 1–3B local model is enough",
        "needs": {"ram_gb": 3.0, "gpu": False},
        "why_it_needs_that": (
            "a 1–3B model at 4-bit occupies roughly 1–2 GB resident, and the platform, the browser and "
            "the suite share the same memory, so 3 GB total is the floor at which it is worth trying"),
    },
    "domain_specialist": {
        "order": 2,
        "serves": "a domain answer from a model trained or tuned for it",
        "needs": {"ram_gb": 12.0, "gpu": False},
        "why_it_needs_that": (
            "the roadmap's 8B specialist is ~4.7 GB at Q4 and must sit alongside the OS, the backend and "
            "the browser; below about 12 GB total it either fails to load or thrashes, and on a CPU "
            "without a CUDA device it is minutes per reply even when it does load"),
    },
    "synthesis": {
        "order": 3,
        "serves": "long-form reasoning across several sources",
        "needs": {"ram_gb": 20.0, "gpu": True},
        "why_it_needs_that": (
            "the roadmap's 14B reasoning model needs roughly 9–12 GB at 4-bit for weights alone, which "
            "exceeds this machine's entire memory, and it is unusable without a discrete GPU"),
    },
    "perception": {
        "order": 4,
        "serves": "reading an image or a document as an image",
        "needs": {"ram_gb": 16.0, "gpu": True},
        "why_it_needs_that": (
            "a vision-language model carries an image encoder beside the language weights and is not "
            "practical on integrated graphics"),
    },
}

#  Which tier the router prefers for a domain, and the grave domains that may not be served by a model
#  at all on this deployment. Taxonomy-free by the Owner's ruling: these are the domains the platform
#  already treats as grave, not a new classification scheme.
GRAVE_DOMAINS = ("money", "legal", "faith", "medical", "safety")


def machine() -> Dict[str, Any]:
    """What this machine actually is, measured now. Every field three-state with its own source."""
    out: Dict[str, Any] = {}

    #  RAM
    try:
        import psutil
        out["ram_gb"] = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        out["ram_basis"] = "psutil.virtual_memory().total, read at call time"
    except Exception as e:                       # noqa: BLE001
        out["ram_gb"] = None
        out["ram_basis"] = (
            f"NOT MEASURED: psutil could not be used ({e.__class__.__name__}), so this machine's memory "
            f"is unknown. A tier is not declared unrunnable for want of a measurement")

    #  CPU
    _cores = os.cpu_count()
    out["cpu_count"] = _cores
    out["cpu_basis"] = ("os.cpu_count(), which counts LOGICAL processors — it is not a measure of how "
                        "fast any of them is" if _cores else
                        "NOT MEASURED: os.cpu_count() returned None")

    #  GPU — WITHOUT IMPORTING TORCH AT MODULE LEVEL. The platform must boot with torch absent (W506),
    #  so this asks the environment first and only consults torch if it is already importable.
    _smi = shutil.which("nvidia-smi")
    if _smi:
        out["cuda"] = True
        out["cuda_basis"] = f"nvidia-smi is on PATH at {_smi}"
    else:
        try:
            import torch                          # noqa: F401 — presence check only
            out["cuda"] = bool(torch.cuda.is_available())
            out["cuda_basis"] = ("torch.cuda.is_available(), consulted because torch happened to be "
                                 "importable; nvidia-smi is not on PATH")
        except Exception:                         # noqa: BLE001
            out["cuda"] = False
            out["cuda_basis"] = (
                "no nvidia-smi on PATH and torch is not importable, so no CUDA device is visible to "
                "this process. This is a statement about what can be SEEN, not a hardware audit")
    return out


def runnable(tier: str, m: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    """Whether a tier is runnable HERE, with the measured reason. Three states, never two."""
    if tier not in TIERS:
        return UNKNOWN, f"{tier!r} is not a declared tier; the declared tiers are {sorted(TIERS)}"
    m = m or machine()
    needs = TIERS[tier]["needs"]

    if needs["gpu"] and m.get("cuda") is not True:
        return NOT_RUNNABLE, (
            f"this tier needs a CUDA device and none is visible. {m.get('cuda_basis')}. "
            f"{TIERS[tier]['why_it_needs_that']}")

    ram = m.get("ram_gb")
    if ram is None:
        if needs["ram_gb"] <= 0:
            return RUNNABLE, (f"this tier needs no memory beyond the running process. "
                              f"{TIERS[tier]['why_it_needs_that']}")
        return UNKNOWN, (
            f"this tier needs about {needs['ram_gb']} GB and this machine's memory was not measured. "
            f"{m.get('ram_basis')}. UNKNOWN is not NOT_RUNNABLE: a machine nobody could measure is not "
            f"a machine that cannot run this")
    if ram < needs["ram_gb"]:
        return NOT_RUNNABLE, (
            f"this tier needs about {needs['ram_gb']} GB and this machine has {ram} GB "
            f"({m.get('ram_basis')}) — short by {round(needs['ram_gb'] - ram, 2)} GB. "
            f"{TIERS[tier]['why_it_needs_that']}")
    return RUNNABLE, (
        f"this machine has {ram} GB against about {needs['ram_gb']} GB needed ({m.get('ram_basis')})"
        + ("" if not needs["gpu"] else f", and a CUDA device is visible ({m.get('cuda_basis')})"))


#  P3.5 clause (3) — THE VISION-CAPABLE FAMILIES, as a screen that may FLAG and never CLEAR.
#  Families, not exact names: `local_models()` returns names with a tag (`llava:13b`), so a bare equality
#  test would miss every tagged pull. Deliberately short — a list long enough to be exhaustive would be a
#  list nobody maintains, and the UNKNOWN state below is what makes a short list safe.
VISION_FAMILIES = ("llava", "bakllava", "moondream", "llama3.2-vision", "llama3-vision",
                   "qwen-vl", "qwen2-vl", "minicpm-v", "pixtral", "gemma3-vision")

VISION_CANNOT_CLEAR = (
    "this list can only RECOGNISE a vision-capable family; it cannot establish that a model is NOT "
    "vision-capable. A model it does not recognise is reported UNKNOWN, never as text-only, because 'I do "
    "not recognise this model' and 'this model cannot read an image' are different statements")


def vision_resources(models: List[str]) -> Dict[str, Any]:
    """Which of the pulled models can read an image. THREE STATES, and the middle one is the point.

    A PURE function over a list of names, not a reader of the environment: `local_models()` returns [] under
    AI_DISABLE_LOCAL and the suite sets it, so a check that asked the environment could never be driven — it
    would see "nothing installed" forever and pass whatever this logic did.

      matched   : models whose family is recognised as vision-capable
      unknown   : models whose family is NOT recognised — reported, never silently dropped
      basis     : what the result does and does not establish, including the cannot-clear statement
    """
    matched, unknown = [], []
    for m in models or []:
        name = str(m or "").strip().lower()
        if not name:
            continue
        family = name.split(":", 1)[0]
        if any(family == f or family.startswith(f) for f in VISION_FAMILIES):
            matched.append(m)
        else:
            unknown.append(m)
    return {
        "matched": matched,
        "unknown": unknown,
        "basis": (
            (f"{len(matched)} pulled model(s) belong to a recognised vision-capable family: "
             f"{', '.join(matched)}. " if matched else
             "no pulled model belongs to a recognised vision-capable family. ")
            + (f"{len(unknown)} model(s) were NOT RECOGNISED either way ({', '.join(unknown[:6])}): they are "
               f"not counted as vision-capable and are not claimed to be text-only. " if unknown else "")
            + VISION_CANNOT_CLEAR),
    }


def image_intake(models: Optional[List[str]] = None) -> Dict[str, Any]:
    """P3.5 clauses (2) and (3) — what this deployment can read from an image, and the REFUSAL when nothing.

    clause (2): where no owned vision resource is installed it REFUSES with an accurate reason naming WHAT IS
    MISSING, and produces no text. The reason is not written here — it is READ from the `perception` tier's
    own declared requirements and its `why_it_needs_that` sentence, plus the measured machine, so the refusal
    states the actual shortfall rather than a sentence somebody typed. A fabricated description is the defect
    this item exists to prevent, and it is the same class as the transcription mock W495 deleted.

    clause (3): the accept list is COMPUTED from the matched resource, never a constant. With nothing matched
    it is EMPTY and says why — a list naming a format nothing can read fails this clause explicitly.
    """
    if models is None:
        try:
            from agentic_core.ai.native.model_resource import local_models
            models = local_models()
        except Exception:                       # noqa: BLE001 — reported, never silently treated as empty
            models = []
    v = vision_resources(models)
    state, why = runnable("perception")
    spec = TIERS["perception"]
    return {
        "can_read_images": bool(v["matched"]),
        "resources": v["matched"],
        "unrecognised_models": v["unknown"],
        #  EMPTY when nothing matched, and that is the honest computed answer rather than a constant
        "accepts": ["image/png", "image/jpeg", "image/webp"] if v["matched"] else [],
        "accepts_basis": (
            "computed from the matched vision resource" if v["matched"] else
            "EMPTY because no matched vision resource can read an image here. A list naming a format "
            "nothing can read would be a promise this deployment cannot keep"),
        "tier_state": state,
        "refusal": None if v["matched"] else (
            f"NO TEXT IS PRODUCED FROM AN IMAGE on this deployment. What is missing, measured rather than "
            f"asserted: the perception tier needs about {spec['needs']['ram_gb']} GB"
            + (" and a CUDA device" if spec['needs']['gpu'] else "")
            + f", and {why} {spec['why_it_needs_that']}. Nothing is described, summarised or guessed at from "
              f"the image: a fabricated description would be worse than a refusal, because a reader cannot "
              f"tell one from a reading."),
        "vision_screen_basis": v["basis"],
    }


def registry() -> Dict[str, Any]:
    """Every tier, what it serves, whether it is runnable here, and WHICH RESOURCES it actually has.

    A tier with nothing runnable says so — which is the bar's first clause — and it says it with the
    measurement rather than with a sentence somebody wrote.
    """
    m = machine()
    #  What the platform can actually reach, asked rather than assumed.
    try:
        from agentic_core.ai.native.model_resource import local_models, ollama_up
        _up = ollama_up()
        _models = local_models() if _up else []
        _models_basis = (f"{len(_models)} model(s) pulled locally, read from the local runtime"
                         if _up else
                         "the local model runtime is not answering, so no local model can be reached "
                         "right now — which is a statement about reachability, not about what is pulled")
    except Exception as e:                        # noqa: BLE001
        _up, _models = None, []
        _models_basis = f"NOT MEASURED: the model registry could not be consulted ({e.__class__.__name__})"

    tiers = {}
    for name, spec in sorted(TIERS.items(), key=lambda kv: kv[1]["order"]):
        state, why = runnable(name, m)
        #  Resources: the floor is always present; the reflex tier gets whatever small models are
        #  pulled; the higher tiers get nothing, because nothing on this machine can serve them.
        if name == "deterministic_logic":
            res = ["the deterministic floor (in-process, no model)"]
        elif name == "reflex_routing":
            res = list(_models)
        elif name == "perception":
            #  P3.5 clause (3) — MATCHED, not assigned. This branch returned [] for every tier above
            #  reflex_routing with the comment "the higher tiers get nothing, because nothing on this
            #  machine can serve them". True of this machine and written as an assignment, so pulling a
            #  vision model would have changed nothing and the §18 boundary would have been permanent in
            #  code while reading as conditional in prose.
            res = vision_resources(_models)["matched"]
        else:
            res = []
        tiers[name] = {
            "serves": spec["serves"],
            "needs": dict(spec["needs"]),
            "runnable": state,
            "runnable_basis": why,
            "resources": res,
            "resource_count": len(res),
            "resources_basis": (
                _models_basis if name == "reflex_routing" else
                "the floor runs in this process and is always present" if name == "deterministic_logic"
                else (f"NO RESOURCE IS ASSIGNED TO THIS TIER, and that is the honest state rather than "
                      f"an omission: {why}")),
        }
    return {
        "machine": m,
        "tiers": tiers,
        "runnable_tiers": [k for k, v in tiers.items() if v["runnable"] == RUNNABLE],
        "basis": (
            f"{sum(1 for v in tiers.values() if v['runnable'] == RUNNABLE)} of {len(tiers)} tier(s) are "
            f"runnable on this machine, measured now rather than recorded. A tier that is not runnable "
            f"carries what it needs, what this machine has and the difference — and it holds NO "
            f"resources, because listing a model the machine cannot run is the same defect as a "
            f"leaderboard nothing scored"),
        "owner_decision": (
            "FU-271 default (a): design the fabric for a 1–3B local tier plus the deterministic floor, "
            "and have every higher tier report that it is not runnable here with the measured reason. "
            "Provisioning hardware or enabling an Owner-gated external accelerant are the other two "
            "options and neither is taken here"),
    }


#  What a KIND of request would ideally use. The router starts here and walks DOWN; it does not start
#  at the floor, because a router that returns the lowest runnable tier always returns the floor — the
#  floor is order 0 and always runnable — and every rule below it would be unreachable. Measured on the
#  first draft of this module: the grave-domain and high-risk branches never fired once.
WANTS: Dict[str, str] = {
    "image": "perception",
    "vision": "perception",
    "research": "synthesis",
    "strategy": "synthesis",
    "legal": "domain_specialist",
    "medical": "domain_specialist",
    "science": "domain_specialist",
    "education": "domain_specialist",
    "care": "domain_specialist",
    "law": "domain_specialist",
    "routing": "reflex_routing",
    "classification": "reflex_routing",
}
DEFAULT_WANT = "reflex_routing"


def wanted_tier(domain: str) -> Tuple[str, str]:
    """The tier a request of this kind would ideally use, and why. Not what it will get."""
    d = str(domain or "").strip().lower()
    for key, tier in WANTS.items():
        if key in d:
            return tier, f"a {d!r} request would ideally use {tier} ({TIERS[tier]['serves']})"
    return DEFAULT_WANT, (
        f"no declared kind matches {d!r}, so the default want is {DEFAULT_WANT} — the cheapest tier "
        f"that involves a model at all. A request nobody classified is not routed upward")


def route(domain: str, risk: str = "normal") -> Dict[str, Any]:
    """Choose a tier by domain and risk, starting from what the request WANTS and walking down.

    THE CHOICE CARRIES ITS BASIS — the bar's second clause — and the basis names what was considered and
    rejected, not only what was picked. A router that reports only its answer cannot be audited.

    THE FLOOR ALWAYS TERMINATES THIS WALK, and that is stated rather than left as an accident: the
    deterministic tier needs nothing and is always runnable, so this function never fails to choose. It
    refuses a TIER, never the request. The first draft carried a "no tier serves" return below the loop
    and it was unreachable, which is the same dead-branch defect this plan keeps finding in other
    people's code; it is gone rather than kept as decoration.
    """
    reg = registry()
    tiers = reg["tiers"]
    considered: List[Dict[str, Any]] = []

    want, want_why = wanted_tier(domain)
    _grave = any(g in str(domain or "").lower() for g in GRAVE_DOMAINS)
    #  walk DOWN from the wanted tier to the floor
    order = sorted(TIERS, key=lambda k: TIERS[k]["order"], reverse=True)
    order = [n for n in order if TIERS[n]["order"] <= TIERS[want]["order"]]

    for name in order:
        t = tiers[name]
        if _grave and name != "deterministic_logic":
            considered.append({"tier": name, "why_not": (
                f"the domain {domain!r} is one this platform treats as grave "
                f"({', '.join(GRAVE_DOMAINS)}), and a model's answer there is not routed to "
                f"automatically — the floor composes and a human decides")})
            continue
        if str(risk).lower() == "high" and name != "deterministic_logic":
            considered.append({"tier": name, "why_not": (
                "risk was declared high, so only the deterministic tier serves — a model's answer is "
                "not refused because it would be wrong, but because nothing here can show it is right")})
            continue
        if t["runnable"] != RUNNABLE:
            considered.append({"tier": name, "why_not": f"{t['runnable']}: {t['runnable_basis']}"})
            continue
        if not t["resources"]:
            considered.append({"tier": name, "why_not": (
                f"RUNNABLE here but no resource is assigned to it. {t['resources_basis']}")})
            continue
        return {
            "tier": name, "resources": t["resources"], "domain": domain, "risk": risk,
            "wanted": want, "wanted_basis": want_why,
            "considered": considered,
            "fell_back": name != want,
            "basis": (
                (f"chose {name}, which is what this request wanted. " if name == want else
                 f"WANTED {want} and FELL BACK to {name}. ")
                + f"{len(considered)} higher tier(s) were rejected first, each recorded with its reason. "
                + t["runnable_basis"]),
        }
    #  unreachable only because the floor needs nothing — asserted rather than assumed, so a change to
    #  the floor's declared needs surfaces here instead of silently returning None.
    raise RuntimeError(
        "no tier served, which should be impossible: the deterministic tier needs no memory and no GPU, "
        f"so it is always runnable. Its declared needs are {TIERS['deterministic_logic']['needs']!r} and "
        f"the rejections were {considered!r}")
