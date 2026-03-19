import os
import requests
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
        if self.openai_key:
            response = "OpenAI response simulation for: " + prompt
        else:
            try:
                res = requests.post(self.ollama_url, json={
                    "model": self.model,
                    "prompt": augmented_prompt,
                    "stream": False
                }, timeout=10)
                response = res.json().get("response", "No response from model.")
            except Exception as e:
                response = f"AI Offline (Ollama connection error: {str(e)})"

        # Apply Guardrails
        if not validate_response(response):
            response = "[POLICY VIOLATION] The generated response was blocked by Workstation safety guardrails."

        # Log Interaction
        interaction_logger.log_interaction(agent, prompt, response)

        # Update Memory
        memory.add_memory(f"User: {prompt} | AI: {response}")

        return response

gateway = ModelGateway()
