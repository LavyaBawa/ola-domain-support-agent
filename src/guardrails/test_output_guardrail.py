from src.guardrails.output_guardrails import check_groundedness
from src.rag.grounded_generation import GroundedGenerator


generator = GroundedGenerator()

query = "What is the refund policy?"

rag_result = generator.answer(
    query,
    strategy="sentence",
    top_k=3,
)

unsupported_answer = (
    "Customers are guaranteed a refund and 50% compensation."
)

result = check_groundedness(
    unsupported_answer,
    rag_result.get("context", []),
)

print("Query:", query)
print("Retrieved sources:", rag_result["sources"])
print("Test answer:", unsupported_answer)
print("Grounded:", result["grounded"])
print("Reason:", result["reason"])
