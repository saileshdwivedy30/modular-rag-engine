# app/context/chunker_li.py
"""
LlamaIndex-powered Chunker that fulfils ChunkerBase.
# Import: Why we need it
# Path: Safer than raw strings; gives exists(), stem, etc.
# List: Keeps the function signature readable (→ List[Chunk]).
# Document: LlamaIndex’s lightweight wrapper around raw text.
# SimpleNodeParser: LlamaIndex utility that splits a Document into “nodes” (chunks) based on token limits and overlap.
# .base.ChunkerBase: Ensures we fulfill the interface promised in 04 IO-Contracts.
# .models.Chunk	Our JSON-friendly dataclass that flows to downstream modules.
"""
from pathlib import Path
from typing import List
from llama_index.readers.file import PDFReader
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

from .base import ChunkerBase
from .models import Chunk


class LlamaIndexChunker(ChunkerBase):
    """
    * Wraps LlamaIndex's SimpleNodeParser
    * Keeps a fixed token window + overlap, so Retriever can do locality.
    """

    def __init__(self, max_tokens: int = 1024, overlap: int = 64):
        # internal LI object; callers never see this
        #max_tokens: How many tokens go into one chunk (default 512).
        #overlap: How many tokens re-appear at both the end of chunk n and the start of chunk n+1 (default 64). Prevents context holes.
        #SimpleNodeParser.from_defaults() returns a ready-to-use parser that respects those limits.
        #I store that parser in a private attribute (_parser) so external code can’t reach into LlamaIndex internals.
        self._parser = SimpleNodeParser.from_defaults(
            chunk_size=max_tokens,
            chunk_overlap=overlap,
            include_metadata=True,
        )

    # -------- public API required by ChunkerBase --------
    def chunk(self, document_path: str) -> List[Chunk]:
        # 1. Safety check — does the file exist?
        path = Path(document_path)
        if not path.exists():
            raise FileNotFoundError(path)

        # 2. Read file into memory
        # text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".pdf":
            # Use LlamaIndex PDF reader
            li_docs = PDFReader().load_data(path)
        else:
            # Plain text fallback
            text = path.read_text(encoding="utf-8")
            li_docs = [Document(text=text, doc_id=path.stem)]

        # # 3. Wrap the raw text in a LlamaIndex Document
        # li_doc = Document(text=text, doc_id=path.stem)

        # 4. Ask the parser to split it into nodes
        # nodes = self._parser.get_nodes_from_documents([li_doc])
        nodes = self._parser.get_nodes_from_documents(li_docs)


        # 5. Convert each Node -> our Pydantic Chunk
        return [
            Chunk(
                doc_id=node.metadata.get("doc_id", path.stem),
                text=node.text,
                metadata={
                **node.metadata,
                "token_start": getattr(node, "start_char_idx", None),
                "token_end": getattr(node, "end_char_idx", None),
            },
            )
            for node in nodes
        ]

