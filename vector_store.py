import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from chunking import get_chunks

load_dotenv()


VECTOR_STORE_DIR = "vector_stores"


def get_embedding_model():
    """
    Create the Gemini embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def create_vector_store(url, video_id):
    """
    Create and save a FAISS vector store from transcript chunks.
    """

    chunks = get_chunks(url)

    embedding_model = get_embedding_model()

    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embedding_model
    )

    save_path = os.path.join(VECTOR_STORE_DIR, video_id)

    os.makedirs(save_path, exist_ok=True)

    vector_store.save_local(save_path)

    return vector_store


def load_vector_store(video_id):
    """
    Load an existing FAISS vector store.
    """

    embedding_model = get_embedding_model()

    save_path = os.path.join(VECTOR_STORE_DIR, video_id)

    vector_store = FAISS.load_local(
        save_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return vector_store