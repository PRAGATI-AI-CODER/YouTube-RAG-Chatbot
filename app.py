from retriever import retrieve_context
from llm import generate_answer


def ask_question(url, question):
    """
    Complete RAG pipeline.

    1. Retrieve relevant context.
    2. Generate an answer using Gemini.
    """

    context = retrieve_context(url, question)

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