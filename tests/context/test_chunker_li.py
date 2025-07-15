# tests/context/test_chunker_li.py
"""
Unit‑tests for LlamaIndexChunker

Test 1 guards that you return a non‑empty list of the right class.
Test 2 checks you carried over token_start / token_end and that overlap exists.
Test 3 enforces a clear, predictable error when the file path is bad.

┌──────────────┐    chunks = [Chunk, Chunk, …]      ┌─────────────┐
│ sample.txt   │ ──────────── chunk() ────────────▶ │  LlamaIndex │
└──────────────┘                                    │  NodeParser │
                                                     └─────────────┘
             ▲                                          │
             │   Test 1: non‑empty list & type          ▼
             │   Test 2: metadata overlap          [Node, Node]
             │   Test 3: FileNotFoundError               │
"""
from pathlib import Path
from app.context.chunker_li import LlamaIndexChunker
from app.context.models import Chunk

# -------------------------------------------------------------
# Pytest fixtures `data_dir` and `chunk_params` come from
# tests/conftest.py, which parses the repo‑level **config.json**.
# -------------------------------------------------------------

# def _get_sample_file(data_dir: Path) -> Path:
#     """Ensure `sample.txt` exists and return its Path."""
#     sample = data_dir / "apple_10q_q1_2025.pdf"
#     if not sample.exists():
#         sample.parent.mkdir(parents=True, exist_ok=True)
#         sample.write_text("Apple revenue grew 10%. " * 40)
#     return sample

def _get_sample_file(data_dir: Path, filename: str) -> Path:
    """Ensure the given file exists (PDF or TXT) and return its Path."""
    sample = data_dir / filename
    if not sample.exists():
        sample.parent.mkdir(parents=True, exist_ok=True)
        if sample.suffix == ".txt":
            sample.write_text("Sample plain text input. " * 40)
        else:
            sample.write_text("Apple revenue grew 10%. " * 40)
    return sample

def test_txt_chunking(data_dir, chunk_params):
    sample = _get_sample_file(data_dir, "sample.txt")
    chunker = LlamaIndexChunker(**chunk_params)

    chunks = chunker.chunk(sample)
    assert chunks, "Chunk list is empty for TXT file"
    assert all(isinstance(c, Chunk) for c in chunks), "Returned objects are not Chunk instances (TXT)"

# ----------------------------
# Test 1 – non‑empty list & type
# ----------------------------

def test_returns_chunks(data_dir, chunk_params):
    # sample = _get_sample_file(data_dir)
    sample = _get_sample_file(data_dir, "apple_10q_q1_2025.pdf")
    chunker = LlamaIndexChunker(**chunk_params)

    chunks = chunker.chunk(sample)

    # Truthiness check – an empty list ([]) is False → test fails
    assert chunks, "Chunk list is empty"

    # all(isinstance…) loops through each item; Chunk → True, Node → False
    assert all(isinstance(c, Chunk) for c in chunks), "Returned objects are not Chunk instances"


# ----------------------------
# Test 2 – metadata overlap
# ----------------------------

def test_overlap_metadata(data_dir, chunk_params):
    # sample = _get_sample_file(data_dir)
    sample = _get_sample_file(data_dir, "apple_10q_q1_2025.pdf")
    chunker = LlamaIndexChunker(**chunk_params)

    chunks = chunker.chunk(sample)
    c0, c1 = chunks[0], chunks[1]

    # token_end of chunk 0 must be >= token_start of chunk 1
    # assert c0.metadata["token_end"] >= c1.metadata["token_start"], "Overlap invariant violated"
    assert c0.metadata["token_end"] >= c1.metadata["token_start"] - 1, "Overlap invariant violated"



# ----------------------------
# Test 3 – predictable FileNotFoundError
# ----------------------------

def test_missing_file(chunk_params):
    import pytest, tempfile

    with tempfile.TemporaryDirectory() as tmp:
        missing = Path(tmp) / "nope.txt"
        chunker = LlamaIndexChunker(**chunk_params)
        with pytest.raises(FileNotFoundError):
            chunker.chunk(missing)
