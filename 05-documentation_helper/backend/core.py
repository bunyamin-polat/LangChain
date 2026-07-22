import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import ToolMessage
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from .logger import log_error, log_info

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.2")
RETRIEVER_K = 4

# Set up the embeddings and vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = PineconeVectorStore(
    embedding=embeddings, index_name=os.getenv("INDEX_NAME")
)
retriever = vectorstore.as_retriever()

# Initialize the chat model
model = init_chat_model(MODEL_NAME, model_provider="openai")


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve relevant context from the vector store based on the query."""
    retrieved_docs = retriever.invoke(query, k=RETRIEVER_K)
    log_info(f"retrieve_context: fetched {len(retrieved_docs)} docs for query={query!r}")

    # Serialize the retrieved documents into a list of dictionaries, each containing the source and content
    serialized_docs = "\n\n".join(
        (
            f"Source: {doc.metadata.get('source', 'Unknown')}\n\nContent: {doc.page_content}"
        )
        for doc in retrieved_docs
    )
    return serialized_docs, retrieved_docs


# Static system prompt and agent, built once at import time and reused across
# requests instead of being rebuilt on every run_llm() call.
SYSTEM_PROMPT = (
    "You are a helpful AI assistant that answers questions about LangChain documentation. "
    "You have access to a tool that retrieves relevant documentation. "
    "Use the tool to find relevant information before answering questions. "
    "Always cite the sources you use in your answers. "
    "If you cannot find the answer in the retrieved documentation, say so."
)
agent = create_agent(model, tools=[retrieve_context], system_prompt=SYSTEM_PROMPT)


def run_llm(query: str) -> Dict[str, Any]:
    """
    Run the RAG pipeline to answer a query using retrieved documentation.

    Args:
        query: The user's question

    Returns:
        Dictionary containing:
            - answer: The generated answer
            - context: List of retrieved documents
    """

    # Build messages list
    messages = [{"role": "user", "content": query}]

    # Invoke the agent
    try:
        response = agent.invoke({"messages": messages})
    except Exception as e:
        log_error(f"run_llm: agent invocation failed for query={query!r} - {e}")
        raise

    # Extract the answer from the last AI message
    answer = response["messages"][-1].content

    # Extract context documents from ToolMessage artifacts
    context_docs = []
    for message in response["messages"]:
        # Check if this is a ToolMessage with artifact
        if isinstance(message, ToolMessage) and hasattr(message, "artifact"):
            # The artifact should contain the list of Document objects
            if isinstance(message.artifact, list):
                context_docs.extend(message.artifact)

    return {"answer": answer, "context": context_docs}


if __name__ == "__main__":
    result = run_llm(query="what are deep agents?")
    print(result)
