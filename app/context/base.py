# app/context/base.py
"""
Abstract base classes.  Every concrete module must inherit from these.
"""
from abc import ABC, abstractmethod
from typing import List
from .models import Chunk


class ChunkerBase(ABC):
    @abstractmethod
    def chunk(self, document_path: str) -> List[Chunk]:
        """Split one document into Chunk objects."""
