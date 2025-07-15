### “Node” vs “Chunk” — what they are and why we convert one into the other

| Aspect                        | **LlamaIndex `Node`**                                                                                 | **Project `Chunk`**                                                                                      |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Origin**                    | Comes **from LlamaIndex** when you call a parser such as `SimpleNodeParser.get_nodes_from_documents`. | Custom **Pydantic dataclass** defined in `app/context/models.py`.                                        |
| **Python type**               | `llama_index.core.schema.Node` (or a subclass like `TextNode`).                                       | `app.context.models.Chunk`.                                                                              |
| **Typical attributes**        | • `text`\n• `start`, `end` (token indices)\n• `metadata`: dict with page, section, etc.               | • `doc_id`\n• `text`\n• `metadata`: the same dict **plus** we always include `token_start`, `token_end`. |
| **Mutable?**                  | Yes, plain class; changes don’t auto-validate.                                                        | Immutable-by-default (`pydantic`); fields validated and easy `.json()` export.                           |
| **Why LlamaIndex returns it** | Internal convenience object for subsequent LlamaIndex steps (embedding, retrieval, etc.).             | Our codebase wants a stable, framework-agnostic object that downstream modules & REST APIs can rely on.  |
| **JSON-friendly?**            | Not guaranteed; some fields aren’t serialisable out-of-the-box.                                       | Always JSON-serialisable (`chunk.json()`).                                                               |
| **Used by tests?**            | No—tests never import Node.                                                                           | Yes—unit tests assert `isinstance(c, Chunk)`.                                                            |
| **Goes into vector store?**   | *Could*, but then Inference Engine would depend on LlamaIndex.                                        | Yes—VectorStore wrapper stores `Chunk.text` & `Chunk.metadata`.                                          |

---

### Why the unit test cares

```python
assert all(isinstance(c, Chunk) for c in chunks)
```

* If you accidentally return raw **`Node`** objects, the `isinstance` check fails → test red.
* If you do the conversion like above, each item *is* a `Chunk`, so the test passes.

---

### Take-away

* **Node** = LlamaIndex’s internal record → great for LI pipelines but **not** portable.
* **Chunk** = your contract-compliant, JSON-safe version → travels through embedding, vector store, FastAPI responses, logs—without tying the rest of the code to LlamaIndex internals.



# ### Node vs Chunk — a side-by-side comparison you can keep in mind while you code

# | Feature                     | **LlamaIndex `Node`**                                                                                     | **Project `Chunk`**                                                                                                                           |
# | --------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
# | **Who creates it?**         | LlamaIndex parsers (`SimpleNodeParser`, `SentenceWindowNodeParser`, etc.).                                | Your adapter layer (`LlamaIndexChunker`) converts each Node to a Chunk.                                                                       |
# | **Python type**             | `llama_index.core.schema.TextNode` (or `ImageNode`, etc.).                                                | `app.context.models.Chunk` (Pydantic dataclass).                                                                                              |
# | **Primary purpose**         | Internal LI object used by LI’s own embeddings / retrieval; rich helper methods.                          | **Stable data contract** that downstream modules (Embedder, VectorStore, API) rely on—framework-agnostic & JSON-safe.                         |
# | **Key attributes**          | • `text`\n• `start_char_idx`, `end_char_idx` (token/char range)\n• `metadata` dict (page, section, etc.). | • `doc_id` (file stem or UUID)\n• `text`\n• `metadata` dict **guaranteed** to include `token_start` & `token_end` (copied from node indices). |
# | **Mutability / validation** | Plain class; no built-in validation.                                                                      | Pydantic model → automatic type-checking & `.model_dump_json()` ready for logs or APIs.                                                       |
# | **Serialization**           | Not JSON-friendly by default (e.g., contains non-serialisable objects).                                   | Always JSON-serialisable.                                                                                                                     |
# | **What tests expect**       | **Never appears in tests.**                                                                               | Unit tests assert `isinstance(item, Chunk)`.                                                                                                  |
# | **Where it’s used later**   | Only inside the Chunker adapter. Once converted, it’s discarded.                                          | Passed to Embedder → VectorStore → Retriever → PromptBuilder → Evaluator → FastAPI response.                                                  |

# ---

# ### Why bother converting?

# * **Decoupling** – If you ever swap LlamaIndex for a different framework (LangChain, custom splitter), only the adapter layer changes; the rest of the pipeline keeps consuming `Chunk`.
# * **Testing** – Pydantic objects are easy to validate and mock; you avoid bringing LlamaIndex into every unit test.
# * **API / logging** – Chunks can be serialised straight into FastAPI responses or JSONL logs without custom encoders.

# Think of **Node** as a *raw ingredient* produced by LlamaIndex’s kitchen, and **Chunk** as the *plated dish* your whole service agrees to eat.
