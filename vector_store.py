import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from chunking import get_chunks

load_dotenv()


def create_vector_store(url):
    """
    Creates a FAISS vector database from transcript chunks.
    """

    chunks = get_chunks(url)

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    return vector_store


if __name__ == "__main__":

    url = input("Enter YouTube URL: ")

    vector_store = create_vector_store(url)

    print("\n✅ Vector Store Created Successfully!")

    print(f"Indexed Chunks : {vector_store.index.ntotal}")