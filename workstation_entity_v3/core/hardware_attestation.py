import logging
class HardwareAttestation:
    async def attest(self) -> bool:
        return True
    async def get_quote(self) -> str:
        return "TPM-SIGNED-V16-GOLDEN-QUOTE"
