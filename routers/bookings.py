# routers/bookings.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user, get_current_incharge_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])


# =========================
# STUDENT: CREATE A BOOKING REQUEST
# =========================
@router.post("/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking_request(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if the book exists and is available
    book_to_book = db.query(models.Book).filter(models.Book.id == booking.book_id).first()
    if not book_to_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if not book_to_book.is_available:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available for booking")

    # Create the booking with 'pending' status
    new_booking = models.Booking(user_id=current_user.id, book_id=booking.book_id)
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


# =========================
# STUDENT: VIEW MY BOOKINGS
# =========================
@router.get("/me", response_model=List[schemas.BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    bookings = db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()
    return bookings


# =========================
# INCHARGE: VIEW ALL BOOKING REQUESTS
# =========================
@router.get("/", response_model=List[schemas.BookingResponseWithDetails])
def get_all_booking_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_incharge_user)
):
    bookings = db.query(models.Booking).options(
        joinedload(models.Booking.user),
        joinedload(models.Booking.book)
    ).all()
    return bookings


# =========================
# INCHARGE: UPDATE BOOKING STATUS (APPROVE/REJECT/RETURN)
# =========================
@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(
    booking_id: int,
    status_update: schemas.BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_incharge_user)
):
    booking_query = db.query(models.Booking).filter(models.Booking.id == booking_id)
    db_booking = booking_query.first()

    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    # Edge case: Can't approve a booking for a book that is no longer available
    if status_update.status == "approved":
        if not db_booking.book.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book has already been booked by someone else."
            )
        db_booking.book.is_available = False

    # If a book is returned, make it available again
    if status_update.status == "returned":
        # Only an approved booking can be returned
        if db_booking.status != "approved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only an approved booking can be marked as returned."
            )
        db_booking.book.is_available = True

    # Update the status
    db_booking.status = status_update.status

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    return db_booking