# 📄 Document 4: Shared Interface Contract Spec

## 🎯 Purpose

This document defines **strict interface contracts** between all modules. It ensures:

- ✅ Smooth parallel development between Inference and Context Engine
- ✅ Pluggability and modularity
- ✅ Easy swapping of components (LLM, retriever, vector store, etc.)
- ✅ Integration-safe refactoring

---

## 🔑 Object Definitions

These are the **data objects** that pass between components.

---

### 📦 `Chunk` Object

```python
class Chunk:
    def __init__(
        self,
        doc_id: str,
        text: str,
        metadata: Dict[str, Any]
    ):
        self.doc_id = doc_id
        self.text = text
        self.metadata = metadata
````

**Used by**: Chunker, Retriever, PromptBuilder, Evaluator

---

### 📦 `LLMResponse`

```python
class LLMResponse:
    def __init__(
        self,
        answer: str,
        raw_response: Optional[Dict] = None
    ):
        self.answer = answer
        self.raw_response = raw_response or {}
```

**Used by**: LLMClient, Evaluator, Logger

---

## 🧱 Component Interfaces

---

### 📄 1. Chunker

```python
class ChunkerBase:
    def chunk(document_path: str) -> List[Chunk]
```

* **Input**: `document_path` (str)
* **Output**: `List[Chunk]`

---

### 🧠 2. Embedder

```python
class EmbedderBase:
    def embed(text: str) -> List[float]
```

* **Input**: text string
* **Output**: dense vector (List\[float])

---

### 🗃️ 3. Vector Store

```python
class VectorStoreBase:
    def add(chunks: List[Chunk]) -> None
    def search(query_vector: List[float], k: int = 3) -> List[Chunk]
```

* `add()` is used during indexing
* `search()` is used during retrieval

---

### 🔍 4. Retriever

```python
class RetrieverBase:
    def retrieve(query: str, k: int = 3) -> List[Chunk]
```

* Internally: calls `embed()` → `search()`

---

### 🧾 5. PromptBuilder

```python
class PromptBuilderBase:
    def build_prompt(chunks: List[Chunk], query: str) -> str
```

* Input: relevant context + query
* Output: formatted prompt string

---

### 🤖 6. LLMClient

```python
class LLMClientBase:
    def complete(prompt: str, temperature: float = 0.7) -> str
```

* Input: prompt string
* Output: string completion (can be wrapped in `LLMResponse`)

---

### 🧪 7. Evaluator

```python
class EvaluatorBase:
    def evaluate(query: str, chunks: List[Chunk], answer: str) -> Dict[str, float]
```

* Output example:

```python
{
  "faithfulness": 0.92,
  "retrieval_relevance": 0.85,
  "latency_ms": 712
}
```

---

### 📜 8. Logger

```python
class LoggerBase:
    def log(event_type: str, payload: Dict[str, Any]) -> None
```

* Example:

```python
logger.log("eval", {"faithfulness": 0.91, "query": ..., "chunks": ...})
```

---

## ✅ Usage Summary

| Component     | Provides                  | Consumes                |
| ------------- | ------------------------- | ----------------------- |
| Chunker       | `List[Chunk]`             | raw document path       |
| Embedder      | `List[float]`             | chunk text or query     |
| Vector Store  | `List[Chunk]` from search | embedding               |
| Retriever     | `List[Chunk]`             | query string            |
| PromptBuilder | prompt string             | chunks + query          |
| LLMClient     | answer string             | prompt                  |
| Evaluator     | metrics dict              | query + chunks + answer |
| Logger        | Logs event                | any type + payload      |

---

## 📌 Integration Philosophy

* Every module must be **independently testable**
* Inputs/outputs should match these contracts exactly
* JSON-serializable objects (like `Chunk`, `LLMResponse`) are encouraged

