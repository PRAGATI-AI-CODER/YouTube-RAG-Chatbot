from vector_store import create_vector_store


def get_retriever(url):
    """
    Create a retriever from the FAISS vector store.
    """

    vector_store = create_vector_store(url)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever


def retrieve_context(url, question):
    """
    Retrieve the most relevant transcript chunks
    for a given question.
    """

    retriever = get_retriever(url)

    documents = retriever.invoke(question)

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context