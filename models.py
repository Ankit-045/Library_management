# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student" or "incharge"

    bookings = relationship("Booking", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="book")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    status = Column(String, default="pending")
    # "pending", "approved", "rejected", "returned"

    booked_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    book = relationship("Book", back_populates="bookings")