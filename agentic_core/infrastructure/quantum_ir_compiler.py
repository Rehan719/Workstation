from typing import Any, Dict, Optional
from .universal_translator import UniversalTranslator
from ..orchestration.backend_mapper import BackendMapper
from ..orchestration.backends.ibm_plugin import IBMBackendPlugin
from ..orchestration.backends.aws_plugin import AWSBackendPlugin

class QuantumIRCompiler:
    """
    Article U (Revised): Hierarchical Two-Layer Compiler.
    Orchestrates the Universal Translator and the Backend Mapper.
    """
    def __init__(self):
        self.translator = UniversalTranslator()
        self.mapper = BackendMapper()

        # Register default plugins
        self.mapper.register_backend("ibm", IBMBackendPlugin())
        self.mapper.register_backend("aws", AWSBackendPlugin())

    async def compile(self, program: Any, framework: str, target_backend: str, orchestrator_context: Dict[str, Any]) -> Any:
        """Full compilation pipeline."""
        # Layer 1: Universal translation
        portable_ir = await self.translator.lower(program, framework)
        portable_ir = await self.translator.apply_agnostic_optimizations(portable_ir)

        # Layer 2: Backend-specific mapping
        backend_ir = await self.mapper.map(portable_ir, target_backend, orchestrator_context)

        return backend_ir

    # Deprecated v32 logic for compatibility if needed
    async def lower_to_mlir(self, program, framework):
        return await self.translator.lower(program, framework)

    async def run_optimization_pipeline(self, mlir_module, pipeline_name='default'):
        return await self.translator.apply_agnostic_optimizations(mlir_module)
