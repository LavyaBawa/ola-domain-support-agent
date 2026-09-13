from pydantic import BaseModel, Field


class VerdictModel(BaseModel):
    decision: str = Field(pattern="^(APPROVE|REVISE)$")
    final_response: str = Field(min_length=1)
    reason: str = Field(min_length=1)
