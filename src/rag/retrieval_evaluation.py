from src.rag.retrieval import Retriever


TEST_CASES = [
    (
        "How quickly should a critical ticket receive a response?",
        "sla_by_severity.txt",
    ),
    (
        "What are the rules for refunds and compensation?",
        "refund_compensation.txt",
    ),
    (
        "What are the customer support business hours?",
        "business_hours.txt",
    ),
    (
        "How should VIP customers be handled?",
        "vip_handling.txt",
    ),
    (
        "How long should customer data be retained?",
        "data_retention.txt",
    ),
]


def evaluate_strategy(retriever, strategy):
    precision_values = []
    recall_values = []

    print("\n" + "=" * 60)
    print("Strategy:", strategy)
    print("=" * 60)

    for query, expected_source in TEST_CASES:
        results = retriever.search(
            query,
            strategy=strategy,
            top_k=3,
        )

        retrieved_sources = []

        for metadata in results["metadatas"][0]:
            source = metadata["source"]

            if source not in retrieved_sources:
                retrieved_sources.append(source)

        relevant_retrieved = int(expected_source in retrieved_sources)

        precision = relevant_retrieved / len(retrieved_sources)

        recall = relevant_retrieved / 1

        precision_values.append(precision)
        recall_values.append(recall)

        print("\nQuery:", query)
        print("Expected:", expected_source)
        print("Retrieved:", retrieved_sources)
        print(
            f"Precision: {relevant_retrieved}/{len(retrieved_sources)}"
            f" = {precision:.3f}"
        )
        print(
            f"Recall: {relevant_retrieved}/1"
            f" = {recall:.3f}"
        )

    average_precision = sum(precision_values) / len(precision_values)
    average_recall = sum(recall_values) / len(recall_values)

    print("\nAverage precision:", round(average_precision, 3))
    print("Average recall:", round(average_recall, 3))

    return average_precision, average_recall


if __name__ == "__main__":
    retriever = Retriever()

    fixed_precision, fixed_recall = evaluate_strategy(
        retriever,
        "fixed",
    )

    sentence_precision, sentence_recall = evaluate_strategy(
        retriever,
        "sentence",
    )

    print("\n" + "=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)

    print(
        f"Fixed-overlap: precision={fixed_precision:.3f}, "
        f"recall={fixed_recall:.3f}"
    )

    print(
        f"Sentence-based: precision={sentence_precision:.3f}, "
        f"recall={sentence_recall:.3f}"
    )
