import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def generate_answer(context, question):
    """
    Generate an answer using Gemini based on retrieved context.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided video transcript."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"]

    return response.content


if __name__ == "__main__":

    context = """
    764 was a Discord server created by Bradley.
    It was named 764 because 764 was the ZIP code of the area where Bradley lived.
    """

    question = "Why was the server called 764?"

    answer = generate_answer(context, question)

    print("\nAnswer:")
    print(answer)