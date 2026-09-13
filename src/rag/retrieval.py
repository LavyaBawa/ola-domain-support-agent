import chromadb

from src.rag.embeddings import LocalEmbedder


CHROMA_PATH = "data/chroma"


class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.embedder = LocalEmbedder()

        self.fixed_collection = self.client.get_collection(
            name="kb_fixed_overlap"
        )

        self.sentence_collection = self.client.get_collection(
            name="kb_sentence"
        )

    def search(self, query, strategy="sentence", top_k=3):
        query_embedding = self.embedder.embed_query(query)

        if strategy == "fixed":
            collection = self.fixed_collection
        else:
            collection = self.sentence_collection

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        if results["distances"] and results["distances"][0]:
            top_distance = results["distances"][0][0]
            top_similarity = 1 - top_distance

            results["top_similarity"] = top_similarity

            if top_similarity < 0.347:
                results["grounded"] = False
            else:
                results["grounded"] = True

        return results


if __name__ == "__main__":
    retriever = Retriever()

    test_queries = [
        "How quickly should a critical ticket receive a response?",
        "How long does a low priority ticket have to receive a response?",
        "What is the refund policy?",
        "What are the business hours?",
        "What is the weather in Delhi today?",
        "Who won the last cricket match?","How should a service outage be communicated to customers?",
    ]

    for query in test_queries:
        results = retriever.search(
            query,
            strategy="sentence",
            top_k=1,
        )

        distance = results["distances"][0][0]
        similarity = 1 - distance

        source = results["metadatas"][0][0]["source"]

        print("\nQuery:", query)
        print("Source:", source)
        print(f"Cosine distance: {distance:.4f}")
        print(f"Cosine similarity: {similarity:.4f}")
        print("Grounded:", results["grounded"])
