import os

from dotenv import load_dotenv

from retriever import retrieve_context
from llm import generate_answer


load_dotenv()


def validate_api_key():
    """
    Check whether the Gemini API key is configured.
    """

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(
            "GOOGLE_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )


def ask_question(url, question):
    """
    Complete RAG pipeline.

    1. Validate configuration and input.
    2. Retrieve relevant context.
    3. Generate an answer using Gemini.
    """

    validate_api_key()

    if not url.strip():
        raise ValueError("YouTube URL cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    context = retrieve_context(url, question)

    answer = generate_answer(
        context=context,
        question=question
    )

    return answer


if __name__ == "__main__":

    try:
        url = input("Enter YouTube URL: ").strip()

        question = input("Ask a question: ").strip()

        answer = ask_question(url, question)

        print("\nAnswer:")
        print(answer)

    except ValueError as e:
        print(f"\n❌ Error: {e}")

    except Exception:
        print(
            "\n❌ Something went wrong while processing your request. "
            "Please check your API configuration and try again."
        )