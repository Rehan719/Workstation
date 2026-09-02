"""
IDBO Genome System — genetic encoding of projects and VSB entities.

Each project/entity has a genome: a structured encoding of its core traits
that can be mutated (evolved), crossed over (combined), and expressed
(used to guide AI behaviour).

Genome traits are domain-specific trait vectors that influence how the AI
generates content, selects agents, and prioritises tasks.

  POST /api/v1/organism/genome/encode    — encode a project into a genome
  POST /api/v1/organism/genome/crossover — combine two genomes
  POST /api/v1/organism/genome/mutate    — apply evolution mutation
  GET  /api/v1/organism/genome/{id}      — retrieve a genome
  GET  /api/v1/organism/genome           — list all genomes

W438 honesty pass (see NATIVE_PRIMITIVE_DEFECT_LEDGER.md for the class): every fitness number now
carries fitness_provenance, every encode carries trait_provenance + served_by, and the +0.05
"crossover bonus" — a constant that ratcheted any lineage to fitness 1.0 with nothing evaluated —
is gone. NOTHING in this module evaluates fitness; the fields say so instead of implying selection.
"""
from __future__ import annotations

import json
import re
import time
import uuid
import random
from pathlib import Path
from agentic_core.config import data_path, atomic_write_json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])

_GENOME_STORE = data_path("genomes")
_GENOME_STORE.mkdir(parents=True, exist_ok=True)

# Trait axes — each genome encodes values 0.0–1.0 on these axes
_TRAIT_AXES = [
    "innovation",       # how novel/experimental vs proven/safe
    "commerciality",    # revenue focus vs mission focus
    "complexity",       # simple/focused vs multi-faceted
    "urgency",          # speed to market vs thoroughness
    "scalability",      # local/niche vs global/mass market
    "collaboration",    # solo vs ecosystem/partnership focus
    "regulation",       # compliance-heavy vs light-touch
    "technology",       # high-tech vs low-tech delivery
    "impact",           # incremental vs transformational impact
    "sustainability",   # short-term gains vs long-term sustainability
]

_CROSSOVER_METHODS = ("uniform", "single_point", "adaptive")


def _genome_path(genome_id: str) -> Path:
    return _GENOME_STORE / f"{genome_id}.json"


