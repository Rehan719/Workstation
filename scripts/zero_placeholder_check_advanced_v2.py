#!/usr/bin/env python3
import ast
import os
import sys
import argparse

class ZeroPlaceholderFinder(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.violations = []

    def visit_Pass(self, node):
        self.violations.append(f"{self.filename}:{node.lineno}: found 'pass'")

    def visit_Raise(self, node):
        if isinstance(node.exc, ast.Call) and getattr(node.exc.func, 'id', '') == 'NotImplementedError':
            self.violations.append(f"{self.filename}:{node.lineno}: found 'NotImplementedError'")
        elif isinstance(node.exc, ast.Name) and node.exc.id == 'NotImplementedError':
            self.violations.append(f"{self.filename}:{node.lineno}: found 'NotImplementedError'")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # Check for empty function body (only docstring)
        body = node.body
        if len(body) == 1 and isinstance(body[0], ast.Expr) and isinstance(body[0].value, (ast.Str, ast.Constant)):
             self.violations.append(f"{self.filename}:{node.lineno}: function '{node.name}' has empty body (only docstring)")
        self.generic_visit(node)

def check_file(filepath):
    violations = []

    # Text-based check for TODO, FIXME, etc. in comments or strings
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if any(placeholder in line for placeholder in ["TODO", "FIXME", "XXX", "# stub", "# mock"]):
                    # Ignore the check script itself and some legitimate uses
                    if "zero_placeholder_check" in filepath or "doc_linter.py" in filepath or "verify_v19_1_sovereign.py" in filepath:
                        continue
                    violations.append(f"{filepath}:{i+1}: found comment placeholder in line: {line.strip()}")
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")

    # AST-based check for Python files
    if filepath.endswith('.py'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=filepath)
                finder = ZeroPlaceholderFinder(filepath)
                finder.visit(tree)
                violations.extend(finder.violations)
        except SyntaxError as e:
            print(f"Warning: Syntax error in {filepath}: {e}")
        except Exception as e:
            print(f"Warning: Error parsing {filepath}: {e}")

    return violations

def main():
    parser = argparse.ArgumentParser(description="Zero-Placeholder Check v2")
    parser.add_argument("targets", nargs='*', default=["agentic_core", "agents", "backend", "config", "core", "products", "realms"])
    args = parser.parse_args()

    all_violations = []
    exclude_dirs = {"node_modules", "venv", "__pycache__", ".git", ".mypy_cache"}

    for target in args.targets:
        if os.path.isfile(target):
            all_violations.extend(check_file(target))
        elif os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                for file in files:
                    if file.endswith(('.py', '.ts', '.tsx')):
                        filepath = os.path.join(root, file)
                        all_violations.extend(check_file(filepath))

    if all_violations:
        print("❌ Zero-Placeholder violations found:")
        for v in all_violations:
            print(v)
        sys.exit(1)
    else:
        print("✅ Zero-Placeholder check passed – 100% concrete logic")

if __name__ == "__main__":
    main()
