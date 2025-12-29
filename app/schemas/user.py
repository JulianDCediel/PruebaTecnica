from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """
    Campos comunes del usuario.
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """
    Esquema para creación de usuarios.
    Incluye password (solo entrada).
    """
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    """
    Esquema para respuestas (lectura).
    NO expone password.
    """
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
