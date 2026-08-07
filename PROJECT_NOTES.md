# 📘 YouTube RAG Chatbot – Learning Notes

# Table of Contents

- Project Information
- Tech Stack
- Day 1 - Environment Setup
- Day 1 - Git Setup
- Day 1 - Gemini API
- Day 1 - Transcript Extraction
- Day 2 - Chunking
- Day 2 - Embeddings
- Day 3 - FAISS Vector Store


---

# Project Information

**Project Name:**
YouTube RAG Chatbot

**Objective:**
Build an AI-powered chatbot that answers questions based on the transcript of any YouTube video using Retrieval-Augmented Generation (RAG).

---

# Tech Stack

## Language
- Python 3.14.6

## IDE
- Visual Studio Code

## Version Control
- Git
- GitHub

Repository:
https://github.com/PRAGATI-AI-CODER/YouTube-RAG-Chatbot

---

# Libraries Used

| Library | Purpose |
|----------|----------|
| Streamlit | Web Interface |
| LangChain | RAG Pipeline |
| LangChain Google GenAI | Gemini Integration |
| youtube-transcript-api | Fetch YouTube Transcript |
| FAISS | Vector Database |
| python-dotenv | Load API Keys |
| tiktoken | Token Counting |

---

# Day 1

## Goal

Set up the complete development environment and build the first module of the RAG pipeline.

---

## Environment Setup

### Python

Installed Python 3.14.6.

Verified using:

```bash
python --version
```

---

### Virtual Environment

Created:

```bash
python -m venv .venv
```

Activated:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Why use a Virtual Environment?

A virtual environment creates an isolated Python environment for one project.

Benefits:

- Avoid dependency conflicts.
- Different projects can use different package versions.
- Standard industry practice.

---

## Installed Packages

```bash
pip install streamlit langchain langchain-community langchain-google-genai youtube-transcript-api faiss-cpu python-dotenv tiktoken
```

---

# Git Setup

Initialized repository:

```bash
git init
```

First Commit:

```
Initial project setup with Gemini API and transcript extraction
```

Second Commit:

```
Ignore VS Code settings
```

---

## Git Workflow

```text
Modify Code
      ↓
git add .
      ↓
git commit
      ↓
git push
```

---

# Gemini API

Created API Key using Google AI Studio.

Stored inside:

```
.env
```

Loaded using:

```python
load_dotenv()
```

Retrieved using:

```python
os.getenv("GOOGLE_API_KEY")
```

---

# Important Lesson

Do NOT hardcode API Keys.

Always store them inside `.env`.

Never upload `.env` to GitHub.

---

# Gemini Debugging

Problems faced:

### 1. Deprecated Models

Initially tried:

```
gemini-2.5-flash
```

Received:

```
404 NOT_FOUND
```

Reason:

The model is deprecated for new users.

Solution:

Listed available models using:

```python
client.models.list()
```

Finally connected successfully using:

```
models/gemini-3.5-flash
```

---

# Transcript Module

Created:

```
transcript.py
```

Responsibilities:

- Accept YouTube URL
- Extract Video ID
- Download Transcript
- Return Transcript

---

## Video ID

Example:

```
https://youtu.be/J5_-l7WIO_w
```

Video ID:

```
J5_-l7WIO_w
```

---

## Transcript

Downloaded using:

```python
YouTubeTranscriptApi().fetch()
```

---

## Hindi Transcript Issue

Problem:

```
NoTranscriptFound
```

Reason:

Video only had Hindi subtitles.

Solution:

```python
languages=["hi","en"]
```

---

# Architecture Completed

```
YouTube URL
      │
      ▼
Extract Video ID
      │
      ▼
Download Transcript
      │
      ▼
Transcript
```

---

# Files Created

```
app.py

transcript.py

chunking.py

embeddings.py

vector_store.py

retriever.py

llm.py

utils.py

config.py
```

---

# Concepts Learned

## What is a Transcript?

A transcript is the textual representation of everything spoken inside a video.

For RAG,

```
Video

↓

Transcript

↓

Knowledge Base
```

---

## Current Progress

✅ Environment Setup

✅ Git Setup

