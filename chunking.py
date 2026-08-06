from langchain_text_splitters import RecursiveCharacterTextSplitter
from transcript import get_transcript

# YouTube URL
url = input("Enter YouTube URL: ")

# Fetch transcript
text = get_transcript(url)

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Split transcript
chunks = text_splitter.split_text(text)

print(f"\nTotal Chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks[:3]):   # Show first 3 chunks
    print("=" * 80)
    print(f"Chunk {i+1}")
    print("=" * 80)
    print(f"Length: {len(chunk)} characters\n")
    print(chunk)
    print()