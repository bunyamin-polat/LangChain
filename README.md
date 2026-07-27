# 🦜 LangChain Playground

<div align="center">

**Five hands-on projects built with [LangChain](https://github.com/langchain-ai/langchain), from a one-line chain to a full RAG chatbot — each in its own self-contained folder.**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-1C3C3C.svg)](https://github.com/langchain-ai/langchain)
[![Ollama](https://img.shields.io/badge/Ollama-local_LLM-000000.svg)](https://ollama.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt--5.2-412991.svg?logo=openai&logoColor=white)](https://platform.openai.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-🌲-000000.svg)](https://www.pinecone.io/)
[![Tavily](https://img.shields.io/badge/Tavily-🔍_web_search-8A2BE2.svg)](https://tavily.com/)
[![uv](https://img.shields.io/badge/uv-dependency%20management-DE5FE9.svg)](https://docs.astral.sh/uv/)

</div>

## 🎯 Overview

Each numbered folder is an independent, from-scratch project — its own `pyproject.toml`, its own `.venv`, its own `README.md`. They build on each other conceptually (a single `prompt | llm` chain → an agent with tools → the same agent peeled down to raw function calls → a minimal RAG pipeline → a full RAG chatbot with a UI), but there's no shared code between them: pick any folder and run it on its own.

## 🗂️ Projects

| # | Project | Pattern | Core Idea |
|---|---------|---------|-----------|
| 01 | [Hello World](01-hello_world/) | **Chain** | `prompt \| llm` over a local `ChatOllama` model — the simplest possible LangChain pipeline |
| 02 | [ReAct Search Agent](02-react_search_agent/) | **ReAct + tools** | `create_agent` with a `TavilySearch` tool, contrasting structured vs. raw output and a custom `@tool` |
| 03 | [Agents Under the Hood](03-agents_under_the_hood/) | **Tool-calling internals** | The same shopping-assistant agent reimplemented three ways: LangChain tool-calling → raw `ollama` function calling → a hand-parsed ReAct text prompt |
| 04 | [RAG Gist](04-rag_gist/) | **RAG** | Embed a blog post into Pinecone, then compare no-RAG vs. manual retrieval chain vs. declarative LCEL retrieval chain |
| 05 | [Documentation Helper](05-documentation_helper/) | **Agentic RAG + UI** | `TavilyCrawl` → Pinecone → tool-driven retrieval agent → Streamlit chat UI, answering questions about the LangChain docs with cited sources |

Complexity increases left to right: 01 is a single chain call, 03 strips an agent down to its bare mechanics, and 05 is a full ingestion + retrieval + UI application.

## ⚡ Quick Start

Every project is standalone — `cd` in, sync, run:

```bash
cd 05-documentation_helper   # or 01-.../02-.../03-.../04-...
uv sync
uv run main.py               # entrypoint name differs per project — see its own README
```

Each project's own `README.md` has the exact `.env` variables it needs and what the example run does. As a rule of thumb:

| Variable | Needed by |
|---|---|
| `OPENAI_API_KEY` | 04, 05 (embeddings + chat); optional swap-in for 01 |
| `TAVILY_API_KEY` | 02 (all scripts), 05 (doc crawling) |
| `PINECONE_API_KEY` / `INDEX_NAME` | 04, 05 (vector storage) |
| `LANGSMITH_API_KEY` | Optional tracing in 01, 02, 03 |
| Local Ollama (`gpt-oss:20b` / `qwen3:1.7b`) | 01, 02, 03 — no API key needed |

## 🧠 What each one teaches

- **01 — Hello World**: the `prompt | llm` chain primitive, running fully locally via Ollama, with no agents or tools yet.
- **02 — ReAct Search Agent**: LangChain's `create_agent` doing a real reason-then-call-tool loop, plus the difference between structured (Pydantic) output and raw message history, and writing a custom `@tool`.
- **03 — Agents Under the Hood**: the same agent implemented at three levels of abstraction — `@tool` + `bind_tools`, then raw JSON tool schemas against the `ollama` client, then a plain-text ReAct prompt parsed by hand — to show exactly what `create_agent` automates.
- **04 — RAG Gist**: the two halves of RAG (ingestion vs. querying), and why LCEL (`RunnablePassthrough.assign(...) | prompt | llm`) is preferred over wiring the same steps together manually.
- **05 — Documentation Helper**: composing crawling (`TavilyCrawl`), chunking, embedding, and tool-driven retrieval into one agent, then wrapping it in a Streamlit chat UI with cited sources and server-side logging.
