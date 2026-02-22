# routers/books.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user, get_current_incharge_user

router = APIRouter(prefix="/books", tags=["Books"])


# =========================
# ADD A NEW BOOK (INCHARGE ONLY)
# =========================
@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_incharge_user)
):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# =========================
# GET ALL BOOKS (ALL AUTHENTICATED USERS)
# =========================
@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    books = db.query(models.Book).all()
    return books


# =========================
# UPDATE A BOOK (INCHARGE ONLY)
# =========================
@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_incharge_user)
):
    book_query = db.query(models.Book).filter(models.Book.id == book_id)
    db_book = book_query.first()

    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    update_data = book_update.dict(exclude_unset=True)
    book_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_book)
    return db_book


# =========================
# DELETE A BOOK (INCHARGE ONLY)
# =========================
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_incharge_user)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(db_book)
    db.commit()