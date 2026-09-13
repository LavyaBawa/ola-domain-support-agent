from src.guardrails.input_guardrails import guard_input
from crewai import Crew, Process

from src.crew.agents import (
    retrieval_agent,
    lookup_agent,
    response_composer,
)

from src.crew.tasks import (
    retrieval_task,
    lookup_task,
    response_task,
)


def run_crew(query, record_id):
    query = guard_input(query)
    crew = Crew(
        agents=[
            retrieval_agent,
            lookup_agent,
            response_composer,
        ],
        tasks=[
            retrieval_task,
            lookup_task,
            response_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "query": query,
            "record_id": record_id,
        }
    )

    return result


if __name__ == "__main__":
    result = run_crew(
        query="What is the SLA for a critical ticket?",
        record_id=2,
    )

    print("\nFINAL RESULT:")
    print(result)
