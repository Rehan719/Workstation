import sys
from agentic_core.main import app
for route in app.routes:
    print(f"{route.path} {getattr(route, 'methods', 'WS')}")
