from fastapi import FastAPI
from database import engine
from models import Base
from routers import user, books, bookings

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(books.router)
app.include_router(bookings.router)