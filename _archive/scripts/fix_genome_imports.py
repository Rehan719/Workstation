import os
import re

def fix_imports(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.py'):
                filepath = os.path.join(dirpath, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Replace 'from agentic_core.genome' with 'from agentic_core.genetic_immune.genome'
                new_content = re.sub(r'from agentic_core\.genome(\.| )', r'from agentic_core.genetic_immune.genome\1', content)
                # Replace 'import agentic_core.genome' with 'import agentic_core.genetic_immune.genome'
                new_content = re.sub(r'import agentic_core\.genome(\.| )', r'import agentic_core.genetic_immune.genome\1', new_content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Updated: {filepath}")

if __name__ == "__main__":
    fix_imports('agentic_core')
