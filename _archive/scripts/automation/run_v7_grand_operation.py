import os
import subprocess

def run_grand_operation():
    print("🏛️ Starting Multi-Domain Grand Operation Workflow v7.0...")

    domains = ["Religion", "Science", "Law", "Employment", "Care", "Enterprise"]

    for domain in domains:
        print(f"\n📌 Processing Domain: {domain}")
        script_path = f"scripts/{domain}/regenerate_v7.0.py"
        if os.path.exists(script_path):
            try:
                # Add current directory to PYTHONPATH so scripts can import from scripts.automation
                env = os.environ.copy()
                env["PYTHONPATH"] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"
                subprocess.run(["python3", script_path], env=env, check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error executing {script_path}: {e}")
        else:
            print(f"⚠️ Script not found: {script_path}")

    print("\n✅ Multi-Domain Grand Operation Workflow v7.0 Execution Complete.")

if __name__ == "__main__":
    run_grand_operation()
