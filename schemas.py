from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int | None = None
    title: str = Field(..., min_length=2, max_length=200)
    description: str | None = Field(None, description="Description is not writed down")
    completed: bool = False


class STaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=200)
    description: str | None = Field(None, description ="Description is not writed down")
    completed: bool = False
