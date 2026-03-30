# Sovereign Digital Organism: Architecture Manifest

## Overview
The Workstation has been transmuted into an **Entity Intelligent Digital Biomimetic Organism**. This architecture follows biological principles to achieve autonomous decision-making, governance, and self-healing.

## Biomimetic Role Mapping
| Organism Organ | Component | Role | Underlying Engine |
| :--- | :--- | :--- | :--- |
| **Brain / CEO** | `NematronAdapter` | Strategic Reasoning | `agentic_core.ai_ceo` |
| **Immune System** | `NemoclawAdapter` | Governance & Security | `VGAEngine` + `ImmuneSystemV2` |
| **Executive Limbs** | `OpenClawAdapter` | Tool Execution | `agentic_core.tools.registry` |
| **Nervous System** | `AsyncEventBus` | Event-Driven Neural Bus | Async Python Pub/Sub |
| **Homeostasis** | `HomeostasisManager` | Self-Healing | `ResilienceManager` (LSTM) |
| **Identity** | `SovereignIdentity` | Cryptographic Soul | RSA-2048 signing |
| **Memory** | `SovereignState` | Persistent Context | Session-isolated JSON |

## Neural Bus Flow
The organism operates on a canonical three-stage reflex arc:
1. **Intent (Nematron)**: Generates a strategic decision event.
2. **Validation (Nemoclaw)**: Validates the intent against governance policies and threat models.
3. **Action (OpenClaw)**: Executes the validated action using the appropriate tools.

## Implementation Details
- **Core**: Python 3.11+ (Asyncio)
- **UI Bridge**: WebSocket-based Neural Bridge
- **Sovereignty Tiers**: Observational, Proposal, Delegated, Sovereign.

## Adapter Pattern for NVIDIA Integration
The core organs are implemented using an adapter pattern. This allows the current stub/legacy implementations to be seamlessly swapped with **NVIDIA OpenClaw**, **Nemoclaw**, and **Nemotron** SDKs once they are available in the local environment.

## Security & Sovereignty
- **Cryptographic Signing**: All autonomous actions are signed by the `SovereignIdentity` layer.
- **Hash-Chained Audit Trail**: The `activity.jsonl` ledger uses hash chaining to ensure immutability and detect tampering.
- **Verification**: Use `python -m src.organism.python.core.audit --path [log_path]` to verify chain integrity.
