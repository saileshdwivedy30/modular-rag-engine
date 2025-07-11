# 01 System Overview


# 📄 Document 1: System Architecture Walkthrough

## 🎯 Goal

Build a **modular, production-grade Retrieval-Augmented Generation (RAG)** system for financial document Q&A using:

- 🧠 **LLaMA 3 8B AWQ** served via **vLLM on GKE**
- 📚 **Vector-based retrieval** using **Vertex AI embeddings** and **FAISS**
- ⚙️ Modular components for each pipeline stage
- 🧪 Built-in evaluation + monitoring for quality + latency
- 🔧 Flexible enough to be extended into agentic behavior later

---

## 🏗️ High-Level Pipeline Flow

```text
             ┌──────────────┐
             │  User Query  │
             └──────┬───────┘
                    ▼
            ┌──────────────┐
            │  FastAPI     │
            │  Backend     │
            └──────┬───────┘
     ┌─────────────┼──────────────┐
     ▼                            ▼
Embed Query             /completion (direct LLM)
     │
     ▼
Vertex AI Embedding → FAISS Vector Store → Retrieve Top-k Chunks
     ▼
Prompt Builder: Combine Chunks + Query → Prompt
     ▼
LLMClient: Send to vLLM → LLaMA3 (hosted on GKE)
     ▼
Answer
     ▼
Evaluator: Faithfulness, relevance, latency
     ▼
Logger: Metrics + Events → W&B or GCP
     ▼
Return Final Response (JSON)
````

---

## 🧱 Pipeline Components and Flow

### 1. **FastAPI Backend**

* Routes:

  * `/completion` → Direct prompt to LLM
  * `/rag` → Full pipeline: query → embed → retrieve → complete → evaluate
* Delegates to modular components based on config

---

### 2. **Chunker**

* Converts raw documents into metadata-rich text chunks
* Used offline before feeding documents into vector store
* Input: Raw PDF/text
* Output: `List[Chunk]` with `doc_id`, `text`, `metadata`

---

### 3. **Embedder (Vertex AI)**

* Converts query or chunk text into embedding vectors
* Wrapped inside LlamaIndex’s embedding interface

---

### 4. **Vector Store (FAISS or Chroma)**

* Stores chunk embeddings
* Returns top-k relevant chunks for query vector
* Swappable backend: local FAISS or cloud-hosted ChromaDB

---

### 5. **Retriever**

* Calls Embedder → Vector Store
* Returns the most relevant chunks for the query
* Input: `query: str`
* Output: `List[Chunk]`

---

### 6. **Prompt Builder**

* Merges query + retrieved chunks into a structured prompt
* Uses configurable templates
* Output: `prompt: str`

---

### 7. **LLM Client**

* Sends prompt to LLaMA 3 (served on GKE via vLLM)
* vLLM exposes an OpenAI-style endpoint
* Output: `answer: str`

---

### 8. **Evaluator**

* Evaluates the response:

  * Faithfulness (LLM-as-judge or similarity)
  * Retrieval quality
  * Latency
* Outputs a dict of metrics

---

### 9. **Logger**

* Records:

  * Latency
  * Vector search stats
  * Chunks used
  * Evaluation scores
* Target: W\&B or Google Cloud Logging

---

## 🔁 Modular Design Principles

Each component:

* Has a well-defined interface
* Can be swapped via config
* Can be unit-tested independently

---

## 🔄 Flow Breakdown (Step-by-Step)

| Step | Module         | Action Taken                 |
| ---- | -------------- | ---------------------------- |
| 1    | User → FastAPI | Sends query                  |
| 2    | Embedder       | Embeds query using Vertex AI |
| 3    | VectorStore    | Finds top-k similar chunks   |
| 4    | Retriever      | Combines embedder + search   |
| 5    | PromptBuilder  | Formats full prompt          |
| 6    | LLMClient      | Sends prompt to vLLM (GKE)   |
| 7    | Evaluator      | Measures quality + latency   |
| 8    | Logger         | Logs all metadata + eval     |
| 9    | FastAPI        | Returns answer JSON          |

---

## 🧠 Future-Ready: Agentic Extension Plan

Later, you can add an agent layer on top:

```text
Agent (ReAct or Planner)
     ↓
Tool: Retrieval Engine (this pipeline)
     ↓
Tool: Calculator, API caller, summarizer, etc.
```

---

## 📦 Key Technologies Used

| Component          | Tool/Framework            |
| ------------------ | ------------------------- |
| LLM Serving        | vLLM + LLaMA3             |
| Backend            | FastAPI                   |
| Vector Store       | FAISS (via LlamaIndex)    |
| Embedding          | Vertex AI                 |
| Chunking/Retrieval | LlamaIndex                |
| Monitoring         | Weights & Biases / GCP    |
| Evaluation         | Custom Python / LLM judge |

---

## ✅ Outputs at Each Layer

| Component      | Input                 | Output                    |
| -------------- | --------------------- | ------------------------- |
| Chunker        | raw document          | `List[Chunk]`             |
| Embedder       | text (query/chunk)    | `List[float]` (embedding) |
| Vector Store   | embedding             | `List[Chunk]`             |
| Retriever      | query                 | `List[Chunk]`             |
| Prompt Builder | query + chunks        | `prompt: str`             |
| LLMClient      | prompt                | `answer: str`             |
| Evaluator      | query, chunks, answer | `Dict[str, float]`        |
| Logger         | event type, metadata  | logged record             |

---

## 🔄 Team Interaction Points

| From Sailesh   | To Sweta                                 |
|----------------|------------------------------------------|
| FastAPI `/rag` | Calls Retriever, PromptBuilder           |
| LLMClient      | Used by Dev B to test prompt output      |
| Logger         | Accepts events from Eval, Retrieval, LLM |

| From Sweta    | To Sailesh                        |
|---------------|-----------------------------------|
| Retriever     | Returns chunks to Dev A's router  |
| PromptBuilder | Sends prompt to Dev A’s LLMClient |
| Evaluator     | Returns metrics to Dev A's Logger |

