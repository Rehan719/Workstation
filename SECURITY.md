# Security Policy

## Supported Versions

We offer security support for the latest released version of this project.

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please report it responsibly. You can email security@example.com.

## Data Privacy and RAG Safety

Jules AI v10.0 utilizes Retrieval-Augmented Generation (RAG) to ground AI responses in provided documents.
- **Local Isolation**: By default, models and vector databases run locally or within isolated Docker networks to prevent data leakage to external providers.
- **Content Sensitivity**: Users should be aware that uploaded documents are indexed in the `SemanticMemory` (ChromaDB/Weaviate). We recommend avoiding the ingestion of highly confidential or personally identifiable information (PII) unless the environment is fully air-gapped.
- **LLM API Security**: The Ollama service is configured to be network-isolated. Ensure that ports are not exposed to the public internet without an authentication proxy.
