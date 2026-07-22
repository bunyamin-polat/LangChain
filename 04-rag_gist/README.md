# 04 - RAG Gist

A minimal Retrieval-Augmented Generation (RAG) pipeline over a Medium blog post:
embed and store chunks in Pinecone, then retrieve relevant context and generate an
answer with an OpenAI chat model. Unlike the earlier projects, this one uses OpenAI
(not Ollama) and a real vector database instead of an in-memory store.

## What it does

- **`01-ingestion.py`** — loads `data/mediumblog.txt` with `UnstructuredLoader`,
  splits it into ~1000-character chunks (200 overlap) via `CharacterTextSplitter`,
  embeds each chunk with `text-embedding-3-small`, and upserts them into a Pinecone
  index.
- **`02-main.py`** — asks *"What is the Pinecone in Machine Learning?"* three ways,
  to contrast approaches:
  - **Implementation 0** — raw `llm.invoke()` with no retrieval, for comparison.
  - **Implementation 1** — `retrieval_chain_without_lcel()`: manually retrieves
    top-3 docs, formats them into context, builds the prompt, and calls the LLM
    step by step.
  - **Implementation 2** — `create_retrieval_chain_with_lcel()`: the same pipeline
    expressed declaratively with LCEL (`RunnablePassthrough.assign(...) | prompt |
    llm | StrOutputParser()`), which adds streaming, async, and batch support for
    free.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- An [OpenAI](https://platform.openai.com/) API key (used for both embeddings and
  chat completion — no local Ollama model in this project)
- A [Pinecone](https://www.pinecone.io/) account with an index already created,
  matching the `text-embedding-3-small` output size (1536 dimensions)
- Run `01-ingestion.py` before `02-main.py` — the index needs to be populated
  before it can be queried

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `OPENAI_API_KEY` | Yes — used for embeddings (`01-ingestion.py`) and chat (`02-main.py`) |
| `PINECONE_API_KEY` | Yes — read implicitly by `langchain-pinecone` |
| `INDEX_NAME` | Yes — name of the Pinecone index both scripts read/write |
| `GOOGLE_API_KEY` | Not used by default |
| `LANGSMITH_API_KEY` | Not used by default |
| `TAVILY_API_KEY` | Not used by default |

## Setup & run

```bash
cd projects/04-rag_gist
uv sync
uv run 01-ingestion.py   # chunk, embed, and upsert data/mediumblog.txt into Pinecone
uv run 02-main.py        # compare no-RAG vs. non-LCEL vs. LCEL retrieval chains
```

## Notes

- `retriever` is configured with `search_kwargs={"k": 3}`, so each query pulls the
  3 most similar chunks as context.
