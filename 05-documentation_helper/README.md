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
- ⚡ **Concurrent indexing** — `ingestion.py` upserts batches into Pinecone in parallel via `asyncio.gather`
- 🎯 **Tool-driven retrieval** — the agent decides when to call `retrieve_context` rather than always stuffing context into the prompt
- 🧠 **Grounded, cited answers** — the system prompt requires the model to answer from retrieved context and cite sources, or say it doesn't know
- 💬 **Chat interface** — Streamlit UI with persistent session history and a collapsible sources panel per answer

## What it does

- **`ingestion.py`** — crawls `docs.langchain.com` with `TavilyCrawl` (`max_depth=5`,
  advanced extraction), converts the results into `Document`s, splits them into
  ~4000-character chunks with `RecursiveCharacterTextSplitter`, and upserts them into
  Pinecone in concurrent batches. Skips pages Tavily couldn't extract content from and
  logs progress via `logger.py`. Run this once (or whenever the docs change) before
  using the app.
- **`backend/core.py`** — the RAG pipeline. `retrieve_context` is a `@tool` that queries
  the same Pinecone index and returns both a text-serialized version of the matched
  chunks (for the LLM to read) and the raw `Document` objects (as an artifact, for the
  app to show as sources). `run_llm()` wraps this tool in a `create_agent` with a
  system prompt that instructs the model to always ground its answer in retrieved
  context and cite sources.
- **`main.py`** — a Streamlit chat interface: keeps conversation history in
  `st.session_state`, calls `run_llm()` on each question, and renders the answer with
  its sources in a collapsible expander.
- **`Tavily_Crawl_Demo.ipynb`** / **`Tavily_Crawl_Tutorial.ipynb`** — standalone
  notebooks exploring `TavilyMap`, `TavilyExtract`, and `TavilyCrawl` independently of
  the app (install their own deps, prompt for the API key interactively). Useful for
  understanding what the ingestion pipeline is doing under the hood, including how
  `instructions`-guided crawling narrows results compared to a plain crawl.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- An [OpenAI](https://platform.openai.com/) API key (embeddings + chat model)
- A [Pinecone](https://www.pinecone.io/) index already created (1536 dimensions, to
  match `text-embedding-3-small`)
- A [Tavily](https://tavily.com/) API key (crawling in `ingestion.py` and the notebooks)
- Run `ingestion.py` before `main.py` — the Pinecone index needs to be populated first

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `OPENAI_API_KEY` | Yes — embeddings and chat model |
| `PINECONE_API_KEY` | Yes — read implicitly by `langchain-pinecone` |
| `INDEX_NAME` | Yes — Pinecone index shared by `ingestion.py` and `backend/core.py` |
| `TAVILY_API_KEY` | Yes — used by `ingestion.py`'s crawler |
| `GOOGLE_API_KEY` | Not used by default |
| `LANGSMITH_API_KEY` | Not used by default |

## Setup & run

```bash
cd projects/05-documentation_helper
uv sync
uv run ingestion.py       # crawl the docs and populate the Pinecone index (run once)
uv run streamlit run main.py   # start the chat UI at http://localhost:8501
```

## Notes

- `ingestion.py` and `backend/core.py` must point at the same vector store — both read
  `INDEX_NAME` from `.env`, so make sure it's set before running either.
- The notebooks manage their own API key input (`getpass`) and don't share state with
  the rest of the project — they're meant to be run independently.
