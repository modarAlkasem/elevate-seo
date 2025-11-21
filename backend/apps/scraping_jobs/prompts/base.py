# Python Imports
from abc import ABC, abstractmethod


class BasePrompt(ABC):
    """Base class for all prompts"""

    @abstractmethod
    def build(self, **kwargs: dict) -> str:
        pass

    def _clean(self, text: str) -> str:
        """Remove extra white spaces"""
        return text.strip()
