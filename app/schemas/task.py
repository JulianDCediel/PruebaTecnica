from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Campos comunes de una tarea.
    """
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """
    Esquema para crear tareas.
    """
    pass


class TaskRead(TaskBase):
    """
    Esquema para devolver tareas.
    """
    id: int
    completed: bool
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
