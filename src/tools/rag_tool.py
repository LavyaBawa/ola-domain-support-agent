from crewai.tools import tool

from src.rag.grounded_generation import GroundedGenerator


generator = GroundedGenerator()


@tool("knowledge_base_search")
def knowledge_base_search(query: str) -> str:
    """Search the support knowledge base and return grounded information."""

    result = generator.answer(
        query,
        strategy="sentence",
        top_k=3,
    )

    if not result["grounded"]:
        return "I don't know based on the available knowledge base."

    return result["answer"]
