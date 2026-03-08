import ast
import os

def check_file(filepath):
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except Exception:
            return

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if body contains only 'pass' or a docstring
            body = node.body
            if len(body) == 0: continue

            # Skip docstring if it's the only thing
            first_stmt = body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
                body = body[1:]

            if len(body) == 1 and isinstance(body[0], ast.Pass):
                 if node.name == "__init__": continue
                 print(f"{filepath}:{node.lineno}: Function '{node.name}' is a stub (pass).")
            elif len(body) == 0:
                 if node.name == "__init__": continue
                 print(f"{filepath}:{node.lineno}: Function '{node.name}' is a stub (empty).")

for root, dirs, files in os.walk('agentic_core'):
    for file in files:
        if file.endswith('.py'):
            check_file(os.path.join(root, file))

for root, dirs, files in os.walk('src'):
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    for file in files:
        if file.endswith('.py'):
            check_file(os.path.join(root, file))
