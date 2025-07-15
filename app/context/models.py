# app/context/models.py
"""
Pydantic dataclasses shared across the whole project.
These MUST stay JSON-serialisable and match 04_io_contracts.md.
"""
from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel


class Chunk(BaseModel):
    doc_id: str                  # “AAPL_2024_Q1”
    text: str                    # raw chunk text
    metadata: Dict[str, Any]     # page, token_start, token_end, etc.
