from vector_store import create_vector_store
from llm import generate_answer


def get_retriever(url):
    """
    Creates a retriever from the FAISS vector store.
    """

    vector_store = create_vector_store(url)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever


def ask_question(url, question):
    """
    Retrieve relevant chunks and generate an answer using Gemini.
    """

    retriever = get_retriever(url)

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    answer = generate_answer(
        context=context,
        question=question
    )

    return answer


if __name__ == "__main__":

    url = input("Enter YouTube URL: ")

    question = input("Ask a question: ")

    answer = ask_question(url, question)

    print("\nAnswer:")
    print(answer)