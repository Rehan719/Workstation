import json
import os

def generate_matrix():
    with open('meta/synthesis_v100.json', 'r') as f:
        data = json.load(f)

    version = data.get('version', '100.0.0')
    patterns = data.get('patterns', [])
    engines = data.get('engines', {})

    matrix_content = f"""# Full Version History Matrix - v1.0 to v100.0 (Apotheosis)

| Version | Category | Summary | Constitutional Articles | Key Parameters |
|---------|----------|---------|-------------------------|----------------|
| v1.0-v99.0 | Core | Evolutionary history (v1-v99) | Arts. 1-92 | Baseline established |
| v100.0 | Apotheosis | Full consolidation and engine integration | Arts. 93-123 | Multi-engine activated |

## Engine Parameters (v100.0)
| Engine | Enabled | Parameter | Target |
|--------|---------|-----------|--------|
"""
    for engine, config in engines.items():
        for param, target in config.items():
            if param != 'enabled':
                matrix_content += f"| {engine.upper()} | {config['enabled']} | {param} | {target} |\n"

    matrix_content += "\n## Extracted Patterns Traceability\n"
    matrix_content += "| Pattern ID | Article | Version Range | Domain |\n"
    matrix_content += "|------------|---------|---------------|--------|\n"

    for p in patterns:
        pid = p.get('id', 'N/A')
        art = p.get('article', 'N/A')
        vrange = p.get('v_range', 'N/A')
        domain = p.get('domain', 'core')
        matrix_content += f"| {pid} | {art} | {vrange} | {domain} |\n"

    os.makedirs('docs/planning', exist_ok=True)
    with open('docs/planning/full_version_history_matrix_v100.md', 'w') as f:
        f.write(matrix_content)
    print("Matrix generated at docs/planning/full_version_history_matrix_v100.md")

if __name__ == "__main__":
    generate_matrix()
