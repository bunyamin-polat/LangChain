# 03 - Agents Under the Hood

Three progressively lower-level implementations of the *same* tool-calling agent
(a shopping assistant with `get_product_price` and `apply_discount` tools), each
peeling back one layer of abstraction to show what LangChain's `create_agent` /
`@tool` do for you under the hood.

## What it does

- **`01-agent_loop_langchain_tool_calling.py`** — the LangChain way: `@tool`-decorated
  functions, `init_chat_model(...).bind_tools(...)`, and a manual iteration loop over
  `AIMessage.tool_calls`.
- **`02-agent_loop_raw_function_calling.py`** — the same loop rewritten against the raw
  `ollama` Python client, with tool JSON schemas written out by hand instead of derived
  from `@tool`.
- **`03-raw_react_prompt.py`** — no structured tool-calling API at all. Tool
  descriptions are embedded as plain text in a ReAct-style prompt, and the model's
  `Action` / `Action Input` output is parsed back out with regex.

Each script prints its reasoning loop (iterations, tool calls, tool results) to the
console, and traces runs to LangSmith via `@traceable`.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Ollama](https://ollama.com/) running locally with the `qwen3:1.7b` model pulled:

  ```bash
  ollama pull qwen3:1.7b
  ```

- (Optional) A [LangSmith](https://smith.langchain.com/) API key if you want the
  `@traceable` calls to actually upload traces — set `LANGSMITH_TRACING=true` and
  `LANGSMITH_API_KEY` in `.env`. Scripts run fine without it; tracing is just a no-op.

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `LANGSMITH_API_KEY` | Optional, enables LangSmith tracing for `@traceable` calls |
| `OPENAI_API_KEY` | Not used by default |
| `GOOGLE_API_KEY` | Not used by default |
| `TAVILY_API_KEY` | Not used by these scripts |

## Setup & run

```bash
cd projects/03-agents_under_the_hood
uv sync
uv run 01-agent_loop_langchain_tool_calling.py
uv run 02-agent_loop_raw_function_calling.py
uv run 03-raw_react_prompt.py
```
