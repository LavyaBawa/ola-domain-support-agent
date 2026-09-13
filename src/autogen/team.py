import asyncio
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.teams import RoundRobinGroupChat

from src.autogen.mock_model import MockAutoGenModel
from src.autogen.schemas import VerdictModel


async def run_case(draft: str, context: str):
    model_client = MockAutoGenModel()

    reviewer = AssistantAgent(
        name="Policy_Compliance_Reviewer",
        model_client=model_client,
        system_message=(
            "You are the Policy Compliance Reviewer. "
            "Review the draft against the supplied context. "
            "If every claim is supported, say APPROVE. "
            "If any claim is unsupported, say REVISE and identify it."
        ),
    )

    editor = AssistantAgent(
        name="Final_Editor",
        model_client=model_client,
        system_message=(
            "You are the Final Editor. "
            "Use the draft, reviewer decision, and supplied context. "
            "Return a structured verdict. "
            "APPROVE means keep the draft unchanged. "
            "REVISE means remove unsupported claims."
        ),
        output_content_type=VerdictModel,
    )

    team = RoundRobinGroupChat(
        participants=[reviewer, editor],
        max_turns=2,
        custom_message_types=[StructuredMessage[VerdictModel]],
    )

    task = (
        "Review and finalize this support response.\n\n"
        f"DRAFT:\n{draft}\n\n"
        f"CONTEXT:\n{context}"
    )

    result = await team.run(task=task)

    print("\nAUTOGEN RESULT:")
    print(result)

    await model_client.close()


async def main():
    context = (
        "Critical tickets should receive an initial response within 1 hour "
        "and should be actively worked until service is restored or a "
        "mitigation is provided."
    )

    print("=" * 60)
    print("CASE 1: APPROVAL")
    print("=" * 60)

    approved_draft = (
        "Critical tickets should receive an initial response within 1 hour."
    )

    await run_case(
        draft=approved_draft,
        context=context,
    )

    print("\n" + "=" * 60)
    print("CASE 2: REVISION")
    print("=" * 60)

    unsupported_draft = (
        "Critical tickets should receive an initial response within 1 hour. "
        "Customers are guaranteed a refund."
    )

    await run_case(
        draft=unsupported_draft,
        context=context,
    )


if __name__ == "__main__":
    asyncio.run(main())
