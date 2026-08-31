import sys
import importlib
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VerifyEnv")

REQUIRED_MODULES = [
    "agentic_core",
    "numpy",
    "shap",
    "jwt",
    "streamlit",
    "langchain",
    "pydantic",
    "fastapi",
    "uvicorn"
]

def verify_modules():
    missing = []
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
            logger.info(f"✅ Module '{module}' is successfully imported.")
        except ImportError as e:
            logger.error(f"❌ Module '{module}' failed to import: {e}")
            missing.append(module)
    return missing

def run_pip_check():
    logger.info("Running 'pip check' to detect dependency conflicts...")
    result = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✅ No dependency conflicts detected.")
        return True
    else:
        logger.warning("⚠️ Dependency conflicts detected:")
        logger.warning(result.stdout)
        return False

if __name__ == "__main__":
    logger.info("⚜️ Jules AI v99: Starting Environment Verification...")

    missing_mods = verify_modules()
    pip_ok = run_pip_check()

    if not missing_mods and pip_ok:
        logger.info("🚀 Environment is HARDENED and ready for TRANSCENDENT operations.")
        sys.exit(0)
    else:
        logger.error("❌ Environment verification FAILED.")
        sys.exit(1)
