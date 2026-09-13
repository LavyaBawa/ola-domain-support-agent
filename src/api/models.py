from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str = Field(min_length=1)
    record_id: int = Field(ge=1)


class AskResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list[str]
    trace_id: str
