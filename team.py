import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat

from src.autogen.mock_model import MockAutoGenModel


class PolicyComplianceReviewer:
    """
    Reviews a support draft against the supplied policy/context.
    """

    @staticmethod
    def review(draft: str, context: str) -> str:
        unsupported = [
            "guaranteed refund",
            "50% compensation",
            "free ride",
            "instant resolution",
        ]

        for claim in unsupported:
            if claim.lower() in draft.lower() and claim.lower() not in context.lower():
                return (
                    f"REJECT: The draft contains an unsupported claim: "
                    f"'{claim}'."
                )

        return "APPROVE: The draft is consistent with the supplied context."


class FinalEditor:
    """
    Produces the final customer-facing response after policy review.
    """

    @staticmethod
    def edit(draft: str, review: str, context: str) -> str:
        if review.startswith("APPROVE"):
            return draft

        return (
            "The original draft contained information that was not supported "
            "by the available policy context. Please rely only on the verified "
            "knowledge-base information."
        )


async def run_autogen_team(draft: str, context: str):
    model_client = MockAutoGenModel()

    reviewer = AssistantAgent(
        name="Policy-Compliance-Reviewer",
        model_client=model_client,
        system_message=(
            "You are the Policy-Compliance-Reviewer. "
            "Review the support draft against the supplied context. "
            "Identify unsupported claims. "
            "Reply with APPROVE when the draft is supported."
        ),
    )

    editor = AssistantAgent(
        name="Final-Editor",
        model_client=model_client,
        system_message=(
            "You are the Final-Editor. "
            "Produce a final response based only on the draft, review, "
            "and supplied context. Remove unsupported claims."
        ),
    )

    team = RoundRobinGroupChat(
        [reviewer, editor],
        max_turns=2,
    )

    task = (
        "Review and finalize this customer-support response.\n\n"
        f"DRAFT:\n{draft}\n\n"
        f"CONTEXT:\n{context}"
    )

    result = await team.run(task=task)

    await model_client.close()

    return result


if __name__ == "__main__":
    draft = (
        "Critical tickets should receive an initial response within 1 hour. "
        "Customers are guaranteed a refund."
    )

    context = (
        "Critical tickets should receive an initial response within 1 hour "
        "and should be actively worked until service is restored or a "
        "mitigation is provided."
    )

    result = asyncio.run(
        run_autogen_team(
            draft=draft,
            context=context,
        )
    )

    print("\nAUTOGEN RESULT:")
    print(result)
