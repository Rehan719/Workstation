import pytest
from agentic_core.protocols.scholarly_object import ScholarlyObject
from cryptography.hazmat.primitives.asymmetric import rsa

def test_scholarly_object_signing():
    # Generate keys
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Create object
    obj = ScholarlyObject(obj_type="manuscript_section", content="Sample content", created_by="agent_1")

    # Sign
    obj.sign(private_key)
    assert obj.signature is not None

    # Verify
    assert obj.verify(public_key) is True

    # Modify and verify failure
    obj.content = "Tampered content"
    assert obj.verify(public_key) is False

    # Re-sign and verify
    obj.sign(private_key)
    assert obj.verify(public_key) is True

if __name__ == "__main__":
    test_scholarly_object_signing()
    print("ScholarlyObject signing test passed!")
