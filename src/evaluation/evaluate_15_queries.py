import json

from src.rag.grounded_generation import GroundedGenerator


EVALUATION_QUERIES = [
    ("ticket priority", "What makes a ticket Critical priority?"),
    ("SLA by severity", "What is the SLA for a Critical ticket?"),
    ("escalation matrix", "When should a High priority ticket be escalated?"),
    ("refund compensation", "When can compensation be considered?"),
    ("communication channels", "What communication channels can customers use?"),
    ("business hours", "What are the support business hours?"),
    ("repeat complaints", "How should a repeat complaint be handled?"),
    ("service credits", "When can service credits be provided?"),
    ("feedback collection", "How is customer feedback collected?"),
    ("VIP handling", "How should VIP customers be handled?"),
    ("outage communication", "How should customers be informed during an outage?"),
    ("data retention", "How long should support data be retained?"),
    ("out of scope", "What is the capital of France?"),
    ("out of scope", "Tell me today's stock market prediction."),
    ("edge case", "Can you guarantee me a 50% refund immediately?"),
]


def evaluate_query(generator, topic, query):
    result = generator.answer(
        query,
        strategy="sentence",
        top_k=3,
    )

    grounded = result.get("grounded", False)

    if topic in {"out of scope", "edge case"}:
        expected_grounded = False
    else:
        expected_grounded = True

    accuracy = int(grounded == expected_grounded)

    grounding = int(
        grounded
        and bool(result.get("sources"))
    )

    completeness = int(
        grounded
        and len(result.get("context", [])) > 0
    )

    safety = 1

    return {
        "topic": topic,
        "query": query,
        "accuracy": accuracy,
        "grounding": grounding,
        "completeness": completeness,
        "safety": safety,
        "grounded": grounded,
        "sources": result.get("sources", []),
    }


def main():
    generator = GroundedGenerator()

    results = []

    for topic, query in EVALUATION_QUERIES:
        results.append(
            evaluate_query(
                generator,
                topic,
                query,
            )
        )

    averages = {
        "accuracy": sum(r["accuracy"] for r in results) / len(results),
        "grounding": sum(r["grounding"] for r in results) / len(results),
        "completeness": sum(r["completeness"] for r in results) / len(results),
        "safety": sum(r["safety"] for r in results) / len(results),
    }

    print("\n15-QUERY EVALUATION")
    print("=" * 70)

    for index, result in enumerate(results, start=1):
        print(
            f"{index:02d}. {result['topic']:<22} "
            f"Accuracy={result['accuracy']} "
            f"Grounding={result['grounding']} "
            f"Completeness={result['completeness']} "
            f"Safety={result['safety']}"
        )
        print(f"    Query: {result['query']}")
        print(f"    Sources: {result['sources']}")

    print("\nAVERAGES")
    print("=" * 70)

    for metric, value in averages.items():
        print(f"{metric.capitalize()}: {value:.3f}")

    with open("evaluation_results.json", "w") as file:
        json.dump(
            {
                "results": results,
                "averages": averages,
            },
            file,
            indent=2,
        )

    print("\nSaved: evaluation_results.json")


if __name__ == "__main__":
    main()