✅ GitHub Repository

✅ Gemini API

✅ Transcript Extraction

⬜ Chunking

⬜ Embeddings

⬜ FAISS

⬜ Retriever

⬜ RAG Pipeline

⬜ Streamlit UI

---

# Next Milestone

Chunking

Topics:

- RecursiveCharacterTextSplitter
- Chunk Size
- Chunk Overlap
- Why Chunking is Required
- Preparing Documents for Embeddings




# Day 2 - Text Chunking

## Objective

Split a long transcript into smaller overlapping chunks before generating embeddings.

---

## Why Chunking?

Large Language Models cannot efficiently process extremely long documents.

Instead of sending the entire transcript, we divide it into smaller sections.

Benefits:

- Faster retrieval
- Lower token usage
- Better context management
- Improved answer quality

---

## Chunking Strategy

Library:

langchain-text-splitters

Class:

RecursiveCharacterTextSplitter

Parameters:

chunk_size = 1000

chunk_overlap = 200

---

## Why Overlap?

Overlap preserves context between consecutive chunks.

Without overlap, important information can be split across chunk boundaries and become harder to retrieve.

---

## Output

The transcript was successfully divided into multiple chunks that are ready for embedding.


# Day 2 - Embeddings

## What is an Embedding?

An embedding is a numerical vector representation of text that captures semantic meaning.

---

## Why are Embeddings Needed?

Keyword search matches words.

Embeddings enable semantic search by matching meaning.

---

## Workflow

Transcript

↓

Chunks

↓

Embedding Model

↓

Vectors

↓

Vector Database

---

## Embedding Model Used

GoogleGenerativeAIEmbeddings

Model:

models/gemini-embedding-001


# Embeddings - Key Takeaways

## What is an Embedding?

An embedding is a fixed-length numerical vector that represents the semantic meaning of a piece of text.

---

## Model Used

GoogleGenerativeAIEmbeddings

Model:

models/gemini-embedding-001

---

## Embedding Dimension

3072

---

## Why are Embeddings Useful?

Embeddings allow semantic search instead of keyword matching.

Chunks with similar meanings have vectors that are close together in the embedding space.

---

## Important Methods

embed_query()

Converts a single query or piece of text into an embedding.

embed_documents()

Converts multiple documents/chunks into embeddings.

Used when indexing documents in a vector database.

## Refactoring

### Why Refactor?

To follow the Single Responsibility Principle.

### Responsibilities

transcript.py

- Fetch transcript

chunking.py

- Split transcript into chunks

embeddings.py

- Generate embeddings

Each module should perform one task and expose reusable functions.

---

# Day 3 - FAISS Vector Store

## Objective

Create a searchable vector database from the transcript embeddings.

---

## What is FAISS?

FAISS (Facebook AI Similarity Search) is a library designed to perform fast similarity searches on high-dimensional vectors.

Unlike traditional databases that search using exact values or keywords, FAISS searches by semantic similarity.

---

## Why is FAISS Needed?

Imagine a transcript produces hundreds or even thousands of chunks.

Each chunk becomes an embedding.

Comparing a user's query embedding against every stored embedding one by one would become inefficient as the number of vectors grows.

FAISS creates an optimized index that makes similarity search much faster.

---

## Workflow

Transcript

↓

Chunks

↓

Embeddings

↓

FAISS Index

↓

Similarity Search

---

## Library Used

langchain_community.vectorstores

Class:

FAISS

---

## Method Used

```python
FAISS.from_texts()
```

This method:

1. Accepts all transcript chunks.
2. Generates embeddings using the supplied embedding model.
3. Builds a FAISS index.
4. Stores the mapping between vectors and their original text.

---

## Output

Successfully created a FAISS Vector Store.

Indexed Chunks:

21

---

## Key Learning

FAISS does not understand text.

It only understands vectors.

When a user asks a question:

Question

↓

Embedding

↓

FAISS searches for the closest vectors

↓

Returns the corresponding text chunks

↓

Gemini generates the final answer.

---

## Important Interview Point

FAISS is not a Large Language Model.

It is a vector similarity search library.

Its responsibility is to retrieve the most relevant information, not generate answers.