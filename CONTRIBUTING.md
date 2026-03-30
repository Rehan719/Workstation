# Contributing to Workstation Sovereign v3.0

Welcome to the digital civilisation. As an open-source project under the Apache 2.0 license, we invite researchers, developers, and sovereign individuals to help shape the future of agentic intelligence.

## How to Contribute

1.  **Audience Realms:** Contribute to specialized hubs (Religion, Science, Law, Employment, Education, Care).
2.  **Engine Development:** Enhance the Quad Engine, Digital Reactor, or Evolution Engine.
3.  **Governance:** Propose constitutional amendments via the RFC process.
4.  **Security:** Report vulnerabilities according to our `SECURITY.md` guidelines.

## Sovereign Organism & NVIDIA SDK Integration

The Workstation now operates as a **Sovereign Digital Organism**. The core organs (**Nematron**, **Nemoclaw**, **OpenClaw**) are implemented using an **Adapter Pattern**.

To contribute real-world integrations:
- **NVIDIA SDKs**: When **NVIDIA OpenClaw**, **Nemoclaw**, or **Nemotron** SDKs become available, create a new adapter in `src/organism/python/organs/` that implements the corresponding interface.
- **New Organs**: Propose new biological functions (e.g., Sensory Ingestion, Metabolic Resource Management) by extending the `AsyncEventBus` with new typed events.

## RFC Process

Major architectural changes must follow the Request for Comments (RFC) process:
- Submit a PR with your proposal in the `docs/rfcs/` directory.
- Participate in the bi-weekly community calls for discussion.
- Await ratification by the AI-led MultiSigCouncil.

## Code of Conduct

Please adhere to the `CODE_OF_CONDUCT.md` to ensure a respectful and collaborative environment for all sovereign entities.

---
*Certified by Article 1121: Open Source Leadership.*
