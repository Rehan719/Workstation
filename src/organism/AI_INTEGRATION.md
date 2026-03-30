# AI Tool Integration (Sovereign Digital Organism)

## Overview
This layer integrates FREE and Open Source AI models into the Workstation's biomimetic architecture. All AI actions are audited, governed by human-in-the-loop workflows, and communicated via the Neural Bus.

## Integrated Providers
| Provider | Role | Key Features |
| :--- | :--- | :--- |
| **DeepSeek** | High-Throughput Ingestion | Forensic document analysis for legal evidence. |
| **Qwen** | Strategic Research | UK Employment Law synthesis (EqA 2010, ERA 1996). |
| **Minimax** | Codebase Reasoning | Autonomous test generation and async refactoring. |

## Governance & Security
- **AIAuditMiddleware**: Every LLM call is hash-chained and signed.
- **@require_human_approval**: Critical actions (e.g., prod deploy, legal filing) block until human signature is received.
- **Local Fallback**: Support for local inference via Ollama/vLLM for full data sovereignty.

## Neural Bus Events
- `AIActionInitiated`: Emitted when an LLM request starts.
- `AIInferenceComplete`: Emitted with usage stats (tokens, latency) on completion.

## Enabling AI Features
AI capabilities are feature-flagged in `src/organism/config/sovereign_config.yaml`:
```yaml
ai_features:
  ai_integration_experimental: { enabled: true }
  deepseek_ingestion: { enabled: true }
```
