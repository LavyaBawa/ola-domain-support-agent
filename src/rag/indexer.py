from pathlib import Path

import chromadb

from src.rag.chunking import fixed_size_chunks, sentence_chunks
from src.rag.embeddings import LocalEmbedder


KB_PATH = Path("data/knowledge_base")
CHROMA_PATH = "data/chroma"


def load_documents():
    documents = []

    for file_path in sorted(KB_PATH.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


def build_collections():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedder = LocalEmbedder()

    fixed_collection = client.get_or_create_collection(
        name="kb_fixed_overlap",metadata={"hnsw:space": "cosine"}
    )

    sentence_collection = client.get_or_create_collection(
        name="kb_sentence",
    metadata={"hnsw:space": "cosine"}
    )

    documents = load_documents()

    fixed_texts = []
    fixed_ids = []
    fixed_metadata = []

    sentence_texts = []
    sentence_ids = []
    sentence_metadata = []

    for document in documents:
        source = document["source"]
        text = document["text"]

        for index, chunk in enumerate(fixed_size_chunks(text)):
            fixed_texts.append(chunk)
            fixed_ids.append(f"{source}-fixed-{index}")
            fixed_metadata.append({"source": source})

        for index, chunk in enumerate(sentence_chunks(text)):
            sentence_texts.append(chunk)
            sentence_ids.append(f"{source}-sentence-{index}")
            sentence_metadata.append({"source": source})

    fixed_embeddings = embedder.embed_documents(fixed_texts)
    sentence_embeddings = embedder.embed_documents(sentence_texts)

    fixed_collection.upsert(
        ids=fixed_ids,
        documents=fixed_texts,
        embeddings=fixed_embeddings,
        metadatas=fixed_metadata,
    )

    sentence_collection.upsert(
        ids=sentence_ids,
        documents=sentence_texts,
        embeddings=sentence_embeddings,
        metadatas=sentence_metadata,
    )

    print(f"Fixed-overlap chunks: {len(fixed_texts)}")
    print(f"Sentence chunks: {len(sentence_texts)}")


if __name__ == "__main__":
    build_collections()
