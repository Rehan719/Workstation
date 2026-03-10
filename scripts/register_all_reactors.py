import asyncio
import logging
from agentic_core.reactor.ecosystem.registry import ReactorRegistry
from agentic_core.reactor.science.physics import PhysicsReactor
from agentic_core.reactor.religion.tafsir import TafsirReactor
from agentic_core.reactor.law.contract import ContractReactor
from agentic_core.reactor.employment.resume import ResumeReactor
from agentic_core.reactor.education.k12 import K12Reactor

# Template imports
from agentic_core.reactor.science.chemistry import ChemistryReactor
from agentic_core.reactor.science.biology import BiologyReactor
from agentic_core.reactor.science.computer_science import Computer_scienceReactor
from agentic_core.reactor.religion.hadith import HadithReactor
from agentic_core.reactor.religion.fiqh import FiqhReactor

async def register_all():
    registry = ReactorRegistry()

    # Gold Standards
    registry.register(PhysicsReactor())
    registry.register(TafsirReactor())
    registry.register(ContractReactor())
    registry.register(ResumeReactor())
    registry.register(K12Reactor())

    # Template instances (Subset for demo)
    registry.register(ChemistryReactor())
    registry.register(BiologyReactor())
    registry.register(Computer_scienceReactor())
    registry.register(HadithReactor())
    registry.register(FiqhReactor())

    print(f"Registered {len(registry.reactors)} sub-reactors.")

if __name__ == "__main__":
    asyncio.run(register_all())
