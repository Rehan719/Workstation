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
"""
from __future__ import annotations

import json
import time
import uuid
import random
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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


def _genome_path(genome_id: str) -> Path:
    return _GENOME_STORE / f"{genome_id}.json"


def _load_genome(genome_id: str) -> dict | None:
    p = _genome_path(genome_id)
    return json.loads(p.read_text()) if p.exists() else None


def _save_genome(genome: dict) -> None:
    _genome_path(genome["genome_id"]).write_text(json.dumps(genome, indent=2))


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
                "created_at": g.get("created_at", ""),
            })
        except Exception:
            pass
    return result


@router.get("/genome")
async def list_genomes():
    return {"genomes": _list_genomes(), "total": len(_list_genomes())}


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


@router.post("/genome/encode")
async def encode_genome(req: EncodeRequest):
    """
    AI-encode a project/entity into a genome trait vector.
    The AI analyses the entity and assigns trait values on 10 axes.
    """
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

    raw = await gateway.query(prompt, agent="genome_encoder")

    # Parse trait values
    traits: dict[str, float] = {}
    fitness = 0.5
    expression = ""

    for line in raw.splitlines():
        line = line.strip()
        for axis in _TRAIT_AXES:
            if line.lower().startswith(axis + ":"):
                try:
                    val = float(line.split(":")[1].strip())
                    traits[axis] = max(0.0, min(1.0, val))
                except (ValueError, IndexError):
                    pass
        if line.lower().startswith("fitness:"):
            try:
                fitness = max(0.0, min(1.0, float(line.split(":")[1].strip())))
            except (ValueError, IndexError):
                pass
        if line.lower().startswith("expression:"):
            expression = line.partition(":")[2].strip()

    # Fill any missing traits with neutral 0.5
    for axis in _TRAIT_AXES:
        if axis not in traits:
            traits[axis] = 0.5

    genome_id = f"genome-{uuid.uuid4().hex[:10]}"
    genome = {
        "genome_id": genome_id,
        "entity_name": req.entity_name,
        "domain": req.domain,
        "realm": req.realm,
        "project_id": req.project_id,
        "traits": traits,
        "fitness_score": fitness,
        "expression": expression,
        "generation": 0,
        "parent_genomes": [],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_genome(genome)

    return genome


class CrossoverRequest(BaseModel):
    genome_a_id: str
    genome_b_id: str
    crossover_method: str = "uniform"  # uniform | single_point | adaptive


@router.post("/genome/crossover")
async def crossover_genomes(req: CrossoverRequest):
    """
    Combine two parent genomes to produce an offspring genome.
    Simulates genetic crossover — the child inherits traits from both parents.
    """
    ga = _load_genome(req.genome_a_id)
    gb = _load_genome(req.genome_b_id)

    if not ga:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_a_id} not found.")
    if not gb:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_b_id} not found.")

    traits_a = ga["traits"]
    traits_b = gb["traits"]
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
        total = fa + fb if (fa + fb) > 0 else 1.0
        for axis in _TRAIT_AXES:
            child_traits[axis] = round(
                (traits_a.get(axis, 0.5) * fa + traits_b.get(axis, 0.5) * fb) / total, 3
            )

    # Child fitness is average of parents' fitness + small bonus for crossover
    child_fitness = round(min(1.0, (ga.get("fitness_score", 0.5) + gb.get("fitness_score", 0.5)) / 2 + 0.05), 3)

    child_name = f"{ga['entity_name']} × {gb['entity_name']}"
    genome_id = f"genome-{uuid.uuid4().hex[:10]}"
    child_genome = {
        "genome_id": genome_id,
        "entity_name": child_name,
        "domain": ga.get("domain", gb.get("domain", "general")),
        "realm": ga.get("realm", gb.get("realm", "enterprise")),
        "traits": child_traits,
        "fitness_score": child_fitness,
        "expression": f"Offspring of {ga['entity_name']} and {gb['entity_name']}",
        "generation": max(ga.get("generation", 0), gb.get("generation", 0)) + 1,
        "parent_genomes": [req.genome_a_id, req.genome_b_id],
        "crossover_method": req.crossover_method,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_genome(child_genome)

    return child_genome


class MutateRequest(BaseModel):
    genome_id: str
    mutation_rate: float = 0.2   # probability each trait mutates
    mutation_strength: float = 0.15  # max magnitude of change


@router.post("/genome/mutate")
async def mutate_genome(req: MutateRequest):
    """
    Apply random mutation to a genome — introduces variation for evolution.
    Returns the mutated genome as a new generation.
    """
    parent = _load_genome(req.genome_id)
    if not parent:
        raise HTTPException(status_code=404, detail=f"Genome {req.genome_id} not found.")

    rate = max(0.0, min(1.0, req.mutation_rate))
    strength = max(0.0, min(0.5, req.mutation_strength))

    mutated_traits: dict[str, float] = {}
    mutations_applied = []

    for axis in _TRAIT_AXES:
        original = parent["traits"].get(axis, 0.5)
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
        "entity_name": f"{parent['entity_name']} (mutant)",
        "domain": parent.get("domain", "general"),
        "realm": parent.get("realm", "enterprise"),
        "traits": mutated_traits,
        "fitness_score": parent.get("fitness_score", 0.5),  # fitness re-evaluated by selection
        "expression": f"Mutation of {parent['entity_name']} — {len(mutations_applied)} trait(s) altered",
        "generation": parent.get("generation", 0) + 1,
        "parent_genomes": [req.genome_id],
        "mutations": mutations_applied,
        "mutation_rate": rate,
        "mutation_strength": strength,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_genome(mutant)

    return mutant
