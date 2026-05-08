import os
import sys
import platform
import subprocess
import shutil

def run_command(command, shell=False):
    print(f"Running: {command}")
    subprocess.check_call(command, shell=shell)

def main():
    print("🧬 Starting Workstation Post-Clone Setup...")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    # 1. Create Virtual Environment
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run_command([sys.executable, "-m", "venv", "venv"])

    # 2. Determine venv python path
    if platform.system() == "Windows":
        venv_python = os.path.join(base_dir, "venv", "Scripts", "python.exe")
        venv_pip = os.path.join(base_dir, "venv", "Scripts", "pip.exe")
    else:
        venv_python = os.path.join(base_dir, "venv", "bin", "python")
        venv_pip = os.path.join(base_dir, "venv", "bin", "pip")

    # 3. Install dependencies
    print("Installing dependencies (CPU-optimized torch)...")
    run_command([venv_pip, "install", "--upgrade", "pip"])
    # CPU version for reliability
    run_command([venv_pip, "install", "torch", "--index-url", "https://download.pytorch.org/whl/cpu"])
    run_command([venv_pip, "install", "-r", "requirements.txt"])

    # 4. Fix Genome Symlink
    print("Fixing genome symlink...")
    run_command([venv_python, "scripts/fix_genome_symlink.py"])

    # 5. Initialize .env
    if not os.path.exists(".env"):
        print("Creating .env from template...")
        if os.path.exists(".env.template"):
            shutil.copy(".env.template", ".env")
        else:
            with open(".env", "w") as f:
                f.write("# Workstation Environment Variables\n")

    print("\n✅ Setup complete. To start the platform, run:")
    if platform.system() == "Windows":
        print("venv\\Scripts\\activate")
    else:
        print("source venv/bin/activate")
    print("python -m uvicorn agentic_core.main:app --host 0.0.0.0 --port 8080 --reload")

if __name__ == "__main__":
    main()
