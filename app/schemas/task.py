from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    completed: bool


class TaskRead(TaskBase):
    id: int
    completed: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

