from src.crew.mock_llm import MockLLM
from crewai import Agent

from src.tools.rag_tool import knowledge_base_search
from src.tools.ticket_lookup_tool import ticket_status_lookup
mock_llm = MockLLM()

retrieval_agent = Agent(
    role="Support Knowledge Retrieval Agent",
    goal="Find accurate answers from the support knowledge base.",
    backstory="You retrieve support-policy information only from the approved knowledge base.",
    tools=[knowledge_base_search],llm=mock_llm,
    verbose=True,
)

lookup_agent = Agent(
    role="Support Ticket Lookup Agent",
    goal="Retrieve accurate ticket status and escalation information.",
    backstory="You look up support tickets using the approved ticket lookup system.",
    tools=[ticket_status_lookup],llm=mock_llm,
    verbose=True,
)

response_composer = Agent(
    role="Support Response Composer",
    goal="Compose a clear and accurate customer support response using the information provided by other agents.",
    backstory="You combine retrieved support information into a concise customer-facing response without inventing unsupported facts.",
    verbose=True,llm=mock_llm,
)
