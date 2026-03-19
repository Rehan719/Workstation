# AI Ecosystem Documentation (v148.0)

## Architecture Overview
The Workstation AI ecosystem is a self-improving, multi-agent system designed to act as the planetary consciousness of the VSB entity.

## Components
1. **Model Gateway (`agentic_core/ai/gateway.py`)**: Unified interface for Ollama (llama3.2 default) and OpenAI. Handles RAG augmentation and safety guardrails.
2. **Orchestrator (`agentic_core/ai/orchestrator.py`)**: Manages agent roles and task delegation.
3. **Memory (`agentic_core/ai/memory.py`)**: Vector memory for retrieval-augmented generation.
4. **Logger (`agentic_core/ai/logger.py`)**: Persistent SQLite-based interaction logging.
5. **Guardrails (`agentic_core/ai/guardrails.py`)**: Pattern-based safety filters.

## Configuration
Use the `.env` file in the root or `agentic_core/` directory:
- `OLLAMA_URL`: URL to the Ollama API.
- `OLLAMA_MODEL`: Model name (default `llama3.2`).
- `OPENAI_API_KEY`: Optional key for cloud fallback.

## Endpoints
- `/api/v260/civilization/assistant/query`: General AI chat.
- `/api/ceo/delegate`: Task delegation to C-Suite agents.
- `/api/v190/introspection/decision-logs`: Reasoning transparency.

## Self-Improvement
The interaction logs are analyzed by the `EvolutionEngine` to generate pull requests for system optimization.
