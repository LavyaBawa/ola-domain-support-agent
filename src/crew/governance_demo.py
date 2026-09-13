from src.crew.agents import retrieval_agent, lookup_agent


def tool_names(agent):
    return [tool.name for tool in agent.tools]


retrieval_tools = tool_names(retrieval_agent)
lookup_tools = tool_names(lookup_agent)

print("Retrieval Agent tools:", retrieval_tools)
print("Lookup Agent tools:", lookup_tools)

assert "knowledge_base_search" in retrieval_tools
assert "ticket_status_lookup" not in retrieval_tools

assert "ticket_status_lookup" in lookup_tools
assert "knowledge_base_search" not in lookup_tools

print("\nLeast-autonomy governance check passed.")
print("Only the Lookup Agent has the ticket lookup tool.")
