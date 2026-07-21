import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

load_dotenv()


if __name__ == "__main__":

    loader = UnstructuredLoader(
        file_path="data/mediumblog.txt",
        chunking_strategy="basic",
        max_characters=1000000,
    )
    document = loader.load()
    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(document)
    print(f"Created {len(docs)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    print("Ingesting...")
    PineconeVectorStore.from_documents(
        docs, embeddings, index_name=os.environ.get("INDEX_NAME")
    )
    print("Done!")
