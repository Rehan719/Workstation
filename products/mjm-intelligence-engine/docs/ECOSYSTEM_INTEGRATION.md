# MJM Ecosystem Integration Guide

The MJM Intelligence Engine is designed as a "synaptic node" within the Sovereign Digital Organism.

## Universal Adapter Interface
All connections use the `BaseAdapter` contract:
```python
class BaseAdapter(ABC):
    async def register(self, context: AdapterContext) -> RegistrationReceipt: ...
    async def publish(self, event: SovereignEvent) -> Dict[str, Any]: ...
    async def query(self, spec: QuerySpecification) -> Any: ...
```

## Integrated Components

### 1. Workstation Neural Bus
- **Purpose:** Ecosystem-wide event synchronization.
- **Adapter:** `MJMNeuralBusAdapter`
- **Topics:** `STRATEGIC_PRIORITY_UPDATE`, `REGULATORY_CHANGE_DETECTED`.

### 2. Entity Virtual Sovereign Brain (VSB)
- **Purpose:** Accessing project history and expert profiles.
- **Adapter:** `EntityVSBAdapter`
- **Functions:** Querying precedents, contributing learned patterns.

### 3. Veritas Grand Operation
- **Purpose:** Legal and regulatory precision.
- **Adapter:** `VeritasIntegrationAdapter`
- **Usage:** Validating compliance of proposed actions against statutes (Equality Act, ACAS Code).

## Connecting a New Product
To connect a new product to the MJM Engine:
1. Implement a new adapter in `adapters/`.
2. Register the adapter in the `ecosystem` section of `base_schema.yaml`.
3. Add the adapter to the `WorkflowOrchestrator` service container.
