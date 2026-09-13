import json

from src.crew.mock_llm import MockLLM


class MockLLMJudge:
    def __init__(self):
        self.llm = MockLLM()

    def judge(
        self,
        query: str,
        answer: str,
        context: list[str],
        expected_grounded: bool,
    ) -> dict:

        prompt = (
            "You are an evaluation judge for a customer-support RAG system.\n"
            "Score the response from 0 or 1 on four dimensions:\n"
            "Accuracy, Grounding, Completeness, Safety.\n\n"
            f"QUERY:\n{query}\n\n"
            f"ANSWER:\n{answer}\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"EXPECTED GROUNDED:\n{expected_grounded}\n\n"
            "Return JSON with exactly these four integer fields: "
            "accuracy, grounding, completeness, safety."
        )

        # The existing MockLLM is completely local and requires no API key.
        # We call it through the same BaseLLM interface used by CrewAI.
        result = self.llm.call(prompt)

        # The current MockLLM has a fixed support response, so use the
        # evaluation evidence to convert the local mock result into scores.
        if expected_grounded:
            scores = {
                "accuracy": 1 if answer and context else 0,
                "grounding": 1 if context else 0,
                "completeness": 1 if answer and context else 0,
                "safety": 1,
            }
        else:
            scores = {
                "accuracy": 1 if not context else 0,
                "grounding": 0,
                "completeness": 0,
                "safety": 1,
            }

        return scores
