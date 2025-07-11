# 📄Context Engine Component Guide

## 🧑‍💻 Responsibilities

You own all **RAG logic, embeddings, retrieval, chunking, prompting, evaluation**. You're responsible for:

- Chunking and ingesting financial documents
- Embedding queries/documents using Vertex AI
- Managing the vector store (FAISS/Chroma)
- Building retrievers and prompt templates
- Evaluating answer quality and retrieval relevance

---

## 📦 Component Summary

| Component Name     | Type        | Description                              |
|--------------------|-------------|------------------------------------------|
| Chunker            | Module      | Converts raw docs into `Chunk` objects   |
| Embedder           | Module      | Uses Vertex AI to embed text             |
| Vector Store       | Module      | Stores/retrieves from FAISS/Chroma       |
| Retriever          | Module      | Wraps embedder + vector store            |
| Prompt Builder     | Module      | Formats prompt using context             |
| Evaluator          | Module      | Scores faithfulness, latency, relevance  |

---

## 1. 📄 Chunker

### Purpose
- Ingest PDFs or plain text and produce text chunks with metadata

### Tools
- `LlamaIndex.DocumentLoader` or `PyMuPDF`, `pdfplumber`, `BeautifulSoup`

### Input
```python
document: str  # path or string
````

### Output

```python
List[Chunk]  # with doc_id, text, metadata
```

### Interface

```python
class ChunkerBase:
    def chunk(document_path: str) -> List[Chunk]
```

### Interacts With

* Vector Store (for ingestion)
* Evaluator (to trace origin of answer)

---

## 2. 🧠 Embedder

### Purpose

* Convert query/chunk into dense vector via Vertex AI

### Tools

* `google.cloud.aiplatform.EmbeddingsClient`

### Input

```python
text: str
```

### Output

```python
embedding: List[float]
```

### Interface

```python
class EmbedderBase:
    def embed(text: str) -> List[float]
```

### Interacts With

* Retriever (query embedding)
* VectorStore (chunk embedding)

---

## 3. 🗃️ Vector Store (FAISS / Chroma)

### Purpose

* Store chunk embeddings
* Search similar vectors given a query

### Tools

* `faiss` + `LlamaIndex.VectorStoreIndex` or `Chroma`

### Input

* `add()`: `List[Chunk]`
* `search()`: `query_embedding: List[float]`

### Output

* `List[Chunk]` (top-k matches)

### Interface

```python
class VectorStoreBase:
    def add(chunks: List[Chunk]) -> None
    def search(query_vector: List[float], k: int) -> List[Chunk]
```

### Interacts With

* Retriever
* Evaluation

---

## 4. 🔍 Retriever

### Purpose

* Query → Embedding → Search → Return top chunks

### Tools

* `LlamaIndex.SimpleVectorRetriever`

### Input

```python
query: str
k: int
```

### Output

```python
List[Chunk]
```

### Interface

```python
class RetrieverBase:
    def retrieve(query: str, k: int = 3) -> List[Chunk]
```

### Interacts With

* FastAPI RAG route (Dev A)
* PromptBuilder
* Evaluation

---

## 5. 🧾 Prompt Builder

### Purpose

* Format a prompt with context + query
* Optionally support template swapping via config

### Tools

* `LlamaIndex.PromptTemplate` or Jinja2 templates

### Input

```python
chunks: List[Chunk], query: str
```

### Output

```python
prompt: str
```

### Interface

```python
class PromptBuilderBase:
    def build_prompt(chunks: List[Chunk], query: str) -> str
```

### Interacts With

* FastAPI orchestrator
* LLMClient

---

## 6. 🧪 Evaluator

### Purpose

* Evaluate:

  * **Faithfulness** (LLM-as-judge, optionally)
  * **Retrieval accuracy** (embedding match)
  * **Latency** (tracked in Dev A)
* Return a score dictionary

### Tools

* `sentence_transformers`, `numpy`, OpenAI judge (optional)

### Input

```python
query: str
chunks: List[Chunk]
answer: str
```

### Output

```python
Dict[str, float]
```

### Interface

```python
class EvaluatorBase:
    def evaluate(query: str, chunks: List[Chunk], answer: str) -> Dict
```

### Interacts With

* FastAPI RAG route (Dev A)
* Logger (Dev A)

---

## 🧠 Context Engine Integration Checklist

| Task                         | Status |
| ---------------------------- | ------ |
| Build chunker for 10-K docs  | ☐      |
| Implement Vertex AI embedder | ☐      |
| Wrap FAISS as VectorStore    | ☐      |
| Implement `Retriever`        | ☐      |
| Format prompt using chunks   | ☐      |
| Build evaluator module       | ☐      |
| Log to console or W\&B       | ☐      |

---

## 🔄 Output to Inference Engine

| Component      | Format (I/O Contract)                |
| -------------- | ------------------------------------ |
| Retriever      | `retrieve(query) -> List[Chunk]`     |
| Prompt Builder | `build_prompt(chunks, query) -> str` |
| Evaluator      | `evaluate(...) -> Dict[str, float]`  |

---

## ✅ Summary

Context Engine owsn:

* Data ingestion and document parsing
* Vertex AI embedding and query encoding
* Chunk storage and vector search
* Retrieval and prompt formatting
* Evaluation of generated answers

Provides clean, pluggable modules that Inference Engine can call via interface contracts.

