import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional, List
from .adapters.base import SovereignLLMClient
from src.organism.python.neural.event_types import AIActionInitiated, AIInferenceComplete

# OpenTelemetry Preparedness
try:
    from opentelemetry import trace
    tracer = trace.get_tracer(__name__)
except ImportError:
    tracer = None

logger = logging.getLogger(__name__)

class AIGateway:
    """
    Provider Registry & Orchestrator for the Sovereign AI Tooling Layer.
    Integrated with Neural Bus, Sovereign Audit Log, and Semantic Cache.
    """
    def __init__(self, event_bus: Optional[Any] = None, audit_middleware: Optional[Any] = None, cache: Optional[Any] = None, budget_manager: Optional[Any] = None):
        self.providers: Dict[str, SovereignLLMClient] = {}
        self.event_bus = event_bus
        self.audit = audit_middleware
        self.cache = cache
        self.budget = budget_manager
        self.default_provider = "deepseek"

    def register_provider(self, name: str, client: SovereignLLMClient):
        self.providers[name] = client
        logger.info(f"AIGateway: Registered provider '{name}'")

    def get_provider(self, name: str) -> Optional[SovereignLLMClient]:
        return self.providers.get(name)

    async def execute_completion(self, provider_name: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        prompt_text = str(messages)

        # 1. Semantic Caching (Step 1.1)
        if self.cache:
            cached_res = await self.cache.get(prompt_text, provider_name)
            if cached_res:
                return {"provider": provider_name, "content": cached_res, "cached": True}

        client = self.get_provider(provider_name)
        if not client:
            logger.warning(f"AIGateway: Provider '{provider_name}' not found. Falling back to {self.default_provider}")
            client = self.get_provider(self.default_provider)
            if not client:
                raise ValueError("No valid AI providers available.")
            provider_name = self.default_provider

        # 2. Token Budgeting (Step 1.2)
        if self.budget:
            # Estimate tokens roughly
            est_tokens = len(prompt_text) // 4
            if not self.budget.check_and_reserve(provider_name, est_tokens):
                raise RuntimeError(f"AIGateway: Quota exhausted for {provider_name}")

        # 3. Neural Bus: Signal Intent
        payload_hash = hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest()
        action_id = f"AI-{int(time.time()*1000)}"

        if self.event_bus:
            await self.event_bus.publish(AIActionInitiated(
                id=action_id,
                source="ai_gateway",
                action="chat_completion",
                provider=provider_name,
                payload_hash=payload_hash,
                priority=3
            ))

        # 4. Execution with Instrumentation
        span = None
        if tracer:
            span = tracer.start_span(f"ai_completion:{provider_name}")
            span.set_attribute("ai.provider", provider_name)

        try:
            result = await client.chat_completion(messages, **kwargs)

            # Update cache and budget
            if self.cache:
                await self.cache.set(prompt_text, result["content"], provider_name)
            if self.budget:
                self.budget.update_usage(provider_name, result.get("usage", {}).get("total_tokens", 0))

            # Neural Bus: Signal Completion
            if self.event_bus:
                await self.event_bus.publish(AIInferenceComplete(
                    action_id=action_id,
                    source="ai_gateway",
                    provider=provider_name,
                    tokens_used=result.get("usage", {}).get("total_tokens", 0),
                    latency_ms=result.get("latency_ms", 0.0),
                    status="SUCCESS"
                ))

            return result

        except Exception as e:
            if self.event_bus:
                await self.event_bus.publish(AIInferenceComplete(
                    action_id=action_id,
                    source="ai_gateway",
                    provider=provider_name,
                    status="FAILED"
                ))
            if span:
                span.record_exception(e)
            raise
        finally:
            if span:
                span.end()

# Global Gateway Instance
gateway = AIGateway()
