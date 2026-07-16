import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv()

llm = ChatOllama(model="gpt-oss:20b", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Hello from react-search-agent!")
    result = agent.invoke({"messages": [HumanMessage(content="Search for 3 job postings for an AI Engineer using langchain in the by area on LinkedIn and list their details")]})
    print(result)


if __name__ == "__main__":
    main()
