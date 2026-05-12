# Workstation Development Setup Guide

## 🧬 Cross-Platform Setup

Workstation uses a specialized architecture including symlinks (for the genome module) and specific PyTorch versions.

### 1. Automated Setup (Recommended)
The recommended way to set up the project is using the provided script:
```bash
python scripts/post_clone_setup.py
```
This script handles:
- Virtual environment creation.
- Installation of CPU-optimized PyTorch.
- Fixing the genome module symlink/junction.
- Initializing the `.env` file from the template.

### 2. Manual PyTorch Installation
If you need to install dependencies manually, ensure you install the CPU version of torch to avoid issues on environments without dedicated GPUs:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### 3. Genome Module Symlink
The `agentic_core.genome` module is a link to `agentic_core.genetic_immune.genome`. If you encounter `ModuleNotFoundError`, run:
```bash
python scripts/fix_genome_symlink.py
```
On Windows, this creates a Directory Junction.

### 4. Running the Digital Twin Bootstrap
To verify the entire system is correctly integrated:
```bash
python scripts/bootstrap_digital_twin.py
```

## 🛡️ Troubleshooting

### IndentationError or SyntaxError
Ensure you are using Python 3.10+. The `agentic_core/main.py` has been patched to fix known IndentationErrors in websocket broadcast loops.

### NPM / Expo Errors
If you encounter errors related to `@expo/metro-runtime` during npm install, ensure you are in the correct workspace. The web app uses Vite and should not require Expo.
