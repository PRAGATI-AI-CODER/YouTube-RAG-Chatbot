from langchain_text_splitters import RecursiveCharacterTextSplitter
from transcript import get_transcript


def get_chunks(url):
    """
    Fetch transcript and split it into chunks.
    """

    text = get_transcript(url)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    return chunks


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")

    chunks = get_chunks(url)

    print(f"\nTotal Chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:3]):
        print("=" * 80)
        print(f"Chunk {i+1}")
        print("=" * 80)
        print(chunk)
        print()