def _load_genome(genome_id: str) -> dict | None:
    p = _genome_path(genome_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except (json.JSONDecodeError, OSError):
        # a torn/corrupt file is a missing genome (clean 404), not a permanent 500 for this id
        return None


def _save_genome(genome: dict) -> None:
    # W438: repo store convention — a bare write_text can be torn-read by the two concurrent
    # readers (_list_genomes, organism_status._genome_state)
    atomic_write_json(_genome_path(genome["genome_id"]), genome)


def _list_genomes() -> list[dict]:
    result = []
    for p in sorted(_GENOME_STORE.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            g = json.loads(p.read_text())
            result.append({
                "genome_id": g["genome_id"],
                "entity_name": g.get("entity_name", ""),
                "domain": g.get("domain", ""),
                "generation": g.get("generation", 0),
                "fitness_score": g.get("fitness_score", 0.0),
                "fitness_provenance": g.get("fitness_provenance", "unknown (pre-W438 genome)"),
                "encoded": g.get("encoded", None),
                "created_at": g.get("created_at", ""),
            })
        except Exception:
            pass
    return result


@router.get("/genome")
async def list_genomes():
    gs = _list_genomes()
    return {"genomes": gs, "total": len(gs)}


@router.get("/genome/{genome_id}")
async def get_genome(genome_id: str):
    g = _load_genome(genome_id)
    if not g:
        raise HTTPException(status_code=404, detail=f"Genome {genome_id} not found.")
    return g


class EncodeRequest(BaseModel):
    entity_name: str
    domain: str = "general"
    realm: str = "enterprise"
    description: str = ""
    project_id: str = ""


_NUM = re.compile(r"\d*\.?\d+")


@router.post("/genome/encode")
async def encode_genome(req: EncodeRequest):
    """AI-encode a project/entity into a genome trait vector — with the provenance stated.

    W438 — under the deterministic native floor this endpoint used to persist ALL TEN axes and the
    fitness at the constant 0.5 and present it as "The AI analyses the entity" (proven: the floor
    emits section scaffolds, never `axis: value` lines, so every parse silently failed). The genome
    now records which resource served, which axes actually parsed vs defaulted, and whether it was
    encoded at all — a flat all-0.5 vector labelled analysis was the §4.5 class verbatim."""
    prompt = (
        f"You are a genetic encoding system for a Digital Biomimetic Organism. "
        f"Encode the following entity into a genome trait vector.\n\n"
        f"Entity: {req.entity_name}\n"
        f"Domain: {req.domain}\nRealm: {req.realm}\n"
        + (f"Description: {req.description}\n" if req.description else "")
        + f"\nAssign a value 0.0–1.0 for each trait axis:\n"
        + "\n".join(f"  {axis}: <value>" for axis in _TRAIT_AXES)
        + "\n\nOutput ONLY the trait lines in the exact format above. No other text.\n"
        "Then add one line: FITNESS: <overall fitness score 0.0–1.0>\n"
        "Then: EXPRESSION: <one sentence describing the entity's dominant trait expression>"
    )

    # augment=False — W332: generation-class output that PERSISTS never gets cross-request recall
    meta = await gateway.query_meta(prompt, agent="genome_encoder", augment=False)
    raw = meta.get("output") or ""
    served_by = meta.get("served_by", "native")
    is_external = bool(meta.get("is_external"))

    # Parse trait values — tolerant of trailing text ("0.8 (high)"). W438 refuter catches, second
    # round: the deterministic floor COMPOSES ITS OUTPUT FROM THE PROMPT, so any number that
    # survives into a floor-served line is an echo of the request (a digit-bearing domain name, a
    # numeric line in the caller's own description), not a declaration — 72 of 240 swept inputs
    # fabricated a "parsed" trait that way. A floor serve therefore NEVER parses: the floor cannot
    # declare traits, by construction. Real-model serves still guard against echoed scaffold lines.
    traits: dict[str, float] = {}
    fitness: float | None = None
    expression = ""
    floor_served = served_by == "native"

    for line in ([] if floor_served else raw.splitlines()):
        line = line.strip()
        if "<" in line:
            continue   # an echoed scaffold placeholder ("FITNESS: <overall fitness score 0.0-1.0>")
                       # contains digits from the RANGE — never parse a value out of the template
        for axis in _TRAIT_AXES:
            if line.lower().startswith(axis + ":") and axis not in traits:
                m = _NUM.search(line.partition(":")[2])
                if m:
                    traits[axis] = max(0.0, min(1.0, float(m.group(0))))
        if line.lower().startswith("fitness:"):
            m = _NUM.search(line.partition(":")[2])
            if m:
                fitness = max(0.0, min(1.0, float(m.group(0))))
        if line.lower().startswith("expression:"):
            expression = line.partition(":")[2].strip()

    parsed = sorted(traits.keys())
    defaulted = sorted(a for a in _TRAIT_AXES if a not in traits)
    for axis in defaulted:
        traits[axis] = 0.5

    genome_id = f"genome-{uuid.uuid4().hex[:10]}"
    genome = {
        "genome_id": genome_id,
        "entity_name": req.entity_name,
        "domain": req.domain,
        "realm": req.realm,
        "project_id": req.project_id,
        "traits": traits,
        "fitness_score": fitness if fitness is not None else 0.5,
        # honest provenance — the fitness is the MODEL'S self-declared number even when parsed;
        # nothing in this system measures it
        "fitness_provenance": ("ai-declared (unverified)" if fitness is not None
                               else "default-unencoded (no FITNESS line parsed)"),
        "expression": expression,
        "encoded": len(parsed) > 0,
        "trait_provenance": {"parsed": parsed, "defaulted": defaulted},
        "served_by": served_by,
        "is_external": is_external,
        "generation": 0,
        "parent_genomes": [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if not parsed:
        genome["encoding_note"] = ("not encoded — "
                                   + ("the deterministic floor composes from the prompt and cannot "
                                      "declare trait values (its output is never parsed), so "
                                      if floor_served else
                                      f"{served_by} served no parseable trait lines, so ")
                                   + "every axis holds the neutral default 0.5; this vector is NOT "
                                     "an analysis of the entity")
    _save_genome(genome)

    return genome


class CrossoverRequest(BaseModel):
    genome_a_id: str
    genome_b_id: str
    crossover_method: str = "uniform"  # uniform | single_point | adaptive


@router.post("/genome/crossover")
async def crossover_genomes(req: CrossoverRequest):
    """Combine two parent genomes into an offspring — real trait recombination, honest fitness.

    W438 — child fitness used to be mean(parents) + a flat 0.05 "bonus for crossover": a constant
    presented as a measurement that ratcheted ANY lineage to 1.0 in ten generations with nothing
    evaluated. The bonus is deleted; the child's fitness is the parents' mean, labelled
    inherited-mean-unevaluated. An unknown crossover_method used to run the adaptive branch while
    stamping the caller's string verbatim — it now 422s."""
    if req.crossover_method not in _CROSSOVER_METHODS:
        raise HTTPException(status_code=422,
                            detail=f"crossover_method must be one of {list(_CROSSOVER_METHODS)} — "
                                   f"got {req.crossover_method!r}")
    ga = _load_genome(req.genome_a_id)
    gb = _load_genome(req.genome_b_id)

    if not ga:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_a_id} not found.")
    if not gb:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_b_id} not found.")

    traits_a = ga.get("traits") or {}
    traits_b = gb.get("traits") or {}
    child_traits: dict[str, float] = {}

    if req.crossover_method == "uniform":
        # Each trait randomly inherited from one parent
        for axis in _TRAIT_AXES:
            child_traits[axis] = traits_a.get(axis, 0.5) if random.random() > 0.5 else traits_b.get(axis, 0.5)
    elif req.crossover_method == "single_point":
        # Split at midpoint
        split = len(_TRAIT_AXES) // 2
        for i, axis in enumerate(_TRAIT_AXES):
            child_traits[axis] = traits_a.get(axis, 0.5) if i < split else traits_b.get(axis, 0.5)
    else:  # adaptive — weighted average based on parent fitness
        fa = ga.get("fitness_score", 0.5)
        fb = gb.get("fitness_score", 0.5)
        if fa + fb > 0:
            total = fa + fb
            for axis in _TRAIT_AXES:
                child_traits[axis] = round(
                    (traits_a.get(axis, 0.5) * fa + traits_b.get(axis, 0.5) * fb) / total, 3
                )
        else:
            # W438 refuter catch: with both parents at fitness 0.0 the old total=1.0 fallback
            # ZEROED every child trait and presented the constant as recombination — fall back to
            # the unweighted mean of the parents' actual traits instead
            for axis in _TRAIT_AXES:
                child_traits[axis] = round(
                    (traits_a.get(axis, 0.5) + traits_b.get(axis, 0.5)) / 2, 3
                )

    child_fitness = round((ga.get("fitness_score", 0.5) + gb.get("fitness_score", 0.5)) / 2, 3)

    name_a = ga.get("entity_name", req.genome_a_id)
    name_b = gb.get("entity_name", req.genome_b_id)
    genome_id = f"genome-{uuid.uuid4().hex[:10]}"
    child_genome = {
        "genome_id": genome_id,
        "entity_name": f"{name_a} × {name_b}",
        "domain": ga.get("domain", gb.get("domain", "general")),
        "realm": ga.get("realm", gb.get("realm", "enterprise")),
        "traits": child_traits,
        "fitness_score": child_fitness,
        "fitness_provenance": "inherited-mean-unevaluated (no selection step exists)",
        "expression": f"Offspring of {name_a} and {name_b}",
        "encoded": bool(ga.get("encoded")) or bool(gb.get("encoded")),
        "generation": max(ga.get("generation", 0), gb.get("generation", 0)) + 1,
        "parent_genomes": [req.genome_a_id, req.genome_b_id],
        "crossover_method": req.crossover_method,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_genome(child_genome)

    return child_genome


class MutateRequest(BaseModel):
    genome_id: str
    mutation_rate: float = Field(default=0.2, ge=0.0, le=1.0)     # probability each trait mutates
    mutation_strength: float = Field(default=0.15, ge=0.0, le=0.5)  # max magnitude of change


@router.post("/genome/mutate")
async def mutate_genome(req: MutateRequest):
    """Apply random mutation to a genome — real perturbation, every change recorded before → after.

    (Random variation IS what GA mutation means; the honesty fix here is the fitness field: the
    mutant inherits the parent's number and nothing re-evaluates it — the old code said "fitness
    re-evaluated by selection" in a comment while no selection step exists anywhere.)"""
    parent = _load_genome(req.genome_id)
    if not parent:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_id} not found.")

    rate = req.mutation_rate
    strength = req.mutation_strength
    parent_traits = parent.get("traits") or {}

    mutated_traits: dict[str, float] = {}
    mutations_applied = []

    for axis in _TRAIT_AXES:
        original = parent_traits.get(axis, 0.5)
        if random.random() < rate:
            delta = random.uniform(-strength, strength)
            new_val = round(max(0.0, min(1.0, original + delta)), 3)
            mutated_traits[axis] = new_val
            mutations_applied.append(f"{axis}: {original:.2f} → {new_val:.2f}")
        else:
            mutated_traits[axis] = original

    genome_id = f"genome-{uuid.uuid4().hex[:10]}"
    mutant = {
        "genome_id": genome_id,
        "entity_name": f"{parent.get('entity_name', req.genome_id)} (mutant)",
        "domain": parent.get("domain", "general"),
        "realm": parent.get("realm", "enterprise"),
        "traits": mutated_traits,
        "fitness_score": parent.get("fitness_score", 0.5),
        "fitness_provenance": "inherited-unevaluated (mutation does not re-score)",
        "expression": f"Mutation of {parent.get('entity_name', req.genome_id)} — {len(mutations_applied)} trait(s) altered",
        "encoded": bool(parent.get("encoded")),
        "generation": parent.get("generation", 0) + 1,
        "parent_genomes": [req.genome_id],
        "mutations": mutations_applied,
        "mutation_rate": rate,
        "mutation_strength": strength,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_genome(mutant)

    return mutant
