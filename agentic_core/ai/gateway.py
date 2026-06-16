import os
import httpx
from typing import Dict, Any
from agentic_core.ai.guardrails import validate_response
from agentic_core.ai.logger import interaction_logger
from agentic_core.ai.memory import memory

class ModelGateway:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.openai_key = os.getenv("OPENAI_API_KEY")

    async def query(self, prompt: str, agent: str = "assistant") -> str:
        # Check Memory (RAG)
        context = memory.query_memory(prompt)
        augmented_prompt = f"Context: {context}\n\nUser: {prompt}" if context else prompt

        response = ""
        openai_succeeded = False
        if self.openai_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=self.openai_key)
                completion = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": augmented_prompt}],
                    timeout=10,
                )
                response = completion.choices[0].message.content or "No response from model."
                openai_succeeded = True
            except Exception as e:
                # Invalid/expired key, quota, or network issue — fall through to Ollama
                # rather than failing the whole request or faking a response.
                response = f"[OpenAI unavailable: {str(e)[:200]}] Falling back to local model."

        if not openai_succeeded:
            try:
                # Ollama can take >10s on a cold model load (evicted after idling),
                # so allow real headroom rather than timing out a healthy request.
                async with httpx.AsyncClient() as client:
                    res = await client.post(self.ollama_url, json={
                        "model": self.model,
                        "prompt": augmented_prompt,
                        "stream": False
                    }, timeout=60)
                    response = res.json().get("response", "No response from model.")
            except Exception as e:
                error_detail = str(e) or type(e).__name__
                response = f"AI Offline (Ollama connection error: {error_detail})"

        # Apply Guardrails
        if not validate_response(response):
            response = "[POLICY VIOLATION] The generated response was blocked by Workstation safety guardrails."

        # Log Interaction
        interaction_logger.log_interaction(agent, prompt, response)

        # Update Memory
        memory.add_memory(f"User: {prompt} | AI: {response}")

        return response

gateway = ModelGateway()
