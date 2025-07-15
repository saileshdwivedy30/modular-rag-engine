# tests/context/conftest.py
import json, pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# -----------------------------------------------
@pytest.fixture(scope="session")
def cfg():
    """Load repo-level config.json once per test session."""
    with open(REPO_ROOT / "config.json") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def data_dir(cfg):
    """Path object for the raw-data folder."""
    return REPO_ROOT / cfg["data_dir"]

@pytest.fixture(scope="session")
def chunk_params(cfg):
    """Dict with default max_tokens / overlap."""
    return cfg["chunk"]
# -----------------------------------------------
