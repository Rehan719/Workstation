# Usage Guide: Living MJM Intelligence Engine

## Graphical Interface
1. Navigate to the `ui/` directory.
2. Run `npm install` and `npm run dev`.
3. Open `http://localhost:3000` in your browser.
4. **Workflow Lifecycle:** Execute the Mushahida -> Jaiza -> Muaina pipeline.
5. **Genome Editor:** View and propose modifications to domain configurations.
6. **Cognitive Cortex:** Monitor learned patterns and approve evolution proposals.

## Command Line Interface
The CLI (`cli.py`) allows running the pipeline from the terminal.

### Example: Running Patient Safety Workflow
```bash
python cli.py mushahida --domain patient_safety --queries "autoimmune risk" --user "rehan"
python cli.py jaiza --checkpoint CHK-MUS-12345 --user "rehan"
python cli.py muaina --checkpoint CHK-JAI-54321 --option opt-1 --user "rehan"
```

## Biomimetic Features
- **Homeostasis:** The system monitors its own quality and flags performance degradation on the dashboard.
- **Learning:** Feedback from proposals is ingested into the Cognitive Cortex to refine pattern confidence.
- **Evolution:** Governed changes to the system "genome" can be proposed when high performance thresholds are met.
