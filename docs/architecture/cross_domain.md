# Architectural Blueprint: Cross-Domain Integration (v99.0)

## 1. Unified Dashboard
*   **Path:** `src/qep_frontend/src/pages/UnifiedDashboard.jsx`
*   **Logic:** Dynamic widget loader using domain-specific metadata.
*   **Entity Link:** Central chat interface delegates to `ConsciousEntityCore.generate_response`.

## 2. Cross-Domain Workflow Engine
*   **Path:** `agentic_core/workflow/engine.py`
*   **Format:** YAML/JSON definitions for multi-step reactor interactions.
*   **Registry:** Managed by `AIDispatcher` with immune-inspired activation.

## 3. Analytics Warehouse
*   **Path:** `agentic_core/analytics/warehouse/`
*   **Storage:** Partitioned SQLite (emulating ClickHouse/PostgreSQL).
*   **ETL:** Real-time event ingestion from the global Event Bus.

## 4. Global Event Bus
*   **Path:** `agentic_core/workflow/event_bus.py`
*   **Pattern:** Pub/Sub for inter-reactor signaling (e.g., `LAW_READY`, `SCIENCE_PUBLISHED`).
