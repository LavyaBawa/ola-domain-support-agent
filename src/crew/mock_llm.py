from crewai.llms.base_llm import BaseLLM


class MockLLM(BaseLLM):
    def __init__(self):
        super().__init__(
            model="mock-llm",
            provider="mock",
        )

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):
        agent_role = getattr(from_agent, "role", None)
     
        if response_model is not None:
            return (
                '{"answer":"Critical tickets should receive an initial response '
                'within 1 hour and should be actively worked until service is '
                'restored or a mitigation is provided. Ticket 2 is currently '
                'Resolved, with a resolution time of 35 hours and an escalation '
                'score of 0.72. Escalation is required for this ticket.",'
                '"grounded":true,'
                '"sources":["sla_by_severity.txt","ticket_lookup"]}'
            )
        print("MOCK CALL - agent:", agent_role)

        message_text = str(messages)

        # If the tool has already produced an observation,
        # return the final answer.
        if (
            "Tool Output" in message_text
            or "Observation:" in message_text
            or "ticket_status_lookup" in message_text
            and "record_id" in message_text
            and "Result:" in message_text
        ):
            if "Support Ticket Lookup Agent" in str(agent_role):
                return (
                    "Thought: I now know the final answer.\n"
                    "Final Answer: Ticket 2 is currently Resolved. "
                    "Its resolution time is 35 hours, its escalation score "
                    "is 0.72, and escalation is required."
                )

            if "Support Knowledge Retrieval Agent" in str(agent_role):
                return (
                    "Thought: I now know the final answer.\n"
                    "Final Answer: Critical tickets should receive an "
                    "initial response within 1 hour and should be actively "
                    "worked until service is restored or a mitigation is provided."
                )
        if "Support Response Composer" in str(agent_role):
            return (
                "Thought: I have the required information from the previous agents.\n"
                "Final Answer: Critical tickets should receive an initial response "
                "within 1 hour and should be actively worked until service is restored "
                "or a mitigation is provided. Ticket 2 is currently Resolved, with a "
                "resolution time of 35 hours and an escalation score of 0.72. "
                "Escalation is required for this ticket."
            )
        # Look for the declared tool schema.
        if (
            "ticket_status_lookup" in message_text
            and '"record_id"' in message_text
        ):
            return (
                "Thought: I should look up the ticket.\n"
                "Action: ticket_status_lookup\n"
                'Action Input: {"record_id": 2}'
            )

        if (
            "knowledge_base_search" in message_text
            and '"query"' in message_text
        ):
            return (
                "Thought: I should search the knowledge base.\n"
                "Action: knowledge_base_search\n"
                'Action Input: {"query": "What is the SLA for a critical ticket?"}'
            )

        return (
            "Thought: I now know the final answer.\n"
            "Final Answer: I don't have enough information to answer."
        )

