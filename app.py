import os

from dotenv import load_dotenv

from retriever import ask_question


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


if __name__ == "__main__":

    try:
        validate_api_key()

        url = input("Enter YouTube URL: ").strip()
        question = input("Ask a question: ").strip()

        answer = ask_question(
            url,
            question
        )

        print("\nAnswer:")
        print(answer)

    except ValueError as error:
        print(f"\n❌ Error: {error}")