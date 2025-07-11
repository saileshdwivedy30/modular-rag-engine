# 🤝 GitHub Collaboration Guide – RAG System (Inference + Context)

## 👥 Team Roles

| Role             | Git Branch        | Responsibilities                                     |
|------------------|-------------------|------------------------------------------------------|
| Inference Engine | `inference-engine`| API, vLLM, LLMClient, orchestration, logging         |
| Context Engine   | `context-engine`  | Chunking, embedding, retrieval, prompt building, eval|

---

## 📁 Repository Structure

```bash
llama-rag-finance/
├── app/
│   ├── inference/       # Inference team code
│   ├── context/         # Context team code
│   └── main.py          # FastAPI orchestrator
├── docs/                # All project documentation
├── tests/               # All unit + integration tests
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🌳 Git Branch Strategy

| Branch Name       | Purpose                                    |
|-------------------|--------------------------------------------|
| `main`            | Production-ready, stable build             |
| `inference-engine`| Dev A's work on LLM, API, server, logging  |
| `context-engine`  | Dev B's work on RAG modules, retrieval     |
| `feature/*`       | Optional branches for experimental features|

---

## 🔁 Development Workflow

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/your-org/llama-rag-finance.git
cd llama-rag-finance
git checkout -b inference-engine  # or context-engine
```

---

### ✅ 2. Work in Your Branch

- Use your assigned folder (`/app/inference/` or `/app/context/`)
- Follow contracts in `docs/04_io_contracts.md`
- Add tests under `/tests/`

---

### ✅ 3. Commit Often

```bash
git add .
git commit -m "feat: add initial Retriever class using FAISS"
```

---

### ✅ 4. Push to GitHub

```bash
git push origin context-engine
```

---

### ✅ 5. Open a Pull Request to `main`

- Title: `feat: add LLMClient wrapper for vLLM`
- Description: Include what changed, checklist, and test output
- Tag your teammate for review

---

### ✅ 6. Review PRs

- Use inline comments
- Approve after test results
- Merge only after all checks pass

---

## 🧪 Testing Guidelines

- All modules must be **unit-testable**
- Add tests to `/tests/`:
  - `test_retriever.py`
  - `test_llm_client.py`
  - `test_eval.py`
- Use `pytest` or `unittest`
- Run tests locally before pushing

---

## 📦 Best Practices

| Task                        | Tip                                  |
|-----------------------------|---------------------------------------|
| Sync with `main`            | `git pull origin main` into your branch |
| Avoid merge conflicts       | Pull before you push                 |
| Keep PRs focused            | One task = one PR                    |
| Review carefully            | Respect API contract doc             |
| Commit meaningful messages  | e.g., "fix: handle empty chunks edge case" |

---

## ✅ Integration Flow

| Component         | Owned by        | Consumed by       |
|------------------|------------------|-------------------|
| LLMClient         | Inference Engine | `/rag` endpoint   |
| Retriever         | Context Engine   | FastAPI route     |
| PromptBuilder     | Context Engine   | InferenceEngine   |
| Evaluator         | Context Engine   | Logger            |

Use mocks or stubs to simulate these during local dev.

---

## 📝 Merge Checklist

Before merging to `main`:
- [ ] All tests pass
- [ ] Interfaces match shared contract (see `docs/04_io_contracts.md`)
- [ ] PR is reviewed by teammate
- [ ] Documentation updated if needed

---

## 🛠 Tooling Tips

| Tool           | Use For                            |
|----------------|-------------------------------------|
| GitHub Issues  | Track bugs or questions             |
| GitHub Projects| Visual task board (optional)        |
| GitHub Actions | CI/CD integration if added later    |
| Markdown Docs  | Developer communication & contracts |

---

## 🧠 Communication & Sync

- Leave comments in PRs for blockers or design questions
- Use shared `.md` docs for schema/interface reference
- Coordinate API breakages before changing shared objects

---

## 🏁 Summary

- Each dev works in their **own branch**
- Use **clean folder structure** (`/app/inference`, `/app/context`)
- Write **tests and interface-compliant code**
- Open clean PRs → review → merge to `main`
- Communicate async via GitHub and docs

---

Let’s build like professionals 🚀