# Jules AI v99.0 TRANSCENDENT: Quick Start Guide

## 🚀 One-Click Setup
Run the command corresponding to your platform to initialize the v99 environment:

### 🪟 Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_windows.ps1
```

### 🍎 macOS / 🐧 Linux
```bash
python3 -m venv venv && source venv/bin/activate && pip install -e . && python3 -m agentic_core.synthesis.grand_synthesis_engine && pytest tests/test_v99_transcendent.py && streamlit run src/dashboard/app.py
```

---

## 🛠️ Verification
To manually verify the environment integrity:
```bash
python scripts/verify_environment.py
```

---

## 🧬 Basic Usage
To interact with the consolidated Conscious Organism Orchestrator:

```python
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99

async def main():
    # Initialize the v99 Transcendent Orchestrator
    organism = ConsciousOrganismV99()

    # Start the discovery cycle
    await organism.awaken()

    print("Jules AI v99.0 is operational and evolving.")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📜 Documentation Reference
Detailed guides are available in the `docs/v99/` directory:
- [Biological Systems Guide](docs/v99/BIOLOGICAL_SYSTEMS_GUIDE.md)
- [Incubation & Evolution Guide](docs/v99/INCUBATION_GUIDE.md)
- [Synthesis & Consolidation Guide](docs/v99/SYNTHESIS_GUIDE.md)
- [Constitution v99.0.0](CONSTITUTION_v99.0.0.md)
