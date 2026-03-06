# Jules AI v60.0 Quick Start

## 1. Setup
```bash
git clone https://github.com/Rehan719/Workstation.git
cd Workstation
pip install -e .
```

## 2. Initialize the Organism
Run the Grand Synthesis Engine to establish the DNA:
```bash
python3 -m agentic_core.synthesis.grand_synthesis_engine
```

## 3. Launch the Dashboard
Monitor the biological health of the organism:
```bash
streamlit run agentic_core/dashboard/app.py
```

## 4. Start an Incubation Project
```python
from agentic_core.incubation.adaptive_incubation_engine import AdaptiveIncubationEngine
import asyncio

async def main():
    engine = AdaptiveIncubationEngine()
    await engine.start_incubation("Study quantum neural networks", {"duration": "long-term"})

asyncio.run(main())
```
