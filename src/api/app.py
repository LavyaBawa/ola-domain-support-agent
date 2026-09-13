from fastapi import FastAPI
from src.api.models import AskRequest, AskResponse
from src.crew.crew_runner import run_crew
app = FastAPI(title="Ola Domain Support Agent")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    result = run_crew(
        query=request.query,
        record_id=request.record_id,
    )

    response = result.pydantic

    return AskResponse(
        answer=response.answer,
        grounded=response.grounded,
        sources=response.sources,
        trace_id="test-trace",
    )
