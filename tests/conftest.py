import sys
from unittest.mock import MagicMock

class MockTensor:
    pass

# Mock heavy dependencies that are not in the sandbox environment
mock_modules = [
    "torch", "torch.nn", "shap", "qiskit", "web3", "ot",
    "reportlab", "reportlab.pdfgen", "reportlab.lib.pagesizes", "reportlab.lib.units",
    "PyPDF2", "pydantic", "pydantic_settings", "psutil"
]

for mod in mock_modules:
    sys.modules[mod] = MagicMock()

# Handle some specific attributes if needed
sys.modules["pydantic"].BaseModel = MagicMock
sys.modules["pydantic"].Field = MagicMock
sys.modules["torch"].Tensor = MockTensor

# Mock Firebase and Stripe to prevent initialization errors at module level
mock_firestore = MagicMock()
mock_firebase = MagicMock()
mock_firebase.firestore.client.return_value = mock_firestore
sys.modules["firebase_admin"] = mock_firebase
sys.modules["firebase_admin.auth"] = MagicMock()
sys.modules["firebase_admin.firestore"] = MagicMock()
sys.modules["firebase_admin.firestore"].client = MagicMock(return_value=mock_firestore)

sys.modules["stripe"] = MagicMock()
