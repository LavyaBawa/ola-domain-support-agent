from src.rag.retrieval import Retriever


class GroundedGenerator:
    def __init__(self):
        self.retriever = Retriever()

    def answer(self, query, strategy="sentence", top_k=3):
        results = self.retriever.search(
            query,
            strategy=strategy,
            top_k=top_k,
        )

        if not results.get("grounded", False):
            return {
                "answer": "I don't know based on the available knowledge base.",
                "grounded": False,
                "top_similarity": results.get("top_similarity"),
                "sources": [],
            }

        contexts = results["documents"][0]
        sources = [
            metadata["source"]
            for metadata in results["metadatas"][0]
        ]

        answer = "Based only on the knowledge base:\n\n"
        answer += "\n\n".join(contexts)

        return {
            "answer": answer,
            "grounded": True,
            "top_similarity": results.get("top_similarity"),
            "sources": sources,"context": contexts,
        }


if __name__ == "__main__":
    generator = GroundedGenerator()

    test_queries = [
        "How quickly should a critical ticket receive a response?",
        "What is the refund policy?",
        "How should VIP customers be handled?",
        "What is the weather in Delhi today?",
    ]

    for query in test_queries:
        result = generator.answer(query, top_k=3)

        print("\n" + "=" * 60)
        print("Query:", query)
        print("Grounded:", result["grounded"])
        print("Similarity:", result["top_similarity"])
        print("Sources:", result["sources"])
        print("Answer:")
        print(result["answer"])
