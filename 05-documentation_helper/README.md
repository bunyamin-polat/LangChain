# 🦜 Documentation Helper

<div align="center">

**A RAG chatbot that answers questions about the LangChain docs, with cited sources**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-1C3C3C.svg)](https://langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Pinecone](https://img.shields.io/badge/Pinecone-🌲-000000.svg)](https://pinecone.io/)
[![Tavily](https://img.shields.io/badge/Tavily-🔍-8A2BE2.svg)](https://tavily.com/)
[![uv](https://img.shields.io/badge/uv-dependency%20management-DE5FE9.svg)](https://docs.astral.sh/uv/)

</div>

## 🎯 Overview

A small RAG chatbot for the LangChain documentation, inspired by
[chat.langchain.com](https://chat.langchain.com/). Tavily crawls and extracts the docs,
OpenAI embeds the chunks into Pinecone, and a LangChain agent retrieves relevant context
to answer questions with cited sources — all served through a Streamlit chat UI.

## ✨ Key Features

- 🌐 **Web crawling** — `TavilyCrawl` pulls live content straight from `docs.langchain.com`, no manual scraping or static dumps
- 📚 **Chunking** — `RecursiveCharacterTextSplitter` breaks crawled pages into ~4000-character chunks with overlap
- 🔍 **Vector storage** — chunks are embedded with `text-embedding-3-small` and indexed in Pinecone for similarity search
- ⚡ **Concurrent indexing** — `backend/ingestion.py` upserts batches into Pinecone in parallel via `asyncio.gather`
- 🎯 **Tool-driven retrieval** — the agent decides when to call `retrieve_context` rather than always stuffing context into the prompt
- 🧠 **Grounded, cited answers** — the system prompt requires the model to answer from retrieved context and cite sources, or say it doesn't know
- 💬 **Chat interface** — Streamlit UI with persistent session history and a collapsible sources panel per answer
- 🪵 **Server-side logging** — both ingestion and the live query path (`app.py` → `backend/core.py`) log through `backend/logger.py`, so failures leave a trace beyond the UI

## Project layout

```text
05-documentation_helper/
├── app.py                 # Streamlit entrypoint (chat UI)
├── backend/
│   ├── core.py             # RAG pipeline: retrieve_context tool + run_llm()
│   ├── ingestion.py         # crawl → chunk → embed → upsert into Pinecone
│   └── logger.py            # shared colored console logging
└── notebooks/              # standalone Tavily exploration notebooks
```

## What it does

- **`backend/ingestion.py`** — crawls `docs.langchain.com` with `TavilyCrawl` (`max_depth=5`,
  advanced extraction), converts the results into `Document`s, splits them into
  ~4000-character chunks with `RecursiveCharacterTextSplitter`, and upserts them into
  Pinecone in concurrent batches. Skips pages Tavily couldn't extract content from and
  logs progress via `backend/logger.py`. Run this once (or whenever the docs change)
  before using the app.
- **`backend/core.py`** — the RAG pipeline. `retrieve_context` is a `@tool` that queries
  the same Pinecone index and returns both a text-serialized version of the matched
  chunks (for the LLM to read) and the raw `Document` objects (as an artifact, for the
  app to show as sources). The chat model, retriever, and agent are all built once at
  import time and reused across requests. `run_llm()` invokes that agent, logs (and
  re-raises) any failure, and returns the answer plus the context documents used.
- **`app.py`** — a Streamlit chat interface: keeps conversation history in
  `st.session_state`, calls `run_llm()` on each question, logs the query and any
  failure server-side, and renders the answer with its sources in a collapsible
  expander.
- **`notebooks/Tavily_Crawl_Demo.ipynb`** / **`notebooks/Tavily_Crawl_Tutorial.ipynb`**
  — standalone notebooks exploring `TavilyMap`, `TavilyExtract`, and `TavilyCrawl`
  independently of the app (install their own deps, prompt for the API key
  interactively). Useful for understanding what the ingestion pipeline is doing under
  the hood, including how `instructions`-guided crawling narrows results compared to a
  plain crawl.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- An [OpenAI](https://platform.openai.com/) API key (embeddings + chat model)
- A [Pinecone](https://www.pinecone.io/) index already created (1536 dimensions, to
  match `text-embedding-3-small`)
- A [Tavily](https://tavily.com/) API key (crawling in `backend/ingestion.py` and the notebooks)
- Run `backend/ingestion.py` before `app.py` — the Pinecone index needs to be populated first

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `OPENAI_API_KEY` | Yes — embeddings and chat model |
| `PINECONE_API_KEY` | Yes — read implicitly by `langchain-pinecone` |
| `INDEX_NAME` | Yes — Pinecone index shared by `backend/ingestion.py` and `backend/core.py` |
| `TAVILY_API_KEY` | Yes — used by `backend/ingestion.py`'s crawler |
| `MODEL_NAME` | No — chat model id, defaults to `gpt-5.2` |
| `GOOGLE_API_KEY` | Not used by default |
| `LANGSMITH_API_KEY` | Not used by default |

## Setup & run

```bash
cd projects/05-documentation_helper
uv sync
uv run python -m backend.ingestion   # crawl the docs and populate the Pinecone index (run once)
uv run streamlit run app.py          # start the chat UI at http://localhost:8501
```

`backend/ingestion.py` is run with `-m` (as a package module, not a bare script) because
it uses a relative import (`from .logger import ...`) to reach `backend/logger.py`.

## Notes

- `backend/ingestion.py` and `backend/core.py` must point at the same vector store —
  both read `INDEX_NAME` from `.env`, so make sure it's set before running either.
- The notebooks manage their own API key input (`getpass`) and don't share state with
  the rest of the project — they're meant to be run independently.
