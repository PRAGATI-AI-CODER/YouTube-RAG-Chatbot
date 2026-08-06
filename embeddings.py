import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from chunking import get_chunks

load_dotenv()


def get_embeddings(url):
    """
    Generate embeddings for all transcript chunks.
    """

    chunks = get_chunks(url)

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    embeddings = embedding_model.embed_documents(chunks)

    return chunks, embeddings


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")

    chunks, embeddings = get_embeddings(url)

    print(f"\nChunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")
    print(f"Embedding Dimension: {len(embeddings[0])}")

    print("\nFirst 10 values:")
    print(embeddings[0][:10])