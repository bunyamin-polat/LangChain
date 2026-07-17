# 01 - Hello World

A minimal LangChain example: build a prompt template, pipe it into a local LLM through
`ChatOllama`, and print the response. This is the "hello world" of a LangChain chain
(`prompt | llm`) before any agents or tools are introduced.

## What it does

`main.py` feeds a short biography of Steve Jobs into a prompt template that asks the
model to produce a summary and two interesting facts, then invokes the chain and prints
the result.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) for dependency management
- [Ollama](https://ollama.com/) running locally with the `gpt-oss:20b` model pulled:

  ```bash
  ollama pull gpt-oss:20b
  ```

- A `.env` file in this folder. By default this project runs fully locally via Ollama
  and needs no API keys.

## Environment variables (`.env`)

| Variable | Required? |
| --- | --- |
| `OPENAI_API_KEY` | Only if you switch `llm` to the commented-out `ChatOpenAI` |
| `GOOGLE_API_KEY` | Not used by default |
| `LANGSMITH_API_KEY` | Optional, enables LangSmith tracing |

## Setup & run

```bash
cd projects/01-hello_world
uv sync
uv run main.py
```

## Notes

- The `ChatOpenAI` line is commented out in `main.py`; swap it in (and set
  `OPENAI_API_KEY`) if you'd rather use OpenAI instead of a local Ollama model.
