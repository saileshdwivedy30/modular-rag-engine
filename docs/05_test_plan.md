
# 📄 Document 5: Component & Integration Test Plan

## 🎯 Purpose

Ensure all components:
- Work as intended in isolation (unit tests)
- Interact correctly with others (integration tests)
- Respect shared I/O contracts (see Doc 4)

This document lists **test cases** for both Inference and Context Engine to run independently **before integration**.

---

## ✅ 1. Chunker – Unit Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Parses text into chunks | PDF file | List of `Chunk` objects with metadata |
| ✅ Handles empty docs | Empty text | Empty list |
| ✅ Metadata presence | Valid doc | `chunk.metadata['source']` exists |

---

## ✅ 2. Embedder – Unit Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Valid text embedding | "Apple Q2 report" | `List[float]` of fixed dimension |
| ✅ Empty string | "" | Raises or returns zero vector |
| ✅ Same input = same output | "Test" x 2 | Identical embeddings |

---

## ✅ 3. Vector Store – Unit Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Add and search | Embeddings + chunks | Top-k relevant chunks |
| ✅ No match fallback | Random vector | Returns empty or lowest scores |
| ✅ Duplicate detection | Re-ingest same chunk | Handles idempotency or overwrites cleanly |

---

## ✅ 4. Retriever – Integration Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Full retrieval chain | Query string | Top-k `Chunk` list |
| ✅ Retriever respects k | Query + k=2 | Exactly 2 chunks returned |
| ✅ Edge case (gibberish) | Random string | Empty or fallback behavior |

---

## ✅ 5. PromptBuilder – Unit Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Builds prompt correctly | `query + chunks` | Structured prompt string |
| ✅ Handles empty chunks | `query + []` | Fallback prompt |
| ✅ Custom template loads | Switch format | Prompt matches expected style |

---

## ✅ 6. LLMClient – Unit Tests (Inference Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Basic prompt → answer | Valid prompt | Non-empty string |
| ✅ Error on empty prompt | "" | Exception or fallback |
| ✅ Timeout handling | Long prompt | Catches errors gracefully |

---

## ✅ 7. Evaluator – Unit Tests (Context Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Computes cosine sim | `query + chunks + answer` | Float between 0–1 |
| ✅ Missing data | Missing chunk | Returns partial eval gracefully |
| ✅ Returns full eval dict | Valid inputs | Dict with faithfulness, relevance, latency |

---

## ✅ 8. Logger – Unit Tests (Inference Engine)

### Test Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| ✅ Logs event to W&B | `event_type + payload` | Appears in dashboard |
| ✅ Handles large logs | Big chunk list | Logs safely |
| ✅ Invalid input | Non-dict payload | Throws validation error |

---

## 🔁 Integration Test Plan

Once unit tests pass, test the full flow:

### ✅ `/rag` Full Flow (Inference Engine + Context Engine)

| Step | Expected |
|------|----------|
| `query → retrieve()` | Top-k chunks |
| `chunks → build_prompt()` | Structured prompt |
| `prompt → complete()` | Answer from LLM |
| `answer → evaluate()` | Dict of metrics |
| `log()` | Outputs evaluation + latency |
| Response | JSON with all fields present |

---

## ⚙️ Test Fixtures & Examples

| Component | Example Fixture |
|----------|------------------|
| Chunk    | `Chunk(doc_id="123", text="Apple risk factors...", metadata={"source": "10K"})` |
| Query    | `"What are Apple’s top risks in 2023?"` |
| Prompt   | `"Context:\n- Apple faces ...\n\nQuestion: What are risks?"` |
| LLM Resp | `"Apple identified X, Y, Z risks in 2023..."` |
| Eval     | `{"faithfulness": 0.92, "retrieval_relevance": 0.88, "latency_ms": 721}` |

---

## 📦 Testing Tips

- Write unit tests using `pytest`
- Use mocks for LLMClient or Evaluator where external APIs exist
- Log and share fixtures across both devs for integration
- Include a notebook for testing retrieval + chunking end-to-end

---

## ✅ Completion Criteria

| Area              | Done? |
|-------------------|-------|
| Each module has unit test | ☐     |
| Integration `/rag` test | ☐     |
| Latency is logged        | ☐     |
| Output JSON is schema-valid | ☐     |


