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

# Day 3 - Retriever

## Objective

Retrieve the most relevant transcript chunks based on a user's question.

---

## What is a Retriever?

A retriever searches the vector database and returns the most semantically similar chunks.

It does not generate answers.

---

## Method Used

vector_store.as_retriever()

---

## Search Type

similarity

---

## Search Parameter

k = 3

Only the three most relevant chunks are returned.

---

## Learning

The Retriever performs semantic search using vector similarity.

The retrieved chunks are later passed to the LLM for answer generation.

---

# Day 4 - LLM Generation

## Objective

Use Gemini to generate a natural-language answer from retrieved context.

## Model Used

Gemini 3.5 Flash

## Implementation

The `llm.py` module accepts:

- Context
- User question

It sends both to Gemini and returns a generated answer.

## Prompt Strategy

The model is instructed to:

- Answer using only the provided context.
- Avoid making up information.
- Clearly state when the answer cannot be found in the provided context.

## Testing

Test Question:

Why was the server called 764?

Test Context:

764 was a Discord server created by Bradley.
It was named 764 because 764 was the ZIP code of the area where Bradley lived.

Result:

The server was named 764 because 764 was the ZIP code of the area where Bradley lived.

## Key Learning

The LLM is responsible for generation, not retrieval.

The Retriever finds relevant information, while the LLM uses that information to formulate the final answer.

---

# Day 4 - Complete RAG Pipeline

## Objective

Connect the Retriever with Gemini to create a complete Retrieval-Augmented Generation pipeline.

## Complete Workflow

YouTube URL

↓

Transcript Extraction

↓

Text Chunking

↓

Gemini Embeddings

↓

FAISS Vector Store

↓

Semantic Retriever

↓

Top 3 Relevant Chunks

↓

Context Construction

↓

Gemini 3.5 Flash

↓

Final Answer

---

## How the Pipeline Works

1. The user provides a YouTube URL.
2. The transcript is extracted from the video.
3. The transcript is divided into smaller chunks.
4. Each chunk is converted into a vector embedding.
5. FAISS indexes the embeddings.
6. The user's question is passed to the retriever.
7. The retriever performs semantic similarity search.
8. The top 3 relevant chunks are selected.
9. The selected chunks are combined into a context.
10. The context and question are sent to Gemini.
11. Gemini generates a natural-language answer based on the context.

---

## RAG Principle

Retrieval-Augmented Generation combines:

### Retrieval

Finding relevant information from an external knowledge source.

### Augmentation

Providing the retrieved information to the language model as context.

### Generation

Using the language model to generate a natural-language response.

---

## Testing

### Test 1 - Answerable Question

Question:

Why was the server called 764?

Result:

The system successfully generated an answer using the retrieved transcript context.

---

### Test 2 - Unanswerable Question

Question:

What is the capital of France?

Result:

The system responded:

"I could not find the answer in the provided video transcript."

This confirmed that the current prompt instructs the LLM not to answer questions when the required information is unavailable in the provided context.

---

## Key Learning

The Retriever and LLM have different responsibilities.

Retriever:

- Finds relevant information.
- Does not generate answers.

LLM:

- Receives the retrieved context.
- Generates the final natural-language response.

Together they form the core RAG pipeline.

---

# Milestone 6 - Clean Application Architecture

## Objective

Refactor the RAG application so that each module has a clear and separate responsibility.

## Architecture

### app.py

Acts as the main orchestrator.

Responsibilities:

- Accept YouTube URL from the user
- Accept the user's question
- Request relevant context from the retriever
- Send the context and question to the LLM
- Display the final answer

### retriever.py

Responsible only for retrieval.

Responsibilities:

- Create the FAISS retriever
- Perform semantic similarity search
- Retrieve the top 3 relevant transcript chunks
- Combine the retrieved chunks into context

### llm.py

Responsible only for generation.

Responsibilities:

- Receive retrieved context and user question
- Construct the prompt
- Send the prompt to Gemini
- Return the generated answer

## Refactored Flow

User Input
↓
app.py
↓
retriever.py
↓
FAISS
↓
Top 3 Relevant Chunks
↓
Context
↓
llm.py
↓
Gemini 3.5 Flash
↓
Final Answer

## Testing

### Test 1 - Answerable Question

Question:

What is 764?

Result:

The application successfully retrieved relevant transcript context and generated a contextual answer.

### Test 2 - Out-of-Context Question

Question:

What is the capital of France?

Result:

The application responded:

"I could not find the answer in the provided video transcript."

## Key Learning

Separating retrieval, generation, and orchestration makes the application easier to understand, maintain, test, and extend.

The application now follows a modular architecture rather than placing the complete workflow inside a single file.