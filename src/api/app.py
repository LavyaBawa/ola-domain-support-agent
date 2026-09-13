import json
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from src.api.models import (
    AskRequest,
    AskResponse,
    AddDocumentRequest,
    AddDocumentResponse,
)
from src.crew.crew_runner import run_crew
from src.guardrails.input_guardrails import guard_input
from src.guardrails.output_guardrails import check_groundedness
from src.rag.grounded_generation import GroundedGenerator
from src.rag.indexer import add_document_to_collections

app = FastAPI(title="Ola Domain Support Agent")

LOG_FILE = Path("logs/requests.jsonl")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    trace_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        safe_query = guard_input(request.query)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    result = run_crew(
        query=safe_query,
        record_id=request.record_id,
    )

    response = result.pydantic

    rag_result = GroundedGenerator().answer(
        safe_query,
        strategy="sentence",
        top_k=3,
    )

    grounding_check = check_groundedness(
        response.answer,
        rag_result.get("context", []),
    )

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2,
    )

    log_entry = {
        "trace_id": trace_id,
        "query": safe_query,
        "record_id": request.record_id,
        "duration_ms": duration_ms,
        "grounded": grounding_check["grounded"],
        "sources": response.sources,
    }

    with LOG_FILE.open("a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return AskResponse(
        answer=response.answer,
        grounded=grounding_check["grounded"],
        sources=response.sources,
        trace_id=trace_id,
    )
@app.post("/add-document", response_model=AddDocumentResponse)
def add_document(request: AddDocumentRequest):
    result = add_document_to_collections(
        request.filename,
        request.content,
    )

    return AddDocumentResponse(
        message=(
            f"Document indexed successfully. "
            f"Fixed chunks: {result['fixed_chunks']}, "
            f"Sentence chunks: {result['sentence_chunks']}."
        ),
        filename=request.filename,
    )
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_json({
                "message": "WebSocket connection is working.",
                "received": message,
            })
    except WebSocketDisconnect:
        print("WebSocket client disconnected.")
