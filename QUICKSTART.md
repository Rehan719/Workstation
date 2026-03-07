# Jules AI v99.0 TRANSCENDENT: Quick Start Guide

## 🚀 One-Click VS Code Setup
This repository is optimized for VS Code. To get started immediately:
1. Open the repository in VS Code.
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
3. Type `Tasks: Run Task` and select **`Awaken Transcendent (v99 Setup)`**.

---

## 💻 Manual Terminal Setup (Copy & Paste)
If you prefer using the terminal, copy and paste the following block into your VS Code terminal to initialize the environment and verify the v99.0.0 integration:

```bash
# 1. Initialize environment and dependencies
python3 -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate

pip install --upgrade pip
pip install -e .

# 2. Run the Grand Synthesis Engine to consolidate the v99 DNA
python3 -m agentic_core.synthesis.grand_synthesis_engine

# 3. Verify the Transcendent Integrity
python3 tests/test_v99_transcendent.py

# 4. Launch the Unified Dashboard
streamlit run src/dashboard/app.py
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
