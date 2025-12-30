from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):

    password: str = Field(..., min_length=6)


class UserRead(UserBase):

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
