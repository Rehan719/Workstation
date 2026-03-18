import re

def validate_response(text: str) -> bool:
    """v148.0 Simple Guardrails for response safety."""
    prohibited_patterns = [
        r"malware", r"hacker", r"exploit" # Example safety patterns
    ]
    for pattern in prohibited_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True
