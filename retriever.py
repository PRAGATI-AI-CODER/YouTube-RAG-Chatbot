from vector_store import create_vector_store


def get_retriever(url):
    """
    Creates a retriever from the FAISS vector store.
    """

    vector_store = create_vector_store(url)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever


if __name__ == "__main__":

    url = input("Enter YouTube URL: ")

    retriever = get_retriever(url)

    query = input("\nAsk a question: ")

    results = retriever.invoke(query)

    print("\nTop Retrieved Chunks:\n")

    for i, doc in enumerate(results):

        print("=" * 80)
        print(f"Chunk {i+1}")
        print("=" * 80)
        print(doc.page_content)
        print()