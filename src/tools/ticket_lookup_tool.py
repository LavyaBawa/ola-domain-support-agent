from crewai.tools import tool

from src.tools.ticket_lookup import lookup_ticket


@tool("ticket_status_lookup")
def ticket_status_lookup(record_id: int) -> str:
    """Look up the status and escalation information for a support ticket."""

    result = lookup_ticket(record_id)

    return str(result)
