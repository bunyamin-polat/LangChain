from typing import Any, Dict, List

import streamlit as st
from backend.core import run_llm
from backend.logger import log_error, log_info


# Turn the raw Document objects returned as RAG "context" into a flat list of
# source strings (their metadata["source"], e.g. the doc URL) for display.
def _format_sources(context_docs: List[Any]) -> List[str]:
    return [
        str((getattr(doc, "metadata", None) or {}).get("source") or "Unknown")
        for doc in (context_docs or [])
    ]


# Page setup
st.set_page_config(page_title="LangChain Documentation Helper", layout="centered")
st.title("LangChain Documentation Helper")

# Sidebar button to wipe the conversation and start fresh
with st.sidebar:
    st.subheader("Session")
    if st.button("Clear the chat", use_container_width=True):
        st.session_state.pop("messages", None)
        st.rerun()

# Seed chat history with a welcome message the first time the app loads
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me anything about LangChain docs. I'll retrieve relevant context and cite sources.",
            "sources": [],
        }
    ]

# Streamlit reruns the whole script on every interaction, so redraw the
# full chat history (including any cited sources) each time.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- {s}")


# Chat input box at the bottom; the block below only runs once the user submits a question
prompt = st.chat_input("Ask a question about LangChain…")
if prompt:
    # Record and immediately render the user's message
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Run the RAG pipeline (retrieve_context tool + LLM) and pull out
            # the answer text plus the Document objects used as context
            log_info(f"app: handling query={prompt!r}")
            with st.spinner("Retrieving docs and generating answer…"):
                result: Dict[str, Any] = run_llm(prompt)
                answer = (
                    str(result.get("answer", "")).strip() or "(No answer returned.)"
                )
                sources = _format_sources(result.get("context", []))

            # Show the answer, with sources collapsed under an expander if any were found
            st.markdown(answer)
            if sources:
                with st.expander("Sources"):
                    for s in sources:
                        st.markdown(f"- {s}")

            # Persist this turn so it's still shown after the next Streamlit rerun
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
        except Exception as e:
            # Log server-side (the UI alone doesn't leave any trace once dismissed)
            # and show the failure in the UI instead of crashing the app
            log_error(f"app: failed to answer query={prompt!r} - {e}")
            st.error("Failed to generate a response.")
            st.exception(e)
