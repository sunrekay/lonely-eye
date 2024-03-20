from pydantic import BaseModel


class SolutionUpdateIn(BaseModel):
    status: bool


class SolutionUpdateOut(SolutionUpdateIn):
    case_id: int
