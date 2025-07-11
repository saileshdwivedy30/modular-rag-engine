# 📄 Inference Engine Component Guide

## 🧑‍💻 Responsibilities

All the **infrastructure, serving, orchestration, API, and logging components**. You’re responsible for:

- Hosting the model (vLLM + LLaMA 3 on GKE)
- Exposing APIs using FastAPI
- Implementing `LLMClient` to connect to vLLM
- Logging + monitoring all system events
- Orchestrating the `/completion` and `/rag` endpoints

---

## 📦 Component Summary

| Component Name       | Type        | Description                              |
|----------------------|-------------|------------------------------------------|
| GKE + vLLM           | Infra       | Runs LLaMA 3 with vLLM OpenAI server     |
| FastAPI Backend      | Backend     | Entry point for all API routes           |
| LLMClient            | Module      | Wrapper to call vLLM from Python         |
| Logger               | Module      | Sends logs to W&B or GCP                 |
| RAG Orchestrator     | Logic       | Pipeline: retrieve → prompt → complete   |
| Config System        | Utility     | Defines which components to load         |

---

## 1. 🏗️ GKE + vLLM Deployment

### Purpose
- Deploy vLLM + LLaMA 3 8B AWQ on a GPU-backed GKE cluster.
- Expose OpenAI-compatible endpoint (e.g., `/v1/completions`)

### Expected Tools
- `vllm` (Docker or pip)
- GKE with 1x L4 GPU node
- Google Container Registry (for custom images)

### Inputs
- Dockerfile
- LLaMA 3 checkpoint
- Ingress config

### Outputs
- Accessible OpenAI-compatible endpoint (e.g. `http://ip:8000/v1/completions`)

### Interactions
- `LLMClient` will call this endpoint

---

## 2. 🚀 FastAPI Backend

### Purpose
- Expose REST API to users: `/completion`, `/rag`, `/healthz`

### Expected Tools
- `FastAPI`
- `uvicorn`
- `pydantic` for request/response models

### Inputs
- HTTP JSON requests

### Outputs
- JSON response with answer, metadata, and eval metrics

### Interactions
- Uses `LLMClient`, `Retriever`, `PromptBuilder`, `Evaluator`, `Logger`

---

## 3. 🤖 LLMClient

### Purpose
- Python interface to send prompts to vLLM server

### Expected Tools
- `requests` or `httpx` to call vLLM endpoint

### Input
```python
prompt: str
temperature: float = 0.7
````

### Output

```python
response: str
```

### Interface

```python
class LLMClientBase:
    def complete(prompt: str, temperature: float = 0.7) -> str
```

### Interactions

* Called by `FastAPI` in `/completion` and `/rag` routes
* Uses config to determine base URL and model settings

---

## 4. 🧾 Logger

### Purpose

* Log events, latency, evaluation metrics to GCP or W\&B

### Expected Tools

* `wandb`, `logging`, `google.cloud.logging`

### Input

```python
event_type: str
payload: Dict
```

### Output

* Console, GCP Logs, or W\&B dashboard

### Interface

```python
class LoggerBase:
    def log(event_type: str, payload: Dict) -> None
```

### Interactions

* Called after each request is completed in API

---

## 5. 🔁 RAG Orchestrator

### Purpose

* Main router for the `/rag` endpoint
* Chains together:

  * `Retriever` (from Retriever component)
  * `PromptBuilder` (from Retriever component)
  * `LLMClient`
  * `Evaluator` (from Retriever component)
  * `Logger`

### Expected Tools

* Native Python logic

### Input

```python
query: str
top_k: int
```

### Output

```json
{
  "answer": "...",
  "chunks_used": [...],
  "eval": { ... },
  "latency_ms": ...
}
```

### Interactions

* Calls: `Retriever`, `PromptBuilder`, `LLMClient`, `Evaluator`, `Logger`
* Respects the interfaces defined in the shared contract doc

---

## 6. ⚙️ Config System

### Purpose

* Determine which implementation of each module to load
* Enables swapping vector store, LLM, retriever, etc.

### Expected Tools

* `pydantic`, `yaml`, or native config parser

### Input

* Config file

### Output

* Instantiated modules

### Interactions

* Used by FastAPI app to initialize modules on startup

---

## 🧠 Inference Engine Integration Checklist

| Task                            | Status |
| ------------------------------- | ------ |
| Deploy vLLM on GKE (LLaMA 3 8B) | ☐      |
| Expose OpenAI-style endpoint    | ☐      |
| Write `LLMClient` abstraction   | ☐      |
| Setup `FastAPI` with routes     | ☐      |
| Create `Logger` (W\&B or GCP)   | ☐      |
| Implement `/completion` route   | ☐      |
| Implement `/rag` orchestrator   | ☐      |
| Load modules via config         | ☐      |

---

## 🔄 Inputs from Context Enginer (Expected)

| Component     | Interface Used                    | Purpose                     |
| ------------- | --------------------------------- | --------------------------- |
| Retriever     | `retrieve(query, k) -> [Chunk]`   | Get top-k chunks from FAISS |
| PromptBuilder | `build_prompt(chunks, query)`     | Create prompt string        |
| Evaluator     | `evaluate(query, chunks, answer)` | Output quality + latency    |

---

## ✅ Summary

Inference Engine Owns:

* The serving infra + model hosting (vLLM)
* The HTTP API layer + response schema
* All orchestration logic + logging
* LLM communication and metrics reporting

Context Engine provides with:

* Retrieval and Prompt modules
* Evaluation functions
* FAISS/Chroma setup
