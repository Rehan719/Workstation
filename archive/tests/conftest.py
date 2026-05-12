import sys
from unittest.mock import MagicMock

class MockTensor:
    pass

# Mock heavy dependencies that are not in the sandbox environment
mock_modules = [
    "torch", "torch.nn", "shap", "qiskit", "web3", "ot",
    "firebase_admin", "firebase_admin.auth", "firebase_admin.firestore", "stripe",
    "reportlab", "reportlab.pdfgen", "reportlab.lib.pagesizes", "reportlab.lib.units",
    "PyPDF2", "pydantic", "pydantic_settings"
]

for mod in mock_modules:
    sys.modules[mod] = MagicMock()

# Handle some specific attributes if needed
sys.modules["pydantic"].BaseModel = MagicMock
sys.modules["pydantic"].Field = MagicMock
sys.modules["torch"].Tensor = MockTensor
