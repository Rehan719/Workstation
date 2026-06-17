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
                timeout = httpx.Timeout(connect=5.0, read=20.0, write=5.0, pool=5.0)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    res = await client.post(self.ollama_url, json={
                        "model": self.model,
                        "prompt": augmented_prompt,
                        "stream": False,
                    })
                    response = res.json().get("response", "No response from model.")
            except httpx.ConnectError:
                response = (
                    "I'm temporarily unavailable — the local AI engine isn't running. "
                    "Start Ollama with `ollama serve` and your next message will connect automatically."
                )
            except httpx.ReadTimeout:
                response = (
                    "The AI model is still loading (this is normal on first use). "
                    "Please resend your message in a moment and it will respond."
                )
            except Exception as e:
                response = f"I encountered an unexpected error ({type(e).__name__}). Please try again."

        # Apply Guardrails
        if not validate_response(response):
            response = "[POLICY VIOLATION] The generated response was blocked by Workstation safety guardrails."

        # Log Interaction
        interaction_logger.log_interaction(agent, prompt, response)

        # Update Memory
        memory.add_memory(f"User: {prompt} | AI: {response}")

        return response

gateway = ModelGateway()
