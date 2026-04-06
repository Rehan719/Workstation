import os
import re

def update_outputs_to_v12():
    path = "outputs/Law/EmploymentTribunal/v12/"
    files = [f for f in os.listdir(path) if f.endswith(".md")]

    print(f"🔄 Updating {len(files)} files to v12.0-OMNISYNTHESIS standard...")

    for filename in files:
        filepath = os.path.join(path, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        # Replace version strings
        content = re.sub(r'v[0-9]+\.[0-9]+(-[A-Z]+)?', 'v12.0-OMNISYNTHESIS', content)

        # Ensure the header reflects the latest standard if it's one of the core files
        if filename.startswith(tuple(f"{i:02d}" for i in range(1, 25))):
            if "Minhas v Lonza" not in content:
                content = f"# Minhas v Lonza Biologics Plc\n## Law Grand Operation v12.0-OMNISYNTHESIS\n\n" + content

        with open(filepath, 'w') as f:
            f.write(content)

    print("✅ All outputs updated.")

if __name__ == "__main__":
    update_outputs_to_v12()
