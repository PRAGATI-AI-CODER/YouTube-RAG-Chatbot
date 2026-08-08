# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about YouTube videos and receive answers based only on the video's transcript.

The application uses **YouTube Transcript API**, **Gemini embeddings**, **FAISS**, **LangChain**, **Gemini**, and **Streamlit** to build an end-to-end RAG pipeline.

---

## ✨ Features

- 🎥 Accepts YouTube video URLs
- 📝 Automatically retrieves available video transcripts
- ✂️ Splits transcripts into manageable chunks
- 🧠 Generates semantic embeddings using Gemini
- 🔎 Performs similarity-based retrieval using FAISS
- 📚 Retrieves the top 3 most relevant transcript chunks
- 🤖 Generates grounded answers using Gemini
- 🚫 Avoids answering questions that cannot be supported by the transcript
- 💾 Persists FAISS vector stores locally
- ⚡ Reuses existing vector stores for previously processed videos
- 💬 Supports multiple questions about the same video
- 🗑️ Clear chat functionality
- 🔄 Load a new video without restarting the application
- 🖥️ Interactive Streamlit interface
- ⚠️ Handles invalid URLs, missing API keys, and unavailable transcripts

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** combines information retrieval with a Large Language Model (LLM).

Instead of asking the LLM to answer a question from its general knowledge, this project first retrieves the most relevant parts of the YouTube transcript and provides those sections to Gemini as context.

### Pipeline

```text
YouTube URL
     │
     ▼
YouTube Transcript
     │
     ▼
Text Chunking
     │
     ▼
Gemini Embeddings
     │
     ▼
FAISS Vector Store
     │
     ▼
User Question
     │
     ▼
Semantic Similarity Search
     │
     ▼
Top 3 Relevant Chunks
     │
     ▼
Gemini LLM
     │
     ▼
Grounded Answer