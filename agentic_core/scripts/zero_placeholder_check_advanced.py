import os
import ast
import sys

class PlaceholderChecker(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.violations = []

    def visit_Pass(self, node):
        self.violations.append(f"{self.filename}:{node.lineno}: Found 'pass'")

    def visit_Raise(self, node):
        if isinstance(node.exc, ast.Call) and getattr(node.exc.func, 'id', '') == 'NotImplementedError':
            self.violations.append(f"{self.filename}:{node.lineno}: Found 'NotImplementedError'")
        elif isinstance(node.exc, ast.Name) and node.exc.id == 'NotImplementedError':
            self.violations.append(f"{self.filename}:{node.lineno}: Found 'NotImplementedError'")

def check_placeholders(directory):
    total_violations = 0
    for root, _, files in os.walk(directory):
        if 'tests' in root or 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        tree = ast.parse(content)
                    checker = PlaceholderChecker(path)
                    checker.visit(tree)

                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if 'TODO' in line:
                            checker.violations.append(f"{path}:{i+1}: Found 'TODO'")

                    if checker.violations:
                        for v in checker.violations:
                            print(v)
                        total_violations += len(checker.violations)
                except Exception:
                    pass
    return total_violations

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "agentic_core"
    violations = check_placeholders(target)
    print(f"\nTotal violations: {violations}")
