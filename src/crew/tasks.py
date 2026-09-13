from src.crew.schemas import SupportResponse
from crewai import Task

from src.crew.agents import retrieval_agent, lookup_agent, response_composer


retrieval_task = Task(
    description=(
        "Find the relevant support policy information for this customer question: "
        "{query}. Use the knowledge base and provide only information supported by it."
    ),
    expected_output=(
        "A concise summary of the relevant knowledge-base information, "
        "including the source of the information."
    ),
    agent=retrieval_agent,
)

from src.crew.agents import lookup_agent


lookup_task = Task(
    description=(
        "Look up support ticket {record_id} and return its current status, "
        "resolution time, escalation score, and whether escalation is required."
    ),
    expected_output=(
        "A structured summary containing the ticket status, resolution time, "
        "escalation score, and escalation decision."
    ),
    agent=lookup_agent,
)

response_task = Task(
    description=(
        "Compose the final customer-facing response using the information "
        "provided by the previous support agents. Do not invent facts or "
        "add information that is not supported by the provided results."
    ),
    expected_output=(
        "A structured support response containing the answer, whether it "
        "is grounded, and the supporting sources."
    ),
    agent=response_composer,
    output_pydantic=SupportResponse,
)
