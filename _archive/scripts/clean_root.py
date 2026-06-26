import os
import shutil
import subprocess

WHITELIST = {
    ".devcontainer", ".git", ".github", "agentic_core", "apps", "config", "deploy",
    "deployment", "docs", "infra", "meta", "packages", "products", "scripts",
    "simulations", "src", "tests", ".env.template", ".gitignore", "CODEOWNERS",
    "CONTRIBUTING.md", "DEPLOYMENT.md", "Makefile", "QUICKSTART.md", "README.md",
    "SECURITY.md", "USER_GUIDE.md", "deploy.sh", "docker-compose-swarm.yml",
    "pyproject.toml", "teardown.sh"
}

ARCHIVE_FILES = [
    "AI-Driven Quranic Education Platfor SAVED.txt",
    "AI-Driven Quranic Education Platform - Developer Guide.txt",
    "AI-Driven Quranic Education Platform - Jules Agent Guide.txt",
    "AI-Driven Quranic Education Platform Jules Updated (2).txt",
    "Build on and enhance the plan; jule SAVED.txt",
    "Build on and enhance the plan; jule.txt",
    "Deepseek further background to Workstation Scripts.txt",
    "Deepseek further background to Workstation.txt",
    "Deepseek workstation background Further development.txt",
    "Deepseek workstation background.txt",
    "Design environment script background.txt",
    "JULES PROMPT WORKSTATION PROJECT v9.txt",
    "LLM URL share links.txt",
    "MinimaxAi  further background to Workstation Evolutionary cognition.txt",
    "Production environment script background.txt",
    "Qwen Further background to Workstation Further.txt",
    "Qwen Further background to Workstation Scripts.txt",
    "Qwen Further background to Workstation.txt",
    "Qwen further background to Workstation Evolutionary cognition.txt",
    "Qwens workstation background Further development.txt",
    "Qwens workstation background.txt",
    "Tools scripts background.txt",
    "scripts background.txt"
]

DELETE_PATTERNS = [
    ".pytest_cache", "final_hardened_test.log", "final_release_test.log",
    "final_test.log", "test_out.log", "verify_out.log", "*.png"
]

def clean_root(execute=False):
    root_items = os.listdir(".")
    archive_dir = "docs/archive"
    os.makedirs(archive_dir, exist_ok=True)

    print(f"{'ACTION':<10} | {'ITEM':<50} | {'REASON'}")
    print("-" * 80)

    for item in root_items:
        if item in WHITELIST or item == "scripts" or item == "docs":
            continue

        # Archive logic
        if item in ARCHIVE_FILES:
            if execute:
                shutil.move(item, os.path.join(archive_dir, item))
                print(f"{'ARCHIVE':<10} | {item:<50} | Historical context")
            else:
                print(f"{'[DRY] ARCH':<10} | {item:<50} | Historical context")
            continue

        # Delete logic for specific items
        should_delete = False
        if any(item.endswith(".log") or item.endswith(".png") for pattern in DELETE_PATTERNS):
            should_delete = True
        if item in [".pytest_cache", "final_hardened_test.log", "final_release_test.log", "final_test.log", "test_out.log", "verify_out.log"]:
            should_delete = True

        if should_delete:
            if execute:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"{'DELETE':<10} | {item:<50} | Temporary/Obsolete artifact")
            else:
                print(f"{'[DRY] DEL':<10} | {item:<50} | Temporary/Obsolete artifact")
            continue

        # Default: archive unknown text or markdown files just in case
        if item.endswith(".txt") or (item.endswith(".md") and item not in WHITELIST):
            if execute:
                shutil.move(item, os.path.join(archive_dir, item))
                print(f"{'ARCHIVE':<10} | {item:<50} | Unknown doc (fallback archive)")
            else:
                print(f"{'[DRY] ARCH':<10} | {item:<50} | Unknown doc (fallback archive)")
        else:
             print(f"{'IGNORE':<10} | {item:<50} | No rule defined")

if __name__ == "__main__":
    import sys
    do_execute = "--execute" in sys.argv
    clean_root(execute=do_execute)
    if not do_execute:
        print("\nRun with --execute to apply changes.")
