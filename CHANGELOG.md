# Changelog

## Version 0.1 - Initial Project Setup

### Added

- Python project setup
- Virtual environment
- Git repository initialization
- GitHub repository
- Gemini API integration
- Environment variable configuration
- YouTube transcript extraction

---

## Version 0.2 - Text Processing

### Added

- Implemented transcript chunking
- Used `RecursiveCharacterTextSplitter`
- Configured chunk size (1000)
- Configured chunk overlap (200)
- Generated embeddings using Gemini Embedding Model
- Refactored project into modular components

### Learned

- Why chunking is required
- What embeddings are
- Difference between `embed_query()` and `embed_documents()`

---

## Version 0.3 - Vector Store

### Added

- Implemented FAISS Vector Store
- Indexed transcript chunks
- Connected Gemini Embedding Model with FAISS
- Created reusable `create_vector_store()` function
- Successfully indexed transcript chunks

### Learned

- What a Vector Store is
- How FAISS performs semantic similarity search
- Difference between a Vector Database and an LLM

---

## Next

- Retriever
- RAG Pipeline
- Streamlit UI
- Deployment


## Version 0.4 - Retriever

### Added

- Implemented semantic retriever using FAISS
- Configured similarity search
- Set `k = 3` to retrieve the top 3 relevant chunks
- Successfully retrieved relevant transcript chunks based on user queries

### Learned

- Difference between retrieval and generation
- Why only the most relevant chunks are sent to the LLM
- How semantic retrieval works using embeddings and FAISS
- Importance of choosing an appropriate value for `k`

### Next

- Connect Retriever with Gemini
- Build the complete RAG pipeline


---

## Version 0.5 - Gemini Generation

### Added

- Implemented Gemini-based answer generation
- Created `generate_answer()` function
- Added context-aware prompting
- Added protection against unsupported answers
- Successfully tested Gemini 3.5 Flash

### Learned

- Difference between retrieval and generation
- How retrieved context is passed to an LLM
- How prompt instructions can restrict the LLM to provided context
- How the LLM converts retrieved information into a natural-language answer

### Next

- Connect Retriever with Gemini
- Build the complete RAG pipeline

---

## Version 0.5 - Complete RAG Pipeline

### Added

- Connected FAISS Retriever with Gemini
- Implemented context construction from retrieved documents
- Integrated retrieved context with Gemini generation
- Built complete Retrieval-Augmented Generation pipeline
- Added context-grounded answer generation

### Testing

- Tested answerable questions
- Tested questions whose answers were not present in the transcript
- Verified that the system can respond when information is unavailable

### Learned

- Complete RAG workflow
- Difference between retrieval, augmentation, and generation
- How retrieved documents become LLM context
- Importance of context-grounded generation

### Next

- Improve application architecture
- Build user-facing interface
- Add persistent vector store
- Improve error handling

---

## Version 0.6 - Clean Application Architecture

### Changed

- Refactored `retriever.py` to handle retrieval only
- Refactored `llm.py` to handle generation only
- Converted `app.py` into the main RAG pipeline orchestrator
- Removed duplicate generation logic from `retriever.py`
- Removed standalone testing logic from `llm.py`

### Testing

- Verified answerable questions still produce contextual answers
- Verified out-of-context questions are rejected appropriately

### Architecture

The application now separates:

- Application orchestration
- Semantic retrieval
- LLM generation

---

## Version 0.7 - Persistent FAISS Vector Store

### Added

- Persistent local FAISS vector stores
- YouTube video ID-based vector store identification
- Automatic vector store saving
- Automatic vector store loading
- Reusable Gemini embedding model configuration

### Changed

- Retriever now checks for an existing vector store before creating a new one
- Existing vector stores are loaded instead of rebuilding embeddings
- Added `vector_stores/` to `.gitignore`

### Testing

- Verified creation of a new vector store
- Verified saved FAISS files
- Verified loading of an existing vector store
- Verified retrieval and Gemini generation after loading

### Performance Improvement

Repeated questions for the same video no longer require transcript processing, embedding generation, or FAISS reconstruction.