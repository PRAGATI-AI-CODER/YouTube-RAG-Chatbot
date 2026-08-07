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