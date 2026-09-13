from pydantic import BaseModel, Field


class SupportResponse(BaseModel):
    answer: str = Field(min_length=1)
    grounded: bool
    sources: list[str]
