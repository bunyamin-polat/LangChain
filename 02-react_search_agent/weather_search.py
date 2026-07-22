import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv()

tavily = TavilyClient()


@tool
def search(query: str) -> str:
    """Tool that searches over Internet

    Args:
        query (str): The query to search for
    Returns:
        str: The search result
    """
    print(f"Searching for: {query}")
    response = tavily.search(query=query)
    return response


llm = ChatOllama(model="gpt-oss:20b", temperature=0)
tools = [search]
agent = create_agent(model=llm, tools=tools)


def main():
    print("Hello from react-search-agent!")
    result = agent.invoke(
        {"messages": [HumanMessage(content="What is the weather in Tokyo?")]}
    )
    print(result)


if __name__ == "__main__":
    main()
