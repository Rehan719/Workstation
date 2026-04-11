# Usage Guide: MJM Intelligence Engine

## Graphical Interface
1. Navigate to the `ui/` directory.
2. Run `npm install` and `npm run dev`.
3. Open `http://localhost:3000` in your browser.
4. Follow the 3-phase wizard (Mushahida -> Jaiza -> Muaina).

## Command Line Interface
The CLI provides a way to run the MJM pipeline from the terminal.

### Mushahida (Observation)
```bash
python cli.py mushahida --queries "patient safety risks" "proceduralism trap" --user "Rehan"
```
*Output: Mushahida completed. Checkpoint: CHK-MUS-12345678*

### Jaiza (Evaluation)
```bash
python cli.py jaiza --checkpoint CHK-MUS-12345678 --user "Rehan"
```
*Output: Jaiza completed. Checkpoint: CHK-JAI-87654321*

### Muaina (Inspection)
```bash
python cli.py muaina --checkpoint CHK-JAI-87654321 --option "regulatory-realignment" --user "Rehan"
```
*Output: Muaina completed. Checkpoint: CHK-MUA-11223344*

## Collaborative Workflow (GitHub)
When a proposal is ready, use the generated GitHub workflow bundle to submit a Pull Request.
1. Copy the `git` commands from the Muaina output.
2. Execute them in your terminal to create a branch and PR.
3. Reviewers can then comment on specific evidence items via the GitHub interface.
