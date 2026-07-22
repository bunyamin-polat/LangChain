# 02 - ReAct Search Agent

Builds on the hello-world chain by introducing a real LangChain agent
(`create_agent`) that can reason and call tools in a ReAct-style loop. All three
scripts use a local `ChatOllama` model and the Tavily web search API as a tool.

## What it does

- **`job_search_structured.py`** — creates an agent with a `TavilySearch` tool and a
  structured `AgentResponse` (Pydantic) output containing an answer plus a list of
  sources. Asks it to find AI Engineer job postings.
- **`job_search_raw.py`** — same idea without structured output, returns the raw
  agent message history. Asks it to find 3 job postings.
- **`weather_search.py`** — defines a custom `@tool`-decorated `search` function that
  wraps the `TavilyClient` directly (instead of the built-in `TavilySearch` tool) and
  asks a weather question.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Ollama](https://ollama.com/) running locally with the `gpt-oss:20b` model pulled:

  ```bash
  ollama pull gpt-oss:20b
  ```

- A [Tavily](https://tavily.com/) API key (required by all three scripts — search is
  the core tool being used)

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `TAVILY_API_KEY` | Yes — used by every script for web search |
| `OPENAI_API_KEY` | Not used by default |
| `GOOGLE_API_KEY` | Not used by default |
| `LANGSMITH_API_KEY` | Optional, enables LangSmith tracing |

## Setup & run

```bash
cd projects/02-react_search_agent
uv sync
uv run job_search_structured.py   # structured response with sources
uv run job_search_raw.py          # raw agent message output
uv run weather_search.py          # custom search tool example
```
