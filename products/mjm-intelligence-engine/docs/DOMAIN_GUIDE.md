# Genome Configuration Guide

The MJM Intelligence Engine uses a "Genomic" configuration system where domain behavior is defined in YAML genomes.

## Base Genome
All domains extend `base_schema.yaml`. It defines the core data structures and default behaviors for Mushahida, Jaiza, and Muaina.

## Creating a New Domain
1. Create a new YAML file in `config/domains/`.
2. Use `extends: base_schema` to inherit core properties.
3. Override specific sections:
   - `mushahida`: Configure allowed sources and attention profiles.
   - `jaiza`: Add domain-specific pattern libraries and weighting.
   - `muaina`: Select output templates and verification protocols.

## Example: Custom Scientific Domain
```yaml
extends: base_schema
domain:
  id: "molecular-biology"
  name: "Molecular Research"
mushahida:
  allowed_sources: [pubmed_api, file_upload]
```
