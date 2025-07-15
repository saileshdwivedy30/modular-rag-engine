from pathlib import Path
import sys, pathlib
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

# --- make repo imports work when run as standalone -------------
repo_root = pathlib.Path(__file__).resolve().parent
sys.path.append(str(repo_root))      # assumes script is in repo root
from app.context.models import Chunk

# --- create sample text file -----------------------------------
Path("demo.txt").write_text("Hello world! " * 40)

# --- build node ------------------------------------------------
doc = Document(text=Path("demo.txt").read_text(), doc_id="demo")
parser = SimpleNodeParser.from_defaults(chunk_size=32, chunk_overlap=8)
node = parser.get_nodes_from_documents([doc])[0]

print("Node type    :", type(node))               # TextNode
print("Node attrs   :", node.start_char_idx, node.end_char_idx)

# --- convert Node -> Chunk -------------------------------------
chunk = Chunk(
    doc_id=node.metadata.get("doc_id", "demo"),
    text=node.text,
    metadata={
        "token_start": node.start_char_idx,
        "token_end": node.end_char_idx,
    },
)

print("Chunk type   :", type(chunk))              # Chunk
print("Chunk JSON   :", chunk.model_dump_json(indent=2)[:150], "…")


# Output_example (Terminal Output):
# (cloudrag) swetapati@Swetas-MacBook-Air modular-rag-engine % python node_vs_chunk.py
# Metadata length (0) is close to chunk size (32). Resulting chunks are less than 50 tokens. Consider increasing the chunk size or decreasing the size of your metadata to avoid this.
# Node type    : <class 'llama_index.core.schema.TextNode'>
# Node attrs   : 0 103
# Chunk type   : <class 'app.context.models.Chunk'>
# Chunk JSON   : {
#   "doc_id": "demo",
#   "text": "Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world! Hello world!",
#   "metadata …
# (cloudrag) swetapati@Swetas-MacBook-Air modular-rag-engine % 