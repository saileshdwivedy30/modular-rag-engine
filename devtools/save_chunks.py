# devtools/save_chunks.py

import json
from pathlib import Path
from app.context.chunker_li import LlamaIndexChunker
from app.context.models import Chunk

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"
with open(CONFIG_PATH) as f:
    cfg = json.load(f)

data_dir = Path(cfg["data_dir"])
chunk_params = cfg["chunk"]
chunker = LlamaIndexChunker(**chunk_params)

FILES = ["sample.txt", "apple_10q_q1_2025.pdf"]
output_dir = data_dir / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

for filename in FILES:
    path = data_dir / filename
    if not path.exists():
        print(f"Skipping missing file: {filename}")
        continue

    chunks = chunker.chunk(path)
    output_path = output_dir / f"{path.stem}_chunks.json"
    with open(output_path, "w") as f:
        json.dump([c.model_dump() for c in chunks], f, indent=2)

    print(f"✅ Saved {len(chunks)} chunks from {filename} → {output_path.name}")