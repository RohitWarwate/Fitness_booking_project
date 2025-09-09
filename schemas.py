# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ClassCreate(BaseModel):
    name: str
    dateTime: datetime  # Expect ISO with timezone or naive -> will be treated as IST
    instructor: str
    availableSlots: int

class ClassOut(BaseModel):
    id: int
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int

    class Config:
        orm_mode = True

class BookRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str
    created_at: datetime

    class Config:
        orm_mode = True
