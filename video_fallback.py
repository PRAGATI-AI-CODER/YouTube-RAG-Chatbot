import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


load_dotenv()


def generate_video_answer(url, question):
    """
    Generate an answer directly from a public YouTube video
    using Gemini's video understanding capability.

    This function is used as a fallback when transcript
    retrieval is unavailable or blocked.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not configured."
        )

    if not url.strip():
        raise ValueError(
            "YouTube URL cannot be empty."
        )

    if not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = (
        "Answer the following question about the YouTube video.\n\n"
        f"Question: {question}\n\n"
        "Use only information that can be determined from the video. "
        "Do not invent information. "
        "If the video does not contain enough information to answer "
        "the question, clearly say so."
    )

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=types.Content(
                parts=[
                    types.Part(
                        file_data=types.FileData(
                            file_uri=url
                        )
                    ),
                    types.Part(
                        text=prompt
                    ),
                ]
            ),
        )

    except ServerError as error:

        if getattr(error, "code", None) == 500:

            raise ValueError(
                "Gemini could not process this particular YouTube "
                "video. Please try another public YouTube video."
            ) from error

        raise ValueError(
            "Gemini was unable to process the video. "
            "Please try again."
        ) from error

    except Exception as error:

        raise ValueError(
            "Gemini was unable to process the video. "
            "Please try again."
        ) from error

    if not response.text:

        raise ValueError(
            "Gemini could not generate an answer from this video."
        )

    return response.text