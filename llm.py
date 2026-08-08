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