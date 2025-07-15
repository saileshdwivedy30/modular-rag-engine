# Modular‑RAG‑Engine

A production‑ready **Retrieval‑Augmented Generation (RAG)** pipeline for financial‑document Q\&A, split into two independently deployable engines.

| Folder           | Owner          | What lives here                                                               |
| ---------------- | -------------- | ----------------------------------------------------------------------------- |
| `app/inference/` | Inference team | FastAPI service, vLLM runner, `/completion` & `/rag` endpoints, logging layer |
| `app/context/`   | Context team   | Chunker → Embedder → Vector Store → Retriever → PromptBuilder → Evaluator     |

---

## 🖥 Local dev setup (Apple‑silicon macOS 14, **Python 3.11.9**)

> The steps below keep the macOS‑shipped Python 3.9 intact. All work happens in a per‑project interpreter managed by **pyenv** and isolated in a `cloudrag` virtual‑env.

\### 1  Clone & check out your long‑lived dev branch

```bash
$ git clone https://github.com/saileshdwivedy30/modular-rag-engine.git
$ cd modular-rag-engine
$ git checkout -b context-engine    # or inference-engine
```

\### 2  Install / wire up **pyenv** (one time)

```bash
$ brew install pyenv
```

Add to **\~/.zshrc** (**ASCII dashes only!**):

```zsh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Reload:

```bash
$ exec $SHELL
```

\### 3  Install & pin Python 3.11.9 **inside this repo**

```bash
$ pyenv install 3.11.9          # skip if already present
$ pyenv local 3.11.9            # writes .python-version here
$ python --version              # → Python 3.11.9
```

\### 4  Create & activate the project venv

```bash
$ python -m venv cloudrag
$ source cloudrag/bin/activate
```

> **Tip:** add `cloudrag/` to **.gitignore** so the venv is never committed.

\### 5  Install dependencies (runtime + dev)

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt   # runtime + dev packages
```

Runtime pkgs: **pydantic, pdfminer.six, tiktoken**
Dev pkgs: **pytest, pytest‑cov**

\### 6  Run tests

```bash
$ pytest -q              # all green
```

Reactivate the venv in new terminals with:

```bash
$ source cloudrag/bin/activate
```

---

## 📂 Branch & PR workflow (condensed)

1. **Sync your dev branch**

   ```bash
   git checkout context-engine
   git pull origin context-engine
   ```
2. **Feature branch**

   ```bash
   git checkout -b feature/context/chunker
   ```
3. **Code → pytest → commit small, meaningful messages.**
4. **Push & open PR** → `feature/*` ➜ `context-engine`.
5. **CI must pass**, teammate reviews → squash & merge.
6. **Pull latest** before the next feature.

---

## 🧪 Pytest commands

| Command            | What it does                 |
| ------------------ | ---------------------------- |
| `pytest -q`        | run all tests quietly        |
| `pytest --cov app` | show coverage (% gate in CI) |

---

## 🤝 Contributing etiquette

* One logical change → one PR.
* Never break contracts in `docs/04_io_contracts.md`.
* Leave `main` deployable at all times.

Happy hacking! 🚀
