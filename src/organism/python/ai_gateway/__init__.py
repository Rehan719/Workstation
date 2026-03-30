import logging
import time
import hashlib
import json
from typing import Dict, Any, Type, Optional, List
from .adapters.base import SovereignLLMClient
from src.organism.python.neural.event_types import AIActionInitiated, AIInferenceComplete

logger = logging.getLogger(__name__)

class AIGateway:
    """
    Provider Registry & Orchestrator for the Sovereign AI Tooling Layer.
    Integrated with Neural Bus and Sovereign Audit Log.
    """
    def __init__(self, event_bus: Optional[Any] = None, audit_middleware: Optional[Any] = None):
        self.providers: Dict[str, SovereignLLMClient] = {}
        self.event_bus = event_bus
        self.audit = audit_middleware
        self.default_provider = "deepseek"

    def register_provider(self, name: str, client: SovereignLLMClient):
        self.providers[name] = client
        logger.info(f"AIGateway: Registered provider '{name}'")

    def get_provider(self, name: str) -> Optional[SovereignLLMClient]:
        return self.providers.get(name)

    async def execute_completion(self, provider_name: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        client = self.get_provider(provider_name)
        if not client:
            # Fallback logic
            logger.warning(f"AIGateway: Provider '{provider_name}' not found. Falling back to {self.default_provider}")
            client = self.get_provider(self.default_provider)
            if not client:
                raise ValueError("No valid AI providers available.")
            provider_name = self.default_provider

        # 1. Neural Bus: Signal Intent
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

        # 2. Sovereign Audit: Log Pre-Execution (Observational/Proposal)
        if self.audit:
            await self.audit.log_ai_action(
                action="chat_completion",
                payload={"messages": messages, "kwargs": kwargs},
                provider=provider_name
            )

        # 3. Execution
        try:
            result = await client.chat_completion(messages, **kwargs)

            # 4. Neural Bus: Signal Completion
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
            logger.error(f"AIGateway: Execution failed for {provider_name}: {e}")
            if self.event_bus:
                await self.event_bus.publish(AIInferenceComplete(
                    action_id=action_id,
                    source="ai_gateway",
                    provider=provider_name,
                    status="FAILED"
                ))
            raise

# Global Gateway Instance
gateway = AIGateway()
