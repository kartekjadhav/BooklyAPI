from fastapi import FastAPI
from src.routes import book_router, user_router
from contextlib import asynccontextmanager
from src.db.db import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting 🟢")
    await init_db()
    yield
    print("Server is stopping 🔴")



app = FastAPI(lifespan=life_span, title="Bookly", description="A REST API for book review web service", version="v1")

# User auth Router
app.include_router(user_router, prefix="/api/v1/auth", tags=["auth"])

# Book Router
app.include_router(book_router, prefix="/api/v1/books", tags=["books"])