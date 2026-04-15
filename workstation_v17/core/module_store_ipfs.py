import logging
class IPFSModuleStore:
    async def pin(self, cid, content):
        return f"ipfs://{cid}"
