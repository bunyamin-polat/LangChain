from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()


class Source(BaseModel):
    """Schema for a source used by the agent."""

    title: str = Field(description="The title of the source.")
    url: str = Field(description="The URL of the source.")


class AgentResponse(BaseModel):
    """Schema for the agent's response with the answer and sources."""

    answer: str = Field(description="The answer provided by the agent.")
    sources: List[Source] = Field(
        default_factory=list,
        description="A list of sources used to generate the answer.",
    )


llm = ChatOllama(model="gpt-oss:20b", temperature=0)
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from react-search-agent!")
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Search for 2 job postings for an AI Engineer using langchain in the by area on LinkedIn and list their details"
                )
            ]
        }
    )
    print(result)


if __name__ == "__main__":
    main()
