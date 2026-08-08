import os
import re

from vector_store import create_vector_store, load_vector_store
from llm import generate_answer


VECTOR_STORE_DIR = "vector_stores"


def extract_video_id(url):
    """
    Extract the YouTube video ID from a YouTube URL.
    """

    patterns = [
        r"(?:v=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    raise ValueError(
        "Invalid YouTube URL. Could not extract video ID."
    )


def get_retriever(url):
    """
    Load an existing FAISS vector store if available.
    Otherwise create and save a new one.
    """

    video_id = extract_video_id(url)

    save_path = os.path.join(
        VECTOR_STORE_DIR,
        video_id
    )

    if os.path.exists(save_path):

        print("Loading existing vector store...")

        vector_store = load_vector_store(video_id)

    else:

        print("Creating new vector store...")

        vector_store = create_vector_store(
            url,
            video_id
        )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever


def retrieve_context(url, question):
    """
    Retrieve the most relevant transcript chunks
    for a given question.
    """

    retriever = get_retriever(url)

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context


def ask_question(url, question):
    """
    Complete RAG pipeline.

    1. Retrieve the most relevant transcript chunks.
    2. Generate an answer using Gemini.
    """

    context = retrieve_context(
        url,
        question
    )

    answer = generate_answer(
        context=context,
        question=question
    )

    return answer