import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Load environment variables from .env file
load_dotenv()


def main():
    information = """Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, inventor,[2] and investor. 
    A pioneer of the personal computer revolution of the 1970s and 1980s, Jobs co-founded Apple Inc. with his early business partner Steve Wozniak as Apple Computer Company in 1976. 
    After the company's board of directors fired him in 1985, he founded NeXT the same year and purchased Pixar in 1986, becoming its chairman and majority shareholder until 2007. 
    Jobs returned to Apple in 1997 as CEO, where he was closely involved with the creation and promotion of many of the company's most influential products until his resignation in 2011. 
    
    In 1997, Jobs returned to Apple as CEO after the company acquired NeXT. He was largely responsible for reviving Apple, which was on the verge of bankruptcy. 
    He worked closely with British designer Jony Ive to develop a line of products and services that had larger cultural ramifications, beginning with the "Think different" advertising campaign and leading to the iMac, iTunes, Mac OS X, Apple Store, iPod, iTunes Store, iPhone, App Store, and iPad. 
    Jobs was also a member of the board of directors at Gap Inc. from 1999 to 2002.[4] In 2003, Jobs was diagnosed with a pancreatic neuroendocrine tumor. 
    He died of tumor-related respiratory arrest in 2011; in 2022, he was posthumously awarded the Presidential Medal of Freedom. 
    Since his death, he has been granted 141 patents; Jobs holds over 450 patents in total.[5]"""

    summary_template = """Given the information {information} about a person, I want you to create:
    1. A short summary of the person in 2-3 sentences.
    2. Two interesting facts about the person."""

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # llm = ChatOpenAI(
    #     model_name="gpt-5", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")
    # )
    llm = ChatOllama(model="gpt-oss:20b", temperature=0)

    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information})
    print(response.content)


if __name__ == "__main__":
    main()
