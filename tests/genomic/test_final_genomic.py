import sys
import os
import numpy as np
from types import ModuleType

# Mock missing modules globally
for mod_name in ['shap', 'jwt', 'casbin', 'alembic', 'pygit2', 'sigstore']:
    if mod_name not in sys.modules:
        mock = ModuleType(mod_name)
        sys.modules[mod_name] = mock

import pytest
from agentic_core.genome.chromosome import Chromosome
from agentic_core.genome.gene import Gene, GeneType
from agentic_core.evolution.mutation.indel import Indel
from agentic_core.evolution.rearrangement.inversion import Inversion
from agentic_core.evolution.evolution_engine import GenomeEvolutionEngine
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

def test_genome_architecture():
    chrom = Chromosome("test")
    chrom.add_gene(Gene("g1", GeneType.STRUCTURAL, "h1"))
    assert len(chrom.sequence) == 1

def test_evolution_engine_cycle():
    chrom = Chromosome("core")
    chrom.add_gene(Gene("base", GeneType.REGULATORY, "h"))
    engine = GenomeEvolutionEngine(chrom)
    best = engine.run_cycle({"target": "test"})
    assert best.chromosome_id.startswith("mutant_")

@pytest.mark.asyncio
async def test_organism_genomic_action():
    org = ConsciousOrganismV99_0(agent_id="test_jules")
    await org.start()
    res = await org._execute_action("EVOLVE_GENOME", "Optimize system")
    assert res["evolution_status"] == "success"
    assert res["generation"] > 0
    await org.shutdown()
