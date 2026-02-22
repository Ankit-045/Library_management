# schemas.py

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Annotated
from datetime import datetime


# =========================
# USER SCHEMAS
# =========================

NameField = Annotated[
    str,
    Field(min_length=2, max_length=50, description="User full name")
]

PasswordField = Annotated[
    str,
    Field(min_length=6, max_length=128, description="User password")
]

RoleField = Annotated[
    str,
    Field(pattern="^(student|incharge)$", description="Role must be student or incharge")
]


class UserCreate(BaseModel):
    name: NameField
    email: EmailStr
    password: PasswordField
    role: RoleField


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordField


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# =========================
# BOOK SCHEMAS
# =========================

TitleField = Annotated[
    str,
    Field(min_length=1, max_length=100, description="Book title")
]

AuthorField = Annotated[
    str,
    Field(min_length=2, max_length=100, description="Book author name")
]


class BookCreate(BaseModel):
    title: TitleField
    author: AuthorField


class BookUpdate(BaseModel):
    title: Optional[TitleField] = None
    author: Optional[AuthorField] = None
    is_available: Optional[bool] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool

    class Config:
        from_attributes = True

# =========================
# BOOKING SCHEMAS
# =========================

BookIdField = Annotated[
    int,
    Field(gt=0, description="Book ID must be greater than 0")
]


class BookingCreate(BaseModel):
    book_id: BookIdField


class BookingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str
    booked_at: datetime

    class Config:
        from_attributes = True


class BookingResponseWithDetails(BookingResponse):
    user: UserResponse
    book: BookResponse

    class Config:
        from_attributes = True


class BookingStatusUpdate(BaseModel):
    status: str

    @validator('status')
    def status_must_be_valid(cls, v):
        if v not in ['approved', 'rejected', 'returned']:
            raise ValueError('Status must be one of: approved, rejected, returned')
        return v