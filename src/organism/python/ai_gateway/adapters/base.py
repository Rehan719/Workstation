from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union

class SovereignLLMClient(ABC):
    """
    Abstract Base Class for all AI model providers.
    Compliant with Sovereign Digital Organism adapter pattern.
    """
    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    async def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Executes a chat completion request."""
        pass

    @abstractmethod
    async def get_embeddings(self, text: Union[str, List[str]]) -> List[List[float]]:
        """Generates embeddings for the given text."""
        pass

    def get_provider_info(self) -> Dict[str, Any]:
        return {"provider": self.provider_name}
