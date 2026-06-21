"""
Workstation's OWN native AI resource fabric (W1).

This package is Workstation's in-house AI capability — its own Model Resources,
Orchestration, and Swarm engine — so the platform is NOT a façade over external API
calls and is NOT dependent on third-party providers for cost, latency, freshness, or
control. External providers (Anthropic/OpenAI) become OPTIONAL accelerants behind an
explicit flag (AI_ALLOW_EXTERNAL=true); a self-hosted local model (Ollama) is used
when present; and a deterministic, owned **native reasoning engine** is always
available as the floor so a real, structured result is produced with NO external key.

Honesty: the native engine is the platform's own *structured* reasoning — it is never
presented as a large-language-model generation. Every result carries `served_by` so the
caller always knows which resource produced it.
"""
from agentic_core.ai.native.engine import NativeReasoningEngine, native_engine
from agentic_core.ai.native.model_resource import ModelResourceRegistry, registry
from agentic_core.ai.native.orchestrator import NativeOrchestrator, orchestrator

__all__ = [
    "NativeReasoningEngine", "native_engine",
    "ModelResourceRegistry", "registry",
    "NativeOrchestrator", "orchestrator",
]
